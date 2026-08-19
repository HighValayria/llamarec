"""STEP 3：生成固定 validation/test 候选集。

候选集只为评测生成一次，后续 Base/Y/N/M 都读取同一份 jsonl 文件，不在
模型评测时重新负采样。N 的 ground truth 表示下一次实际交互，不等价于喜欢。
"""

from __future__ import annotations

import argparse
from collections import Counter
import copy
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
    candidate_num: int | None = None,
    label_set: list[str] | None = None,
    variant_name: str | None = None,
    output_dir: str | Path | None = None,
    seed: int | None = None,
    shuffle_order: bool | None = None,
    candidate_method: str | None = None,
) -> dict[str, Any]:
    """生成并写出 validation/test 固定候选集。"""

    config = load_experiment_config(config_path)
    dataset_key = dataset_key or config["dataset"]["development"]
    config = _candidate_variant_config(
        config,
        candidate_num=candidate_num,
        label_set=label_set,
        variant_name=variant_name,
        seed=seed,
        shuffle_order=shuffle_order,
        candidate_method=candidate_method,
    )
    all_movie_ids = _candidate_item_universe(config, dataset_key)
    base_seed = int(config["seed"]["random_seed"])
    method = str(config.get("negative_sampling", {}).get("method", "random"))
    movie_popularity = (
        _load_movie_popularity(config, dataset_key)
        if method == "popularity_matched"
        else Counter()
    )

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
            movie_popularity=movie_popularity,
        )
        for record in records:
            validate_candidate_record(
                record,
                candidate_num=int(config["candidates"]["candidate_num"]),
            )
        output_path = _candidate_output_path(
            config,
            dataset_key,
            split_name,
            variant_name=variant_name,
            output_dir=output_dir,
        )
        _write_jsonl(output_path, records)
        summaries[split_name] = _candidate_summary(records, output_path)

    return {
        "dataset": dataset_key,
        "variant_name": variant_name or "canonical",
        "candidate_num": int(config["candidates"]["candidate_num"]),
        "label_set": list(config["candidates"]["label_set"]),
        "candidate_sets": summaries,
    }


def build_candidate_order_variant(
    config_path: str | Path,
    dataset_key: str | None = None,
    variant_name: str | None = None,
    source_candidate_files: dict[str, str | Path] | None = None,
    output_dir: str | Path | None = None,
    seed: int | None = None,
) -> dict[str, Any]:
    """Create a candidate-order variant from existing fixed candidate files."""

    if not variant_name:
        raise ValueError("variant_name is required for order variants")

    config = load_experiment_config(config_path)
    dataset_key = dataset_key or config["dataset"]["development"]
    base_seed = int(seed if seed is not None else config["seed"]["random_seed"])

    summaries = {}
    for split_name in ("validation", "test"):
        source_path = _source_candidate_path(
            config,
            dataset_key,
            split_name,
            source_candidate_files,
        )
        rng = Random(base_seed + SPLIT_SEED_OFFSETS[split_name])
        records = [
            _permute_candidate_record(
                record,
                rng,
                variant_name=variant_name,
                seed=base_seed + SPLIT_SEED_OFFSETS[split_name],
                source_path=source_path,
            )
            for record in _read_jsonl(source_path)
        ]
        candidate_num = max((len(record["candidate_movie_ids"]) for record in records), default=0)
        for record in records:
            validate_candidate_record(record, candidate_num=candidate_num)
        output_path = _candidate_output_path(
            config,
            dataset_key,
            split_name,
            variant_name=variant_name,
            output_dir=output_dir,
        )
        _write_jsonl(output_path, records)
        summaries[split_name] = _candidate_summary(records, output_path)

    return {
        "dataset": dataset_key,
        "variant_name": variant_name,
        "candidate_sets": summaries,
    }


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
    movie_popularity: Counter[str] | None = None,
) -> list[dict[str, Any]]:
    candidate_num = int(config["candidates"]["candidate_num"])
    negative_num = candidate_num - 1
    label_set = _candidate_label_set(config, candidate_num)
    shuffle_order = bool(config["candidates"].get("shuffle_order", True))
    method = str(config.get("negative_sampling", {}).get("method", "random"))
    movie_popularity = movie_popularity or Counter()

    if len(label_set) < candidate_num:
        raise ValueError("label_set 长度必须不小于 candidate_num")

    records = []
    for sample_index, sample in enumerate(source_samples):
        ground_truth_movie_id = str(sample["ground_truth_movie_id"])
        negatives = _sample_negatives(
            method=method,
            all_movie_ids=all_movie_ids,
            ground_truth_movie_id=ground_truth_movie_id,
            negative_num=negative_num,
            rng=rng,
            movie_popularity=movie_popularity,
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
                    "method": method,
                    "variant_name": config["candidates"].get("variant_name", "canonical"),
                    "candidate_num": candidate_num,
                    "negative_num": negative_num,
                    "seed": int(config["seed"]["random_seed"])
                    + SPLIT_SEED_OFFSETS[split_name],
                    "pool": config["negative_sampling"]["pool"],
                    "shuffle_order": shuffle_order,
                    **_negative_sampling_metadata(
                        method,
                        ground_truth_movie_id,
                        negatives,
                        movie_popularity,
                    ),
                },
            }
        )

    return records


