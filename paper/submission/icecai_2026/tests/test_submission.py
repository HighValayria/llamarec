from __future__ import annotations

from pathlib import Path
import tempfile
import unittest


REPO = Path(__file__).resolve().parents[4]
LAYER = REPO / "paper" / "submission" / "icecai_2026"
import sys
sys.path.insert(0, str(LAYER))

from build_submission import BuildError, build_submission, render_author_block


class IcecaiSubmissionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        builds = REPO / "paper" / "builds"
        cls.temp = tempfile.TemporaryDirectory(dir=builds, prefix="icecai_test_")
        cls.root = Path(cls.temp.name)
        cls.en = build_submission("en", cls.root)
        cls.bi = build_submission("bilingual", cls.root)

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_pre_final_build_contract(self):
        self.assertEqual(self.en["submission_status"], "VENUE_ADAPTED_PRE_FINAL")
        self.assertEqual(self.en["author_status"], "USER_MANUAL_COMPLETION_REQUIRED")
        self.assertEqual(self.en["genai_status"], "USER_MANUAL_COMPLETION_REQUIRED")
        self.assertEqual(self.en["word_status"], "ORGANIZER_OR_PORTAL_CONFIRMATION_REQUIRED")
        self.assertEqual(len(self.en["tables"]), 9)
        self.assertEqual(len(self.en["figures"]), 2)

    def test_keywords_and_english_isolation(self):
        keywords = (self.root / "en" / "sections" / "00_keywords.tex").read_text(encoding="utf-8")
        self.assertIn("Large language model recommendation", keywords)
        self.assertIn("Task-sample exposure", keywords)
        self.assertNotIn("pending user decision", keywords)
        self.assertEqual(len(self.en["keywords"]), 5)

    def test_reference_recency_and_country_contracts(self):
        self.assertEqual(self.en["reference_recency"]["active_cited_references"], 25)
        self.assertEqual(self.en["reference_recency"]["recent_2024_2026"], 13)
        self.assertEqual(self.en["reference_recency"]["status"], "PASS")
        self.assertEqual(self.en["country_source_compliance"]["status"], "PASS")
        self.assertGreaterEqual(len(self.en["country_source_compliance"]["countries"]), 3)

    def test_disclosure_is_disabled_and_not_rendered(self):
        self.assertFalse(self.en["genai_disclosure"]["enabled"])
        self.assertFalse((self.root / "en" / "sections" / "99_genai_disclosure.tex").exists())
        main = (self.root / "en" / "main.tex").read_text(encoding="utf-8")
        self.assertNotIn("99_genai_disclosure", main)

    def test_author_submission_validation_and_rendering(self):
        with self.assertRaisesRegex(BuildError, "real author information"):
            render_author_block({"authors": []}, "submission")
        authors = [
            {"name": "A", "department": "D", "institution": "I", "city": "C", "country": "X", "email": "a@x", "corresponding": True},
            {"name": "B", "department": "D", "institution": "I", "city": "C", "country": "Y", "email": "b@y", "corresponding": False},
        ]
        rendered = render_author_block({"authors": authors}, "submission")
        self.assertEqual(rendered.count(r"\textsuperscript{*}"), 1)
        self.assertIn("a@x", rendered)
        authors[1]["corresponding"] = True
        with self.assertRaisesRegex(BuildError, "exactly one"):
            render_author_block({"authors": authors}, "submission")

    def test_en_bilingual_scientific_source_identity(self):
        self.assertEqual(self.en["paragraph_ids"], self.bi["paragraph_ids"])
        self.assertEqual(self.en["english_paragraph_sha256"], self.bi["english_paragraph_sha256"])
        self.assertEqual(self.en["citation_keys"], self.bi["citation_keys"])


if __name__ == "__main__":
    unittest.main()
