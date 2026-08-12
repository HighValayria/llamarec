"""Summarize the SASRec N-sample-exposure-matched diagnostic."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any

from src.data.config import load_experiment_config


UNAVAILABLE = "unavailable"
TARGET_N_EXPOSURE = 12_000
SASREC_EXP_MATCH_STEPS = 23
SASREC_EXP_MATCH_EFFECTIVE_BATCH = 512
SASREC_EXP_MATCH_EXPOSURE = SASREC_EXP_MATCH_STEPS * SASREC_EXP_MATCH_EFFECTIVE_BATCH

DEFAULT_RUNS = {
    "N-K0": {
        "metrics": "outputs/n/movielens-1m/pool200k_1m_n_1500_popmatch_eval/test_metrics.json",
        "run_summary": "outputs/n/movielens-1m/pool200k_1m_n_1500/run_summary.json",
        "n_exposure": TARGET_N_EXPOSURE,
        "optimizer_steps": 1500,
        "effective_batch": 8,
        "role": "primary_llm",
    },
    "SASRec-exp-match": {
        "metrics": "outputs/baselines/movielens-1m/sasrec_exp_match_k5_popmatch_seed42_s23/test_metrics.json",
        "run_summary": "outputs/baselines/movielens-1m/sasrec_exp_match_k5_popmatch_seed42_s23/run_summary.json",
        "n_exposure": SASREC_EXP_MATCH_EXPOSURE,
        "optimizer_steps": SASREC_EXP_MATCH_STEPS,
        "effective_batch": SASREC_EXP_MATCH_EFFECTIVE_BATCH,
        "role": "primary_sasrec",
    },
    "M1 supplemental": {
        "metrics": "outputs/m/movielens-1m/diag_m1_1m_m_200k_3000_popmatch_eval/test_metrics.json",
        "run_summary": "outputs/m/movielens-1m/diag_m1_1m_m_200k_3000/run_summary.json",
        "n_exposure": TARGET_N_EXPOSURE,
        "total_exposure": 24_000,
        "optimizer_steps": 3000,
        "effective_batch": 8,
        "role": "supplemental_multitask",
    },
}


def run_sample_exposure_matched_diagnostic(
    config_path: str | Path,
    dataset_key: str = "movielens-1m",
    output_dir: str | Path | None = None,
    runs: dict[str, dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Write comparison rows for N-K0 and roughly exposure-matched SASRec."""

    config = load_experiment_config(config_path)
    repo_root = Path(config["_repo_root"])
    output_path = _resolve_path(
        repo_root,
        output_dir or "outputs/fair_budget_baseline_positioning",
    )
    output_path.mkdir(parents=True, exist_ok=True)

    rows = [_metric_row(repo_root, model, spec) for model, spec in (runs or DEFAULT_RUNS).items()]
    payload = {
        "dataset": dataset_key,
        "protocol": "N-sample-exposure roughly matched diagnostic",
        "target_n_exposure": TARGET_N_EXPOSURE,
        "sasrec_match": {
            "target_exposure": TARGET_N_EXPOSURE,
            "actual_exposure": SASREC_EXP_MATCH_EXPOSURE,
            "relative_mismatch_percent": _round(
                (SASREC_EXP_MATCH_EXPOSURE - TARGET_N_EXPOSURE) / TARGET_N_EXPOSURE * 100
            ),
            "match_status": "roughly exposure matched",
        },
        "rows": rows,
        "gaps": _gap_rows(rows),
        "answers": _answers(rows),
    }

    csv_path = output_path / "sample_exposure_matched_diagnostic.csv"
    json_path = output_path / "sample_exposure_matched_diagnostic.json"
    markdown_path = output_path / "sample_exposure_matched_diagnostic.md"
    _write_csv(csv_path, rows)
    _write_json(json_path, payload)
    _write_markdown(markdown_path, payload)

    return {
        "dataset": dataset_key,
        "rows": len(rows),
        "missing_rows": sum(1 for row in rows if row["evidence_status"] != "computed"),
        "paths": {
            "csv": str(csv_path),
            "json": str(json_path),
            "markdown": str(markdown_path),
        },
    }


def _metric_row(repo_root: Path, model: str, spec: dict[str, Any]) -> dict[str, Any]:
    metrics_path = _resolve_path(repo_root, spec["metrics"])
    run_summary_path = _resolve_path(repo_root, spec["run_summary"])
    if not metrics_path.exists():
        return _missing_row(model, spec, metrics_path, run_summary_path)
    metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
    ranking = metrics.get("ranking", {})
    run_summary = (
        json.loads(run_summary_path.read_text(encoding="utf-8"))
        if run_summary_path.exists()
        else {}
    )
    n_exposure = int(spec["n_exposure"])
    row = {
        "Model": model,
        "role": spec.get("role", ""),
        "N-task exposure": n_exposure,
        "total exposure": spec.get("total_exposure", n_exposure),
        "optimizer steps": spec["optimizer_steps"],
        "effective batch": spec["effective_batch"],
        "target exposure": TARGET_N_EXPOSURE,
        "actual exposure": n_exposure,
        "relative mismatch %": _round((n_exposure - TARGET_N_EXPOSURE) / TARGET_N_EXPOSURE * 100),
        "HR@1": _value(ranking.get("HR@1")),
        "NDCG@5": _value(ranking.get("NDCG@5")),
        "MRR": _value(ranking.get("MRR")),
        "samples": ranking.get("samples", UNAVAILABLE),
        "evidence_status": "computed",
        "match_status": "exact target" if n_exposure == TARGET_N_EXPOSURE else "roughly exposure matched",
        "metrics_path": str(metrics_path),
        "run_summary_path": str(run_summary_path),
        "training_stop": run_summary.get("training_stop", UNAVAILABLE),
    }
    return row


