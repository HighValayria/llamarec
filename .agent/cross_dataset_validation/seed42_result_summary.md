# Amazon Musical Instruments Seed42 Result Summary

## Status

Seed42 full-test cross-dataset run is complete. All ten planned
`test_metrics.json` files were reported by the cloud queue on 2026-08-22.

Dataset: `amazon-musical-instruments`

Test samples per ranking run: 57,439

## Metrics

| model | candidate set | AUC | F1 | Accuracy | HR@1 | NDCG@5 | MRR |
|---|---|---:|---:|---:|---:|---:|---:|
| Base | random-k5 | 0.6086838368 | 0.3978976056 | 0.3538525817 | 0.3387419697 | 0.6734956068 | 0.5664174167 |
| Base | popmatch-k5 | 0.6084359088 | 0.3990274739 | 0.3545315275 | 0.3573007887 | 0.6829490861 | 0.5789568064 |
| Y-K0 | random-k5 | 0.4902616517 | 0.9059705193 | 0.8283137774 | 0.2211563572 | 0.6029133520 | 0.4739668750 |
| Y-K0 | popmatch-k5 | 0.4902616517 | 0.9059705193 | 0.8283137774 | 0.2297916050 | 0.6099650726 | 0.4830304033 |
| N-K0 | random-k5 | unavailable | unavailable | unavailable | 0.5172269712 | 0.7703895001 | 0.6943197711 |
| N-K0 | popmatch-k5 | unavailable | unavailable | unavailable | 0.4668779053 | 0.7420073620 | 0.6569789980 |
| M1 | random-k5 | 0.5128936310 | 0.9032109784 | 0.8240486055 | 0.5160431066 | 0.7693689176 | 0.6930160692 |
| M1 | popmatch-k5 | 0.5128936310 | 0.9032109784 | 0.8240486055 | 0.4581730183 | 0.7383638504 | 0.6520839499 |
| SASRec-exp-match | random-k5 | unavailable | unavailable | unavailable | 0.4496596389 | 0.7293161170 | 0.6405569387 |
| SASRec-exp-match | popmatch-k5 | unavailable | unavailable | unavailable | 0.1756646181 | 0.5685149085 | 0.4295165306 |

## Primary PopMatch Comparisons

| comparison | delta HR@1 | delta NDCG@5 | delta MRR |
|---|---:|---:|---:|
| N-K0 minus M1 | 0.0087048869 | 0.0036435116 | 0.0048950481 |
| N-K0 minus SASRec-exp-match | 0.2912132871 | 0.1734924534 | 0.2274624674 |
| N-K0 minus Base | 0.1095771166 | 0.0590582759 | 0.0780221917 |
| N-K0 minus Y-K0 | 0.2370863002 | 0.1320422893 | 0.1739485947 |

## Random-k5 Supplemental Comparisons

| comparison | delta HR@1 | delta NDCG@5 | delta MRR |
|---|---:|---:|---:|
| N-K0 minus M1 | 0.0011838646 | 0.0010205825 | 0.0013037019 |
| N-K0 minus SASRec-exp-match | 0.0675673323 | 0.0410733831 | 0.0537628325 |

## Candidate Set Effect

| model | popmatch HR@1 minus random HR@1 | popmatch NDCG@5 minus random NDCG@5 | popmatch MRR minus random MRR |
|---|---:|---:|---:|
| Base | 0.0185588189 | 0.0094534793 | 0.0125393896 |
| N-K0 | -0.0503490660 | -0.0283821382 | -0.0373407731 |
| M1 | -0.0578700883 | -0.0310050672 | -0.0409321193 |
| SASRec-exp-match | -0.2739950208 | -0.1608012085 | -0.2110404081 |

## Direct Answers

- `cross_dataset_direction_replicates_on_popmatch`: yes, with a small N-K0 over M1 margin and a large N-K0 over SASRec-exp-match margin.
- `n_k0_above_m1_on_popmatch`: yes by HR@1, NDCG@5, and MRR.
- `n_k0_above_sasrec_exp_match_on_popmatch`: yes by a large margin.
- `random_k5_primary_claim_suitable`: no. Random-k5 leaves N-K0 and M1 nearly tied, so it should be treated as an easier/supplemental condition.
- `need_seed43_44_now`: not required before seed42 synthesis; consider only if the small N-K0 vs M1 margin needs robustness evidence.

## Interpretation

The Amazon Musical Instruments seed42 result supports the main cross-dataset
direction under PopMatch-k5: the N-task specialist remains ahead of the
multitask M1 model, and it is far ahead of the sample-exposure-matched SASRec
baseline. The N-K0 versus M1 margin is much narrower than on MovieLens-1M, so
the durable claim should be phrased as directionally replicated rather than as
a large cross-dataset specialist advantage.

Random-k5 is useful as a supplemental/easier condition but should not carry the
primary claim: N-K0 and M1 are nearly tied on Random-k5. The stronger evidence
comes from PopMatch-k5, where the popularity shortcut is reduced and SASRec
drops sharply relative to Random-k5.

## Boundary

This is a single Amazon seed42 full-test result. It does not establish
multi-seed Amazon stability. Do not claim seed stability unless seed43/44 are
run.
