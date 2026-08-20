# Seed42 Plan

## Status

Prepared. The formal CPU/data/candidate gate passed on the cloud run reported
by the user on 2026-08-19. GPU execution now needs explicit user approval.

## Dataset

```text
amazon-musical-instruments
```

## Fixed Candidate Files

Random-k5:

```text
data/candidates/amazon-musical-instruments/variants/random_k5_seed42/valid.jsonl
data/candidates/amazon-musical-instruments/variants/random_k5_seed42/test.jsonl
```

PopMatch-k5:

```text
data/candidates/amazon-musical-instruments/variants/popmatch_k5_seed42/valid.jsonl
data/candidates/amazon-musical-instruments/variants/popmatch_k5_seed42/test.jsonl
```

## Model Matrix

| Model | Binary | Random-k5 | PopMatch-k5 |
|---|---|---|---|
| Base | yes | yes | yes |
| Y-K0 | yes | P(Yes) ranking | P(Yes) ranking |
| N-K0 | no | candidate-label ranking | candidate-label ranking |
| M1 | M-Y | M-N | M-N |
| SASRec-exp-match | no | candidate ranking | candidate ranking |

## Candidate And Training Seeds

- random candidate seed: 42
- popmatch candidate seed: 42
- model train seed: 42

Candidate files must remain fixed across any later seed43/44 runs.
Candidate negatives are drawn from retained observed interaction items, not
from metadata-only ASINs.

## Seed42 Budget

Use the same diagnostic N-task exposure target as MovieLens-1M unless a later
paper-design decision changes the budget:

```text
N-K0 optimizer steps = 1500
N-K0 effective batch = 8
target_n_exposure = 12000
SASRec effective batch = 512
SASRec exp-match steps = round(12000 / 512) = 23
SASRec actual exposure = 11776
relative mismatch = -1.8666666667%
```

M1 remains supplemental because total Y+N exposure is not pure N supervision.

## Execution Order

1. Base inference on Y and N cohorts.
2. Y-K0 training and evaluation.
3. N-K0 training and evaluation.
4. M1 training and evaluation.
5. SASRec closest-exposure training and evaluation.
6. Generate a seed42 cross-dataset summary.

No seed43/44 runs should start until seed42 synthesis is reviewed.
