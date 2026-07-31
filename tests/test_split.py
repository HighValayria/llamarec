"""STEP 2 测试：timestamp bucket 时间划分。"""

from src.data.split import (
    build_full_sequence_leave_two_out_split,
    validate_split_no_leakage,
)


def test_timestamp_tie_does_not_remove_user_from_y_split():
    full_sequences = _toy_sequences()

    split = build_full_sequence_leave_two_out_split(
        full_sequences,
        _toy_config(),
        dataset_key="toy",
    )

    assert "u1" in split["y"]["users"]
    assert split["timestamp_tie_policy"]["skip_entire_user_on_tie"] is False
    assert split["y"]["users"]["u1"]["validation_bucket_timestamp"] == 4
    assert split["y"]["users"]["u1"]["test_bucket_timestamp"] == 5
    validate_split_no_leakage(split, full_sequences)


def test_n_skips_ambiguous_sample_not_entire_user():
    full_sequences = _toy_sequences()

    split = build_full_sequence_leave_two_out_split(
        full_sequences,
        _toy_config(),
        dataset_key="toy",
    )

    n_info = split["n"]["users"]["u1"]
    assert n_info["legal_sample_count"] == 3
    assert n_info["ambiguous_next_bucket_count"] == 1
    assert n_info["validation_target"]["movie_id"] == "E"
    assert n_info["test_target"]["movie_id"] == "F"


def _toy_config():
    return {
        "dataset": {"history_length": 10, "positive_rating_threshold": 4},
        "split": {"minimum_legal_next_item_samples_for_n": 2},
    }


def _toy_sequences():
    # t=2 有两个 interaction。Y 会保留它们；N 会跳过以该 bucket 为 target 的样本。
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
