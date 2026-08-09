import json
from pathlib import Path

from src.baselines.bpr_mf import run_bpr_mf_baseline


def test_bpr_mf_baseline_writes_predictions_metrics_and_model(tmp_path):
    _write_config(tmp_path)
    _write_jsonl(
        tmp_path / "data" / "processed" / "toy" / "next_item_train.jsonl",
        [
            _train_sample("u1", "a"),
            _train_sample("u1", "a"),
            _train_sample("u2", "b"),
            _train_sample("u2", "b"),
        ],
    )
    _write_jsonl(
        tmp_path / "data" / "candidates" / "toy" / "test.jsonl",
        [
            _candidate_sample("u1", ["a", "b"], "a", 0),
            _candidate_sample("u2", ["a", "b"], "b", 1),
        ],
    )

    summary = run_bpr_mf_baseline(
        config_path=tmp_path / "configs" / "experiment.yaml",
        dataset_key="toy",
        splits=["test"],
        output_dir=tmp_path / "outputs" / "bpr_mf",
        embedding_dim=8,
        epochs=1,
        batch_size=2,
        seed=7,
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
    run_summary = json.loads((output_dir / "run_summary.json").read_text(encoding="utf-8"))

    assert len(predictions) == 2
    assert predictions[0]["model"] == "bpr_mf"
    assert len(predictions[0]["scores"]) == 2
    assert metrics["ranking"]["samples"] == 2
    assert metrics["ranking_scoring"] == "bpr_mf_dot_product"
    assert run_summary["train_pairs"] == 4
    assert len(run_summary["epoch_losses"]) == 1
    assert (output_dir / "model.pt").exists()
    assert (output_dir / "mappings.json").exists()


def test_bpr_mf_baseline_accepts_candidate_file_overrides(tmp_path):
    _write_config(tmp_path)
    _write_jsonl(
        tmp_path / "data" / "processed" / "toy" / "next_item_train.jsonl",
        [_train_sample("u1", "a"), _train_sample("u1", "a")],
    )
    override_path = tmp_path / "custom" / "test_candidates.jsonl"
    _write_jsonl(
        override_path,
        [_candidate_sample("u1", ["a", "z"], "a", 0)],
    )

    summary = run_bpr_mf_baseline(
        config_path=tmp_path / "configs" / "experiment.yaml",
        dataset_key="toy",
        splits=["test"],
        candidate_files={"test": override_path},
        output_dir=tmp_path / "outputs" / "override",
        epochs=0,
        seed=11,
    )

    assert summary["candidate_files"]["test"] == str(override_path)
    assert summary["counts"]["test"]["n_predictions"] == 1


def _write_config(root: Path) -> None:
    config_dir = root / "configs"
    config_dir.mkdir(parents=True)
    (config_dir / "experiment.yaml").write_text(
        "\n".join(
            [
                "dataset:",
                "  formal: toy",
                "seed:",
                "  random_seed: 42",
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


def _train_sample(user_id: str, movie_id: str):
    return {
        "task": "N",
        "split": "train",
        "user_id": user_id,
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
