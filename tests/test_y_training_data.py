"""STEP 5 测试：Y-K0 训练数据编码。"""

from src.train.preference_dataset import (
    IGNORE_INDEX,
    PreferenceTrainingDataset,
    encode_preference_record,
    summarize_encoded_examples,
)
from src.train.train_y import _normalize_token_ids, load_training_config


class FakeTokenizer:
    pad_token_id = 0
    eos_token_id = 2

    def encode(self, text, add_special_tokens=True):
        prefix = [101] if add_special_tokens else []
        return prefix + [(ord(char) % 89) + 10 for char in text]


class FakeEncoding:
    input_ids = [41, 42, 43]


def _sample(label="Yes"):
    return {
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
            "movie_id": "2",
            "title": "Target Movie",
            "rating": 4.0 if label == "Yes" else 2.0,
            "timestamp": 2,
        },
        "label": label,
    }


def test_preference_record_masks_prompt_tokens():
    encoded = encode_preference_record(
        record=_sample("Yes"),
        tokenizer=FakeTokenizer(),
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


def test_preference_dataset_rejects_invalid_label():
    try:
        PreferenceTrainingDataset(
            records=[_sample("Maybe")],
            tokenizer=FakeTokenizer(),
            max_seq_length=512,
            use_chat_format=False,
        )
    except ValueError as exc:
        assert "Yes/No" in str(exc)
    else:
        raise AssertionError("非法 Y 标签应当失败")


def test_preference_dataset_summary_counts_supervised_tokens():
    dataset = PreferenceTrainingDataset(
        records=[_sample("Yes"), _sample("No")],
        tokenizer=FakeTokenizer(),
        max_seq_length=512,
        use_chat_format=False,
    )
    summary = summarize_encoded_examples(dataset.examples)

    assert summary["examples"] == 2
    assert summary["min_supervised_tokens"] > 0
    assert summary["max_length"] >= summary["min_length"]


def test_y_config_inherits_experiment_contract():
    config = load_training_config("configs/y.yaml")

    assert config["variant"] == "y_k0"
    assert config["tasks"]["y"]["task"] == "yes_no_preference_prediction"
    assert config["model"]["base_model"]["name_or_path"]
    assert config["_repo_root"].name == "llamarec"


def test_y_reload_token_ids_accept_dict_return():
    token_ids = _normalize_token_ids(FakeTokenizer(), {"input_ids": [31, 32, 33]})

    assert token_ids == [31, 32, 33]


def test_y_reload_token_ids_accept_input_ids_attribute():
    token_ids = _normalize_token_ids(FakeTokenizer(), FakeEncoding())

    assert token_ids == [41, 42, 43]


def test_y_reload_token_ids_accept_single_batched_return():
    token_ids = _normalize_token_ids(FakeTokenizer(), [[51, 52, 53]])

    assert token_ids == [51, 52, 53]
