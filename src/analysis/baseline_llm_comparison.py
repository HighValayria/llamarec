"""Compare baseline ranking rows with Phase 2C LLM popmatch results."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from src.data.config import load_experiment_config


def run_baseline_llm_comparison(
    config_path: str | Path,
    dataset_key: str = "movielens-1m",
    baseline_summary_json: str | Path | None = None,
    phase2c_summary_json: str | Path | None = None,
    output_dir: str | Path | None = None,
) -> dict[str, Any]:
    """Write a compact comparison table for baselines and Phase 2C LLM rows."""

    config = load_experiment_config(config_path)
    repo_root = Path(config["_repo_root"])
    baseline_path = _resolve_path(
        repo_root,
        baseline_summary_json
        or Path("outputs") / "baselines" / dataset_key / "summary" / "baseline_ranking_summary.json",
    )
    phase2c_path = _resolve_path(
        repo_root,
        phase2c_summary_json
        or Path("outputs") / "phase2c" / dataset_key / "result_summary" / "phase2c_popmatch_result_summary.json",
    )
    output_path = _resolve_path(
        repo_root,
        output_dir or Path("outputs") / "baselines" / dataset_key / "llm_comparison",
    )
    output_path.mkdir(parents=True, exist_ok=True)

    baseline_payload = json.loads(baseline_path.read_text(encoding="utf-8"))
    phase2c_payload = json.loads(phase2c_path.read_text(encoding="utf-8"))
    rows = _comparison_rows(baseline_payload, phase2c_payload)
    deltas = _comparison_deltas(rows)
    payload = {
        "dataset": dataset_key,
        "baseline_summary_json": str(baseline_path),
        "phase2c_summary_json": str(phase2c_path),
        "rows": rows,
        "deltas": deltas,
    }

    json_path = output_path / "baseline_llm_comparison.json"
    markdown_path = output_path / "baseline_llm_comparison.md"
    _write_json(json_path, payload)
    _write_markdown(markdown_path, payload)

    return {
        "dataset": dataset_key,
        "rows": len(rows),
        "paths": {
            "json": str(json_path),
            "markdown": str(markdown_path),
        },
    }


def _comparison_rows(
    baseline_payload: dict[str, Any],
    phase2c_payload: dict[str, Any],
) -> list[dict[str, Any]]:
    rows = []
    for row in baseline_payload.get("baseline_metrics", []):
        condition = "popmatch k5" if "popmatch" in row["baseline"] else "canonical k5"
        rows.append(
            {
                "family": "baseline",
                "model": row["baseline"],
                "condition": condition,
                "HR@1": row.get("HR@1"),
                "NDCG@5": row.get("NDCG@5"),
                "MRR": row.get("MRR"),
            }
        )
    for row in phase2c_payload.get("overall_test_metrics", []):
        rows.append(
            {
                "family": "llm",
                "model": row["model"],
                "condition": "popmatch k5",
                "HR@1": row.get("HR@1"),
                "NDCG@5": row.get("NDCG@5"),
                "MRR": row.get("MRR"),
            }
        )
    return rows


def _comparison_deltas(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_model = {row["model"]: row for row in rows}
    available_llm_models = {
        row["model"]
        for row in rows
        if row["family"] == "llm" and row["condition"] == "popmatch k5"
    }
    preferred_order = ["N-K0", "M1", "Base", "Y-K0"]
    llm_models = [
        model
        for model in preferred_order
        if model in available_llm_models
    ] + [
        model
        for model in sorted(available_llm_models)
        if model not in preferred_order
    ]
    baseline_models = [
        row["model"]
        for row in rows
        if row["family"] == "baseline" and row["condition"] == "popmatch k5"
    ]
    deltas = []
    for left in llm_models:
        for right in baseline_models:
            deltas.extend(_metric_deltas(by_model, left, right))
    return deltas


def _metric_deltas(
    by_model: dict[str, dict[str, Any]],
    left: str,
    right: str,
) -> list[dict[str, Any]]:
    left_row = by_model.get(left)
    right_row = by_model.get(right)
    if not left_row or not right_row:
        return []
    output = []
    for metric in ["HR@1", "NDCG@5", "MRR"]:
        if left_row.get(metric) is None or right_row.get(metric) is None:
            continue
        output.append(
            {
                "comparison": f"{left} minus {right}",
                "metric": metric,
                "delta": round(float(left_row[metric]) - float(right_row[metric]), 10),
            }
        )
    return output


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def _write_markdown(path: Path, payload: dict[str, Any]) -> None:
    lines = [
        f"# {payload['dataset']} Baseline and LLM Ranking Comparison",
        "",
        "## Ranking Metrics",
        "",
        "| family | model | condition | HR@1 | NDCG@5 | MRR |",
        "|---|---|---|---:|---:|---:|",
    ]
    for row in payload["rows"]:
        lines.append(
            f"| {row['family']} | {row['model']} | {row['condition']} | "
            f"{_fmt(row['HR@1'])} | {_fmt(row['NDCG@5'])} | {_fmt(row['MRR'])} |"
        )

    lines += [
        "",
        "## Popmatch Deltas",
        "",
        "| comparison | metric | delta |",
        "|---|---|---:|",
    ]
    for row in payload["deltas"]:
        lines.append(f"| {row['comparison']} | {row['metric']} | {row['delta']:.10f} |")

    lines += [
        "",
        "## Interpretation",
        "",
        "- Canonical baseline rows are included to expose random-candidate popularity shortcuts.",
        "- Popmatch rows are the fair comparison point for Phase 2C LLM results.",
        "- Do not compare canonical baseline rows against popmatch LLM rows as a like-for-like ranking claim.",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def _resolve_path(base: Path, path: str | Path) -> Path:
    output = Path(path)
    if output.is_absolute():
        return output
    return base / output


def _fmt(value: Any) -> str:
    if value is None or value == "":
        return ""
    return f"{float(value):.10f}"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compare baseline and Phase 2C LLM ranking rows")
    parser.add_argument("--config", default="configs/experiment.yaml")
    parser.add_argument("--dataset", default="movielens-1m")
    parser.add_argument("--baseline-summary-json", default=None)
    parser.add_argument("--phase2c-summary-json", default=None)
    parser.add_argument("--output-dir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    summary = run_baseline_llm_comparison(
        config_path=args.config,
        dataset_key=args.dataset,
        baseline_summary_json=args.baseline_summary_json,
        phase2c_summary_json=args.phase2c_summary_json,
        output_dir=args.output_dir,
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
