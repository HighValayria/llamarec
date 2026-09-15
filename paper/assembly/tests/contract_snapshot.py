from __future__ import annotations

import hashlib
import json
from pathlib import Path


CONTRACT_RELATIVE_PATH = "paper/plan/review/manuscript_contract_icecai_2026_science_frozen_pre_metadata_2026-09-11.json"
PARENT_CONTRACT_RELATIVE_PATH = "paper/plan/review/manuscript_contract_icecai_2026_post_scientific_repair_2026-09-11.json"
PARENT_CONTRACT_SHA256 = "b0cc96ed9d511e86a71d56e2b8e7bc9dce29a442e653447c5a369049da4db4f0"
HISTORICAL_BASELINES = {
    "paper/evidence/asset_provenance.json",
    "paper/plan/review/ms96_scope_baseline.json",
}
REQUIRED_CONTROLS = {
    "paper/assembly/paper_manifest.yaml",
    "paper/evidence/bootstrap_provenance_closure.md",
    "paper/evidence/claim_matrix.md",
    "paper/evidence/pending_evidence.md",
    "paper/evidence/run_metadata_ledger.md",
    "paper/evidence/source_of_truth.md",
    "paper/evidence/story_and_novelty_freeze.md",
    "paper/references/citation_claim_map.md",
    "paper/references/citation_registry.json",
    "paper/references/library.bib",
    "paper/references/primary_source_notes.md",
}
DISALLOWED_PARTS = {"build", "builds", "cache", ".pytest_cache", "tmp", "temp"}


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def assert_current_contract(testcase, repo: Path) -> dict:
    contract_path = repo / CONTRACT_RELATIVE_PATH
    contract = json.loads(contract_path.read_text(encoding="utf-8"))

    testcase.assertEqual(contract["schema_version"], 4)
    testcase.assertEqual(contract["contract_id"], "icecai-2026-science-frozen-pre-metadata-2026-09-11")
    testcase.assertEqual(contract["venue"], "ICECAI 2026")
    testcase.assertEqual(contract["stage"], "SCIENCE_FROZEN_PRE_METADATA")
    testcase.assertEqual(contract["status"], "SCIENTIFIC_CONTENT_FROZEN_PRE_METADATA")
    testcase.assertEqual(contract["author_status"], "DEFERRED")
    testcase.assertEqual(contract["genai_status"], "DEFERRED")
    testcase.assertEqual(contract["reference_recency"]["active_cited_references"], 25)
    testcase.assertEqual(contract["reference_recency"]["recent_2024_2026"], 13)
    testcase.assertEqual(contract["reference_recency"]["status"], "PASS")
    testcase.assertEqual(contract["parent_contract"]["path"], PARENT_CONTRACT_RELATIVE_PATH)
    testcase.assertEqual(contract["parent_contract"]["sha256"], PARENT_CONTRACT_SHA256)
    testcase.assertEqual(file_sha256(repo / PARENT_CONTRACT_RELATIVE_PATH), PARENT_CONTRACT_SHA256)

    historical = contract["inherited_historical_baselines"]
    historical_paths = [row["path"] for row in historical]
    testcase.assertEqual(len(historical_paths), len(set(historical_paths)))
    testcase.assertEqual(set(historical_paths), HISTORICAL_BASELINES)
    for row in historical:
        testcase.assertEqual(file_sha256(repo / row["path"]), row["sha256"], row["path"])

    protected = contract["protected"]
    protected_paths = [row["path"] for row in protected]
    testcase.assertEqual(len(protected_paths), len(set(protected_paths)))
    testcase.assertNotIn(CONTRACT_RELATIVE_PATH, protected_paths)

    expected_author_sources = {
        path.relative_to(repo).as_posix()
        for root in (repo / "paper/modules", repo / "paper/modules_parts")
        for path in root.rglob("*.md")
    }
    contracted_author_sources = {
        row["path"] for row in protected if row["category"] == "author_source"
    }
    testcase.assertEqual(contracted_author_sources, expected_author_sources)
    testcase.assertTrue(REQUIRED_CONTROLS.issubset(set(protected_paths)))

    for row in protected:
        path = Path(row["path"])
        testcase.assertFalse(DISALLOWED_PARTS.intersection(path.parts), row["path"])
        testcase.assertEqual(file_sha256(repo / path), row["sha256"], row["path"])

    return contract
