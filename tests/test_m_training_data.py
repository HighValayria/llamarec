"""STEP 7 测试：M-K0 多任务训练数据编码。"""

from src.train.multitask_dataset import (
    MultitaskTrainingDataset,
    count_ratio_examples,
    summarize_multitask_examples,
)
from src.train.preference_dataset import IGNORE_INDEX
from src.train.train_m import (
    _resolve_task_ratio,
    _select_train_sampler_dataset,
    _should_run_per_task_validation,
)
from src.train.train_y import load_training_config


class FakeTokenizer:
    pad_token_id = 0
    eos_token_id = 2

    def encode(self, text, add_special_tokens=True):
        prefix = [101] if add_special_tokens else []
        return prefix + [(ord(char) % 89) + 10 for char in text]


def _movie_lookup():
    return {
        "2": {"title": "Candidate Two"},
        "3": {"title": "Candidate Three"},
        "4": {"title": "Candidate Four"},
        "5": {"title": "Candidate Five"},
        "6": {"title": "Candidate Six"},
    }


def _y_sample(user_id="u1", label="Yes"):
    return {
        "task": "Y",
        "user_id": user_id,
        "history": [
            {
                "movie_id": "1",
                "title": "History Movie",
                "rating": 5.0,
                "timestamp": 1,
            }
        ],
        "target": {
            "movie_id": "2",
            "title": "Target Movie",
            "rating": 4.0 if label == "Yes" else 2.0,
            "timestamp": 2,
        },
        "label": label,
    }


def _n_sample(user_id="u1", label="C"):
    label_set = ["A", "B", "C", "D", "E"]
    return {
        "task": "N",
        "user_id": user_id,
        "history": [
            {
                "movie_id": "1",
                "title": "History Movie",
                "rating": 5.0,
                "timestamp": 1,
            }
        ],
        "target": {
            "movie_id": "4",
            "title": "Candidate Four",
            "rating": 2.0,
            "timestamp": 2,
        },
        "candidate_movie_ids": ["2", "3", "4", "5", "6"],
        "ground_truth_movie_id": "4",
        "ground_truth_index": 2,
        "label": label,
        "label_set": label_set,
    }


def test_multitask_dataset_interleaves_y_and_n_examples():
    dataset = MultitaskTrainingDataset(
        preference_records=[_y_sample("u1"), _y_sample("u2", "No")],
        next_item_records=[_n_sample("u1", "C"), _n_sample("u2", "A")],
        tokenizer=FakeTokenizer(),
        movie_lookup=_movie_lookup(),
        max_seq_length=512,
        use_chat_format=False,
    )

    assert len(dataset) == 4
    assert [dataset[index]["task"] for index in range(len(dataset))] == [
        "Y",
        "N",
        "Y",
        "N",
    ]
    assert dataset.task_counts == {"Y": 2, "N": 2}


def test_multitask_dataset_uses_balanced_pair_count():
    dataset = MultitaskTrainingDataset(
        preference_records=[_y_sample("u1"), _y_sample("u2"), _y_sample("u3")],
        next_item_records=[_n_sample("u1")],
        tokenizer=FakeTokenizer(),
        movie_lookup=_movie_lookup(),
        max_seq_length=512,
        use_chat_format=False,
    )

    assert len(dataset) == 2
    assert dataset.task_counts == {"Y": 1, "N": 1}


def test_multitask_dataset_supports_y_heavy_ratio():
    dataset = MultitaskTrainingDataset(
        preference_records=[
            _y_sample("u1"),
            _y_sample("u2"),
            _y_sample("u3"),
            _y_sample("u4"),
            _y_sample("u5"),
        ],
        next_item_records=[_n_sample("u1"), _n_sample("u2"), _n_sample("u3")],
        tokenizer=FakeTokenizer(),
        movie_lookup=_movie_lookup(),
        max_seq_length=512,
        use_chat_format=False,
        task_ratio_y=2,
        task_ratio_n=1,
    )

    assert [dataset[index]["task"] for index in range(len(dataset))] == [
        "Y",
        "Y",
        "N",
        "Y",
        "Y",
        "N",
    ]
    assert dataset.task_counts == {"Y": 4, "N": 2}
    assert dataset.task_ratio == {"Y": 2, "N": 1}
    assert dataset.cycle_count == 2


