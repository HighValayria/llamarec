"""STEP 2 端到端入口：构建 MovieLens 数据层产物。

本脚本只做本地 CPU 数据处理，不加载 LLM，不启动训练。生成 MovieLens-100K
产物后应先人工检查 inspection samples，再处理 MovieLens-32M。
"""

from __future__ import annotations

import argparse
from collections import Counter
from contextlib import ExitStack
import json
from pathlib import Path
from random import Random
from typing import Any

try:
    from .build_preference import (
        build_preference_samples,
        validate_preference_sample,
        write_preference_samples,
    )
    from .build_next_item import (
        build_next_item_samples,
        validate_next_item_sample,
        write_next_item_samples,
    )
    from .config import get_positive_rating_threshold, load_experiment_config
    from .config import (
        dataset_uses_gzip_outputs,
        open_text_auto,
        resolve_configured_output_path,
    )
    from .preprocess import (
        build_user_sequences,
        iter_user_rating_groups,
        load_movies,
        load_ratings,
        write_sequence_outputs,
    )
    from .split import (
        build_full_sequence_leave_two_out_split,
        validate_split_no_leakage,
        write_split,
    )
    from .stats import (
        compute_dataset_stats,
        write_inspection_samples,
        write_stats,
    )
except ImportError:  # 允许执行 python src/data/build_step2.py 进行本地调试。
    from build_preference import (
        build_preference_samples,
        validate_preference_sample,
        write_preference_samples,
    )
    from build_next_item import (
        build_next_item_samples,
        validate_next_item_sample,
        write_next_item_samples,
    )
    from config import get_positive_rating_threshold, load_experiment_config
    from config import (
        dataset_uses_gzip_outputs,
        open_text_auto,
        resolve_configured_output_path,
    )
    from preprocess import (
        build_user_sequences,
        iter_user_rating_groups,
        load_movies,
        load_ratings,
        write_sequence_outputs,
    )
    from split import (
        build_full_sequence_leave_two_out_split,
        validate_split_no_leakage,
        write_split,
    )
    from stats import compute_dataset_stats, write_inspection_samples, write_stats


def run_step2(
    config_path: str | Path,
    dataset_key: str | None = None,
    inspection_limit: int = 20,
    eval_only: bool = False,
) -> dict[str, Any]:
    """执行 STEP 2 数据处理并返回摘要。

    Args:
        config_path: 共享实验配置路径。
        dataset_key: 要处理的数据集；不传时使用配置中的 development 数据集。
        inspection_limit: 写入人工检查样本的数量。
    """

    config = load_experiment_config(config_path)
    dataset_key = dataset_key or config["dataset"]["development"]
    threshold = get_positive_rating_threshold(config)
    rng = Random(int(config["seed"]["random_seed"]))

    if dataset_uses_gzip_outputs(config, dataset_key):
        return _run_step2_streaming(
            config=config,
            dataset_key=dataset_key,
            threshold=threshold,
            inspection_limit=inspection_limit,
            eval_only=eval_only,
        )

    # 1. 标准化 MovieLens 原始交互并构建用户内时间序列。
    ratings = load_ratings(dataset_key, config)
    movies = load_movies(dataset_key, config)
    full_sequences, positive_sequences = build_user_sequences(ratings, threshold)
    write_sequence_outputs(dataset_key, full_sequences, positive_sequences, config)

    # 2. 基于 full_sequence 创建 Base/Y/N/M 共享的时间划分。
    split = build_full_sequence_leave_two_out_split(
        full_sequences,
        config,
        dataset_key=dataset_key,
    )
    validate_split_no_leakage(split, full_sequences)
    write_split(dataset_key, split, config)

    # 3. 构造 Y 样本：评分阈值只决定 Yes/No 标签，不影响 split。
    preference_samples = build_preference_samples(full_sequences, split, config)
    for sample in preference_samples:
        validate_preference_sample(sample, threshold)
    write_preference_samples(dataset_key, preference_samples, config)

    # 4. 构造 N 样本：先由 split 确定合法 N target，再写出 train/validation/test。
    all_movie_ids = sorted(str(movie_id) for movie_id in movies)
    next_item_samples = build_next_item_samples(
        full_sequences,
        split,
        all_movie_ids,
        config,
        rng,
    )
    candidate_num = int(config["candidates"]["candidate_num"])
    for sample in next_item_samples:
        validate_next_item_sample(sample, candidate_num=candidate_num)
    write_next_item_samples(dataset_key, next_item_samples, config)

    # 5. 输出统计和人工检查样本，作为进入 STEP 3 前的停靠点。
    stats = compute_dataset_stats(
        full_sequences,
        positive_sequences,
        split,
        config,
        preference_samples=preference_samples,
        next_item_samples=next_item_samples,
    )
    write_stats(dataset_key, stats, config)
    inspection_samples = select_inspection_samples(
        preference_samples,
        next_item_samples,
        inspection_limit,
        rng,
    )
    write_inspection_samples(dataset_key, inspection_samples, config, inspection_limit)

    return {
        "dataset": dataset_key,
        "users_in_split": {
            "y": len(split.get("y", {}).get("users", {})),
            "n": len(split.get("n", {}).get("users", {})),
        },
        "preference_samples": stats["preference_sample_count"],
        "next_item_samples": stats["next_item_sample_count"],
        "inspection_samples": len(inspection_samples),
    }


