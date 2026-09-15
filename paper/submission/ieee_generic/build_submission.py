"""Generate reproducible English and bilingual generic IEEE LaTeX builds."""

from __future__ import annotations

import argparse
from collections import OrderedDict
import csv
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import mistune


REPO = Path(__file__).resolve().parents[3]
ASSEMBLY_DIR = REPO / "paper" / "assembly"
if str(ASSEMBLY_DIR) not in sys.path:
    sys.path.insert(0, str(ASSEMBLY_DIR))

from assemble import ASSET, COMMENT, DIRECTIVE, SourceReader, digest  # noqa: E402
from template_adapter import AssemblyError, contained_path, parse_yaml  # noqa: E402


LAYER_DIR = Path(__file__).resolve().parent
CONFIG_PATH = LAYER_DIR / "submission_config.yaml"
MANIFEST_PATH = REPO / "paper" / "assembly" / "paper_manifest.yaml"
MAIN_TEMPLATE_PATH = LAYER_DIR / "main_template.tex"
IEEE_CLASS_PATH = REPO / "paper" / "templates" / "Conference-LaTeX-template_10-17-19" / "IEEEtran.cls"
BIB_PATH = REPO / "paper" / "references" / "library.bib"
DEFAULT_BUILD_ROOT = REPO / "paper" / "builds" / "ieee_generic"

CITATION = re.compile(r"\[((?:\s*@[-:.\w]+\s*(?:;\s*)?)+)\]")
CITATION_KEY = re.compile(r"@([-:.\w]+)")
BIB_KEY = re.compile(r"@\w+\s*\{\s*([^,\s]+)", re.I)
CJK = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]")
FLOAT_NUMBER = re.compile(r"[-+]?(?:\d+\.\d+|\d+(?:\.\d+)?[eE][-+]?\d+)\Z")
FORBIDDEN = (
    "EVIDENCE:", "PARAGRAPH:", "RUN_METADATA", "BOOTSTRAP_PROVENANCE",
    "claim_matrix", ".agent", "F:/Projects", "F:\\Projects", "/root/llamarec",
)


class BuildError(RuntimeError):
    """Submission generation or validation failure."""


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_text(value: str) -> str:
    return sha256_bytes(value.encode("utf-8"))


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def latex_escape(value: str) -> str:
    replacements = {
        "\\": r"\textbackslash{}", "&": r"\&", "%": r"\%", "$": r"\$",
        "#": r"\#", "_": r"\_", "{": r"\{", "}": r"\}",
        "~": r"\textasciitilde{}", "^": r"\textasciicircum{}",
    }
    return "".join(replacements.get(char, char) for char in value)


def load_yaml(path: Path) -> dict:
    value = parse_yaml(path.read_text(encoding="utf-8-sig"))
    if not isinstance(value, dict):
        raise BuildError(f"YAML root must be a mapping: {path}")
    return value


def read_frontmatter(path: Path) -> dict:
    source = path.read_text(encoding="utf-8-sig")
    if not source.startswith("---\n") or "\n---\n" not in source[4:]:
        raise BuildError(f"Missing frontmatter: {path}")
    return parse_yaml(source[4:].split("\n---\n", 1)[0])


class RecordingSourceReader(SourceReader):
    """SourceReader with ordered document IDs and language text fingerprints."""

    def __init__(self, root: Path, manifest: dict, lang: str, mode: str):
        super().__init__(root, manifest, lang, mode)
        self.ordered_document_ids: list[str] = []
        self.paragraph_records: OrderedDict[str, dict] = OrderedDict()

    def read(self, relative: str, level: int = 1, expected_id: str | None = None, title_override=None) -> str:
        path = contained_path(self.root, relative)
        meta = read_frontmatter(path)
        self.ordered_document_ids.append(meta["id"])
        return super().read(relative, level, expected_id, title_override)

    def paragraph(self, identifier: str, segment: str, relative: str) -> str:
        rendered = super().paragraph(identifier, segment, relative)
        clean = COMMENT.sub("", segment).strip()
        pair = re.fullmatch(r"\*\*EN\*\*\s*\n+(.+?)\n+\*\*ZH\*\*\s*\n+(.+)", clean, re.S)
        if pair is None:
            raise BuildError(f"Unable to record language pair: {identifier}")
        en, zh = (part.strip() for part in pair.groups())
        self.paragraph_records[identifier] = {"source": relative, "en": en, "zh": zh}
        return rendered


