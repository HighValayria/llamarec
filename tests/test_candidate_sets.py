"""STEP 3 测试：固定候选集生成。"""

from collections import Counter
from random import Random

from src.eval.candidate_sets import (
    _build_candidate_records,
    _permute_candidate_record,
    sample_popularity_matched_negatives,
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


def test_popularity_matched_negatives_prefer_nearest_popularity():
    popularity = Counter(
        {
            "target": 10,
            "near-low": 9,
            "near-same": 10,
            "near-high": 11,
            "far": 100,
        }
    )

    negatives = sample_popularity_matched_negatives(
        ["target", "near-low", "near-same", "near-high", "far"],
        target_movie_id="target",
        n=3,
        rng=Random(42),
        movie_popularity=popularity,
        candidate_pool_multiplier=1,
    )

    assert set(negatives) == {"near-low", "near-same", "near-high"}


def test_candidate_records_support_popularity_matched_variant():
    config = _toy_config()
    config["negative_sampling"]["method"] = "popularity_matched"
    config["candidates"]["variant_name"] = "k5_popmatch_seed42"
    records = _build_candidate_records(
        source_samples=[_sample("u1", "B", 2)],
        all_movie_ids=[str(index) for index in range(50)] + ["A", "B", "C", "D", "E"],
        config=config,
        dataset_key="toy",
        split_name="validation",
        rng=Random(42),
        movie_popularity=Counter({"B": 10, "C": 9, "D": 10, "E": 11, "A": 0}),
    )

    record = records[0]
    validate_candidate_record(record, candidate_num=5)
    assert record["candidate_generation"]["method"] == "popularity_matched"
    assert record["candidate_generation"]["variant_name"] == "k5_popmatch_seed42"
    assert record["candidate_generation"]["target_popularity"] == 10
    assert "negative_popularity_mean" in record["candidate_generation"]


def test_permute_candidate_record_preserves_candidate_ids_and_updates_label(tmp_path):
    record = _toy_candidate_records(seed=42)[0]
    permuted = _permute_candidate_record(
        record,
        rng=Random(7),
        variant_name="k5_perm_seed7",
        seed=108,
        source_path=tmp_path / "valid.jsonl",
    )

    validate_candidate_record(permuted, candidate_num=5)
    assert set(permuted["candidate_movie_ids"]) == set(record["candidate_movie_ids"])
    assert permuted["candidate_movie_ids"] != record["candidate_movie_ids"]
    assert permuted["candidate_generation"]["method"] == "order_permutation"
    assert permuted["candidate_generation"]["variant_name"] == "k5_perm_seed7"
    assert permuted["candidate_generation"]["preserves_candidate_ids"] is True


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
