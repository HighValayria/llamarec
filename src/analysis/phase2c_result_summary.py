"""Phase 2C final summary for popmatch hard-candidate diagnostics."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any

from src.data.config import load_experiment_config


DEFAULT_RUNS = {
    "Base": "base_k5_popmatch_seed42/test_metrics.json",
    "N-K0": "n_k0_k5_popmatch_seed42/test_metrics.json",
    "M1": "m1_k5_popmatch_seed42/test_metrics.json",
    "Y-K0": "y_k0_k5_popmatch_seed42/test_metrics.json",
}


def run_phase2c_result_summary(
    config_path: str | Path,
    dataset_key: str = "movielens-1m",
    eval_dir: str | Path | None = None,
    candidate_diagnostics_json: str | Path | None = None,
    grouped_csv: str | Path | None = None,
    output_dir: str | Path | None = None,
    runs: dict[str, str | Path] | None = None,
) -> dict[str, Any]:
    """Write a compact Phase 2C popmatch result summary."""

    config = load_experiment_config(config_path)
    repo_root = Path(config["_repo_root"])
    base_dir = Path("outputs") / "phase2c" / dataset_key
    eval_path = _resolve_path(repo_root, eval_dir or base_dir / "popmatch_eval_clean")
    if not eval_path.exists():
        eval_path = _resolve_path(repo_root, base_dir / "popmatch_eval")
    output_path = _resolve_path(repo_root, output_dir or base_dir / "result_summary")
    output_path.mkdir(parents=True, exist_ok=True)

    diagnostics_path = _resolve_path(
        repo_root,
        candidate_diagnostics_json
        or base_dir
        / "candidate_set_diagnostics"
        / "k5_popmatch_seed42"
        / "candidate_set_diagnostics.json",
    )
    grouped_path = _resolve_path(
        repo_root,
        grouped_csv or base_dir / "popmatch_grouped" / "test_ranking_by_target_popularity.csv",
    )

    overall_rows = _overall_rows(eval_path, runs or DEFAULT_RUNS)
    diagnostic_rows = _candidate_diagnostic_rows(diagnostics_path)
    grouped_rows = _read_csv(grouped_path) if grouped_path.exists() else []
    bucket_delta_rows = _bucket_deltas(grouped_rows, left="N-K0", right="M1")
    model_delta_rows = _model_deltas(overall_rows, left="N-K0", right="M1")

    payload = {
        "dataset": dataset_key,
        "eval_dir": str(eval_path),
        "candidate_diagnostics": diagnostic_rows,
        "overall_test_metrics": overall_rows,
        "n_k0_minus_m1": model_delta_rows,
        "bucket_n_k0_minus_m1": bucket_delta_rows,
    }

    json_path = output_path / "phase2c_popmatch_result_summary.json"
    markdown_path = output_path / "phase2c_popmatch_result_summary.md"
    _write_json(json_path, payload)
    _write_markdown(markdown_path, payload)

    return {
        "dataset": dataset_key,
        "paths": {
            "json": str(json_path),
            "markdown": str(markdown_path),
        },
    }


def _overall_rows(eval_path: Path, runs: dict[str, str | Path]) -> list[dict[str, Any]]:
    rows = []
    for model, relative_path in runs.items():
        metrics = json.loads((eval_path / relative_path).read_text(encoding="utf-8"))
        ranking = metrics.get("ranking", {})
        binary = metrics.get("binary", {})
        rows.append(
            {
                "model": model,
                "HR@1": ranking.get("HR@1"),
                "NDCG@5": ranking.get("NDCG@5"),
                "MRR": ranking.get("MRR"),
                "AUC": binary.get("AUC"),
                "F1": binary.get("F1"),
            }
        )
    return rows


def _candidate_diagnostic_rows(path: Path) -> list[dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    return [
        {
            "split": row["split"],
            "method": row["method"],
            "samples": row["samples"],
            "mean_abs_popularity_gap": row["mean_abs_popularity_gap"],
        }
        for row in payload.get("diagnostics", [])
    ]


def _model_deltas(
    rows: list[dict[str, Any]],
    left: str,
    right: str,
) -> list[dict[str, Any]]:
    by_model = {row["model"]: row for row in rows}
    output = []
    if left not in by_model or right not in by_model:
        return output
    for metric in ["HR@1", "NDCG@5", "MRR"]:
        output.append(
            {
                "comparison": f"{left} minus {right}",
                "metric": metric,
                "delta": _round(float(by_model[left][metric]) - float(by_model[right][metric])),
            }
        )
    return output


def _bucket_deltas(
    rows: list[dict[str, Any]],
    left: str,
    right: str,
) -> list[dict[str, Any]]:
    by_key = {(row["model"], row["group_value"]): row for row in rows}
    buckets = ["<=10", "11-50", "51-200", "201-500", ">500"]
    output = []
    for bucket in buckets:
        left_row = by_key.get((left, bucket))
        right_row = by_key.get((right, bucket))
        if not left_row or not right_row:
            continue
        output.append(
            {
                "bucket": bucket,
                "samples": int(left_row["samples"]),
                "delta_HR@1": _round(float(left_row["HR@1"]) - float(right_row["HR@1"])),
                "delta_NDCG@5": _round(float(left_row["NDCG@5"]) - float(right_row["NDCG@5"])),
                "delta_MRR": _round(float(left_row["MRR"]) - float(right_row["MRR"])),
            }
        )
    return output


def _write_markdown(path: Path, payload: dict[str, Any]) -> None:
    lines = [
        "# Phase 2C Popmatch Result Summary",
        "",
        "## Stage Purpose",
        "",
        (
            "Phase 2C is a diagnosis and consolidation stage. It evaluates existing "
            "Base, Y-K0, N-K0, and M1 models under popularity-matched hard candidates "
            "before approving any new training or Phase 3 method changes."
        ),
        "",
        "## Candidate Diagnostics",
        "",
        "| split | method | samples | mean_abs_popularity_gap |",
        "|---|---|---:|---:|",
    ]
    for row in payload["candidate_diagnostics"]:
        lines.append(
            f"| {row['split']} | {row['method']} | {row['samples']} | "
            f"{row['mean_abs_popularity_gap']} |"
        )

    lines += [
        "",
        "## Overall Test Metrics",
        "",
        "| model | HR@1 | NDCG@5 | MRR | AUC | F1 |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for row in payload["overall_test_metrics"]:
        lines.append(
            f"| {row['model']} | {_fmt(row['HR@1'])} | {_fmt(row['NDCG@5'])} | "
            f"{_fmt(row['MRR'])} | {_fmt(row['AUC'])} | {_fmt(row['F1'])} |"
        )

    lines += [
        "",
        "## N-K0 Minus M1",
        "",
        "| metric | delta |",
        "|---|---:|",
    ]
    for row in payload["n_k0_minus_m1"]:
        lines.append(f"| {row['metric']} | {row['delta']:.10f} |")

    lines += [
        "",
        "## N-K0 Minus M1 by Target Popularity",
        "",
        "| bucket | samples | delta_HR@1 | delta_NDCG@5 | delta_MRR |",
        "|---|---:|---:|---:|---:|",
    ]
    for row in payload["bucket_n_k0_minus_m1"]:
        lines.append(
            f"| {row['bucket']} | {row['samples']} | {row['delta_HR@1']:.10f} | "
            f"{row['delta_NDCG@5']:.10f} | {row['delta_MRR']:.10f} |"
        )

    lines += [
        "",
        "## Interpretation",
        "",
        "- N-K0 remains the strongest next-item ranking model under popularity-matched hard candidates.",
        "- M1 remains close to N-K0 but does not surpass it on ranking.",
        "- Y-K0 remains binary-strong but weak as next-item ranking, supporting the Y/N semantic boundary.",
        "- N-K0's advantage over M1 appears across target popularity buckets; the `<=10` bucket is small and should be interpreted cautiously.",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def _resolve_path(base: Path, path: str | Path) -> Path:
    output = Path(path)
    if output.is_absolute():
        return output
    return base / output


def _fmt(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, float):
        return f"{value:.10f}"
    return str(value)


def _round(value: float) -> float:
    return round(float(value), 10)


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
    parser = argparse.ArgumentParser(description="Phase 2C popmatch final summary")
    parser.add_argument("--config", default="configs/experiment.yaml")
    parser.add_argument("--dataset", default="movielens-1m")
    parser.add_argument("--eval-dir", default=None)
    parser.add_argument("--candidate-diagnostics-json", default=None)
    parser.add_argument("--grouped-csv", default=None)
    parser.add_argument("--output-dir", default=None)
    parser.add_argument("--run", action="append", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    summary = run_phase2c_result_summary(
        config_path=args.config,
        dataset_key=args.dataset,
        eval_dir=args.eval_dir,
        candidate_diagnostics_json=args.candidate_diagnostics_json,
        grouped_csv=args.grouped_csv,
        output_dir=args.output_dir,
        runs=_run_overrides(args.run),
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
