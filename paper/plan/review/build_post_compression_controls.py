from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SNAPSHOT = ROOT / "paper/archive/manuscript/pre_compression_2026-09-10"
OLD_CONTRACT = ROOT / "paper/plan/review/manuscript_contract_2026-09-10.json"
PARAGRAPH_MAP = ROOT / "paper/plan/review/compression_paragraph_mapping_2026-09-10.json"
TABLE_MAP = ROOT / "paper/plan/review/compression_table_mapping_2026-09-10.json"
POST_CONTRACT = ROOT / "paper/plan/review/manuscript_contract_post_compression_2026-09-10.json"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def active_paragraphs() -> dict[str, dict[str, str]]:
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

    manifest = parse_yaml((ROOT / "paper/assembly/paper_manifest.yaml").read_text(encoding="utf-8-sig"))
    by_language = {}
    for language in ("en", "zh"):
        reader = CapturingReader(ROOT, manifest, language, "draft")
        for module in manifest["modules"]:
            if module["id"] != "contributions":
                reader.read(module["source"], expected_id=module["id"])
        by_language[language] = reader.texts
    return {
        identifier: {language: by_language[language][identifier] for language in ("en", "zh")}
        for identifier in by_language["en"]
    }


def archived_paragraphs() -> dict[str, dict[str, str]]:
    paragraphs: dict[str, dict[str, str]] = {}
    pattern = re.compile(
        r"<!-- PARAGRAPH:\s*([^\s]+)\s*-->.*?\*\*EN\*\*\s*(.*?)\s*\*\*ZH\*\*\s*(.*?)(?=<!-- PARAGRAPH:|\Z)",
        re.DOTALL,
    )
    for path in (SNAPSHOT / "source").rglob("*.md"):
        for identifier, english, chinese in pattern.findall(path.read_text(encoding="utf-8-sig")):
            paragraphs[identifier] = {"en": english.strip(), "zh": chinese.strip()}
    return paragraphs


def sync_literature_wording(current: dict[str, dict[str, str]]) -> None:
    path = ROOT / "paper/references/literature_gap_registry.json"
    registry = json.loads(path.read_text(encoding="utf-8"))
    for row in registry["gaps"]:
        identifier = row["paragraphs"][0]
        row["final_wording_en"] = current[identifier]["en"]
        row["final_wording_zh"] = current[identifier]["zh"]
    write_json(path, registry)


def build_paragraph_mapping(old: dict, current: dict) -> None:
    old_ids = json.loads(
        (ROOT / "paper/builds/ieee_generic/en/build_manifest.json").read_text(encoding="utf-8")
    )["paragraph_ids"]
    merges = {
        "results.rq4.p03": "results.rq4.p02",
        "discussion.unification.p01": "discussion.exposure.p03",
        "discussion.unification.p02": "discussion.exposure.p03",
        "discussion.external.p02": "discussion.external.p01",
        "conclusion.p03": "conclusion.p02",
        "conclusion.p04": "conclusion.p03",
    }
    rows = []
    for identifier in old_ids:
        target = merges.get(identifier, identifier if identifier in current else None)
        if identifier in merges:
            action = "MERGED_INTO"
        elif target is None:
            action = "REMOVED_REDUNDANT_COMPONENT"
        elif old[identifier] == current[target]:
            action = "UNCHANGED"
        else:
            action = "TIGHTENED"
        rows.append(
            {
                "old_id": identifier,
                "new_id": target,
                "action": action,
                "old_en_sha256": hashlib.sha256(old[identifier]["en"].encode()).hexdigest(),
                "old_zh_sha256": hashlib.sha256(old[identifier]["zh"].encode()).hexdigest(),
                "new_en_sha256": hashlib.sha256(current[target]["en"].encode()).hexdigest() if target else None,
                "new_zh_sha256": hashlib.sha256(current[target]["zh"].encode()).hexdigest() if target else None,
            }
        )
    write_json(
        PARAGRAPH_MAP,
        {
            "schema_version": 1,
            "parent_snapshot": "pre_compression_2026-09-10",
            "old_submission_paragraph_count": len(old_ids),
            "new_submission_paragraph_count": len(current),
            "scientific_claims_deleted": False,
            "mapping": rows,
        },
    )


