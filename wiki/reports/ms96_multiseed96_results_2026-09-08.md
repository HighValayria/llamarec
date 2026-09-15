---
title: MS96 Multiseed Results Freeze
type: report
status: current
authority: descriptive
source: mixed
created: 2026-09-08
updated: 2026-09-08
last_verified: 2026-09-08
related_code:
  - .agent/exposure_scaling/multiseed96/commands/multiseed96_queue.sh
  - artifacts/multiseed96/seed43/validation_summary.txt
  - artifacts/multiseed96/seed43/test_summary.txt
  - artifacts/multiseed96/seed44/validation_summary.txt
  - artifacts/multiseed96/seed44/test_summary.txt
  - outputs/y/movielens-1m/exposure_y_s12000/popmatch_eval
  - outputs/n/movielens-1m/exposure_n_s12000/popmatch_eval
  - outputs/m/movielens-1m/exposure_m1_s24000/popmatch_eval
superseded_by:
---

# MS96 Multiseed Results Freeze

This report records the seed42/43/44 MovieLens-1M MS96 evidence available as of
2026-09-08. It is descriptive only. It does not launch training or inference and
does not change the validation-first decision rule.

## Scope

- Models: `Y96`, `N96`, `M1-96`.
- Seeds: `42`, `43`, `44`.
- Main protocol: PopMatch `k5`.
- Robustness protocol: hard-candidate `k20_seed42` and `k50_seed42`.
- Decision rule: validation metrics are used for model/protocol decisions; test
  metrics are report-only after the decision boundary is fixed.

## Evidence Location

Seed43 and seed44 were trained/evaluated on separate machines. Their lightweight
results are preserved in GitHub under:

- `artifacts/multiseed96/seed43/validation_summary.txt`
- `artifacts/multiseed96/seed43/test_summary.txt`
- `artifacts/multiseed96/seed43/artifact_index.txt`
- `artifacts/multiseed96/seed44/validation_summary.txt`
- `artifacts/multiseed96/seed44/test_summary.txt`
- `artifacts/multiseed96/seed44/artifact_index.txt`

For cross-machine summaries, the `artifacts/multiseed96` files are the reliable
lightweight synchronization source. Raw `outputs/` paths are local to the machine
that ran each seed. A single-machine scan of `outputs/` can therefore report
false `MISSING` values for another machine's seed even when the lightweight
GitHub artifacts are complete.

## Evaluation Semantics

- `Y96` native metric: binary `AUC`, `F1`, `Accuracy`.
- `Y96` as ranker: PopMatch candidate ranking by `P(Yes)`, reported as
  `HR@1`, `NDCG@5`, `MRR`.
- `N96` native metric: candidate ranking, reported as `HR@1`, `NDCG@5`, `MRR`.
- `M1-96` native metrics: both M-Y binary and M-N ranking.
- `HR@5` under `k5` is omitted in the comparison narrative because it is
  saturated at 1.0 in this protocol.

## Main K5 Validation

| Run | Seed | Samples | AUC | F1 | Accuracy | HR@1 | NDCG@5 | MRR |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Y96 | 42 | 12381 | 0.7843504067 | 0.7783174665 | 0.7235279864 | 0.2211453744 | 0.6030699894 | 0.4741791483 |
| N96 | 42 | 5675 |  |  |  | 0.6237885463 | 0.8302923694 | 0.7732422907 |
| M1-96 | 42 | 12381 | 0.7868352749 | 0.7838427948 | 0.7281318149 | 0.6234361233 | 0.8291402759 | 0.7717533040 |
| Y96 | 43 | 12381 | 0.7790875354 | 0.7832388154 | 0.7221549148 | 0.2052863436 | 0.5917630391 | 0.4594801762 |
| N96 | 43 | 5675 |  |  |  | 0.6280176211 | 0.8321566054 | 0.7757151248 |
| M1-96 | 43 | 12381 | 0.7881196538 | 0.7868914807 | 0.7284548906 | 0.6253744493 | 0.8303896743 | 0.7734008811 |
| Y96 | 44 | 12381 | 0.7821654924 | 0.7800167386 | 0.7240126000 | 0.2045814978 | 0.5915151746 | 0.4591453744 |
| N96 | 44 | 5675 |  |  |  | 0.6352422907 | 0.8345124329 | 0.7789574156 |
| M1-96 | 44 | 12381 | 0.7851159778 | 0.7844838426 | 0.7231241418 | 0.6206167401 | 0.8291123175 | 0.7716211454 |

## Main K5 Test

Test is report-only.

