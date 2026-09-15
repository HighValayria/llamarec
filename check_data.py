from pathlib import Path
import pandas as pd
import numpy as np

ROOT = Path("data/raw/amazon_reviews_2023/musical_instruments")

INTERACTION_FILE = ROOT / "interactions" / "Musical_Instruments.csv"
META_DIR = ROOT / "metadata"


# ============================================================
# 1. 读取 interaction
# ============================================================

print("=" * 100)
print("1. INTERACTIONS")
print("=" * 100)

df = pd.read_csv(INTERACTION_FILE)

print("shape:", df.shape)
print("columns:", df.columns.tolist())
print()
print(df.head())
print()
print(df.dtypes)


required_interaction_cols = {
    "user_id",
    "parent_asin",
    "rating",
    "timestamp",
}

missing = required_interaction_cols - set(df.columns)

print("\nrequired columns missing:", missing)

if missing:
    raise RuntimeError(
        f"Interaction 文件缺少必要字段: {missing}"
    )


# ============================================================
# 2. interaction 基本统计
# ============================================================

print("\n" + "=" * 100)
print("2. INTERACTION STATS")
print("=" * 100)

print("rows:", len(df))
print("users:", df["user_id"].nunique())
print("items:", df["parent_asin"].nunique())

print("\nrating distribution:")
print(df["rating"].value_counts(dropna=False).sort_index())

print("\nnull counts:")
print(
    df[
        ["user_id", "parent_asin", "rating", "timestamp"]
    ].isna().sum()
)

print("\nduplicated rows:", df.duplicated().sum())

print(
    "duplicated user-item-timestamp:",
    df.duplicated(
        subset=["user_id", "parent_asin", "timestamp"]
    ).sum()
)


# ============================================================
# 3. rating 检查
# ============================================================

rating = pd.to_numeric(df["rating"], errors="coerce")

print("\nrating min:", rating.min())
print("rating max:", rating.max())
print("non-numeric rating:", rating.isna().sum())

positive = (rating >= 4).mean()

print("rating >= 4 ratio:", positive)
print("rating < 4 ratio:", 1 - positive)


# ============================================================
# 4. 检查 5-core
# ============================================================

print("\n" + "=" * 100)
print("3. 5-CORE CHECK")
print("=" * 100)

user_counts = df.groupby("user_id").size()
item_counts = df.groupby("parent_asin").size()

print("min interactions / user:", user_counts.min())
print("median interactions / user:", user_counts.median())
print("mean interactions / user:", user_counts.mean())
print("max interactions / user:", user_counts.max())

print()

print("min interactions / item:", item_counts.min())
print("median interactions / item:", item_counts.median())
print("mean interactions / item:", item_counts.mean())
print("max interactions / item:", item_counts.max())

print("\nusers with <5 interactions:", (user_counts < 5).sum())
print("items with <5 interactions:", (item_counts < 5).sum())


# ============================================================
# 5. timestamp 检查
# ============================================================

print("\n" + "=" * 100)
print("4. TIMESTAMP CHECK")
print("=" * 100)

ts = pd.to_numeric(df["timestamp"], errors="coerce")

print("non-numeric timestamp:", ts.isna().sum())
print("timestamp min:", ts.min())
print("timestamp max:", ts.max())
print("unique timestamps:", ts.nunique())

median_ts = ts.dropna().median()

# Amazon 数据可能是 ms，也可能已经处理成 sec
if median_ts > 1e11:
    dt = pd.to_datetime(ts, unit="ms", errors="coerce")
else:
    dt = pd.to_datetime(ts, unit="s", errors="coerce")

print("datetime range:")
print(dt.min(), "->", dt.max())


# ============================================================
# 6. timestamp tie
# ============================================================

bucket_sizes = (
    df.groupby(["user_id", "timestamp"])
      .size()
      .rename("bucket_size")
)

print("\nuser-timestamp buckets:", len(bucket_sizes))
print("multi-item timestamp buckets:", (bucket_sizes > 1).sum())
print(
    "multi-item bucket ratio:",
    (bucket_sizes > 1).mean()
)

print("\nbucket size distribution:")
print(bucket_sizes.value_counts().sort_index().head(20))


