# English Master / Bilingual Review DOCX Sync

This directory uses one authoritative English Word document and one derived
bilingual review document:

- `work/ICECAI_2026_English_MASTER.docx` is the only editable English source.
- `work/ICECAI_2026_Bilingual_REVIEW.docx` is derived for bilingual review.
- `English.docx` and `Bilingual.docx` are immutable initialization inputs.

The system reuses the 78 manuscript paragraph IDs already embedded in the
modular Markdown source. Invisible OOXML bookmarks bind those IDs to Word
paragraphs; headings, captions, tables, figures, references, and selected
metadata have additional managed identities.

## Daily workflow

Run commands from `F:\Projects\llamarec` with the bundled Python runtime shown
in `run_sync_status.bat`, or use the batch files directly.

```text
paper\human_alter\status.bat
paper\human_alter\sync_en.bat --dry-run
paper\human_alter\sync_en.bat
paper\human_alter\check.bat
paper\human_alter\commit.bat --dry-run
paper\human_alter\commit.bat --confirm-zh-reviewed
```

`sync-en` creates a timestamped backup before writing. It copies English
paragraph content at run-level OOXML granularity, updates table cells and image
parts, and never translates Chinese text. Changed paired blocks are written to
`out/zh_update_required.md`, `out/zh_update_required.json`, and the deliberately
narrow `out/semantic_review_required.json`.

`commit` is blocked until English synchronization, tables, references, numeric
parity, citation parity, structural integrity, and the Chinese update queue all
pass. Use `remap` only after reviewing a structural edit; it deliberately does
not guess a new mapping.

`init` refuses to overwrite an existing managed state. `--force-init` exists
only for deliberate reinitialization after reviewed work has been preserved.

All write-capable commands accept `--dry-run`. Do not edit the two original
DOCX files or the bilingual English layer by hand.
