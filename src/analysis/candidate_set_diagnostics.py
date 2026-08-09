"""Phase 2C candidate-set diagnostics.

This module summarizes fixed N candidate files before model inference. It is
CPU-only and keeps the existing split/candidate/metric contracts intact.
"""

from __future__ import annotations

import argparse
import csv
from collections import Counter
from datetime import datetime, timezone
import json
from pathlib import Path
from statistics import mean
from typing import Any

from src.data.config import (
    load_experiment_config,
    open_text_auto,
    resolve_configured_output_path,
    resolve_repo_path_from_config,
)
from src.inference.prediction_io import write_json


def run_candidate_set_diagnostics(
    config_path: str | Path,
    dataset_key: str | None = None,
    candidate_files: dict[str, str | Path] | None = None,
    output_dir: str | Path | None = None,
    variant_name: str | None = None,
    splits: list[str] | tuple[str, ...] = ("validation", "test"),
) -> dict[str, Any]:
    """Write summary diagnostics for fixed candidate files."""

    config = load_experiment_config(config_path)
    dataset_key = dataset_key or config["dataset"]["formal"]
    output_path = _resolve_output_dir(config, dataset_key, output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    movie_popularity = _load_movie_popularity(config, dataset_key)
    rows = []
    candidate_paths = {}
    for split_name in splits:
        normalized_split = _normalize_split(split_name)
        path = _candidate_path(config, dataset_key, normalized_split, candidate_files)
        records = _read_jsonl(path)
        candidate_paths[normalized_split] = str(path)
        rows.append(
            _split_diagnostic_row(
                records,
                split_name=normalized_split,
                path=path,
                movie_popularity=movie_popularity,
                variant_name=variant_name,
            )
        )

    paths = {
        "csv": output_path / "candidate_set_diagnostics.csv",
        "json": output_path / "candidate_set_diagnostics.json",
        "report": output_path / "candidate_set_diagnostics.md",
    }
    _write_csv(paths["csv"], rows)
    write_json(
        paths["json"],
        {
            "dataset": dataset_key,
            "created_at_utc": datetime.now(timezone.utc).isoformat(),
            "candidate_files": candidate_paths,
            "diagnostics": rows,
        },
    )
    _write_markdown_report(paths["report"], dataset_key, rows)

    return {
        "dataset": dataset_key,
        "rows": len(rows),
        "output_dir": str(output_path),
        "paths": {name: str(path) for name, path in paths.items()},
    }


def _split_diagnostic_row(
    records: list[dict[str, Any]],
    split_name: str,
    path: Path,
    movie_popularity: Counter[str],
    variant_name: str | None,
) -> dict[str, Any]:
    candidate_counts = [len(record.get("candidate_movie_ids", [])) for record in records]
    target_popularities = []
    negative_popularities = []
    mean_negative_popularities = []
    mean_abs_popularity_gaps = []
    min_abs_popularity_gaps = []
    max_abs_popularity_gaps = []
    target_buckets = Counter()
    methods = Counter()
    variants = Counter()

    for record in records:
        generation = record.get("candidate_generation", {})
        methods[str(generation.get("method", "unknown"))] += 1
        variants[str(generation.get("variant_name", variant_name or "unknown"))] += 1

        ground_truth_movie_id = str(record["ground_truth_movie_id"])
        target_popularity = int(movie_popularity.get(ground_truth_movie_id, 0))
        negatives = [
            str(movie_id)
            for movie_id in record.get("candidate_movie_ids", [])
            if str(movie_id) != ground_truth_movie_id
        ]
        neg_pops = [int(movie_popularity.get(movie_id, 0)) for movie_id in negatives]
        gaps = [abs(value - target_popularity) for value in neg_pops]

        target_popularities.append(target_popularity)
        negative_popularities.extend(neg_pops)
        mean_negative_popularities.append(mean(neg_pops) if neg_pops else 0.0)
        mean_abs_popularity_gaps.append(mean(gaps) if gaps else 0.0)
        min_abs_popularity_gaps.append(min(gaps, default=0))
        max_abs_popularity_gaps.append(max(gaps, default=0))
        target_buckets[_target_popularity_bucket(target_popularity)] += 1

    return {
        "split": split_name,
        "path": str(path),
        "variant_name": _dominant_key(variants, variant_name or "unknown"),
        "method": _dominant_key(methods, "unknown"),
        "samples": len(records),
        "candidate_num_min": min(candidate_counts, default=0),
        "candidate_num_max": max(candidate_counts, default=0),
        "mean_target_popularity": _round(mean(target_popularities) if target_popularities else 0.0),
        "mean_negative_popularity": _round(mean(negative_popularities) if negative_popularities else 0.0),
        "mean_record_negative_popularity": _round(mean(mean_negative_popularities) if mean_negative_popularities else 0.0),
        "mean_abs_popularity_gap": _round(mean(mean_abs_popularity_gaps) if mean_abs_popularity_gaps else 0.0),
        "mean_min_abs_popularity_gap": _round(mean(min_abs_popularity_gaps) if min_abs_popularity_gaps else 0.0),
        "mean_max_abs_popularity_gap": _round(mean(max_abs_popularity_gaps) if max_abs_popularity_gaps else 0.0),
        "target_popularity_buckets": json.dumps(dict(sorted(target_buckets.items())), sort_keys=True),
    }


def _candidate_path(
    config: dict[str, Any],
    dataset_key: str,
    split_name: str,
    candidate_files: dict[str, str | Path] | None = None,
) -> Path:
    candidate_key = "validation" if split_name == "validation" else "test"
    if candidate_files and candidate_key in candidate_files:
        path = Path(candidate_files[candidate_key])
        if path.is_absolute():
            return path
        return Path(config["_repo_root"]) / path
    raw_path = config["candidates"]["save_files"][candidate_key]
    return resolve_repo_path_from_config(config, raw_path, dataset_key=dataset_key)


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


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    records = []
    with open_text_auto(path, "rt", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                records.append(json.loads(line))
    return records


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def _write_markdown_report(path: Path, dataset_key: str, rows: list[dict[str, Any]]) -> None:
    lines = [
        f"# {dataset_key} Candidate Set Diagnostics",
        "",
        f"Generated at: {datetime.now(timezone.utc).isoformat()}",
        "",
        _markdown_table(
            rows,
            [
                "split",
                "variant_name",
                "method",
                "samples",
                "candidate_num_min",
                "candidate_num_max",
                "mean_abs_popularity_gap",
                "mean_min_abs_popularity_gap",
                "mean_max_abs_popularity_gap",
            ],
        ),
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def _markdown_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._"
    output = [
        "| " + " | ".join(fields) + " |",
        "|" + "|".join("---" for _ in fields) + "|",
    ]
    for row in rows:
        output.append("| " + " | ".join(str(row.get(field, "")) for field in fields) + " |")
    return "\n".join(output)


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
    return Path(config["_repo_root"]) / "outputs" / "phase2c" / dataset_key / "candidate_set_diagnostics"


def _normalize_split(split_name: str) -> str:
    if split_name == "valid":
        return "validation"
    if split_name not in {"validation", "test"}:
        raise ValueError(f"Unsupported split: {split_name}")
    return split_name


def _target_popularity_bucket(value: int) -> str:
    if value <= 10:
        return "<=10"
    if value <= 50:
        return "11-50"
    if value <= 200:
        return "51-200"
    if value <= 500:
        return "201-500"
    return ">500"


def _dominant_key(counter: Counter[str], fallback: str) -> str:
    if not counter:
        return fallback
    if len(counter) == 1:
        return next(iter(counter))
    return "mixed:" + ",".join(f"{key}={counter[key]}" for key in sorted(counter))


def _round(value: float) -> float:
    return round(float(value), 10)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Phase 2C candidate-set diagnostics")
    parser.add_argument("--config", default="configs/experiment.yaml")
    parser.add_argument("--dataset", default=None)
    parser.add_argument("--variant-name", default=None)
    parser.add_argument("--output-dir", default=None)
    parser.add_argument("--splits", nargs="+", default=["validation", "test"])
    parser.add_argument("--valid-candidates", default=None)
    parser.add_argument("--test-candidates", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    summary = run_candidate_set_diagnostics(
        config_path=args.config,
        dataset_key=args.dataset,
        candidate_files=_candidate_file_overrides(
            args.valid_candidates,
            args.test_candidates,
        ),
        output_dir=args.output_dir,
        variant_name=args.variant_name,
        splits=args.splits,
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
