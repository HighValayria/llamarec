"""MS96 data and scope checks; fixed point estimates only, no model execution."""
import csv
import io
import json
import math
from pathlib import Path
import re
import sys
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "paper/analysis"))
import ms96_evidence as ms96
from paper.assembly.tests.contract_snapshot import assert_current_contract, file_sha256


def rows(path):
    with (ROOT / path).open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


class MS96EvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw = rows("paper/evidence/ms96_raw_metrics.csv")
        cls.deltas = rows("paper/evidence/ms96_per_seed_deltas.csv")
        cls.summary = rows("paper/tables/ms96_delta_summary.csv")
        cls.lookup = {(r["training_seed"], r["split"], r["protocol"], r["metric"]): float(r["delta"])
                      for r in cls.deltas}

    def test_generated_files_match_fixed_sources(self):
        for path, content in ms96.build_outputs().items():
            self.assertEqual((ROOT / path).read_text(encoding="utf-8"), content, path)

    def test_full_native_coverage_without_duplicate_validation(self):
        self.assertEqual(len(self.raw), 144)
        self.assertEqual(len(self.deltas), 72)
        self.assertEqual(len(self.summary), 24)
        self.assertEqual({r["training_seed"] for r in self.raw}, {"42", "43", "44"})
        for seed in ("42", "43", "44"):
            for split in ("validation", "test"):
                subset = [r for r in self.raw if r["training_seed"] == seed and r["split"] == split]
                self.assertEqual(len(subset), 24)
                self.assertFalse(any("bridge" in r["interface"] for r in subset))
        self.assertFalse(any(r["source"].endswith("/summary.txt") for r in self.raw))

    def test_native_sample_counts_and_candidate_seed_are_separate(self):
        for row in self.raw:
            if row["training_seed"] == "42":
                self.assertEqual(row["samples"], "")
            else:
                expected = ("12381" if row["split"] == "validation" else "11544") if row["interface"] == "Y" else "5675"
                self.assertEqual(row["samples"], expected)
            self.assertEqual(row["candidate_seed"], "" if row["interface"] == "Y" else "42")

    def test_new_seed_raw_values_match_tsv_cells(self):
        for seed in ("43", "44"):
            for split in ("validation", "test"):
                filename = "validation_summary.txt" if split == "validation" else "test_summary.txt"
                path = ms96.IMPORTED / f"seed{seed}" / filename
                base, hard = ms96.read_sections(path)
                for source in base + hard:
                    protocol = source.get("variant", "k5")
                    for interface, metrics in (("Y", ms96.BINARY), ("N", ms96.RANKING)):
                        if interface == "Y" and (source["run"] == "N96" or "variant" in source):
                            continue
                        if interface == "N" and source["run"] == "Y96":
                            continue
                        for metric in metrics:
                            found = [r for r in self.raw if (r["training_seed"], r["split"], r["model"], r["interface"], r["protocol"], r["metric"])
                                     == (seed, split, source["run"], interface, "binary" if interface == "Y" else protocol, metric)]
                            self.assertEqual(len(found), 1)
                            self.assertEqual(found[0]["value"], source[metric])

    def test_delta_orientation_and_independent_sample_std(self):
        for row in self.deltas:
            expected = float(row["multitask_value"]) - float(row["specialist_value"])
            if row["protocol"] != "binary":
                expected = -expected
            self.assertEqual(float(row["delta"]), expected)
        for row in self.summary:
            values = [self.lookup[str(seed), row["split"], row["protocol"], row["metric"]]
                      for seed in (42, 43, 44)]
            mean = sum(values) / 3
            sd = math.sqrt(sum((x - mean) ** 2 for x in values) / 2)
            self.assertAlmostEqual(float(row["mean"]), mean, places=14)
            self.assertAlmostEqual(float(row["sample_std"]), sd, places=14)
            self.assertEqual((row["n_training_seeds"], row["ddof"]), ("3", "1"))

    def test_protocol_direction_and_nonmonotonic_gap(self):
        for seed in ("42", "43", "44"):
            for split in ("validation", "test"):
                for metric in ms96.RANKING:
                    k5, k20, k50 = [self.lookup[seed, split, p, metric] for p in ms96.PROTOCOLS]
                    self.assertGreater(k5, 0)
                    self.assertGreater(k50, 0)
                    self.assertGreater(k20, k5)
                    self.assertGreater(k20, k50)
        self.assertLess(self.lookup["43", "test", "k50_seed42", "HR@1"], self.lookup["43", "test", "k5", "HR@1"])
        self.assertLess(self.lookup["44", "validation", "k50_seed42", "HR@1"], self.lookup["44", "validation", "k5", "HR@1"])

    def test_y_exception_and_all_test_point_estimates(self):
        for seed in ("42", "43", "44"):
            for metric in ms96.BINARY:
                self.assertGreater(self.lookup[seed, "test", "binary", metric], 0)
        self.assertLess(self.lookup["44", "validation", "binary", "Accuracy"], 0)
        self.assertAlmostEqual(self.lookup["44", "validation", "binary", "Accuracy"], -0.0008884581213148834)

    def test_exposure_narrowing_is_validation_only(self):
        source = rows(".agent/exposure_scaling/final_evidence/exposure_main_table.csv")
        points = {(r["run"], r["split"]): float(r["primary_value"]) for r in source
                  if r["task"] in ("N-native ranking", "M-N ranking")}
        validation48 = points["N48", "validation"] - points["M1-48", "validation"]
        test48 = points["N48", "test"] - points["M1-48", "test"]
        self.assertLess(self.lookup["42", "validation", "k5", "HR@1"], validation48)
        self.assertGreater(self.lookup["42", "test", "k5", "HR@1"], test48)

    def test_preserved_files_and_append_only_literature_freeze(self):
        baseline = json.loads((ROOT / "paper/plan/review/ms96_scope_baseline.json").read_text(encoding="utf-8"))
        contract = assert_current_contract(self, ROOT)
        historical = {row["path"]: row for row in contract["historical_baselines"]}
        baseline_path = "paper/plan/review/ms96_scope_baseline.json"
        self.assertEqual(file_sha256(ROOT / baseline_path), historical[baseline_path]["sha256"])
        freeze = (ROOT / "paper/evidence/story_and_novelty_freeze.md").read_text(encoding="utf-8")
        self.assertTrue(freeze.startswith(baseline["freeze_prefix"]))
        self.assertIn("## MS96 Evidence Update", freeze[len(baseline["freeze_prefix"]):])

    def test_split_tables_and_mean_std_cannot_replace_raw_values(self):
        for split in ("validation", "test"):
            main = rows(f"paper/tables/ms96_main_{split}.csv")
            protocols = rows(f"paper/tables/ms96_protocol_{split}.csv")
            self.assertEqual(len(main), 3)
            self.assertEqual(len(main[0]), 13)
            self.assertEqual(len(protocols), 9)
            self.assertEqual({r["protocol"] for r in protocols}, set(ms96.PROTOCOLS))

    def test_current_markers_and_required_evidence_boundaries(self):
        paths = list((ROOT / "paper/modules").glob("*.md"))
        paths += list((ROOT / "paper/modules_parts/results").glob("*.md"))
        paths += list((ROOT / "paper/modules_parts/discussion").glob("*.md"))
        paths += [ROOT / "paper/modules_parts/methods/bootstrap_and_statistics.md"]
        prose = "\n".join(p.read_text(encoding="utf-8") for p in paths if p.name != "02_related_work.md")
        self.assertNotRegex(prose, r"EVIDENCE_PENDING:\s*(MS96|Y96_STATUS)")
        self.assertIn("sample SD with n=3 and ddof=1", prose)
        self.assertIn("full MovieLens trajectories remain seed42-only", prose)
        self.assertIn("not equivalence or positive transfer across training seeds", prose)
        self.assertIn("not uniformly larger than k5", prose)
        self.assertIn("candidate-generation seed42", prose.lower())
        self.assertNotRegex(prose, r"(?i)near.perfect parity|gap disappears|significant improvement across seeds")

    def test_incomplete_and_wrong_seed_summary_are_rejected(self):
        real_read = ms96.read_sections
        first = ms96.IMPORTED / "seed43/validation_summary.txt"
        base, hard = real_read(first)
        with patch.object(ms96, "read_sections", return_value=(base[:-1], hard)):
            with self.assertRaisesRegex(ValueError, "Incomplete"):
                ms96.load_records()
        wrong = [dict(row) for row in base]
        wrong[0]["seed"] = "44"
        with patch.object(ms96, "read_sections", return_value=(wrong, hard)):
            with self.assertRaisesRegex(ValueError, "Seed/split mismatch"):
                ms96.load_records()


if __name__ == "__main__":
    unittest.main()
