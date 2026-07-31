"""STEP 2 实现：数据统计与人工检查产物。

positive_sequence 只作为辅助统计字段出现；MVP 的 split、N target 和 N history
都必须以 full_sequence 为准。
"""

from __future__ import annotations

from collections import Counter
import json
from typing import Any

try:
    from .config import (
        get_positive_rating_threshold,
        resolve_configured_output_path,
        resolve_dataset_paths,
    )
except ImportError:  # 允许在 src/data 目录内直接调试单个模块文件。
    from config import (
        get_positive_rating_threshold,
        resolve_configured_output_path,
        resolve_dataset_paths,
    )


def compute_dataset_stats(
    full_sequences: dict[str, list[dict[str, Any]]],
    positive_sequences: dict[str, list[dict[str, Any]]],
    split: dict[str, Any],
    config: dict[str, Any],
    preference_samples: list[dict[str, Any]] | None = None,
    next_item_samples: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """计算 STEP 2 必需的基础统计。"""

    threshold = get_positive_rating_threshold(config)
    rating_distribution: Counter[str] = Counter()
    label_distribution: Counter[str] = Counter()
    movie_ids = set()
    full_lengths = []
    positive_lengths = []

    for user_id, interactions in full_sequences.items():
        full_lengths.append(len(interactions))
        positive_lengths.append(len(positive_sequences.get(user_id, [])))
        for interaction in interactions:
            rating_distribution[str(interaction["rating"])] += 1
            label = "Yes" if interaction["rating"] >= threshold else "No"
            label_distribution[label] += 1
            movie_ids.add(str(interaction["movie_id"]))

    preference_sample_count = _count_samples_by_split(preference_samples)
    next_item_sample_count = _count_samples_by_split(next_item_samples)

    y_user_ids = set(split.get("y", {}).get("users", {}))
    n_user_ids = set(split.get("n", {}).get("users", {}))
    n_skipped_user_ids = set(full_sequences) - n_user_ids

    return {
        "user_count": len(full_sequences),
        "movie_count": len(movie_ids),
        "interaction_count": sum(full_lengths),
        "rating_distribution": dict(sorted(rating_distribution.items())),
        "yes_no_label_distribution": dict(label_distribution),
        "full_sequence_length": _length_summary(full_lengths),
        "positive_sequence_length_auxiliary": _length_summary(positive_lengths),
        "timestamp_bucket_size_distribution": _normalized_bucket_distribution(
            split.get("bucket_size_distribution", {})
        ),
        "singleton_timestamp_bucket_ratio": _singleton_bucket_ratio(
            split.get("bucket_size_distribution", {})
        ),
        "split_user_count": split.get("user_count", {}),
        "y_split_user_count": split.get("y", {}).get("user_count", {}),
        "n_split_user_count": split.get("n", {}).get("user_count", {}),
        "y_sample_count": preference_sample_count,
        "n_sample_count": next_item_sample_count,
        "preference_sample_count": preference_sample_count,
        "next_item_sample_count": next_item_sample_count,
        "y_user_count_by_split": _count_users_by_split(preference_samples),
        "n_user_count_by_split": _count_users_by_split(next_item_samples),
        "legal_next_item_sample_count_per_user": _legal_n_count_per_user(split),
        "legal_next_item_sample_count_summary": _length_summary(
            list(_legal_n_count_per_user(split).values())
        ),
        "n_skipped_user_count_insufficient_legal_samples": split.get("n", {})
        .get("user_count", {})
        .get("skipped_by_reason", {})
        .get("too_few_legal_next_item_samples", 0),
        "n_retained_vs_skipped_user_comparison": {
            "retained": _summarize_user_subset(full_sequences, n_user_ids),
            "skipped": _summarize_user_subset(full_sequences, n_skipped_user_ids),
        },
        "split_source_sequence": split.get("source_sequence"),
        "timestamp_tie_policy": split.get("timestamp_tie_policy"),
    }


def write_stats(dataset_key: str, stats: dict[str, Any], config: dict[str, Any]) -> None:
    """写出 stats.json。"""

    output_dir = resolve_dataset_paths(config, dataset_key)["output_dir"]
    output_dir.mkdir(parents=True, exist_ok=True)
    stats_path = resolve_configured_output_path(config, dataset_key, "stats")
    stats_path.parent.mkdir(parents=True, exist_ok=True)
    with stats_path.open("w", encoding="utf-8") as handle:
        json.dump(stats, handle, ensure_ascii=False, indent=2)


def write_inspection_samples(
    dataset_key: str,
    samples: list[dict[str, Any]],
    config: dict[str, Any],
    limit: int = 20,
) -> None:
    """写出至少用于人工检查的样本片段。"""

    output_dir = resolve_dataset_paths(config, dataset_key)["output_dir"]
    output_dir.mkdir(parents=True, exist_ok=True)
    inspection_path = resolve_configured_output_path(
        config,
        dataset_key,
        "inspection_samples",
    )
    inspection_path.parent.mkdir(parents=True, exist_ok=True)
    with inspection_path.open("w", encoding="utf-8") as handle:
        handle.write("# STEP 2 人工检查样本\n\n")
        for index, sample in enumerate(samples[:limit], start=1):
            handle.write(f"## Sample {index}\n\n")
            handle.write("```json\n")
            handle.write(json.dumps(sample, ensure_ascii=False, indent=2))
            handle.write("\n```\n\n")


def _summarize_user_subset(
    full_sequences: dict[str, list[dict[str, Any]]],
    user_ids: set[str],
) -> dict[str, Any]:
    lengths = []
    rating_distribution: Counter[str] = Counter()

    for user_id in user_ids:
        interactions = full_sequences[user_id]
        lengths.append(len(interactions))
        for interaction in interactions:
            rating_distribution[str(interaction["rating"])] += 1

    return {
        "user_count": len(user_ids),
        "interaction_count": sum(lengths),
        "interaction_length": _length_summary(lengths),
        "rating_distribution": dict(sorted(rating_distribution.items())),
    }


def _legal_n_count_per_user(split: dict[str, Any]) -> dict[str, int]:
    return {
        user_id: int(info["legal_sample_count"])
        for user_id, info in split.get("n", {}).get("users", {}).items()
    }


def _normalized_bucket_distribution(raw_distribution: dict[str, int]) -> dict[str, int]:
    return {
        "size=1": int(raw_distribution.get("size=1", 0)),
        "size=2": int(raw_distribution.get("size=2", 0)),
        "size=3": int(raw_distribution.get("size=3", 0)),
        "size>=4": int(raw_distribution.get("size>=4", 0)),
    }


def _singleton_bucket_ratio(raw_distribution: dict[str, int]) -> float | None:
    normalized = _normalized_bucket_distribution(raw_distribution)
    total = sum(normalized.values())
    if total == 0:
        return None
    return normalized["size=1"] / total


def _length_summary(values: list[int]) -> dict[str, float | int | None]:
    if not values:
        return {
            "min": None,
            "p50": None,
            "p90": None,
            "p95": None,
            "max": None,
            "mean": None,
        }

    ordered = sorted(values)
    return {
        "min": ordered[0],
        "p50": _percentile(ordered, 0.50),
        "p90": _percentile(ordered, 0.90),
        "p95": _percentile(ordered, 0.95),
        "max": ordered[-1],
        "mean": sum(ordered) / len(ordered),
    }


def _percentile(ordered_values: list[int], ratio: float) -> int:
    index = round((len(ordered_values) - 1) * ratio)
    return ordered_values[index]


def _count_samples_by_split(
    samples: list[dict[str, Any]] | None,
) -> dict[str, int] | None:
    if samples is None:
        return None

    counter: Counter[str] = Counter(sample["split"] for sample in samples)
    return {
        "train": counter.get("train", 0),
        "validation": counter.get("validation", 0),
        "test": counter.get("test", 0),
    }


def _count_users_by_split(
    samples: list[dict[str, Any]] | None,
) -> dict[str, int] | None:
    if samples is None:
        return None

    users_by_split: dict[str, set[str]] = {
        "train": set(),
        "validation": set(),
        "test": set(),
    }
    for sample in samples:
        users_by_split[sample["split"]].add(str(sample["user_id"]))

    return {
        split_name: len(user_ids)
        for split_name, user_ids in users_by_split.items()
    }
