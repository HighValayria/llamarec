from __future__ import annotations

import csv
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
TABLES = ROOT / "paper/tables/scientific_repair_2026-09-11"


def rows(name: str) -> list[dict[str, str]]:
    with (TABLES / name).open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


class ScientificRepairContractTest(unittest.TestCase):
    def test_clean_table_shapes_and_directions(self) -> None:
        exposure = rows("m1_common_safe_exposure.csv")
        multiseed = rows("m1_clean_multiseed_96.csv")
        coverage = rows("m1_cross_task_safe_coverage.csv")
        self.assertEqual(len(exposure), 12)
        self.assertEqual(len(multiseed), 18)
        self.assertEqual(len(coverage), 4)
        self.assertTrue(all(float(row["delta_N_minus_M1"]) > 0 for row in exposure))
        self.assertTrue(all(row["signs_42_43_44"] == "+/+/+" for row in multiseed))
        self.assertEqual([row["retained"] for row in coverage], ["5494", "5600", "5318", "5535"])

    def test_active_manuscript_uses_final_protocol_framing(self) -> None:
        paths = sorted((ROOT / "paper/modules").glob("*.md"))
        paths += sorted((ROOT / "paper/modules_parts").rglob("*.md"))
        text = "\n".join(path.read_text(encoding="utf-8") for path in paths).lower()
        for phrase in ("detected leakage", "contaminated", "post-hoc repair", "salvage"):
            self.assertNotIn(phrase, text)
        self.assertIn("cross-task-safe subset", text)
        self.assertIn("evaluation-side restriction", text)
        self.assertNotIn("training used a joint temporal cutoff", text)

    def test_old_ranking_intervals_are_not_active(self) -> None:
        for name in ("m1_common_safe_exposure.csv", "m1_clean_multiseed_96.csv", "m1_cross_task_safe_coverage.csv"):
            header = set(rows(name)[0])
            self.assertFalse({"ci95_low", "ci95_high"} & header)
        self.assertEqual(len(rows("y_side_binary_bootstrap.csv")), 3)
        self.assertEqual(len(rows("amazon_certified_models.csv")), 4)

    def test_sasrec_disclosure_is_complete(self) -> None:
        text = (ROOT / "paper/modules_parts/methods/baseline_setup.md").read_text(encoding="utf-8")
        for token in ("64", "2 causal Transformer layers", "256", "GELU", "0.2", "AdamW", "0.001", "512", "S391", "200,000", "independently trained from scratch"):
            self.assertIn(token, text)


if __name__ == "__main__":
    unittest.main()
