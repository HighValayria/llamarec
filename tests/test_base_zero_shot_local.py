"""STEP 4 测试：Base zero-shot 本地 dry-run。"""

import json
from pathlib import Path

from src.inference.base_zero_shot import run_base_zero_shot
from src.inference.prediction_io import read_jsonl
from src.inference.prompts import (
    assert_no_candidate_rating_in_candidate_prompt,
    assert_no_target_rating_in_yesno_prompt,
    render_candidate_prompt,
    render_yesno_prompt,
)
from src.inference.scoring import MockScorer, RealModelScorer, build_scorer
from src.inference.tokenization_check import build_tokenization_report


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
    yesno_batch = scorer.score_yesno_batch(["prompt 1", "prompt 2"])
    candidate_batch = scorer.score_candidates_batch(
        ["prompt 1", "prompt 2"],
        [["A", "B"], ["A", "B"]],
    )

    assert abs(yesno["p_yes"] + yesno["p_no"] - 1.0) < 1e-9
    assert abs(sum(candidates["label_probabilities"].values()) - 1.0) < 1e-9
    assert candidates["predicted_label"] in {"A", "B", "C"}
    assert len(yesno_batch) == 2
    assert len(candidate_batch) == 2


def test_real_scorer_requires_config_before_loading_model():
    try:
        build_scorer("real")
    except ValueError as exc:
        assert "配置" in str(exc)
    else:
        raise AssertionError("real 模式缺少配置时应直接失败")


def test_tokenization_report_uses_loaded_tokenizer():
    class FakeTokenizer:
        def encode(self, text, add_special_tokens=False):
            token_map = {
                "Yes": [1],
                "No": [2],
                "Long": [3, 4],
            }
            return token_map[text]

    report = build_tokenization_report(
        mode="real",
        tokenizer=FakeTokenizer(),
        answers=["Yes", "No", "Long"],
    )

    assert report["checked"] is True
    assert report["answers"]["Yes"]["single_token"] is True
    assert report["answers"]["Long"]["token_count"] == 2
    assert report["use_sequence_likelihood_for"] == ["Long"]


def test_real_scorer_normalizes_tokenizer_outputs():
    class FakeTokenizer:
        def encode(self, text, add_special_tokens=False):
            if text == "chat text":
                return [7, 8, 9]
            return [1, 2, 3]

    scorer = RealModelScorer.__new__(RealModelScorer)
    scorer.tokenizer = FakeTokenizer()

    assert scorer._normalize_token_ids("chat text") == [7, 8, 9]
    assert scorer._normalize_token_ids([1, 2, 3]) == [1, 2, 3]
    assert scorer._normalize_token_ids([[1, 2, 3]]) == [1, 2, 3]


def test_real_scorer_accepts_wrapped_model_outputs_with_logits():
    class FakeTensor:
        device = "cpu"

        def __init__(self, data):
            self.data = data
            if isinstance(data[0][0], list):
                self.shape = (len(data), len(data[0]), len(data[0][0]))
            else:
                self.shape = (len(data), len(data[0]))

        def __getitem__(self, key):
            row_indexes, position_indexes = key
            return FakeTensor(
                [
                    self.data[row_index][position_index]
                    for row_index, position_index in zip(row_indexes, position_indexes)
                ]
            )

    class FakeTorch:
        long = "long"

        def arange(self, size, device=None):
            return list(range(size))

        def tensor(self, values, dtype=None, device=None):
            return list(values)

    class FakeOutput:
        def __init__(self):
            self.logits = FakeTensor(
                [
                    [[0.1, 0.2], [0.3, 0.4]],
                    [[0.5, 0.6], [0.7, 0.8]],
                ]
            )

    class FakeInnerModel:
        def __call__(self, input_ids, attention_mask, use_cache):
            return FakeOutput()

    class FakeWrappedModel:
        model = FakeInnerModel()

        def lm_head(self, hidden_states):
            raise AssertionError("已有 logits 时不应再调用 lm_head")

    scorer = RealModelScorer.__new__(RealModelScorer)
    scorer.model = FakeWrappedModel()
    scorer.torch = FakeTorch()

    selected = scorer._last_token_logits(
        input_ids=None,
        attention_mask=None,
        last_positions=[1, 0],
    )

    assert selected.data == [[0.3, 0.4], [0.5, 0.6]]


def test_base_zero_shot_mock_writes_predictions_and_metrics():
    summary = run_base_zero_shot(
        config_path="configs/experiment.yaml",
        dataset_key="movielens-100k",
        mode="mock",
        splits=["validation"],
        limit=3,
        batch_size=2,
    )

    output_dir = Path(summary["outputs_dir"])
    y_predictions = read_jsonl(output_dir / "y_valid_predictions.jsonl")
    n_predictions = read_jsonl(output_dir / "n_valid_predictions.jsonl")

    assert summary["batch_size"] == 2
    assert len(y_predictions) == 3
    assert len(n_predictions) == 3
    assert (output_dir / "valid_metrics.json").exists()
    assert (output_dir / "tokenization_report.json").exists()


def test_base_zero_shot_mock_accepts_candidate_file_override(tmp_path):
    candidate_path = tmp_path / "valid.jsonl"
    labels = [chr(ord("A") + index) for index in range(20)]
    record = {
        "dataset": "movielens-100k",
        "split": "validation",
        "source_task": "N",
        "source_sample_index": 0,
        "user_id": "1",
        "history": [
            {
                "movie_id": "1",
                "title": "History Movie",
                "rating": 5.0,
                "timestamp": 1,
                "sequence_index": 0,
            }
        ],
        "target": {
            "movie_id": "2",
            "title": "Ground Truth",
            "rating": 4.0,
            "timestamp": 2,
            "sequence_index": 1,
        },
        "candidate_movie_ids": [str(index) for index in range(2, 22)],
        "ground_truth_movie_id": "2",
        "ground_truth_index": 0,
        "label": "A",
        "label_set": labels,
        "candidate_generation": {
            "variant_name": "k20_test",
            "candidate_num": 20,
        },
    }
    candidate_path.write_text(json.dumps(record) + "\n", encoding="utf-8")

    summary = run_base_zero_shot(
        config_path="configs/experiment.yaml",
        dataset_key="movielens-100k",
        mode="mock",
        splits=["validation"],
        limit=1,
        batch_size=1,
        candidate_files={"validation": candidate_path},
    )

    output_dir = Path(summary["outputs_dir"])
    n_predictions = read_jsonl(output_dir / "n_valid_predictions.jsonl")
    metrics = summary["metrics"]["validation"]["ranking"]

    assert len(n_predictions[0]["scores"]) == 20
    assert n_predictions[0]["candidate_generation"]["variant_name"] == "k20_test"
    assert "HR@20" in metrics
    assert summary["candidate_files"]["validation"] == str(candidate_path)
