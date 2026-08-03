"""二分类阈值校准：用 validation 选择阈值，再应用到 test。"""

from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import json
from pathlib import Path
from statistics import mean
from typing import Any

from src.data.config import load_experiment_config, resolve_repo_path_from_config
from src.eval.binary_metrics import auc
from src.inference.prediction_io import read_jsonl, write_json


SPLIT_TO_FILE = {
    "validation": "valid",
    "valid": "valid",
    "test": "test",
}


def run_threshold_calibration(
    config_path: str | Path,
    dataset_key: str | None = None,
    y_run: str | None = None,
    m_runs: list[str] | None = None,
    m_labels: list[str] | None = None,
    output_dir: str | Path | None = None,
) -> dict[str, Any]:
    """用 validation 的 best-F1 threshold 评估 Base/Y/M 的 test 表现。"""

    config = load_experiment_config(config_path)
    dataset_key = dataset_key or config["dataset"]["formal"]
    output_path = _resolve_output_dir(config, dataset_key, output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    specs = _prediction_specs(config, dataset_key, y_run, m_runs, m_labels)
    rows = []
    for spec in specs:
        valid_records = _load_binary_records(spec["validation_path"])
        test_records = _load_binary_records(spec["test_path"])
        threshold = find_best_threshold(valid_records)
        rows.append(
            _summary_row(
                spec=spec,
                split_name="validation",
                records=valid_records,
                threshold=threshold,
                threshold_source="validation_best_f1",
            )
        )
        rows.append(
            _summary_row(
                spec=spec,
                split_name="test",
                records=test_records,
                threshold=threshold,
                threshold_source="validation_best_f1",
            )
        )

    csv_path = output_path / "threshold_calibration.csv"
    json_path = output_path / "threshold_calibration.json"
    report_path = output_path / "threshold_calibration.md"
    _write_csv(csv_path, rows)
    write_json(
        json_path,
        {
            "dataset": dataset_key,
            "created_at_utc": datetime.now(timezone.utc).isoformat(),
            "selection_rule": "maximize validation F1; tie-break by accuracy, closeness to 0.5, then lower threshold",
            "rows": rows,
        },
    )
    _write_markdown_report(report_path, dataset_key, rows)

    return {
        "dataset": dataset_key,
        "models": len(specs),
        "rows": len(rows),
        "output_dir": str(output_path),
        "csv_path": str(csv_path),
        "json_path": str(json_path),
        "report_path": str(report_path),
    }


def find_best_threshold(records: list[dict[str, Any]]) -> float:
    """在 validation records 上选择正类 F1 最优阈值。"""

    if not records:
        raise ValueError("阈值校准需要非空 validation records。")
    candidates = sorted({0.0, 0.5, 1.0, *[float(record["score"]) for record in records]})
    best_threshold = candidates[0]
    best_key: tuple[float, float, float, float] | None = None
    for threshold in candidates:
        metrics = binary_metrics_at_threshold(records, threshold)
        key = (
            float(metrics["f1"]),
            float(metrics["accuracy"]),
            -abs(threshold - 0.5),
            -threshold,
        )
        if best_key is None or key > best_key:
            best_key = key
            best_threshold = threshold
    return float(best_threshold)


def binary_metrics_at_threshold(
    records: list[dict[str, Any]],
    threshold: float,
) -> dict[str, Any]:
    """按指定 threshold 计算二分类指标和混淆矩阵。"""

    labels = [_label_to_int(record["label"]) for record in records]
    scores = [float(record["score"]) for record in records]
    predictions = [1 if score >= threshold else 0 for score in scores]

    tp = sum(1 for pred, label in zip(predictions, labels) if pred == label == 1)
    tn = sum(1 for pred, label in zip(predictions, labels) if pred == label == 0)
    fp = sum(1 for pred, label in zip(predictions, labels) if pred == 1 and label == 0)
    fn = sum(1 for pred, label in zip(predictions, labels) if pred == 0 and label == 1)
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    accuracy = (tp + tn) / len(records) if records else 0.0
    yes_scores = [score for score, label in zip(scores, labels) if label == 1]
    no_scores = [score for score, label in zip(scores, labels) if label == 0]

    return {
        "threshold": _round(threshold),
        "samples": len(records),
        "yes_labels": sum(labels),
        "no_labels": len(labels) - sum(labels),
        "predicted_yes": sum(predictions),
        "predicted_no": len(predictions) - sum(predictions),
        "tp": tp,
        "tn": tn,
        "fp": fp,
        "fn": fn,
        "precision": _round(precision),
        "recall": _round(recall),
        "f1": _round(f1),
        "accuracy": _round(accuracy),
        "auc": _optional_round(auc(scores, labels)),
        "mean_p_yes_for_yes": _round(mean(yes_scores)) if yes_scores else 0.0,
        "mean_p_yes_for_no": _round(mean(no_scores)) if no_scores else 0.0,
    }


def _prediction_specs(
    config: dict[str, Any],
    dataset_key: str,
    y_run: str | None,
    m_runs: list[str] | None,
    m_labels: list[str] | None,
) -> list[dict[str, Any]]:
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
    m_base = resolve_repo_path_from_config(
        config,
        config["outputs"]["m"],
        dataset_key=dataset_key,
    )
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
    model_label: str,
    run_name: str,
    base_path: Path,
    file_prefix: str,
) -> dict[str, Any]:
    return {
        "model_key": model_key,
        "model": model_label,
        "run_name": run_name,
        "validation_path": base_path / f"{file_prefix}_valid_predictions.jsonl",
        "test_path": base_path / f"{file_prefix}_test_predictions.jsonl",
    }


def _load_binary_records(path: Path) -> list[dict[str, Any]]:
    records = []
    for record in read_jsonl(path):
        records.append(
            {
                "label": record["label"],
                "score": float(record.get("p_yes", record.get("score", 0.0))),
            }
        )
    return records


def _summary_row(
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
    fieldnames = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _write_markdown_report(path: Path, dataset_key: str, rows: list[dict[str, Any]]) -> None:
    fields = [
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
        "mean_p_yes_for_yes",
        "mean_p_yes_for_no",
    ]
    lines = [
        f"# {dataset_key} Threshold Calibration",
        "",
        f"Generated at: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Threshold is selected on validation by best F1, then applied to test.",
        "",
        _markdown_table(rows, fields),
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
        raise FileNotFoundError(f"找不到输出目录: {base_dir}")
    candidates = [path for path in base_dir.iterdir() if path.is_dir()]
    if not candidates:
        raise FileNotFoundError(f"输出目录下没有 run: {base_dir}")
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
    return Path(config["_repo_root"]) / "outputs" / "calibration" / dataset_key


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
    raise ValueError(f"无法解析二分类标签: {label!r}")


def _round(value: float) -> float:
    return round(float(value), 10)


def _optional_round(value: float | None) -> float | None:
    if value is None:
        return None
    return _round(value)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="基于 validation 的 Yes/No threshold calibration")
    parser.add_argument("--config", default="configs/experiment.yaml")
    parser.add_argument("--dataset", default=None)
    parser.add_argument("--y-run", default=None)
    parser.add_argument("--m-runs", nargs="*", default=None)
    parser.add_argument("--m-labels", nargs="*", default=None)
    parser.add_argument("--output-dir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    summary = run_threshold_calibration(
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
