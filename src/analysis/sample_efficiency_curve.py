"""Summarize N-K0 and SASRec sample-efficiency curve points."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any

from src.data.config import load_experiment_config
from src.analysis.training_budget_audit import sasrec_processed_instances


UNAVAILABLE = "unavailable"
DEFAULT_OUTPUT_DIR = "outputs/sample_efficiency_training_efficiency"
METRICS = ["HR@1", "NDCG@5", "MRR"]


DEFAULT_CURVE_POINTS = [
    {
        "model": "N-K0",
        "point": "n_s375",
        "family": "llm",
        "n_exposure": 3_000,
        "total_exposure": 3_000,
        "optimizer_steps": 375,
        "effective_batch": 8,
        "metrics": "outputs/n/movielens-1m/sample_efficiency_n_s375_popmatch_eval/test_metrics.json",
        "run_summary": "outputs/n/movielens-1m/sample_efficiency_n_s375/run_summary.json",
        "evaluation_summary": "outputs/n/movielens-1m/sample_efficiency_n_s375_popmatch_eval/evaluation_summary.json",
    },
    {
        "model": "N-K0",
        "point": "n_s750",
        "family": "llm",
        "n_exposure": 6_000,
        "total_exposure": 6_000,
        "optimizer_steps": 750,
        "effective_batch": 8,
        "metrics": "outputs/n/movielens-1m/sample_efficiency_n_s750_popmatch_eval/test_metrics.json",
        "run_summary": "outputs/n/movielens-1m/sample_efficiency_n_s750/run_summary.json",
        "evaluation_summary": "outputs/n/movielens-1m/sample_efficiency_n_s750_popmatch_eval/evaluation_summary.json",
    },
    {
        "model": "N-K0",
        "point": "n_s1500",
        "family": "llm",
        "n_exposure": 12_000,
        "total_exposure": 12_000,
        "optimizer_steps": 1500,
        "effective_batch": 8,
        "metrics": "outputs/n/movielens-1m/pool200k_1m_n_1500_popmatch_eval/test_metrics.json",
        "run_summary": "outputs/n/movielens-1m/pool200k_1m_n_1500/run_summary.json",
        "evaluation_summary": "outputs/n/movielens-1m/pool200k_1m_n_1500_popmatch_eval/evaluation_summary.json",
    },
    {
        "model": "N-K0",
        "point": "n_s3000",
        "family": "llm",
        "n_exposure": 24_000,
        "total_exposure": 24_000,
        "optimizer_steps": 3000,
        "effective_batch": 8,
        "metrics": "outputs/n/movielens-1m/sample_efficiency_n_s3000_popmatch_eval/test_metrics.json",
        "run_summary": "outputs/n/movielens-1m/sample_efficiency_n_s3000/run_summary.json",
        "evaluation_summary": "outputs/n/movielens-1m/sample_efficiency_n_s3000_popmatch_eval/evaluation_summary.json",
    },
    {
        "model": "SASRec",
        "point": "sasrec_s6",
        "family": "sasrec",
        "n_exposure": sasrec_processed_instances(200_000, 512, 6),
        "total_exposure": sasrec_processed_instances(200_000, 512, 6),
        "optimizer_steps": 6,
        "effective_batch": 512,
        "metrics": "outputs/baselines/movielens-1m/sample_efficiency_sasrec_s6_popmatch_eval/test_metrics.json",
        "run_summary": "outputs/baselines/movielens-1m/sample_efficiency_sasrec_s6/run_summary.json",
    },
    {
        "model": "SASRec",
        "point": "sasrec_s12",
        "family": "sasrec",
        "n_exposure": sasrec_processed_instances(200_000, 512, 12),
        "total_exposure": sasrec_processed_instances(200_000, 512, 12),
        "optimizer_steps": 12,
        "effective_batch": 512,
        "metrics": "outputs/baselines/movielens-1m/sample_efficiency_sasrec_s12_popmatch_eval/test_metrics.json",
        "run_summary": "outputs/baselines/movielens-1m/sample_efficiency_sasrec_s12/run_summary.json",
    },
    {
        "model": "SASRec",
        "point": "sasrec_s23",
        "family": "sasrec",
        "n_exposure": sasrec_processed_instances(200_000, 512, 23),
        "total_exposure": sasrec_processed_instances(200_000, 512, 23),
        "optimizer_steps": 23,
        "effective_batch": 512,
        "metrics": "outputs/baselines/movielens-1m/sasrec_exp_match_k5_popmatch_seed42_s23/test_metrics.json",
        "run_summary": "outputs/baselines/movielens-1m/sasrec_exp_match_k5_popmatch_seed42_s23/run_summary.json",
    },
    {
        "model": "SASRec",
        "point": "sasrec_s47",
        "family": "sasrec",
        "n_exposure": sasrec_processed_instances(200_000, 512, 47),
        "total_exposure": sasrec_processed_instances(200_000, 512, 47),
        "optimizer_steps": 47,
        "effective_batch": 512,
        "metrics": "outputs/baselines/movielens-1m/sample_efficiency_sasrec_s47_popmatch_eval/test_metrics.json",
        "run_summary": "outputs/baselines/movielens-1m/sample_efficiency_sasrec_s47/run_summary.json",
    },
    {
        "model": "SASRec",
        "point": "sasrec_s1500",
        "family": "sasrec",
        "n_exposure": sasrec_processed_instances(200_000, 512, 1500),
        "total_exposure": sasrec_processed_instances(200_000, 512, 1500),
        "optimizer_steps": 1500,
        "effective_batch": 512,
        "metrics": "outputs/baselines/movielens-1m/sasrec_fixed_popmatch_k5_200k_s1500_eval/test_metrics.json",
        "run_summary": "outputs/baselines/movielens-1m/sasrec_fixed_canonical_k5_200k_s1500/run_summary.json",
    },
    {
        "model": "SASRec",
        "point": "sasrec_s3000",
        "family": "sasrec",
        "n_exposure": sasrec_processed_instances(200_000, 512, 3000),
        "total_exposure": sasrec_processed_instances(200_000, 512, 3000),
        "optimizer_steps": 3000,
        "effective_batch": 512,
        "metrics": "outputs/baselines/movielens-1m/sasrec_fixed_popmatch_k5_200k_s3000_eval/test_metrics.json",
        "run_summary": "outputs/baselines/movielens-1m/sasrec_fixed_canonical_k5_200k_s3000/run_summary.json",
    },
]


def run_sample_efficiency_curve(
    config_path: str | Path,
    dataset_key: str = "movielens-1m",
    output_dir: str | Path | None = None,
    points: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Write sample-efficiency curve rows and closest-exposure gaps."""

    config = load_experiment_config(config_path)
    repo_root = Path(config["_repo_root"])
    output_path = _resolve_path(repo_root, output_dir or DEFAULT_OUTPUT_DIR)
    output_path.mkdir(parents=True, exist_ok=True)

    rows = [_curve_row(repo_root, spec) for spec in (points or DEFAULT_CURVE_POINTS)]
    gap_rows = _closest_gap_rows(rows)
    payload = {
        "dataset": dataset_key,
        "protocol": "N-task sample-efficiency curve on fixed popmatch candidates",
        "rows": rows,
        "closest_exposure_gaps": gap_rows,
        "answers": _answers(rows, gap_rows),
        "boundary": "This is a sample-exposure curve, not strict compute/capacity matching.",
    }

    csv_path = output_path / "sample_efficiency_curve.csv"
    gaps_csv_path = output_path / "sample_efficiency_curve_gaps.csv"
    json_path = output_path / "sample_efficiency_curve.json"
    markdown_path = output_path / "sample_efficiency_curve.md"
    _write_csv(csv_path, rows)
    _write_csv(gaps_csv_path, gap_rows)
    _write_json(json_path, payload)
    _write_markdown(markdown_path, payload)

    return {
        "dataset": dataset_key,
        "rows": len(rows),
        "computed_rows": sum(1 for row in rows if row["evidence_status"] == "computed"),
        "missing_rows": sum(1 for row in rows if row["evidence_status"] != "computed"),
        "closest_gap_rows": len(gap_rows),
        "paths": {
            "csv": str(csv_path),
            "gaps_csv": str(gaps_csv_path),
            "json": str(json_path),
            "markdown": str(markdown_path),
        },
    }


