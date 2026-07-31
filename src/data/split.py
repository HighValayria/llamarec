"""STEP 2 实现：基于 full_sequence 的时间划分。

当前 MVP 使用 timestamp bucket 理解用户内时间。严格历史规则永远是：
history = 所有 timestamp < target_timestamp 的 interaction。

同一 timestamp 内没有可观测先后顺序，因此 tie 不会删除整个用户；只有 N
任务中无法确定唯一 next item 的局部样本会被跳过。
"""

from __future__ import annotations

from collections import Counter
import json
from typing import Any

try:
    from .config import resolve_configured_output_path, resolve_dataset_paths
except ImportError:  # 允许在 src/data 目录内直接调试单个模块文件。
    from config import resolve_configured_output_path, resolve_dataset_paths


def build_full_sequence_leave_two_out_split(
    full_sequences: dict[str, list[dict[str, Any]]],
    config: dict[str, Any],
    dataset_key: str | None = None,
) -> dict[str, Any]:
    """为 Y 与 N 构造各自公平、无泄漏的 full_sequence 时间划分。

    函数名保留旧入口，便于已有脚本继续调用；返回内容已经迁移为新版
    timestamp-bucket split。
    """

    min_y_buckets = int(
        config.get("split", {}).get("minimum_timestamp_buckets_for_y", 2)
    )
    min_n_legal_samples = int(
        config.get("split", {}).get(
            "minimum_legal_next_item_samples_for_n",
            config.get("split", {})
            .get("n_split", {})
            .get("minimum_legal_next_item_samples_for_n", 2),
        )
    )

    y_users: dict[str, dict[str, Any]] = {}
    n_users: dict[str, dict[str, Any]] = {}
    y_skipped_users: Counter[str] = Counter()
    n_skipped_users: Counter[str] = Counter()
    bucket_size_distribution: Counter[str] = Counter()

    for user_id, raw_interactions in full_sequences.items():
        interactions = _sorted_interactions(raw_interactions)
        buckets = _timestamp_buckets(interactions)

        for bucket in buckets:
            bucket_size_distribution[_bucket_size_key(len(bucket["indices"]))] += 1

        if len(buckets) < min_y_buckets:
            y_skipped_users["too_few_timestamp_buckets"] += 1
        else:
            y_users[user_id] = _build_y_user_split(interactions, buckets)

        legal_n_samples, ambiguous_bucket_count = _legal_next_item_targets(
            interactions,
            buckets,
        )
        if len(legal_n_samples) < min_n_legal_samples:
            n_skipped_users["too_few_legal_next_item_samples"] += 1
        else:
            n_users[user_id] = _build_n_user_split(
                legal_n_samples,
                ambiguous_bucket_count,
            )

    y_user_count = _user_count(
        total=len(full_sequences),
        included=len(y_users),
        skipped_users=y_skipped_users,
    )
    n_user_count = _user_count(
        total=len(full_sequences),
        included=len(n_users),
        skipped_users=n_skipped_users,
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
        "bucket_size_distribution": dict(bucket_size_distribution),
        "user_count": {
            "total": len(full_sequences),
            "y_included": len(y_users),
            "n_included": len(n_users),
        },
        "y": {
            "split_rule": "last_timestamp_bucket_test_second_last_validation",
            "user_count": y_user_count,
            "users": y_users,
        },
        "n": {
            "split_rule": "last_two_legal_next_item_samples_for_validation_test",
            "minimum_legal_next_item_samples": min_n_legal_samples,
            "user_count": n_user_count,
            "users": n_users,
        },
        # 兼容旧调用方：不要再把这个字段理解为 Y/N 共享用户全集。
        "users": y_users,
    }


