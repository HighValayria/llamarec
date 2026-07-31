"""STEP 2 实现：Y 任务样本构造。

Y = Yes/No Preference Prediction：
History + Target -> Yes / No

标签只由 target 的评分决定：
rating >= positive_rating_threshold -> Yes
rating < positive_rating_threshold  -> No
"""

import json
from typing import Any

try:
    from .config import (
        get_positive_rating_threshold,
        open_text_auto,
        resolve_configured_output_path,
        resolve_dataset_paths,
    )
except ImportError:  # 允许在 src/data 目录内直接调试单个模块文件。
    from config import (
        get_positive_rating_threshold,
        open_text_auto,
        resolve_configured_output_path,
        resolve_dataset_paths,
    )


def build_preference_samples(
    full_sequences: dict[str, list[dict[str, Any]]],
    split: dict[str, Any],
    config: dict[str, Any],
    include_splits: set[str] | None = None,
) -> list[dict[str, Any]]:
    """基于 full_sequence 和 Y 专属 bucket split 构造 Y 样本。"""

    threshold = get_positive_rating_threshold(config)
    history_length = int(config.get("dataset", {}).get("history_length", 10))
    samples = []

    y_users = split.get("y", {}).get("users", split.get("users", {}))

    for user_id, info in y_users.items():
        interactions = _sorted_interactions(full_sequences[user_id])
        validation_timestamp = info["validation_bucket_timestamp"]
        test_timestamp = info["test_bucket_timestamp"]

        if _should_include_split("train", include_splits):
            # Y 的训练区间是 validation timestamp bucket 之前的所有 bucket。
            for target_index, target in enumerate(interactions):
                if target["timestamp"] >= validation_timestamp:
                    continue
                samples.append(
                    _make_preference_sample(
                        user_id,
                        "train",
                        interactions,
                        target_index,
                        history_length,
                        threshold,
                    )
                )

        if _should_include_split("validation", include_splits):
            # 同一 timestamp bucket 内可以有多个 Y target，它们共享严格历史。
            for target_index, target in enumerate(interactions):
                if target["timestamp"] != validation_timestamp:
                    continue
                samples.append(
                    _make_preference_sample(
                        user_id,
                        "validation",
                        interactions,
                        target_index,
                        history_length,
                        threshold,
                    )
                )

        if _should_include_split("test", include_splits):
            for target_index, target in enumerate(interactions):
                if target["timestamp"] != test_timestamp:
                    continue
                samples.append(
                    _make_preference_sample(
                        user_id,
                        "test",
                        interactions,
                        target_index,
                        history_length,
                        threshold,
                    )
                )

    return samples


def validate_preference_sample(
    sample: dict[str, Any],
    positive_rating_threshold: float | None = None,
) -> None:
    """验证单条 Y 样本没有时间泄漏且标签正确。"""

    target = sample["target"]
    threshold = positive_rating_threshold
    if threshold is None:
        threshold = float(sample.get("positive_rating_threshold", 4))

    if sample["history"]:
        assert max(item["timestamp"] for item in sample["history"]) < target["timestamp"]

    target_identity = (
        target.get("sequence_index"),
        target["movie_id"],
        target["timestamp"],
    )
    history_identities = {
        (item.get("sequence_index"), item["movie_id"], item["timestamp"])
        for item in sample["history"]
    }
    assert target_identity not in history_identities

    expected_label = "Yes" if target["rating"] >= threshold else "No"
    assert sample["label"] == expected_label
    assert sample["split"] in {"train", "validation", "test"}
    assert sample["task"] == "Y"


def write_preference_samples(
    dataset_key: str,
    samples: list[dict[str, Any]],
    config: dict[str, Any],
) -> None:
    """按配置写出 Y 样本。

    同时写出合并文件和 train/validation/test 三个拆分文件，避免后续训练入口
    找不到配置中声明的数据路径。
    """

    output_dir = resolve_dataset_paths(config, dataset_key)["output_dir"]
    output_dir.mkdir(parents=True, exist_ok=True)

    _write_jsonl(
        resolve_configured_output_path(config, dataset_key, "preference_samples", "all"),
        samples,
    )
    for split_name, config_key in (
        ("train", "train"),
        ("validation", "validation"),
        ("test", "test"),
    ):
        split_samples = [sample for sample in samples if sample["split"] == split_name]
        _write_jsonl(
            resolve_configured_output_path(
                config,
                dataset_key,
                "preference_samples",
                config_key,
            ),
            split_samples,
        )


def build_binary_samples(*args, **kwargs):
    """兼容旧调用名；当前语义等同于 build_preference_samples。"""

    return build_preference_samples(*args, **kwargs)


def validate_binary_sample(*args, **kwargs):
    """兼容旧调用名；当前语义等同于 validate_preference_sample。"""

    return validate_preference_sample(*args, **kwargs)


def write_binary_samples(*args, **kwargs):
    """兼容旧调用名；当前语义等同于 write_preference_samples。"""

    return write_preference_samples(*args, **kwargs)


def _make_preference_sample(
    user_id: str,
    split_name: str,
    interactions: list[dict[str, Any]],
    target_index: int,
    history_length: int,
    threshold: float,
) -> dict[str, Any]:
    target = interactions[target_index]
    # 真实数据中可能存在同一用户多条 interaction 共享同一个 timestamp。
    # 为满足无泄漏约束，history 必须按 timestamp 严格早于 target，而不是只按序号早于 target。
    history = _strict_history_before_target(interactions, target_index, history_length)
    label = "Yes" if target["rating"] >= threshold else "No"

    return {
        "task": "Y",
        "task_name": "yes_no_preference",
        "user_id": user_id,
        "split": split_name,
        "history": history,
        "target": target,
        "label": label,
        "positive_rating_threshold": threshold,
    }


def _sorted_interactions(interactions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(interactions, key=lambda item: (item["timestamp"], item["movie_id"]))


def _should_include_split(split_name: str, include_splits: set[str] | None) -> bool:
    return include_splits is None or split_name in include_splits


def _strict_history_before_target(
    interactions: list[dict[str, Any]],
    target_index: int,
    history_length: int,
) -> list[dict[str, Any]]:
    target_timestamp = interactions[target_index]["timestamp"]
    strict_history = [
        item for item in interactions[:target_index] if item["timestamp"] < target_timestamp
    ]
    return strict_history[-history_length:]


def _write_jsonl(path, samples: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open_text_auto(path, "wt", encoding="utf-8") as handle:
        for sample in samples:
            handle.write(json.dumps(sample, ensure_ascii=False) + "\n")
