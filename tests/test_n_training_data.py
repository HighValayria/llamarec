"""STEP 6 测试：N-K0 训练数据编码。"""

from src.train.next_item_dataset import NextItemTrainingDataset, encode_next_item_record
from src.train.preference_dataset import IGNORE_INDEX, summarize_encoded_examples
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


def _sample(label="C"):
    label_set = ["A", "B", "C", "D", "E"]
    ground_truth_index = label_set.index(label) if label in label_set else 2
    return {
        "task": "N",
        "user_id": "u1",
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
        "ground_truth_index": ground_truth_index,
        "label": label,
        "label_set": label_set,
    }


def test_next_item_record_masks_prompt_tokens():
    encoded = encode_next_item_record(
        record=_sample("C"),
        tokenizer=FakeTokenizer(),
        movie_lookup=_movie_lookup(),
        max_seq_length=512,
        use_chat_format=False,
    )

    supervised_positions = [
        index
        for index, label_id in enumerate(encoded["labels"])
        if label_id != IGNORE_INDEX
    ]

    assert supervised_positions
    assert all(
        encoded["labels"][index] == encoded["input_ids"][index]
        for index in supervised_positions
    )
    assert all(
        label_id == IGNORE_INDEX
        for label_id in encoded["labels"][:supervised_positions[0]]
    )


def test_next_item_dataset_rejects_invalid_label():
    try:
        NextItemTrainingDataset(
            records=[_sample("Z")],
            tokenizer=FakeTokenizer(),
            movie_lookup=_movie_lookup(),
            max_seq_length=512,
            use_chat_format=False,
        )
    except ValueError as exc:
        assert "label_set" in str(exc)
    else:
        raise AssertionError("非法 N 标签应当失败")


def test_next_item_dataset_summary_counts_supervised_tokens():
    dataset = NextItemTrainingDataset(
        records=[_sample("A"), _sample("E")],
        tokenizer=FakeTokenizer(),
        movie_lookup=_movie_lookup(),
        max_seq_length=512,
        use_chat_format=False,
    )
    summary = summarize_encoded_examples(dataset.examples)

    assert summary["examples"] == 2
    assert summary["min_supervised_tokens"] > 0
    assert summary["max_length"] >= summary["min_length"]


def test_n_config_inherits_experiment_contract():
    config = load_training_config("configs/n.yaml")

    assert config["variant"] == "n_k0"
    assert config["tasks"]["n"]["task"] == "full_sequence_next_item_prediction"
    assert config["model"]["base_model"]["name_or_path"]
    assert config["_repo_root"].name == "llamarec"
