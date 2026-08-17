---
title: "Multi-seed Stability"
type: report
status: current
authority: descriptive
source: mixed
created: 2026-08-17
updated: 2026-08-17
last_verified: 2026-08-17
related_code:
  - src/analysis/multiseed_stability_summary.py
  - src/train/train_y.py
  - src/train/train_n.py
  - src/train/train_m.py
  - src/baselines/sasrec.py
  - tests/test_analysis_outputs.py
  - .agent/multiseed_stability/final/multiseed_metrics.csv
  - .agent/multiseed_stability/final/multiseed_aggregates.csv
  - .agent/multiseed_stability/final/multiseed_comparisons.csv
  - .agent/multiseed_stability/final/multiseed_stability_summary.json
  - .agent/multiseed_stability/final/multiseed_stability_summary.md
superseded_by: null
---

# Multi-seed Stability

Dataset: `movielens-1m`.

Protocol: MovieLens-1M multi-seed stability on fixed
`k5_popmatch_seed42` candidates. Candidate sets remain fixed while model
training seeds vary across 42, 43, and 44.

## Direct Answers

- Y-K0 binary stability: available across 3 seeds; binary F1 range
  `0.0097766064`.
- N-K0 above M1 by HR@1: yes across 3 seeds; minimum margin `0.0103964758`.
- N-K0 above SASRec exposure-match by HR@1: yes across 3 seeds; minimum margin
  `0.2766519824`.
- SASRec high-exposure s3000 above N-K0 by HR@1: yes across 3 seeds; minimum
  margin `0.0777092511`.
- Candidate protocol fixed: yes, all rows use `k5_popmatch_seed42`.

## Metrics

| model | seed | regime | binary AUC | binary F1 | HR@1 | NDCG@5 | MRR |
|---|---:|---|---:|---:|---:|---:|---:|
| Y-K0 | 42 | binary preference | 0.7690966770 | 0.7799722571 | 0.3048458150 | 0.6503957066 | 0.5365521292 |
| Y-K0 | 43 | binary preference | 0.7638536397 | 0.7770993369 | 0.1948898678 | 0.5869765641 | 0.4531071953 |
| Y-K0 | 44 | binary preference | 0.7667400862 | 0.7701956507 | 0.2116299559 | 0.5941504467 | 0.4627518355 |
| N-K0 | 42 | popmatch ranking | unavailable | unavailable | 0.5466079295 | 0.7884963692 | 0.7180411160 |
| N-K0 | 43 | popmatch ranking | unavailable | unavailable | 0.5427312775 | 0.7869133539 | 0.7158825257 |
| N-K0 | 44 | popmatch ranking | unavailable | unavailable | 0.5383259912 | 0.7831335521 | 0.7110044053 |
| M1 | 42 | popmatch ranking | 0.7664368902 | 0.7281077294 | 0.5238766520 | 0.7781912330 | 0.7042525698 |
| M1 | 43 | popmatch ranking | 0.7669426412 | 0.7356690329 | 0.5219383260 | 0.7767052601 | 0.7023289280 |
| M1 | 44 | popmatch ranking | 0.7615278434 | 0.6922447644 | 0.5279295154 | 0.7794587445 | 0.7059941263 |
| SASRec exp-match | 42 | roughly exposure matched | unavailable | unavailable | 0.2699559471 | 0.6348928207 | 0.5156622614 |
| SASRec exp-match | 43 | roughly exposure matched | unavailable | unavailable | 0.2548017621 | 0.6264308277 | 0.5044816446 |
| SASRec exp-match | 44 | roughly exposure matched | unavailable | unavailable | 0.2532158590 | 0.6263785286 | 0.5043935389 |
| SASRec high s3000 | 42 | high exposure | unavailable | unavailable | 0.6243171806 | 0.8283562609 | 0.7708663730 |
| SASRec high s3000 | 43 | high exposure | unavailable | unavailable | 0.6285462555 | 0.8295574494 | 0.7725022026 |
| SASRec high s3000 | 44 | high exposure | unavailable | unavailable | 0.6304845815 | 0.8294692615 | 0.7724992658 |

## Aggregates

| model | metric | mean | std | min | max | range |
|---|---|---:|---:|---:|---:|---:|
| Y-K0 | binary F1 | 0.7757557482 | 0.0041027983 | 0.7701956507 | 0.7799722571 | 0.0097766064 |
| N-K0 | HR@1 | 0.5425550661 | 0.0033833823 | 0.5383259912 | 0.5466079295 | 0.0082819383 |
| M1 | HR@1 | 0.5245814978 | 0.0024961562 | 0.5219383260 | 0.5279295154 | 0.0059911894 |
| SASRec exp-match | HR@1 | 0.2593245227 | 0.0075453809 | 0.2532158590 | 0.2699559471 | 0.0167400881 |
| SASRec high s3000 | HR@1 | 0.6277826725 | 0.0025750732 | 0.6243171806 | 0.6304845815 | 0.0061674009 |

## Comparisons

| comparison | seed | delta HR@1 | delta NDCG@5 | delta MRR |
|---|---:|---:|---:|---:|
| N-K0 minus M1 | 42 | 0.0227312775 | 0.0103051362 | 0.0137885462 |
| N-K0 minus M1 | 43 | 0.0207929515 | 0.0102080938 | 0.0135535977 |
| N-K0 minus M1 | 44 | 0.0103964758 | 0.0036748076 | 0.0050102790 |
| N-K0 minus SASRec exp-match | 42 | 0.2766519824 | 0.1536035485 | 0.2023788546 |
| N-K0 minus SASRec exp-match | 43 | 0.2879295154 | 0.1604825262 | 0.2114008811 |
| N-K0 minus SASRec exp-match | 44 | 0.2851101322 | 0.1567550235 | 0.2066108664 |
| SASRec high s3000 minus N-K0 | 42 | 0.0777092511 | 0.0398598917 | 0.0528252570 |
| SASRec high s3000 minus N-K0 | 43 | 0.0858149780 | 0.0426440955 | 0.0566196769 |
| SASRec high s3000 minus N-K0 | 44 | 0.0921585903 | 0.0463357094 | 0.0614948605 |

## Interpretation

The main ranking and sample-efficiency directions are stable across seeds
42/43/44. N-K0 remains above M1 on fixed popmatch ranking, and N-K0 remains far
above the roughly exposure-matched SASRec s23 diagnostic. SASRec high s3000
also remains above N-K0 across all three seeds, but this row belongs to a
separate high-exposure budget regime.

Y-K0 remains the dedicated binary preference model tracked for this stage. Its
binary F1 varies by less than 0.01 across the three seeds. Y-K0's candidate
ranking scores remain weaker and more variable than N-K0 because that ranking
uses `P(Yes)` over candidates rather than the N-task candidate-label objective.

## Boundary

This is a three-seed stability diagnostic, not a strict statistical
significance study and not a compute/capacity-matched LLM-vs-SASRec comparison.
Candidate files are fixed at `k5_popmatch_seed42`; changing candidate
generation would define a different robustness stage.