def sample_popularity_matched_negatives(
    all_movie_ids: list[str],
    target_movie_id: str,
    n: int,
    rng: Random,
    movie_popularity: Counter[str] | dict[str, int],
    candidate_pool_multiplier: int = 10,
) -> list[str]:
    """Sample negatives from movies with popularity closest to the target item."""

    target_movie_id = str(target_movie_id)
    if n < 0:
        raise ValueError("n must be non-negative")
    if n == 0:
        return []

    pool = [str(movie_id) for movie_id in all_movie_ids if str(movie_id) != target_movie_id]
    if len(pool) < n:
        raise ValueError(f"negative pool too small: need={n}, available={len(pool)}")

    target_popularity = int(movie_popularity.get(target_movie_id, 0))
    ranked_pool = sorted(
        pool,
        key=lambda movie_id: (
            abs(int(movie_popularity.get(movie_id, 0)) - target_popularity),
            str(movie_id),
        ),
    )
    hard_pool_size = min(len(ranked_pool), max(n, n * int(candidate_pool_multiplier)))
    return rng.sample(ranked_pool[:hard_pool_size], n)


def _sample_negatives(
    method: str,
    all_movie_ids: list[str],
    ground_truth_movie_id: str,
    negative_num: int,
    rng: Random,
    movie_popularity: Counter[str],
) -> list[str]:
    if method == "random":
        return sample_random_negatives_from_all_movies(
            all_movie_ids,
            target_movie_id=ground_truth_movie_id,
            n=negative_num,
            rng=rng,
        )
    if method == "popularity_matched":
        return sample_popularity_matched_negatives(
            all_movie_ids,
            target_movie_id=ground_truth_movie_id,
            n=negative_num,
            rng=rng,
            movie_popularity=movie_popularity,
        )
    raise ValueError(f"Unsupported candidate negative sampling method: {method}")


def _negative_sampling_metadata(
    method: str,
    ground_truth_movie_id: str,
    negatives: list[str],
    movie_popularity: Counter[str],
) -> dict[str, Any]:
    if method != "popularity_matched":
        return {}

    target_popularity = int(movie_popularity.get(str(ground_truth_movie_id), 0))
    negative_popularities = [
        int(movie_popularity.get(str(movie_id), 0))
        for movie_id in negatives
    ]
    mean_negative_popularity = (
        sum(negative_popularities) / len(negative_popularities)
        if negative_popularities
        else 0.0
    )
    return {
        "target_popularity": target_popularity,
        "negative_popularity_mean": round(mean_negative_popularity, 10),
        "negative_popularity_min": min(negative_popularities, default=0),
        "negative_popularity_max": max(negative_popularities, default=0),
    }