class LatexRenderer:
    def __init__(self, lang: str, document_ids: list[str]):
        self.lang = lang
        self.document_ids = iter(document_ids)
        self.citation_keys: set[str] = set()
        self.reference_labels: set[str] = set()
        self.defined_labels: set[str] = set()
        self.equation_ids: list[str] = []
        self.assets_to_emit: list[tuple[str, str]] = []
        self.emitted_assets: set[tuple[str, str]] = set()
        self.current_pair_language: str | None = None
        self.markdown = mistune.create_markdown(renderer="ast", plugins=["math"])

    def render(self, markdown: str, drop_first_heading: bool = False) -> str:
        nodes = self.markdown(markdown)
        if drop_first_heading:
            if not nodes or nodes[0].get("type") != "heading":
                raise BuildError("Abstract source must begin with a heading")
            self._consume_heading_id(nodes.pop(0))
        output = self._blocks(nodes)
        try:
            extra = next(self.document_ids)
        except StopIteration:
            extra = None
        if extra is not None:
            raise BuildError(f"Document ID was not mapped to a heading: {extra}")
        return output.rstrip() + "\n"

    def _consume_heading_id(self, node: dict) -> str:
        try:
            identifier = next(self.document_ids)
        except StopIteration as exc:
            raise BuildError("Heading has no source document ID") from exc
        label = f"sec:{identifier}"
        self.defined_labels.add(label)
        return label

    def _blocks(self, nodes: list[dict]) -> str:
        parts: list[str] = []
        for node in nodes:
            kind = node["type"]
            if kind == "blank_line":
                continue
            if kind == "heading":
                level = int(node.get("attrs", {}).get("level", 1))
                command = {1: "section", 2: "subsection", 3: "subsubsection"}.get(level, "paragraph")
                label = self._consume_heading_id(node)
                parts.append(f"\\{command}{{{self._inline(node.get('children', []))}}}\\label{{{label}}}")
            elif kind in {"paragraph", "block_text"}:
                rendered = self._inline(node.get("children", []))
                parts.append(rendered)
                if self.lang == "en" or self.current_pair_language == "zh":
                    parts.extend(self._flush_assets())
            elif kind == "block_math":
                raw = node.get("raw", "").strip()
                identifier = "eq:" + sha256_text(raw)[:12]
                self.equation_ids.append(identifier)
                self.defined_labels.add(identifier)
                parts.append(f"\\begin{{equation}}\n{raw}\n\\label{{{identifier}}}\n\\end{{equation}}")
            elif kind == "block_code":
                parts.append("\\begin{verbatim}\n" + node.get("raw", "").rstrip() + "\n\\end{verbatim}")
            elif kind == "list":
                ordered = bool(node.get("attrs", {}).get("ordered"))
                env = "enumerate" if ordered else "itemize"
                items = []
                for item in node.get("children", []):
                    if item.get("type") != "list_item":
                        raise BuildError(f"Unsupported list child: {item.get('type')}")
                    items.append("\\item " + self._blocks(item.get("children", [])).strip())
                parts.append(f"\\begin{{{env}}}\n" + "\n".join(items) + f"\n\\end{{{env}}}")
            elif kind == "thematic_break":
                parts.append(r"\par\noindent\rule{\columnwidth}{0.4pt}")
            else:
                raise BuildError(f"Unsupported Markdown block: {kind}")
        return "\n\n".join(part for part in parts if part)

    def _inline(self, nodes: list[dict]) -> str:
        parts: list[str] = []
        index = 0
        while index < len(nodes):
            node = nodes[index]
            kind = node["type"]
            if kind == "text":
                raw = node.get("raw", "")
                index += 1
                while index < len(nodes) and nodes[index].get("type") == "text":
                    raw += nodes[index].get("raw", "")
                    index += 1
                parts.append(self._text(raw))
                continue
            elif kind == "strong":
                raw = self._plain(node.get("children", [])).strip()
                if self.lang == "bilingual" and raw in {"EN", "ZH"}:
                    self.current_pair_language = raw.lower()
                    parts.append(f"\\llamarec{raw}{{}}")
                else:
                    parts.append("\\textbf{" + self._inline(node.get("children", [])) + "}")
            elif kind == "emphasis":
                parts.append("\\emph{" + self._inline(node.get("children", [])) + "}")
            elif kind == "codespan":
                parts.append("\\texttt{" + latex_escape(node.get("raw", "")) + "}")
            elif kind == "inline_math":
                parts.append("$" + node.get("raw", "") + "$")
            elif kind == "link":
                url = latex_escape(node.get("attrs", {}).get("url", ""))
                parts.append(f"\\href{{{url}}}{{{self._inline(node.get('children', []))}}}")
            elif kind == "image":
                raise BuildError("Inline Markdown images are not allowed; use [FIGURE: id]")
            elif kind in {"softbreak", "linebreak"}:
                parts.append("\n" if kind == "softbreak" else "\\\\\n")
            else:
                raise BuildError(f"Unsupported Markdown inline: {kind}")
            index += 1
        return "".join(parts)

    def _plain(self, nodes: list[dict]) -> str:
        return "".join(node.get("raw", "") if node.get("type") == "text" else self._plain(node.get("children", [])) for node in nodes)

    def _text(self, value: str) -> str:
        tokens: list[str] = []
        combined = re.compile(r"\[((?:\s*@[-:.\w]+\s*(?:;\s*)?)+)\]|\[(TABLE|FIGURE):\s*([a-z][a-z0-9_]*)\]")
        position = 0
        for match in combined.finditer(value):
            tokens.append(latex_escape(value[position:match.start()]))
            if match.group(1) is not None:
                keys = CITATION_KEY.findall(match.group(1))
                self.citation_keys.update(keys)
                tokens.append("\\cite{" + ",".join(keys) + "}")
            else:
                kind, key = match.group(2), match.group(3)
                label = ("tab:" if kind == "TABLE" else "fig:") + key
                self.reference_labels.add(label)
                tokens.append(("Table" if kind == "TABLE" else "Figure") + f"~\\ref{{{label}}}")
                asset = (kind, key)
                if asset not in self.emitted_assets and asset not in self.assets_to_emit:
                    self.assets_to_emit.append(asset)
            position = match.end()
        tokens.append(latex_escape(value[position:]))
        return "".join(tokens)

    def _flush_assets(self) -> list[str]:
        rendered = []
        for kind, key in self.assets_to_emit:
            asset = (kind, key)
            if asset in self.emitted_assets:
                continue
            group = "generated_tables" if kind == "TABLE" else "generated_figures"
            rendered.append(f"\\input{{{group}/{key}}}")
            self.emitted_assets.add(asset)
        self.assets_to_emit.clear()
        return rendered


