"""English-master / bilingual-review DOCX synchronization CLI."""

from __future__ import annotations

import argparse
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

from checks import (
    block_text,
    extract_citations,
    inspect,
    reference_entries,
    summary_lines,
)
from docx_model import (
    add_bookmark,
    anchor_name,
    copy_paragraph_content,
    copy_paragraph_group_content,
    document_signature,
    find_anchor_paragraph,
    image_hashes,
    image_parts,
    load_doc,
    next_bookmark_id,
    normalized_text,
    paragraph_index,
    paragraph_text,
    replace_table,
    sha256_file,
    table_hash,
    text_hash,
    visible_digest,
)
from mapping import align_records, section_for, source_records


BASE = Path(__file__).resolve().parent
WORK = BASE / "work"
OUT = BASE / "out"
BACKUPS = BASE / "backups"
HISTORY = BASE / "history"
MASTER = WORK / "ICECAI_2026_English_MASTER.docx"
BILINGUAL = WORK / "ICECAI_2026_Bilingual_REVIEW.docx"
ORIGINAL_MASTER = BASE / "English.docx"
ORIGINAL_BILINGUAL = BASE / "Bilingual.docx"
MANIFEST = BASE / "sync_manifest.json"
QUEUE_MD = OUT / "zh_update_required.md"
QUEUE_JSON = OUT / "zh_update_required.json"
SEMANTIC_JSON = OUT / "semantic_review_required.json"

HEADING_MASTER = [5, 13, 27, 34, 44, 77, 131, 148, 153]
HEADING_BILINGUAL = [7, 22, 45, 57, 74, 119, 178, 207, 216]
TABLE_CAPTION_MASTER = [47, 57, 68, 82, 94, 101, 106, 113, 127]
TABLE_CAPTION_BILINGUAL = [77, 88, 105, 127, 143, 146, 157, 160, 171]
FIGURE_CAPTION_MASTER = [91, 121]
FIGURE_CAPTION_BILINGUAL = [138, 164]
ROMAN = ("I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX")


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_manifest() -> dict:
    if not MANIFEST.exists():
        raise SystemExit("sync_manifest.json is missing; run `sync.py init` first")
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def save_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def add_anchor(doc, paragraph_index: int, name: str) -> None:
    add_bookmark(doc.paragraphs[paragraph_index], name, next_bookmark_id(doc))


def add_block(blocks: list, master_doc, bilingual_doc, identifier: str,
              master_index: int, bilingual_en_index: int | None,
              bilingual_zh_index: int | None, *, kind: str,
              scientific: bool = False, combined: bool = False,
              casefold: bool = False, zh_omits_citations: bool = False) -> dict:
    block = {
        "id": identifier,
        "kind": kind,
        "section": section_for(identifier),
        "scientific": scientific,
        "bilingual_combined": combined,
        "casefold": casefold,
        "zh_omits_citations": zh_omits_citations,
        "master_anchor": anchor_name("EN", identifier),
        "bilingual_en_anchor": anchor_name("BIEN", identifier) if bilingual_en_index is not None else None,
        "bilingual_zh_anchor": anchor_name("BIZH", identifier) if bilingual_zh_index is not None else None,
    }
    block["english_master_anchor"] = block["master_anchor"]
    block["bilingual_english_anchor"] = block["bilingual_en_anchor"]
    block["bilingual_chinese_anchor"] = block["bilingual_zh_anchor"]
    block["metadata_policy"] = "english_only" if bilingual_en_index is None else ("bilingual_pair" if bilingual_zh_index is not None else "shared")
    add_anchor(master_doc, master_index, block["master_anchor"])
    if bilingual_en_index is not None:
        add_anchor(bilingual_doc, bilingual_en_index, block["bilingual_en_anchor"])
    if bilingual_zh_index is not None:
        add_anchor(bilingual_doc, bilingual_zh_index, block["bilingual_zh_anchor"])
    blocks.append(block)
    return block


