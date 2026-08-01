"""STEP 5 测试：Y-K0 adapter 评测入口。"""

from pathlib import Path

from src.inference.evaluate_y_adapter import (
    _candidate_preference_sample,
    _record_batch_size_for_candidate_prompts,
    run_y_adapter_evaluation,
)
from src.inference.prediction_io import read_jsonl
from src.inference.prompts import (
    assert_no_target_rating_in_yesno_prompt,
    render_yesno_prompt,
)


def test_y_adapter_mock_evaluation_writes_predictions_and_metrics():
    output_dir = Path("outputs/test_y_adapter_evaluation")
    summary = run_y_adapter_evaluation(
        config_path="configs/y.yaml",
        dataset_key="movielens-100k",
        mode="mock",
        splits=["validation"],
        limit=2,
        batch_size=10,
        output_dir=output_dir,
    )

    output_dir = Path(summary["outputs_dir"])
    y_predictions = read_jsonl(output_dir / "y_valid_predictions.jsonl")
    n_predictions = read_jsonl(output_dir / "n_valid_predictions.jsonl")

    assert summary["counts"]["validation"]["y_predictions"] == 2
    assert summary["counts"]["validation"]["n_predictions"] == 2
    assert len(y_predictions) == 2
    assert len(n_predictions) == 2
    assert y_predictions[0]["model"] == "y_k0"
    assert y_predictions[0]["inference_mode"] == "yesno_p_yes"
    assert n_predictions[0]["inference_mode"] == "candidate_sort_by_p_yes"
    assert n_predictions[0]["scores"] == n_predictions[0]["candidate_p_yes"]
    assert len(n_predictions[0]["scores"]) == 5
    assert (output_dir / "valid_metrics.json").exists()
    assert (output_dir / "evaluation_summary.json").exists()
    assert (output_dir / "evaluation_tokenization_report.json").exists()


def test_candidate_preference_sample_has_no_candidate_rating():
    record = {
        "user_id": "u1",
        "history": [
            {
                "movie_id": "1",
                "title": "History Movie",
                "rating": 5.0,
            }
        ],
    }
    sample = _candidate_preference_sample(
        record=record,
        movie_id="2",
        movie_lookup={"2": {"title": "Candidate Movie"}},
    )

    prompt = render_yesno_prompt(sample)

    assert sample["target"] == {"movie_id": "2", "title": "Candidate Movie"}
    assert "Candidate Movie" in prompt
    assert_no_target_rating_in_yesno_prompt(prompt, sample)


def test_n_by_y_record_batch_size_keeps_prompt_batch_under_limit():
    records = [
        {"candidate_movie_ids": ["1", "2", "3", "4", "5"]},
        {"candidate_movie_ids": ["6", "7", "8", "9", "10"]},
    ]

    assert _record_batch_size_for_candidate_prompts(records, batch_size=16) == 3
    assert _record_batch_size_for_candidate_prompts(records, batch_size=4) == 1
