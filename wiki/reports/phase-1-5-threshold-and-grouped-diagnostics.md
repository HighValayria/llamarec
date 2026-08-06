---
title: "Phase 1.5 Threshold and Grouped Diagnostics"
type: report
status: current
authority: descriptive
source: mixed
created: 2026-08-06
updated: 2026-08-06
last_verified: 2026-08-06
related_code:
  - src/analysis/threshold_comparison.py
  - src/analysis/grouped_error_analysis.py
  - src/analysis/threshold_calibration.py
  - src/analysis/README.md
  - tests/test_analysis_outputs.py
  - configs/experiment.yaml
---

# Phase 1.5 Threshold and Grouped Diagnostics

## Scope

This report records Phase 1.5 STEP B/C results for MovieLens-1M using existing
Base, Y-K0, N-K0, M0, M1, and M2 prediction outputs. No new model training was
performed for this stage.

STEP B separates binary evaluation into three explicit views:

- threshold-free AUC;
- fixed threshold `0.5`;
- validation-calibrated best-F1 threshold.

STEP C joins prediction files back to fixed Y samples, fixed N candidate records,
and full-sequence-derived user/movie statistics, then reports grouped binary and
ranking diagnostics.

## Evidence

Code and local verification:

- Commit `e8f3148 analysis: add grouped error diagnostics`.
- `C:\Users\33967\AppData\Local\Programs\Python\Python312\python.exe -m pytest tests\test_analysis_outputs.py --basetemp .pytest_tmp`: `5 passed`.
- `C:\Users\33967\AppData\Local\Programs\Python\Python312\python.exe tools\stage_guard.py`: `0 error(s), 0 warning(s)`.

Cloud output reports:

- `/root/llamarec/outputs/calibration/movielens-1m/threshold_comparison/threshold_comparison.md`, generated `2026-08-06T14:27:02.802653+00:00`.
- `/root/llamarec/outputs/error_analysis/movielens-1m/grouped/test_grouped_error_analysis.md`, generated `2026-08-06T14:48:31.135824+00:00`.
- `/root/llamarec/outputs/error_analysis/movielens-1m/grouped/valid_grouped_error_analysis.md`, generated `2026-08-06T14:51:49.583098+00:00`.

Cloud run names:

- Y-K0: `pool200k_1m_y_1500`
- N-K0: `pool200k_1m_n_1500`
- M0: `pool200k_1m_m_1500`
- M1: `diag_m1_1m_m_200k_3000`
- M2: `diag_m2_1m_m_y2n1_1500`

## STEP B Binary Threshold Comparison

STEP B confirms that binary metrics must not be mixed across threshold regimes.
AUC is threshold-free; F1 and accuracy depend strongly on the selected threshold.

### Test Split

| model | auc | fixed_0.5_f1 | calibrated_threshold | calibrated_f1 | calibrated_accuracy |
|---|---:|---:|---:|---:|---:|
| Base | 0.6204640889 | 0.7055389804 | 0.0953494649 | 0.7414450771 | 0.5948544699 |
| Y-K0 | 0.7690966770 | 0.7799722571 | 0.4073334000 | 0.7830635118 | 0.6981981982 |
| M0 | 0.7234059346 | 0.7629621151 | 0.5312093734 | 0.7687245753 | 0.6651074151 |
| M1 | 0.7668964028 | 0.7276403795 | 0.3208213008 | 0.7817788523 | 0.7028759529 |
| M2 | 0.7246538748 | 0.7674552799 | 0.6224593312 | 0.7734258800 | 0.6832986833 |

### Validation Split

| model | auc | fixed_0.5_f1 | calibrated_threshold | calibrated_f1 | calibrated_accuracy |
|---|---:|---:|---:|---:|---:|
| Base | 0.6223513215 | 0.7091932458 | 0.0953494649 | 0.7422829168 | 0.5960746305 |
| Y-K0 | 0.7702133449 | 0.7801849898 | 0.4073334000 | 0.7857975746 | 0.7032549875 |
| M0 | 0.7209320725 | 0.7609823961 | 0.5312093734 | 0.7659929848 | 0.6605282287 |
| M1 | 0.7668458780 | 0.7205323194 | 0.3208213008 | 0.7816474504 | 0.7032549875 |
| M2 | 0.7313839925 | 0.7686905791 | 0.6224593312 | 0.7748727441 | 0.6856473629 |

Interpretation:

- Y-K0 remains the strongest dedicated binary model.
- M1 nearly matches Y-K0 after validation threshold calibration.
- M1's fixed `0.5` F1 underestimates its binary capacity because its calibrated
  threshold is much lower (`0.3208213008`).
- M2's Y-heavy sampling does not improve the overall multi-task tradeoff.

## STEP C Grouped Diagnostics

### Binary Overview

| split | model | calibrated_f1 | accuracy | fp | fn |
|---|---|---:|---:|---:|---:|
| validation | Base | 0.7422829168 | 0.5960746305 | 4908 | 93 |
| validation | Y-K0 | 0.7857975746 | 0.7032549875 | 3118 | 556 |
| validation | M0 | 0.7659929848 | 0.6605282287 | 3787 | 416 |
| validation | M1 | 0.7816474504 | 0.7032549875 | 2955 | 719 |
| validation | M2 | 0.7748727441 | 0.6856473629 | 3295 | 597 |
| test | Base | 0.7414450771 | 0.5948544699 | 4561 | 116 |
| test | Y-K0 | 0.7830635118 | 0.6981981982 | 2950 | 534 |
| test | M0 | 0.7687245753 | 0.6651074151 | 3469 | 397 |
| test | M1 | 0.7817788523 | 0.7028759529 | 2752 | 678 |
| test | M2 | 0.7734258800 | 0.6832986833 | 3074 | 582 |