def _replace_image(source_doc, target_doc, index: int) -> None:
    source = image_parts(source_doc)[index][1]
    target = image_parts(target_doc)[index][1]
    target._blob = source.blob


def _synchronize_english_layer(manifest: dict, master_doc, bilingual_doc) -> dict:
    changed = {"blocks": [], "tables": [], "figures": [], "references": []}
    for block in manifest["blocks"]:
        if not block.get("bilingual_en_anchor"):
            continue
        source = block_text(master_doc, block, "master")
        target = block_text(bilingual_doc, block, "bilingual_en")
        if source is None or target is None:
            continue
        if normalized_text(source, casefold=block.get("casefold", False)) == normalized_text(target, casefold=block.get("casefold", False)):
            continue
        source_p = find_anchor_paragraph(master_doc, block["master_anchor"])
        target_p = find_anchor_paragraph(bilingual_doc, block["bilingual_en_anchor"])
        if block.get("bilingual_combined"):
            zh = block_text(bilingual_doc, block, "bilingual_zh") or ""
            from docx_model import set_paragraph_text
            set_paragraph_text(target_p, source + (" / " + zh if zh else ""))
        else:
            copy_paragraph_content(source_p, target_p)
        changed["blocks"].append(block["id"])

    for table in manifest["tables"]:
        index = table["index"]
        if table_hash(master_doc.tables[index]) != table_hash(bilingual_doc.tables[index]):
            replace_table(master_doc.tables[index], bilingual_doc.tables[index])
            changed["tables"].append(table["id"])
    master_images, bilingual_images = image_hashes(master_doc), image_hashes(bilingual_doc)
    for figure in manifest["figures"]:
        index = figure["index"]
        if master_images[index] != bilingual_images[index]:
            _replace_image(master_doc, bilingual_doc, index)
            changed["figures"].append(figure["id"])
    master_refs = reference_entries(master_doc)
    bilingual_refs = reference_entries(bilingual_doc)
    if len(master_refs) == len(bilingual_refs) == len(manifest["references"]) and any(
        left != right for left, right in zip(master_refs, bilingual_refs)
    ):
        master_anchor = find_anchor_paragraph(master_doc, "SYNC_EN_REFERENCES")
        bilingual_anchor = find_anchor_paragraph(bilingual_doc, "SYNC_BI_REFERENCES")
        master_start = paragraph_index(master_doc, master_anchor)
        bilingual_start = paragraph_index(bilingual_doc, bilingual_anchor)
        source_paragraphs = master_doc.paragraphs[master_start:master_start + len(master_refs)]
        sizes = manifest.get("reference_group_sizes", [13, 12])
        offset = 0
        for group_index, size in enumerate(sizes):
            copy_paragraph_group_content(source_paragraphs[offset:offset + size], bilingual_doc.paragraphs[bilingual_start + group_index])
            offset += size
        changed["references"] = list(range(1, len(master_refs) + 1))
    return changed


def _set_baseline(manifest: dict, master_doc, bilingual_doc) -> None:
    for block in manifest["blocks"]:
        master = block_text(master_doc, block, "master") or ""
        bilingual_zh = block_text(bilingual_doc, block, "bilingual_zh") or ""
        block["baseline_master_text"] = master
        block["baseline_master_normalized"] = normalized_text(master, casefold=block.get("casefold", False))
        block["baseline_zh_text"] = bilingual_zh
        block["baseline_english_hash"] = text_hash(master, casefold=block.get("casefold", False))
        block["baseline_chinese_hash"] = text_hash(bilingual_zh, compact_cjk=True) if block.get("bilingual_zh_anchor") else None
    for table in manifest["tables"]:
        table["baseline_master_hash"] = table_hash(master_doc.tables[table["index"]])
    for figure in manifest["figures"]:
        figure["baseline_master_hash"] = image_hashes(master_doc)[figure["index"]]
    refs = reference_entries(master_doc)
    for index, reference in enumerate(manifest["references"]):
        reference["baseline_master_normalized"] = __import__("checks").normalize_reference(refs[index])
    manifest["structure"] = {
        "master": document_signature(master_doc),
        "bilingual": document_signature(bilingual_doc),
        "reference_count": len(reference_entries(master_doc)),
    }


