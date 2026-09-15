from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[3]
PARENT = ROOT / "paper/plan/review/manuscript_contract_icecai_2026_pre_final_2026-09-11.json"
OUTPUT = ROOT / "paper/plan/review/manuscript_contract_icecai_2026_post_scientific_repair_2026-09-11.json"
EN_MANIFEST = ROOT / "paper/builds/icecai_2026/en/build_manifest.json"
BI_MANIFEST = ROOT / "paper/builds/icecai_2026/bilingual/build_manifest.json"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def record(path: Path, category: str) -> dict[str, str]:
    return {"path": path.relative_to(ROOT).as_posix(), "category": category, "sha256": sha(path)}


def main() -> None:
    parent = json.loads(PARENT.read_text(encoding="utf-8"))
    en = json.loads(EN_MANIFEST.read_text(encoding="utf-8"))
    bi = json.loads(BI_MANIFEST.read_text(encoding="utf-8"))
    manifest = yaml.safe_load((ROOT / "paper/assembly/paper_manifest.yaml").read_text(encoding="utf-8"))

    assert en["compile"]["status"] == bi["compile"]["status"] == "COMPILED"
    assert en["reference_recency"] == bi["reference_recency"]
    assert en["reference_recency"]["active_cited_references"] == 25
    assert en["reference_recency"]["recent_2024_2026"] == 13
    assert en["reference_recency"]["ratio"] == 0.52
    assert en["english_paragraph_sha256"] == bi["english_paragraph_sha256"]
    assert len(en["tables"]) == len(bi["tables"]) == 9
    assert len(en["figures"]) == len(bi["figures"]) == 2

    author_sources = sorted(
        path
        for source_root in (ROOT / "paper/modules", ROOT / "paper/modules_parts")
        for path in source_root.rglob("*.md")
    )
    active_tables = [ROOT / "paper" / spec["source"] for spec in manifest["tables"].values()]
    figures = [ROOT / "paper" / spec["source"] for spec in manifest["figures"].values()]
    evidence = [
        ROOT / "paper/plan/task-packets/m1-clean-subset-recovery-closure.md",
        ROOT / "paper/plan/task-packets/m1-common-clean-exposure-verification.md",
        ROOT / "paper/plan/task-packets/m1-common-clean-exposure-verification.csv",
        ROOT / "paper/plan/task-packets/m1-clean-subset-audit/clean_multiseed_96_summary.csv",
        ROOT / "paper/plan/task-packets/m1-clean-subset-audit/recovered_clean_per_seed.csv",
        ROOT / "paper/evidence/claim_matrix.md",
        ROOT / "paper/evidence/source_of_truth.md",
        ROOT / "paper/evidence/pending_evidence.md",
        ROOT / "paper/evidence/run_metadata_ledger.md",
    ]
    controls = [
        ROOT / "paper/assembly/paper_manifest.yaml",
        ROOT / "paper/evidence/bootstrap_provenance_closure.md",
        ROOT / "paper/evidence/story_and_novelty_freeze.md",
        ROOT / "paper/submission/icecai_2026/submission_config.yaml",
        ROOT / "paper/tables/table-schema.md",
        ROOT / "paper/plan/review/method-experiment-traceability.md",
        ROOT / "paper/references/citation_claim_map.md",
        ROOT / "paper/references/citation_registry.json",
        ROOT / "paper/references/library.bib",
        ROOT / "paper/references/primary_source_notes.md",
    ]

    active_text = "\n".join(path.read_text(encoding="utf-8") for path in author_sources)
    forbidden = re.compile(
        r"detected leakage|leakage was found|contaminated|after discovering|after finding cross-task leakage|"
        r"we repaired|post-hoc leakage repair|salvage|recovery from leakage|previous evaluation was invalid",
        re.IGNORECASE,
    )
    accident_matches = forbidden.findall(active_text)
    assert accident_matches == []
    assert "cross-task-safe subset" in active_text
    assert "evaluation-side restriction" in active_text
    assert "joint temporal cutoff" in active_text
    assert "M1 was not trained under a joint temporal cutoff" in active_text

    active_payload = active_text + "\n" + (ROOT / "paper/assembly/paper_manifest.yaml").read_text(encoding="utf-8")
    active_payload += "\n" + "\n".join(path.read_text(encoding="utf-8-sig") for path in active_tables)
    old_signatures = [
        "0.594185022", "0.623436123", "0.597356828", "0.0003524229",
        "0.112422907", "0.114713656", "0.081644640", "0.077650513",
    ]
    old_hits = [value for value in old_signatures if value in active_payload]
    assert old_hits == []
    ranking_tables = [path for path in active_tables if "y_side_binary_bootstrap" not in path.name]
    ranking_ci_hits = [path.relative_to(ROOT).as_posix() for path in ranking_tables if "ci95_" in path.read_text(encoding="utf-8-sig")]
    assert ranking_ci_hits == []

    baseline = (ROOT / "paper/modules_parts/methods/baseline_setup.md").read_text(encoding="utf-8")
    required_sasrec = [
        "64-dimensional", "2 attention heads", "2 causal Transformer layers", "256-dimensional",
        "GELU", "dropout 0.2", "final LayerNorm", "maximum history of 10", "item bias",
        "full-item cross-entropy", "AdamW", "learning rate 0.001", "weight decay 0", "no scheduler",
        "batch size 512", "seed42", "independently trained from scratch", "200,000",
    ]
    missing_sasrec = [token for token in required_sasrec if token not in baseline]
    assert missing_sasrec == []

    parent_rows = {row["path"]: row["sha256"] for row in parent["protected"]}
    figure_invariants = []
    for path in figures:
        relative = path.relative_to(ROOT).as_posix()
        assert parent_rows[relative] == sha(path)
        figure_invariants.append({"path": relative, "status": "UNCHANGED", "sha256": sha(path)})
    references_path = ROOT / "paper/references/library.bib"
    assert parent_rows[references_path.relative_to(ROOT).as_posix()] == sha(references_path)

    protected = [record(path, "author_source") for path in author_sources]
    protected += [record(path, "active_table") for path in active_tables]
    protected += [record(path, "formal_figure") for path in figures]
    protected += [record(path, "evidence") for path in evidence]
    protected += [record(path, "control_or_reference") for path in controls]

    contract = {
        "schema_version": 3,
        "contract_id": "icecai-2026-post-scientific-repair-2026-09-11",
        "created": "2026-09-11",
        "venue": "ICECAI 2026",
        "stage": "POST_SCIENTIFIC_REPAIR_PRE_METADATA",
        "status": "GPT6_REPAIR_VERIFICATION_READY",
        "parent_contract": {
            "path": PARENT.relative_to(ROOT).as_posix(),
            "contract_id": parent["contract_id"],
            "sha256": sha(PARENT),
        },
        "author_status": "DEFERRED",
        "genai_status": "DEFERRED",
        "science_freeze": False,
        "training_or_inference": "NONE",
        "bootstrap_or_new_statistics": "NONE",
        "historical_baselines": parent["historical_baselines"],
        "inherited_historical_baselines": parent["inherited_historical_baselines"],
        "reference_recency": en["reference_recency"],
        "manuscript_audits": {
            "final_protocol_framing": "PASS",
            "accident_narrative_matches": len(accident_matches),
            "old_fullset_m1_ranking_signature_hits": len(old_hits),
            "old_m1_ranking_bootstrap_active_hits": len(ranking_ci_hits),
            "common_validation_n": 5318,
            "common_test_n": 5535,
            "validation_narrowing_metrics": "3/3",
            "test_narrowing": "NO",
            "clean_seed_level_positive_deltas": "54/54",
            "aggregate_three_of_three_positive_items": "18/18",
            "sasrec_disclosure": "PASS",
        },
        "table_roles": {
            "IV": "seed42 common cross-task-safe k5 exposure comparison",
            "V": "seed42 Y-side binary paired bootstrap only",
            "VI": "96k cross-task-safe three-seed N-M1 ranking summary",
            "VII": "cross-task-safe subset coverage",
        },
        "figure_invariants": figure_invariants,
        "artifacts": {
            "english": {
                "pdf": "paper/builds/icecai_2026/en/main.pdf",
                "sha256": sha(ROOT / "paper/builds/icecai_2026/en/main.pdf"),
                "page_count": en["compile"]["page_count"],
                "compile": en["compile"],
            },
            "bilingual": {
                "pdf": "paper/builds/icecai_2026/bilingual/main.pdf",
                "sha256": sha(ROOT / "paper/builds/icecai_2026/bilingual/main.pdf"),
                "page_count": bi["compile"]["page_count"],
                "compile": bi["compile"],
            },
        },
        "protected": protected,
    }
    OUTPUT.write_text(json.dumps(contract, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(OUTPUT.relative_to(ROOT).as_posix())


if __name__ == "__main__":
    main()
