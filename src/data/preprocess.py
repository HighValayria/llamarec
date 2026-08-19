"""STEP 2 实现：交互读取与用户序列构造。

MVP 的主数据来源是 full_sequence。positive_sequence 只作为辅助统计产物保留，
不参与 MVP split，也不决定 N 的 history 或 target。
"""

from collections import defaultdict
import csv
import json
from typing import Any

try:
    from .config import (
        open_text_auto,
        resolve_configured_output_path,
        resolve_dataset_paths,
    )
except ImportError:  # 允许在 src/data 目录内直接调试单个模块文件。
    from config import open_text_auto, resolve_configured_output_path, resolve_dataset_paths


def load_ratings(dataset_key: str, config: dict[str, Any]) -> list[dict[str, Any]]:
    """读取评分/交互记录并标准化字段名。"""

    return list(iter_ratings(dataset_key, config))


def iter_ratings(dataset_key: str, config: dict[str, Any]):
    """逐条读取评分/交互记录，避免大数据集一次性进入内存。"""

    paths = resolve_dataset_paths(config, dataset_key)
    movies = load_movies(dataset_key, config)
    prompt_item_type = (
        config.get("raw_files", {})
        .get(dataset_key, {})
        .get("prompt_item_type", "movie")
    )
    ratings_format = paths["ratings_format"]

    if ratings_format == "tab_separated_no_header":
        row_iter = _iter_movielens_100k_ratings(paths["ratings_path"])
    elif ratings_format == "csv_with_header":
        row_iter = _iter_movielens_csv_ratings(paths["ratings_path"])
    elif ratings_format == "double_colon_no_header":
        row_iter = _iter_movielens_1m_ratings(paths["ratings_path"])
    elif ratings_format == "amazon_reviews_2023_csv":
        row_iter = _iter_amazon_reviews_2023_ratings(paths["ratings_path"])
    else:
        raise ValueError(f"暂不支持的 ratings_format: {ratings_format}")

    for row in row_iter:
        movie_meta = movies.get(row["movie_id"], {})
        if not _valid_title(movie_meta.get("title")):
            continue
        # prompt 当前只需要 title。genres 不参与 MVP 任务语义，避免在 32M 中重复膨胀。
        row["title"] = str(movie_meta.get("title"))
        row["item_type"] = str(prompt_item_type)
        yield row


def iter_user_rating_groups(dataset_key: str, config: dict[str, Any]):
    """按 user_id 连续分组流式产出评分。

    MovieLens 32M 的 ratings.csv 按 userId 成块排列。若发现同一 user_id
    在文件后面再次出现，立即报错，避免错误地把一个用户拆成多个时间序列。
    """

    completed_users = set()
    current_user_id = None
    current_rows = []

    for row in iter_ratings(dataset_key, config):
        user_id = row["user_id"]
        if current_user_id is None:
            current_user_id = user_id

        if user_id != current_user_id:
            completed_users.add(current_user_id)
            yield current_user_id, current_rows
            if user_id in completed_users:
                raise ValueError(
                    f"ratings 文件不是按 user_id 连续分组: {user_id}"
                )
            current_user_id = user_id
            current_rows = []

        current_rows.append(row)

    if current_user_id is not None:
        yield current_user_id, current_rows


def load_movies(dataset_key: str, config: dict[str, Any]) -> dict[str, dict[str, str]]:
    """读取 item 元数据，并以内部 ``movie_id`` 兼容既有链路。"""

    paths = resolve_dataset_paths(config, dataset_key)
    movies_format = paths["movies_format"]

    if movies_format == "pipe_separated_latin1":
        return _read_movielens_100k_movies(paths["movies_path"])
    if movies_format == "csv_with_header":
        return _read_movielens_csv_movies(paths["movies_path"])
    if movies_format == "double_colon_movies_dat":
        return _read_movielens_1m_movies(paths["movies_path"])
    if movies_format == "amazon_reviews_2023_parquet_metadata":
        return _read_amazon_reviews_2023_metadata(paths["movies_path"])

    raise ValueError(f"暂不支持的 movies_format: {movies_format}")