def format_table_cell(value: str, precision: int) -> str:
    if FLOAT_NUMBER.fullmatch(value):
        return f"{float(value):.{precision}f}"
    return value


def table_tex(key: str, spec: dict, lang: str, width_class: str, display_precision: int) -> tuple[str, dict]:
    source = contained_path(REPO / "paper", spec["source"])
    columns = spec.get("columns", [])
    keys = [column["key"] for column in columns]
    with source.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        if not keys or len(set(keys)) != len(keys) or not set(keys).issubset(reader.fieldnames or []):
            raise BuildError(f"Invalid displayed columns for table {key}")
        if not rows or any(None in row or any(row.get(name) is None for name in keys) for row in rows):
            raise BuildError(f"Empty or malformed CSV table {key}")
    caption = spec["caption"]["en"]
    if lang == "bilingual":
        caption += " / " + spec["caption"]["zh"]
    headers = [column["title"]["en"] for column in columns]
    wide = width_class == "LIKELY_DOUBLE_COLUMN"
    env = "table*" if wide else "table"
    width = r"\textwidth" if wide else r"\columnwidth"
    alignment = "l" + "r" * (len(keys) - 1)
    body = [
        f"\\begin{{{env}}}[!t]",
        "\\caption{" + latex_escape(caption) + "}",
        f"\\label{{tab:{key}}}",
        "\\centering", "\\scriptsize", r"\setlength{\tabcolsep}{3pt}",
        f"\\resizebox{{{width}}}{{!}}{{%", f"\\begin{{tabular}}{{{alignment}}}", r"\toprule",
        " & ".join(latex_escape(value) for value in headers) + r" \\", r"\midrule",
    ]
    payload = []
    for row in rows:
        values = [row[name] for name in keys]
        payload.append(values)
        displayed = [format_table_cell(value, display_precision) for value in values]
        body.append(" & ".join(latex_escape(value) for value in displayed) + r" \\")
    body.extend([r"\bottomrule", r"\end{tabular}%", "}", f"\\end{{{env}}}"])
    metadata = {
        "id": key, "source": str(source.relative_to(REPO)).replace("\\", "/"),
        "source_sha256": digest(source), "data_payload_sha256": sha256_text(json.dumps(payload, ensure_ascii=False, separators=(",", ":"))),
        "row_count": len(rows), "columns": keys, "width_class": width_class,
        "display_precision": display_precision,
    }
    return "\n".join(body), metadata


