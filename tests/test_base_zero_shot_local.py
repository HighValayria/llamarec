"""STEP 4 测试：Base zero-shot 本地 dry-run。"""

from pathlib import Path

from src.inference.base_zero_shot import run_base_zero_shot
from src.inference.prediction_io import read_jsonl
from src.inference.prompts import (
    assert_no_candidate_rating_in_candidate_prompt,
    assert_no_target_rating_in_yesno_prompt,
    render_candidate_prompt,
    render_yesno_prompt,
)
from src.inference.scoring import MockScorer


def test_yesno_prompt_does_not_leak_target_rating():
    sample = {
        "history": [
            {"movie_id": "1", "title": "History Movie", "rating": 5.0}
        ],
        "target": {
            "movie_id": "2",
            "title": "Target Movie",
            "rating": 3.0,
        },
    }

    prompt = render_yesno_prompt(sample)

    assert "History Movie (rating: 5)" in prompt
    assert "Target Movie" in prompt
    assert_no_target_rating_in_yesno_prompt(prompt, sample)


def test_candidate_prompt_does_not_include_ratings():
    record = {
        "history": [
            {"movie_id": "1", "title": "History Movie", "rating": 5.0}
        ],
        "candidate_movie_ids": ["2", "3"],
        "label_set": ["A", "B"],
    }
    movie_lookup = {
        "2": {"title": "Candidate Two"},
        "3": {"title": "Candidate Three"},
    }

    prompt = render_candidate_prompt(record, movie_lookup)

    assert "Candidate Two" in prompt
    assert "Candidate Three" in prompt
    assert_no_candidate_rating_in_candidate_prompt(prompt)


def test_mock_scorer_outputs_probabilities():
    scorer = MockScorer()

    yesno = scorer.score_yesno("prompt")
    candidates = scorer.score_candidates("prompt", ["A", "B", "C"])

    assert abs(yesno["p_yes"] + yesno["p_no"] - 1.0) < 1e-9
    assert abs(sum(candidates["label_probabilities"].values()) - 1.0) < 1e-9
    assert candidates["predicted_label"] in {"A", "B", "C"}


def test_base_zero_shot_mock_writes_predictions_and_metrics():
    summary = run_base_zero_shot(
        config_path="configs/experiment.yaml",
        dataset_key="movielens-100k",
        mode="mock",
        splits=["validation"],
        limit=2,
    )

    output_dir = Path(summary["outputs_dir"])
    y_predictions = read_jsonl(output_dir / "y_valid_predictions.jsonl")
    n_predictions = read_jsonl(output_dir / "n_valid_predictions.jsonl")

    assert len(y_predictions) == 2
    assert len(n_predictions) == 2
    assert (output_dir / "valid_metrics.json").exists()
    assert (output_dir / "tokenization_report.json").exists()
