"""Cold/tail target-popularity slice synthesis for fixed candidate runs."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path
from typing import Any

from src.analysis.phase2c_popmatch_grouped import (
    _candidate_target_buckets,
    _load_movie_popularity,
    _model_bucket_rows,
)
from src.data.config import load_experiment_config


BUCKET_ORDER = ["<=10", "11-50", "51-200", "201-500", ">500"]
METRICS = ["HR@1", "NDCG@5", "MRR"]
UNAVAILABLE = "unavailable"

DEFAULT_RUNS = {
    "N-K0": "outputs/n/movielens-1m/pool200k_1m_n_1500_popmatch_eval/n_test_predictions.jsonl",
    "M1": "outputs/m/movielens-1m/diag_m1_1m_m_200k_3000_popmatch_eval/m_n_test_predictions.jsonl",
    "SASRec exp-match": "outputs/baselines/movielens-1m/sasrec_exp_match_k5_popmatch_seed42_s23/n_test_predictions.jsonl",
    "SASRec s47": "outputs/baselines/movielens-1m/sample_efficiency_sasrec_s47_popmatch_eval/n_test_predictions.jsonl",
    "SASRec s1500": "outputs/baselines/movielens-1m/sasrec_fixed_popmatch_k5_200k_s1500_eval/n_test_predictions.jsonl",
    "SASRec s3000": "outputs/baselines/movielens-1m/sasrec_fixed_popmatch_k5_200k_s3000_eval/n_test_predictions.jsonl",
}

DEFAULT_COMPARISONS = [
    ("N-K0", "M1"),
    ("SASRec exp-match", "N-K0"),
    ("SASRec s47", "N-K0"),
    ("SASRec s1500", "N-K0"),
    ("SASRec s3000", "N-K0"),
]


def run_cold_tail_slice_diagnostic(
    config_path: str | Path,
    dataset_key: str = "movielens-1m",
    split_name: str = "test",
    candidate_file: str | Path | None = None,
    output_dir: str | Path | None = None,
    runs: dict[str, str | Path] | None = None,
    comparisons: list[tuple[str, str]] | None = None,
) -> dict[str, Any]:
    """Write cold/tail bucket metrics and model deltas for prediction files."""

    config = load_experiment_config(config_path)
    repo_root = Path(config["_repo_root"])
    output_path = _resolve_path(
        repo_root,
        output_dir or "outputs/cold_tail_item_slice_diagnostic",
    )
    output_path.mkdir(parents=True, exist_ok=True)

    candidate_path = _resolve_path(
        repo_root,
        candidate_file
        or f"data/candidates/{dataset_key}/variants/k5_popmatch_seed42/{_split_file(split_name)}.jsonl",
    )
    movie_popularity = _load_movie_popularity(config, dataset_key)
    buckets = _candidate_target_buckets(candidate_path, movie_popularity)
    bucket_counts = Counter(buckets)

    rows, missing_runs = _bucket_rows(repo_root, buckets, runs or DEFAULT_RUNS)
    delta_rows = _delta_rows(rows, comparisons or DEFAULT_COMPARISONS)
    payload = {
        "dataset": dataset_key,
        "split": split_name,
        "candidate_file": str(candidate_path),
        "group_field": "target_popularity_bucket",
        "bucket_counts": {bucket: bucket_counts.get(bucket, 0) for bucket in BUCKET_ORDER},
        "rows": rows,
        "deltas": delta_rows,
        "missing_runs": missing_runs,
        "answers": _answers(rows, delta_rows, missing_runs),
        "boundary": (
            "This is a target-popularity slice diagnostic on fixed candidate "
            "prediction files, not a multi-seed or strict compute-matched claim."
        ),
    }

    csv_path = output_path / "cold_tail_slice_metrics.csv"
    deltas_csv_path = output_path / "cold_tail_slice_deltas.csv"
    json_path = output_path / "cold_tail_slice_diagnostic.json"
    markdown_path = output_path / "cold_tail_slice_diagnostic.md"
    _write_csv(csv_path, rows)
    _write_csv(deltas_csv_path, delta_rows)
    _write_json(json_path, payload)
    _write_markdown(markdown_path, payload)

    return {
        "dataset": dataset_key,
        "split": split_name,
        "models": len(runs or DEFAULT_RUNS),
        "rows": len(rows),
        "delta_rows": len(delta_rows),
        "missing_runs": len(missing_runs),
        "paths": {
            "csv": str(csv_path),
            "deltas_csv": str(deltas_csv_path),
            "json": str(json_path),
            "markdown": str(markdown_path),
        },
    }


def _bucket_rows(
    repo_root: Path,
    buckets: list[str],
    runs: dict[str, str | Path],
) -> tuple[list[dict[str, Any]], list[dict[str, str]]]:
    rows = []
    missing = []
    for model, raw_prediction_path in runs.items():
        prediction_path = _resolve_path(repo_root, raw_prediction_path)
        if not prediction_path.exists():
            missing.append(
                {
                    "model": model,
                    "prediction_path": str(prediction_path),
                    "reason": "prediction file not present",
                }
            )
            continue
        for row in _model_bucket_rows(model, prediction_path, buckets):
            rows.append(
                {
                    "model": row["model"],
                    "bucket": row["group_value"],
                    "sample_count": row["samples"],
                    "HR@1": row["HR@1"],
                    "NDCG@5": row["NDCG@5"],
                    "MRR": row["MRR"],
                    "mean_rank": row["mean_rank"],
                    "evidence_status": "computed_from_prediction_file",
                    "prediction_path": str(prediction_path),
                }
            )
    return rows, missing


def _delta_rows(
    rows: list[dict[str, Any]],
    comparisons: list[tuple[str, str]],
) -> list[dict[str, Any]]:
    by_model_bucket = {(row["model"], row["bucket"]): row for row in rows}
    output = []
    for left_model, right_model in comparisons:
        for bucket in BUCKET_ORDER:
            left = by_model_bucket.get((left_model, bucket))
            right = by_model_bucket.get((right_model, bucket))
            if not left or not right:
                continue
            output.append(_delta_row(left_model, right_model, bucket, left, right))
    return output


def _delta_row(
    left_model: str,
    right_model: str,
    bucket: str,
    left: dict[str, Any],
    right: dict[str, Any],
) -> dict[str, Any]:
    return {
        "comparison": f"{left_model}_minus_{right_model}",
        "left_model": left_model,
        "right_model": right_model,
        "bucket": bucket,
        "sample_count": left["sample_count"],
        "delta_HR@1": _delta(left["HR@1"], right["HR@1"]),
        "delta_NDCG@5": _delta(left["NDCG@5"], right["NDCG@5"]),
        "delta_MRR": _delta(left["MRR"], right["MRR"]),
        "delta_mean_rank": _delta(left["mean_rank"], right["mean_rank"]),
        "evidence_status": "computed",
    }


def _answers(
    rows: list[dict[str, Any]],
    delta_rows: list[dict[str, Any]],
    missing_runs: list[dict[str, str]],
) -> dict[str, str]:
    if missing_runs:
        return {
            "cold_tail_status": "incomplete until all requested prediction files exist",
            "n_k0_cold_tail_advantage": "unavailable",
            "sasrec_cold_tail_advantage": "unavailable",
            "next_action": "run missing eval-only prediction files or narrow runs, then regenerate",
        }
    if not rows:
        return {
            "cold_tail_status": "unavailable: no bucket rows were computed",
            "n_k0_cold_tail_advantage": "unavailable",
            "sasrec_cold_tail_advantage": "unavailable",
            "next_action": "provide prediction files and regenerate",
        }

    nk0_m1 = _comparison_bucket(delta_rows, "N-K0_minus_M1", "<=10", "delta_HR@1")
    sasrec_exp = _comparison_bucket(
        delta_rows,
        "SASRec exp-match_minus_N-K0",
        "<=10",
        "delta_HR@1",
    )
    sasrec_high = [
        _comparison_bucket(delta_rows, comparison, "<=10", "delta_HR@1")
        for comparison in ["SASRec s1500_minus_N-K0", "SASRec s3000_minus_N-K0"]
    ]
    high_available = [value for value in sasrec_high if isinstance(value, float)]

    return {
        "cold_tail_status": "computed for requested prediction files",
        "n_k0_cold_tail_advantage": _sign_answer(nk0_m1, "N-K0 exceeds M1", "M1 exceeds N-K0"),
        "sasrec_exposure_matched_cold_tail_advantage": _sign_answer(
            sasrec_exp,
            "SASRec exp-match exceeds N-K0",
            "N-K0 exceeds SASRec exp-match",
        ),
        "sasrec_high_exposure_cold_tail_advantage": (
            "mixed or unavailable"
            if not high_available
            else (
                "high-exposure SASRec exceeds N-K0 in the coldest bucket"
                if any(value > 0 for value in high_available)
                else "N-K0 exceeds high-exposure SASRec in the coldest bucket"
            )
        ),
        "next_action": "inspect low-sample cold buckets before making durable claims",
    }


def _comparison_bucket(
    rows: list[dict[str, Any]],
    comparison: str,
    bucket: str,
    metric: str,
) -> float | str:
    for row in rows:
        if row["comparison"] == comparison and row["bucket"] == bucket:
            return row.get(metric, UNAVAILABLE)
    return UNAVAILABLE


def _sign_answer(value: float | str, positive: str, negative: str) -> str:
    if not isinstance(value, float):
        return "unavailable"
    if value > 0:
        return positive
    if value < 0:
        return negative
    return "tie"


def _delta(left: Any, right: Any) -> float | str:
    left_value = _optional_float(left)
    right_value = _optional_float(right)
    if left_value is None or right_value is None:
        return UNAVAILABLE
    return _round(left_value - right_value)


def _optional_float(value: Any) -> float | None:
    if value is None or value == "" or value == UNAVAILABLE:
        return None
    return float(value)


def _round(value: float) -> float:
    return round(float(value), 10)


def _split_file(split_name: str) -> str:
    if split_name in {"validation", "valid"}:
        return "valid"
    if split_name == "test":
        return "test"
    raise ValueError(f"Unsupported split: {split_name}")


def _resolve_path(base: Path, path: str | Path) -> Path:
    output = Path(path)
    if output.is_absolute():
        return output
    return base / output


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def _write_markdown(path: Path, payload: dict[str, Any]) -> None:
    lines = [
        "# Cold/Tail Item Slice Diagnostic",
        "",
        f"Dataset: `{payload['dataset']}`.",
        f"Split: `{payload['split']}`.",
        f"Candidate file: `{payload['candidate_file']}`.",
        "",
        "## Target Popularity Buckets",
        "",
        "| bucket | sample_count |",
        "|---|---:|",
    ]
    for bucket, count in payload["bucket_counts"].items():
        lines.append(f"| {bucket} | {count} |")

    lines += [
        "",
        "## Metrics",
        "",
        "| model | bucket | samples | HR@1 | NDCG@5 | MRR | mean_rank | evidence_status |",
        "|---|---|---:|---:|---:|---:|---:|---|",
    ]
    for row in payload["rows"]:
        lines.append(
            f"| {row['model']} | {row['bucket']} | {row['sample_count']} | "
            f"{row['HR@1']} | {row['NDCG@5']} | {row['MRR']} | {row['mean_rank']} | "
            f"{row['evidence_status']} |"
        )

    lines += [
        "",
        "## Deltas",
        "",
        "| comparison | bucket | samples | delta_HR@1 | delta_NDCG@5 | delta_MRR | delta_mean_rank | evidence_status |",
        "|---|---|---:|---:|---:|---:|---:|---|",
    ]
    for row in payload["deltas"]:
        lines.append(
            f"| {row['comparison']} | {row['bucket']} | {row['sample_count']} | "
            f"{row['delta_HR@1']} | {row['delta_NDCG@5']} | {row['delta_MRR']} | "
            f"{row['delta_mean_rank']} | {row['evidence_status']} |"
        )

    lines += ["", "## Direct Answers", ""]
    for key, value in payload["answers"].items():
        lines.append(f"- {key}: {value}")

    if payload["missing_runs"]:
        lines += [
            "",
            "## Missing Runs",
            "",
            "| model | prediction_path | reason |",
            "|---|---|---|",
        ]
        for row in payload["missing_runs"]:
            lines.append(f"| {row['model']} | `{row['prediction_path']}` | {row['reason']} |")

    lines += ["", "## Boundary", "", payload["boundary"], ""]
    path.write_text("\n".join(lines), encoding="utf-8")


def _run_overrides(values: list[str] | None) -> dict[str, str] | None:
    if not values:
        return None
    runs = {}
    for value in values:
        if "=" not in value:
            raise ValueError("--run values must be MODEL=path")
        model, path = value.split("=", 1)
        runs[model] = path
    return runs


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Write cold/tail item slice diagnostics")
    parser.add_argument("--config", default="configs/experiment.yaml")
    parser.add_argument("--dataset", default="movielens-1m")
    parser.add_argument("--split", default="test", choices=["validation", "valid", "test"])
    parser.add_argument("--candidate-file", default=None)
    parser.add_argument("--output-dir", default=None)
    parser.add_argument("--run", action="append", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    summary = run_cold_tail_slice_diagnostic(
        config_path=args.config,
        dataset_key=args.dataset,
        split_name=args.split,
        candidate_file=args.candidate_file,
        output_dir=args.output_dir,
        runs=_run_overrides(args.run),
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
