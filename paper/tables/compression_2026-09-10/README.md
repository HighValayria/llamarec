# Compression Table Sources, 2026-09-10

This directory contains new display identities derived deterministically from the frozen CSV files in `paper/tables/`. The original 14 CSV files and their immutable archive are not overwritten or deleted.

`build_compact_tables.py` permits only row/column selection, two-panel concatenation, protocol-label normalization, per-seed sign extraction, and interval-to-zero status classification. It does not train or evaluate a model, recompute a metric, rerun bootstrap, or create a new scientific statistic.

- `training_exposure_compact.csv` retains run, optimizer steps, total exposure, and Y/N task exposure. Effective batch 8 and the M1 resume caveat move to the table caption.
- `supervision_semantics_compact.csv` merges the former native-preference and bridge-ranking displays as separate panels with separate metric labels.
- `ms96_delta_summary_compact.csv` retains all 24 split/protocol/metric summaries and adds the sign of each seed-specific delta in 42/43/44 order.
- `hard_candidate_compact.csv` retains all 18 split/protocol/metric point estimates, numeric HR@1 intervals, and per-metric CI status. Omitted secondary-metric bounds remain in the frozen source and archive.
- `lineage.csv` records the source row, source column, and permitted transformation for every output cell.
- `manifest.json` records input and output SHA-256 identities and row counts.

Run `python paper/tables/compression_2026-09-10/build_compact_tables.py --check` to verify byte-reproducibility after generation.
