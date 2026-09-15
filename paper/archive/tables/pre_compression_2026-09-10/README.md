# Pre-Compression Table Archive

This directory is the immutable snapshot of the 14 active CSV table sources used by the compiled English manuscript on 2026-09-10, before any evidence-preserving table compression is executed.

## Rules

- Files under `csv/` are byte-for-byte copies, not active inputs. Current builds continue to read `paper/tables/*.csv`.
- Build scripts must never write into this archive. The archive is outside `paper/builds/` and is not a generation target.
- Do not overwrite, delete, rename, normalize, reformat, or regenerate archived CSVs.
- Any future compact, merged, or replacement table should use a new active identity such as `*_compact.csv` or another explicitly versioned path.
- If an active filename must be reused, preserve the old bytes here first and verify the SHA256 recorded in `manifest.json`.
- A table removed from the main manuscript remains in this archive even when it is no longer cited or submitted.
- `manifest.json` maps every archived file to its original active path, table identity, manuscript role, dimensions, and snapshot SHA256.
- `metadata/baseline.json` records the write-boundary fingerprints used to prove that this audit did not modify active tables, manuscript author sources, or the submission adapter.

This archive preserves evidence history. It does not authorize or execute table compression, merging, deletion, replacement, or supplement migration.