| Run | Seed | Samples | AUC | F1 | Accuracy | HR@1 | NDCG@5 | MRR |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Y96 | 42 | 11544 | 0.7853511126 | 0.7780238029 | 0.7221067221 | 0.2065198238 | 0.5921565513 | 0.4600528634 |
| N96 | 42 | 5675 |  |  |  | 0.6100440529 | 0.8218966233 | 0.7622026432 |
| M1-96 | 42 | 11544 | 0.7864837284 | 0.7835646558 | 0.7271309771 | 0.5973568282 | 0.8162307888 | 0.7546490455 |
| Y96 | 43 | 11544 | 0.7815048040 | 0.7785762712 | 0.7170824671 | 0.1970044053 | 0.5850320200 | 0.4508516887 |
| N96 | 43 | 5675 |  |  |  | 0.6139207048 | 0.8237104382 | 0.7646196769 |
| M1-96 | 43 | 11544 | 0.7849652028 | 0.7845401440 | 0.7252252252 | 0.6061674009 | 0.8191371392 | 0.7586108664 |
| Y96 | 44 | 11544 | 0.7802665958 | 0.7769764407 | 0.7187283437 | 0.1970044053 | 0.5861916201 | 0.4522320117 |
| N96 | 44 | 5675 |  |  |  | 0.6105726872 | 0.8220727347 | 0.7624375918 |
| M1-96 | 44 | 11544 | 0.7857056225 | 0.7875151679 | 0.7269577270 | 0.6005286344 | 0.8172676643 | 0.7560587372 |

## Hard-Candidate Validation

| Run | Seed | Variant | Samples | HR@1 | NDCG@5 | MRR |
| --- | ---: | --- | ---: | ---: | ---: | ---: |
| M1-96 | 42 | k20_seed42 | 5675 | 0.2766519824 | 0.3940015350 | 0.4186302037 |
| N96 | 42 | k20_seed42 | 5675 | 0.3890748899 | 0.5209809566 | 0.5248862838 |
| M1-96 | 42 | k50_seed42 | 5675 | 0.0787665198 | 0.1054866460 | 0.1593155373 |
| N96 | 42 | k50_seed42 | 5675 | 0.0958590308 | 0.1344422226 | 0.1851448975 |
| M1-96 | 43 | k20_seed42 | 5675 | 0.1955947137 | 0.2533107435 | 0.3240114881 |
| N96 | 43 | k20_seed42 | 5675 | 0.2770044053 | 0.3797155065 | 0.4152810343 |
| M1-96 | 43 | k50_seed42 | 5675 | 0.0752422907 | 0.0938652543 | 0.1450338396 |
| N96 | 43 | k50_seed42 | 5675 | 0.0785903084 | 0.0985437212 | 0.1566889508 |
| M1-96 | 44 | k20_seed42 | 5675 | 0.1941850220 | 0.2450496026 | 0.3228180313 |
| N96 | 44 | k20_seed42 | 5675 | 0.2452863436 | 0.3509868581 | 0.3899550194 |
| M1-96 | 44 | k50_seed42 | 5675 | 0.0690748899 | 0.0906771623 | 0.1418256458 |
| N96 | 44 | k50_seed42 | 5675 | 0.0794713656 | 0.1006068901 | 0.1598371854 |

## Hard-Candidate Test

Test is report-only.

| Run | Seed | Variant | Samples | HR@1 | NDCG@5 | MRR |
| --- | ---: | --- | ---: | ---: | ---: | ---: |
| M1-96 | 42 | k20_seed42 | 5675 | 0.2611453744 | 0.3755105073 | 0.4040452486 |
| N96 | 42 | k20_seed42 | 5675 | 0.3758590308 | 0.5014430507 | 0.5099145579 |
| M1-96 | 42 | k50_seed42 | 5675 | 0.0690748899 | 0.0975277110 | 0.1511870614 |
| N96 | 42 | k50_seed42 | 5675 | 0.0829955947 | 0.1253057918 | 0.1746050600 |
| M1-96 | 43 | k20_seed42 | 5675 | 0.1971806167 | 0.2488457065 | 0.3206260258 |
| N96 | 43 | k20_seed42 | 5675 | 0.2688986784 | 0.3710362625 | 0.4069725230 |
| M1-96 | 43 | k50_seed42 | 5675 | 0.0625550661 | 0.0862598928 | 0.1363257461 |
| N96 | 43 | k50_seed42 | 5675 | 0.0676651982 | 0.0906269352 | 0.1479518054 |
| M1-96 | 44 | k20_seed42 | 5675 | 0.1908370044 | 0.2387944363 | 0.3171560135 |
| N96 | 44 | k20_seed42 | 5675 | 0.2373568282 | 0.3399677881 | 0.3805081923 |
| M1-96 | 44 | k50_seed42 | 5675 | 0.0592070485 | 0.0835008599 | 0.1346546316 |
| N96 | 44 | k50_seed42 | 5675 | 0.0704845815 | 0.0935959206 | 0.1533174453 |

## Derived Deltas

Positive binary deltas mean `M1-96 - Y96`. Positive ranking deltas mean
`N96 - M1-96`.

### Binary Validation Deltas

| Seed | AUC | F1 | Accuracy |
| ---: | ---: | ---: | ---: |
| 42 | +0.0024848682 | +0.0055253283 | +0.0046038284 |
| 43 | +0.0090321184 | +0.0036526654 | +0.0062999758 |
| 44 | +0.0029504854 | +0.0044671040 | -0.0008884581 |
| Mean | +0.0048224907 | +0.0045483659 | +0.0033384487 |