def build_table_mapping() -> None:
    archive = json.loads(
        (ROOT / "paper/archive/tables/pre_compression_2026-09-10/manifest.json").read_text(encoding="utf-8")
    )
    specs = {
        "datasets": ("datasets", "paper/tables/datasets.csv", "I", "CORE_MAIN", ["dataset scope and split counts"]),
        "training_exposure": ("training_exposure_compact", "paper/tables/compression_2026-09-10/training_exposure_compact.csv", "II", "REPLACED_IN_MAIN", ["optimizer steps", "task-sample exposure"]),
        "binary_exposure": ("supervision_semantics_compact", "paper/tables/compression_2026-09-10/supervision_semantics_compact.csv", "III", "MERGED_INTO", ["Y-native exposure response"]),
        "semantics_bridge": ("supervision_semantics_compact", "paper/tables/compression_2026-09-10/supervision_semantics_compact.csv", "III", "MERGED_INTO", ["Y bridge ranking", "N96 native ranking"]),
        "exposure_scaling": ("exposure_scaling", "paper/tables/exposure_scaling.csv", "IV", "CORE_MAIN", ["N exposure trajectory"]),
        "specialist_multitask": ("specialist_multitask", "paper/tables/specialist_multitask.csv", "V", "CORE_MAIN", ["matched-exposure specialist/shared comparison"]),
        "ms96_main_validation": ("ms96_delta_summary_compact", "paper/tables/compression_2026-09-10/ms96_delta_summary_compact.csv", "VI", "REMOVED_FROM_MAIN; RAW_ARCHIVED", ["96k validation three-seed deltas"]),
        "ms96_main_test": ("ms96_delta_summary_compact; hard_candidate_compact", "paper/tables/compression_2026-09-10/ms96_delta_summary_compact.csv; paper/tables/compression_2026-09-10/hard_candidate_compact.csv", "VI; VII", "REMOVED_FROM_MAIN; RAW_ARCHIVED", ["96k test three-seed deltas", "seed42 paired intervals"]),
        "ms96_delta_summary": ("ms96_delta_summary_compact", "paper/tables/compression_2026-09-10/ms96_delta_summary_compact.csv", "VI", "REPLACED_IN_MAIN", ["mean", "sample SD", "direction by training seed"]),
        "hard_candidate": ("hard_candidate_compact", "paper/tables/compression_2026-09-10/hard_candidate_compact.csv", "VII", "REPLACED_IN_MAIN", ["seed42 paired bootstrap interval status"]),
        "ms96_protocol_validation": ("ms96_delta_summary_compact; hard_candidate_compact", "paper/tables/compression_2026-09-10/ms96_delta_summary_compact.csv; paper/tables/compression_2026-09-10/hard_candidate_compact.csv", "VI; VII", "REMOVED_FROM_MAIN; RAW_ARCHIVED", ["validation protocol robustness"]),
        "ms96_protocol_test": ("ms96_delta_summary_compact; hard_candidate_compact", "paper/tables/compression_2026-09-10/ms96_delta_summary_compact.csv; paper/tables/compression_2026-09-10/hard_candidate_compact.csv", "VI; VII", "REMOVED_FROM_MAIN; RAW_ARCHIVED", ["test protocol robustness"]),
        "n_vs_sasrec_exposure": ("n_vs_sasrec_exposure", "paper/tables/n_vs_sasrec_exposure.csv", "VIII", "CORE_MAIN", ["approximately exposure-aligned LlamaRec/SASRec comparison"]),
        "cross_dataset": ("cross_dataset", "paper/tables/cross_dataset.csv", "IX", "CORE_MAIN", ["Amazon directional external check"]),
    }
    rows = []
    for item in archive["tables"]:
        new_id, new_csv, number, status, claims = specs[item["table_id"]]
        new_sources = [part.strip() for part in new_csv.split(";")]
        rows.append(
            {
                "old_logical_table": item["table_id"],
                "old_pdf_table_number": item["current_pdf_table_number"],
                "old_csv": item["active_source_path"],
                "old_source_sha256": item["sha256"],
                "archive_path": item["archive_path"],
                "new_logical_table": new_id,
                "new_csv": new_csv,
                "new_source_sha256": {p: sha(ROOT / p) for p in new_sources},
                "new_pdf_table_number": number,
                "status": status,
                "evidence_summarized_by": new_id,
                "claim_coverage": claims,
            }
        )
    write_json(
        TABLE_MAP,
        {
            "schema_version": 1,
            "parent_table_snapshot": "paper/archive/tables/pre_compression_2026-09-10",
            "old_table_count": 14,
            "new_main_table_count": 9,
            "old_csv_deleted_or_overwritten": False,
            "mapping": rows,
        },
    )


