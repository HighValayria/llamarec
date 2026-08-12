import csv
import json
from pathlib import Path

from src.analysis.training_budget_audit import (
    run_training_budget_audit,
    sasrec_processed_instances,
)


def test_sasrec_processed_instances_accounts_for_short_epoch_batch():
    assert sasrec_processed_instances(
        train_examples=200_000,
        batch_size=512,
        optimizer_steps=1500,
    ) == 767_424
    assert sasrec_processed_instances(
        train_examples=200_000,
        batch_size=512,
        optimizer_steps=3000,
    ) == 1_534_656


def test_training_budget_audit_writes_rows_and_answers(tmp_path):
    _write_config(tmp_path)
    processed_dir = tmp_path / "data" / "processed" / "movielens-1m"
    _write_jsonl(processed_dir / "next_item_train.jsonl", 20)
    _write_jsonl(processed_dir / "preference_train.jsonl", 30)

    summary = run_training_budget_audit(
        config_path=tmp_path / "configs" / "experiment.yaml",
    )

    output_dir = Path(summary["paths"]["csv"]).parent
    rows = list(csv.DictReader((output_dir / "training_budget_audit.csv").open()))
    payload = json.loads(
        (output_dir / "training_budget_audit.json").read_text(encoding="utf-8")
    )
    report = (output_dir / "training_budget_audit.md").read_text(encoding="utf-8")

    assert summary["rows"] == 4
    assert rows[0]["model"] == "N-K0"
    assert rows[1]["processed_n_instances"] == "12000"
    assert rows[1]["processed_y_instances"] == "12000"
    assert payload["answers"]["m1_y_n_update_ratio"] == "1:1"
    assert "sample-exposure mismatch" in report


def _write_config(root: Path) -> None:
    config_dir = root / "configs"
    config_dir.mkdir(parents=True)
    (config_dir / "experiment.yaml").write_text(
        "\n".join(
            [
                "dataset:",
                "  formal: movielens-1m",
            ]
        ),
        encoding="utf-8",
    )


def _write_jsonl(path: Path, count: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join("{}\n" for _ in range(count)), encoding="utf-8")