Binary conclusion:

- Validation and test agree: Y-K0 and M1 are the first tier.
- M1 has slightly lower F1 than Y-K0 but slightly higher test accuracy.
- M1 reduces M0's Yes bias: M1 has fewer false positives than M0 under the
  calibrated threshold, while accepting more false negatives.
- `history_length_bucket` is not informative for Y-task test diagnostics because
  prompt history is capped at 10 and all test rows fall into `6-10`.

### Ranking Overview

| split | model | hr_at_1 | ndcg_at_5 | mrr | mean_rank | mean_margin |
|---|---|---:|---:|---:|---:|---:|
| validation | Base | 0.3170044053 | 0.6643498145 | 0.5541439060 | 2.5295154185 | -0.0774862045 |
| validation | Y-K0 | 0.3171806167 | 0.6578250671 | 0.5462466960 | 2.6225550661 | -0.0937135883 |
| validation | N-K0 | 0.7215859031 | 0.8797052759 | 0.8387371512 | 1.4398237885 | 0.3826833866 |
| validation | M0 | 0.6747136564 | 0.8583709933 | 0.8102613803 | 1.5272246696 | 0.3027310381 |
| validation | M1 | 0.7064317181 | 0.8721296338 | 0.8287107195 | 1.4777092511 | 0.3475351601 |
| validation | M2 | 0.6650220264 | 0.8528146927 | 0.8029397944 | 1.5566519824 | 0.2415836704 |
| test | Base | 0.3166519824 | 0.6630782998 | 0.5525168869 | 2.5388546256 | -0.0776478919 |
| test | Y-K0 | 0.3048458150 | 0.6503957066 | 0.5365521292 | 2.6710132159 | -0.0997644025 |
| test | N-K0 | 0.7189427313 | 0.8773024023 | 0.8356446402 | 1.4577973568 | 0.3705203151 |
| test | M0 | 0.6717180617 | 0.8561638472 | 0.8073920705 | 1.5418502203 | 0.2936281769 |
| test | M1 | 0.6949779736 | 0.8673895627 | 0.8223230543 | 1.4925110132 | 0.3309466066 |
| test | M2 | 0.6548017621 | 0.8474343945 | 0.7958237885 | 1.5834361233 | 0.2372050099 |

Ranking conclusion:

- N-K0 is still the strongest ranking model.
- M1 is the best multi-task ranking variant and clearly improves over M0/M2.
- M1 remains below N-K0, so the current multi-task model is a tradeoff rather
  than a full positive transfer result.
- Y-K0 ranking is not a substitute for N-K0. It uses `P(Yes)` and therefore
  behaves like preference scoring, not next-interaction transition scoring.

## Group Effects

Target popularity is the strongest grouped ranking diagnostic.

| split | model | hr_at_1_popularity_le_10 | hr_at_1_popularity_gt_500 |
|---|---|---:|---:|
| validation | N-K0 | 0.0666666667 | 0.8156407035 |
| validation | M1 | 0.2000000000 | 0.8084170854 |
| validation | M0 | 0.0666666667 | 0.7883165829 |
| validation | M2 | 0.0000000000 | 0.8005653266 |
| test | N-K0 | 0.1923076923 | 0.8167150694 |
| test | M1 | 0.1923076923 | 0.8002581478 |
| test | M0 | 0.1538461538 | 0.7867053888 |
| test | M2 | 0.1923076923 | 0.7873507583 |

Interpretation:

- Ranking performance is much stronger on highly popular target items.
- Very low-popularity buckets are small, but both validation and test show the
  same direction: rare target items are the main weakness.
- Future robustness work should treat target popularity as a primary diagnostic
  axis before claiming general ranking improvements.

Y-K0 ranking is rating-sensitive.

| split | rating_1_hr_at_1 | rating_5_hr_at_1 |
|---|---:|---:|
| validation | 0.1077844311 | 0.4990006662 |
| test | 0.1043956044 | 0.4668874172 |

Interpretation:

- Y-K0's ranking improves as target rating increases.
- This is expected because Y-K0 scores candidate items through the Yes/No
  preference interface.
- This reinforces the project constraint that Y and N measure different
  supervision semantics.

## Final Stage 1 Conclusion

Phase 1.5 STEP B/C supports four durable conclusions:

- Binary reporting must remain split into AUC, fixed threshold, and calibrated
  threshold views.
- M1 is the current best multi-task diagnostic model.
- M1 nearly matches Y-K0 on calibrated binary metrics and is the best M variant
  on ranking, but it does not surpass N-K0.
- Popularity-conditioned ranking diagnostics are necessary for future claims,
  because high-popularity and low-popularity targets show very different
  behavior.

## Recommended Next Work

- Do not launch M3, KAR, hard negatives, SASRec, 7B, multi-seed, or MovieLens-32M
  full training as part of this stage.
- If Phase 2 continues, first define candidate-size and candidate-order
  robustness protocols, including separate output paths and explicit tokenizer
  label checks.
- Preserve M1 as the current multi-task baseline for comparison against any
  future Phase 2 model.
