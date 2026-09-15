import csv
import importlib.util
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / "paper/plan/task-packets/m1_clean_subset_recovered_analysis.py"


def load_module():
    spec = importlib.util.spec_from_file_location("clean_recovered", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def frozen_metrics():
    path = ROOT / "paper/evidence/ms96_raw_metrics.csv"
    output = {}
    with path.open(encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            if (
                int(row["training_seed"]) in (43, 44)
                and row["interface"] == "N"
                and row["model"] in ("N96", "M1-96")
                and row["protocol"] in ("k5", "k20_seed42", "k50_seed42")
                and row["metric"] in ("HR@1", "NDCG@5", "MRR")
            ):
                output[
                    (
                        int(row["training_seed"]),
                        row["split"],
                        row["model"],
                        row["protocol"],
                        row["metric"],
                    )
                ] = float(row["value"])
    return output


def aggregate(module, path):
    totals = defaultdict(float)
    rows = module.load_jsonl(path)
    for record in rows:
        values = module.metric_values(module.rank(record))
        for metric, value in values.items():
            totals[metric] += value
    return {metric: total / len(rows) for metric, total in totals.items()}


def test_recovered_full_metrics_match_frozen_summaries():
    module = load_module()
    expected = frozen_metrics()
    assert len(expected) == 72
    protocols = {"k5": "k5", "k20": "k20_seed42", "k50": "k50_seed42"}
    for (seed, variant, split), (n_path, m_path) in module.prediction_paths().items():
        if seed not in (43, 44):
            continue
        frozen_split = "validation" if split == "valid" else "test"
        for model, path in (("N96", n_path), ("M1-96", m_path)):
            actual = aggregate(module, path)
            for metric, value in actual.items():
                key = (seed, frozen_split, model, protocols[variant], metric)
                assert abs(value - expected[key]) < 1e-12


def test_clean_outputs_cover_expected_pairs_and_keep_positive_direction():
    module = load_module()
    summary = module.json.loads(module.OUTPUT_JSON.read_text(encoding="utf-8"))
    assert summary["pair_count"] == 14
    assert summary["source_file_count"] == 28
    assert summary["training"] is False
    assert summary["inference"] is False
    assert summary["bootstrap"] is False
    assert {row["rows_clean"] for row in summary["per_seed_results"] if row["seed"] == 42} == {5494, 5600}
    assert {row["rows_clean"] for row in summary["per_seed_results"] if row["seed"] in (43, 44)} == {5318, 5535}
    deltas = [
        values["delta_N_minus_M1"]
        for row in summary["per_seed_results"]
        for values in row["metrics"].values()
    ]
    assert len(deltas) == 42
    assert all(delta > 0 for delta in deltas)
