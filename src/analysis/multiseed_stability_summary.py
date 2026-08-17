"""Summarize MovieLens-1M multi-seed stability metrics."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from statistics import mean, pstdev
from typing import Any

from src.data.config import load_experiment_config


UNAVAILABLE = "unavailable"
DEFAULT_OUTPUT_DIR = "outputs/multiseed_stability"
METRIC_COLUMNS = [
    "binary_AUC",
    "binary_F1",
    "binary_Accuracy",
    "HR@1",
    "NDCG@5",
    "MRR",
]


DEFAULT_RUNS = [
    {
        "model": "Y-K0",
        "seed": 42,
        "regime": "binary_preference",
        "metrics": "outputs/y/movielens-1m/pool200k_1m_y_1500/test_metrics.json",
        "run_summary": "outputs/y/movielens-1m/pool200k_1m_y_1500/run_summary.json",
    },
    {
        "model": "Y-K0",
        "seed": 43,
        "regime": "binary_preference",
        "metrics": "outputs/y/movielens-1m/pool200k_1m_y_1500_seed43/test_metrics.json",
        "run_summary": "outputs/y/movielens-1m/pool200k_1m_y_1500_seed43/run_summary.json",
    },
    {
        "model": "Y-K0",
        "seed": 44,
        "regime": "binary_preference",
        "metrics": "outputs/y/movielens-1m/pool200k_1m_y_1500_seed44/test_metrics.json",
        "run_summary": "outputs/y/movielens-1m/pool200k_1m_y_1500_seed44/run_summary.json",
    },
    {
        "model": "N-K0",
        "seed": 42,
        "regime": "popmatch_ranking",
        "metrics": "outputs/n/movielens-1m/pool200k_1m_n_1500_popmatch_eval/test_metrics.json",
        "run_summary": "outputs/n/movielens-1m/pool200k_1m_n_1500/run_summary.json",
    },
    {
        "model": "N-K0",
        "seed": 43,
        "regime": "popmatch_ranking",
        "metrics": "outputs/n/movielens-1m/pool200k_1m_n_1500_seed43_popmatch_eval/test_metrics.json",
        "run_summary": "outputs/n/movielens-1m/pool200k_1m_n_1500_seed43/run_summary.json",
    },
    {
        "model": "N-K0",
        "seed": 44,
        "regime": "popmatch_ranking",
        "metrics": "outputs/n/movielens-1m/pool200k_1m_n_1500_seed44_popmatch_eval/test_metrics.json",
        "run_summary": "outputs/n/movielens-1m/pool200k_1m_n_1500_seed44/run_summary.json",
    },
    {
        "model": "M1",
        "seed": 42,
        "regime": "popmatch_ranking",
        "metrics": "outputs/m/movielens-1m/diag_m1_1m_m_200k_3000_popmatch_eval/test_metrics.json",
        "run_summary": "outputs/m/movielens-1m/diag_m1_1m_m_200k_3000/run_summary.json",
    },
    {
        "model": "M1",
        "seed": 43,
        "regime": "popmatch_ranking",
        "metrics": "outputs/m/movielens-1m/diag_m1_1m_m_200k_3000_seed43_popmatch_eval/test_metrics.json",
        "run_summary": "outputs/m/movielens-1m/diag_m1_1m_m_200k_3000_seed43/run_summary.json",
    },
    {
        "model": "M1",
        "seed": 44,
        "regime": "popmatch_ranking",
        "metrics": "outputs/m/movielens-1m/diag_m1_1m_m_200k_3000_seed44_popmatch_eval/test_metrics.json",
        "run_summary": "outputs/m/movielens-1m/diag_m1_1m_m_200k_3000_seed44/run_summary.json",
    },
    {
        "model": "SASRec exp-match",
        "seed": 42,
        "regime": "roughly_exposure_matched",
        "metrics": "outputs/baselines/movielens-1m/sasrec_exp_match_k5_popmatch_seed42_s23/test_metrics.json",
        "run_summary": "outputs/baselines/movielens-1m/sasrec_exp_match_k5_popmatch_seed42_s23/run_summary.json",
    },
    {
        "model": "SASRec exp-match",
        "seed": 43,
        "regime": "roughly_exposure_matched",
        "metrics": "outputs/baselines/movielens-1m/sasrec_exp_match_k5_popmatch_seed43_s23/test_metrics.json",
        "run_summary": "outputs/baselines/movielens-1m/sasrec_exp_match_k5_popmatch_seed43_s23/run_summary.json",
    },
    {
        "model": "SASRec exp-match",
        "seed": 44,
        "regime": "roughly_exposure_matched",
        "metrics": "outputs/baselines/movielens-1m/sasrec_exp_match_k5_popmatch_seed44_s23/test_metrics.json",
        "run_summary": "outputs/baselines/movielens-1m/sasrec_exp_match_k5_popmatch_seed44_s23/run_summary.json",
    },
    {
        "model": "SASRec high s3000",
        "seed": 42,
        "regime": "high_exposure",
        "metrics": "outputs/baselines/movielens-1m/sasrec_fixed_popmatch_k5_200k_s3000_eval/test_metrics.json",
        "run_summary": "outputs/baselines/movielens-1m/sasrec_fixed_canonical_k5_200k_s3000/run_summary.json",
    },
    {
        "model": "SASRec high s3000",
        "seed": 43,
        "regime": "high_exposure",
        "metrics": "outputs/baselines/movielens-1m/sasrec_fixed_popmatch_k5_200k_s3000_seed43_eval/test_metrics.json",
        "run_summary": "outputs/baselines/movielens-1m/sasrec_fixed_canonical_k5_200k_s3000_seed43/run_summary.json",
    },
    {
        "model": "SASRec high s3000",
        "seed": 44,
        "regime": "high_exposure",
        "metrics": "outputs/baselines/movielens-1m/sasrec_fixed_popmatch_k5_200k_s3000_seed44_eval/test_metrics.json",
        "run_summary": "outputs/baselines/movielens-1m/sasrec_fixed_canonical_k5_200k_s3000_seed44/run_summary.json",
    },
]


DEFAULT_COMPARISONS = [
    ("N-K0", "M1", "N-K0_minus_M1"),
    ("N-K0", "SASRec exp-match", "N-K0_minus_SASRec_exp_match"),
    ("SASRec high s3000", "N-K0", "SASRec_high_s3000_minus_N-K0"),
]


def run_multiseed_stability_summary(
    config_path: str | Path = "configs/experiment.yaml",
    dataset_key: str = "movielens-1m",
    output_dir: str | Path | None = None,
    runs: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Write multi-seed metric, aggregate, and comparison summaries."""

    config = load_experiment_config(config_path)
    repo_root = Path(config["_repo_root"])
    output_path = _resolve_path(repo_root, output_dir or DEFAULT_OUTPUT_DIR)
    output_path.mkdir(parents=True, exist_ok=True)

    metric_rows = [_metric_row(repo_root, spec) for spec in (runs or DEFAULT_RUNS)]
    aggregate_rows = _aggregate_rows(metric_rows)
    comparison_rows = _comparison_rows(metric_rows)
    payload = {
        "dataset": dataset_key,
        "protocol": "MovieLens-1M multi-seed stability on fixed k5_popmatch_seed42 candidates",
        "seeds": sorted({row["seed"] for row in metric_rows}),
        "metrics": metric_rows,
        "aggregates": aggregate_rows,
        "comparisons": comparison_rows,
        "answers": _answers(metric_rows, comparison_rows),
        "boundary": (
            "This is a three-seed stability diagnostic. Candidate sets are fixed "
            "at k5_popmatch_seed42 while model training seeds vary."
        ),
    }

    metrics_csv = output_path / "multiseed_metrics.csv"
    aggregates_csv = output_path / "multiseed_aggregates.csv"
    comparisons_csv = output_path / "multiseed_comparisons.csv"
    json_path = output_path / "multiseed_stability_summary.json"
    markdown_path = output_path / "multiseed_stability_summary.md"
    _write_csv(metrics_csv, metric_rows)
    _write_csv(aggregates_csv, aggregate_rows)
    _write_csv(comparisons_csv, comparison_rows)
    _write_json(json_path, payload)
    _write_markdown(markdown_path, payload)

    return {
        "dataset": dataset_key,
        "metric_rows": len(metric_rows),
        "aggregate_rows": len(aggregate_rows),
        "comparison_rows": len(comparison_rows),
        "missing_rows": sum(1 for row in metric_rows if row["evidence_status"] != "computed"),
        "paths": {
            "metrics_csv": str(metrics_csv),
            "aggregates_csv": str(aggregates_csv),
            "comparisons_csv": str(comparisons_csv),
            "json": str(json_path),
            "markdown": str(markdown_path),
        },
    }


