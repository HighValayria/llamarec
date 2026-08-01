"""STEP 6/7 测试：N-K0 与 M-K0 adapter 评测入口。"""

from pathlib import Path

from src.inference.evaluate_m_adapter import run_m_adapter_evaluation
from src.inference.evaluate_n_adapter import run_n_adapter_evaluation
from src.inference.prediction_io import read_jsonl


def test_n_adapter_mock_evaluation_writes_predictions_and_metrics():
    output_dir = Path("outputs/test_n_adapter_evaluation")
    summary = run_n_adapter_evaluation(
        config_path="configs/n.yaml",
        dataset_key="movielens-100k",
        mode="mock",
        splits=["validation"],
        limit=2,
        batch_size=2,
        output_dir=output_dir,
    )

    output_dir = Path(summary["outputs_dir"])
    predictions = read_jsonl(output_dir / "n_valid_predictions.jsonl")

    assert summary["counts"]["validation"]["n_predictions"] == 2
    assert len(predictions) == 2
    assert predictions[0]["model"] == "n_k0"
    assert predictions[0]["inference_mode"] == "candidate_label_probability"
    assert len(predictions[0]["scores"]) == 5
    assert set(predictions[0]["label_probabilities"]) == {"A", "B", "C", "D", "E"}
    assert (output_dir / "valid_metrics.json").exists()
    assert (output_dir / "evaluation_summary.json").exists()


def test_m_adapter_mock_evaluation_writes_two_interfaces():
    output_dir = Path("outputs/test_m_adapter_evaluation")
    summary = run_m_adapter_evaluation(
        config_path="configs/m.yaml",
        dataset_key="movielens-100k",
        mode="mock",
        splits=["validation"],
        limit=2,
        batch_size=2,
        output_dir=output_dir,
    )

    output_dir = Path(summary["outputs_dir"])
    y_predictions = read_jsonl(output_dir / "m_y_valid_predictions.jsonl")
    n_predictions = read_jsonl(output_dir / "m_n_valid_predictions.jsonl")
    metrics = summary["metrics"]["validation"]

    assert summary["counts"]["validation"]["m_y_predictions"] == 2
    assert summary["counts"]["validation"]["m_n_predictions"] == 2
    assert y_predictions[0]["model"] == "m_k0"
    assert y_predictions[0]["inference_mode"] == "m_yesno_p_yes"
    assert n_predictions[0]["model"] == "m_k0"
    assert n_predictions[0]["inference_mode"] == "m_next_item_candidate_probability"
    assert "binary" in metrics
    assert "ranking" in metrics
    assert metrics["binary_scoring"] == "m_yesno_p_yes"
    assert metrics["ranking_scoring"] == "m_next_item_candidate_probability"
    assert (output_dir / "valid_metrics.json").exists()
    assert (output_dir / "evaluation_summary.json").exists()
