"""STEP 8：汇总 Base/Y/N/M 主结果表。"""

from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any

from src.data.config import load_experiment_config, resolve_repo_path_from_config


SPLIT_TO_FILE = {
    "validation": "valid",
    "valid": "valid",
    "test": "test",
}


def run_result_summary(
    config_path: str | Path,
    dataset_key: str | None = None,
    y_run: str | None = None,
    n_run: str | None = None,
    m_run: str | None = None,
    splits: list[str] | None = None,
    output_csv: str | Path | None = None,
    report_path: str | Path | None = None,
) -> dict[str, Any]:
    """读取各模型 metrics.json 并写出统一 CSV 与 Markdown 报告。"""

    config = load_experiment_config(config_path)
    dataset_key = dataset_key or config["dataset"]["formal"]
    split_names = _normalize_splits(splits or ["validation", "test"])

    paths = _resolve_model_paths(config, dataset_key, y_run, n_run, m_run)
    rows = []
    for model_key, model_info in paths.items():
        for split_name in split_names:
            metrics_path = model_info["path"] / f"{SPLIT_TO_FILE[split_name]}_metrics.json"
            metrics = _read_json(metrics_path)
            rows.append(
                _flatten_metrics_row(
                    dataset_key=dataset_key,
                    split_name=split_name,
                    model_key=model_key,
                    model_label=model_info["label"],
                    run_name=model_info.get("run_name"),
                    metrics_path=metrics_path,
                    metrics=metrics,
                )
            )

    output_csv_path = _resolve_output_csv(config, dataset_key, output_csv)
    report_output_path = _resolve_report_path(config, dataset_key, report_path)
    _write_csv(output_csv_path, rows)
    _write_report(report_output_path, rows, dataset_key)

    return {
        "dataset": dataset_key,
        "rows": len(rows),
        "splits": split_names,
        "output_csv": str(output_csv_path),
        "report_path": str(report_output_path),
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
    }


def _resolve_model_paths(
    config: dict[str, Any],
    dataset_key: str,
    y_run: str | None,
    n_run: str | None,
    m_run: str | None,
) -> dict[str, dict[str, Any]]:
    base_path = resolve_repo_path_from_config(
        config,
        config["outputs"]["base"],
        dataset_key=dataset_key,
    )
    y_base = resolve_repo_path_from_config(
        config,
        config["outputs"]["y"],
        dataset_key=dataset_key,
    )
    n_base = resolve_repo_path_from_config(
        config,
        config["outputs"]["n"],
        dataset_key=dataset_key,
    )
    m_base = resolve_repo_path_from_config(
        config,
        config["outputs"]["m"],
        dataset_key=dataset_key,
    )

    y_run = y_run or _latest_run_name(y_base)
    n_run = n_run or _latest_run_name(n_base)
    m_run = m_run or _latest_run_name(m_base)

    return {
        "base": {"label": "Base", "path": base_path, "run_name": ""},
        "y": {"label": "Y-K0", "path": y_base / y_run, "run_name": y_run},
        "n": {"label": "N-K0", "path": n_base / n_run, "run_name": n_run},
        "m": {"label": "M-K0", "path": m_base / m_run, "run_name": m_run},
    }


def _latest_run_name(base_dir: Path) -> str:
    if not base_dir.exists():
        raise FileNotFoundError(f"找不到输出目录: {base_dir}")
    candidates = [path for path in base_dir.iterdir() if path.is_dir()]
    if not candidates:
        raise FileNotFoundError(f"输出目录下没有 run: {base_dir}")
    return max(candidates, key=lambda path: path.stat().st_mtime).name


def _flatten_metrics_row(
    dataset_key: str,
    split_name: str,
    model_key: str,
    model_label: str,
    run_name: str | None,
    metrics_path: Path,
    metrics: dict[str, Any],
) -> dict[str, Any]:
    binary = metrics.get("binary", {})
    ranking = metrics.get("ranking", {})
    return {
        "dataset": dataset_key,
        "split": split_name,
        "model_key": model_key,
        "model": model_label,
        "run_name": run_name or "",
        "binary_auc": _optional_float(binary.get("AUC")),
        "binary_f1": _optional_float(binary.get("F1")),
        "binary_accuracy": _optional_float(binary.get("Accuracy")),
        "binary_samples": binary.get("samples", ""),
        "hr_at_1": _optional_float(ranking.get("HR@1")),
        "hr_at_5": _optional_float(ranking.get("HR@5")),
        "ndcg_at_5": _optional_float(ranking.get("NDCG@5")),
        "mrr": _optional_float(ranking.get("MRR")),
        "ranking_samples": ranking.get("samples", ""),
        "binary_scoring": metrics.get("binary_scoring", ""),
        "ranking_scoring": metrics.get("ranking_scoring", ""),
        "metrics_path": str(metrics_path),
    }


