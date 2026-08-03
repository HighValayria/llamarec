"""Phase 1.5 STEP B：统一 Yes/No 二分类阈值口径报告。"""

from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import json
from pathlib import Path
from statistics import mean
from typing import Any

from src.analysis.threshold_calibration import (
    binary_metrics_at_threshold,
    find_best_threshold,
)
from src.data.config import load_experiment_config, resolve_repo_path_from_config
from src.eval.binary_metrics import auc
from src.inference.prediction_io import read_jsonl, write_json


def run_threshold_comparison(
    config_path: str | Path,
    dataset_key: str | None = None,
    y_run: str | None = None,
    m_runs: list[str] | None = None,
    m_labels: list[str] | None = None,
    output_dir: str | Path | None = None,
) -> dict[str, Any]:
    """读取 Base/Y/M 的 Y-task predictions，输出三种二分类评测口径。"""

    config = load_experiment_config(config_path)
    dataset_key = dataset_key or config["dataset"]["formal"]
    output_path = _resolve_output_dir(config, dataset_key, output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    specs = _prediction_specs(config, dataset_key, y_run, m_runs, m_labels)
    auc_rows: list[dict[str, Any]] = []
    fixed_rows: list[dict[str, Any]] = []
    calibrated_rows: list[dict[str, Any]] = []
    thresholds: dict[str, float] = {}

    for spec in specs:
        records_by_split = {
            "validation": _load_binary_records(spec["validation_path"]),
            "test": _load_binary_records(spec["test_path"]),
        }
        threshold = find_best_threshold(records_by_split["validation"])
        thresholds[spec["model"]] = threshold

        for split_name, records in records_by_split.items():
            auc_rows.append(_auc_row(spec, split_name, records))
            fixed_rows.append(
                _metric_row(
                    spec=spec,
                    split_name=split_name,
                    records=records,
                    threshold=0.5,
                    threshold_source="fixed_0.5",
                )
            )
            calibrated_rows.append(
                _metric_row(
                    spec=spec,
                    split_name=split_name,
                    records=records,
                    threshold=threshold,
                    threshold_source="validation_best_f1",
                )
            )

    paths = {
        "auc_csv": output_path / "binary_auc.csv",
        "fixed_csv": output_path / "binary_fixed_0_5.csv",
        "calibrated_csv": output_path / "binary_calibrated.csv",
        "json": output_path / "threshold_comparison.json",
        "report": output_path / "threshold_comparison.md",
    }
    _write_csv(paths["auc_csv"], auc_rows)
    _write_csv(paths["fixed_csv"], fixed_rows)
    _write_csv(paths["calibrated_csv"], calibrated_rows)
    write_json(
        paths["json"],
        {
            "dataset": dataset_key,
            "created_at_utc": datetime.now(timezone.utc).isoformat(),
            "selection_rule": "每个模型在 validation 上选择 best-F1 threshold，再应用到 validation/test。",
            "thresholds": thresholds,
            "tables": {
                "auc": auc_rows,
                "fixed_0_5": fixed_rows,
                "validation_calibrated": calibrated_rows,
            },
        },
    )
    _write_markdown_report(
        paths["report"],
        dataset_key=dataset_key,
        auc_rows=auc_rows,
        fixed_rows=fixed_rows,
        calibrated_rows=calibrated_rows,
    )

    return {
        "dataset": dataset_key,
        "models": len(specs),
        "rows": {
            "auc": len(auc_rows),
            "fixed_0_5": len(fixed_rows),
            "validation_calibrated": len(calibrated_rows),
        },
        "output_dir": str(output_path),
        "paths": {name: str(path) for name, path in paths.items()},
    }


def _prediction_specs(
    config: dict[str, Any],
    dataset_key: str,
    y_run: str | None,
    m_runs: list[str] | None,
    m_labels: list[str] | None,
) -> list[dict[str, Any]]:
    base_path = resolve_repo_path_from_config(config, config["outputs"]["base"], dataset_key=dataset_key)
    y_base = resolve_repo_path_from_config(config, config["outputs"]["y"], dataset_key=dataset_key)
    m_base = resolve_repo_path_from_config(config, config["outputs"]["m"], dataset_key=dataset_key)

    y_run = y_run or _latest_run_name(y_base)
    if not m_runs:
        m_runs = [_latest_run_name(m_base)]
    if m_labels and len(m_labels) != len(m_runs):
        raise ValueError("m_labels 数量必须与 m_runs 一致。")

    specs = [
        _binary_spec("base", "Base", "", base_path, "y"),
        _binary_spec("y", "Y-K0", y_run, y_base / y_run, "y"),
    ]
    for index, m_run in enumerate(m_runs):
        label = m_labels[index] if m_labels else ("M-K0" if len(m_runs) == 1 else f"M-K0:{m_run}")
        specs.append(_binary_spec("m", label, m_run, m_base / m_run, "m_y"))
    return specs


def _binary_spec(
    model_key: str,
    model: str,
    run_name: str,
    base_path: Path,
    file_prefix: str,
) -> dict[str, Any]:
    return {
        "model_key": model_key,
        "model": model,
        "run_name": run_name,
        "validation_path": base_path / f"{file_prefix}_valid_predictions.jsonl",
        "test_path": base_path / f"{file_prefix}_test_predictions.jsonl",
    }


def _load_binary_records(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        raise FileNotFoundError(f"找不到二分类 prediction 文件：{path}")
    records = []
    for record in read_jsonl(path):
        records.append(
            {
                "label": record["label"],
                "score": float(record.get("p_yes", record.get("score", 0.0))),
            }
        )
    if not records:
        raise ValueError(f"二分类 prediction 文件为空：{path}")
    return records


def _auc_row(spec: dict[str, Any], split_name: str, records: list[dict[str, Any]]) -> dict[str, Any]:
    labels = [_label_to_int(record["label"]) for record in records]
    scores = [float(record["score"]) for record in records]
    yes_scores = [score for score, label in zip(scores, labels) if label == 1]
    no_scores = [score for score, label in zip(scores, labels) if label == 0]
    return {
        "model_key": spec["model_key"],
        "model": spec["model"],
        "run_name": spec["run_name"],
        "split": split_name,
        "auc": _optional_round(auc(scores, labels)),
        "samples": len(records),
        "yes_labels": sum(labels),
        "no_labels": len(labels) - sum(labels),
        "positive_ratio": _round(sum(labels) / len(labels)),
        "mean_p_yes_for_yes": _round(mean(yes_scores)) if yes_scores else 0.0,
        "mean_p_yes_for_no": _round(mean(no_scores)) if no_scores else 0.0,
    }


def _metric_row(
    spec: dict[str, Any],
    split_name: str,
    records: list[dict[str, Any]],
    threshold: float,
    threshold_source: str,
) -> dict[str, Any]:
    metrics = binary_metrics_at_threshold(records, threshold)
    return {
        "model_key": spec["model_key"],
        "model": spec["model"],
        "run_name": spec["run_name"],
        "split": split_name,
        "threshold_source": threshold_source,
        **metrics,
    }


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def _write_markdown_report(
    path: Path,
    dataset_key: str,
    auc_rows: list[dict[str, Any]],
    fixed_rows: list[dict[str, Any]],
    calibrated_rows: list[dict[str, Any]],
) -> None:
    lines = [
        f"# {dataset_key} Binary Threshold Comparison",
        "",
        f"Generated at: {datetime.now(timezone.utc).isoformat()}",
        "",
        "本报告只比较 Y-task 的 Yes/No 二分类口径，不包含 N-task ranking 指标。",
        "",
        "## Table A：Threshold-free AUC",
        "",
        _markdown_table(
            auc_rows,
            [
                "model",
                "run_name",
                "split",
                "auc",
                "samples",
                "positive_ratio",
                "mean_p_yes_for_yes",
                "mean_p_yes_for_no",
            ],
        ),
        "",
        "## Table B：Fixed Threshold = 0.5",
        "",
        _markdown_table(
            fixed_rows,
            [
                "model",
                "run_name",
                "split",
                "threshold",
                "auc",
                "f1",
                "accuracy",
                "precision",
                "recall",
                "fp",
                "fn",
            ],
        ),
        "",
        "## Table C：Validation-calibrated Threshold",
        "",
        "每个模型先在 validation 上选择 best-F1 threshold，再将同一 threshold 应用于 test。",
        "",
        _markdown_table(
            calibrated_rows,
            [
                "model",
                "run_name",
                "split",
                "threshold",
                "auc",
                "f1",
                "accuracy",
                "precision",
                "recall",
                "fp",
                "fn",
            ],
        ),
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def _markdown_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._"
    output = [
        "| " + " | ".join(fields) + " |",
        "|" + "|".join("---" for _ in fields) + "|",
    ]
    for row in rows:
        output.append("| " + " | ".join(str(row.get(field, "")) for field in fields) + " |")
    return "\n".join(output)


def _latest_run_name(base_dir: Path) -> str:
    if not base_dir.exists():
        raise FileNotFoundError(f"找不到输出目录：{base_dir}")
    candidates = [path for path in base_dir.iterdir() if path.is_dir()]
    if not candidates:
        raise FileNotFoundError(f"输出目录下没有 run：{base_dir}")
    return max(candidates, key=lambda path: path.stat().st_mtime).name


def _resolve_output_dir(
    config: dict[str, Any],
    dataset_key: str,
    output_dir: str | Path | None,
) -> Path:
    if output_dir is not None:
        path = Path(output_dir)
        if path.is_absolute():
            return path
        return Path(config["_repo_root"]) / path
    return Path(config["_repo_root"]) / "outputs" / "calibration" / dataset_key / "threshold_comparison"


def _label_to_int(label: Any) -> int:
    if isinstance(label, str):
        normalized = label.strip().lower()
        if normalized == "yes":
            return 1
        if normalized == "no":
            return 0
    if label in {1, True}:
        return 1
    if label in {0, False}:
        return 0
    raise ValueError(f"无法解析二分类标签：{label!r}")


def _round(value: float) -> float:
    return round(float(value), 10)


def _optional_round(value: float | None) -> float | None:
    if value is None:
        return None
    return _round(value)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Phase 1.5 STEP B：统一 Yes/No 二分类阈值报告")
    parser.add_argument("--config", default="configs/experiment.yaml")
    parser.add_argument("--dataset", default=None)
    parser.add_argument("--y-run", default=None)
    parser.add_argument("--m-runs", nargs="*", default=None)
    parser.add_argument("--m-labels", nargs="*", default=None)
    parser.add_argument("--output-dir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    summary = run_threshold_comparison(
        config_path=args.config,
        dataset_key=args.dataset,
        y_run=args.y_run,
        m_runs=args.m_runs,
        m_labels=args.m_labels,
        output_dir=args.output_dir,
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
