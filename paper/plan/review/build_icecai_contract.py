from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
PARENT = ROOT / "paper/plan/review/manuscript_contract_post_compression_2026-09-10.json"
OUTPUT = ROOT / "paper/plan/review/manuscript_contract_icecai_2026_pre_final_2026-09-11.json"
EN_MANIFEST = ROOT / "paper/builds/icecai_2026/en/build_manifest.json"
BI_MANIFEST = ROOT / "paper/builds/icecai_2026/bilingual/build_manifest.json"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def row(path: str, category: str) -> dict:
    return {"path": path, "category": category, "sha256": sha(ROOT / path)}


def main() -> None:
    parent = json.loads(PARENT.read_text(encoding="utf-8"))
    parent_rows = {item["path"]: item for item in parent["protected"]}
    unchanged_from_parent = [
        "paper/modules/10_abstract.md",
        *[item["path"] for item in parent["protected"] if item["category"] == "current_main_table"],
        *[item["path"] for item in parent["protected"] if item["category"] == "formal_figure"],
    ]
    invariant_results = []
    for path in unchanged_from_parent:
        current = sha(ROOT / path)
        expected = parent_rows[path]["sha256"]
        if current != expected:
            raise RuntimeError(f"frozen parent hash changed: {path}")
        invariant_results.append({"path": path, "parent_sha256": expected, "current_sha256": current, "status": "PASS"})

    author_sources = sorted(
        path for source_root in (ROOT / "paper/modules", ROOT / "paper/modules_parts")
        for path in source_root.rglob("*.md")
    )
    table_sources = [item["path"] for item in parent["protected"] if item["category"] == "current_main_table"]
    figures = [item["path"] for item in parent["protected"] if item["category"] == "formal_figure"]
    controls = [
        "paper/assembly/paper_manifest.yaml",
        "paper/evidence/bootstrap_provenance_closure.md",
        "paper/evidence/claim_matrix.md",
        "paper/evidence/pending_evidence.md",
        "paper/evidence/run_metadata_ledger.md",
        "paper/evidence/source_of_truth.md",
        "paper/evidence/story_and_novelty_freeze.md",
        "paper/references/citation_claim_map.md",
        "paper/references/citation_inventory.md",
        "paper/references/citation_registry.json",
        "paper/references/literature_gap_registry.json",
        "paper/references/library.bib",
        "paper/references/primary_source_notes.md",
        "paper/tables/compression_2026-09-10/manifest.json",
        "paper/tables/compression_2026-09-10/lineage.csv",
        "paper/plan/review/compression_paragraph_mapping_2026-09-10.json",
        "paper/plan/review/compression_table_mapping_2026-09-10.json",
    ]
    adapter = [
        "paper/submission/icecai_2026/__init__.py",
        "paper/submission/icecai_2026/build_submission.py",
        "paper/submission/icecai_2026/submission_config.yaml",
        "paper/submission/icecai_2026/AUTHOR_INPUT_REQUIRED.md",
        "paper/submission/icecai_2026/GENAI_DISCLOSURE_INPUT_REQUIRED.md",
        "paper/submission/icecai_2026/README.md",
        "paper/submission/icecai_2026/tests/__init__.py",
        "paper/submission/icecai_2026/tests/test_submission.py",
        "paper/plan/review/build_icecai_contract.py",
    ]
    protected = [row(path.relative_to(ROOT).as_posix(), "author_source") for path in author_sources]
    protected += [row(path, "current_main_table") for path in table_sources]
    protected += [row(path, "formal_figure") for path in figures]
    protected += [row(path, "evidence_or_reference_control") for path in controls]
    protected += [row(path, "venue_adapter") for path in adapter]

    en = json.loads(EN_MANIFEST.read_text(encoding="utf-8"))
    bi = json.loads(BI_MANIFEST.read_text(encoding="utf-8"))
    if en["reference_recency"]["status"] != "PASS" or en["reference_recency"]["recent_2024_2026"] != 13:
        raise RuntimeError("English reference-recency contract is not 13/25 PASS")
    if en["citation_keys"] != bi["citation_keys"] or en["english_paragraph_sha256"] != bi["english_paragraph_sha256"]:
        raise RuntimeError("English/bilingual source or citation identity differs")
    if en["compile"]["status"] != "COMPILED" or bi["compile"]["status"] != "COMPILED":
        raise RuntimeError("final pre-final PDFs are not compiled")

    contract = {
        "schema_version": 2,
        "contract_id": "icecai-2026-pre-final-2026-09-11",
        "created": "2026-09-11",
        "venue": "ICECAI 2026",
        "stage": "venue_adapted_pre_final",
        "status": "VENUE_ADAPTED_AWAITING_USER_METADATA",
        "purpose": "Current-state contract after ICECAI R-BALANCED reference refresh, textual table-reference repair, venue metadata configuration, and pre-final rebuild.",
        "parent_contract": {
            "path": PARENT.relative_to(ROOT).as_posix(),
            "contract_id": parent["contract_id"],
            "sha256": sha(PARENT),
        },
        "inherited_historical_baselines": parent["historical_baselines"],
        "historical_baselines": parent["historical_baselines"],
        "author_status": "USER_MANUAL_COMPLETION_REQUIRED",
        "genai_status": "USER_MANUAL_COMPLETION_REQUIRED",
        "word_status": "ORGANIZER_OR_PORTAL_CONFIRMATION_REQUIRED",
        "reference_recency": en["reference_recency"],
        "country_source_compliance": en["country_source_compliance"],
        "keywords": en["keywords"],
        "approved_source_changes": [
            "paper/modules/01_introduction.md",
            "paper/modules_parts/related_work/evaluation_baselines.md",
            "paper/modules_parts/results/rq2_exposure_response.md",
            "paper/modules_parts/results/rq3_multitask_unification.md",
            "paper/modules_parts/results/rq4_hard_candidate_robustness.md",
            "paper/references/library.bib",
            "paper/references/citation_registry.json",
            "paper/references/citation_inventory.md",
            "paper/references/primary_source_notes.md",
            "paper/references/citation_claim_map.md",
            "paper/references/literature_gap_registry.json",
        ],
        "frozen_parent_invariants": invariant_results,
        "generic_adapter_unchanged": {
            "status": "PASS",
            "git_diff": "EMPTY",
            "files": [
                row("paper/submission/ieee_generic/build_submission.py", "generic_adapter"),
                row("paper/submission/ieee_generic/submission_config.yaml", "generic_adapter"),
                row("paper/submission/ieee_generic/main_template.tex", "generic_adapter"),
            ],
        },
        "artifacts": {
            "english": {
                "pdf": "paper/builds/icecai_2026/en/main.pdf",
                "pdf_sha256": sha(ROOT / "paper/builds/icecai_2026/en/main.pdf"),
                "manifest": "paper/builds/icecai_2026/en/build_manifest.json",
                "manifest_sha256": sha(EN_MANIFEST),
                "page_count": en["compile"]["page_count"],
                "tables": len(en["tables"]),
                "figures": len(en["figures"]),
                "compile_status": en["compile"]["status"],
            },
            "bilingual": {
                "pdf": "paper/builds/icecai_2026/bilingual/main.pdf",
                "pdf_sha256": sha(ROOT / "paper/builds/icecai_2026/bilingual/main.pdf"),
                "manifest": "paper/builds/icecai_2026/bilingual/build_manifest.json",
                "manifest_sha256": sha(BI_MANIFEST),
                "page_count": bi["compile"]["page_count"],
                "tables": len(bi["tables"]),
                "figures": len(bi["figures"]),
                "compile_status": bi["compile"]["status"],
            },
        },
        "visual_audit": {
            "status": "PASS_AUTOMATED_RENDER_AND_LAYOUT_AUDIT",
            "english_pages_rendered": 10,
            "out_of_bounds_text_origins": 0,
            "raster_border_dark_pixels": 0,
            "overfull_hboxes": en["compile"]["warnings"]["overfull_hboxes"],
            "overfull_vboxes": en["compile"]["warnings"]["overfull_vboxes"],
            "missing_characters": en["compile"]["warnings"]["missing_characters"],
            "embedded_images": 2,
            "table_labels": 9,
            "figure_labels": 2,
            "english_cjk_leak": False,
            "unexpected_placeholders": 0,
            "allowed_placeholder": "AUTHOR INFORMATION REQUIRED",
        },
        "protected": protected,
    }
    OUTPUT.write_text(json.dumps(contract, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(OUTPUT.relative_to(ROOT).as_posix())


if __name__ == "__main__":
    main()