### Binary Test Deltas

| Seed | AUC | F1 | Accuracy |
| ---: | ---: | ---: | ---: |
| 42 | +0.0011326158 | +0.0055408528 | +0.0050242550 |
| 43 | +0.0034603988 | +0.0059638728 | +0.0081427581 |
| 44 | +0.0054390267 | +0.0105387272 | +0.0082293832 |
| Mean | +0.0033440137 | +0.0073478176 | +0.0071321321 |

### K5 Ranking Validation Deltas

| Seed | HR@1 | NDCG@5 | MRR |
| ---: | ---: | ---: | ---: |
| 42 | +0.0003524229 | +0.0011520935 | +0.0014889868 |
| 43 | +0.0026431718 | +0.0017669311 | +0.0023142438 |
| 44 | +0.0146255507 | +0.0054001154 | +0.0073362702 |
| Mean | +0.0058737151 | +0.0027730467 | +0.0037131669 |

### K5 Ranking Test Deltas

| Seed | HR@1 | NDCG@5 | MRR |
| ---: | ---: | ---: | ---: |
| 42 | +0.0126872247 | +0.0056658345 | +0.0075535977 |
| 43 | +0.0077533040 | +0.0045732989 | +0.0060088106 |
| 44 | +0.0100440529 | +0.0048050704 | +0.0063788546 |
| Mean | +0.0101615272 | +0.0050147346 | +0.0066470876 |

### Hard-Candidate Validation Deltas

| Variant | Metric | Seed42 | Seed43 | Seed44 | Mean |
| --- | --- | ---: | ---: | ---: | ---: |
| k20_seed42 | HR@1 | +0.1124229075 | +0.0814096916 | +0.0511013216 | +0.0816446402 |
| k20_seed42 | NDCG@5 | +0.1269794216 | +0.1264047631 | +0.1059372555 | +0.1197738134 |
| k20_seed42 | MRR | +0.1062560801 | +0.0912695462 | +0.0671369880 | +0.0882208714 |
| k50_seed42 | HR@1 | +0.0170925110 | +0.0033480176 | +0.0103964758 | +0.010278, approx |
| k50_seed42 | NDCG@5 | +0.0289555766 | +0.0046784669 | +0.0099297278 | +0.0145212571 |
| k50_seed42 | MRR | +0.0258293602 | +0.0116551112 | +0.0180115395 | +0.0184986703 |

### Hard-Candidate Test Deltas

| Variant | Metric | Seed42 | Seed43 | Seed44 | Mean |
| --- | --- | ---: | ---: | ---: | ---: |
| k20_seed42 | HR@1 | +0.1147136564 | +0.0717180617 | +0.0465198238 | +0.0776505139 |
| k20_seed42 | NDCG@5 | +0.1259325434 | +0.1221905560 | +0.1011733518 | +0.1164321504 |
| k20_seed42 | MRR | +0.1058693094 | +0.0863464972 | +0.0633521788 | +0.0851893285 |
| k50_seed42 | HR@1 | +0.0139207048 | +0.0051101322 | +0.0112775330 | +0.0101027900 |
| k50_seed42 | NDCG@5 | +0.0277780808 | +0.0043670424 | +0.0100950607 | +0.0140800613 |
| k50_seed42 | MRR | +0.0234179986 | +0.0116260593 | +0.0186628137 | +0.0179022905 |

## Result Interpretation Boundary

Supported by seed42/43/44:

- `M1-96` does not show observable Y-side binary degradation relative to `Y96`.
  Across the three seeds, `M1-96 - Y96` is positive for AUC and F1 on both
  validation and test. Accuracy is positive for seed42/43 and slightly negative
  for seed44 validation.
- On the main `k5` N-ranking protocol, `M1-96` is close to but still below
  `N96`. The validation mean gap is small: approximately `+0.0059 HR@1`,
  `+0.0028 NDCG@5`, and `+0.0037 MRR` for `N96 - M1-96`.
- On hard-candidate `k20/k50`, `N96` consistently outperforms `M1-96`.
  The `k20` gap is materially larger than the `k50` gap.

Not supported by this evidence alone:

- Do not claim that `M1-96` globally beats both specialized models.
- Do not claim established positive transfer without uncertainty analysis and
  a wording boundary. A safer phrasing is no detectable Y-side degradation with
  near-parity on the main `k5` N-ranking protocol.
- Do not use report-only test metrics to retroactively change model-selection
  decisions.

## Data Completeness Note

The lightweight seed43/44 result data are complete in `artifacts/multiseed96`.
Earlier `MISSING` output came from scanning local `outputs/` on a machine that
did not contain the other seed's raw local outputs, and from an incorrect
directory assumption using `*_popmatch_eval` instead of the actual
`*/popmatch_eval` directory layout for seed43/44 k5 test files.
