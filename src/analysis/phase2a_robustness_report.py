"""Phase 2A ranking robustness report from explicit variant metric files."""

from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any


DEFAULT_MODEL_ORDER = ["base", "n_k0", "m1", "y_k0"]
DEFAULT_VARIANT_ORDER = [
    "k5_perm_seed43",
    "k20_seed42",
    "k20_perm_seed43",
    "k50_seed42",
]
METRIC_FIELDS = [
    "HR@1",
    "HR@5",
    "HR@10",
    "HR@20",
    "HR@50",
    "NDCG@5",
    "NDCG@10",
    "NDCG@20",
    "NDCG@50",
    "MRR",
]


def run_phase2a_robustness_report(
    input_dir: str | Path = "outputs/phase2a/ranking_robustness",
    output_dir: str | Path | None = None,
    dataset_key: str | None = None,
) -> dict[str, Any]:
    """Read Phase 2A metric files and write CSV/JSON/Markdown summaries."""

    input_path = Path(input_dir)
    output_path = Path(output_dir) if output_dir is not None else input_path
    output_path.mkdir(parents=True, exist_ok=True)

    rows = _metric_rows(input_path, dataset_key=dataset_key)
    test_rows = [row for row in rows if row["split"] == "test"]
    comparisons = _comparison_rows(test_rows)

    paths = {
        "metrics_csv": output_path / "phase2a_ranking_robustness_metrics.csv",
        "metrics_json": output_path / "phase2a_ranking_robustness_metrics.json",
        "comparison_csv": output_path / "phase2a_ranking_robustness_comparison.csv",
        "report": output_path / "phase2a_ranking_robustness_report.md",
    }
    _write_csv(paths["metrics_csv"], rows)
    paths["metrics_json"].write_text(json.dumps(rows, indent=2), encoding="utf-8")
    _write_csv(paths["comparison_csv"], comparisons)
    _write_markdown_report(paths["report"], rows, comparisons)

    return {
        "input_dir": str(input_path),
        "output_dir": str(output_path),
        "rows": len(rows),
        "test_rows": len(test_rows),
        "comparison_rows": len(comparisons),
        "paths": {name: str(path) for name, path in paths.items()},
    }


def _metric_rows(input_path: Path, dataset_key: str | None = None) -> list[dict[str, Any]]:
    rows = []
    for metrics_path in sorted(input_path.glob("*/*_metrics.json")):
        payload = json.loads(metrics_path.read_text(encoding="utf-8"))
        if dataset_key and payload.get("dataset") != dataset_key:
            continue
        ranking = payload.get("ranking", {})
        run_dir = metrics_path.parent.name
        model_key, variant = _parse_run_dir(run_dir)
        row = {
            "run_dir": run_dir,
            "model_key": model_key,
            "model": payload.get("model", model_key),
            "variant": variant,
            "split": "validation" if metrics_path.name == "valid_metrics.json" else "test",
            "dataset": payload.get("dataset"),
            "samples": ranking.get("samples"),
        }
        for field in METRIC_FIELDS:
            row[field] = ranking.get(field)
        rows.append(row)
    return sorted(rows, key=_row_sort_key)


def _parse_run_dir(run_dir: str) -> tuple[str, str]:
    for prefix in ("n_k0_", "base_", "m1_", "y_k0_"):
        if run_dir.startswith(prefix):
            return prefix[:-1], run_dir[len(prefix):]
    parts = run_dir.split("_", 1)
    if len(parts) == 2:
        return parts[0], parts[1]
    return run_dir, ""


