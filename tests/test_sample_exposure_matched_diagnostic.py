import csv
import json
from pathlib import Path

from src.analysis.sample_exposure_matched_diagnostic import (
    run_sample_exposure_matched_diagnostic,
)


def test_sample_exposure_matched_diagnostic_writes_gap(tmp_path):
    _write_config(tmp_path)
    root = tmp_path / "outputs"
    _write_metrics(root / "n_metrics.json", 0.55, 0.78, 0.72)
    _write_json(root / "n_summary.json", {"training_stop": "max_steps"})
    _write_metrics(root / "sasrec_metrics.json", 0.58, 0.80, 0.74)
    _write_json(root / "sasrec_summary.json", {"training_stop": "max_steps"})

    summary = run_sample_exposure_matched_diagnostic(
        config_path=tmp_path / "configs" / "experiment.yaml",
        dataset_key="toy",
        output_dir=tmp_path / "outputs" / "fair_budget",
        runs={
            "N-K0": {
                "metrics": root / "n_metrics.json",
                "run_summary": root / "n_summary.json",
                "n_exposure": 12000,
                "optimizer_steps": 1500,
                "effective_batch": 8,
                "role": "primary_llm",
            },
            "SASRec-exp-match": {
                "metrics": root / "sasrec_metrics.json",
                "run_summary": root / "sasrec_summary.json",
                "n_exposure": 11776,
                "optimizer_steps": 23,
                "effective_batch": 512,
                "role": "primary_sasrec",
            },
        },
    )

    output_dir = Path(summary["paths"]["csv"]).parent
    rows = list(csv.DictReader((output_dir / "sample_exposure_matched_diagnostic.csv").open()))
    payload = json.loads(
        (output_dir / "sample_exposure_matched_diagnostic.json").read_text(encoding="utf-8")
    )

    assert summary["missing_rows"] == 0
    assert rows[1]["relative mismatch %"] == "-1.8666666667"
    assert payload["gaps"][0]["delta_HR@1"] == 0.03
    assert payload["answers"]["sasrec_greater_than_n_k0_after_exposure_match"].startswith("yes")


def test_sample_exposure_matched_diagnostic_marks_missing_metrics(tmp_path):
    _write_config(tmp_path)

    summary = run_sample_exposure_matched_diagnostic(
        config_path=tmp_path / "configs" / "experiment.yaml",
        dataset_key="toy",
        output_dir=tmp_path / "outputs" / "fair_budget",
        runs={
            "SASRec-exp-match": {
                "metrics": tmp_path / "missing.json",
                "run_summary": tmp_path / "missing_summary.json",
                "n_exposure": 11776,
                "optimizer_steps": 23,
                "effective_batch": 512,
            }
        },
    )

    rows = list(csv.DictReader(Path(summary["paths"]["csv"]).open()))
    report = Path(summary["paths"]["markdown"]).read_text(encoding="utf-8")

    assert summary["missing_rows"] == 1
    assert rows[0]["evidence_status"] == "missing_metrics_file"
    assert rows[0]["HR@1"] == "unavailable"
    assert "roughly N-sample-exposure-matched diagnostic" in report


def _write_config(root: Path) -> None:
    config_dir = root / "configs"
    config_dir.mkdir(parents=True)
    (config_dir / "experiment.yaml").write_text(
        "\n".join(
            [
                "dataset:",
                "  formal: toy",
            ]
        ),
        encoding="utf-8",
    )


def _write_metrics(path: Path, hr_at_1: float, ndcg_at_5: float, mrr: float) -> None:
    _write_json(
        path,
        {
            "ranking": {
                "HR@1": hr_at_1,
                "NDCG@5": ndcg_at_5,
                "MRR": mrr,
                "samples": 2,
            }
        },
    )


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload), encoding="utf-8")
