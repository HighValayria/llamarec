"""Isolated behavioral fixtures for the DOCX synchronization gates."""

from __future__ import annotations

import copy
import json
from pathlib import Path

import sync
from checks import inspect
from docx_model import find_anchor_paragraph, load_doc, set_paragraph_text


def fresh():
    return sync.load_manifest(), load_doc(sync.MASTER), load_doc(sync.BILINGUAL)


def block(manifest, predicate):
    return next(item for item in manifest["blocks"] if predicate(item))


def run() -> list[dict]:
    results = []

    manifest, master, bilingual = fresh()
    item = block(manifest, lambda x: x["scientific"])
    paragraph = find_anchor_paragraph(master, item["master_anchor"])
    set_paragraph_text(paragraph, paragraph.text + " Controlled sentence edit.")
    check = inspect(manifest, master, bilingual)
    results.append({"fixture": "A_sentence_edit", "pass": item["id"] in check["changed_master_blocks"] and item["id"] in check["en_mismatches"] and item["id"] in check["pending_zh_updates"]})

    manifest, master, bilingual = fresh()
    item = block(manifest, lambda x: x["scientific"] and x.get("bilingual_zh_anchor"))
    paragraph = find_anchor_paragraph(master, item["master_anchor"])
    set_paragraph_text(paragraph, paragraph.text + " 98765.")
    sync._synchronize_english_layer(manifest, master, bilingual)
    check = inspect(manifest, master, bilingual)
    results.append({"fixture": "B_numeric_edit", "pass": item["id"] in check["numeric_mismatches"] and item["id"] in check["pending_zh_updates"]})

    manifest, master, bilingual = fresh()
    item = block(manifest, lambda x: x["scientific"] and not x.get("zh_omits_citations"))
    paragraph = find_anchor_paragraph(master, item["master_anchor"])
    set_paragraph_text(paragraph, paragraph.text + " [99]")
    sync._synchronize_english_layer(manifest, master, bilingual)
    check = inspect(manifest, master, bilingual)
    results.append({"fixture": "C_citation_edit", "pass": item["id"] in check["citation_mismatches"] and item["id"] in check["pending_zh_updates"]})

    manifest, master, bilingual = fresh()
    item = block(manifest, lambda x: x["kind"] == "heading")
    paragraph = find_anchor_paragraph(master, item["master_anchor"])
    set_paragraph_text(paragraph, paragraph.text + " REVIEW")
    sync._synchronize_english_layer(manifest, master, bilingual)
    check = inspect(manifest, master, bilingual)
    results.append({"fixture": "D_heading_edit", "pass": item["id"] not in check["en_mismatches"] and item["id"] in check["pending_zh_updates"]})

    manifest, master, bilingual = fresh()
    master.tables[0].cell(0, 0).text += " TEST"
    before = inspect(manifest, master, bilingual)
    sync._synchronize_english_layer(manifest, master, bilingual)
    after = inspect(manifest, master, bilingual)
    results.append({"fixture": "E_table_cell_edit", "pass": bool(before["table_mismatches"]) and "table_caption.1" in before["pending_zh_updates"] and not after["table_mismatches"]})

    manifest, master, bilingual = fresh()
    item = block(manifest, lambda x: x["scientific"])
    paragraph = find_anchor_paragraph(master, item["master_anchor"])
    paragraph._p.getparent().remove(paragraph._p)
    check = inspect(manifest, master, bilingual)
    results.append({"fixture": "F_paragraph_delete", "pass": check["structural_drift_count"] > 0})

    manifest, master, bilingual = fresh()
    master.add_paragraph("Simulated split paragraph")
    check = inspect(manifest, master, bilingual)
    results.append({"fixture": "G_paragraph_split", "pass": check["structural_drift_count"] > 0})

    return results


if __name__ == "__main__":
    output = run()
    sync.OUT.mkdir(parents=True, exist_ok=True)
    path = sync.OUT / "fixture_test_report.json"
    path.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    for item in output:
        print(f"{item['fixture']}={'PASS' if item['pass'] else 'FAIL'}")
    raise SystemExit(0 if all(item["pass"] for item in output) else 1)
