---
title: "Cold/Tail Item Slice Diagnostic"
type: report
status: current
authority: descriptive
source: agent
created: 2026-08-16
updated: 2026-08-16
last_verified: 2026-08-16
related_code:
  - src/analysis/cold_tail_slice_diagnostic.py
  - src/analysis/phase2c_popmatch_grouped.py
  - src/eval/candidate_sets.py
  - src/eval/ranking_metrics.py
  - tests/test_analysis_outputs.py
  - .agent/cold_tail_item_slice_diagnostic/final/cold_tail_slice_metrics.csv
  - .agent/cold_tail_item_slice_diagnostic/final/cold_tail_slice_deltas.csv
  - .agent/cold_tail_item_slice_diagnostic/final/cold_tail_slice_diagnostic.json
  - .agent/cold_tail_item_slice_diagnostic/final/cold_tail_slice_diagnostic.md
---

# Cold/Tail Item Slice Diagnostic

## Question

Are the N-K0, M1, and SASRec differences on fixed MovieLens-1M popmatch
candidates concentrated in cold or tail target-popularity buckets?

## Scope

This report covers the MovieLens-1M `k5_popmatch_seed42` test candidate file.
It reuses existing per-record prediction files and computes ranking metrics by
target-popularity bucket. It does not train new models.

The analyzed models are:

- N-K0
- M1
- SASRec exp-match
- SASRec s47
- SASRec s1500
- SASRec s3000

This is a slice diagnostic, not a multi-seed, strict compute-matched, or
capacity-matched claim.

## Evidence

The analysis script is `src/analysis/cold_tail_slice_diagnostic.py`. The final
tracked artifact commit is `3d76f3f Record cold tail slice diagnostic`, which
stores CSV, JSON, deltas CSV, and Markdown under
`.agent/cold_tail_item_slice_diagnostic/final/`.

Cloud execution completed with 6 models, 30 metric rows, 25 delta rows, and
0 missing prediction runs.

## Bucket Sizes

| target-popularity bucket | samples |
|---|---:|
| <=10 | 26 |
| 11-50 | 199 |
| 51-200 | 854 |
| 201-500 | 1497 |
| >500 | 3099 |

The coldest bucket has only 26 samples, so its direction is useful but must not
be overstated.

## N-K0 vs M1

N-K0 exceeds M1 by HR@1 in every target-popularity bucket:

| bucket | delta HR@1 | delta NDCG@5 | delta MRR |
|---|---:|---:|---:|
| <=10 | 0.0384615385 | 0.0232857716 | 0.0307692308 |
| 11-50 | 0.0904522613 | 0.0312876421 | 0.0428810721 |
| 51-200 | 0.0304449649 | 0.0127557775 | 0.0171935988 |
| 201-500 | 0.0213760855 | 0.0111314375 | 0.0147962592 |
| >500 | 0.0167796063 | 0.0077743728 | 0.0103528019 |

This preserves the earlier interpretation that M1 is a useful multi-task
tradeoff, not a replacement for the strongest dedicated N-K0 ranking run.

## SASRec vs N-K0

SASRec exp-match and SASRec s47 are below N-K0 in every target-popularity
bucket. High-exposure SASRec rows behave differently: they remain below N-K0 in
the coldest bucket, but exceed N-K0 in middle/head buckets.

| comparison | bucket | delta HR@1 | delta NDCG@5 | delta MRR |
|---|---|---:|---:|---:|
| SASRec exp-match minus N-K0 | <=10 | -0.3846153846 | -0.2213816818 | -0.2903846154 |
| SASRec s47 minus N-K0 | <=10 | -0.3461538462 | -0.2162774345 | -0.2826923077 |
| SASRec s1500 minus N-K0 | <=10 | -0.1923076923 | -0.1155226212 | -0.1512820513 |
| SASRec s3000 minus N-K0 | <=10 | -0.2307692308 | -0.1304224023 | -0.1711538461 |
| SASRec s3000 minus N-K0 | 11-50 | 0.0402010050 | 0.0281923829 | 0.0367671692 |
| SASRec s3000 minus N-K0 | 51-200 | 0.0878220141 | 0.0457464776 | 0.0605581577 |
| SASRec s3000 minus N-K0 | 201-500 | 0.0774883100 | 0.0380088801 | 0.0505232688 |
| SASRec s3000 minus N-K0 | >500 | 0.0800258148 | 0.0413097122 | 0.0547165753 |

## Interpretation

The high-exposure SASRec advantage on popmatch candidates is not cold-tail
driven. It appears mainly in the middle and head target-popularity buckets. In
the coldest bucket, N-K0 remains above all SASRec rows, including the
high-exposure s1500 and s3000 anchors.

This strengthens the budget-sensitive story from the sample-efficiency curve:
SASRec is a strong specialized sequence baseline, especially with large sample
exposure, but the advantage does not cover the coldest target-popularity slice.

## Boundary

The `<=10` bucket has only 26 samples. Treat it as a diagnostic signal and a
motivation for larger cold-tail evaluation, not a final statistical claim.
Future work should replicate this slice with multi-seed runs, larger cold-tail
candidate construction, or stricter compute/capacity matching before using it
as a paper-level conclusion.
