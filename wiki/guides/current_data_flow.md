---
title: "Current Data Flow"
type: guide
status: current
authority: descriptive
source: user-requested
created: 2026-07-30
updated: 2026-08-16
last_verified: 2026-08-16
related_code:
  - configs/experiment.yaml
  - configs/y.yaml
  - configs/n.yaml
  - configs/m.yaml
  - src/data/build_step2.py
  - src/data/preprocess.py
  - src/data/split.py
  - src/data/build_preference.py
  - src/data/build_next_item.py
  - src/data/stats.py
  - src/eval/candidate_sets.py
  - src/eval/ranking_metrics.py
  - src/eval/binary_metrics.py
  - src/inference/base_zero_shot.py
  - src/inference/evaluate_n_adapter.py
  - src/inference/evaluate_m_adapter.py
  - src/baselines/sasrec.py
  - wiki/modules/movielens_data_layer.md
  - wiki/modules/evaluation_layer.md
---

# Current Data Flow

## One-Sentence Version

STEP 2 converts MovieLens ratings into Y and N task samples. STEP 3 converts N
validation/test samples into fixed ranking candidate records that all ranking
models reuse.

## Main Flow

```text
MovieLens raw ratings and movies
-> standardized rating rows
-> per-user full_sequence
-> timestamp-bucket split with strict history
-> Y samples and N samples
-> fixed ranking candidate records
-> Base/Y/N/M and baseline evaluation
-> analysis reports
```

The formal result dataset is MovieLens-1M. MovieLens-100K remains useful for
development checks. MovieLens-32M is not the active formal result dataset.

## Task Files

Y files:

```text
data/processed/{dataset}/preference_train.jsonl
data/processed/{dataset}/preference_valid.jsonl
data/processed/{dataset}/preference_test.jsonl
```

N files:

```text
data/processed/{dataset}/next_item_train.jsonl
data/processed/{dataset}/next_item_valid.jsonl
data/processed/{dataset}/next_item_test.jsonl
```

Fixed candidate files:

```text
data/candidates/{dataset}/valid.jsonl
data/candidates/{dataset}/test.jsonl
data/candidates/{dataset}/variants/*/valid.jsonl
data/candidates/{dataset}/variants/*/test.jsonl
```

The important current variant is
`data/candidates/movielens-1m/variants/k5_popmatch_seed42/test.jsonl`, which
contains 5675 test records.

## What Uses Each File

| file family | producer | consumers | purpose |
|---|---|---|---|
| `full_sequences.jsonl` | STEP 2 | data construction and checks | complete per-user interaction sequence |
| `preference_train.jsonl` | STEP 2 | Y-K0, M variants | yes/no preference training |
| `preference_valid/test.jsonl` | STEP 2 | Base-Y, Y-K0, M-Y | binary evaluation |
| `next_item_train.jsonl` | STEP 2 | N-K0, M variants, SASRec | next-item training |
| `next_item_valid/test.jsonl` | STEP 2 | STEP 3 | source records for ranking candidates |
| `data/candidates/{dataset}/valid/test.jsonl` | STEP 3 | Base/Y/N/M ranking eval | fixed ranking evaluation records |
| `variants/k5_popmatch_seed42/*` | Phase 2C candidate generation | LLM and baseline popmatch eval | popularity-matched hard candidates |

## Candidate Protocols

Canonical k5 candidates contain one ground-truth next item and four random
negative candidates. The project also has explicit candidate variants for
ranking robustness:

- `k20_seed42`
- `k50_seed42`
- `k5_perm_seed43`
- `k20_perm_seed43`
- `k5_popmatch_seed42`

Evaluation reports must identify which candidate file they used. Old metrics
must not be reused as popmatch evidence unless the prediction records match the
popmatch candidate file by content.

## Model-Specific Consumption

Base-N, N-K0, M-N, SASRec, Popularity, and BPR-MF all score fixed candidate
records. N-K0 and M-N output candidate-label probabilities `P(A)` through
`P(E)`. SASRec scores candidates by sequence/candidate dot product.

Y-K0 and M-Y can also be evaluated in ranking mode, but they score each
candidate independently through the yes/no interface and rank by `P(Yes)`.

## Current Result Tail

The current formal result path is MovieLens-1M with fixed candidate protocols.
The latest sample-efficiency result uses the popmatch candidate file and records
that SASRec does not exceed N-K0 at closest N-task sample-exposure points by
HR@1, NDCG@5, or MRR. The high-exposure SASRec anchors remain above N-K0, so
the correct interpretation is budget-sensitive rather than architecture-final.
