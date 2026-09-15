"""Build the ICECAI 2026 pre-final package without inventing user metadata."""

from __future__ import annotations

import argparse
from contextlib import contextmanager
import importlib.util
import json
import re
import sys
from pathlib import Path


LAYER_DIR = Path(__file__).resolve().parent
REPO = LAYER_DIR.parents[2]
GENERIC_DIR = REPO / "paper" / "submission" / "ieee_generic"
CONFIG_PATH = LAYER_DIR / "submission_config.yaml"
DEFAULT_BUILD_ROOT = REPO / "paper" / "builds" / "icecai_2026"

_spec = importlib.util.spec_from_file_location("llamarec_ieee_generic", GENERIC_DIR / "build_submission.py")
if _spec is None or _spec.loader is None:
    raise RuntimeError("Unable to load generic IEEE adapter")
generic = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = generic
_spec.loader.exec_module(generic)

BuildError = generic.BuildError


def render_author_block(config: dict, mode: str) -> str:
    if mode == "prefinal_placeholder":
        return r"\author{\IEEEauthorblockN{AUTHOR INFORMATION REQUIRED}}"
    if mode != "submission":
        raise BuildError(f"Unsupported ICECAI mode: {mode}")
    authors = config.get("authors") or []
    if not authors:
        raise BuildError("submission mode requires real author information")
    required = ("name", "department", "institution", "city", "country", "email")
    for index, author in enumerate(authors, 1):
        missing = [key for key in required if not str(author.get(key, "")).strip()]
        if missing:
            raise BuildError(f"author {index} is missing: {', '.join(missing)}")
        if not isinstance(author.get("corresponding"), bool):
            raise BuildError(f"author {index} corresponding must be true or false")
    corresponding = [author for author in authors if author["corresponding"]]
    if len(corresponding) != 1:
        raise BuildError("submission mode requires exactly one corresponding author")
    blocks = []
    for author in authors:
        name = generic.latex_escape(author["name"].strip())
        if author["corresponding"]:
            name += r"\textsuperscript{*}"
        affiliation = r"\\".join(
            generic.latex_escape(str(author[key]).strip())
            for key in ("department", "institution")
        )
        location = generic.latex_escape(f"{author['city'].strip()}, {author['country'].strip()}")
        email = generic.latex_escape(author["email"].strip())
        blocks.append(
            "\\IEEEauthorblockN{" + name + "}\n"
            "\\IEEEauthorblockA{" + affiliation + r"\\" + location + r"\\" + email + "}"
        )
    return "\\author{\n" + "\n\\and\n".join(blocks) + "\n}"


@contextmanager
def generic_layer_overrides():
    original = {
        "CONFIG_PATH": generic.CONFIG_PATH,
        "DEFAULT_BUILD_ROOT": generic.DEFAULT_BUILD_ROOT,
        "render_author_block": generic.render_author_block,
    }
    generic.CONFIG_PATH = CONFIG_PATH
    generic.DEFAULT_BUILD_ROOT = DEFAULT_BUILD_ROOT
    generic.render_author_block = render_author_block
    try:
        yield
    finally:
        for key, value in original.items():
            setattr(generic, key, value)


def bib_years(path: Path) -> dict[str, int]:
    text = path.read_text(encoding="utf-8-sig")
    entries = re.finditer(r"@\w+\s*\{\s*([^,\s]+)\s*,(.*?)(?=\n@|\Z)", text, re.I | re.S)
    result: dict[str, int] = {}
    for entry in entries:
        year = re.search(r"\byear\s*=\s*[\{\"](\d{4})", entry.group(2), re.I)
        if year:
            result[entry.group(1)] = int(year.group(1))
    return result


def validate_reference_compliance(result: dict, config: dict, build_dir: Path) -> tuple[dict, dict]:
    cited = set(result["citation_keys"])
    years = bib_years(build_dir / "library.bib")
    missing_year = sorted(cited - set(years))
    if missing_year:
        raise BuildError("cited references lack publication years: " + ", ".join(missing_year))
    rules = config["reference_recency"]
    recent = sorted(key for key in cited if rules["start_year"] <= years[key] <= rules["end_year"])
    ratio = len(recent) / len(cited)
    if len(cited) != rules["expected_active"] or len(recent) != rules["expected_recent"]:
        raise BuildError(
            f"reference recency count differs: active={len(cited)}, recent={len(recent)}"
        )
    recency = {
        "status": "PASS" if ratio >= rules["minimum_ratio"] else "FAIL",
        "active_cited_references": len(cited),
        "recent_2024_2026": len(recent),
        "ratio": ratio,
        "recent_citation_keys": recent,
    }
    if recency["status"] != "PASS":
        raise BuildError("reference recency requirement failed")
    country_rows = config["country_source_evidence"]
    missing_country_keys = sorted(row["citation_key"] for row in country_rows if row["citation_key"] not in cited)
    countries = sorted({row["country"] for row in country_rows})
    country = {
        "status": "PASS" if len(countries) >= 3 and not missing_country_keys else "FAIL",
        "countries": countries,
        "active_reference_evidence": country_rows,
        "missing_active_keys": missing_country_keys,
    }
    if country["status"] != "PASS":
        raise BuildError("country-source requirement failed")
    return recency, country


