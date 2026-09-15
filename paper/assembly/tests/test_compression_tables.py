from __future__ import annotations

import csv
import importlib.util
import json
from pathlib import Path
import unittest


REPO = Path(__file__).resolve().parents[3]
DERIVED = REPO / "paper" / "tables" / "compression_2026-09-10"
spec = importlib.util.spec_from_file_location("build_compact_tables", DERIVED / "build_compact_tables.py")
compact = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(compact)


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


class CompressionTableTests(unittest.TestCase):
    def test_generated_outputs_are_byte_reproducible(self):
        expected, _ = compact.build()
        for name, data in expected.items():
            self.assertEqual((DERIVED / name).read_bytes(), data, name)

    def test_lineage_covers_every_output_cell(self):
        lineage = rows(DERIVED / "lineage.csv")
        self.assertEqual(len(lineage), 449)
        keys = {(r["output_file"], r["output_row"], r["output_column"]) for r in lineage}
        self.assertEqual(len(keys), len(lineage))
        for name in (
            "training_exposure_compact.csv", "supervision_semantics_compact.csv",
            "ms96_delta_summary_compact.csv", "hard_candidate_compact.csv",
        ):
            table = rows(DERIVED / name)
            fields = list(table[0])
            for index in range(1, len(table) + 1):
                for field in fields:
                    self.assertIn((name, str(index), field), keys)

    def test_original_fourteen_csv_files_match_immutable_archive(self):
        manifest = json.loads((REPO / "paper/archive/tables/pre_compression_2026-09-10/manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(len(manifest["tables"]), 14)
        for record in manifest["tables"]:
            self.assertEqual(
                (REPO / record["active_source_path"]).read_bytes(),
                (REPO / record["archive_path"]).read_bytes(),
                record["active_source_path"],
            )

    def test_compact_exposure_and_supervision_contracts(self):
        exposure = rows(DERIVED / "training_exposure_compact.csv")
        self.assertEqual(len(exposure), 9)
        for row in exposure:
            self.assertEqual(int(row["total_exposure"]), int(row["Y_exposure"]) + int(row["N_exposure"]))
            if row["run"].startswith("M1"):
                self.assertEqual(int(row["total_exposure"]), 2 * int(row["Y_exposure"]))
        supervision = rows(DERIVED / "supervision_semantics_compact.csv")
        self.assertEqual((len([r for r in supervision if r["panel"] == "A"]), len([r for r in supervision if r["panel"] == "B"])), (4, 6))
        self.assertEqual({r["metric_1"] for r in supervision if r["panel"] == "A"}, {"AUC"})
        self.assertEqual({r["metric_1"] for r in supervision if r["panel"] == "B"}, {"HR@1"})

    def test_compact_ix_retains_rc01(self):
        table = rows(DERIVED / "ms96_delta_summary_compact.csv")
        self.assertEqual(len(table), 24)
        self.assertEqual({r["split"] for r in table}, {"validation", "test"})
        self.assertEqual({r["protocol"] for r in table}, {"binary", "k5", "k20", "k50"})
        for split in ("validation", "test"):
            binary = [r for r in table if r["split"] == split and r["protocol"] == "binary"]
            self.assertEqual({r["metric"] for r in binary}, {"AUC", "F1", "Accuracy"})
            for protocol in ("k5", "k20", "k50"):
                ranking = [r for r in table if r["split"] == split and r["protocol"] == protocol]
                self.assertEqual({r["metric"] for r in ranking}, {"HR@1", "NDCG@5", "MRR"})
        exception = next(r for r in table if (r["split"], r["protocol"], r["metric"]) == ("validation", "binary", "Accuracy"))
        self.assertEqual(exception["seed_directions_42_43_44"], "+/+/-")
        source = rows(REPO / "paper/tables/ms96_protocol_test.csv")
        lookup = {(r["training_seed"], r["protocol"], "HR@1"): float(r["delta_HR@1"]) for r in source}
        self.assertAlmostEqual(lookup[("43", "k50_seed42", "HR@1")], 0.005110132158590297)
        self.assertAlmostEqual(lookup[("43", "k5", "HR@1")], 0.007753303964757707)

    def test_compact_x_retains_seed42_interval_contract(self):
        table = rows(DERIVED / "hard_candidate_compact.csv")
        self.assertEqual(len(table), 18)
        self.assertEqual({(r["candidate_protocol"], r["split"]) for r in table}, {
            (protocol, split) for protocol in ("k5", "k20", "k50") for split in ("validation", "test")
        })
        for row in table:
            self.assertIn(row["ci_status"], {"POSITIVE", "CROSSES_ZERO", "NEGATIVE", "NA"})
            if row["metric"] == "HR@1":
                self.assertTrue(row["ci95_low"] and row["ci95_high"])
            else:
                self.assertEqual((row["ci95_low"], row["ci95_high"]), ("", ""))
        crossing = [r for r in table if r["candidate_protocol"] == "k5" and r["split"] == "validation"]
        self.assertEqual({r["ci_status"] for r in crossing}, {"CROSSES_ZERO"})


if __name__ == "__main__":
    unittest.main()
