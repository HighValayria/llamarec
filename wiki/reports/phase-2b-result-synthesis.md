---
title: "Phase 2B Result Synthesis"
type: report
status: current
authority: descriptive
source: mixed
created: 2026-08-09
updated: 2026-08-09
last_verified: 2026-08-09
related_code:
  - src/analysis/phase2b_result_synthesis.py
  - src/analysis/README.md
  - tests/test_analysis_outputs.py
  - wiki/reports/phase-1-5-threshold-and-grouped-diagnostics.md
  - wiki/reports/phase-2a-ranking-robustness.md
---

# Phase 2B Result Synthesis

## Scope

Phase 2B synthesizes existing MovieLens-1M Phase 1.5 diagnostics and Phase 2A
ranking robustness outputs into paper-ready tables and cautious interpretation
text. It does not train new models or recompute inference.

The stage added `src/analysis/phase2b_result_synthesis.py`, which reads:

```text
outputs/calibration/movielens-1m/threshold_comparison/threshold_comparison.json
outputs/error_analysis/movielens-1m/grouped/test_grouped_error_analysis.json
outputs/phase2a/ranking_robustness/phase2a_ranking_robustness_metrics.json
outputs/phase2a/ranking_robustness/phase2a_ranking_robustness_comparison.csv
```

Cloud output:

```text
/root/llamarec/outputs/phase2b/result_synthesis/phase2b_result_synthesis.md
```

## Generated Artifacts

The Phase 2B synthesis writes:

```text
phase2b_binary_calibrated_test.csv
phase2b_canonical_ranking_test.csv
phase2b_robustness_test.csv
phase2b_robustness_key_deltas.csv
phase2b_paper_ready_claims.json
phase2b_result_synthesis.md
```

The report was generated from existing analysis artifacts only. It preserves the
candidate-set context for robustness metrics and does not mix canonical
5-candidate rows into explicit k20/k50 variant comparisons.

## Paper-Ready Claims

The generated report records six claims:

- Y-K0 gives the strongest validation-calibrated binary F1 on the test split:
  F1 `0.7831`, AUC `0.7691`.
- M1 nearly matches Y-K0 after validation-threshold calibration: Y-K0 F1
  `0.7831`, M1 F1 `0.7818`.
- N-K0 is the strongest canonical next-item ranking model: HR@1 `0.7189`,
  NDCG@5 `0.8773`, MRR `0.8356`.
- M1 is the strongest multi-task ranking variant but remains below N-K0:
  N-K0 HR@1 `0.7189`, M1 HR@1 `0.6950`, gap `0.0240`.
- The N-K0 advantage over M1 grows under k50 candidate-size stress: N-K0 k50
  HR@1 `0.1995`, M1 k50 HR@1 `0.1219`.
- Candidate order perturbation has small effects compared with candidate-size
  expansion: the maximum absolute k20 order HR@1 delta among reported models is
  `0.0065`.

## Key Tables

### Validation-Calibrated Binary Test Metrics

| model | threshold | auc | f1 | accuracy |
|---|---:|---:|---:|---:|
| Base | 0.0953494649 | 0.6204640889 | 0.7414450771 | 0.5948544699 |
| Y-K0 | 0.4073334000 | 0.7690966770 | 0.7830635118 | 0.6981981982 |
| M0 | 0.5312093734 | 0.7234059346 | 0.7687245753 | 0.6651074151 |
| M1 | 0.3208213008 | 0.7668964028 | 0.7817788523 | 0.7028759529 |
| M2 | 0.6224593312 | 0.7246538748 | 0.7734258800 | 0.6832986833 |

### Canonical 5-Candidate Ranking Test Metrics

| model | HR@1 | NDCG@5 | MRR | mean_margin |
|---|---:|---:|---:|---:|
| Base | 0.3166519824 | 0.6630782998 | 0.5525168869 | -0.0776478919 |
| Y-K0 | 0.3048458150 | 0.6503957066 | 0.5365521292 | -0.0997644025 |
| N-K0 | 0.7189427313 | 0.8773024023 | 0.8356446402 | 0.3705203151 |
| M0 | 0.6717180617 | 0.8561638472 | 0.8073920705 | 0.2936281769 |
| M1 | 0.6949779736 | 0.8673895627 | 0.8223230543 | 0.3309466066 |
| M2 | 0.6548017621 | 0.8474343945 | 0.7958237885 | 0.2372050099 |

### Phase 2A Robustness Test Metrics

| model | variant | HR@1 | HR@5 | NDCG@5 | MRR |
|---|---|---:|---:|---:|---:|
| Base | k5_perm_seed43 | 0.3217621145 | 1.0000000000 | 0.6654236813 | 0.5556710720 |
| Base | k20_seed42 | 0.0690748899 | 0.2928634361 | 0.1811710274 | 0.2088236555 |
| Base | k50_seed42 | 0.0292511013 | 0.1210572687 | 0.0744893997 | 0.1057905143 |
| N-K0 | k5_perm_seed43 | 0.7150660793 | 1.0000000000 | 0.8756450438 | 0.8334302496 |
| N-K0 | k20_seed42 | 0.4163876652 | 0.7859030837 | 0.6157234085 | 0.5818276991 |
| N-K0 | k50_seed42 | 0.1994713656 | 0.4387665198 | 0.3250292649 | 0.3241909857 |
| M1 | k5_perm_seed43 | 0.6932158590 | 1.0000000000 | 0.8665986756 | 0.8212657856 |
| M1 | k20_seed42 | 0.3711013216 | 0.7022026432 | 0.5482297492 | 0.5285907582 |
| M1 | k50_seed42 | 0.1219383260 | 0.3064317181 | 0.2149517589 | 0.2346155309 |

## Interpretation

Phase 2B supports a tradeoff interpretation. Dedicated Y supervision remains
strongest for calibrated preference prediction. Dedicated N supervision remains
strongest for next-interaction ranking. M1 is the best current multi-task
compromise: it approaches Y-K0 on calibrated binary metrics and is the strongest
M ranking variant, but it does not replace N-K0.

Phase 2A robustness results make the boundary sharper. Candidate order
perturbation is small, while larger candidate sets sharply reduce HR@1 and
increase the N-K0 versus M1 gap. Ranking claims should therefore report the
candidate-set size and should not rely only on the canonical 5-candidate
setting.

## Claim Boundaries

- Do not claim that M1 surpasses the best single-task models.
- Do not treat Y-K0 `P(Yes)` ranking as next-interaction ranking.
- Do not mix canonical 5-candidate metrics with explicit k20/k50 variant
  metrics unless the candidate context is named.
- Treat cold-item ranking as an unresolved weakness rather than a solved
  robustness result.

## Verification

Local verification for the Phase 2B script:

```text
C:\Users\33967\AppData\Local\Programs\Python\Python312\python.exe -m pytest tests\test_analysis_outputs.py --basetemp .pytest_tmp_phase2b_synthesis
8 passed in 0.45s
```

Stage guard after implementation:

```text
C:\Users\33967\AppData\Local\Programs\Python\Python312\python.exe tools\stage_guard.py
0 error(s), 0 warning(s)
```
