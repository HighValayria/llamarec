import json
from pathlib import Path

from src.analysis.baseline_llm_comparison import run_baseline_llm_comparison


def test_baseline_llm_comparison_writes_table_and_deltas(tmp_path):
    _write_config(tmp_path)
    baseline_path = tmp_path / "baseline_summary.json"
    phase2c_path = tmp_path / "phase2c_summary.json"
    _write_json(
        baseline_path,
        {
            "baseline_metrics": [
                _baseline_row("Popularity N-train canonical k5", 0.6, 0.8, 0.7),
                _baseline_row("Popularity N-train popmatch k5", 0.3, 0.6, 0.5),
                _baseline_row("Popularity preference-train popmatch k5", 0.1, 0.5, 0.4),
            ]
        },
    )
    _write_json(
        phase2c_path,
        {
            "overall_test_metrics": [
                {"model": "Base", "HR@1": 0.32, "NDCG@5": 0.66, "MRR": 0.55},
                {"model": "N-K0", "HR@1": 0.55, "NDCG@5": 0.79, "MRR": 0.72},
                {"model": "M1", "HR@1": 0.52, "NDCG@5": 0.78, "MRR": 0.70},
            ]
        },
    )

    summary = run_baseline_llm_comparison(
        config_path=tmp_path / "configs" / "experiment.yaml",
        dataset_key="toy",
        baseline_summary_json=baseline_path,
        phase2c_summary_json=phase2c_path,
        output_dir=tmp_path / "outputs" / "comparison",
    )

    output_dir = Path(summary["paths"]["json"]).parent
    payload = json.loads((output_dir / "baseline_llm_comparison.json").read_text(encoding="utf-8"))
    report = (output_dir / "baseline_llm_comparison.md").read_text(encoding="utf-8")

    assert summary["rows"] == 6
    assert payload["deltas"][0]["comparison"] == "N-K0 minus Popularity N-train popmatch k5"
    assert payload["deltas"][0]["delta"] == 0.25
    assert "Popmatch rows are the fair comparison point" in report


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


def _baseline_row(label: str, hr_at_1: float, ndcg_at_5: float, mrr: float):
    return {
        "baseline": label,
        "HR@1": hr_at_1,
        "NDCG@5": ndcg_at_5,
        "MRR": mrr,
    }


def _write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload), encoding="utf-8")