# ============================================================
# 7. metadata
# ============================================================

print("\n" + "=" * 100)
print("5. METADATA")
print("=" * 100)

meta_files = sorted(META_DIR.glob("*.parquet"))

print("metadata parquet files:", len(meta_files))

if not meta_files:
    raise RuntimeError("metadata 目录中没有 parquet 文件")

meta_parts = []

for p in meta_files:
    x = pd.read_parquet(p)
    print(p.name, x.shape)
    meta_parts.append(x)

meta = pd.concat(meta_parts, ignore_index=True)

print("\nmetadata shape:", meta.shape)
print("metadata columns:", meta.columns.tolist())
print()
print(meta.head())


required_meta_cols = {
    "parent_asin",
    "title",
}

missing_meta = required_meta_cols - set(meta.columns)

print("\nmetadata required columns missing:", missing_meta)

if missing_meta:
    raise RuntimeError(
        f"Metadata 缺少字段: {missing_meta}"
    )


# ============================================================
# 8. metadata title
# ============================================================

meta["title"] = meta["title"].astype("string")

valid_title = (
    meta["title"].notna()
    & (meta["title"].str.strip() != "")
)

print("\nmetadata rows:", len(meta))
print("metadata unique parent_asin:", meta["parent_asin"].nunique())
print("valid title ratio:", valid_title.mean())

print(
    "duplicate parent_asin rows:",
    meta.duplicated(subset=["parent_asin"]).sum()
)


# ============================================================
# 9. interaction / metadata join coverage
# ============================================================

print("\n" + "=" * 100)
print("6. JOIN COVERAGE")
print("=" * 100)

meta_simple = (
    meta.loc[valid_title, ["parent_asin", "title"]]
        .drop_duplicates("parent_asin")
)

interaction_items = set(df["parent_asin"].dropna().unique())
metadata_items = set(meta_simple["parent_asin"].dropna().unique())

matched = interaction_items & metadata_items
missing_items = interaction_items - metadata_items

print("interaction unique items:", len(interaction_items))
print("items with metadata title:", len(matched))
print(
    "item title coverage:",
    len(matched) / len(interaction_items)
)

print("items without title:", len(missing_items))

print("\nexample missing items:")
print(list(missing_items)[:20])


# ============================================================
# 10. Y/N temporal feasibility
# ============================================================

print("\n" + "=" * 100)
print("7. STRICT TEMPORAL FEASIBILITY")
print("=" * 100)

# 每个 user + timestamp 是一个 timestamp bucket。
# history 只允许 timestamp < target_timestamp。

bucket_df = (
    df.groupby(["user_id", "timestamp"])
      .size()
      .rename("bucket_size")
      .reset_index()
      .sort_values(["user_id", "timestamp"])
)

bucket_df["bucket_index"] = (
    bucket_df.groupby("user_id").cumcount()
)

# bucket_index > 0 意味着 target 前至少有一个更早 timestamp
has_history = bucket_df["bucket_index"] > 0

# Y:
# 同一个 timestamp bucket 内可以有多个 Y target，
# 只要存在严格更早 history。
legal_y = bucket_df.loc[has_history, "bucket_size"].sum()

# N:
# 下一 timestamp bucket 必须只有一个 interaction
legal_n_mask = has_history & (bucket_df["bucket_size"] == 1)

legal_n = legal_n_mask.sum()

legal_n_per_user = (
    bucket_df.assign(legal_n=legal_n_mask.astype(int))
             .groupby("user_id")["legal_n"]
             .sum()
)

print("approx legal strict-Y targets:", int(legal_y))
print("legal strict-N targets:", int(legal_n))

print(
    "users with >=1 legal N target:",
    int((legal_n_per_user >= 1).sum())
)

print(
    "users with >=2 legal N targets:",
    int((legal_n_per_user >= 2).sum())
)

print(
    "users with >=3 legal N targets:",
    int((legal_n_per_user >= 3).sum())
)

# 按你目前 N protocol：
# last legal N -> test
# second last -> valid
# earlier -> train
# 因此 >=3 最理想，可以同时产生 train/valid/test。


print("\n" + "=" * 100)
print("CHECK FINISHED")
print("=" * 100)