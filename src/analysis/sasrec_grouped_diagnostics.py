"""SASRec grouped diagnostics for fair-budget baseline positioning."""

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
UNAVAILABLE = "unavailable"

DEFAULT_RUNS = {
    "N-K0": "outputs/n/movielens-1m/pool200k_1m_n_1500_popmatch_eval/n_test_predictions.jsonl",
    "M1": "outputs/m/movielens-1m/diag_m1_1m_m_200k_3000_popmatch_eval/m_n_test_predictions.jsonl",
    "SASRec s1500": "outputs/baselines/movielens-1m/sasrec_fixed_popmatch_k5_200k_s1500_eval/n_test_predictions.jsonl",
    "SASRec s3000": "outputs/baselines/movielens-1m/sasrec_fixed_popmatch_k5_200k_s3000_eval/n_test_predictions.jsonl",
}


def run_sasrec_grouped_diagnostics(
    config_path: str | Path,
    dataset_key: str = "movielens-1m",
    split_name: str = "test",
    candidate_file: str | Path | None = None,
    output_dir: str | Path | None = None,
    runs: dict[str, str | Path] | None = None,
) -> dict[str, Any]:
    """Write target-popularity grouped diagnostics for SASRec/LLM popmatch runs."""

    config = load_experiment_config(config_path)
    repo_root = Path(config["_repo_root"])
    output_path = _resolve_path(
        repo_root,
        output_dir or "outputs/fair_budget_baseline_positioning",
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

    rows: list[dict[str, Any]] = []
    missing_runs: list[dict[str, str]] = []
    for model, raw_prediction_path in (runs or DEFAULT_RUNS).items():
        prediction_path = _resolve_path(repo_root, raw_prediction_path)
        if not prediction_path.exists():
            missing_runs.append(
                {
                    "model": model,
                    "prediction_path": str(prediction_path),
                    "reason": "prediction file not present in local workspace",
                }
            )
            rows.extend(_missing_rows(model, prediction_path, bucket_counts))
            continue
        computed_rows = _model_bucket_rows(model, prediction_path, buckets)
        for row in computed_rows:
            rows.append(_normalize_computed_row(row, prediction_path))

    payload = {
        "dataset": dataset_key,
        "split": split_name,
        "candidate_file": str(candidate_path),
        "group_field": "target_popularity_bucket",
        "bucket_counts": {bucket: bucket_counts.get(bucket, 0) for bucket in BUCKET_ORDER},
        "missing_runs": missing_runs,
        "rows": rows,
        "answers": _answers(rows, missing_runs),
    }

    csv_path = output_path / "sasrec_grouped_diagnostics.csv"
    json_path = output_path / "sasrec_grouped_diagnostics.json"
    markdown_path = output_path / "sasrec_grouped_diagnostics.md"
    _write_csv(csv_path, rows)
    _write_json(json_path, payload)
    _write_markdown(markdown_path, payload)

    return {
        "dataset": dataset_key,
        "split": split_name,
        "models": len(runs or DEFAULT_RUNS),
        "rows": len(rows),
        "missing_runs": len(missing_runs),
        "paths": {
            "csv": str(csv_path),
            "json": str(json_path),
            "markdown": str(markdown_path),
        },
    }


def _missing_rows(
    model: str,
    prediction_path: Path,
    bucket_counts: Counter[str],
) -> list[dict[str, Any]]:
    return [
        {
            "model": model,
            "group_field": "target_popularity_bucket",
            "group_value": bucket,
            "sample_count": bucket_counts.get(bucket, 0),
            "HR@1": UNAVAILABLE,
            "NDCG@5": UNAVAILABLE,
            "MRR": UNAVAILABLE,
            "mean_rank": UNAVAILABLE,
            "evidence_status": "missing_prediction_file",
            "prediction_path": str(prediction_path),
        }
        for bucket in BUCKET_ORDER
        if bucket_counts.get(bucket, 0)
    ]


def _normalize_computed_row(row: dict[str, Any], prediction_path: Path) -> dict[str, Any]:
    return {
        "model": row["model"],
        "group_field": row["group_field"],
        "group_value": row["group_value"],
        "sample_count": row["samples"],
        "HR@1": row["HR@1"],
        "NDCG@5": row["NDCG@5"],
        "MRR": row["MRR"],
        "mean_rank": row["mean_rank"],
        "evidence_status": "computed_from_prediction_file",
        "prediction_path": str(prediction_path),
    }


def _answers(
    rows: list[dict[str, Any]],
    missing_runs: list[dict[str, str]],
) -> dict[str, str]:
    if missing_runs:
        return {
            "sasrec_popularity_dependence": "unavailable: formal per-record prediction files are missing locally",
            "cold_item_weakness_scope": "unavailable: cannot compare buckets without formal per-record prediction files",
            "sasrec_advantage_source": "unavailable: cannot attribute head/middle/tail advantage without formal per-record prediction files",
        }
    by_model: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        by_model.setdefault(str(row["model"]), []).append(row)
    sasrec_rows = by_model.get("SASRec s1500") or by_model.get("SASRec s3000") or []
    if not sasrec_rows:
        return {
            "sasrec_popularity_dependence": "unavailable: no SASRec rows were computed",
            "cold_item_weakness_scope": "unavailable: no SASRec rows were computed",
            "sasrec_advantage_source": "unavailable: no SASRec rows were computed",
        }
    head = _metric_for_bucket(sasrec_rows, ">500", "HR@1")
    tail = _metric_for_bucket(sasrec_rows, "<=10", "HR@1")
    dependence = "present" if head is not None and tail is not None and head > tail else "not established"
    return {
        "sasrec_popularity_dependence": dependence,
        "cold_item_weakness_scope": "computed; inspect CSV bucket rows for SASRec vs N-K0/M1",
        "sasrec_advantage_source": "computed; inspect per-bucket SASRec minus N-K0/M1 deltas manually",
    }


def _metric_for_bucket(
    rows: list[dict[str, Any]],
    bucket: str,
    metric: str,
) -> float | None:
    for row in rows:
        if row["group_value"] == bucket and row.get(metric) != UNAVAILABLE:
            return float(row[metric])
    return None


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
    fieldnames = [
        "model",
        "group_field",
        "group_value",
        "sample_count",
        "HR@1",
        "NDCG@5",
        "MRR",
        "mean_rank",
        "evidence_status",
        "prediction_path",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def _write_markdown(path: Path, payload: dict[str, Any]) -> None:
    lines = [
        "# SASRec Grouped Diagnostics",
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
        "| model | bucket | sample_count | HR@1 | NDCG@5 | MRR | mean_rank | evidence_status |",
        "|---|---|---:|---:|---:|---:|---:|---|",
    ]
    for row in payload["rows"]:
        lines.append(
            f"| {row['model']} | {row['group_value']} | {row['sample_count']} | "
            f"{row['HR@1']} | {row['NDCG@5']} | {row['MRR']} | {row['mean_rank']} | "
            f"{row['evidence_status']} |"
        )

    lines += [
        "",
        "## Direct Answers",
        "",
    ]
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
    lines += [
        "",
        "## Boundary",
        "",
        "Do not interpret unavailable rows as negative results. The current local workspace lacks the formal per-record prediction files needed for target-popularity grouped SASRec/N-K0/M1 metrics.",
        "",
    ]
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
    parser = argparse.ArgumentParser(description="Write SASRec grouped diagnostics")
    parser.add_argument("--config", default="configs/experiment.yaml")
    parser.add_argument("--dataset", default="movielens-1m")
    parser.add_argument("--split", default="test", choices=["validation", "valid", "test"])
    parser.add_argument("--candidate-file", default=None)
    parser.add_argument("--output-dir", default=None)
    parser.add_argument("--run", action="append", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    summary = run_sasrec_grouped_diagnostics(
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
