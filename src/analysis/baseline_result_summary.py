"""Summarize traditional baseline ranking results."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any

from src.data.config import load_experiment_config


DEFAULT_RUNS = {
    "Popularity N-train canonical k5": "popularity_canonical_k5/test_metrics.json",
    "Popularity N-train popmatch k5": "popularity_k5_popmatch_seed42/test_metrics.json",
    "Popularity preference-train canonical k5": "popularity_preftrain_canonical_k5/test_metrics.json",
    "Popularity preference-train popmatch k5": "popularity_preftrain_k5_popmatch_seed42/test_metrics.json",
    "BPR-MF canonical k5": "bpr_mf_canonical_k5/test_metrics.json",
    "BPR-MF popmatch k5": "bpr_mf_k5_popmatch_seed42/test_metrics.json",
}


def run_baseline_result_summary(
    config_path: str | Path,
    dataset_key: str = "movielens-1m",
    input_dir: str | Path | None = None,
    output_dir: str | Path | None = None,
    runs: dict[str, str | Path] | None = None,
) -> dict[str, Any]:
    """Write CSV/JSON/Markdown summary for baseline ranking metrics."""

    config = load_experiment_config(config_path)
    repo_root = Path(config["_repo_root"])
    baseline_dir = _resolve_path(
        repo_root,
        input_dir or Path("outputs") / "baselines" / dataset_key,
    )
    output_path = _resolve_path(
        repo_root,
        output_dir or baseline_dir / "summary",
    )
    output_path.mkdir(parents=True, exist_ok=True)

    rows = _metric_rows(baseline_dir, runs or DEFAULT_RUNS)
    deltas = _condition_deltas(rows)
    payload = {
        "dataset": dataset_key,
        "input_dir": str(baseline_dir),
        "baseline_metrics": rows,
        "condition_deltas": deltas,
    }

    csv_path = output_path / "baseline_ranking_summary.csv"
    json_path = output_path / "baseline_ranking_summary.json"
    markdown_path = output_path / "baseline_ranking_summary.md"
    _write_csv(csv_path, rows)
    _write_json(json_path, payload)
    _write_markdown(markdown_path, payload)

    return {
        "dataset": dataset_key,
        "rows": len(rows),
        "paths": {
            "csv": str(csv_path),
            "json": str(json_path),
            "markdown": str(markdown_path),
        },
    }


def _metric_rows(base_dir: Path, runs: dict[str, str | Path]) -> list[dict[str, Any]]:
    rows = []
    for label, relative_path in runs.items():
        metrics_path = base_dir / relative_path
        metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
        ranking = metrics.get("ranking", {})
        rows.append(
            {
                "baseline": label,
                "metrics_path": str(metrics_path),
                "HR@1": ranking.get("HR@1"),
                "NDCG@5": ranking.get("NDCG@5"),
                "MRR": ranking.get("MRR"),
                "HR@5": ranking.get("HR@5"),
                "samples": ranking.get("samples"),
                "ranking_scoring": metrics.get("ranking_scoring", ""),
            }
        )
    return rows


def _condition_deltas(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    output = []
    by_baseline = {row["baseline"]: row for row in rows}
    for canonical_label, canonical_row in by_baseline.items():
        if " canonical " not in canonical_label:
            continue
        popmatch_label = canonical_label.replace(" canonical ", " popmatch ")
        popmatch_row = by_baseline.get(popmatch_label)
        if not popmatch_row:
            continue
        for metric in ["HR@1", "NDCG@5", "MRR"]:
            if canonical_row.get(metric) is None or popmatch_row.get(metric) is None:
                continue
            output.append(
                {
                    "comparison": f"{popmatch_label} minus {canonical_label}",
                    "metric": metric,
                    "delta": round(float(popmatch_row[metric]) - float(canonical_row[metric]), 10),
                }
            )
    return output


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fieldnames = [
        "baseline",
        "HR@1",
        "NDCG@5",
        "MRR",
        "HR@5",
        "samples",
        "ranking_scoring",
        "metrics_path",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def _write_markdown(path: Path, payload: dict[str, Any]) -> None:
    lines = [
        f"# {payload['dataset']} Baseline Ranking Summary",
        "",
        "## Metrics",
        "",
        "| baseline | HR@1 | NDCG@5 | MRR | HR@5 | samples |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for row in payload["baseline_metrics"]:
        lines.append(
            f"| {row['baseline']} | {_fmt(row['HR@1'])} | {_fmt(row['NDCG@5'])} | "
            f"{_fmt(row['MRR'])} | {_fmt(row['HR@5'])} | {row['samples']} |"
        )

    lines += [
        "",
        "## Candidate-Condition Delta",
        "",
        "| comparison | metric | delta |",
        "|---|---|---:|",
    ]
    for row in payload["condition_deltas"]:
        lines.append(f"| {row['comparison']} | {row['metric']} | {row['delta']:.10f} |")

    lines += [
        "",
        "## Interpretation",
        "",
        "- Popularity is a non-LLM ranking baseline scored from training-only item counts.",
        "- `N-train` counts next-item train targets; `preference-train` counts Y train targets as train-region interactions.",
        "- BPR-MF is a trainable matrix-factorization baseline trained from `next_item_train` targets.",
        "- A large canonical-to-popmatch drop indicates that random candidates expose a popularity shortcut.",
        "- Compare these rows with LLM metrics only when the same candidate files and splits are used.",
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


def _run_overrides(values: list[str] | None) -> dict[str, str] | None:
    if not values:
        return None
    runs = {}
    for value in values:
        if "=" not in value:
            raise ValueError("--run values must be LABEL=path")
        label, path = value.split("=", 1)
        runs[label] = path
    return runs


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Summarize baseline ranking metrics")
    parser.add_argument("--config", default="configs/experiment.yaml")
    parser.add_argument("--dataset", default="movielens-1m")
    parser.add_argument("--input-dir", default=None)
    parser.add_argument("--output-dir", default=None)
    parser.add_argument("--run", action="append", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    summary = run_baseline_result_summary(
        config_path=args.config,
        dataset_key=args.dataset,
        input_dir=args.input_dir,
        output_dir=args.output_dir,
        runs=_run_overrides(args.run),
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