def _optional_float(value: Any) -> str:
    if value is None or value == "":
        return ""
    return f"{float(value):.10f}"


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "dataset",
        "split",
        "model_key",
        "model",
        "run_name",
        "binary_auc",
        "binary_f1",
        "binary_accuracy",
        "binary_samples",
        "hr_at_1",
        "hr_at_5",
        "ndcg_at_5",
        "mrr",
        "ranking_samples",
        "binary_scoring",
        "ranking_scoring",
        "metrics_path",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _write_report(path: Path, rows: list[dict[str, Any]], dataset_key: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    test_rows = [row for row in rows if row["split"] == "test"]
    valid_rows = [row for row in rows if row["split"] == "validation"]
    lines = [
        f"# {dataset_key} MVP Results",
        "",
        f"Generated at: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Test",
        "",
        _markdown_table(test_rows),
        "",
        "## Validation",
        "",
        _markdown_table(valid_rows),
        "",
        "## Notes",
        "",
        "- HR@5 is expected to have little discrimination when candidate_num is 5.",
        "- Y-K0 ranking uses candidate sorting by P(Yes).",
        "- N-K0 and M-K0 ranking use candidate label probabilities.",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def _markdown_table(rows: list[dict[str, Any]]) -> str:
    headers = ["Model", "AUC", "F1", "Acc", "HR@1", "NDCG@5", "MRR"]
    output = [
        "| " + " | ".join(headers) + " |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for row in rows:
        output.append(
            "| "
            + " | ".join(
                [
                    row["model"],
                    _display_metric(row["binary_auc"]),
                    _display_metric(row["binary_f1"]),
                    _display_metric(row["binary_accuracy"]),
                    _display_metric(row["hr_at_1"]),
                    _display_metric(row["ndcg_at_5"]),
                    _display_metric(row["mrr"]),
                ]
            )
            + " |"
        )
    return "\n".join(output)


def _display_metric(value: Any) -> str:
    if value == "" or value is None:
        return "-"
    return f"{float(value):.4f}"


def _resolve_output_csv(
    config: dict[str, Any],
    dataset_key: str,
    output_csv: str | Path | None,
) -> Path:
    if output_csv is not None:
        path = Path(output_csv)
        if path.is_absolute():
            return path
        return Path(config["_repo_root"]) / path
    return resolve_repo_path_from_config(
        config,
        config["outputs"].get("aggregate_results", "outputs/results.csv"),
        dataset_key=dataset_key,
    )


def _resolve_report_path(
    config: dict[str, Any],
    dataset_key: str,
    report_path: str | Path | None,
) -> Path:
    if report_path is not None:
        path = Path(report_path)
        if path.is_absolute():
            return path
        return Path(config["_repo_root"]) / path
    return Path(config["_repo_root"]) / "outputs" / "reports" / f"{dataset_key}_mvp_report.md"


def _normalize_splits(splits: list[str]) -> list[str]:
    normalized = []
    for split in splits:
        key = "validation" if split == "valid" else split
        if key not in {"validation", "test"}:
            raise ValueError(f"不支持的 split: {split}")
        normalized.append(key)
    return normalized


def _read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"metrics 文件不存在: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="汇总 Base/Y/N/M 主结果表")
    parser.add_argument("--config", default="configs/experiment.yaml")
    parser.add_argument("--dataset", default=None)
    parser.add_argument("--y-run", default=None)
    parser.add_argument("--n-run", default=None)
    parser.add_argument("--m-run", default=None)
    parser.add_argument("--splits", nargs="+", default=["validation", "test"])
    parser.add_argument("--output-csv", default=None)
    parser.add_argument("--report-path", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    summary = run_result_summary(
        config_path=args.config,
        dataset_key=args.dataset,
        y_run=args.y_run,
        n_run=args.n_run,
        m_run=args.m_run,
        splits=args.splits,
        output_csv=args.output_csv,
        report_path=args.report_path,
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
