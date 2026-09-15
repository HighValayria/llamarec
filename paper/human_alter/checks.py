"""Consistency checks for the English-master DOCX workflow."""

from __future__ import annotations

import re
import unicodedata
from collections import Counter

from docx_model import (
    document_signature,
    find_anchor_paragraph,
    image_hashes,
    normalized_text,
    paragraph_text,
    table_hash,
)


QUALIFIERS = (
    "validation", "test", "held-out", "seed42", "seed43", "seed44",
    "48k", "96k", "200k", "k5", "k20", "k50", "cross-task-safe",
    "common subset", "only", "not", "no", "rather than", "approximately",
    "conditional", "directional", "significance", "equivalence", "causal",
    "monotonic",
    "suggest", "suggests", "suggested", "indicate", "indicates", "indicated",
    "consistent with", "directional", "descriptive", "may", "might", "could",
    "cannot", "not establish", "not prove", "no significance", "不显著", "表明",
    "提示", "可能", "方向性", "描述性", "不能", "无法证明", "未证明",
)


def _split_combined(text: str) -> tuple[str, str]:
    for separator in (" / ", "/", "／"):
        if separator in text:
            left, right = text.split(separator, 1)
            return left.strip(), right.strip()
    return text.strip(), ""


def block_text(document, block: dict, side: str) -> str | None:
    anchor = block.get(f"{side}_anchor")
    if not anchor:
        return None
    paragraph = find_anchor_paragraph(document, anchor)
    if paragraph is None:
        return None
    text = paragraph_text(paragraph)
    if block.get("bilingual_combined") and side in {"bilingual_en", "bilingual_zh"}:
        en, zh = _split_combined(text)
        return en if side == "bilingual_en" else zh
    return text


def extract_numbers(text: str) -> Counter:
    text = re.sub(r"\[[0-9,\-–—\s]+\]", " ", text or "")
    tokens = re.findall(
        r"(?i)(?:(?:seeds?|随机种子)\s*[\-–—]?\s*\d+\s*k?|k\s*\d+|(?<![A-Za-z])\d+(?:,\d{3})*(?:\.\d+)?\s*(?:[%％]|k)?)",
        text,
    )
    normalized = []
    for token in tokens:
        value = re.sub(r"\s+", "", token).replace(",", "").replace("％", "%").lower()
        value = re.sub(r"^(?:seeds?|随机种子)[\-–—]?", "", value)
        normalized.append(value)
    return Counter(normalized)


def extract_citations(text: str) -> Counter:
    result: Counter = Counter()
    for content in re.findall(r"\[([0-9,\-–—\s]+)\]", text or ""):
        for part in content.split(","):
            part = part.strip()
            match = re.fullmatch(r"(\d+)\s*[\-–—]\s*(\d+)", part)
            if match:
                start, end = map(int, match.groups())
                for value in range(min(start, end), max(start, end) + 1):
                    result[str(value)] += 1
            elif part.isdigit():
                result[part] += 1
    return result


def extract_qualifiers(text: str) -> set[str]:
    lowered = unicodedata.normalize("NFKC", text or "").casefold()
    return {item for item in QUALIFIERS if item.casefold() in lowered}


def reference_entries(document) -> list[str]:
    paragraphs = list(document.paragraphs)
    start = None
    for index, paragraph in enumerate(paragraphs):
        text = normalized_text(paragraph_text(paragraph), casefold=True)
        if text in {"references", "references / 参考文献", "references/参考文献"}:
            start = index + 1
            break
    if start is None:
        return []
    payload = "\n".join(paragraph_text(p) for p in paragraphs[start:])
    matches = list(re.finditer(r"(?:^|\n|\s)(\[(\d+)\])\s*", payload))
    entries = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(payload)
        entries.append((match.group(1) + payload[match.end():end]).strip())
    return entries


def normalize_reference(text: str) -> str:
    value = unicodedata.normalize("NFKC", text or "")
    value = re.sub(r"(?<=\w)-\s+(?=\w)", "", value)
    return re.sub(r"\s+", "", value).casefold()


