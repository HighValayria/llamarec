from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import sys
import tempfile
import unittest
from unittest import mock


REPO = Path(__file__).resolve().parents[4]
LAYER = REPO / "paper" / "submission" / "ieee_generic"
sys.path.insert(0, str(LAYER))

from build_submission import (
    BuildError, CJK, LatexRenderer, build_submission, format_table_cell,
    language_setup, latexmk_is_usable, tex_engine_command,
)


def tree_hashes(root: Path) -> dict[str, str]:
    return {
        str(path.relative_to(root)).replace("\\", "/"): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(root.rglob("*")) if path.is_file()
    }


class SubmissionBuildTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        builds = REPO / "paper" / "builds"
        cls.temp = tempfile.TemporaryDirectory(dir=builds, prefix="ieee_test_")
        cls.root = Path(cls.temp.name)
        cls.en = build_submission("en", cls.root)
        cls.bi = build_submission("bilingual", cls.root)

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def text(self, lang: str) -> str:
        return "\n".join(path.read_text(encoding="utf-8") for path in sorted((self.root / lang).rglob("*.tex")))

    def test_shared_source_has_expected_structure(self):
        self.assertEqual(self.en["section_order"], self.bi["section_order"])
        self.assertEqual(len(self.en["section_order"]), 9)
        self.assertEqual(self.en["paragraph_count"], 78)
        self.assertEqual(self.bi["paragraph_count"], 78)
        self.assertEqual(self.en["paragraph_ids"], self.bi["paragraph_ids"])
        self.assertEqual(self.en["english_paragraph_sha256"], self.bi["english_paragraph_sha256"])
        self.assertEqual(self.en["source_of_truth"], "paper/modules and paper/modules_parts Markdown")

    def test_language_isolation_and_pair_interleaving(self):
        english = self.text("en")
        bilingual = self.text("bilingual")
        self.assertIsNone(CJK.search(english))
        sequence = re.findall(r"\\llamarec(EN|ZH)\{\}", bilingual)
        self.assertEqual(sequence, [item for _ in range(78) for item in ("EN", "ZH")])
        self.assertEqual(bilingual.count(r"\llamarecEN{}"), 78)
        self.assertEqual(bilingual.count(r"\llamarecZH{}"), 78)

    def test_citations_and_references_are_closed(self):
        self.assertEqual(self.en["citation_keys"], self.bi["citation_keys"])
        self.assertEqual(len(self.en["citation_keys"]), 25)
        self.assertEqual(self.en["reference_labels"], self.bi["reference_labels"])
        self.assertEqual(len(self.en["reference_labels"]), 11)
        self.assertEqual(self.en["static_validation"]["status"], "PASSED")
        self.assertEqual(self.bi["static_validation"]["status"], "PASSED")

    def test_all_tables_are_editable_and_data_identical(self):
        self.assertEqual(len(self.en["tables"]), 9)
        self.assertEqual(len(self.bi["tables"]), 9)
        en_tables = {item["id"]: item for item in self.en["tables"]}
        bi_tables = {item["id"]: item for item in self.bi["tables"]}
        self.assertEqual(set(en_tables), set(bi_tables))
        for key in en_tables:
            self.assertEqual(en_tables[key]["source_sha256"], bi_tables[key]["source_sha256"])
            self.assertEqual(en_tables[key]["data_payload_sha256"], bi_tables[key]["data_payload_sha256"])
            self.assertEqual(en_tables[key]["row_count"], bi_tables[key]["row_count"])
            self.assertEqual(en_tables[key]["display_precision"], 5)
            self.assertEqual(bi_tables[key]["display_precision"], 5)
            generated = (self.root / "en" / "generated_tables" / f"{key}.tex").read_text(encoding="utf-8")
            self.assertIn(r"\begin{tabular}", generated)
            self.assertNotIn(r"\includegraphics", generated)

    def test_figure_bytes_and_shared_dependencies_are_identical(self):
        self.assertEqual(len(self.en["figures"]), 2)
        self.assertEqual(len(self.bi["figures"]), 2)
        en_figures = {item["id"]: item for item in self.en["figures"]}
        bi_figures = {item["id"]: item for item in self.bi["figures"]}
        for key in en_figures:
            self.assertEqual(en_figures[key]["source_sha256"], en_figures[key]["generated_sha256"])
            self.assertEqual(en_figures[key]["generated_sha256"], bi_figures[key]["generated_sha256"])
        for name in ("library.bib", "IEEEtran.cls"):
            self.assertEqual(
                hashlib.sha256((self.root / "en" / name).read_bytes()).hexdigest(),
                hashlib.sha256((self.root / "bilingual" / name).read_bytes()).hexdigest(),
            )

    def test_anonymous_default_and_camera_ready_guard(self):
        main = (self.root / "en" / "main.tex").read_text(encoding="utf-8")
        self.assertIn("Anonymous Authors", main)
        self.assertNotIn("Transatlanticism", main)
        guarded_root = self.root / "guarded"
        with self.assertRaisesRegex(BuildError, "configured authors"):
            build_submission("en", guarded_root, mode="camera_ready")

    def test_markdown_ast_supports_required_constructs(self):
        markdown = """# Methods

Text with **bold**, *emphasis*, `code_value`, $x+y$, [@ref].

$$
x = y + 1
$$

- first
- second
"""
        renderer = LatexRenderer("en", ["methods"])
        rendered = renderer.render(markdown)
        self.assertIn(r"\section{Methods}\label{sec:methods}", rendered)
        self.assertIn(r"\textbf{bold}", rendered)
        self.assertIn(r"\emph{emphasis}", rendered)
        self.assertIn(r"\texttt{code\_value}", rendered)
        self.assertIn(r"$x+y$", rendered)
        self.assertIn(r"\cite{ref}", rendered)
        self.assertIn(r"\begin{equation}", rendered)
        self.assertIn(r"\begin{itemize}", rendered)
        self.assertEqual(len(renderer.equation_ids), 1)

    def test_numeric_display_precision_preserves_integer_and_sign(self):
        self.assertEqual(format_table_cell("42", 5), "42")
        self.assertEqual(format_table_cell("24000", 5), "24000")
        self.assertEqual(format_table_cell("0.784350667", 5), "0.78435")
        self.assertEqual(format_table_cell("-0.0000001", 5), "-0.00000")
        self.assertEqual(format_table_cell("k20_seed42", 5), "k20_seed42")

    def test_cjk_auto_fallback_is_portable_and_ordered(self):
        config = {
            "bilingual_cjk_font": "AUTO",
            "bilingual_cjk_font_candidates": [
                "Noto Serif CJK SC", "Noto Serif SC", "Source Han Serif SC", "SimSun",
            ],
        }
        setup = language_setup("bilingual", config)
        positions = [setup.index(value) for value in config["bilingual_cjk_font_candidates"]]
        self.assertEqual(positions, sorted(positions))
        self.assertNotRegex(setup, r"[A-Za-z]:[/\\]")
        self.assertIn("No supported CJK font found", setup)

    def test_latexmk_probe_and_miktex_explicit_command(self):
        with mock.patch("build_submission.subprocess.run") as run:
            run.return_value.returncode = 1
            self.assertFalse(latexmk_is_usable("latexmk"))
            run.return_value.returncode = 0
            self.assertTrue(latexmk_is_usable("latexmk"))
        miktex = tex_engine_command(r"D:\\Tools\\miketex\\pdflatex.exe")
        other = tex_engine_command("/usr/bin/pdflatex")
        self.assertIn("--disable-installer", miktex)
        self.assertNotIn("--disable-installer", other)

    def test_repeated_generation_is_byte_reproducible(self):
        before_en = tree_hashes(self.root / "en")
        before_bi = tree_hashes(self.root / "bilingual")
        build_submission("en", self.root)
        build_submission("bilingual", self.root)
        self.assertEqual(before_en, tree_hashes(self.root / "en"))
        self.assertEqual(before_bi, tree_hashes(self.root / "bilingual"))


if __name__ == "__main__":
    unittest.main()