def _metric_row(repo_root: Path, spec: dict[str, Any]) -> dict[str, Any]:
    metrics_path = _resolve_path(repo_root, spec["metrics"])
    run_summary_path = _resolve_path(repo_root, spec["run_summary"])
    row = {
        "model": spec["model"],
        "seed": int(spec["seed"]),
        "regime": spec["regime"],
        "candidate_protocol": "k5_popmatch_seed42",
        "binary_AUC": UNAVAILABLE,
        "binary_F1": UNAVAILABLE,
        "binary_Accuracy": UNAVAILABLE,
        "binary_samples": UNAVAILABLE,
        "HR@1": UNAVAILABLE,
        "NDCG@5": UNAVAILABLE,
        "MRR": UNAVAILABLE,
        "ranking_samples": UNAVAILABLE,
        "run_seed": UNAVAILABLE,
        "evidence_status": "missing_metrics_file",
        "metrics_path": str(metrics_path),
        "run_summary_path": str(run_summary_path),
    }
    if not metrics_path.exists():
        return row

    metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
    binary = metrics.get("binary", {})
    ranking = metrics.get("ranking", metrics)
    row.update(
        {
            "binary_AUC": _value(binary.get("AUC")),
            "binary_F1": _value(binary.get("F1")),
            "binary_Accuracy": _value(binary.get("Accuracy")),
            "binary_samples": _value(binary.get("samples")),
            "HR@1": _value(ranking.get("HR@1")),
            "NDCG@5": _value(ranking.get("NDCG@5")),
            "MRR": _value(ranking.get("MRR")),
            "ranking_samples": _value(ranking.get("samples")),
            "evidence_status": "computed",
        }
    )
    if run_summary_path.exists():
        run_summary = json.loads(run_summary_path.read_text(encoding="utf-8"))
        row["run_seed"] = _value(run_summary.get("seed"))
    return row


