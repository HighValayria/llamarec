"""STEP 8 测试：结果汇总与基础错误分析。"""

import csv
import json
from pathlib import Path

from src.analysis.basic_error_analysis import run_basic_error_analysis
from src.analysis.summarize_results import run_result_summary


def test_result_summary_writes_csv_and_report(tmp_path):
    _write_config(tmp_path)
    _write_metrics_tree(tmp_path)

    summary = run_result_summary(
        config_path=tmp_path / "configs" / "experiment.yaml",
        dataset_key="toy",
        y_run="run_y",
        n_run="run_n",
        m_run="run_m",
        splits=["test"],
        output_csv=tmp_path / "outputs" / "results.csv",
        report_path=tmp_path / "outputs" / "report.md",
    )

    rows = list(csv.DictReader((tmp_path / "outputs" / "results.csv").open()))

    assert summary["rows"] == 4
    assert [row["model"] for row in rows] == ["Base", "Y-K0", "N-K0", "M-K0"]
    assert rows[2]["binary_auc"] == ""
    assert rows[2]["hr_at_1"] == "0.7000000000"
    assert "MVP Results" in (tmp_path / "outputs" / "report.md").read_text(
        encoding="utf-8"
    )


def test_basic_error_analysis_writes_summaries_and_examples(tmp_path):
    _write_config(tmp_path)
    _write_prediction_tree(tmp_path)

    summary = run_basic_error_analysis(
        config_path=tmp_path / "configs" / "experiment.yaml",
        dataset_key="toy",
        y_run="run_y",
        n_run="run_n",
        m_run="run_m",
        split_name="test",
        output_dir=tmp_path / "outputs" / "error_analysis" / "toy",
        example_limit=2,
    )

    output_dir = Path(summary["output_dir"])
    binary_rows = list(csv.DictReader((output_dir / "test_binary_error_summary.csv").open()))
    ranking_rows = list(csv.DictReader((output_dir / "test_ranking_error_summary.csv").open()))
    examples = [
        json.loads(line)
        for line in (output_dir / "test_error_examples.jsonl").read_text(
            encoding="utf-8"
        ).splitlines()
        if line.strip()
    ]

    assert summary["binary_models"] == 3
    assert summary["ranking_models"] == 4
    assert binary_rows[0]["fp"] == "1"
    assert ranking_rows[0]["rank_distribution"] == '{"1": 1, "2": 1}'
    assert any(example["error_type"] == "ranking_miss" for example in examples)
    assert (output_dir / "test_error_analysis.md").exists()


def _write_config(root: Path) -> None:
    config_dir = root / "configs"
    config_dir.mkdir(parents=True)
    (config_dir / "experiment.yaml").write_text(
        "\n".join(
            [
                "dataset:",
                "  formal: toy",
                "outputs:",
                "  base: outputs/base/{dataset}",
                "  y: outputs/y/{dataset}",
                "  n: outputs/n/{dataset}",
                "  m: outputs/m/{dataset}",
                "  aggregate_results: outputs/results.csv",
            ]
        ),
        encoding="utf-8",
    )


def _write_metrics_tree(root: Path) -> None:
    metrics = {
        "base": _metrics(binary_auc=0.6, hr_at_1=0.3),
        "y": _metrics(binary_auc=0.8, hr_at_1=0.25),
        "n": _metrics(binary_auc=None, hr_at_1=0.7),
        "m": _metrics(binary_auc=0.75, hr_at_1=0.65),
    }
    _write_json(root / "outputs" / "base" / "toy" / "test_metrics.json", metrics["base"])
    _write_json(root / "outputs" / "y" / "toy" / "run_y" / "test_metrics.json", metrics["y"])
    _write_json(root / "outputs" / "n" / "toy" / "run_n" / "test_metrics.json", metrics["n"])
    _write_json(root / "outputs" / "m" / "toy" / "run_m" / "test_metrics.json", metrics["m"])


def _metrics(binary_auc, hr_at_1):
    payload = {
        "model": "model",
        "dataset": "toy",
        "split": "test",
        "ranking": {
            "HR@1": hr_at_1,
            "HR@5": 1.0,
            "NDCG@5": 0.8,
            "MRR": 0.75,
            "samples": 2,
        },
    }
    if binary_auc is not None:
        payload["binary"] = {
            "AUC": binary_auc,
            "F1": 0.7,
            "Accuracy": 0.65,
            "samples": 2,
        }
    return payload


def _write_prediction_tree(root: Path) -> None:
    _write_jsonl(
        root / "outputs" / "base" / "toy" / "y_test_predictions.jsonl",
        _binary_predictions("base"),
    )
    _write_jsonl(
        root / "outputs" / "base" / "toy" / "n_test_predictions.jsonl",
        _ranking_predictions("base"),
    )
    _write_jsonl(
        root / "outputs" / "y" / "toy" / "run_y" / "y_test_predictions.jsonl",
        _binary_predictions("y_k0"),
    )
    _write_jsonl(
        root / "outputs" / "y" / "toy" / "run_y" / "n_test_predictions.jsonl",
        _ranking_predictions("y_k0"),
    )
    _write_jsonl(
        root / "outputs" / "n" / "toy" / "run_n" / "n_test_predictions.jsonl",
        _ranking_predictions("n_k0"),
    )
    _write_jsonl(
        root / "outputs" / "m" / "toy" / "run_m" / "m_y_test_predictions.jsonl",
        _binary_predictions("m_k0"),
    )
    _write_jsonl(
        root / "outputs" / "m" / "toy" / "run_m" / "m_n_test_predictions.jsonl",
        _ranking_predictions("m_k0"),
    )


def _binary_predictions(model: str):
    return [
        {
            "model": model,
            "task": "Y",
            "split": "test",
            "user_id": "u1",
            "target_movie_id": "m1",
            "label": "Yes",
            "p_yes": 0.9,
            "predicted_label": "Yes",
        },
        {
            "model": model,
            "task": "Y",
            "split": "test",
            "user_id": "u2",
            "target_movie_id": "m2",
            "label": "No",
            "p_yes": 0.8,
            "predicted_label": "Yes",
        },
    ]


def _ranking_predictions(model: str):
    return [
        {
            "model": model,
            "task": "N",
            "split": "test",
            "user_id": "u1",
            "candidate_movie_ids": ["a", "b"],
            "ground_truth_movie_id": "a",
            "ground_truth_index": 0,
            "scores": [0.9, 0.1],
        },
        {
            "model": model,
            "task": "N",
            "split": "test",
            "user_id": "u2",
            "candidate_movie_ids": ["c", "d"],
            "ground_truth_movie_id": "d",
            "ground_truth_index": 1,
            "scores": [0.7, 0.3],
        },
    ]


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload), encoding="utf-8")


def _write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "\n".join(json.dumps(row) for row in rows) + "\n",
        encoding="utf-8",
    )