def validate_split_no_leakage(
    split: dict[str, Any],
    full_sequences: dict[str, list[dict[str, Any]]],
) -> None:
    """验证 split 自身满足新版严格历史与局部跳过规则。"""

    assert split["source_sequence"] == "full_sequence"
    assert split.get("timestamp_tie_policy", {}).get("skip_entire_user_on_tie") is False

    for user_id, info in split.get("y", {}).get("users", {}).items():
        interactions = _sorted_interactions(full_sequences[user_id])
        buckets = _timestamp_buckets(interactions)
        assert len(buckets) >= 2

        validation_timestamp = info["validation_bucket_timestamp"]
        test_timestamp = info["test_bucket_timestamp"]
        assert validation_timestamp == buckets[-2]["timestamp"]
        assert test_timestamp == buckets[-1]["timestamp"]

        for target in info["validation_targets"]:
            _assert_history_before_target(
                _history_before_timestamp(interactions, target["timestamp"]),
                target,
                user_id,
                "Y validation",
            )
        for target in info["test_targets"]:
            _assert_history_before_target(
                _history_before_timestamp(interactions, target["timestamp"]),
                target,
                user_id,
                "Y test",
            )

    for user_id, info in split.get("n", {}).get("users", {}).items():
        interactions = _sorted_interactions(full_sequences[user_id])
        buckets = _timestamp_buckets(interactions)
        legal_samples, _ = _legal_next_item_targets(interactions, buckets)

        assert len(legal_samples) == info["legal_sample_count"]
        assert len(legal_samples) >= split["n"]["minimum_legal_next_item_samples"]

        validation_sample = legal_samples[-2]
        test_sample = legal_samples[-1]
        assert validation_sample["target_index"] == info["validation_target_index"]
        assert test_sample["target_index"] == info["test_target_index"]
        assert _same_target(validation_sample["target"], info["validation_target"])
        assert _same_target(test_sample["target"], info["test_target"])

        for split_name, sample in (
            ("N validation", validation_sample),
            ("N test", test_sample),
        ):
            target = sample["target"]
            _assert_target_bucket_is_singleton(buckets, target["timestamp"], user_id)
            _assert_history_before_target(
                _history_before_timestamp(interactions, target["timestamp"]),
                target,
                user_id,
                split_name,
            )


def write_split(dataset_key: str, split: dict[str, Any], config: dict[str, Any]) -> None:
    """写出 split 文件。"""

    output_dir = resolve_dataset_paths(config, dataset_key)["output_dir"]
    output_dir.mkdir(parents=True, exist_ok=True)
    split_path = resolve_configured_output_path(config, dataset_key, "split")
    split_path.parent.mkdir(parents=True, exist_ok=True)
    with split_path.open("w", encoding="utf-8") as handle:
        json.dump(split, handle, ensure_ascii=False, indent=2)


def build_legal_next_item_targets_for_user(
    interactions: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """暴露给 N 样本构造器的合法 next-item target 枚举函数。"""

    sorted_interactions = _sorted_interactions(interactions)
    buckets = _timestamp_buckets(sorted_interactions)
    legal_samples, _ = _legal_next_item_targets(sorted_interactions, buckets)
    return legal_samples


def _build_y_user_split(
    interactions: list[dict[str, Any]],
    buckets: list[dict[str, Any]],
) -> dict[str, Any]:
    validation_bucket = buckets[-2]
    test_bucket = buckets[-1]

    return {
        "train_bucket_timestamps": [bucket["timestamp"] for bucket in buckets[:-2]],
        "validation_bucket_timestamp": validation_bucket["timestamp"],
        "test_bucket_timestamp": test_bucket["timestamp"],
        "validation_target_indices": validation_bucket["indices"],
        "test_target_indices": test_bucket["indices"],
        "validation_targets": [
            _target_view(interactions[index], index)
            for index in validation_bucket["indices"]
        ],
        "test_targets": [
            _target_view(interactions[index], index) for index in test_bucket["indices"]
        ],
        "train_region_interaction_count": sum(
            len(bucket["indices"]) for bucket in buckets[:-2]
        ),
        "train_cutoff_timestamp": validation_bucket["timestamp"],
    }


def _build_n_user_split(
    legal_samples: list[dict[str, Any]],
    ambiguous_bucket_count: int,
) -> dict[str, Any]:
    validation_sample = legal_samples[-2]
    test_sample = legal_samples[-1]

    return {
        "legal_sample_count": len(legal_samples),
        "train_legal_sample_count": max(len(legal_samples) - 2, 0),
        "ambiguous_next_bucket_count": ambiguous_bucket_count,
        "validation_target_index": validation_sample["target_index"],
        "test_target_index": test_sample["target_index"],
        "validation_target": validation_sample["target"],
        "test_target": test_sample["target"],
        "validation_target_timestamp": validation_sample["target"]["timestamp"],
        "test_target_timestamp": test_sample["target"]["timestamp"],
    }


def _legal_next_item_targets(
    interactions: list[dict[str, Any]],
    buckets: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], int]:
    """枚举某用户所有严格可确定的 N target。

    第一个 timestamp bucket 没有历史，不能形成 History -> Next Item 样本。
    后续 bucket 只有在 size=1 时才有唯一 next-item ground truth。
    """

    legal_samples = []
    ambiguous_bucket_count = 0

    for bucket_position, bucket in enumerate(buckets):
        if bucket_position == 0:
            continue
        if len(bucket["indices"]) != 1:
            ambiguous_bucket_count += 1
            continue

        target_index = bucket["indices"][0]
        legal_samples.append(
            {
                "target_index": target_index,
                "target": _target_view(interactions[target_index], target_index),
            }
        )

    return legal_samples, ambiguous_bucket_count


