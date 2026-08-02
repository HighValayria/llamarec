"""STEP 2 测试：MovieLens-1M 原始格式读取。"""

from pathlib import Path

from src.data.preprocess import load_movies, load_ratings


def test_movielens_1m_double_colon_files_are_normalized(tmp_path):
    raw_dir = tmp_path / "data" / "raw" / "ml-1m"
    raw_dir.mkdir(parents=True)
    (raw_dir / "ratings.dat").write_text(
        "1::1193::5::978300760\n"
        "1::661::3::978302109\n",
        encoding="latin-1",
    )
    (raw_dir / "movies.dat").write_text(
        "1193::One Flew Over the Cuckoo's Nest (1975)::Drama\n"
        "661::James and the Giant Peach (1996)::Animation|Children's|Musical\n",
        encoding="latin-1",
    )

    config = _config(tmp_path)

    movies = load_movies("movielens-1m", config)
    ratings = load_ratings("movielens-1m", config)

    assert movies["1193"]["title"] == "One Flew Over the Cuckoo's Nest (1975)"
    assert movies["661"]["genres"] == "Animation|Children's|Musical"
    assert ratings == [
        {
            "user_id": "1",
            "movie_id": "1193",
            "rating": 5.0,
            "timestamp": 978300760,
            "title": "One Flew Over the Cuckoo's Nest (1975)",
        },
        {
            "user_id": "1",
            "movie_id": "661",
            "rating": 3.0,
            "timestamp": 978302109,
            "title": "James and the Giant Peach (1996)",
        },
    ]


def _config(repo_root: Path):
    return {
        "_repo_root": repo_root,
        "paths": {"processed_root": "data/processed"},
        "raw_files": {
            "movielens-1m": {
                "ratings": "data/raw/ml-1m/ratings.dat",
                "movies": "data/raw/ml-1m/movies.dat",
                "ratings_format": "double_colon_no_header",
                "movies_format": "double_colon_movies_dat",
            }
        },
    }
