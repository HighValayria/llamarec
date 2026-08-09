"""Popularity baseline for fixed next-item candidate sets."""

from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any

from src.data.config import (
    load_experiment_config,
    open_text_auto,
    resolve_configured_output_path,
    resolve_repo_path_from_config,
)
from src.eval.ranking_metrics import aggregate_ranking_metrics, default_ranking_ks
from src.inference.prediction_io import read_jsonl, write_json, write_jsonl, write_yaml


OUTPUT_SPLIT_NAMES = {
    "validation": "valid",
    "test": "test",
}

SPLIT_ALIASES = {
    "validation": "validation",
    "valid": "validation",
    "val": "validation",
    "test": "test",
}


def run_popularity_baseline(
    config_path: str | Path,
    dataset_key: str | None = None,
    splits: list[str] | None = None,
    limit: int | None = None,
    output_dir: str | Path | None = None,
    candidate_files: dict[str, str | Path] | None = None,
    popularity_source: str = "n_train_targets",
) -> dict[str, Any]:
    """Score candidates by item frequency in a training-only source."""

    config = load_experiment_config(config_path)
    dataset_key = dataset_key or config["dataset"]["formal"]
    normalized_splits = _normalize_splits(splits or ["validation", "test"])
    output_path = _resolve_output_dir(config, dataset_key, output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    popularity = _load_popularity(config, dataset_key, popularity_source)
    write_yaml(output_path / "config_snapshot.yaml", _config_snapshot(config))

    metrics_by_split = {}
    counts_by_split = {}
    for split_name in normalized_splits:
        records = _read_candidate_records(
            config,
            dataset_key,
            split_name,
            limit,
            candidate_files=candidate_files,
        )
        output_split = OUTPUT_SPLIT_NAMES[split_name]
        prediction_path = output_path / f"n_{output_split}_predictions.jsonl"
        predictions, metric_records = _predict_records(
            records=records,
            popularity=popularity,
            split_name=split_name,
            popularity_source=popularity_source,
        )
        write_jsonl(prediction_path, predictions)

        metrics = _metrics_for_split(
            dataset_key=dataset_key,
            split_name=split_name,
            metric_records=metric_records,
            popularity_source=popularity_source,
        )
        write_json(output_path / f"{output_split}_metrics.json", metrics)
        metrics_by_split[split_name] = metrics
        counts_by_split[split_name] = {"n_predictions": len(predictions)}

    run_summary = {
        "model": "popularity",
        "dataset": dataset_key,
        "splits": normalized_splits,
        "limit": limit,
        "candidate_files": _resolved_candidate_files_for_summary(
            config,
            dataset_key,
            normalized_splits,
            candidate_files,
        ),
        "outputs_dir": str(output_path),
        "counts": counts_by_split,
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "popularity_source": popularity_source,
        "unique_popularity_items": len(popularity),
        "ranking_scoring": f"{popularity_source}_popularity",
    }
    write_json(output_path / "run_summary.json", run_summary)

    return {
        "dataset": dataset_key,
        "candidate_files": run_summary["candidate_files"],
        "outputs_dir": str(output_path),
        "counts": counts_by_split,
        "metrics": metrics_by_split,
    }


def _load_popularity(
    config: dict[str, Any],
    dataset_key: str,
    source: str,
) -> Counter[str]:
    if source == "n_train_targets":
        train_path = resolve_configured_output_path(
            config,
            dataset_key,
            "next_item_samples",
            "train",
        )
    elif source == "preference_train_targets":
        train_path = resolve_configured_output_path(
            config,
            dataset_key,
            "preference_samples",
            "train",
        )
    else:
        raise ValueError(f"Unsupported popularity_source: {source}")

    popularity: Counter[str] = Counter()
    for record in _iter_jsonl(train_path):
        target = record.get("target", {})
        movie_id = target.get("movie_id", record.get("ground_truth_movie_id"))
        popularity[str(movie_id)] += 1
    return popularity


def _predict_records(
    records: list[dict[str, Any]],
    popularity: Counter[str],
    split_name: str,
    popularity_source: str,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    predictions = []
    metric_records = []
    for record in records:
        label_set = list(record.get("label_set", []))
        if not label_set:
            label_set = [chr(ord("A") + index) for index in range(len(record["candidate_movie_ids"]))]
        scores = [
            float(popularity.get(str(movie_id), 0))
            for movie_id in record["candidate_movie_ids"]
        ]
        best_index = max(range(len(scores)), key=lambda index: (scores[index], -index))
        prediction = {
            "model": "popularity",
            "task": "N",
            "inference_mode": f"{popularity_source}_popularity",
            "split": split_name,
            "user_id": record["user_id"],
            "candidate_movie_ids": [str(movie_id) for movie_id in record["candidate_movie_ids"]],
            "ground_truth_index": int(record["ground_truth_index"]),
            "ground_truth_movie_id": str(record["ground_truth_movie_id"]),
            "label": record.get("label"),
            "label_set": label_set,
            "candidate_generation": record.get("candidate_generation"),
            "label_scores": dict(zip(label_set, scores)),
            "scores": scores,
            "predicted_label": label_set[best_index],
            "popularity_source": popularity_source,
            "scoring_mode": f"{popularity_source}_popularity",
        }
        predictions.append(prediction)
        metric_records.append(
            {
                "scores": scores,
                "ground_truth_index": int(record["ground_truth_index"]),
            }
        )
    return predictions, metric_records


def _metrics_for_split(
    dataset_key: str,
    split_name: str,
    metric_records: list[dict[str, Any]],
    popularity_source: str,
) -> dict[str, Any]:
    ranking = aggregate_ranking_metrics(metric_records, ks=_ranking_metric_ks(metric_records))
    return {
        "model": "popularity",
        "dataset": dataset_key,
        "split": split_name,
        "ranking": {**ranking, "samples": len(metric_records)},
        "ranking_scoring": f"{popularity_source}_popularity",
    }


def _iter_jsonl(path: str | Path):
    with open_text_auto(path, "rt", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                yield json.loads(line)


def _ranking_metric_ks(records: list[dict[str, Any]]) -> list[int]:
    candidate_count = max((len(record["scores"]) for record in records), default=5)
    return default_ranking_ks(candidate_count) or [candidate_count]


def _read_candidate_records(
    config: dict[str, Any],
    dataset_key: str,
    split_name: str,
    limit: int | None,
    candidate_files: dict[str, str | Path] | None = None,
) -> list[dict[str, Any]]:
    return read_jsonl(_candidate_path(config, dataset_key, split_name, candidate_files), limit=limit)


def _candidate_path(
    config: dict[str, Any],
    dataset_key: str,
    split_name: str,
    candidate_files: dict[str, str | Path] | None = None,
) -> Path:
    save_key = "validation" if split_name == "validation" else "test"
    if candidate_files and save_key in candidate_files:
        path = Path(candidate_files[save_key])
        if path.is_absolute():
            return path
        return Path(config["_repo_root"]) / path
    raw_path = config["candidates"]["save_files"][save_key]
    return resolve_repo_path_from_config(
        config,
        raw_path,
        dataset_key=dataset_key,
        split_name=split_name,
    )


def _resolved_candidate_files_for_summary(
    config: dict[str, Any],
    dataset_key: str,
    splits: list[str],
    candidate_files: dict[str, str | Path] | None = None,
) -> dict[str, str]:
    return {
        split_name: str(_candidate_path(config, dataset_key, split_name, candidate_files))
        for split_name in splits
    }


def _resolve_output_dir(
    config: dict[str, Any],
    dataset_key: str,
    output_dir: str | Path | None,
) -> Path:
    if output_dir is not None:
        path = Path(output_dir)
        if path.is_absolute():
            return path
        return Path(config["_repo_root"]) / path
    return Path(config["_repo_root"]) / "outputs" / "baselines" / dataset_key / "popularity"


def _config_snapshot(config: dict[str, Any]) -> dict[str, Any]:
    return {
        key: value
        for key, value in config.items()
        if key != "_repo_root"
    }


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


def _normalize_splits(splits: list[str]) -> list[str]:
    normalized = []
    for split in splits:
        key = split.strip().lower()
        if key not in SPLIT_ALIASES:
            raise ValueError(f"Unknown split: {split}")
        value = SPLIT_ALIASES[key]
        if value not in normalized:
            normalized.append(value)
    return normalized


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a popularity baseline on fixed N candidates")
    parser.add_argument("--config", default="configs/experiment.yaml")
    parser.add_argument("--dataset", default=None)
    parser.add_argument("--splits", nargs="+", default=["validation", "test"])
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--output-dir", default=None)
    parser.add_argument("--valid-candidates", default=None)
    parser.add_argument("--test-candidates", default=None)
    parser.add_argument(
        "--popularity-source",
        choices=["n_train_targets", "preference_train_targets"],
        default="n_train_targets",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    summary = run_popularity_baseline(
        config_path=args.config,
        dataset_key=args.dataset,
        splits=args.splits,
        limit=args.limit,
        output_dir=args.output_dir,
        candidate_files=_candidate_file_overrides(
            args.valid_candidates,
            args.test_candidates,
        ),
        popularity_source=args.popularity_source,
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