def figure_tex(key: str, spec: dict, lang: str) -> str:
    caption = spec["caption"]["en"]
    if lang == "bilingual":
        caption += " / " + spec["caption"]["zh"]
    return "\n".join([
        r"\begin{figure}[!t]", r"\centering",
        f"\\includegraphics[width=\\columnwidth]{{figures/{key}.png}}",
        "\\caption{" + latex_escape(caption) + "}", f"\\label{{fig:{key}}}", r"\end{figure}",
    ])


def bib_keys(path: Path) -> set[str]:
    return set(BIB_KEY.findall(path.read_text(encoding="utf-8-sig")))


def render_author_block(config: dict, mode: str) -> str:
    if mode == "anonymous_placeholder":
        return r"\author{\IEEEauthorblockN{Anonymous Authors}}"
    authors = config.get("authors") or []
    if not authors:
        raise BuildError("camera_ready mode requires configured authors")
    names = [author.get("name", "").strip() for author in authors]
    affiliations = [author.get("affiliation", "").strip() for author in authors]
    if not all(names) or not all(affiliations):
        raise BuildError("camera_ready authors require name and affiliation")
    return "\\author{\\IEEEauthorblockN{" + latex_escape(", ".join(names)) + "}\\\\\n\\IEEEauthorblockA{" + latex_escape("; ".join(affiliations)) + "}}"


def language_setup(lang: str, config: dict) -> str:
    if lang == "en":
        return ""
    configured = config.get("bilingual_cjk_font", "AUTO")
    if configured == "AUTO":
        candidates = config.get("bilingual_cjk_font_candidates", [])
        if not candidates or not all(isinstance(value, str) and value.strip() for value in candidates):
            raise BuildError("AUTO CJK font selection requires non-empty font-family candidates")
        selection = r"\PackageError{llamarec}{No supported CJK font found}{Configure bilingual_cjk_font with a portable font family}"
        for family in reversed(candidates):
            escaped = latex_escape(family)
            selection = f"\\IfFontExistsTF{{{escaped}}}{{\\setCJKmainfont{{{escaped}}}}}{{{selection}}}"
    else:
        if not isinstance(configured, str) or not configured.strip() or re.search(r"[/\\]|^[A-Za-z]:", configured):
            raise BuildError("bilingual_cjk_font must be a portable font-family name")
        selection = "\\setCJKmainfont{" + latex_escape(configured) + "}"
    return "\n".join([
        r"\usepackage{fontspec}", r"\usepackage{xeCJK}",
        selection,
        r"\newcommand{\llamarecEN}{\par\smallskip\noindent\textbf{EN}\quad}",
        r"\newcommand{\llamarecZH}{\par\smallskip\noindent\textbf{ZH}\quad}",
    ])