def _curve_row(repo_root: Path, spec: dict[str, Any]) -> dict[str, Any]:
    metrics_path = _resolve_path(repo_root, spec["metrics"])
    run_summary_path = _resolve_path(repo_root, spec.get("run_summary", ""))
    evaluation_summary_path = _resolve_path(repo_root, spec.get("evaluation_summary", ""))
    row = {
        "model": spec["model"],
        "point": spec["point"],
        "family": spec.get("family", spec["model"]),
        "N-task exposure": int(spec["n_exposure"]),
        "total exposure": int(spec.get("total_exposure", spec["n_exposure"])),
        "optimizer steps": int(spec["optimizer_steps"]),
        "effective batch": int(spec["effective_batch"]),
        "HR@1": UNAVAILABLE,
        "NDCG@5": UNAVAILABLE,
        "MRR": UNAVAILABLE,
        "samples": UNAVAILABLE,
        "candidate_protocol": spec.get("candidate_protocol", "k5_popmatch_seed42"),
        "evidence_status": "missing_metrics_file",
        "training_stop": UNAVAILABLE,
        "metrics_path": str(metrics_path),
        "run_summary_path": str(run_summary_path) if spec.get("run_summary") else "",
        "evaluation_summary_path": (
            str(evaluation_summary_path) if spec.get("evaluation_summary") else ""
        ),
    }
    if not metrics_path.exists():
        return row

    metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
    ranking = metrics.get("ranking", {})
    row.update(
        {
            "HR@1": _value(ranking.get("HR@1")),
            "NDCG@5": _value(ranking.get("NDCG@5")),
            "MRR": _value(ranking.get("MRR")),
            "samples": ranking.get("samples", UNAVAILABLE),
            "evidence_status": "computed",
        }
    )
    if run_summary_path.exists():
        run_summary = json.loads(run_summary_path.read_text(encoding="utf-8"))
        row["training_stop"] = run_summary.get("training_stop", UNAVAILABLE)
    if evaluation_summary_path.exists():
        evaluation_summary = json.loads(evaluation_summary_path.read_text(encoding="utf-8"))
        candidate_files = evaluation_summary.get("candidate_files", {})
        row["candidate_protocol"] = _candidate_protocol(candidate_files) or row["candidate_protocol"]
    return row