def write_queue(result: dict, manifest: dict, *, dry_run: bool = False) -> None:
    blocks = {block["id"]: block for block in manifest["blocks"]}
    master_doc, bilingual_doc = load_doc(MASTER), load_doc(BILINGUAL)
    items = []
    for identifier in result["pending_zh_updates"]:
        block = blocks[identifier]
        items.append({
            "id": identifier,
            "section": block["section"],
            "old_english": block.get("baseline_master_text", ""),
            "new_english": block_text(master_doc, block, "master"),
            "current_chinese": block_text(bilingual_doc, block, "bilingual_zh"),
            "numeric_parity": "FAIL" if identifier in result["numeric_mismatches"] else "PASS",
            "citation_parity": "FAIL" if identifier in result["citation_mismatches"] else "PASS",
            "scientific_scope_changed": identifier in result["qualifier_warnings"],
        })
    lines = ["# Chinese Update Queue", "", f"Generated: {now()}", "", f"Pending blocks: {len(items)}", ""]
    for item in items:
        lines.extend([
            f"## {item['id']}", "", f"Section: `{item['section']}`",
            f"Numeric parity: **{item['numeric_parity']}**",
            f"Citation parity: **{item['citation_parity']}**",
            f"SCIENTIFIC_SCOPE_CHANGED: **{'YES' if item['scientific_scope_changed'] else 'NO'}**",
            "", "**OLD EN**", "", item["old_english"] or "", "",
            "**NEW EN**", "", item["new_english"] or "", "",
            "**Current Chinese**", "", item["current_chinese"] or "", "",
            "**REQUIRED**", "", "Update Chinese translation to match NEW EN, then review semantic parity.", "",
        ])
    if not dry_run:
        OUT.mkdir(parents=True, exist_ok=True)
        QUEUE_MD.write_text("\n".join(lines), encoding="utf-8")
        save_json(QUEUE_JSON, {"generated": now(), "items": items})
        save_json(SEMANTIC_JSON, {
            "generated": now(),
            "guarantee": "Manual semantic review required; scripts only check numbers, citations, and known scope qualifiers.",
            "items": [{"id": item["id"], "old_english": item["old_english"], "new_english": item["new_english"], "current_chinese": item["current_chinese"]} for item in items],
        })


