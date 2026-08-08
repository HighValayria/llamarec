"""STEP 3 测试：固定候选集生成。"""

from random import Random

from src.eval.candidate_sets import (
    _build_candidate_records,
    spreadsheet_labels,
    validate_candidate_record,
)


def test_candidate_record_contains_ground_truth_once():
    records = _toy_candidate_records(seed=42)

    for record in records:
        validate_candidate_record(record, candidate_num=5)
        assert record["candidate_movie_ids"].count(record["ground_truth_movie_id"]) == 1


def test_candidate_generation_is_reproducible_with_same_seed():
    assert _toy_candidate_records(seed=42) == _toy_candidate_records(seed=42)


def test_ground_truth_position_is_not_forced_to_zero():
    records = _toy_candidate_records(seed=42)
    positions = {record["ground_truth_index"] for record in records}

    assert positions != {0}


def test_spreadsheet_labels_support_large_candidate_sets():
    labels = spreadsheet_labels(28)

    assert labels[:5] == ["A", "B", "C", "D", "E"]
    assert labels[25:] == ["Z", "AA", "AB"]


def test_candidate_records_support_twenty_candidate_variant():
    config = _toy_config()
    config["candidates"]["candidate_num"] = 20
    config["candidates"]["label_set"] = spreadsheet_labels(20)
    config["candidates"]["variant_name"] = "k20_seed42"
    records = _build_candidate_records(
        source_samples=[_sample("u1", "B", 2)],
        all_movie_ids=[str(index) for index in range(30)] + ["B"],
        config=config,
        dataset_key="toy",
        split_name="validation",
        rng=Random(42),
    )

    record = records[0]
    validate_candidate_record(record, candidate_num=20)
    assert len(record["label_set"]) == 20
    assert record["candidate_generation"]["variant_name"] == "k20_seed42"
    assert record["candidate_generation"]["candidate_num"] == 20


def _toy_candidate_records(seed):
    source_samples = [
        _sample("u1", "B", 2),
        _sample("u2", "C", 3),
        _sample("u3", "D", 4),
        _sample("u4", "E", 5),
    ]
    return _build_candidate_records(
        source_samples=source_samples,
        all_movie_ids=list("ABCDEFGH"),
        config=_toy_config(),
        dataset_key="toy",
        split_name="validation",
        rng=Random(seed),
    )


def _sample(user_id, movie_id, timestamp):
    return {
        "user_id": user_id,
        "history": [
            {
                "movie_id": "A",
                "title": "Movie A",
                "rating": 5.0,
                "timestamp": 1,
                "sequence_index": 0,
            }
        ],
        "target": {
            "movie_id": movie_id,
            "title": f"Movie {movie_id}",
            "rating": 3.0,
            "timestamp": timestamp,
            "sequence_index": timestamp,
        },
        "ground_truth_movie_id": movie_id,
    }


def _toy_config():
    return {
        "seed": {"random_seed": 42},
        "negative_sampling": {
            "method": "random",
            "pool": "all_movies_minus_current_ground_truth_item",
        },
        "candidates": {
            "candidate_num": 5,
            "label_set": ["A", "B", "C", "D", "E"],
            "shuffle_order": True,
        },
    }