def test_multitask_dataset_supports_n_heavy_ratio():
    dataset = MultitaskTrainingDataset(
        preference_records=[_y_sample("u1"), _y_sample("u2"), _y_sample("u3")],
        next_item_records=[
            _n_sample("u1"),
            _n_sample("u2"),
            _n_sample("u3"),
            _n_sample("u4"),
            _n_sample("u5"),
        ],
        tokenizer=FakeTokenizer(),
        movie_lookup=_movie_lookup(),
        max_seq_length=512,
        use_chat_format=False,
        task_ratio_y=1,
        task_ratio_n=2,
    )

    assert [dataset[index]["task"] for index in range(len(dataset))] == [
        "Y",
        "N",
        "N",
        "Y",
        "N",
        "N",
    ]
    assert dataset.task_counts == {"Y": 2, "N": 4}
    assert dataset.task_ratio == {"Y": 1, "N": 2}


def test_multitask_dataset_rejects_invalid_ratio():
    try:
        MultitaskTrainingDataset(
            preference_records=[_y_sample("u1")],
            next_item_records=[_n_sample("u1")],
            tokenizer=FakeTokenizer(),
            movie_lookup=_movie_lookup(),
            max_seq_length=512,
            use_chat_format=False,
            task_ratio_y=0,
            task_ratio_n=1,
        )
    except ValueError as exc:
        assert "正整数" in str(exc)
    else:
        raise AssertionError("非法 M 任务比例应触发 ValueError")


def test_count_ratio_examples_reports_actual_encoded_counts():
    assert count_ratio_examples(
        y_count=200000,
        n_count=200000,
        task_ratio_y=2,
        task_ratio_n=1,
    ) == {
        "cycle_count": 100000,
        "Y": 200000,
        "N": 100000,
        "total": 300000,
    }


def test_multitask_summary_counts_tasks_and_supervised_tokens():
    dataset = MultitaskTrainingDataset(
        preference_records=[_y_sample("u1")],
        next_item_records=[_n_sample("u1")],
        tokenizer=FakeTokenizer(),
        movie_lookup=_movie_lookup(),
        max_seq_length=512,
        use_chat_format=False,
    )
    summary = summarize_multitask_examples(dataset.examples)

    assert summary["examples"] == 2
    assert summary["task_counts"] == {"Y": 1, "N": 1}
    assert summary["min_supervised_tokens"] > 0
    assert any(label != IGNORE_INDEX for label in dataset[0]["labels"])
    assert any(label != IGNORE_INDEX for label in dataset[1]["labels"])


def test_m_config_inherits_experiment_contract():
    config = load_training_config("configs/m.yaml")

    assert config["variant"] == "m_k0"
    assert config["tasks"]["m"]["task"] == "y_plus_n_multitask"
    assert config["model"]["base_model"]["name_or_path"]
    assert config["_repo_root"].name == "llamarec"


def test_resolve_task_ratio_uses_config_and_cli_override():
    class Args:
        task_ratio_y = None
        task_ratio_n = None

    assert _resolve_task_ratio(Args(), {"optimizer_step_ratio": {"y": 1, "n": 1}}) == {
        "y": 1,
        "n": 1,
    }

    Args.task_ratio_y = 2
    Args.task_ratio_n = 1
    assert _resolve_task_ratio(Args(), {"optimizer_step_ratio": {"y": 1, "n": 1}}) == {
        "y": 2,
        "n": 1,
    }


def test_train_sampler_dataset_compatibility():
    passed_dataset = object()
    fallback_dataset = object()

    assert _select_train_sampler_dataset(passed_dataset, fallback_dataset) is passed_dataset
    assert _select_train_sampler_dataset(None, fallback_dataset) is fallback_dataset


def test_per_task_validation_only_runs_for_default_mixed_eval():
    assert _should_run_per_task_validation(None, "eval") is True
    assert _should_run_per_task_validation(object(), "eval") is False
    assert _should_run_per_task_validation(None, "eval_y") is False
