"""STEP 2 测试：确定性数据生成。"""

from random import Random

from src.data.build_next_item import build_next_item_samples
from src.data.split import build_full_sequence_leave_two_out_split


def test_seed_42_reproduces_split():
    full_sequences = _toy_sequences()
    config = _toy_config()

    split_a = build_full_sequence_leave_two_out_split(full_sequences, config)
    split_b = build_full_sequence_leave_two_out_split(full_sequences, config)

    assert split_a == split_b


def test_seed_42_reproduces_training_candidates():
    full_sequences = _toy_sequences()
    config = _toy_config()
    split = build_full_sequence_leave_two_out_split(full_sequences, config)

    samples_a = build_next_item_samples(
        full_sequences,
        split,
        all_movie_ids=list("ABCDEFG"),
        config=config,
        rng=Random(42),
    )
    samples_b = build_next_item_samples(
        full_sequences,
        split,
        all_movie_ids=list("ABCDEFG"),
        config=config,
        rng=Random(42),
    )

    assert samples_a == samples_b


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
