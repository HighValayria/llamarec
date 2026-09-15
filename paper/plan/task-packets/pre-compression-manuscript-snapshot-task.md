# Pre-Compression Manuscript Immutable Snapshot Task

## Goal

Create a byte-for-byte recovery snapshot of the current bilingual manuscript sources before any approved T-BALANCED, D-BALANCED, or modified P-BALANCED compression is executed.

## Allowed Writes

- `paper/archive/manuscript/pre_compression_2026-09-10/**`
- `.agent/current_task.md`
- `.agent/stage_state.yaml`
- This task packet

## Read-Only Inputs

- `paper/modules/**`
- `paper/modules_parts/**`
- `paper/tables/*.csv`
- `paper/figures/*`
- `paper/references/library.bib`
- `paper/builds/ieee_generic/{en,bilingual}/**`
- `paper/plan/review/manuscript_contract_2026-09-10.json`
- The seven approved compression planning and judge documents
- `paper/archive/tables/pre_compression_2026-09-10/**`

## Forbidden Work

- No manuscript, table, figure, reference, submission-adapter, or PDF edits.
- No T/D/P compression, compact-table creation, supplement migration, scientific rewriting, compilation, training, inference, or statistical recomputation.
- No Wiki access or synchronization.

## Required Archive

- Preserve all 35 Markdown author sources and 2 `.gitkeep` placeholders byte for byte under `source/` with their relative hierarchy.
- Archive the current manuscript contract and seven planning documents byte for byte.
- Record source, table-archive, formal-figure, PDF, reference, and adapter identities in `manifest.json` and `metadata/baseline.json`.
- Document the aggregate hash algorithm and immutable-write boundary in `README.md`.

## Verification

- Verify 35/35 archived Markdown hashes equal active-source hashes.
- Restore all 35 Markdown files into a temporary directory and compare them with the manifest.
- Re-hash active manuscript sources and all protected active assets after archival.
- Verify the existing 14-table archive remains complete and unchanged.
- Run `python tools/stage_guard.py`.

## Completion State

Close only as `CONTENT_RECOVERY_READY`. This task does not authorize or execute compression.
