import csv
import json
from pathlib import Path

from src.analysis.baseline_result_summary import run_baseline_result_summary


def test_baseline_result_summary_writes_metrics_and_deltas(tmp_path):
    _write_config(tmp_path)
    input_dir = tmp_path / "outputs" / "baselines" / "toy"
    _write_metrics(input_dir / "popularity_canonical_k5" / "test_metrics.json", 0.6, 0.8, 0.7)
    _write_metrics(input_dir / "popularity_k5_popmatch_seed42" / "test_metrics.json", 0.3, 0.6, 0.5)
    _write_metrics(input_dir / "popularity_preftrain_canonical_k5" / "test_metrics.json", 0.5, 0.7, 0.6)
    _write_metrics(input_dir / "popularity_preftrain_k5_popmatch_seed42" / "test_metrics.json", 0.1, 0.4, 0.3)

    summary = run_baseline_result_summary(
        config_path=tmp_path / "configs" / "experiment.yaml",
        dataset_key="toy",
    )

    output_dir = Path(summary["paths"]["csv"]).parent
    rows = list(csv.DictReader((output_dir / "baseline_ranking_summary.csv").open()))
    payload = json.loads(
        (output_dir / "baseline_ranking_summary.json").read_text(encoding="utf-8")
    )
    report = (output_dir / "baseline_ranking_summary.md").read_text(encoding="utf-8")

    assert summary["rows"] == 4
    assert rows[0]["baseline"] == "Popularity N-train canonical k5"
    assert payload["condition_deltas"][0]["delta"] == -0.3
    assert len(payload["condition_deltas"]) == 6
    assert "popularity shortcut" in report


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
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {
                "ranking": {
                    "HR@1": hr_at_1,
                    "NDCG@5": ndcg_at_5,
                    "MRR": mrr,
                    "HR@5": 1.0,
                    "samples": 2,
                },
                "ranking_scoring": "n_train_target_popularity",
            }
        ),
        encoding="utf-8",
    )
