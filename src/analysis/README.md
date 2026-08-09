# Analysis Module

`src/analysis` contains offline analysis entry points for MVP and Phase 1.5.
These scripts read existing `outputs/**/predictions.jsonl` and `metrics.json`
artifacts. They do not train or re-run models.

## Current Files

- `summarize_results.py`: reads Base, Y-K0, N-K0, and M-K0 metrics and writes
  `outputs/results.csv` plus a Markdown summary.
- `basic_error_analysis.py`: reads prediction JSONL files and writes binary
  confusion summaries, ranking sanity checks, and representative errors.
- `threshold_calibration.py`: selects a Yes/No best-F1 threshold on validation,
  then applies the same threshold to test.
- `threshold_comparison.py`: Phase 1.5 STEP B entry point. It writes separate
  binary views for threshold-free AUC, fixed 0.5 threshold, and
  validation-calibrated threshold.
- `grouped_error_analysis.py`: Phase 1.5 STEP C entry point. It joins
  predictions back to fixed Y samples, fixed N candidate records, and
  full-sequence-derived user/movie statistics, then writes grouped diagnostics.
- `phase2a_robustness_report.py`: Phase 2A ranking robustness entry point. It
  reads explicit candidate-variant metric directories and writes CSV/JSON plus a
  Markdown report without mixing canonical output paths into variant analysis.
- `phase2b_result_synthesis.py`: Phase 2B synthesis entry point. It reads
  existing Phase 1.5 and Phase 2A analysis artifacts and writes paper-ready
  CSV/JSON/Markdown tables plus cautious interpretation text.

## Phase 1.5 STEP B Example

```bash
python -m src.analysis.threshold_comparison \
  --config configs/experiment.yaml \
  --dataset movielens-1m \
  --y-run pool200k_1m_y_1500 \
  --m-runs pool200k_1m_m_1500 diag_m1_1m_m_200k_3000 diag_m2_1m_m_y2n1_1500 \
  --m-labels M0 M1 M2 \
  --output-dir outputs/calibration/movielens-1m/threshold_comparison
```

Outputs:

```text
binary_auc.csv
binary_fixed_0_5.csv
binary_calibrated.csv
threshold_comparison.json
threshold_comparison.md
```

This script compares only Y-task Yes/No binary metrics. It does not include
N-task ranking metrics.

## Phase 1.5 STEP C Example

```bash
python -m src.analysis.grouped_error_analysis \
  --config configs/experiment.yaml \
  --dataset movielens-1m \
  --y-run pool200k_1m_y_1500 \
  --n-run pool200k_1m_n_1500 \
  --m-runs pool200k_1m_m_1500 diag_m1_1m_m_200k_3000 diag_m2_1m_m_y2n1_1500 \
  --m-labels M0 M1 M2 \
  --split test \
  --threshold-mode validation_best_f1 \
  --output-dir outputs/error_analysis/movielens-1m/grouped
```

Outputs:

```text
test_binary_group_metrics.csv
test_ranking_group_metrics.csv
test_grouped_error_analysis.json
test_grouped_error_analysis.md
```

Use `--split validation` for validation diagnostics. Binary grouped metrics keep
the threshold source explicit via `--threshold-mode`; ranking grouped metrics
report HR@1, HR@5, NDCG@5, MRR, mean rank, and mean margin by group.

## Phase 2A Ranking Robustness Example

```bash
python -m src.analysis.phase2a_robustness_report \
  --input-dir outputs/phase2a/ranking_robustness \
  --dataset movielens-1m
```

Outputs:

```text
phase2a_ranking_robustness_metrics.csv
phase2a_ranking_robustness_metrics.json
phase2a_ranking_robustness_comparison.csv
phase2a_ranking_robustness_report.md
```

## Phase 2B Result Synthesis Example

```bash
python -m src.analysis.phase2b_result_synthesis \
  --dataset movielens-1m \
  --threshold-json outputs/calibration/movielens-1m/threshold_comparison/threshold_comparison.json \
  --grouped-json outputs/error_analysis/movielens-1m/grouped/test_grouped_error_analysis.json \
  --phase2a-metrics-json outputs/phase2a/ranking_robustness/phase2a_ranking_robustness_metrics.json \
  --phase2a-comparison-csv outputs/phase2a/ranking_robustness/phase2a_ranking_robustness_comparison.csv \
  --output-dir outputs/phase2b/result_synthesis
```

Outputs:

```text
phase2b_binary_calibrated_test.csv
phase2b_canonical_ranking_test.csv
phase2b_robustness_test.csv
phase2b_robustness_key_deltas.csv
phase2b_paper_ready_claims.json
phase2b_result_synthesis.md
```
