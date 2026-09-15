from __future__ import annotations

import hashlib
import json
import re
from copy import deepcopy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
PARENT = ROOT / "paper/plan/review/manuscript_contract_icecai_2026_post_scientific_repair_2026-09-11.json"
OUTPUT = ROOT / "paper/plan/review/manuscript_contract_icecai_2026_post_stale_cleanup_2026-09-11.json"
EN_MANIFEST = ROOT / "paper/builds/icecai_2026/en/build_manifest.json"
BI_MANIFEST = ROOT / "paper/builds/icecai_2026/bilingual/build_manifest.json"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parent = json.loads(PARENT.read_text(encoding="utf-8"))
    en = json.loads(EN_MANIFEST.read_text(encoding="utf-8"))
    bi = json.loads(BI_MANIFEST.read_text(encoding="utf-8"))
    dataset = (ROOT / "paper/modules_parts/methods/datasets.md").read_text(encoding="utf-8")

    assert en["compile"]["status"] == bi["compile"]["status"] == "COMPILED"
    assert en["compile"]["page_count"] == 10
    assert bi["compile"]["page_count"] == 16
    assert en["english_paragraph_sha256"] == bi["english_paragraph_sha256"]
    assert "covering Y-as-ranker, N, and sequential references" in dataset
    assert "覆盖Y-as-ranker、N及序列参照" in dataset
    assert "covering Y-as-ranker, N, M-N" not in dataset
    assert "覆盖Y-as-ranker、N、M-N" not in dataset

    author_sources = sorted(
        path
        for source_root in (ROOT / "paper/modules", ROOT / "paper/modules_parts")
        for path in source_root.rglob("*.md")
    )
    active_text = "\n".join(path.read_text(encoding="utf-8") for path in author_sources)
    amazon_segments = [
        segment for segment in re.split(r"(?<=[.!?。！？])\s*", active_text)
        if "amazon" in segment.lower()
    ]
    stale_amazon_segments = [
        segment for segment in amazon_segments
        if re.search(r"\bM1\b|M-N", segment)
    ]
    assert stale_amazon_segments == []

    amazon_rows = (ROOT / "paper/tables/scientific_repair_2026-09-11/amazon_certified_models.csv").read_text(encoding="utf-8-sig")
    assert "m1" not in amazon_rows.lower()
    assert "m-n" not in amazon_rows.lower()

    contract = deepcopy(parent)
    contract.update(
        {
            "schema_version": 3,
            "contract_id": "icecai-2026-post-stale-cleanup-2026-09-11",
            "created": "2026-09-11",
            "stage": "POST_STALE_EVIDENCE_CLEANUP_PRE_GPT6",
            "status": "GPT6_REPAIR_VERIFICATION_READY",
            "parent_contract": {
                "path": PARENT.relative_to(ROOT).as_posix(),
                "contract_id": parent["contract_id"],
                "sha256": sha(PARENT),
            },
            "author_status": "DEFERRED",
            "genai_status": "DEFERRED",
        }
    )
    contract["manuscript_audits"]["amazon_stale_m1_mn_segments"] = 0
    contract["manuscript_audits"]["stale_cleanup_scope"] = "datasets paragraph only; EN/ZH synchronized"
    contract["artifacts"] = {
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
    }
    contract["protected"] = [
        {
            "path": row["path"],
            "category": row["category"],
            "sha256": sha(ROOT / row["path"]),
        }
        for row in parent["protected"]
    ]
    OUTPUT.write_text(json.dumps(contract, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(OUTPUT.relative_to(ROOT).as_posix())


if __name__ == "__main__":
    main()
