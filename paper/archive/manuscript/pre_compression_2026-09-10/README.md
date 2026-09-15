# PRE-COMPRESSION IMMUTABLE SNAPSHOT

Snapshot ID: `pre_compression_2026-09-10`

This directory is the byte-for-byte recovery point for the bilingual LlamaRec manuscript immediately before any T-BALANCED, D-BALANCED, or modified P-BALANCED compression execution.

## Contents

- `source/`: 35 Markdown author sources and 2 directory placeholders, preserving the active hierarchy below `paper/`.
- `metadata/contracts/`: byte-identical copy of the current manuscript contract.
- `metadata/planning/`: byte-identical copies of the seven compression audit and judge documents.
- `metadata/baseline.json`: identities of protected active tables, figures, references, submission adapters, PDFs, and cross-referenced archives.
- `manifest.json`: authoritative source-level paths, sizes, roles, and SHA-256 values.

The existing 14-table snapshot at `paper/archive/tables/pre_compression_2026-09-10/` is cross-referenced by path and manifest hash. It is not duplicated here.

## Aggregate Identity

`PRE_COMPRESSION_MANUSCRIPT_AGGREGATE_SHA256 = 0dd7bfc219bb47b1fa1fc649cd71cdfa399b2955ca62e391c0a25bf08f0565b5`

Algorithm: sort the 35 content-source records by `active_path` using ordinal path order. For every record, encode `active_path + TAB + lowercase sha256 + LF` as UTF-8 without a BOM. Concatenate all encoded records and calculate SHA-256 over that byte stream. Placeholders are counted and hashed individually but excluded from the content aggregate.

## Write Boundary

This snapshot becomes immutable when archive verification and restore simulation pass. Do not overwrite, delete, regenerate, or edit files in place. Any later manuscript state must create a new versioned snapshot directory with its own manifest and aggregate identity.

Recovery state: `CONTENT_RECOVERY_READY`. This label means the pre-compression content can be restored; it does not mean compression has run or that the paper is submission-ready or final.
