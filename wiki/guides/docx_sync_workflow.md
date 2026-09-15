---
title: "English Master and Bilingual Review DOCX Sync"
type: guide
status: current
authority: normative
source: user-requested
created: 2026-09-12
updated: 2026-09-12
last_verified: 2026-09-12
related_code:
  - paper/human_alter/sync.py
  - paper/human_alter/docx_model.py
  - paper/human_alter/mapping.py
  - paper/human_alter/checks.py
  - paper/human_alter/test_sync.py
  - paper/human_alter/sync_manifest.json
  - paper/human_alter/README.md
---

# English Master and Bilingual Review DOCX Sync

## Authoritative Documents

The Word workflow has one English source of truth and one derived bilingual review document:

```text
paper/human_alter/work/ICECAI_2026_English_MASTER.docx
paper/human_alter/work/ICECAI_2026_Bilingual_REVIEW.docx
```

Only the English MASTER should be edited for English polishing. The English content inside the bilingual REVIEW is synchronized by tooling and must not be maintained manually. The original `English.docx` and `Bilingual.docx` are initialization inputs and are not overwritten.

The current manifest reuses all 78 manuscript paragraph IDs and manages 101 English blocks, including 99 EN/ZH pairs and two blocks without Chinese. It also maps nine tables, two figures, and 25 references. Stable invisible OOXML bookmarks provide block identity; paragraph indexes are not the durable key.

## Normal Workflow

After saving and closing the English MASTER, run from the repository root:

```text
paper\human_alter\status.bat
paper\human_alter\sync_en.bat --dry-run
paper\human_alter\sync_en.bat
paper\human_alter\check.bat
paper\human_alter\commit.bat --confirm-zh-reviewed
```

`status.bat` reports changed English blocks, English-layer mismatches, pending Chinese updates, table/figure changes, and structural drift. `sync_en.bat` creates a timestamped backup, then copies changed English content into the bilingual REVIEW at run-level OOXML granularity.

`out/zh_update_required.md` identifies the old English, new English, current Chinese, number/citation changes, and scientific-scope changes. Chinese is updated manually only for queued blocks. Scripts do not claim to guarantee translation semantics. The machine-readable semantic-review queue is `paper/human_alter/out/semantic_review_required.json`.

`check.bat` requires English, table, reference, numeric, and citation consistency and zero structural drift. `commit.bat --confirm-zh-reviewed` records a new synchronization baseline after the Chinese review is complete. This is not a Git commit.

## Structural Edits

Deleting, merging, or splitting a managed paragraph; adding a section; or adding/removing a complete table or figure is a structural edit. Do not run automatic synchronization when `STRUCTURAL_DRIFT` is nonzero. Run the remap proposal command and review it; the tool never silently applies a low-confidence mapping.

```text
C:\Users\33967\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe paper\human_alter\sync.py remap --dry-run
```

## Verification Boundaries

The initialized baseline passes `EN_SYNC`, `TABLE_SYNC`, `REFERENCE_SYNC`, `NUMERIC_PARITY`, and `CITATION_PARITY`; `STRUCTURAL_DRIFT` and `ZH_UPDATE_REQUIRED` are zero. Seven isolated fixtures cover sentence, number, citation, heading, table-cell, paragraph-deletion, and paragraph-split behavior. Invisible anchors do not change visible content. The English and bilingual managed documents render to 10 and 14 pages.

Synchronization compliance is not submission-template compliance. The managed documents intentionally inherit the input Word formatting. At the current baseline, page size, margins, two-column layout, fonts, tables, figures, and pagination render correctly, but the English document still relies heavily on the `Normal` paragraph style and has a section structure that is not identical to the official Word template. Template adaptation must be handled as a separate, explicitly authorized formatting stage.