def _timestamp_buckets(
    interactions: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    buckets = []
    current_timestamp = None
    current_indices: list[int] = []

    for index, interaction in enumerate(interactions):
        timestamp = interaction["timestamp"]
        if current_timestamp is None or timestamp == current_timestamp:
            current_timestamp = timestamp
            current_indices.append(index)
            continue

        buckets.append({"timestamp": current_timestamp, "indices": current_indices})
        current_timestamp = timestamp
        current_indices = [index]

    if current_timestamp is not None:
        buckets.append({"timestamp": current_timestamp, "indices": current_indices})

    return buckets


def _sorted_interactions(interactions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    # movie_id 只用于稳定输出，不表示同 timestamp 内存在真实先后顺序。
    return sorted(interactions, key=lambda item: (item["timestamp"], item["movie_id"]))


def _history_before_timestamp(
    interactions: list[dict[str, Any]],
    target_timestamp: int,
) -> list[dict[str, Any]]:
    return [
        interaction
        for interaction in interactions
        if interaction["timestamp"] < target_timestamp
    ]


def _target_view(interaction: dict[str, Any], sequence_index: int) -> dict[str, Any]:
    return {
        "movie_id": interaction["movie_id"],
        "title": interaction.get("title", "Unknown"),
        "rating": interaction["rating"],
        "timestamp": interaction["timestamp"],
        "sequence_index": sequence_index,
    }


def _same_target(left: dict[str, Any], right: dict[str, Any]) -> bool:
    return (
        str(left["movie_id"]) == str(right["movie_id"])
        and left["timestamp"] == right["timestamp"]
        and float(left["rating"]) == float(right["rating"])
        and left.get("sequence_index") == right.get("sequence_index")
    )


def _assert_target_bucket_is_singleton(
    buckets: list[dict[str, Any]],
    target_timestamp: int,
    user_id: str,
) -> None:
    matching = [
        bucket for bucket in buckets if bucket["timestamp"] == target_timestamp
    ]
    assert len(matching) == 1, f"用户 {user_id} 的 target timestamp 不存在"
    assert len(matching[0]["indices"]) == 1, (
        f"用户 {user_id} 的 N target bucket 非 singleton: {target_timestamp}"
    )


def _assert_history_before_target(
    history: list[dict[str, Any]],
    target: dict[str, Any],
    user_id: str,
    split_name: str,
) -> None:
    """检查单个 target 的 history 时间边界。"""

    if history:
        max_history_timestamp = max(item["timestamp"] for item in history)
        assert max_history_timestamp < target["timestamp"], (
            f"用户 {user_id} 的 {split_name} history 存在未来泄漏: "
            f"{max_history_timestamp} >= {target['timestamp']}"
        )

    target_identity = (
        target.get("sequence_index"),
        str(target["movie_id"]),
        target["timestamp"],
    )
    history_identities = {
        (item.get("sequence_index"), str(item["movie_id"]), item["timestamp"])
        for item in history
    }
    assert target_identity not in history_identities, (
        f"用户 {user_id} 的 {split_name} target 出现在自身 history 中"
    )


def _bucket_size_key(size: int) -> str:
    if size >= 4:
        return "size>=4"
    return f"size={size}"


def _user_count(total: int, included: int, skipped_users: Counter[str]) -> dict[str, Any]:
    skipped_by_reason = dict(skipped_users)
    skipped = sum(skipped_by_reason.values())
    return {
        "total": total,
        "included": included,
        "skipped": skipped,
        "skipped_by_reason": skipped_by_reason,
    }