def build_user_sequences(
    ratings: list[dict[str, Any]],
    positive_rating_threshold: float,
) -> tuple[dict[str, list[dict[str, Any]]], dict[str, list[dict[str, Any]]]]:
    """构造 full_sequence 和辅助 positive_sequence。"""

    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for rating in ratings:
        grouped[rating["user_id"]].append(rating)

    full_sequences: dict[str, list[dict[str, Any]]] = {}
    positive_sequences: dict[str, list[dict[str, Any]]] = {}

    for user_id, user_ratings in grouped.items():
        # 先按真实时间排序；movie_id 只作为同 timestamp 时的稳定 tie-breaker。
        interactions = sorted(
            user_ratings,
            key=lambda item: (item["timestamp"], item["movie_id"]),
        )
        indexed_interactions = []
        for sequence_index, interaction in enumerate(interactions):
            # sequence_index 后续用于判断 target 是否误入自身 history。
            indexed = dict(interaction)
            indexed["sequence_index"] = sequence_index
            indexed_interactions.append(indexed)

        full_sequences[user_id] = indexed_interactions
        positive_sequences[user_id] = [
            interaction
            for interaction in indexed_interactions
            if interaction["rating"] >= positive_rating_threshold
        ]

    return full_sequences, positive_sequences


def write_sequence_outputs(
    dataset_key: str,
    full_sequences: dict[str, list[dict[str, Any]]],
    positive_sequences: dict[str, list[dict[str, Any]]],
    config: dict[str, Any],
) -> None:
    """写出 full_sequence 和辅助 positive_sequence。"""

    output_dir = resolve_dataset_paths(config, dataset_key)["output_dir"]
    output_dir.mkdir(parents=True, exist_ok=True)

    _write_jsonl(
        resolve_configured_output_path(config, dataset_key, "full_sequences"),
        full_sequences,
    )
    _write_jsonl(
        resolve_configured_output_path(
            config,
            dataset_key,
            "positive_sequences_auxiliary",
        ),
        positive_sequences,
    )


def _read_movielens_100k_ratings(ratings_path) -> list[dict[str, Any]]:
    return list(_iter_movielens_100k_ratings(ratings_path))


def _read_movielens_csv_ratings(ratings_path) -> list[dict[str, Any]]:
    return list(_iter_movielens_csv_ratings(ratings_path))


def _iter_movielens_100k_ratings(ratings_path):
    with ratings_path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            user_id, movie_id, rating, timestamp = line.rstrip("\n").split("\t")[:4]
            yield {
                "user_id": user_id,
                "movie_id": movie_id,
                "rating": float(rating),
                "timestamp": int(timestamp),
            }


def _iter_movielens_csv_ratings(ratings_path):
    with ratings_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            yield {
                "user_id": _first_present(row, "user_id", "userId"),
                "movie_id": _first_present(row, "movie_id", "movieId"),
                "rating": float(_first_present(row, "rating")),
                "timestamp": int(float(_first_present(row, "timestamp"))),
            }


def _iter_movielens_1m_ratings(ratings_path):
    """读取 MovieLens-1M 的 ``ratings.dat``。"""

    with ratings_path.open("r", encoding="latin-1") as handle:
        for line in handle:
            if not line.strip():
                continue
            user_id, movie_id, rating, timestamp = _split_double_colon(line, 4)[:4]
            yield {
                "user_id": user_id,
                "movie_id": movie_id,
                "rating": float(rating),
                "timestamp": int(timestamp),
            }


def _iter_amazon_reviews_2023_ratings(ratings_path):
    """读取 Amazon Reviews 2023 interaction CSV。

    外部 item id 是 ``parent_asin``；内部保留为 ``movie_id``，以复用现有
    split、candidate、training、inference、SASRec 代码。
    """

    with ratings_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            user_id = _first_present(row, "user_id", "reviewerID", "reviewer_id")
            parent_asin = _first_present(row, "parent_asin", "asin", "item_id")
            rating = _first_present(row, "rating", "overall")
            timestamp = _first_present(row, "timestamp", "unixReviewTime")
            yield {
                "user_id": str(user_id),
                "movie_id": str(parent_asin),
                "parent_asin": str(parent_asin),
                "rating": float(rating),
                "timestamp": _parse_amazon_timestamp(timestamp),
            }