def render_optional_disclosure(build_dir: Path, config: dict) -> dict:
    disclosure = config.get("genai_disclosure") or {}
    enabled = disclosure.get("enabled", False)
    text = str(disclosure.get("text", "")).strip()
    if not isinstance(enabled, bool):
        raise BuildError("genai_disclosure.enabled must be true or false")
    if not enabled:
        if text:
            raise BuildError("disclosure text is present but genai_disclosure.enabled is false")
        return {"status": "USER_MANUAL_COMPLETION_REQUIRED", "enabled": False, "rendered": False}
    if not text:
        raise BuildError("enabled disclosure requires user-supplied text")
    target = build_dir / "sections" / "99_genai_disclosure.tex"
    generic.write_text(target, r"\section*{Disclosure}" + "\n" + generic.latex_escape(text))
    main_path = build_dir / "main.tex"
    main = main_path.read_text(encoding="utf-8")
    marker = r"\bibliographystyle{IEEEtran}"
    if main.count(marker) != 1:
        raise BuildError("unable to locate disclosure insertion point")
    generic.write_text(main_path, main.replace(marker, r"\input{sections/99_genai_disclosure}" + "\n" + marker))
    return {"status": "USER_SUPPLIED", "enabled": True, "rendered": True}


def build_submission(lang: str, output_root: Path = DEFAULT_BUILD_ROOT, mode: str | None = None, compile_pdf: bool = False) -> dict:
    config = generic.load_yaml(CONFIG_PATH)
    mode = mode or config["mode"]
    with generic_layer_overrides():
        result = generic.build_submission(lang, output_root, mode, compile_pdf=False)
    build_dir = Path(output_root).resolve() / lang
    disclosure = render_optional_disclosure(build_dir, config)
    recency, country = validate_reference_compliance(result, config, build_dir)
    manifest = generic.load_yaml(generic.MANIFEST_PATH)
    result["static_validation"] = generic.validate_build(
        build_dir,
        lang,
        config["section_order"],
        set(manifest.get("tables", {})),
        set(manifest.get("figures", {})),
        result["paragraph_count"],
    )
    result.update({
        "schema_version": 2,
        "venue": "ICECAI 2026",
        "stage": "venue_adapted_pre_final",
        "submission_status": "VENUE_ADAPTED_PRE_FINAL",
        "author_status": "USER_MANUAL_COMPLETION_REQUIRED" if mode == "prefinal_placeholder" else "USER_SUPPLIED",
        "genai_status": disclosure["status"],
        "genai_disclosure": disclosure,
        "word_status": "ORGANIZER_OR_PORTAL_CONFIRMATION_REQUIRED",
        "reference_recency": recency,
        "country_source_compliance": country,
        "keywords": config["keywords"]["en"],
        "keywords_status": "CONFIGURED",
        "generic_adapter_inheritance": "paper/submission/ieee_generic (unchanged)",
    })
    result["compile"] = generic.compile_build(build_dir, lang) if compile_pdf else {
        "status": "NOT_REQUESTED", "engine": "pdflatex" if lang == "en" else "xelatex",
        "reason": None, "page_count": None, "warnings": {},
    }
    generic.write_text(build_dir / "build_manifest.json", json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate the ICECAI 2026 pre-final package")
    parser.add_argument("--lang", choices=["en", "bilingual"], required=True)
    parser.add_argument("--mode", choices=["prefinal_placeholder", "submission"])
    parser.add_argument("--output-root", type=Path, default=DEFAULT_BUILD_ROOT)
    parser.add_argument("--compile", action="store_true", dest="compile_pdf")
    args = parser.parse_args()
    try:
        result = build_submission(args.lang, args.output_root, args.mode, args.compile_pdf)
    except (generic.AssemblyError, BuildError, OSError, KeyError, TypeError, ValueError) as exc:
        parser.exit(2, f"ICECAI build failed: {exc}\n")
    print(
        f"Generated {args.lang}: {result['paragraph_count']} paragraphs, "
        f"{len(result['tables'])} tables, {len(result['figures'])} figures"
    )
    print(f"Reference recency: {result['reference_recency']['recent_2024_2026']}/"
          f"{result['reference_recency']['active_cited_references']} PASS")
    print(f"Compile: {result['compile']['status']} ({result['compile']['reason'] or 'no issue'})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
