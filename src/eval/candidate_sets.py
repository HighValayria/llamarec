"""STEP 3：生成固定 validation/test 候选集。

候选集只为评测生成一次，后续 Base/Y/N/M 都读取同一份 jsonl 文件，不在
模型评测时重新负采样。N 的 ground truth 表示下一次实际交互，不等价于喜欢。
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from random import Random
from typing import Any

try:
    from src.data.config import (
        load_experiment_config,
        open_text_auto,
        resolve_configured_output_path,
        resolve_repo_path_from_config,
    )
    from src.data.negative_sampling import sample_random_negatives_from_all_movies
    from src.data.preprocess import load_movies
except ImportError:  # 允许在 src/eval 目录附近直接调试。
    from data.config import (
        load_experiment_config,
        open_text_auto,
        resolve_configured_output_path,
        resolve_repo_path_from_config,
    )
    from data.negative_sampling import sample_random_negatives_from_all_movies
    from data.preprocess import load_movies

SPLIT_SEED_OFFSETS = {"validation": 101, "test": 202}


def build_fixed_candidate_sets(
    config_path: str | Path,
    dataset_key: str | None = None,
) -> dict[str, Any]:
    """生成并写出 validation/test 固定候选集。"""

    config = load_experiment_config(config_path)
    dataset_key = dataset_key or config["dataset"]["development"]
    all_movie_ids = sorted(str(movie_id) for movie_id in load_movies(dataset_key, config))
    base_seed = int(config["seed"]["random_seed"])

    summaries = {}
    for split_name in ("validation", "test"):
        source_samples = _read_jsonl(
            resolve_configured_output_path(
                config,
                dataset_key,
                "next_item_samples",
                split_name,
            )
        )
        rng = Random(base_seed + SPLIT_SEED_OFFSETS[split_name])
        records = _build_candidate_records(
            source_samples=source_samples,
            all_movie_ids=all_movie_ids,
            config=config,
            dataset_key=dataset_key,
            split_name=split_name,
            rng=rng,
        )
        for record in records:
            validate_candidate_record(
                record,
                candidate_num=int(config["candidates"]["candidate_num"]),
            )
        output_path = _candidate_output_path(config, dataset_key, split_name)
        _write_jsonl(output_path, records)
        summaries[split_name] = _candidate_summary(records, output_path)

    return {"dataset": dataset_key, "candidate_sets": summaries}


def validate_candidate_record(
    record: dict[str, Any],
    candidate_num: int | None = None,
) -> None:
    """验证固定候选集中的单条记录。"""

    candidates = [str(movie_id) for movie_id in record["candidate_movie_ids"]]
    ground_truth_movie_id = str(record["ground_truth_movie_id"])

    if candidate_num is not None:
        assert len(candidates) == candidate_num

    assert len(candidates) == len(set(candidates)), "候选集中存在重复 movie_id"
    assert candidates.count(ground_truth_movie_id) == 1
    assert record["ground_truth_index"] == candidates.index(ground_truth_movie_id)
    assert record["label"] == record["label_set"][record["ground_truth_index"]]

    target = record["target"]
    assert str(target["movie_id"]) == ground_truth_movie_id
    if record["history"]:
        assert max(item["timestamp"] for item in record["history"]) < target["timestamp"]


def _build_candidate_records(
    source_samples: list[dict[str, Any]],
    all_movie_ids: list[str],
    config: dict[str, Any],
    dataset_key: str,
    split_name: str,
    rng: Random,
) -> list[dict[str, Any]]:
    candidate_num = int(config["candidates"]["candidate_num"])
    negative_num = candidate_num - 1
    label_set = list(config["candidates"].get("label_set", ["A", "B", "C", "D", "E"]))
    shuffle_order = bool(config["candidates"].get("shuffle_order", True))

    if len(label_set) < candidate_num:
        raise ValueError("label_set 长度必须不小于 candidate_num")

    records = []
    for sample_index, sample in enumerate(source_samples):
        ground_truth_movie_id = str(sample["ground_truth_movie_id"])
        negatives = sample_random_negatives_from_all_movies(
            all_movie_ids,
            target_movie_id=ground_truth_movie_id,
            n=negative_num,
            rng=rng,
        )
        candidate_movie_ids = [ground_truth_movie_id, *negatives]
        if shuffle_order:
            rng.shuffle(candidate_movie_ids)
        ground_truth_index = candidate_movie_ids.index(ground_truth_movie_id)

        records.append(
            {
                "dataset": dataset_key,
                "split": split_name,
                "source_task": "N",
                "source_sample_index": sample_index,
                "user_id": sample["user_id"],
                "history": sample["history"],
                "target": sample["target"],
                "candidate_movie_ids": candidate_movie_ids,
                "ground_truth_movie_id": ground_truth_movie_id,
                "ground_truth_index": ground_truth_index,
                "label": label_set[ground_truth_index],
                "label_set": label_set[:candidate_num],
                "candidate_generation": {
                    "method": config["negative_sampling"]["method"],
                    "candidate_num": candidate_num,
                    "negative_num": negative_num,
                    "seed": int(config["seed"]["random_seed"])
                    + SPLIT_SEED_OFFSETS[split_name],
                    "pool": config["negative_sampling"]["pool"],
                },
            }
        )

    return records


def _candidate_summary(records: list[dict[str, Any]], output_path: Path) -> dict[str, Any]:
    position_counts = {str(index): 0 for index in range(5)}
    for record in records:
        key = str(record["ground_truth_index"])
        position_counts[key] = position_counts.get(key, 0) + 1

    return {
        "path": str(output_path),
        "records": len(records),
        "ground_truth_index_distribution": position_counts,
    }


def _candidate_output_path(
    config: dict[str, Any],
    dataset_key: str,
    split_name: str,
) -> Path:
    save_key = "validation" if split_name == "validation" else "test"
    raw_path = config["candidates"]["save_files"][save_key]
    return resolve_repo_path_from_config(
        config,
        raw_path,
        dataset_key=dataset_key,
        split_name=split_name,
    )


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    records = []
    with open_text_auto(path, "rt", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                records.append(json.loads(line))
    return records


def _write_jsonl(path: Path, records: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="生成 STEP 3 固定候选集")
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
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    summary = build_fixed_candidate_sets(args.config, dataset_key=args.dataset)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
