"""Amazon Reviews 2023 adapter tests."""

from pathlib import Path

import pytest

from src.data.preprocess import iter_ratings


def test_amazon_reviews_csv_is_standardized_and_drops_missing_titles(tmp_path, monkeypatch):
    raw_dir = tmp_path / "data" / "raw" / "amazon_reviews_2023" / "musical_instruments"
    interactions_dir = raw_dir / "interactions"
    metadata_dir = raw_dir / "metadata"
    interactions_dir.mkdir(parents=True)
    metadata_dir.mkdir(parents=True)
    (interactions_dir / "Musical_Instruments.csv").write_text(
        "user_id,parent_asin,rating,timestamp\n"
        "u1,B00A,5.0,1415286067000\n"
        "u1,B00B,3.0,1418071619\n"
        "u2,B00MISSING,4.0,1419869174000\n",
        encoding="utf-8",
    )

    import src.data.preprocess as preprocess

    monkeypatch.setattr(
        preprocess,
        "_read_amazon_reviews_2023_metadata",
        lambda path: {
            "B00A": {"movie_id": "B00A", "parent_asin": "B00A", "title": "Book A"},
            "B00B": {"movie_id": "B00B", "parent_asin": "B00B", "title": "Book B"},
        },
    )

    rows = list(iter_ratings("amazon-musical-instruments", _config(tmp_path)))

    assert rows == [
        {
            "user_id": "u1",
            "movie_id": "B00A",
            "parent_asin": "B00A",
            "rating": 5.0,
            "timestamp": 1415286067,
            "title": "Book A",
        },
        {
            "user_id": "u1",
            "movie_id": "B00B",
            "parent_asin": "B00B",
            "rating": 3.0,
            "timestamp": 1418071619,
            "title": "Book B",
        },
    ]


def test_amazon_metadata_reader_reports_missing_parquet_engine(tmp_path, monkeypatch):
    metadata_dir = tmp_path / "metadata"
    metadata_dir.mkdir()
    (metadata_dir / "full-00000-of-00001.parquet").write_bytes(b"not parquet")

    import src.data.preprocess as preprocess

    class BrokenPandas:
        @staticmethod
        def read_parquet(*args, **kwargs):
            raise ImportError("missing parquet engine")

    monkeypatch.setitem(__import__("sys").modules, "pandas", BrokenPandas)

    with pytest.raises(RuntimeError, match="pyarrow"):
        preprocess._read_amazon_reviews_2023_metadata(metadata_dir)


def _config(repo_root: Path):
    return {
        "_repo_root": repo_root,
        "paths": {"processed_root": "data/processed"},
        "raw_files": {
            "amazon-musical-instruments": {
                "ratings": (
                    "data/raw/amazon_reviews_2023/musical_instruments/"
                    "interactions/Musical_Instruments.csv"
                ),
                "movies": "data/raw/amazon_reviews_2023/musical_instruments/metadata",
                "ratings_format": "amazon_reviews_2023_csv",
                "movies_format": "amazon_reviews_2023_parquet_metadata",
            }
        },
    }