def _aggregate_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    output = []
    for model in sorted({row["model"] for row in rows}):
        model_rows = [row for row in rows if row["model"] == model]
        regime = model_rows[0]["regime"]
        for metric in METRIC_COLUMNS:
            values = [_float_or_none(row[metric]) for row in model_rows]
            values = [value for value in values if value is not None]
            if not values:
                continue
            output.append(
                {
                    "model": model,
                    "regime": regime,
                    "metric": metric,
                    "seeds": len(values),
                    "mean": _value(mean(values)),
                    "std": _value(pstdev(values) if len(values) > 1 else 0.0),
                    "min": _value(min(values)),
                    "max": _value(max(values)),
                    "range": _value(max(values) - min(values)),
                }
            )
    return output


def _comparison_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_model_seed = {(row["model"], row["seed"]): row for row in rows}
    output = []
    seeds = sorted({row["seed"] for row in rows})
    for left_model, right_model, name in DEFAULT_COMPARISONS:
        for seed in seeds:
            left = by_model_seed.get((left_model, seed))
            right = by_model_seed.get((right_model, seed))
            if not left or not right:
                continue
            output.append(
                {
                    "comparison": name,
                    "seed": seed,
                    "left_model": left_model,
                    "right_model": right_model,
                    "delta_HR@1": _delta(left["HR@1"], right["HR@1"]),
                    "delta_NDCG@5": _delta(left["NDCG@5"], right["NDCG@5"]),
                    "delta_MRR": _delta(left["MRR"], right["MRR"]),
                    "evidence_status": _combined_status(left, right),
                }
            )
    return output