def _run_step2_streaming(
    config: dict[str, Any],
    dataset_key: str,
    threshold: float,
    inspection_limit: int,
    eval_only: bool,
) -> dict[str, Any]:
    """面向 32M 的流式 STEP 2。

    该路径保持与内存版相同的 Y/N/M 语义，但逐用户写盘，避免把全部评分、
    全部 Y 样本和全部 N 样本同时保存在内存中。
    """

    movies = load_movies(dataset_key, config)
    all_movie_ids = sorted(str(movie_id) for movie_id in movies)
    base_seed = int(config["seed"]["random_seed"])
    candidate_rng = Random(base_seed)
    inspection_rng = Random(base_seed + 909)

    split = _empty_streaming_split(dataset_key, config)
    counters = _empty_streaming_counters()
    stats_state = _empty_streaming_stats()
    inspection_state = {
        "seen": 0,
        "samples": [],
    }

    with ExitStack() as stack:
        writers = _open_streaming_writers(
            stack,
            dataset_key,
            config,
            eval_only=eval_only,
        )

        for user_id, raw_interactions in iter_user_rating_groups(dataset_key, config):
            interactions = _sorted_and_index_interactions(raw_interactions)
            positive_interactions = [
                interaction
                for interaction in interactions
                if interaction["rating"] >= threshold
            ]
            user_sequences = {user_id: interactions}
            user_positive_sequences = {user_id: positive_interactions}

            if not eval_only:
                _write_jsonl_record(
                    writers["full_sequences"],
                    {"user_id": user_id, "interactions": interactions},
                )
                _write_jsonl_record(
                    writers["positive_sequences"],
                    {"user_id": user_id, "interactions": positive_interactions},
                )

            user_split = build_full_sequence_leave_two_out_split(
                user_sequences,
                config,
                dataset_key=dataset_key,
            )
            validate_split_no_leakage(user_split, user_sequences)
            _merge_user_split(split, counters, user_split)

            preference_samples = build_preference_samples(
                user_sequences,
                user_split,
                config,
                include_splits={"validation", "test"} if eval_only else None,
            )
            for sample in preference_samples:
                validate_preference_sample(sample, threshold)
                if not eval_only:
                    _write_jsonl_record(writers["preference_all"], sample)
                _write_jsonl_record(writers[f"preference_{sample['split']}"], sample)
                _update_sample_stats(stats_state, "Y", sample)
                _maybe_add_inspection_sample(
                    inspection_state,
                    {"inspection_task": "Y", **sample},
                    inspection_limit,
                    inspection_rng,
                )

            next_item_samples = build_next_item_samples(
                user_sequences,
                user_split,
                all_movie_ids,
                config,
                candidate_rng,
                include_splits={"validation", "test"} if eval_only else None,
            )
            candidate_num = int(config["candidates"]["candidate_num"])
            for sample in next_item_samples:
                validate_next_item_sample(sample, candidate_num=candidate_num)
                _write_jsonl_record(writers[f"next_item_{sample['split']}"], sample)
                _update_sample_stats(stats_state, "N", sample)
                _maybe_add_inspection_sample(
                    inspection_state,
                    {"inspection_task": "N", **sample},
                    inspection_limit,
                    inspection_rng,
                )

            _update_interaction_stats(
                stats_state,
                interactions,
                positive_interactions,
                threshold,
                user_id in user_split.get("n", {}).get("users", {}),
                user_split,
            )

            if stats_state["user_count"] % 10000 == 0:
                print(
                    json.dumps(
                        {
                            "dataset": dataset_key,
                            "processed_users": stats_state["user_count"],
                            "processed_interactions": stats_state["interaction_count"],
                        },
                        ensure_ascii=False,
                    ),
                    flush=True,
                )

    _finalize_streaming_split(split, counters)
    write_split(dataset_key, split, config)

    stats = _finalize_streaming_stats(stats_state, split, config)
    stats["local_eval_only"] = eval_only
    write_stats(dataset_key, stats, config)
    write_inspection_samples(
        dataset_key,
        inspection_state["samples"],
        config,
        inspection_limit,
    )

    return {
        "dataset": dataset_key,
        "users_in_split": {
            "y": len(split.get("y", {}).get("users", {})),
            "n": len(split.get("n", {}).get("users", {})),
        },
        "preference_samples": stats["preference_sample_count"],
        "next_item_samples": stats["next_item_sample_count"],
        "inspection_samples": len(inspection_state["samples"]),
        "storage": "gzip_processed_jsonl",
        "eval_only": eval_only,
    }