def inspect_compile_log(build_dir: Path) -> dict:
    log = build_dir / "main.log"
    text = log.read_text(encoding="utf-8", errors="replace") if log.is_file() else ""
    patterns = {
        "overfull_hboxes": r"Overfull \\hbox", "underfull_hboxes": r"Underfull \\hbox",
        "overfull_vboxes": r"Overfull \\vbox", "underfull_vboxes": r"Underfull \\vbox",
        "undefined_citations": r"Citation .* undefined", "undefined_references": r"Reference .* undefined",
        "missing_style": r"I couldn't open style file|not found: IEEEtran\.bst",
        "missing_characters": r"Missing character:", "duplicate_labels": r"multiply defined",
        "float_only_pages": r"contains only floats", "unprocessed_floats": r"Too many unprocessed floats",
    }
    return {name: len(re.findall(pattern, text)) for name, pattern in patterns.items()}


def latexmk_is_usable(path: str | None) -> bool:
    if not path:
        return False
    try:
        probe = subprocess.run(
            [path, "--version"], text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            encoding="utf-8", errors="replace", timeout=15, check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return False
    return probe.returncode == 0


def tex_engine_command(path: str, source: str = "main.tex") -> list[str]:
    command = [path]
    if any(marker in path.lower() for marker in ("miktex", "miketex")):
        command.append("--disable-installer")
    command.extend(["-interaction=nonstopmode", "-halt-on-error", source])
    return command


def compile_build(build_dir: Path, lang: str) -> dict:
    engine = "pdflatex" if lang == "en" else "xelatex"
    engine_path = shutil.which(engine)
    latexmk = shutil.which("latexmk")
    latexmk_usable = latexmk_is_usable(latexmk)
    if not engine_path and not latexmk_usable:
        reason = "LATEX_TOOLCHAIN_UNAVAILABLE" if lang == "en" else "BILINGUAL_COMPILE_PENDING_CJK_ENV"
        return {"status": "COMPILE_PENDING", "engine": engine, "reason": reason, "page_count": None, "warnings": {}}
    if latexmk_usable:
        command = [latexmk, "-pdf" if lang == "en" else "-xelatex", "-interaction=nonstopmode", "-halt-on-error", "main.tex"]
        runs = [command]
        driver = "latexmk"
    else:
        if not engine_path:
            return {"status": "COMPILE_PENDING", "engine": engine, "reason": "LATEX_ENGINE_UNAVAILABLE", "page_count": None, "warnings": {}}
        engine_command = tex_engine_command(engine_path)
        runs = [engine_command]
        bibtex = shutil.which("bibtex")
        if not bibtex:
            return {"status": "COMPILE_PENDING", "engine": engine, "reason": "BIBTEX_UNAVAILABLE", "page_count": None, "warnings": {}}
        runs.append([bibtex, "main"])
        runs.extend([engine_command] * 2)
        driver = "explicit_engine_bibtex"
    transcripts = []
    for command in runs:
        proc = subprocess.run(command, cwd=build_dir, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding="utf-8", errors="replace", check=False)
        transcripts.append(proc.stdout)
        if proc.returncode:
            return {"status": "COMPILE_FAILED", "engine": engine, "driver": driver, "latexmk_probe": "USABLE" if latexmk_usable else "UNUSABLE_OR_MISSING", "reason": f"EXIT_{proc.returncode}", "page_count": None, "warnings": inspect_compile_log(build_dir)}
    pdf = build_dir / "main.pdf"
    pages = None
    if pdf.is_file():
        try:
            from pypdf import PdfReader
            pages = len(PdfReader(str(pdf)).pages)
        except (ImportError, OSError):
            pages = None
    return {"status": "COMPILED", "engine": engine, "driver": driver, "latexmk_probe": "USABLE" if latexmk_usable else "UNUSABLE_OR_MISSING", "reason": None, "page_count": pages, "warnings": inspect_compile_log(build_dir)}


def validate_build(build_dir: Path, lang: str, expected_sections: list[str], expected_tables: set[str], expected_figures: set[str], paragraph_count: int) -> dict:
    tex_paths = sorted(build_dir.rglob("*.tex"))
    combined = "\n".join(path.read_text(encoding="utf-8") for path in tex_paths)
    failures: list[str] = []
    inputs = re.findall(r"\\input\{([^}]+)\}", combined)
    for value in inputs:
        if not (build_dir / (value + ".tex")).is_file():
            failures.append(f"missing input: {value}")
    for value in re.findall(r"\\includegraphics(?:\[[^]]*\])?\{([^}]+)\}", combined):
        if not (build_dir / value).is_file():
            failures.append(f"missing figure: {value}")
    cited = {key for group in re.findall(r"\\cite\{([^}]+)\}", combined) for key in group.split(",")}
    unknown_citations = sorted(cited - bib_keys(build_dir / "library.bib"))
    if unknown_citations:
        failures.append("unknown citations: " + ", ".join(unknown_citations))
    labels = set(re.findall(r"\\label\{([^}]+)\}", combined))
    refs = set(re.findall(r"\\ref\{([^}]+)\}", combined))
    if refs - labels:
        failures.append("undefined refs: " + ", ".join(sorted(refs - labels)))
    table_labels = {value[4:] for value in labels if value.startswith("tab:")}
    figure_labels = {value[4:] for value in labels if value.startswith("fig:")}
    if table_labels != expected_tables:
        failures.append(f"table IDs differ: {sorted(table_labels ^ expected_tables)}")
    if figure_labels != expected_figures:
        failures.append(f"figure IDs differ: {sorted(figure_labels ^ expected_figures)}")
    main = (build_dir / "main.tex").read_text(encoding="utf-8")
    actual_sections = [Path(value).name.split("_", 1)[1] for value in re.findall(r"\\input\{sections/(\d\d_[^}]+)\}", main) if not value.startswith("00_")]
    if actual_sections != expected_sections:
        failures.append(f"section order differs: {actual_sections}")
    if main.count(r"\input{sections/00_abstract}") != 1 or main.count(r"\bibliography{library}") != 1:
        failures.append("abstract or bibliography occurrence differs")
    for token in FORBIDDEN:
        if token in combined:
            failures.append(f"internal token leaked: {token}")
    if ASSET.search(combined) or CITATION.search(combined):
        failures.append("unconverted source marker remains")
    if lang == "en" and CJK.search(combined):
        failures.append("CJK text leaked into English build")
    if lang == "bilingual":
        en_positions = [match.start() for match in re.finditer(r"\\llamarecEN\{\}", combined)]
        zh_positions = [match.start() for match in re.finditer(r"\\llamarecZH\{\}", combined)]
        if len(en_positions) != paragraph_count or len(zh_positions) != paragraph_count:
            failures.append(f"bilingual pair count differs: EN={len(en_positions)}, ZH={len(zh_positions)}, expected={paragraph_count}")
        sequence = re.findall(r"\\llamarec(EN|ZH)\{\}", combined)
        if sequence != [item for _ in range(paragraph_count) for item in ("EN", "ZH")]:
            failures.append("bilingual paragraphs are not strictly interleaved")
    if failures:
        raise BuildError("Static validation failed:\n- " + "\n- ".join(failures))
    return {
        "status": "PASSED", "tex_file_count": len(tex_paths), "citation_keys": sorted(cited),
        "labels": sorted(labels), "references": sorted(refs), "checks": [
            "inputs", "figures", "citations", "references", "section_order", "single_abstract",
            "single_bibliography", "internal_markers", "language_isolation", "asset_ids", "paragraph_pairs",
        ],
    }


def build_submission(lang: str, output_root: Path = DEFAULT_BUILD_ROOT, mode: str | None = None, compile_pdf: bool = False) -> dict:
    if lang not in {"en", "bilingual"}:
        raise BuildError(f"Unsupported build language: {lang}")
    config = load_yaml(CONFIG_PATH)
    manifest = load_yaml(MANIFEST_PATH)
    mode = mode or config["mode"]
    section_order = config["section_order"]
    modules = {module["id"]: module for module in manifest["modules"]}
    missing = set(section_order + ["abstract"]) - set(modules)
    if missing:
        raise BuildError("Missing manuscript modules: " + ", ".join(sorted(missing)))
    build_dir = Path(output_root).resolve() / lang
    builds_root = (REPO / "paper" / "builds").resolve()
    if not build_dir.is_relative_to(builds_root):
        raise BuildError("Output must remain under paper/builds")
    if build_dir.exists():
        shutil.rmtree(build_dir)
    for directory in ("sections", "generated_tables", "generated_figures", "figures"):
        (build_dir / directory).mkdir(parents=True, exist_ok=True)

    reader = RecordingSourceReader(REPO, manifest, lang, "draft")
    rendered_sections = []
    aggregate_citations: set[str] = set()
    aggregate_refs: set[str] = set()
    aggregate_labels: set[str] = set()
    aggregate_equations: list[str] = []

    def render_module(module_id: str, drop_first_heading: bool = False) -> str:
        module = modules[module_id]
        before = len(reader.ordered_document_ids)
        markdown = reader.read(module["source"], expected_id=module_id, title_override=module.get("title_override"))
        ids = reader.ordered_document_ids[before:]
        renderer = LatexRenderer(lang, ids)
        result = renderer.render(markdown, drop_first_heading=drop_first_heading)
        aggregate_citations.update(renderer.citation_keys)
        aggregate_refs.update(renderer.reference_labels)
        aggregate_labels.update(renderer.defined_labels)
        aggregate_equations.extend(renderer.equation_ids)
        return result

    abstract_body = render_module("abstract", drop_first_heading=True)
    write_text(build_dir / "sections" / "00_abstract.tex", "\\begin{abstract}\n" + abstract_body + "\\end{abstract}")
    keywords = config.get("keywords", {}).get(lang if lang == "en" else "en", [])
    if keywords:
        keyword_text = ", ".join(keywords)
    else:
        keyword_text = "Keywords pending user decision."
        if lang == "bilingual":
            keyword_text += " / 关键词待用户确定。"
    write_text(build_dir / "sections" / "00_keywords.tex", "\\begin{IEEEkeywords}\n" + latex_escape(keyword_text) + "\n\\end{IEEEkeywords}")
    for index, module_id in enumerate(section_order, 1):
        rendered = render_module(module_id)
        name = f"{index:02d}_{module_id}"
        write_text(build_dir / "sections" / f"{name}.tex", rendered)
        rendered_sections.append(name)

    table_manifest = []
    display_precision = config.get("table_numeric_display_precision")
    if not isinstance(display_precision, int) or not 0 <= display_precision <= 10:
        raise BuildError("table_numeric_display_precision must be an integer from 0 to 10")
    for key, spec in manifest.get("tables", {}).items():
        rendered, metadata = table_tex(
            key, spec, lang, config["table_width_class"].get(key, "NEEDS_COMPILE_CHECK"), display_precision
        )
        write_text(build_dir / "generated_tables" / f"{key}.tex", rendered)
        table_manifest.append(metadata)
        aggregate_labels.add(f"tab:{key}")
    figure_manifest = []
    for key, spec in manifest.get("figures", {}).items():
        source = contained_path(REPO / "paper", spec["source"])
        target = build_dir / "figures" / f"{key}.png"
        shutil.copyfile(source, target)
        write_text(build_dir / "generated_figures" / f"{key}.tex", figure_tex(key, spec, lang))
        figure_manifest.append({
            "id": key, "source": str(source.relative_to(REPO)).replace("\\", "/"),
            "source_sha256": digest(source), "generated_sha256": digest(target),
            "width_class": config["figure_width_class"].get(key, "NEEDS_COMPILE_CHECK"),
        })
        aggregate_labels.add(f"fig:{key}")

    shutil.copyfile(IEEE_CLASS_PATH, build_dir / "IEEEtran.cls")
    shutil.copyfile(BIB_PATH, build_dir / "library.bib")
    title = latex_escape(config["title"]["en"])
    if lang == "bilingual":
        title += r"\\{\large " + latex_escape(config["title"]["zh"]) + "}"
    references_setup = r"\renewcommand{\refname}{References / 参考文献}" if lang == "bilingual" else ""
    main = MAIN_TEMPLATE_PATH.read_text(encoding="utf-8")
    replacements = {
        "@@LANGUAGE_SETUP@@": language_setup(lang, config), "@@TITLE@@": title,
        "@@AUTHOR_BLOCK@@": render_author_block(config, mode),
        "@@SECTION_INPUTS@@": "\n".join(f"\\input{{sections/{name}}}" for name in rendered_sections),
        "@@REFERENCES_SETUP@@": references_setup,
    }
    for marker, value in replacements.items():
        main = main.replace(marker, value)
    if re.search(r"@@[A-Z_]+@@", main):
        raise BuildError("Unresolved main template placeholder")
    write_text(build_dir / "main.tex", main)

    english_payload = [(key, value["en"]) for key, value in reader.paragraph_records.items()]
    result = {
        "schema_version": 1, "variant": lang, "mode": mode, "template": config["template"],
        "template_version": config["template_version"], "source_of_truth": "paper/modules and paper/modules_parts Markdown",
        "section_order": section_order, "paragraph_count": len(reader.paragraph_records),
        "paragraph_ids": list(reader.paragraph_records),
        "english_paragraph_sha256": sha256_text(json.dumps(english_payload, ensure_ascii=False, separators=(",", ":"))),
        "source_files_sha256": reader.sources, "manifest_sha256": digest(MANIFEST_PATH),
        "config_sha256": digest(CONFIG_PATH), "library_bib_sha256": digest(BIB_PATH),
        "ieeetran_class_sha256": digest(IEEE_CLASS_PATH), "citation_keys": sorted(aggregate_citations),
        "reference_labels": sorted(aggregate_refs), "defined_source_labels": sorted(aggregate_labels),
        "equation_ids": aggregate_equations, "tables": table_manifest, "figures": figure_manifest,
        "table_numeric_display_precision": display_precision,
        "bilingual_cjk_font": config.get("bilingual_cjk_font") if lang == "bilingual" else None,
        "bilingual_cjk_font_candidates": config.get("bilingual_cjk_font_candidates", []) if lang == "bilingual" else [],
        "unknown_submission_parameters": {
            key: config[key] for key in (
                "venue", "track", "anonymous_policy", "page_limit_reference_policy", "appendix_policy",
                "supplement_policy", "abstract_word_limit",
            )
        },
        "keywords_status": "USER_DECISION_REQUIRED" if not config.get("keywords", {}).get("en") else "CONFIGURED",
        "bibliography_style": {"name": "IEEEtran", "bundled": False, "status": "RUNTIME_DEPENDENCY_UNRESOLVED_LOCALLY"},
    }
    result["static_validation"] = validate_build(
        build_dir, lang, section_order, set(manifest.get("tables", {})), set(manifest.get("figures", {})), len(reader.paragraph_records)
    )
    result["compile"] = compile_build(build_dir, lang) if compile_pdf else {
        "status": "NOT_REQUESTED", "engine": "pdflatex" if lang == "en" else "xelatex", "reason": None,
        "page_count": None, "warnings": {},
    }
    write_text(build_dir / "build_manifest.json", json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a generic IEEE LaTeX submission package")
    parser.add_argument("--lang", choices=["en", "bilingual"], required=True)
    parser.add_argument("--mode", choices=["anonymous_placeholder", "camera_ready"])
    parser.add_argument("--output-root", type=Path, default=DEFAULT_BUILD_ROOT)
    parser.add_argument("--compile", action="store_true", dest="compile_pdf")
    args = parser.parse_args()
    try:
        result = build_submission(args.lang, args.output_root, args.mode, args.compile_pdf)
    except (AssemblyError, BuildError, OSError, KeyError, TypeError, ValueError) as exc:
        parser.exit(2, f"IEEE build failed: {exc}\n")
    print(f"Generated {args.lang}: {result['paragraph_count']} paragraphs, {len(result['tables'])} tables, {len(result['figures'])} figures")
    print(f"Static validation: {result['static_validation']['status']}")
    print(f"Compile: {result['compile']['status']} ({result['compile']['reason'] or 'no issue'})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
