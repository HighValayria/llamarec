import json
from pathlib import Path

from src.baselines.popularity import run_popularity_baseline


def test_popularity_baseline_scores_fixed_candidates_from_n_train_targets(tmp_path):
    _write_config(tmp_path)
    _write_jsonl(
        tmp_path / "data" / "processed" / "toy" / "next_item_train.jsonl",
        [
            _train_sample("popular"),
            _train_sample("popular"),
            _train_sample("other"),
            _train_sample("other"),
            _train_sample("other"),
        ],
    )
    _write_jsonl(
        tmp_path / "data" / "candidates" / "toy" / "test.jsonl",
        [
            _candidate_sample("u1", ["cold", "popular", "target"], "target", 2),
            _candidate_sample("u2", ["other", "cold", "popular"], "other", 0),
        ],
    )

    summary = run_popularity_baseline(
        config_path=tmp_path / "configs" / "experiment.yaml",
        dataset_key="toy",
        splits=["test"],
        output_dir=tmp_path / "outputs" / "baselines" / "toy" / "popularity",
    )

    output_dir = Path(summary["outputs_dir"])
    metrics = json.loads((output_dir / "test_metrics.json").read_text(encoding="utf-8"))
    predictions = [
        json.loads(line)
        for line in (output_dir / "n_test_predictions.jsonl").read_text(
            encoding="utf-8"
        ).splitlines()
        if line.strip()
    ]

    assert predictions[0]["scores"] == [0.0, 2.0, 0.0]
    assert predictions[0]["predicted_label"] == "B"
    assert predictions[1]["scores"] == [3.0, 0.0, 2.0]
    assert metrics["ranking"]["samples"] == 2
    assert metrics["ranking"]["HR@1"] == 0.5
    assert metrics["ranking"]["MRR"] == (1 / 3 + 1) / 2
    assert (output_dir / "run_summary.json").exists()


def test_popularity_baseline_accepts_candidate_file_overrides(tmp_path):
    _write_config(tmp_path)
    _write_jsonl(
        tmp_path / "data" / "processed" / "toy" / "next_item_train.jsonl",
        [_train_sample("target")],
    )
    override_path = tmp_path / "custom" / "test_candidates.jsonl"
    _write_jsonl(
        override_path,
        [_candidate_sample("u1", ["cold", "target"], "target", 1)],
    )

    summary = run_popularity_baseline(
        config_path=tmp_path / "configs" / "experiment.yaml",
        dataset_key="toy",
        splits=["test"],
        candidate_files={"test": override_path},
        output_dir=tmp_path / "outputs" / "baseline_override",
    )

    assert summary["candidate_files"]["test"] == str(override_path)
    assert summary["metrics"]["test"]["ranking"]["HR@1"] == 1.0


def _write_config(root: Path) -> None:
    config_dir = root / "configs"
    config_dir.mkdir(parents=True)
    (config_dir / "experiment.yaml").write_text(
        "\n".join(
            [
                "dataset:",
                "  formal: toy",
                "processed_outputs:",
                "  next_item_samples:",
                "    train: data/processed/{dataset}/next_item_train.jsonl",
                "candidates:",
                "  save_files:",
                "    validation: data/candidates/{dataset}/valid.jsonl",
                "    test: data/candidates/{dataset}/test.jsonl",
            ]
        ),
        encoding="utf-8",
    )


def _train_sample(movie_id: str):
    return {
        "task": "N",
        "split": "train",
        "target": {"movie_id": movie_id},
        "ground_truth_movie_id": movie_id,
    }


def _candidate_sample(
    user_id: str,
    candidate_movie_ids: list[str],
    ground_truth_movie_id: str,
    ground_truth_index: int,
):
    return {
        "task": "N",
        "split": "test",
        "user_id": user_id,
        "candidate_movie_ids": candidate_movie_ids,
        "ground_truth_movie_id": ground_truth_movie_id,
        "ground_truth_index": ground_truth_index,
        "label": chr(ord("A") + ground_truth_index),
        "label_set": [chr(ord("A") + index) for index in range(len(candidate_movie_ids))],
    }


def _write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "\n".join(json.dumps(row) for row in rows) + "\n",
        encoding="utf-8",
    )