def initialize(dry_run: bool, force_init: bool = False) -> int:
    if not ORIGINAL_MASTER.exists() or not ORIGINAL_BILINGUAL.exists():
        raise SystemExit("English.docx and Bilingual.docx must exist in paper/human_alter")
    if not dry_run and not force_init and any(path.exists() for path in (MASTER, BILINGUAL, MANIFEST)):
        raise SystemExit("Managed state already exists; refusing to overwrite it. Use --force-init only after preserving reviewed work.")
    records = source_records()
    master_doc, bilingual_doc = load_doc(ORIGINAL_MASTER), load_doc(ORIGINAL_BILINGUAL)
    original_visible = {"master": visible_digest(master_doc), "bilingual": visible_digest(bilingual_doc)}
    en_map = align_records(records, master_doc.paragraphs, "en")
    bi_en_map = align_records(records, bilingual_doc.paragraphs, "en")
    bi_zh_map = align_records(records, bilingual_doc.paragraphs, "zh")
    by_en = {item["id"]: item for item in en_map}
    by_bien = {item["id"]: item for item in bi_en_map}
    by_bizh = {item["id"]: item for item in bi_zh_map}
    blocks = []
    record_by_id = {record["id"]: record for record in records}
    for record in records:
        identifier = record["id"]
        omitted = bool(extract_citations(record["en"])) and not bool(extract_citations(record["zh"]))
        add_block(
            blocks, master_doc, bilingual_doc, identifier,
            by_en[identifier]["paragraph_index"], by_bien[identifier]["paragraph_index"],
            by_bizh[identifier]["paragraph_index"], kind="scientific_prose",
            scientific=True, zh_omits_citations=omitted,
        )
    add_block(blocks, master_doc, bilingual_doc, "metadata.title", 0, 0, 1, kind="metadata")
    add_block(blocks, master_doc, bilingual_doc, "metadata.author", 1, None, None, kind="metadata")
    add_block(blocks, master_doc, bilingual_doc, "metadata.keywords", 3, 6, None, kind="metadata")
    for index, (m, b) in enumerate(zip(HEADING_MASTER, HEADING_BILINGUAL), 1):
        add_block(blocks, master_doc, bilingual_doc, f"heading.{index}", m, b, b,
                  kind="heading", combined=True, casefold=True)
    for index, (m, b) in enumerate(zip(TABLE_CAPTION_MASTER, TABLE_CAPTION_BILINGUAL), 1):
        add_block(blocks, master_doc, bilingual_doc, f"table_caption.{index}", m, b, b,
                  kind="table_caption", combined=True)
    for index, (m, b) in enumerate(zip(FIGURE_CAPTION_MASTER, FIGURE_CAPTION_BILINGUAL), 1):
        add_block(blocks, master_doc, bilingual_doc, f"figure_caption.{index}", m, b, b,
                  kind="figure_caption", combined=True)

    add_anchor(master_doc, 158, "SYNC_EN_REFERENCES")
    add_anchor(bilingual_doc, 224, "SYNC_BI_REFERENCES")
    manifest = {
        "schema_version": 1,
        "created": now(),
        "updated": now(),
        "policy": "ONE_MASTER_ONE_DERIVED_REVIEW",
        "metadata_policies": {"author": "english_only", "genai": "english_only", "keywords": "shared"},
        "paths": {
            "original_master": str(ORIGINAL_MASTER.relative_to(BASE)),
            "original_bilingual": str(ORIGINAL_BILINGUAL.relative_to(BASE)),
            "master": str(MASTER.relative_to(BASE)),
            "bilingual": str(BILINGUAL.relative_to(BASE)),
        },
        "existing_paragraph_ids_reused": len(records),
        "blocks": blocks,
        "tables": [{
            "id": f"table.{ROMAN[i]}", "index": i,
            "caption_block": f"table_caption.{i + 1}",
            "row_count": len(master_doc.tables[i].rows),
            "column_count": len(master_doc.tables[i].columns),
            "table_matrix_hash": table_hash(master_doc.tables[i]),
        } for i in range(len(master_doc.tables))],
        "figures": [{
            "id": f"figure.{i + 1}", "index": i,
            "caption_block": f"figure_caption.{i + 1}",
            "image_sha256": image_hashes(master_doc)[i],
        } for i in range(len(image_hashes(master_doc)))],
        "references": [{
            "id": f"reference.{i + 1}", "index": i,
            "english_master_anchor": "SYNC_EN_REFERENCES",
            "bilingual_english_anchor": "SYNC_BI_REFERENCES",
            "bilingual_chinese_anchor": None,
            "metadata_policy": "shared",
        } for i in range(len(reference_entries(master_doc)))],
        "reference_group_sizes": [13, 12],
        "source_mapping": {
            "master_min_score": min(item["score"] for item in en_map),
            "bilingual_en_min_score": min(item["score"] for item in bi_en_map),
            "bilingual_zh_min_score": min(item["score"] for item in bi_zh_map),
            "records": record_by_id,
        },
    }
    anchor_visible = {"master": visible_digest(master_doc), "bilingual": visible_digest(bilingual_doc)}
    aligned = _synchronize_english_layer(manifest, master_doc, bilingual_doc)
    _set_baseline(manifest, master_doc, bilingual_doc)
    result = inspect(manifest, master_doc, bilingual_doc)
    manifest["initialization"] = {
        "source_sha256": {"master": sha256_file(ORIGINAL_MASTER), "bilingual": sha256_file(ORIGINAL_BILINGUAL)},
        "source_visible_digest": original_visible,
        "anchor_visible_diff": {
            "master": anchor_visible["master"] != original_visible["master"],
            "bilingual": anchor_visible["bilingual"] != original_visible["bilingual"],
        },
        "derived_english_alignment_changes": aligned,
        "baseline_checks": result,
    }
    if dry_run:
        print("DRY_RUN: initialization would create managed files")
    else:
        WORK.mkdir(parents=True, exist_ok=True)
        master_doc.save(MASTER)
        bilingual_doc.save(BILINGUAL)
        save_json(MANIFEST, manifest)
        write_queue(result, manifest)
    for line in summary_lines(result):
        print(line)
    return 0 if result["en_sync"] == result["table_sync"] == result["reference_sync"] == "PASS" and not result["structural_drift_count"] else 2


