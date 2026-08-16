---
title: "Sample-Efficiency Training-Efficiency Curve"
type: report
status: current
authority: descriptive
source: agent
created: 2026-08-16
updated: 2026-08-16
last_verified: 2026-08-16
related_code:
  - src/analysis/sample_efficiency_curve.py
  - src/analysis/training_budget_audit.py
  - src/baselines/sasrec.py
  - src/train/train_n.py
  - src/inference/evaluate_n_adapter.py
  - tests/test_analysis_outputs.py
---

# Sample-Efficiency Training-Efficiency Curve

## Question

Does SASRec exceed N-K0 when the comparison is organized by comparable N-task
sample exposure instead of optimizer-step count?

## Scope

This report covers a MovieLens-1M diagnostic on the fixed
`k5_popmatch_seed42` test candidate file. It compares N-K0 and SASRec along a
small N-task exposure grid:

- N-K0 at 3000, 6000, 12000, and 24000 N-task exposures.
- SASRec at the closest batch-512 exposure points, plus high-exposure s1500 and
  s3000 anchors.

The diagnostic is not strict compute matching, capacity matching, wall-clock
matching, token-exposure matching, or multi-seed stability.

## Evidence

The analysis script is `src/analysis/sample_efficiency_curve.py`. The tracked
artifact commit is `6b29fcd Record sample efficiency final curve`, which stores
the final CSV, JSON, gaps CSV, and Markdown under
`.agent/sample_efficiency_training_efficiency/final_curve/`.

Cloud execution generated 10 planned rows, 10 computed rows, 0 missing rows,
and 4 closest-exposure gap rows. All metric rows use 5675 test samples.

## Curve Points

| model | point | N-task exposure | optimizer steps | effective batch | HR@1 | NDCG@5 | MRR |
|---|---|---:|---:|---:|---:|---:|---:|
| N-K0 | n_s375 | 3000 | 375 | 8 | 0.4313656388 | 0.7260192668 | 0.6355653451 |
| N-K0 | n_s750 | 6000 | 750 | 8 | 0.5222907489 | 0.7761254710 | 0.7016299559 |
| N-K0 | n_s1500 | 12000 | 1500 | 8 | 0.5466079295 | 0.7884963692 | 0.7180411160 |
| N-K0 | n_s3000 | 24000 | 3000 | 8 | 0.5612334802 | 0.7968087155 | 0.7289720999 |
| SASRec | sasrec_s6 | 3072 | 6 | 512 | 0.2112775330 | 0.6011741153 | 0.4713597651 |
| SASRec | sasrec_s12 | 6144 | 12 | 512 | 0.2421145374 | 0.6176512047 | 0.4930631424 |
| SASRec | sasrec_s23 | 11776 | 23 | 512 | 0.2699559471 | 0.6348928207 | 0.5156622614 |
| SASRec | sasrec_s47 | 24064 | 47 | 512 | 0.2840528634 | 0.6429537473 | 0.5261879589 |
| SASRec | sasrec_s1500 | 767424 | 1500 | 512 | 0.6088105727 | 0.8198039644 | 0.7595506608 |
| SASRec | sasrec_s3000 | 1534656 | 3000 | 512 | 0.6243171806 | 0.8283562609 | 0.7708663730 |

## Closest-Exposure Gaps

All closest-exposure gaps are computed as SASRec minus N-K0.

| comparison | N-K0 exposure | SASRec exposure | mismatch % | delta HR@1 | delta NDCG@5 | delta MRR |
|---|---:|---:|---:|---:|---:|---:|
| sasrec_s6_minus_n_s375 | 3000 | 3072 | 2.4 | -0.2200881058 | -0.1248451515 | -0.1642055800 |
| sasrec_s12_minus_n_s750 | 6000 | 6144 | 2.4 | -0.2801762115 | -0.1584742663 | -0.2085668135 |
| sasrec_s23_minus_n_s1500 | 12000 | 11776 | -1.8666666667 | -0.2766519824 | -0.1536035485 | -0.2023788546 |
| sasrec_s47_minus_n_s3000 | 24000 | 24064 | 0.2666666667 | -0.2771806168 | -0.1538549682 | -0.2027841410 |

## Interpretation

SASRec does not exceed N-K0 at the closest N-task sample-exposure points by
HR@1. The same direction holds for NDCG@5 and MRR at each closest-exposure
point.

The high-exposure SASRec anchors remain above N-K0, but they use much larger
N-task exposure: 767424 and 1534656 examples versus N-K0's 12000 and 24000
exposure points. These anchors remain useful evidence that SASRec is a strong
specialized sequence baseline; they are not sample-exposure-matched evidence
against N-K0.

## Boundary

This report supports a sample-exposure-sensitive interpretation. It should not
be used as a final architecture-level claim without multi-seed replication,
stricter compute/capacity accounting, and targeted slice diagnostics such as
cold-item or tail-item robustness.