def _missing_row(
    model: str,
    spec: dict[str, Any],
    metrics_path: Path,
    run_summary_path: Path,
) -> dict[str, Any]:
    n_exposure = int(spec["n_exposure"])
    return {
        "Model": model,
        "role": spec.get("role", ""),
        "N-task exposure": n_exposure,
        "total exposure": spec.get("total_exposure", n_exposure),
        "optimizer steps": spec["optimizer_steps"],
        "effective batch": spec["effective_batch"],
        "target exposure": TARGET_N_EXPOSURE,
        "actual exposure": n_exposure,
        "relative mismatch %": _round((n_exposure - TARGET_N_EXPOSURE) / TARGET_N_EXPOSURE * 100),
        "HR@1": UNAVAILABLE,
        "NDCG@5": UNAVAILABLE,
        "MRR": UNAVAILABLE,
        "samples": UNAVAILABLE,
        "evidence_status": "missing_metrics_file",
        "match_status": "exact target" if n_exposure == TARGET_N_EXPOSURE else "roughly exposure matched",
        "metrics_path": str(metrics_path),
        "run_summary_path": str(run_summary_path),
        "training_stop": UNAVAILABLE,
    }


def _gap_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_model = {row["Model"]: row for row in rows}
    output = []
    n_k0 = by_model.get("N-K0")
    sasrec = by_model.get("SASRec-exp-match")
    m1 = by_model.get("M1 supplemental")
    if n_k0 and sasrec:
        output.append(_gap_row("SASRec-exp-match_minus_N-K0", sasrec, n_k0))
    if m1 and n_k0:
        output.append(_gap_row("M1_supplemental_minus_N-K0", m1, n_k0))
    return output


def _gap_row(label: str, left: dict[str, Any], right: dict[str, Any]) -> dict[str, Any]:
    return {
        "comparison": label,
        "evidence_status": _combined_status(left, right),
        "delta_HR@1": _delta(left["HR@1"], right["HR@1"]),
        "delta_NDCG@5": _delta(left["NDCG@5"], right["NDCG@5"]),
        "delta_MRR": _delta(left["MRR"], right["MRR"]),
    }


def _answers(rows: list[dict[str, Any]]) -> dict[str, str]:
    by_model = {row["Model"]: row for row in rows}
    n_k0 = by_model.get("N-K0")
    sasrec = by_model.get("SASRec-exp-match")
    if not n_k0 or not sasrec or n_k0["evidence_status"] != "computed" or sasrec["evidence_status"] != "computed":
        return {
            "sasrec_greater_than_n_k0_after_exposure_match": "unavailable until N-K0 and SASRec-exp-match metrics exist",
            "interpretation": "unavailable",
        }
    hr_gap = _delta(sasrec["HR@1"], n_k0["HR@1"])
    if isinstance(hr_gap, float) and hr_gap > 0:
        result = "yes by HR@1 under roughly matched N-task sample exposure"
    elif isinstance(hr_gap, float) and hr_gap < 0:
        result = "no by HR@1 under roughly matched N-task sample exposure"
    else:
        result = "tied by HR@1 under roughly matched N-task sample exposure"
    return {
        "sasrec_greater_than_n_k0_after_exposure_match": result,
        "interpretation": "single diagnostic only; do not turn into a final claim without replication",
    }


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
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def _write_markdown(path: Path, payload: dict[str, Any]) -> None:
    rows = payload["rows"]
    lines = [
        "# Sample-Exposure-Matched Diagnostic",
        "",
        f"Dataset: `{payload['dataset']}`.",
        f"Protocol: `{payload['protocol']}`.",
        "",
        "## Exposure Match",
        "",
        f"- Target N-task exposure: {payload['sasrec_match']['target_exposure']}.",
        f"- SASRec actual exposure: {payload['sasrec_match']['actual_exposure']}.",
        f"- Relative mismatch: {payload['sasrec_match']['relative_mismatch_percent']}%.",
        f"- Status: {payload['sasrec_match']['match_status']}.",
        "",
        "## Metrics",
        "",
        "| Model | N-task exposure | optimizer steps | effective batch | HR@1 | NDCG@5 | MRR | samples | match_status | evidence_status |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---|---|",
    ]
    for row in rows:
        lines.append(
            f"| {row['Model']} | {row['N-task exposure']} | {row['optimizer steps']} | "
            f"{row['effective batch']} | {row['HR@1']} | {row['NDCG@5']} | {row['MRR']} | "
            f"{row['samples']} | {row['match_status']} | {row['evidence_status']} |"
        )

    lines += [
        "",
        "## Gaps",
        "",
        "| comparison | delta_HR@1 | delta_NDCG@5 | delta_MRR | evidence_status |",
        "|---|---:|---:|---:|---|",
    ]
    for row in payload["gaps"]:
        lines.append(
            f"| {row['comparison']} | {row['delta_HR@1']} | {row['delta_NDCG@5']} | "
            f"{row['delta_MRR']} | {row['evidence_status']} |"
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
        "This is a roughly N-sample-exposure-matched diagnostic, not an exact compute-matched comparison. M1 is supplemental because total Y+N exposure is not pure N supervision.",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Write sample-exposure-matched diagnostic")
    parser.add_argument("--config", default="configs/experiment.yaml")
    parser.add_argument("--dataset", default="movielens-1m")
    parser.add_argument("--output-dir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    summary = run_sample_exposure_matched_diagnostic(
        config_path=args.config,
        dataset_key=args.dataset,
        output_dir=args.output_dir,
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