def _load_movie_popularity(config: dict[str, Any], dataset_key: str) -> Counter[str]:
    full_sequences_path = resolve_configured_output_path(
        config,
        dataset_key,
        "full_sequences",
    )
    popularity: Counter[str] = Counter()
    with open_text_auto(full_sequences_path, "rt", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            record = json.loads(line)
            for interaction in record.get("interactions", []):
                popularity[str(interaction["movie_id"])] += 1
    return popularity


def _candidate_item_universe(config: dict[str, Any], dataset_key: str) -> list[str]:
    raw_info = config.get("raw_files", {}).get(dataset_key, {})
    if raw_info.get("candidate_item_universe") != "observed_interactions":
        return sorted(str(movie_id) for movie_id in load_movies(dataset_key, config))

    full_sequences_path = resolve_configured_output_path(
        config,
        dataset_key,
        "full_sequences",
    )
    item_ids = set()
    with open_text_auto(full_sequences_path, "rt", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            record = json.loads(line)
            for interaction in record.get("interactions", []):
                item_ids.add(str(interaction["movie_id"]))
    if not item_ids:
        raise ValueError(f"observed interaction item universe is empty: {dataset_key}")
    return sorted(item_ids)


def _permute_candidate_record(
    record: dict[str, Any],
    rng: Random,
    variant_name: str,
    seed: int,
    source_path: Path,
) -> dict[str, Any]:
    output = copy.deepcopy(record)
    original_candidates = [str(movie_id) for movie_id in record["candidate_movie_ids"]]
    candidate_movie_ids = list(original_candidates)
    rng.shuffle(candidate_movie_ids)
    if len(candidate_movie_ids) > 1 and candidate_movie_ids == original_candidates:
        candidate_movie_ids = candidate_movie_ids[1:] + candidate_movie_ids[:1]

    label_set = list(record["label_set"])
    ground_truth_movie_id = str(record["ground_truth_movie_id"])
    ground_truth_index = candidate_movie_ids.index(ground_truth_movie_id)
    previous_generation = dict(record.get("candidate_generation", {}))

    output["candidate_movie_ids"] = candidate_movie_ids
    output["ground_truth_index"] = ground_truth_index
    output["label"] = label_set[ground_truth_index]
    output["label_set"] = label_set
    output["candidate_generation"] = {
        **previous_generation,
        "method": "order_permutation",
        "variant_name": variant_name,
        "source_variant_name": previous_generation.get("variant_name", "canonical"),
        "source_path": str(source_path),
        "candidate_num": len(candidate_movie_ids),
        "seed": seed,
        "preserves_candidate_ids": True,
    }
    return output


def _candidate_summary(records: list[dict[str, Any]], output_path: Path) -> dict[str, Any]:
    candidate_num = max((len(record["candidate_movie_ids"]) for record in records), default=0)
    position_counts = {str(index): 0 for index in range(candidate_num)}
    for record in records:
        key = str(record["ground_truth_index"])
        position_counts[key] = position_counts.get(key, 0) + 1

    return {
        "path": str(output_path),
        "records": len(records),
        "candidate_num": candidate_num,
        "ground_truth_index_distribution": position_counts,
    }


def _candidate_output_path(
    config: dict[str, Any],
    dataset_key: str,
    split_name: str,
    variant_name: str | None = None,
    output_dir: str | Path | None = None,
) -> Path:
    output_split = "valid" if split_name == "validation" else "test"
    if output_dir is not None:
        path = Path(output_dir)
        if not path.is_absolute():
            path = Path(config["_repo_root"]) / path
        return path / f"{output_split}.jsonl"
    if variant_name:
        return (
            Path(config["_repo_root"])
            / "data"
            / "candidates"
            / dataset_key
            / "variants"
            / variant_name
            / f"{output_split}.jsonl"
        )
    save_key = "validation" if split_name == "validation" else "test"
    raw_path = config["candidates"]["save_files"][save_key]
    return resolve_repo_path_from_config(
        config,
        raw_path,
        dataset_key=dataset_key,
        split_name=split_name,
    )


def _source_candidate_path(
    config: dict[str, Any],
    dataset_key: str,
    split_name: str,
    source_candidate_files: dict[str, str | Path] | None = None,
) -> Path:
    save_key = "validation" if split_name == "validation" else "test"
    if source_candidate_files and save_key in source_candidate_files:
        path = Path(source_candidate_files[save_key])
        if path.is_absolute():
            return path
        return Path(config["_repo_root"]) / path
    return _candidate_output_path(config, dataset_key, split_name)


def _candidate_file_overrides(
    valid_candidates: str | None,
    test_candidates: str | None,
) -> dict[str, str] | None:
    overrides = {}
    if valid_candidates:
        overrides["validation"] = valid_candidates
    if test_candidates:
        overrides["test"] = test_candidates
    return overrides or None


def _candidate_variant_config(
    config: dict[str, Any],
    candidate_num: int | None,
    label_set: list[str] | None,
    variant_name: str | None,
    seed: int | None,
    shuffle_order: bool | None,
    candidate_method: str | None,
) -> dict[str, Any]:
    copied = dict(config)
    copied["seed"] = dict(config.get("seed", {}))
    copied["candidates"] = dict(config.get("candidates", {}))
    copied["negative_sampling"] = dict(config.get("negative_sampling", {}))

    if candidate_num is not None:
        if candidate_num <= 1:
            raise ValueError("candidate_num must be greater than 1")
        copied["candidates"]["candidate_num"] = int(candidate_num)
        copied["candidates"]["negative_num"] = int(candidate_num) - 1

    resolved_candidate_num = int(copied["candidates"]["candidate_num"])
    labels = list(label_set) if label_set is not None else _candidate_label_set(
        copied,
        resolved_candidate_num,
    )
    if len(labels) < resolved_candidate_num:
        raise ValueError("label_set length must be at least candidate_num")
    copied["candidates"]["label_set"] = labels[:resolved_candidate_num]
    copied["candidates"]["variant_name"] = variant_name or copied["candidates"].get(
        "variant_name",
        "canonical",
    )

    if seed is not None:
        copied["seed"]["random_seed"] = int(seed)
    if shuffle_order is not None:
        copied["candidates"]["shuffle_order"] = bool(shuffle_order)
    if candidate_method is not None:
        copied["negative_sampling"]["method"] = str(candidate_method)
    return copied


def _candidate_label_set(config: dict[str, Any], candidate_num: int) -> list[str]:
    configured = list(config.get("candidates", {}).get("label_set", []))
    if len(configured) >= candidate_num:
        return configured[:candidate_num]
    return spreadsheet_labels(candidate_num)


def spreadsheet_labels(count: int) -> list[str]:
    """Return A, B, ..., Z, AA, AB style labels for candidate variants."""

    if count <= 0:
        raise ValueError("label count must be positive")
    return [_spreadsheet_label(index) for index in range(count)]


def _spreadsheet_label(index: int) -> str:
    label = ""
    value = index
    while True:
        value, remainder = divmod(value, 26)
        label = chr(ord("A") + remainder) + label
        if value == 0:
            return label
        value -= 1


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
    parser.add_argument("--candidate-num", type=int, default=None)
    parser.add_argument("--label-set", nargs="+", default=None)
    parser.add_argument("--variant-name", default=None)
    parser.add_argument("--output-dir", default=None)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--no-shuffle-order", action="store_true")
    parser.add_argument(
        "--candidate-method",
        choices=["random", "popularity_matched"],
        default=None,
    )
    parser.add_argument("--order-variant", action="store_true")
    parser.add_argument("--source-valid-candidates", default=None)
    parser.add_argument("--source-test-candidates", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.order_variant:
        summary = build_candidate_order_variant(
            args.config,
            dataset_key=args.dataset,
            variant_name=args.variant_name,
            source_candidate_files=_candidate_file_overrides(
                args.source_valid_candidates,
                args.source_test_candidates,
            ),
            output_dir=args.output_dir,
            seed=args.seed,
        )
    else:
        summary = build_fixed_candidate_sets(
            args.config,
            dataset_key=args.dataset,
            candidate_num=args.candidate_num,
            label_set=args.label_set,
            variant_name=args.variant_name,
            output_dir=args.output_dir,
            seed=args.seed,
            shuffle_order=False if args.no_shuffle_order else None,
            candidate_method=args.candidate_method,
        )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