def backup() -> Path:
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    destination = BACKUPS / stamp
    destination.mkdir(parents=True, exist_ok=False)
    shutil.copy2(MASTER, destination / MASTER.name)
    shutil.copy2(BILINGUAL, destination / BILINGUAL.name)
    shutil.copy2(MANIFEST, destination / MANIFEST.name)
    return destination


def run_check(write_queue_files: bool = True) -> tuple[dict, dict]:
    manifest = load_manifest()
    result = inspect(manifest, load_doc(MASTER), load_doc(BILINGUAL))
    if write_queue_files:
        write_queue(result, manifest)
    for line in summary_lines(result):
        print(line)
    print(f"ENGLISH_BLOCKS={manifest.get('existing_paragraph_ids_reused', 0)}/{manifest.get('existing_paragraph_ids_reused', 0)}")
    print(f"MASTER_CHANGED_BLOCKS={len(result['changed_master_blocks'])} {result['changed_master_blocks']}")
    print(f"BILINGUAL_EN_MISMATCH={len(result['en_mismatches'])} {result['en_mismatches']}")
    print(f"TABLE_CHANGES={len(result['changed_tables'])} {result['changed_tables']}")
    print(f"FIGURE_CHANGES={len(result['changed_figures'])} {result['changed_figures']}")
    print(f"FIGURE_IDENTITY={'PASS' if not result['figure_mismatches'] else 'FAIL'}")
    return result, manifest


def sync_english(dry_run: bool) -> int:
    manifest = load_manifest()
    master_doc, bilingual_doc = load_doc(MASTER), load_doc(BILINGUAL)
    before = inspect(manifest, master_doc, bilingual_doc)
    if before["structural_drift_count"]:
        for line in summary_lines(before):
            print(line)
        return 3
    changed = _synchronize_english_layer(manifest, master_doc, bilingual_doc)
    if dry_run:
        print("DRY_RUN=" + json.dumps(changed, ensure_ascii=False))
        return 0
    destination = backup()
    bilingual_doc.save(BILINGUAL)
    result = inspect(manifest, master_doc, bilingual_doc)
    write_queue(result, manifest)
    print(f"BACKUP={destination}")
    for line in summary_lines(result):
        print(line)
    return 0 if result["en_sync"] == result["table_sync"] == "PASS" else 2