def select_inspection_samples(
    preference_samples: list[dict[str, Any]],
    next_item_samples: list[dict[str, Any]],
    limit: int,
    rng: Random,
) -> list[dict[str, Any]]:
    """抽取 Y/N 混合样本，便于人工检查时间边界和标签。"""

    tagged_samples = [
        {"inspection_task": "Y", **sample} for sample in preference_samples
    ] + [{"inspection_task": "N", **sample} for sample in next_item_samples]

    if len(tagged_samples) <= limit:
        return tagged_samples
    return rng.sample(tagged_samples, limit)


def _open_streaming_writers(
    stack: ExitStack,
    dataset_key: str,
    config: dict[str, Any],
    eval_only: bool,
) -> dict[str, Any]:
    paths = {
        "preference_validation": resolve_configured_output_path(
            config,
            dataset_key,
            "preference_samples",
            "validation",
        ),
        "preference_test": resolve_configured_output_path(
            config,
            dataset_key,
            "preference_samples",
            "test",
        ),
        "next_item_validation": resolve_configured_output_path(
            config,
            dataset_key,
            "next_item_samples",
            "validation",
        ),
        "next_item_test": resolve_configured_output_path(
            config,
            dataset_key,
            "next_item_samples",
            "test",
        ),
    }

    if not eval_only:
        paths.update(
            {
                "full_sequences": resolve_configured_output_path(
                    config,
                    dataset_key,
                    "full_sequences",
                ),
                "positive_sequences": resolve_configured_output_path(
                    config,
                    dataset_key,
                    "positive_sequences_auxiliary",
                ),
                "preference_all": resolve_configured_output_path(
                    config,
                    dataset_key,
                    "preference_samples",
                    "all",
                ),
                "preference_train": resolve_configured_output_path(
                    config,
                    dataset_key,
                    "preference_samples",
                    "train",
                ),
                "next_item_train": resolve_configured_output_path(
                    config,
                    dataset_key,
                    "next_item_samples",
                    "train",
                ),
            }
        )

    writers = {}
    for key, path in paths.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        writers[key] = stack.enter_context(open_text_auto(path, "wt", encoding="utf-8"))
    return writers


