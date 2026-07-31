"""STEP 2 测试：Y/N 样本历史无泄漏。"""

from random import Random

from src.data.build_preference import (
    build_preference_samples,
    validate_preference_sample,
)
from src.data.build_next_item import (
    build_next_item_samples,
    validate_next_item_sample,
)
from src.data.split import build_full_sequence_leave_two_out_split


def test_y_history_uses_strictly_earlier_timestamps():
    full_sequences = _toy_sequences()
    split = build_full_sequence_leave_two_out_split(full_sequences, _toy_config())

    samples = build_preference_samples(full_sequences, split, _toy_config())

    tied_train_samples = [
        sample
        for sample in samples
        if sample["split"] == "train" and sample["target"]["timestamp"] == 2
    ]
    assert len(tied_train_samples) == 2
    for sample in tied_train_samples:
        validate_preference_sample(sample, positive_rating_threshold=4)
        assert [item["movie_id"] for item in sample["history"]] == ["A"]


def test_n_history_and_candidates_are_valid_for_all_splits():
    full_sequences = _toy_sequences()
    split = build_full_sequence_leave_two_out_split(full_sequences, _toy_config())

    samples = build_next_item_samples(
        full_sequences,
        split,
        all_movie_ids=list("ABCDEFG"),
        config=_toy_config(),
        rng=Random(42),
    )

    assert {sample["split"] for sample in samples} == {"train", "validation", "test"}
    for sample in samples:
        validate_next_item_sample(sample, candidate_num=5)
        assert max(item["timestamp"] for item in sample["history"]) < sample["target"][
            "timestamp"
        ]


def _toy_config():
    return {
        "dataset": {"history_length": 10, "positive_rating_threshold": 4},
        "candidates": {
            "candidate_num": 5,
            "label_set": ["A", "B", "C", "D", "E"],
            "shuffle_order": True,
        },
        "split": {"minimum_legal_next_item_samples_for_n": 2},
    }


def _toy_sequences():
    return {
        "u1": [
            _interaction("A", 5, 1, 0),
            _interaction("B", 2, 2, 1),
            _interaction("C", 4, 2, 2),
            _interaction("D", 1, 3, 3),
            _interaction("E", 5, 4, 4),
            _interaction("F", 3, 5, 5),
        ]
    }


def _interaction(movie_id, rating, timestamp, sequence_index):
    return {
        "user_id": "u1",
        "movie_id": movie_id,
        "title": f"Movie {movie_id}",
        "rating": float(rating),
        "timestamp": timestamp,
        "sequence_index": sequence_index,
    }