def build_contract() -> None:
    author_sources = sorted(
        p for root in (ROOT / "paper/modules", ROOT / "paper/modules_parts") for p in root.rglob("*.md")
    )
    table_sources = [
        "paper/tables/datasets.csv",
        "paper/tables/compression_2026-09-10/training_exposure_compact.csv",
        "paper/tables/compression_2026-09-10/supervision_semantics_compact.csv",
        "paper/tables/exposure_scaling.csv",
        "paper/tables/specialist_multitask.csv",
        "paper/tables/compression_2026-09-10/ms96_delta_summary_compact.csv",
        "paper/tables/compression_2026-09-10/hard_candidate_compact.csv",
        "paper/tables/n_vs_sasrec_exposure.csv",
        "paper/tables/cross_dataset.csv",
    ]
    figures = ["paper/figures/fig_n_native_exposure.png", "paper/figures/fig_n_vs_sasrec_exposure.png"]
    controls = [
        "paper/assembly/paper_manifest.yaml",
        "paper/evidence/bootstrap_provenance_closure.md",
        "paper/evidence/claim_matrix.md",
        "paper/evidence/pending_evidence.md",
        "paper/evidence/run_metadata_ledger.md",
        "paper/evidence/source_of_truth.md",
        "paper/evidence/story_and_novelty_freeze.md",
        "paper/references/citation_claim_map.md",
        "paper/references/citation_registry.json",
        "paper/references/literature_gap_registry.json",
        "paper/references/library.bib",
        "paper/references/primary_source_notes.md",
        "paper/tables/compression_2026-09-10/manifest.json",
        "paper/tables/compression_2026-09-10/lineage.csv",
        "paper/plan/review/compression_paragraph_mapping_2026-09-10.json",
        "paper/plan/review/compression_table_mapping_2026-09-10.json",
        "paper/plan/task-packets/compression-scientific-judge.md",
    ]
    protected = []
    for path in author_sources:
        protected.append({"path": path.relative_to(ROOT).as_posix(), "category": "author_source", "sha256": sha(path)})
    for path in table_sources:
        protected.append({"path": path, "category": "current_main_table", "sha256": sha(ROOT / path)})
    for path in figures:
        protected.append({"path": path, "category": "formal_figure", "sha256": sha(ROOT / path)})
    for path in controls:
        protected.append({"path": path, "category": "evidence_or_reference_control", "sha256": sha(ROOT / path)})
    old = json.loads(OLD_CONTRACT.read_text(encoding="utf-8"))
    write_json(
        POST_CONTRACT,
        {
            "schema_version": 1,
            "contract_id": "post-compression-2026-09-10",
            "created": "2026-09-10",
            "stage": "evidence-preserving-compression-execution",
            "purpose": "Current-state hash contract after bilingual evidence-preserving manuscript and table compression.",
            "parent_snapshot": "pre_compression_2026-09-10",
            "parent_snapshot_path": "paper/archive/manuscript/pre_compression_2026-09-10",
            "parent_snapshot_aggregate_sha256": "0dd7bfc219bb47b1fa1fc649cd71cdfa399b2955ca62e391c0a25bf08f0565b5",
            "parent_table_snapshot_path": "paper/archive/tables/pre_compression_2026-09-10",
            "parent_contract": {
                "path": OLD_CONTRACT.relative_to(ROOT).as_posix(),
                "contract_id": old["contract_id"],
                "sha256": sha(OLD_CONTRACT),
            },
            "historical_baselines": old["historical_baselines"],
            "protected": protected,
        },
    )


def main() -> None:
    current = active_paragraphs()
    old = archived_paragraphs()
    sync_literature_wording(current)
    build_paragraph_mapping(old, current)
    build_table_mapping()
    build_contract()
    print(f"paragraphs: {len(old)} archived / {len(current)} current submission")
    print("tables: 14 archived / 9 current main")
    print(POST_CONTRACT.relative_to(ROOT).as_posix())


if __name__ == "__main__":
    main()
