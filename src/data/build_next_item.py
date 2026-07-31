"""STEP 2 实现：N 任务样本构造。

N = Full-sequence Next-item Prediction：
History + Candidate Set -> 实际发生的下一个 Item

N 的 ground truth 来自 full_sequence 中真实发生的下一次 interaction，不根据评分
筛选。若下一 timestamp bucket 有多个 interaction，则该位置没有唯一 next item，
只跳过该 N 样本，不跳过整个用户。
"""

from __future__ import annotations

import json
from random import Random
from typing import Any

try:
    from .config import open_text_auto, resolve_configured_output_path, resolve_dataset_paths
    from .negative_sampling import sample_random_negatives_from_all_movies
    from .split import build_legal_next_item_targets_for_user
except ImportError:  # 允许在 src/data 目录内直接调试单个模块文件。
    from config import open_text_auto, resolve_configured_output_path, resolve_dataset_paths
    from negative_sampling import sample_random_negatives_from_all_movies
    from split import build_legal_next_item_targets_for_user

DEFAULT_LABEL_SET = ("A", "B", "C", "D", "E")


def build_next_item_samples(
    full_sequences: dict[str, list[dict[str, Any]]],
    split: dict[str, Any],
    all_movie_ids: list[str],
    config: dict[str, Any],
    rng: Random,
    include_splits: set[str] | None = None,
) -> list[dict[str, Any]]:
    """构造 N 的 train/validation/test 候选选择样本。"""

    candidate_num = int(config.get("candidates", {}).get("candidate_num", 5))
    negative_num = candidate_num - 1
    label_set = tuple(config.get("candidates", {}).get("label_set", DEFAULT_LABEL_SET))
    history_length = int(config.get("dataset", {}).get("history_length", 10))
    shuffle_order = bool(config.get("candidates", {}).get("shuffle_order", True))

    if len(label_set) < candidate_num:
        raise ValueError("label_set 长度必须不小于 candidate_num")

    samples = []
    n_users = split.get("n", {}).get("users", {})
    for user_id, info in n_users.items():
        interactions = _sorted_interactions(full_sequences[user_id])
        legal_targets = build_legal_next_item_targets_for_user(interactions)

        if len(legal_targets) != info["legal_sample_count"]:
            raise AssertionError(f"用户 {user_id} 的合法 N 样本数与 split 不一致")

        validation_position = len(legal_targets) - 2
        test_position = len(legal_targets) - 1

        for legal_position, legal_target in enumerate(legal_targets):
            if legal_position < validation_position:
                split_name = "train"
            elif legal_position == validation_position:
                split_name = "validation"
            elif legal_position == test_position:
                split_name = "test"
            else:  # 理论不可达，保留断言式保护。
                raise AssertionError("N legal target position 超出预期")

            if not _should_include_split(split_name, include_splits):
                continue

            target_index = legal_target["target_index"]
            target = interactions[target_index]
            history = _strict_history_before_target(
                interactions,
                target_index,
                history_length,
            )
            if not history:
                # build_legal_next_item_targets_for_user 已跳过第一个 bucket；
                # 这里保留保护，避免未来改动引入空 history 的 N 样本。
                continue

            candidates = _build_candidate_ids(
                target_movie_id=target["movie_id"],
                all_movie_ids=all_movie_ids,
                negative_num=negative_num,
                shuffle_order=shuffle_order,
                rng=rng,
            )
            ground_truth_index = candidates.index(str(target["movie_id"]))

            samples.append(
                {
                    "task": "N",
                    "task_name": "full_sequence_next_item",
                    "user_id": user_id,
                    "split": split_name,
                    "history": history,
                    "target": target,
                    "candidate_movie_ids": candidates,
                    "ground_truth_movie_id": str(target["movie_id"]),
                    "ground_truth_index": ground_truth_index,
                    "label": label_set[ground_truth_index],
                    "label_set": list(label_set[:candidate_num]),
                }
            )

    return samples


def build_next_item_train_samples(*args, **kwargs):
    """兼容旧调用名；当前会返回 N 的 train/validation/test 全部样本。"""

    return build_next_item_samples(*args, **kwargs)


def validate_next_item_sample(
    sample: dict[str, Any],
    candidate_num: int | None = None,
) -> None:
    """验证单条 N 样本的候选集和时间边界。"""

    assert sample["task"] == "N"
    assert sample["split"] in {"train", "validation", "test"}
    candidates = [str(movie_id) for movie_id in sample["candidate_movie_ids"]]
    ground_truth_movie_id = str(sample["ground_truth_movie_id"])

    if candidate_num is not None:
        assert len(candidates) == candidate_num

    assert len(set(candidates)) == len(candidates), "candidate_movie_ids 存在重复项"
    assert candidates.count(ground_truth_movie_id) == 1
    assert sample["ground_truth_index"] == candidates.index(ground_truth_movie_id)
    assert sample["label"] == sample["label_set"][sample["ground_truth_index"]]

    target = sample["target"]
    assert str(target["movie_id"]) == ground_truth_movie_id
    if sample["history"]:
        assert max(item["timestamp"] for item in sample["history"]) < target["timestamp"]

    target_identity = (
        target.get("sequence_index"),
        str(target["movie_id"]),
        target["timestamp"],
    )
    history_identities = {
        (item.get("sequence_index"), str(item["movie_id"]), item["timestamp"])
        for item in sample["history"]
    }
    assert target_identity not in history_identities


def write_next_item_samples(
    dataset_key: str,
    samples: list[dict[str, Any]],
    config: dict[str, Any],
) -> None:
    """按 split 写出 N 样本。"""

    output_dir = resolve_dataset_paths(config, dataset_key)["output_dir"]
    output_dir.mkdir(parents=True, exist_ok=True)

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
                "next_item_samples",
                config_key,
            ),
            split_samples,
        )


def write_next_item_train_samples(*args, **kwargs):
    """兼容旧调用名；当前会写出 N 的 train/validation/test 三个文件。"""

    return write_next_item_samples(*args, **kwargs)


def _build_candidate_ids(
    target_movie_id: str,
    all_movie_ids: list[str],
    negative_num: int,
    shuffle_order: bool,
    rng: Random,
) -> list[str]:
    target_movie_id = str(target_movie_id)
    negatives = sample_random_negatives_from_all_movies(
        all_movie_ids,
        target_movie_id=target_movie_id,
        n=negative_num,
        rng=rng,
    )
    candidates = [target_movie_id, *negatives]
    if shuffle_order:
        rng.shuffle(candidates)
    return candidates


def _sorted_interactions(interactions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    # movie_id 只用于稳定输出，不表示同 timestamp 内存在真实先后顺序。
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