def _closest_gap_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    n_rows = [row for row in rows if row["model"] == "N-K0"]
    s_rows = [row for row in rows if row["model"] == "SASRec"]
    output = []
    for n_row in n_rows:
        if not s_rows:
            continue
        closest = min(
            s_rows,
            key=lambda row: abs(int(row["N-task exposure"]) - int(n_row["N-task exposure"])),
        )
        output.append(_gap_row(n_row, closest))
    return output


def _gap_row(n_row: dict[str, Any], sasrec_row: dict[str, Any]) -> dict[str, Any]:
    return {
        "comparison": f"{sasrec_row['point']}_minus_{n_row['point']}",
        "n_point": n_row["point"],
        "sasrec_point": sasrec_row["point"],
        "n_exposure": n_row["N-task exposure"],
        "sasrec_exposure": sasrec_row["N-task exposure"],
        "relative_exposure_mismatch %": _round(
            (
                (int(sasrec_row["N-task exposure"]) - int(n_row["N-task exposure"]))
                / int(n_row["N-task exposure"])
                * 100
            )
        ),
        "delta_HR@1": _delta(sasrec_row["HR@1"], n_row["HR@1"]),
        "delta_NDCG@5": _delta(sasrec_row["NDCG@5"], n_row["NDCG@5"]),
        "delta_MRR": _delta(sasrec_row["MRR"], n_row["MRR"]),
        "evidence_status": _combined_status(n_row, sasrec_row),
    }


