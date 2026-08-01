"""STEP 7 测试：M-K0 多任务训练数据编码。"""

from src.train.multitask_dataset import (
    MultitaskTrainingDataset,
    summarize_multitask_examples,
)
from src.train.preference_dataset import IGNORE_INDEX
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