def _write_jsonl_record(handle: Any, record: dict[str, Any]) -> None:
    handle.write(json.dumps(record, ensure_ascii=False) + "\n")


def _sorted_and_index_interactions(
    raw_interactions: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    interactions = sorted(
        raw_interactions,
        key=lambda item: (item["timestamp"], item["movie_id"]),
    )
    indexed_interactions = []
    for sequence_index, interaction in enumerate(interactions):
        indexed = dict(interaction)
        indexed["sequence_index"] = sequence_index
        indexed_interactions.append(indexed)
    return indexed_interactions


def _empty_streaming_split(dataset_key: str, config: dict[str, Any]) -> dict[str, Any]:
    min_n_legal_samples = int(
        config.get("split", {})
        .get("n_split", {})
        .get("minimum_legal_next_item_samples_for_n", 2)
    )
    return {
        "dataset": dataset_key,
        "method": "timestamp_bucket_strict_history_per_task",
        "source_sequence": "full_sequence",
        "strict_history_rule": "history_timestamp_lt_target_timestamp",
        "timestamp_tie_policy": {
            "same_timestamp_not_ordered": True,
            "skip_entire_user_on_tie": False,
            "y_policy": "same timestamp targets share strict history",
            "n_policy": "skip only ambiguous next-item samples",
        },
        "bucket_size_distribution": {},
        "user_count": {},
        "y": {
            "split_rule": "last_timestamp_bucket_test_second_last_validation",
            "user_count": {},
            "users": {},
        },
        "n": {
            "split_rule": "last_two_legal_next_item_samples_for_validation_test",
            "minimum_legal_next_item_samples": min_n_legal_samples,
            "user_count": {},
            "users": {},
        },
        "users": {},
    }


def _empty_streaming_counters() -> dict[str, Any]:
    return {
        "total_users": 0,
        "bucket_size_distribution": Counter(),
        "y_skipped_users": Counter(),
        "n_skipped_users": Counter(),
    }


def _empty_streaming_stats() -> dict[str, Any]:
    return {
        "user_count": 0,
        "movie_ids": set(),
        "interaction_count": 0,
        "rating_distribution": Counter(),
        "yes_no_label_distribution": Counter(),
        "full_lengths": [],
        "positive_lengths": [],
        "preference_sample_count": Counter(),
        "next_item_sample_count": Counter(),
        "y_users_by_split": {
            "train": set(),
            "validation": set(),
            "test": set(),
        },
        "n_users_by_split": {
            "train": set(),
            "validation": set(),
            "test": set(),
        },
        "legal_next_item_sample_count_per_user": {},
        "n_retained_lengths": [],
        "n_skipped_lengths": [],
        "n_retained_rating_distribution": Counter(),
        "n_skipped_rating_distribution": Counter(),
    }


def _merge_user_split(
    split: dict[str, Any],
    counters: dict[str, Any],
    user_split: dict[str, Any],
) -> None:
    counters["total_users"] += user_split["user_count"]["total"]
    counters["bucket_size_distribution"].update(user_split["bucket_size_distribution"])
    counters["y_skipped_users"].update(
        user_split["y"]["user_count"].get("skipped_by_reason", {})
    )
    counters["n_skipped_users"].update(
        user_split["n"]["user_count"].get("skipped_by_reason", {})
    )
    split["y"]["users"].update(user_split["y"]["users"])
    split["n"]["users"].update(user_split["n"]["users"])


def _finalize_streaming_split(
    split: dict[str, Any],
    counters: dict[str, Any],
) -> None:
    total_users = counters["total_users"]
    y_included = len(split["y"]["users"])
    n_included = len(split["n"]["users"])
    split["bucket_size_distribution"] = dict(counters["bucket_size_distribution"])
    split["user_count"] = {
        "total": total_users,
        "y_included": y_included,
        "n_included": n_included,
    }
    split["y"]["user_count"] = _user_count(
        total_users,
        y_included,
        counters["y_skipped_users"],
    )
    split["n"]["user_count"] = _user_count(
        total_users,
        n_included,
        counters["n_skipped_users"],
    )
    split["users"] = split["y"]["users"]


def _update_sample_stats(
    stats_state: dict[str, Any],
    task: str,
    sample: dict[str, Any],
) -> None:
    split_name = sample["split"]
    user_id = str(sample["user_id"])
    if task == "Y":
        stats_state["preference_sample_count"][split_name] += 1
        stats_state["y_users_by_split"][split_name].add(user_id)
    elif task == "N":
        stats_state["next_item_sample_count"][split_name] += 1
        stats_state["n_users_by_split"][split_name].add(user_id)
    else:
        raise ValueError(f"未知任务: {task}")


def _maybe_add_inspection_sample(
    inspection_state: dict[str, Any],
    sample: dict[str, Any],
    limit: int,
    rng: Random,
) -> None:
    if limit <= 0:
        return

    inspection_state["seen"] += 1
    seen = inspection_state["seen"]
    samples = inspection_state["samples"]
    if len(samples) < limit:
        samples.append(sample)
        return

    replace_index = rng.randrange(seen)
    if replace_index < limit:
        samples[replace_index] = sample


def _update_interaction_stats(
    stats_state: dict[str, Any],
    interactions: list[dict[str, Any]],
    positive_interactions: list[dict[str, Any]],
    threshold: float,
    n_retained: bool,
    user_split: dict[str, Any],
) -> None:
    stats_state["user_count"] += 1
    stats_state["interaction_count"] += len(interactions)
    stats_state["full_lengths"].append(len(interactions))
    stats_state["positive_lengths"].append(len(positive_interactions))

    for interaction in interactions:
        stats_state["rating_distribution"][str(interaction["rating"])] += 1
        label = "Yes" if interaction["rating"] >= threshold else "No"
        stats_state["yes_no_label_distribution"][label] += 1
        stats_state["movie_ids"].add(str(interaction["movie_id"]))

    if user_split.get("n", {}).get("users"):
        for user_id, info in user_split["n"]["users"].items():
            stats_state["legal_next_item_sample_count_per_user"][user_id] = int(
                info["legal_sample_count"]
            )

    if n_retained:
        stats_state["n_retained_lengths"].append(len(interactions))
        rating_counter = stats_state["n_retained_rating_distribution"]
    else:
        stats_state["n_skipped_lengths"].append(len(interactions))
        rating_counter = stats_state["n_skipped_rating_distribution"]

    for interaction in interactions:
        rating_counter[str(interaction["rating"])] += 1


def _finalize_streaming_stats(
    stats_state: dict[str, Any],
    split: dict[str, Any],
    config: dict[str, Any],
) -> dict[str, Any]:
    bucket_distribution = _normalized_bucket_distribution(
        split.get("bucket_size_distribution", {})
    )
    legal_counts = stats_state["legal_next_item_sample_count_per_user"]
    return {
        "user_count": stats_state["user_count"],
        "movie_count": len(stats_state["movie_ids"]),
        "interaction_count": stats_state["interaction_count"],
        "rating_distribution": dict(sorted(stats_state["rating_distribution"].items())),
        "yes_no_label_distribution": dict(stats_state["yes_no_label_distribution"]),
        "full_sequence_length": _length_summary(stats_state["full_lengths"]),
        "positive_sequence_length_auxiliary": _length_summary(
            stats_state["positive_lengths"]
        ),
        "timestamp_bucket_size_distribution": bucket_distribution,
        "singleton_timestamp_bucket_ratio": _singleton_bucket_ratio(bucket_distribution),
        "split_user_count": split.get("user_count", {}),
        "y_split_user_count": split.get("y", {}).get("user_count", {}),
        "n_split_user_count": split.get("n", {}).get("user_count", {}),
        "y_sample_count": _counter_to_split_dict(
            stats_state["preference_sample_count"]
        ),
        "n_sample_count": _counter_to_split_dict(
            stats_state["next_item_sample_count"]
        ),
        "preference_sample_count": _counter_to_split_dict(
            stats_state["preference_sample_count"]
        ),
        "next_item_sample_count": _counter_to_split_dict(
            stats_state["next_item_sample_count"]
        ),
        "y_user_count_by_split": _user_sets_to_counts(
            stats_state["y_users_by_split"]
        ),
        "n_user_count_by_split": _user_sets_to_counts(
            stats_state["n_users_by_split"]
        ),
        "legal_next_item_sample_count_per_user": legal_counts,
        "legal_next_item_sample_count_summary": _length_summary(
            list(legal_counts.values())
        ),
        "n_skipped_user_count_insufficient_legal_samples": split.get("n", {})
        .get("user_count", {})
        .get("skipped_by_reason", {})
        .get("too_few_legal_next_item_samples", 0),
        "n_retained_vs_skipped_user_comparison": {
            "retained": {
                "user_count": len(stats_state["n_retained_lengths"]),
                "interaction_count": sum(stats_state["n_retained_lengths"]),
                "interaction_length": _length_summary(stats_state["n_retained_lengths"]),
                "rating_distribution": dict(
                    sorted(stats_state["n_retained_rating_distribution"].items())
                ),
            },
            "skipped": {
                "user_count": len(stats_state["n_skipped_lengths"]),
                "interaction_count": sum(stats_state["n_skipped_lengths"]),
                "interaction_length": _length_summary(stats_state["n_skipped_lengths"]),
                "rating_distribution": dict(
                    sorted(stats_state["n_skipped_rating_distribution"].items())
                ),
            },
        },
        "split_source_sequence": split.get("source_sequence"),
        "timestamp_tie_policy": split.get("timestamp_tie_policy"),
        "processed_storage": {
            "gzip": dataset_uses_gzip_outputs(config, split["dataset"]),
        },
    }


def _counter_to_split_dict(counter: Counter[str]) -> dict[str, int]:
    return {
        "train": counter.get("train", 0),
        "validation": counter.get("validation", 0),
        "test": counter.get("test", 0),
    }


def _user_sets_to_counts(users_by_split: dict[str, set[str]]) -> dict[str, int]:
    return {
        split_name: len(user_ids)
        for split_name, user_ids in users_by_split.items()
    }


def _normalized_bucket_distribution(raw_distribution: dict[str, int]) -> dict[str, int]:
    return {
        "size=1": int(raw_distribution.get("size=1", 0)),
        "size=2": int(raw_distribution.get("size=2", 0)),
        "size=3": int(raw_distribution.get("size=3", 0)),
        "size>=4": int(raw_distribution.get("size>=4", 0)),
    }


def _singleton_bucket_ratio(distribution: dict[str, int]) -> float | None:
    total = sum(distribution.values())
    if total == 0:
        return None
    return distribution["size=1"] / total


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


def _user_count(total: int, included: int, skipped_users: Counter[str]) -> dict[str, Any]:
    skipped_by_reason = dict(skipped_users)
    skipped = sum(skipped_by_reason.values())
    return {
        "total": total,
        "included": included,
        "skipped": skipped,
        "skipped_by_reason": skipped_by_reason,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="构建 STEP 2 MovieLens 数据层产物")
    parser.add_argument(
        "--config",
        default="configs/experiment.yaml",
        help="共享实验配置路径",
    )
    parser.add_argument(
        "--dataset",
        default=None,
        help="数据集 key；默认使用配置中的 dataset.development",
    )
    parser.add_argument(
        "--inspection-limit",
        type=int,
        default=20,
        help="写入 inspection_samples.md 的人工检查样本数量",
    )
    parser.add_argument(
        "--eval-only",
        action="store_true",
        help="只写 validation/test 样本，用于 32M 本地评测包准备；不写训练大文件。",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    summary = run_step2(
        config_path=args.config,
        dataset_key=args.dataset,
        inspection_limit=args.inspection_limit,
        eval_only=args.eval_only,
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