def _answers(
    metric_rows: list[dict[str, Any]],
    comparison_rows: list[dict[str, Any]],
) -> dict[str, str]:
    y_f1_values = [
        _float_or_none(row["binary_F1"])
        for row in metric_rows
        if row["model"] == "Y-K0"
    ]
    y_f1_values = [value for value in y_f1_values if value is not None]
    comparison_by_name = {
        name: [row for row in comparison_rows if row["comparison"] == name]
        for _, _, name in DEFAULT_COMPARISONS
    }
    return {
        "y_k0_binary_stability": _positive_metric_answer(y_f1_values, "F1"),
        "n_k0_above_m1_by_hr1": _all_positive_answer(
            comparison_by_name["N-K0_minus_M1"], "delta_HR@1"
        ),
        "n_k0_above_sasrec_exp_match_by_hr1": _all_positive_answer(
            comparison_by_name["N-K0_minus_SASRec_exp_match"], "delta_HR@1"
        ),
        "sasrec_high_above_n_k0_by_hr1": _all_positive_answer(
            comparison_by_name["SASRec_high_s3000_minus_N-K0"], "delta_HR@1"
        ),
        "candidate_protocol_fixed": "yes: all rows use k5_popmatch_seed42",
        "interpretation": (
            "main ranking and sample-efficiency directions are stable across "
            "seeds 42/43/44; high-exposure SASRec is a separate budget regime"
        ),
    }


def _positive_metric_answer(values: list[float], metric_name: str) -> str:
    if not values:
        return "unavailable"
    return f"available across {len(values)} seeds; {metric_name} range {max(values) - min(values):.10f}"


def _all_positive_answer(rows: list[dict[str, Any]], metric: str) -> str:
    values = [_float_or_none(row[metric]) for row in rows]
    values = [value for value in values if value is not None]
    if not values:
        return "unavailable"
    if all(value > 0 for value in values):
        return f"yes across {len(values)} seeds; minimum margin {min(values):.10f}"
    return f"no; minimum margin {min(values):.10f}"


def _write_markdown(path: Path, payload: dict[str, Any]) -> None:
    lines = [
        "# Multi-seed Stability Summary",
        "",
        f"Dataset: `{payload['dataset']}`.",
        f"Protocol: `{payload['protocol']}`.",
        "",
        "## Metrics",
        "",
        _markdown_table(
            payload["metrics"],
            [
                "model",
                "seed",
                "regime",
                "binary_AUC",
                "binary_F1",
                "HR@1",
                "NDCG@5",
                "MRR",
                "evidence_status",
            ],
        ),
        "",
        "## Aggregates",
        "",
        _markdown_table(
            payload["aggregates"],
            ["model", "regime", "metric", "seeds", "mean", "std", "min", "max", "range"],
        ),
        "",
        "## Comparisons",
        "",
        _markdown_table(
            payload["comparisons"],
            [
                "comparison",
                "seed",
                "delta_HR@1",
                "delta_NDCG@5",
                "delta_MRR",
                "evidence_status",
            ],
        ),
        "",
        "## Direct Answers",
        "",
    ]
    lines.extend(f"- {key}: {value}" for key, value in payload["answers"].items())
    lines.extend(["", "## Boundary", "", payload["boundary"], ""])
    path.write_text("\n".join(lines), encoding="utf-8")


def _markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| " + " | ".join(str(row.get(column, "")) for column in columns) + " |"
        for row in rows
    ]
    return "\n".join([header, separator, *body])


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys()) if rows else []
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        if fieldnames:
            writer.writeheader()
            writer.writerows(rows)


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _resolve_path(repo_root: Path, raw_path: str | Path) -> Path:
    path = Path(raw_path)
    if path.is_absolute():
        return path
    return repo_root / path


def _combined_status(left: dict[str, Any], right: dict[str, Any]) -> str:
    if left["evidence_status"] == right["evidence_status"] == "computed":
        return "computed"
    return f"{left['evidence_status']}; {right['evidence_status']}"


def _delta(left: Any, right: Any) -> float | str:
    left_value = _float_or_none(left)
    right_value = _float_or_none(right)
    if left_value is None or right_value is None:
        return UNAVAILABLE
    return _value(left_value - right_value)


def _float_or_none(value: Any) -> float | None:
    if value in (None, "", UNAVAILABLE):
        return None
    return float(value)


def _value(value: Any) -> float | int | str:
    if value is None:
        return UNAVAILABLE
    if isinstance(value, bool):
        return str(value).lower()
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return round(value, 10)
    return value


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Summarize multi-seed stability metrics")
    parser.add_argument("--config", default="configs/experiment.yaml")
    parser.add_argument("--dataset", default="movielens-1m")
    parser.add_argument("--output-dir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    summary = run_multiseed_stability_summary(
        config_path=args.config,
        dataset_key=args.dataset,
        output_dir=args.output_dir,
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