def _comparison_rows(test_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_model_variant = {
        (row["model_key"], row["variant"]): row
        for row in test_rows
    }
    output = []

    for variant in DEFAULT_VARIANT_ORDER:
        n_row = by_model_variant.get(("n_k0", variant))
        m1_row = by_model_variant.get(("m1", variant))
        base_row = by_model_variant.get(("base", variant))
        if n_row and m1_row:
            output.append(_gap_row("n_k0_minus_m1", variant, n_row, m1_row))
        if n_row and base_row:
            output.append(_gap_row("n_k0_minus_base", variant, n_row, base_row))
        if m1_row and base_row:
            output.append(_gap_row("m1_minus_base", variant, m1_row, base_row))

    for model_key in DEFAULT_MODEL_ORDER:
        k20 = by_model_variant.get((model_key, "k20_seed42"))
        k20_perm = by_model_variant.get((model_key, "k20_perm_seed43"))
        k5_perm = by_model_variant.get((model_key, "k5_perm_seed43"))
        k50 = by_model_variant.get((model_key, "k50_seed42"))
        if k20 and k20_perm:
            output.append(_gap_row(f"{model_key}_k20_perm_minus_k20", "order_sensitivity", k20_perm, k20))
        if k5_perm and k20:
            output.append(_gap_row(f"{model_key}_k20_minus_k5_perm", "candidate_size", k20, k5_perm))
        if k20 and k50:
            output.append(_gap_row(f"{model_key}_k50_minus_k20", "candidate_size", k50, k20))
    return output


def _gap_row(name: str, variant: str, left: dict[str, Any], right: dict[str, Any]) -> dict[str, Any]:
    row = {
        "comparison": name,
        "variant": variant,
        "left_run": left["run_dir"],
        "right_run": right["run_dir"],
    }
    for field in METRIC_FIELDS:
        row[f"delta_{field}"] = _delta(left.get(field), right.get(field))
    return row


def _delta(left: Any, right: Any) -> float | None:
    if left is None or right is None:
        return None
    return round(float(left) - float(right), 10)


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def _write_markdown_report(
    path: Path,
    rows: list[dict[str, Any]],
    comparisons: list[dict[str, Any]],
) -> None:
    test_rows = [row for row in rows if row["split"] == "test"]
    lines = [
        "# Phase 2A Ranking Robustness Report",
        "",
        f"Generated at: {datetime.now(timezone.utc).isoformat()}",
        "",
        "This report only uses explicit Phase 2A variant metric files. It does not mix in canonical Base/Y paths.",
        "",
        "## Test Metrics",
        "",
        _markdown_table(
            test_rows,
            ["model_key", "variant", "samples", "HR@1", "HR@5", "HR@10", "HR@20", "HR@50", "NDCG@5", "MRR"],
        ),
        "",
        "## Key Deltas",
        "",
        _markdown_table(
            comparisons,
            ["comparison", "variant", "delta_HR@1", "delta_HR@5", "delta_NDCG@5", "delta_MRR"],
        ),
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def _markdown_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._"
    lines = [
        "| " + " | ".join(fields) + " |",
        "|" + "|".join("---" for _ in fields) + "|",
    ]
    for row in rows:
        lines.append("| " + " | ".join(_format_value(row.get(field)) for field in fields) + " |")
    return "\n".join(lines)


def _format_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, float):
        return f"{value:.10g}"
    return str(value)


def _row_sort_key(row: dict[str, Any]) -> tuple[int, int, int, str]:
    model_order = DEFAULT_MODEL_ORDER.index(row["model_key"]) if row["model_key"] in DEFAULT_MODEL_ORDER else 99
    variant_order = DEFAULT_VARIANT_ORDER.index(row["variant"]) if row["variant"] in DEFAULT_VARIANT_ORDER else 99
    split_order = 0 if row["split"] == "validation" else 1
    return model_order, variant_order, split_order, row["run_dir"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Write Phase 2A ranking robustness report")
    parser.add_argument("--input-dir", default="outputs/phase2a/ranking_robustness")
    parser.add_argument("--output-dir", default=None)
    parser.add_argument("--dataset", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    summary = run_phase2a_robustness_report(
        input_dir=args.input_dir,
        output_dir=args.output_dir,
        dataset_key=args.dataset,
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
