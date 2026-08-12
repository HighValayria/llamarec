"""Candidate-size robustness summary for SASRec and LLM ranking runs."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any

from src.data.config import load_experiment_config, open_text_auto
from src.eval.ranking_metrics import ground_truth_rank


UNAVAILABLE = "unavailable"

VARIANTS = {
    "k5": "k5_perm_seed43",
    "k20": "k20_seed42",
    "k50": "k50_seed42",
}
METRICS = ["HR@1", "HR@5", "HR@10", "NDCG@5", "NDCG@10", "MRR", "mean_rank"]

DEFAULT_RUNS = {
    "N-K0": {
        "k5": (
            "outputs/phase2a/ranking_robustness/n_k0_k5_perm_seed43/test_metrics.json",
            "outputs/phase2a/ranking_robustness/n_k0_k5_perm_seed43/n_test_predictions.jsonl",
        ),
        "k20": (
            "outputs/phase2a/ranking_robustness/n_k0_k20_seed42/test_metrics.json",
            "outputs/phase2a/ranking_robustness/n_k0_k20_seed42/n_test_predictions.jsonl",
        ),
        "k50": (
            "outputs/phase2a/ranking_robustness/n_k0_k50_seed42/test_metrics.json",
            "outputs/phase2a/ranking_robustness/n_k0_k50_seed42/n_test_predictions.jsonl",
        ),
    },
    "M1": {
        "k5": (
            "outputs/phase2a/ranking_robustness/m1_k5_perm_seed43/test_metrics.json",
            "outputs/phase2a/ranking_robustness/m1_k5_perm_seed43/m_n_test_predictions.jsonl",
        ),
        "k20": (
            "outputs/phase2a/ranking_robustness/m1_k20_seed42/test_metrics.json",
            "outputs/phase2a/ranking_robustness/m1_k20_seed42/m_n_test_predictions.jsonl",
        ),
        "k50": (
            "outputs/phase2a/ranking_robustness/m1_k50_seed42/test_metrics.json",
            "outputs/phase2a/ranking_robustness/m1_k50_seed42/m_n_test_predictions.jsonl",
        ),
    },
    "SASRec s1500": {
        "k5": (
            "outputs/baselines/movielens-1m/sasrec_fixed_phase2a_k5_perm_seed43_s1500_eval/test_metrics.json",
            "outputs/baselines/movielens-1m/sasrec_fixed_phase2a_k5_perm_seed43_s1500_eval/n_test_predictions.jsonl",
        ),
        "k20": (
            "outputs/baselines/movielens-1m/sasrec_fixed_phase2a_k20_seed42_s1500_eval/test_metrics.json",
            "outputs/baselines/movielens-1m/sasrec_fixed_phase2a_k20_seed42_s1500_eval/n_test_predictions.jsonl",
        ),
        "k50": (
            "outputs/baselines/movielens-1m/sasrec_fixed_phase2a_k50_seed42_s1500_eval/test_metrics.json",
            "outputs/baselines/movielens-1m/sasrec_fixed_phase2a_k50_seed42_s1500_eval/n_test_predictions.jsonl",
        ),
    },
    "SASRec s3000": {
        "k5": (
            "outputs/baselines/movielens-1m/sasrec_fixed_phase2a_k5_perm_seed43_s3000_eval/test_metrics.json",
            "outputs/baselines/movielens-1m/sasrec_fixed_phase2a_k5_perm_seed43_s3000_eval/n_test_predictions.jsonl",
        ),
        "k20": (
            "outputs/baselines/movielens-1m/sasrec_fixed_phase2a_k20_seed42_s3000_eval/test_metrics.json",
            "outputs/baselines/movielens-1m/sasrec_fixed_phase2a_k20_seed42_s3000_eval/n_test_predictions.jsonl",
        ),
        "k50": (
            "outputs/baselines/movielens-1m/sasrec_fixed_phase2a_k50_seed42_s3000_eval/test_metrics.json",
            "outputs/baselines/movielens-1m/sasrec_fixed_phase2a_k50_seed42_s3000_eval/n_test_predictions.jsonl",
        ),
    },
}


def run_sasrec_candidate_size_robustness(
    config_path: str | Path,
    dataset_key: str = "movielens-1m",
    output_dir: str | Path | None = None,
    runs: dict[str, dict[str, tuple[str | Path, str | Path]]] | None = None,
) -> dict[str, Any]:
    """Write k5/k20/k50 metrics and degradation deltas for LLM/SASRec runs."""

    config = load_experiment_config(config_path)
    repo_root = Path(config["_repo_root"])
    output_path = _resolve_path(
        repo_root,
        output_dir or "outputs/fair_budget_baseline_positioning",
    )
    output_path.mkdir(parents=True, exist_ok=True)

    metric_rows = _metric_rows(repo_root, runs or DEFAULT_RUNS)
    degradation_rows = _degradation_rows(metric_rows)
    gap_rows = _gap_rows(metric_rows)
    payload = {
        "dataset": dataset_key,
        "protocol": "Phase 2A candidate-size robustness",
        "variant_mapping": VARIANTS,
        "metrics": metric_rows,
        "degradation": degradation_rows,
        "gaps": gap_rows,
        "answers": _answers(metric_rows, degradation_rows, gap_rows),
    }

    csv_path = output_path / "sasrec_candidate_size_robustness.csv"
    degradation_csv = output_path / "sasrec_candidate_size_robustness_deltas.csv"
    json_path = output_path / "sasrec_candidate_size_robustness.json"
    markdown_path = output_path / "sasrec_candidate_size_robustness.md"
    _write_csv(csv_path, metric_rows)
    _write_csv(degradation_csv, degradation_rows)
    _write_json(json_path, payload)
    _write_markdown(markdown_path, payload)

    return {
        "dataset": dataset_key,
        "metric_rows": len(metric_rows),
        "degradation_rows": len(degradation_rows),
        "gap_rows": len(gap_rows),
        "missing_metric_rows": sum(1 for row in metric_rows if row["evidence_status"] != "computed"),
        "paths": {
            "csv": str(csv_path),
            "deltas_csv": str(degradation_csv),
            "json": str(json_path),
            "markdown": str(markdown_path),
        },
    }


def _metric_rows(
    repo_root: Path,
    runs: dict[str, dict[str, tuple[str | Path, str | Path]]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for model, variants in runs.items():
        for candidate_size in ["k5", "k20", "k50"]:
            metrics_path, predictions_path = variants[candidate_size]
            metric_path = _resolve_path(repo_root, metrics_path)
            prediction_path = _resolve_path(repo_root, predictions_path)
            rows.append(_metric_row(model, candidate_size, metric_path, prediction_path))
    return rows


def _metric_row(
    model: str,
    candidate_size: str,
    metrics_path: Path,
    prediction_path: Path,
) -> dict[str, Any]:
    if not metrics_path.exists():
        return _missing_metric_row(
            model,
            candidate_size,
            metrics_path,
            prediction_path,
            "missing_metrics_file",
        )
    metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
    ranking = metrics.get("ranking", {})
    row = {
        "model": model,
        "candidate_size": candidate_size,
        "variant": VARIANTS[candidate_size],
        "samples": ranking.get("samples", UNAVAILABLE),
        "HR@1": _value(ranking.get("HR@1")),
        "HR@5": _value(ranking.get("HR@5")),
        "HR@10": _value(ranking.get("HR@10")),
        "NDCG@5": _value(ranking.get("NDCG@5")),
        "NDCG@10": _value(ranking.get("NDCG@10")),
        "MRR": _value(ranking.get("MRR")),
        "mean_rank": _mean_rank(prediction_path),
        "evidence_status": "computed",
        "metrics_path": str(metrics_path),
        "predictions_path": str(prediction_path),
    }
    if row["mean_rank"] == UNAVAILABLE and not prediction_path.exists():
        row["evidence_status"] = "computed_metrics_missing_predictions"
    return row


def _missing_metric_row(
    model: str,
    candidate_size: str,
    metrics_path: Path,
    prediction_path: Path,
    status: str,
) -> dict[str, Any]:
    return {
        "model": model,
        "candidate_size": candidate_size,
        "variant": VARIANTS[candidate_size],
        "samples": UNAVAILABLE,
        "HR@1": UNAVAILABLE,
        "HR@5": UNAVAILABLE,
        "HR@10": UNAVAILABLE,
        "NDCG@5": UNAVAILABLE,
        "NDCG@10": UNAVAILABLE,
        "MRR": UNAVAILABLE,
        "mean_rank": UNAVAILABLE,
        "evidence_status": status,
        "metrics_path": str(metrics_path),
        "predictions_path": str(prediction_path),
    }


def _mean_rank(prediction_path: Path) -> float | str:
    if not prediction_path.exists():
        return UNAVAILABLE
    ranks = []
    with open_text_auto(prediction_path, "rt", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            record = json.loads(line)
            ranks.append(
                ground_truth_rank(
                    [float(score) for score in record["scores"]],
                    int(record["ground_truth_index"]),
                )
            )
    if not ranks:
        return UNAVAILABLE
    return _round(sum(ranks) / len(ranks))


def _degradation_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_model_size = {(row["model"], row["candidate_size"]): row for row in rows}
    output = []
    for model in sorted({row["model"] for row in rows}):
        for left_size, right_size in [("k20", "k5"), ("k50", "k20"), ("k50", "k5")]:
            left = by_model_size.get((model, left_size))
            right = by_model_size.get((model, right_size))
            if not left or not right:
                continue
            output.append(_delta_row(model, f"{right_size}_to_{left_size}", left, right))
    return output


def _gap_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_model_size = {(row["model"], row["candidate_size"]): row for row in rows}
    output = []
    for candidate_size in ["k5", "k20", "k50"]:
        n_row = by_model_size.get(("N-K0", candidate_size))
        m_row = by_model_size.get(("M1", candidate_size))
        s1500 = by_model_size.get(("SASRec s1500", candidate_size))
        s3000 = by_model_size.get(("SASRec s3000", candidate_size))
        for sasrec in [s1500, s3000]:
            if n_row and sasrec:
                output.append(_gap_row(sasrec["model"], "N-K0", candidate_size, sasrec, n_row))
            if m_row and sasrec:
                output.append(_gap_row(sasrec["model"], "M1", candidate_size, sasrec, m_row))
        if n_row and m_row:
            output.append(_gap_row("N-K0", "M1", candidate_size, n_row, m_row))
    return output


def _delta_row(
    model: str,
    comparison: str,
    left: dict[str, Any],
    right: dict[str, Any],
) -> dict[str, Any]:
    row = {
        "model": model,
        "comparison": comparison,
        "left_candidate_size": left["candidate_size"],
        "right_candidate_size": right["candidate_size"],
        "evidence_status": _combined_status(left, right),
    }
    for metric in METRICS:
        row[f"delta_{metric}"] = _delta(left.get(metric), right.get(metric))
    return row


def _gap_row(
    left_model: str,
    right_model: str,
    candidate_size: str,
    left: dict[str, Any],
    right: dict[str, Any],
) -> dict[str, Any]:
    row = {
        "comparison": f"{left_model}_minus_{right_model}",
        "candidate_size": candidate_size,
        "evidence_status": _combined_status(left, right),
    }
    for metric in METRICS:
        row[f"delta_{metric}"] = _delta(left.get(metric), right.get(metric))
    return row


def _combined_status(left: dict[str, Any], right: dict[str, Any]) -> str:
    if left.get("evidence_status") == "computed" and right.get("evidence_status") == "computed":
        return "computed"
    return f"{left.get('evidence_status')}; {right.get('evidence_status')}"


def _answers(
    metric_rows: list[dict[str, Any]],
    degradation_rows: list[dict[str, Any]],
    gap_rows: list[dict[str, Any]],
) -> dict[str, str]:
    if any(row["evidence_status"] != "computed" for row in metric_rows):
        return {
            "sasrec_degrades_with_candidate_size": "unavailable until SASRec k5/k20/k50 eval metrics exist",
            "sasrec_degradation_vs_llm": "unavailable until SASRec k5/k20/k50 eval metrics exist",
            "n_k0_sasrec_gap_with_candidate_size": "unavailable until SASRec k5/k20/k50 eval metrics exist",
            "weakness_type": "unavailable until SASRec k5/k20/k50 eval metrics exist",
        }
    s3000_degradation = _find_degradation(degradation_rows, "SASRec s3000", "k5_to_k50", "delta_HR@1")
    n_degradation = _find_degradation(degradation_rows, "N-K0", "k5_to_k50", "delta_HR@1")
    m_degradation = _find_degradation(degradation_rows, "M1", "k5_to_k50", "delta_HR@1")
    gap_k5 = _find_gap(gap_rows, "SASRec s3000_minus_N-K0", "k5", "delta_HR@1")
    gap_k50 = _find_gap(gap_rows, "SASRec s3000_minus_N-K0", "k50", "delta_HR@1")
    return {
        "sasrec_degrades_with_candidate_size": "yes" if s3000_degradation is not None and s3000_degradation < 0 else "not established",
        "sasrec_degradation_vs_llm": _slope_answer(s3000_degradation, n_degradation, m_degradation),
        "n_k0_sasrec_gap_with_candidate_size": _gap_answer(gap_k5, gap_k50),
        "weakness_type": "computed; interpret with metric and gap tables",
    }


def _find_degradation(
    rows: list[dict[str, Any]],
    model: str,
    comparison: str,
    metric: str,
) -> float | None:
    for row in rows:
        if row["model"] == model and row["comparison"] == comparison:
            return _optional_float(row.get(metric))
    return None


def _find_gap(
    rows: list[dict[str, Any]],
    comparison: str,
    candidate_size: str,
    metric: str,
) -> float | None:
    for row in rows:
        if row["comparison"] == comparison and row["candidate_size"] == candidate_size:
            return _optional_float(row.get(metric))
    return None


def _slope_answer(
    sasrec_delta: float | None,
    n_delta: float | None,
    m_delta: float | None,
) -> str:
    if sasrec_delta is None or n_delta is None or m_delta is None:
        return UNAVAILABLE
    sasrec_drop = abs(sasrec_delta)
    if sasrec_drop < abs(n_delta) and sasrec_drop < abs(m_delta):
        return "SASRec degradation is smaller than both N-K0 and M1 by HR@1 k5-to-k50"
    return "SASRec degradation is not smaller than both N-K0 and M1 by HR@1 k5-to-k50"


def _gap_answer(gap_k5: float | None, gap_k50: float | None) -> str:
    if gap_k5 is None or gap_k50 is None:
        return UNAVAILABLE
    if gap_k50 > gap_k5:
        return "SASRec s3000 minus N-K0 gap increases from k5 to k50 by HR@1"
    return "SASRec s3000 minus N-K0 gap does not increase from k5 to k50 by HR@1"


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
        "# SASRec Candidate-Size Robustness",
        "",
        f"Dataset: `{payload['dataset']}`.",
        f"Protocol: `{payload['protocol']}`.",
        "",
        "## Metrics",
        "",
        "| model | candidate_size | variant | samples | HR@1 | HR@5 | HR@10 | NDCG@5 | NDCG@10 | MRR | mean_rank | evidence_status |",
        "|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in payload["metrics"]:
        lines.append(
            f"| {row['model']} | {row['candidate_size']} | {row['variant']} | {row['samples']} | "
            f"{row['HR@1']} | {row['HR@5']} | {row['HR@10']} | {row['NDCG@5']} | "
            f"{row['NDCG@10']} | {row['MRR']} | {row['mean_rank']} | {row['evidence_status']} |"
        )

    lines += [
        "",
        "## Degradation",
        "",
        "| model | comparison | delta_HR@1 | delta_HR@5 | delta_HR@10 | delta_NDCG@5 | delta_NDCG@10 | delta_MRR | delta_mean_rank | evidence_status |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in payload["degradation"]:
        lines.append(
            f"| {row['model']} | {row['comparison']} | {row['delta_HR@1']} | "
            f"{row['delta_HR@5']} | {row['delta_HR@10']} | {row['delta_NDCG@5']} | "
            f"{row['delta_NDCG@10']} | {row['delta_MRR']} | {row['delta_mean_rank']} | "
            f"{row['evidence_status']} |"
        )

    lines += [
        "",
        "## Gaps",
        "",
        "| comparison | candidate_size | delta_HR@1 | delta_NDCG@5 | delta_MRR | delta_mean_rank | evidence_status |",
        "|---|---|---:|---:|---:|---:|---|",
    ]
    for row in payload["gaps"]:
        lines.append(
            f"| {row['comparison']} | {row['candidate_size']} | {row['delta_HR@1']} | "
            f"{row['delta_NDCG@5']} | {row['delta_MRR']} | {row['delta_mean_rank']} | "
            f"{row['evidence_status']} |"
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
        "`k5` is the Phase 2A `k5_perm_seed43` row, not the Phase 2C `k5_popmatch_seed42` row. Keep this protocol separate from popmatch claims.",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Write SASRec candidate-size robustness summary")
    parser.add_argument("--config", default="configs/experiment.yaml")
    parser.add_argument("--dataset", default="movielens-1m")
    parser.add_argument("--output-dir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    summary = run_sasrec_candidate_size_robustness(
        config_path=args.config,
        dataset_key=args.dataset,
        output_dir=args.output_dir,
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