def inspect(manifest: dict, master_doc, bilingual_doc) -> dict:
    result = {
        "missing_anchors": [],
        "changed_master_blocks": [],
        "en_mismatches": [],
        "numeric_mismatches": [],
        "citation_mismatches": [],
        "qualifier_warnings": [],
        "changed_tables": [],
        "table_mismatches": [],
        "changed_figures": [],
        "figure_mismatches": [],
        "reference_mismatches": [],
        "changed_references": [],
        "pending_zh_updates": [],
        "structural_drift": [],
    }

    for block in manifest.get("blocks", []):
        master = block_text(master_doc, block, "master")
        bilingual_en = block_text(bilingual_doc, block, "bilingual_en")
        bilingual_zh = block_text(bilingual_doc, block, "bilingual_zh")
        for side, value in (("master", master), ("bilingual_en", bilingual_en), ("bilingual_zh", bilingual_zh)):
            if block.get(f"{side}_anchor") and value is None:
                result["missing_anchors"].append(f"{block['id']}:{side}")
        if master is None:
            continue

        current_hash = normalized_text(master, casefold=block.get("casefold", False))
        baseline_hash = block.get("baseline_master_normalized")
        changed = baseline_hash is not None and current_hash != baseline_hash
        if changed:
            result["changed_master_blocks"].append(block["id"])
            if block.get("bilingual_zh_anchor"):
                result["pending_zh_updates"].append(block["id"])

        if bilingual_en is not None:
            left = normalized_text(master, casefold=block.get("casefold", False))
            right = normalized_text(bilingual_en, casefold=block.get("casefold", False))
            if left != right:
                result["en_mismatches"].append(block["id"])

        if block.get("scientific") and bilingual_zh is not None:
            if extract_numbers(master) != extract_numbers(bilingual_zh):
                result["numeric_mismatches"].append(block["id"])
            if not block.get("zh_omits_citations") and extract_citations(master) != extract_citations(bilingual_zh):
                result["citation_mismatches"].append(block["id"])
            if changed and extract_qualifiers(master) != extract_qualifiers(block.get("baseline_master_text", "")):
                result["qualifier_warnings"].append(block["id"])

    for table in manifest.get("tables", []):
        index = table["index"]
        if index >= len(master_doc.tables) or index >= len(bilingual_doc.tables):
            result["structural_drift"].append(f"missing table {table['id']}")
            continue
        master_hash = table_hash(master_doc.tables[index])
        bilingual_hash = table_hash(bilingual_doc.tables[index])
        if master_hash != table.get("baseline_master_hash"):
            result["changed_tables"].append(table["id"])
            if table.get("caption_block"):
                result["pending_zh_updates"].append(table["caption_block"])
        if master_hash != bilingual_hash:
            result["table_mismatches"].append(table["id"])

    master_images = image_hashes(master_doc)
    bilingual_images = image_hashes(bilingual_doc)
    for figure in manifest.get("figures", []):
        index = figure["index"]
        if index >= len(master_images) or index >= len(bilingual_images):
            result["structural_drift"].append(f"missing figure {figure['id']}")
            continue
        if master_images[index] != figure.get("baseline_master_hash"):
            result["changed_figures"].append(figure["id"])
            if figure.get("caption_block"):
                result["pending_zh_updates"].append(figure["caption_block"])
        if master_images[index] != bilingual_images[index]:
            result["figure_mismatches"].append(figure["id"])

    master_refs = reference_entries(master_doc)
    bilingual_refs = reference_entries(bilingual_doc)
    expected_refs = manifest.get("structure", {}).get("reference_count", 0)
    if len(master_refs) != expected_refs or len(bilingual_refs) != expected_refs:
        result["structural_drift"].append(
            f"reference count master={len(master_refs)} bilingual={len(bilingual_refs)} expected={expected_refs}"
        )
    for index in range(min(len(master_refs), len(bilingual_refs))):
        if normalize_reference(master_refs[index]) != normalize_reference(bilingual_refs[index]):
            result["reference_mismatches"].append(index + 1)
        baseline = manifest.get("references", [])[index].get("baseline_master_normalized") if index < len(manifest.get("references", [])) else None
        if baseline is not None and normalize_reference(master_refs[index]) != baseline:
            result["changed_references"].append(index + 1)

    baseline_structure = manifest.get("structure", {})
    for label, document in (("master", master_doc), ("bilingual", bilingual_doc)):
        expected = baseline_structure.get(label)
        if expected and document_signature(document) != expected:
            result["structural_drift"].append(f"{label} document signature changed")
    if result["missing_anchors"]:
        result["structural_drift"].append("one or more stable anchors are missing or duplicated")

    result["pending_zh_updates"] = list(dict.fromkeys(result["pending_zh_updates"]))
    result.update({
        "en_sync": "PASS" if not result["en_mismatches"] else "FAIL",
        "table_sync": "PASS" if not result["table_mismatches"] else "FAIL",
        "reference_sync": "PASS" if not result["reference_mismatches"] else "FAIL",
        "numeric_parity": "PASS" if not result["numeric_mismatches"] else "FAIL",
        "citation_parity": "PASS" if not result["citation_mismatches"] else "FAIL",
        "structural_drift_count": len(result["structural_drift"]),
        "zh_update_required": len(result["pending_zh_updates"]),
    })
    return result


def summary_lines(result: dict) -> list[str]:
    lines = [
        f"EN_SYNC={result['en_sync']}",
        f"TABLE_SYNC={result['table_sync']}",
        f"REFERENCE_SYNC={result['reference_sync']}",
        f"NUMERIC_PARITY={result['numeric_parity']}",
        f"CITATION_PARITY={result['citation_parity']}",
        f"STRUCTURAL_DRIFT={result['structural_drift_count']}",
        f"ZH_UPDATE_REQUIRED={result['zh_update_required']}",
    ]
    for key in (
        "changed_master_blocks", "en_mismatches", "numeric_mismatches",
        "citation_mismatches", "qualifier_warnings", "table_mismatches",
        "figure_mismatches", "reference_mismatches", "changed_references", "structural_drift",
    ):
        if result.get(key):
            lines.append(f"{key.upper()}={result[key]}")
    return lines
