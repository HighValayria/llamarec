---
title: "Cross-dataset Validation"
type: report
status: current
authority: descriptive
source: mixed
created: 2026-08-22
updated: 2026-08-22
last_verified: 2026-08-22
related_code:
  - configs/experiment.yaml
  - src/data/preprocess.py
  - src/data/build_step2.py
  - src/data/split.py
  - src/eval/candidate_sets.py
  - src/inference/prompts.py
  - src/inference/base_zero_shot.py
  - src/inference/evaluate_y_adapter.py
  - src/inference/evaluate_n_adapter.py
  - src/inference/evaluate_m_adapter.py
  - src/train/train_y.py
  - src/train/train_n.py
  - src/train/train_m.py
  - src/baselines/sasrec.py
  - tests/test_amazon_reviews_preprocess.py
  - .agent/cross_dataset_validation/stage_synthesis.md
  - .agent/cross_dataset_validation/seed42_result_summary.md
superseded_by: null
---

# Cross-dataset Validation

## Status

The Cross-dataset Validation stage is complete for the current scope. The
selected second dataset is `amazon-musical-instruments`, built from
user-provided local Amazon Reviews 2023 5-core Musical_Instruments files.

The originally selected `Amazon-books` catalog source was rejected inside the
same stage because the supplied files were product metadata, not user-item
interaction logs.

## Protocol

Allowed Amazon inputs:

- interaction `user_id`
- interaction `parent_asin`
- interaction `rating`
- interaction `timestamp`
- metadata `parent_asin`
- metadata `title`

Excluded inputs:

- review text
- product descriptions
- brand/category/price fields
- images
- external product knowledge

The strict temporal contract is unchanged:

```text
history = interactions with timestamp < target_timestamp
```

Y labels use `rating >= 4 -> Yes`; N targets remain the actual next
full-sequence interaction, not the next positive interaction.

## Data Gate

Formal retained Amazon data:

| quantity | value |
|---|---:|
| users | 57,439 |
| items | 24,584 |
| interactions | 511,792 |
| Y train | 396,908 |
| Y validation | 57,442 |
| Y test | 57,442 |
| N train | 339,449 |
| N validation | 57,439 |
| N test | 57,439 |

The formal Y label distribution is 437,418 `Yes` and 74,374 `No`. No users
were skipped for insufficient legal N samples.

## Candidate Gate

Both fixed candidate protocols were generated for validation and test, with
57,439 records per split and five candidates per record.

| candidate set | validation rows | test rows | test mean abs popularity gap |
|---|---:|---:|---:|
| Random-k5 seed42 | 57,439 | 57,439 | 130.7513710197 |
| PopMatch-k5 seed42 | 57,439 | 57,439 | 29.3606869897 |

PopMatch-k5 reduced the test mean absolute popularity gap by about 77.5%
relative to Random-k5.

## Seed42 Results

Primary PopMatch-k5 ranking metrics:

| model | HR@1 | NDCG@5 | MRR |
|---|---:|---:|---:|
| Base | 0.3573007887 | 0.6829490861 | 0.5789568064 |
| Y-K0 | 0.2297916050 | 0.6099650726 | 0.4830304033 |
| N-K0 | 0.4668779053 | 0.7420073620 | 0.6569789980 |
| M1 | 0.4581730183 | 0.7383638504 | 0.6520839499 |
| SASRec-exp-match | 0.1756646181 | 0.5685149085 | 0.4295165306 |

Primary PopMatch-k5 comparisons:

| comparison | delta HR@1 | delta NDCG@5 | delta MRR |
|---|---:|---:|---:|
| N-K0 minus M1 | 0.0087048869 | 0.0036435116 | 0.0048950481 |
| N-K0 minus SASRec-exp-match | 0.2912132871 | 0.1734924534 | 0.2274624674 |
| N-K0 minus Base | 0.1095771166 | 0.0590582759 | 0.0780221917 |
| N-K0 minus Y-K0 | 0.2370863002 | 0.1320422893 | 0.1739485947 |

Random-k5 supplemental comparisons:

| comparison | delta HR@1 | delta NDCG@5 | delta MRR |
|---|---:|---:|---:|
| N-K0 minus M1 | 0.0011838646 | 0.0010205825 | 0.0013037019 |
| N-K0 minus SASRec-exp-match | 0.0675673323 | 0.0410733831 | 0.0537628325 |

## Interpretation

The Amazon Musical Instruments seed42 result directionally replicates the
MovieLens-1M PopMatch finding: N-K0 remains above M1 and far above the
sample-exposure-matched SASRec baseline under PopMatch-k5.

The N-K0 over M1 margin is small on Amazon: HR@1 `+0.0087048869`,
NDCG@5 `+0.0036435116`, and MRR `+0.0048950481`. The safe claim is therefore
directional cross-dataset replication, not a large cross-dataset specialist
advantage over the multitask model.

The N-K0 over SASRec-exp-match margin is large on Amazon under PopMatch-k5:
HR@1 `+0.2912132871`, NDCG@5 `+0.1734924534`, and MRR `+0.2274624674`.

Random-k5 should remain supplemental. On Random-k5, N-K0 and M1 are nearly tied
with N-K0 minus M1 HR@1 `+0.0011838646`, so Random-k5 is not the best primary
claim condition.

## Claim Boundaries

Allowed claims:

- Cross-dataset direction replicates on Amazon Musical Instruments under
  PopMatch-k5.
- N-K0 remains above M1 on Amazon under PopMatch-k5, but the margin is small.
- N-K0 is far above sample-exposure-matched SASRec on Amazon under PopMatch-k5.
- Random-k5 is a supplemental/easier condition, not the primary claim setting.

Disallowed or risky claims:

- Amazon multi-seed stability; only seed42 has been run.
- A large N-K0 over M1 advantage on Amazon.
- Strict compute matching; SASRec-exp-match is a sample-exposure diagnostic.
- Generalization to all Amazon categories.