def remap(dry_run: bool) -> int:
    manifest = load_manifest()
    master_doc, bilingual_doc = load_doc(MASTER), load_doc(BILINGUAL)
    current = inspect(manifest, master_doc, bilingual_doc)
    missing_ids = sorted({value.split(":", 1)[0] for value in current["missing_anchors"]})
    proposals = []
    if missing_ids:
        rows = source_records()
        en_map = {item["id"]: item for item in align_records(rows, master_doc.paragraphs, "en")}
        bi_en_map = {item["id"]: item for item in align_records(rows, bilingual_doc.paragraphs, "en")}
        bi_zh_map = {item["id"]: item for item in align_records(rows, bilingual_doc.paragraphs, "zh")}
        for identifier in missing_ids:
            if identifier not in en_map:
                proposals.append({"id": identifier, "status": "MANUAL_REMAP_REQUIRED"})
                continue
            candidate = {
                "id": identifier,
                "master": en_map.get(identifier),
                "bilingual_en": bi_en_map.get(identifier),
                "bilingual_zh": bi_zh_map.get(identifier),
            }
            scores = [value["score"] for key, value in candidate.items() if key != "id" and value]
            candidate["status"] = "PROPOSAL_REVIEW_REQUIRED" if scores and min(scores) >= 0.75 else "MANUAL_REMAP_REQUIRED"
            proposals.append(candidate)
    payload = {"generated": now(), "applied": False, "missing_ids": missing_ids, "proposals": proposals}
    if not dry_run:
        save_json(OUT / "remap_proposal.json", payload)
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    print("No remap was applied automatically.")
    return 3 if any(item.get("status") == "MANUAL_REMAP_REQUIRED" for item in proposals) else 0


def commit(dry_run: bool, confirm_zh_reviewed: bool) -> int:
    result, manifest = run_check(write_queue_files=False)
    gates = ["en_mismatches", "table_mismatches", "reference_mismatches", "numeric_mismatches", "citation_mismatches", "structural_drift"]
    if any(result[key] for key in gates) or (result["pending_zh_updates"] and not confirm_zh_reviewed):
        print("COMMIT=BLOCKED")
        if result["pending_zh_updates"] and not confirm_zh_reviewed:
            print("Use --confirm-zh-reviewed only after the Chinese blocks have been manually reviewed.")
        return 4
    if dry_run:
        print("DRY_RUN: baseline commit would succeed")
        return 0
    destination = backup()
    master_doc, bilingual_doc = load_doc(MASTER), load_doc(BILINGUAL)
    _set_baseline(manifest, master_doc, bilingual_doc)
    manifest["updated"] = now()
    history_path = HISTORY / datetime.now().strftime("%Y%m%d-%H%M%S")
    history_path.mkdir(parents=True, exist_ok=False)
    save_json(history_path / "change_report.json", {"committed": now(), "confirmed_zh_reviewed": confirm_zh_reviewed, "checks": result})
    save_json(MANIFEST, manifest)
    shutil.copy2(MANIFEST, history_path / MANIFEST.name)
    (history_path / "document_hashes.txt").write_text(
        f"{sha256_file(MASTER)}  {MASTER.name}\n{sha256_file(BILINGUAL)}  {BILINGUAL.name}\n",
        encoding="ascii",
    )
    write_queue(inspect(manifest, master_doc, bilingual_doc), manifest)
    print(f"COMMIT=PASS BACKUP={destination} HISTORY={history_path}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["init", "status", "check", "sync-en", "commit", "remap"])
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--confirm-zh-reviewed", action="store_true")
    parser.add_argument("--force-init", action="store_true")
    args = parser.parse_args()
    if args.command == "init":
        return initialize(args.dry_run, args.force_init)
    if args.command == "status":
        result, _ = run_check(write_queue_files=False)
        return 0 if not result["structural_drift_count"] else 3
    if args.command == "check":
        result, _ = run_check(write_queue_files=not args.dry_run)
        return 0 if not result["structural_drift_count"] else 3
    if args.command == "sync-en":
        return sync_english(args.dry_run)
    if args.command == "commit":
        return commit(args.dry_run, args.confirm_zh_reviewed)
    if args.command == "remap":
        return remap(args.dry_run)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
