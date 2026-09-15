"""核验本轮文献资产与双语段落的可追溯关系，不代替原文核验。"""

from collections import Counter
import json
from pathlib import Path
import re
import sys
import unittest

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "paper/assembly"))

from assemble import SourceReader
from template_adapter import parse_yaml


class CapturingReader(SourceReader):
    def __init__(self, *args):
        super().__init__(*args)
        self.texts = {}

    def paragraph(self, identifier, segment, relative):
        rendered = super().paragraph(identifier, segment, relative)
        self.texts[identifier] = rendered
        return rendered


class LiteratureAssetTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        manifest = parse_yaml(
            (ROOT / "paper/assembly/paper_manifest.yaml").read_text(encoding="utf-8-sig")
        )
        cls.readers = {}
        for lang in ("en", "zh"):
            reader = CapturingReader(ROOT, manifest, lang, "draft")
            for module in manifest["modules"]:
                if module["id"] in {"contributions", "introduction", "related_work"}:
                    reader.read(module["source"], expected_id=module["id"])
            cls.readers[lang] = reader
        cls.manuscript_reader = CapturingReader(ROOT, manifest, "en", "draft")
        for module in manifest["modules"]:
            cls.manuscript_reader.read(module["source"], expected_id=module["id"])
        cls.registry = json.loads(
            (ROOT / "paper/references/citation_registry.json").read_text(encoding="utf-8")
        )
        cls.records = {row["citation_key"]: row for row in cls.registry["sources"]}
        cls.gaps = json.loads(
            (ROOT / "paper/references/literature_gap_registry.json").read_text(encoding="utf-8")
        )

    def test_cited_keys_resolve_and_match_languages(self):
        # 这里只校验现有BibTeX键，不将键扫描当作完整BibTeX解析。
        bib = (ROOT / "paper/references/library.bib").read_text(encoding="utf-8-sig")
        bib_keys = set(re.findall(r"(?m)^@\w+\s*\{\s*([^,\s]+)\s*,", bib))
        en, zh = self.readers["en"], self.readers["zh"]
        self.assertEqual(set(en.texts), set(zh.texts))
        for identifier, english in en.texts.items():
            with self.subTest(paragraph=identifier):
                citations = Counter(re.findall(r"@([A-Za-z0-9_.:-]+)", english))
                self.assertEqual(
                    citations,
                    Counter(re.findall(r"@([A-Za-z0-9_.:-]+)", zh.texts[identifier])),
                )
                for key in citations:
                    self.assertIn(key, bib_keys)
                    self.assertIn(key, self.records)
                    row = self.records[key]
                    self.assertEqual(row["verified"], "VERIFIED")
                    self.assertIn(row["source_id"], en.paragraphs[identifier]["evidence"])

    def test_gap_registry_matches_bilingual_markers(self):
        expected = {}
        for row in self.gaps["gaps"]:
            if not row.get("marker_required", True):
                continue
            for identifier in row["paragraphs"]:
                expected.setdefault(identifier, Counter())[row["label"]] += 1
        for lang, reader in self.readers.items():
            actual = {}
            for identifier, text in reader.texts.items():
                labels = re.findall(r"\[CITATION_NEEDED:\s*([A-Z0-9_]+)\]", text)
                if labels:
                    actual[identifier] = Counter(labels)
            with self.subTest(language=lang):
                self.assertEqual(actual, expected)

    def test_registry_has_scoped_local_provenance(self):
        rows = self.registry["sources"]
        self.assertEqual(len(rows), len(self.records))
        self.assertEqual(len(rows), len({row["source_id"] for row in rows}))
        for row in rows:
            with self.subTest(citation=row["citation_key"]):
                for field in (
                    "title", "authors", "year", "venue", "source", "topic", "current_paper_section",
                    "supported_claim", "source_location", "verification_scope",
                ):
                    self.assertTrue(row[field])
                self.assertIn(row["verified"], {"VERIFIED", "PARTIAL", "REJECTED"})
                self.assertIsInstance(row["full_text_read"], bool)
                for location in row["source_location"].split(";"):
                    path = (ROOT / location.strip().split("#", 1)[0]).resolve()
                    self.assertTrue(path.is_relative_to(ROOT))
                    self.assertTrue(path.is_file(), str(path))


    def test_applied_gaps_have_bilingual_wording_and_scoped_evidence(self):
        self.assertEqual(self.gaps["mode"], "MANUSCRIPT_INTEGRATION")
        self.assertEqual(self.gaps["manuscript_application"], "APPLIED")
        self.assertEqual(len(self.gaps["gaps"]), 6)
        self.assertEqual(len({row["label"] for row in self.gaps["gaps"]}), 6)
        for row in self.gaps["gaps"]:
            with self.subTest(gap=row["label"]):
                self.assertIn(
                    row["status"], {"RESOLVED_WITH_CITATION", "REWRITTEN_AND_RESOLVED"}
                )
                self.assertEqual(row["action"], row["status"])
                self.assertEqual(row["manuscript_status"], row["status"])
                self.assertFalse(row["marker_required"])
                self.assertEqual(row["manuscript_application"], "APPLIED")
                self.assertIn(row["evidence_status"], {"RESOLVED", "PARTIALLY_RESOLVED"})
                self.assertTrue(row["original_claim"])
                self.assertTrue(row["resolution"])
                self.assertTrue(row["remaining_uncertainty"])
                self.assertTrue((ROOT / row["evidence"]).is_file())
                self.assertTrue(row["supporting_citations"])
                for lang in ("en", "zh"):
                    actual = self.readers[lang].texts[row["paragraphs"][0]]
                    self.assertEqual(actual, row["final_wording_" + lang])
                    cited = set(re.findall(r"@([A-Za-z0-9_.:-]+)", actual))
                    self.assertEqual(cited, set(row["supporting_citations"]))
                for key in row["supporting_citations"]:
                    self.assertEqual(self.records[key]["verified"], "VERIFIED")
        joint = next(row for row in self.gaps["gaps"] if row["priority"] == "P0")
        self.assertEqual(joint["evidence_status"], "PARTIALLY_RESOLVED")
        self.assertEqual(joint["status"], "REWRITTEN_AND_RESOLVED")
        self.assertFalse(joint["blocker"])

    def test_actual_citation_positions_match_registry(self):
        actual = {}
        for identifier, text in self.manuscript_reader.texts.items():
            for key in set(re.findall(r"@([A-Za-z0-9_.:-]+)", text)):
                actual.setdefault(key, set()).add(identifier)
        for key, row in self.records.items():
            with self.subTest(citation=key):
                if key in actual:
                    self.assertEqual(
                        set(row["current_paper_section"].split("; ")), actual[key]
                    )
                else:
                    self.assertTrue(row["current_paper_section"].startswith("未引用"))
        self.assertTrue({
            "geng2022p5", "bao2023tallrec", "liu2025itdr",
            "zhang2023instructrec", "zhou2025openonerec",
            "penha2024bridging", "onerecteam2026onereason",
        }.issubset(actual))
        self.assertNotIn("sun2019bert4rec", actual)

    def test_contribution_hierarchy_and_bounded_findings(self):
        texts = self.readers["en"].texts
        self.assertEqual(len(texts), 20)
        sizes = [len(texts[f"contributions.p0{i}"].split()) for i in range(1, 5)]
        self.assertEqual(sizes[0], min(sizes))
        self.assertEqual(sizes[1], max(sizes))
        for phrase in ("seed42", "standard-k5 validation", "test subset", "N advantage"):
            self.assertIn(phrase, texts["intro.p06"])
        prose = "\n".join(texts.values())
        self.assertNotRegex(
            prose,
            r"(?i)we are the first|no prior work|largely in isolation|"
            r"across seeds|P5 used unmatched budgets|novel evaluation protocol",
        )

    def test_primary_notes_and_landscapes_exist(self):
        notes = (ROOT / "paper/references/primary_source_notes.md").read_text(encoding="utf-8")
        for row in self.registry["sources"]:
            self.assertIn("## " + row["source_id"] + "\n", notes)
            self.assertIsInstance(row["body_sections_read"], bool)
            self.assertTrue(row["primary_sources"])
            for source in row["primary_sources"]:
                self.assertTrue(source["url"].startswith("https://"))
                self.assertTrue(source["locator"])
        for name in (
            "joint_conditioning_landscape.md", "unified_multitask_landscape.md",
            "evaluation_sampling_evidence.md", "exposure_budget_landscape.md",
            "targeted_search_log.md",
        ):
            self.assertTrue((ROOT / "paper/references" / name).is_file())


if __name__ == "__main__":
    unittest.main()