def _read_movielens_100k_movies(movies_path) -> dict[str, dict[str, str]]:
    movies = {}
    with movies_path.open("r", encoding="latin-1") as handle:
        for line in handle:
            if not line.strip():
                continue
            parts = line.rstrip("\n").split("|")
            movies[parts[0]] = {"movie_id": parts[0], "title": parts[1], "genres": ""}
    return movies


def _read_movielens_csv_movies(movies_path) -> dict[str, dict[str, str]]:
    movies = {}
    with movies_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            movie_id = _first_present(row, "movie_id", "movieId")
            movies[movie_id] = {
                "movie_id": movie_id,
                "title": _first_present(row, "title"),
                "genres": row.get("genres", ""),
            }
    return movies


def _read_movielens_1m_movies(movies_path) -> dict[str, dict[str, str]]:
    """读取 MovieLens-1M 的 ``movies.dat``。"""

    movies = {}
    with movies_path.open("r", encoding="latin-1") as handle:
        for line in handle:
            if not line.strip():
                continue
            movie_id, title, genres = _split_double_colon(line, 3)[:3]
            movies[movie_id] = {
                "movie_id": movie_id,
                "title": title,
                "genres": genres,
            }
    return movies


def _read_amazon_reviews_2023_metadata(metadata_path) -> dict[str, dict[str, str]]:
    """读取 Amazon Reviews 2023 parquet metadata shard。"""

    try:
        import pandas as pd
    except ImportError as exc:  # pragma: no cover - depends on runtime packaging.
        raise RuntimeError(
            "读取 Amazon parquet metadata 需要 pandas 和 pyarrow/fastparquet。"
        ) from exc

    paths = _amazon_metadata_files(metadata_path)
    movies: dict[str, dict[str, str]] = {}
    for path in paths:
        try:
            frame = pd.read_parquet(path, columns=["parent_asin", "title"])
        except Exception as exc:  # pragma: no cover - exercised in integration env.
            raise RuntimeError(
                f"无法读取 Amazon parquet metadata: {path}. "
                "请确认环境安装了 pyarrow 或 fastparquet。"
            ) from exc

        for row in frame.itertuples(index=False):
            parent_asin = str(getattr(row, "parent_asin", "") or "").strip()
            title = str(getattr(row, "title", "") or "").strip()
            if not parent_asin or not _valid_title(title):
                continue
            movies[parent_asin] = {
                "movie_id": parent_asin,
                "parent_asin": parent_asin,
                "title": title,
                "genres": "",
            }
    return movies


def _amazon_metadata_files(metadata_path) -> list[Any]:
    path = metadata_path
    if path.is_dir():
        files = sorted(path.glob("*.parquet"))
    else:
        files = [path]
    if not files:
        raise FileNotFoundError(f"Amazon metadata parquet 文件不存在: {path}")
    return files


def _first_present(row: dict[str, Any], *keys: str) -> str:
    for key in keys:
        value = row.get(key)
        if value is not None:
            return value
    raise KeyError(f"缺少字段，候选字段: {keys}")


def _parse_amazon_timestamp(value: Any) -> int:
    numeric = int(float(str(value).strip()))
    if numeric > 10_000_000_000:
        return numeric // 1000
    return numeric


def _valid_title(value: Any) -> bool:
    if value is None:
        return False
    title = str(value).strip()
    return bool(title) and title.lower() not in {"nan", "none", "null"}


def _split_double_colon(line: str, expected_fields: int) -> list[str]:
    parts = line.rstrip("\n").split("::")
    if len(parts) < expected_fields:
        raise ValueError(
            f"MovieLens-1M 行字段数不足，期望至少 {expected_fields} 个字段: {line!r}"
        )
    return parts


def _write_jsonl(path, sequences: dict[str, list[dict[str, Any]]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open_text_auto(path, "wt", encoding="utf-8") as handle:
        for user_id, interactions in sequences.items():
            record = {"user_id": user_id, "interactions": interactions}
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")
