from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
PARENT = ROOT / "paper/plan/review/manuscript_contract_icecai_2026_post_scientific_repair_2026-09-11.json"
INTERMEDIATE = ROOT / "paper/plan/review/manuscript_contract_icecai_2026_post_stale_cleanup_2026-09-11.json"
OUTPUT = ROOT / "paper/plan/review/manuscript_contract_icecai_2026_science_frozen_pre_metadata_2026-09-11.json"
PACKET = ROOT / "paper/plan/task-packets/icecai-gpt6-p1-closure-packet.md"
REPORT = ROOT / "paper/plan/task-packets/icecai-gpt6-p1-closure-report.md"
EN_MANIFEST = ROOT / "paper/builds/icecai_2026/en/build_manifest.json"
BI_MANIFEST = ROOT / "paper/builds/icecai_2026/bilingual/build_manifest.json"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def record(path: Path, category: str) -> dict[str, str]:
    return {
        "path": path.relative_to(ROOT).as_posix(),
        "category": category,
        "sha256": sha(path),
    }


def main() -> None:
    parent = json.loads(PARENT.read_text(encoding="utf-8"))
    intermediate = json.loads(INTERMEDIATE.read_text(encoding="utf-8"))
    en = json.loads(EN_MANIFEST.read_text(encoding="utf-8"))
    bi = json.loads(BI_MANIFEST.read_text(encoding="utf-8"))
    report = REPORT.read_text(encoding="utf-8")

    assert "P1_01_CLOSED" in report
    assert "P1_02_CLOSED" in report
    assert "ALL_ORIGINAL_P1S_CLOSED" in report
    assert "New P0: `NO`" in report
    assert "New P1: `NO`" in report
    assert en["compile"]["status"] == bi["compile"]["status"] == "COMPILED"
    assert en["compile"]["page_count"] == 10
    assert bi["compile"]["page_count"] == 16
    assert en["english_paragraph_sha256"] == bi["english_paragraph_sha256"]

    protected = []
    seen = set()
    for row in intermediate["protected"]:
        path = ROOT / row["path"]
        protected.append(record(path, row["category"]))
        seen.add(row["path"])
    for path, category in ((PACKET, "verification_evidence"), (REPORT, "verification_report")):
        relative = path.relative_to(ROOT).as_posix()
        if relative not in seen:
            protected.append(record(path, category))
            seen.add(relative)

    scientific_sources = [row for row in protected if row["category"] == "author_source"]
    table_hashes = [row for row in protected if row["category"] == "active_table"]
    figure_hashes = [row for row in protected if row["category"] == "formal_figure"]
    library = ROOT / "paper/references/library.bib"

    contract = {
        "schema_version": 4,
        "contract_id": "icecai-2026-science-frozen-pre-metadata-2026-09-11",
        "created": "2026-09-11",
        "venue": "ICECAI 2026",
        "stage": "SCIENCE_FROZEN_PRE_METADATA",
        "status": "SCIENTIFIC_CONTENT_FROZEN_PRE_METADATA",
        "parent_contract": {
            "path": PARENT.relative_to(ROOT).as_posix(),
            "contract_id": parent["contract_id"],
            "sha256": sha(PARENT),
        },
        "intermediate_stale_cleanup_contract": {
            "path": INTERMEDIATE.relative_to(ROOT).as_posix(),
            "contract_id": intermediate["contract_id"],
            "sha256": sha(INTERMEDIATE),
        },
        "gpt6_verification": {
            "model": "gpt-6-astra",
            "judge_task": "01a090f3-bf65-7323-af04-e73d8d9394df",
            "p1_01_status": "P1_01_CLOSED",
            "p1_02_status": "P1_02_CLOSED",
            "new_p0": "NO",
            "new_p1": "NO",
            "overall_verdict": "ALL_ORIGINAL_P1S_CLOSED",
            "packet": PACKET.relative_to(ROOT).as_posix(),
            "report": REPORT.relative_to(ROOT).as_posix(),
        },
        "author_status": "DEFERRED",
        "genai_status": "DEFERRED",
        "science_freeze": True,
        "reference_recency": en["reference_recency"],
        "future_change_whitelist": [
            "AUTHOR_METADATA",
            "CORRESPONDING_AUTHOR_METADATA",
            "GENAI_DISCLOSURE",
            "MANUAL_LANGUAGE_POLISHING_WITH_EXPLICIT_USER_AUTHORIZATION",
        ],
        "manual_language_polishing_constraints": {
            "allowed": ["grammar", "wording", "readability", "local transitions"],
            "forbidden": [
                "numbers", "claims", "scope", "RQ conclusions", "tables", "figures",
                "statistical interpretation", "reference evidence role",
            ],
            "post_word_requirement": "claim/numeric consistency check without reopening scientific review",
        },
        "historical_baselines": parent["historical_baselines"],
        "inherited_historical_baselines": parent["inherited_historical_baselines"],
        "scientific_source_hashes": scientific_sources,
        "table_hashes": table_hashes,
        "figure_hashes": figure_hashes,
        "library_bib": record(library, "reference_library"),
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