def _answers(rows: list[dict[str, Any]], gap_rows: list[dict[str, Any]]) -> dict[str, str]:
    computed = [row for row in rows if row["evidence_status"] == "computed"]
    if len(computed) < 2 or any(row["evidence_status"] != "computed" for row in gap_rows):
        return {
            "curve_status": "incomplete until all planned curve metrics exist",
            "sample_efficiency_claim": "unavailable",
            "next_action": "run missing cloud training/eval points, then regenerate this report",
        }
    positive_gaps = [
        row for row in gap_rows
        if isinstance(row["delta_HR@1"], float) and row["delta_HR@1"] > 0
    ]
    return {
        "curve_status": "computed for planned points",
        "sample_efficiency_claim": (
            "SASRec exceeds N-K0 at at least one closest-exposure point by HR@1"
            if positive_gaps
            else "SASRec does not exceed N-K0 at closest-exposure points by HR@1"
        ),
        "next_action": "interpret curve with candidate-size and cold-slice diagnostics before making durable claims",
    }


def _candidate_protocol(candidate_files: Any) -> str | None:
    if not isinstance(candidate_files, dict):
        return None
    test_path = str(candidate_files.get("test") or "")
    if not test_path:
        return None
    marker = "variants/"
    if marker not in test_path:
        return "canonical"
    after = test_path.split(marker, 1)[1]
    return after.split("/", 1)[0].split("\\", 1)[0]


def _combined_status(left: dict[str, Any], right: dict[str, Any]) -> str:
    if left["evidence_status"] == "computed" and right["evidence_status"] == "computed":
        return "computed"
    return f"{left['evidence_status']}; {right['evidence_status']}"


def _value(value: Any) -> float | str:
    if value is None or value == "":
        return UNAVAILABLE
    return _round(float(value))


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
        "# Sample-Efficiency Curve",
        "",
        f"Dataset: `{payload['dataset']}`.",
        f"Protocol: `{payload['protocol']}`.",
        "",
        "## Curve Points",
        "",
        "| model | point | N-task exposure | optimizer steps | effective batch | HR@1 | NDCG@5 | MRR | samples | evidence_status |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in payload["rows"]:
        lines.append(
            f"| {row['model']} | {row['point']} | {row['N-task exposure']} | "
            f"{row['optimizer steps']} | {row['effective batch']} | {row['HR@1']} | "
            f"{row['NDCG@5']} | {row['MRR']} | {row['samples']} | {row['evidence_status']} |"
        )

    lines += [
        "",
        "## Closest Exposure Gaps",
        "",
        "| comparison | n_exposure | sasrec_exposure | mismatch % | delta_HR@1 | delta_NDCG@5 | delta_MRR | evidence_status |",
        "|---|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in payload["closest_exposure_gaps"]:
        lines.append(
            f"| {row['comparison']} | {row['n_exposure']} | {row['sasrec_exposure']} | "
            f"{row['relative_exposure_mismatch %']} | {row['delta_HR@1']} | "
            f"{row['delta_NDCG@5']} | {row['delta_MRR']} | {row['evidence_status']} |"
        )

    lines += [
        "",
        "## Direct Answers",
        "",
    ]
    for key, value in payload["answers"].items():
        lines.append(f"- {key}: {value}")
    lines += [
        "",
        "## Boundary",
        "",
        payload["boundary"],
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Write N-K0/SASRec sample-efficiency curve")
    parser.add_argument("--config", default="configs/experiment.yaml")
    parser.add_argument("--dataset", default="movielens-1m")
    parser.add_argument("--output-dir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    summary = run_sample_efficiency_curve(
        config_path=args.config,
        dataset_key=args.dataset,
        output_dir=args.output_dir,
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
