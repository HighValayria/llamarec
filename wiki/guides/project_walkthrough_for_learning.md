---
title: "Project Walkthrough for Learning"
type: guide
status: current
authority: descriptive
source: user-requested
created: 2026-08-01
updated: 2026-08-16
last_verified: 2026-08-16
related_code:
  - README.md
  - task.md
  - configs/experiment.yaml
  - configs/y.yaml
  - configs/n.yaml
  - configs/m.yaml
  - src/data/preprocess.py
  - src/data/split.py
  - src/data/build_preference.py
  - src/data/build_next_item.py
  - src/data/negative_sampling.py
  - src/data/build_step2.py
  - src/eval/candidate_sets.py
  - src/eval/ranking_metrics.py
  - src/eval/binary_metrics.py
  - src/inference/base_zero_shot.py
  - src/inference/evaluate_y_adapter.py
  - src/inference/evaluate_n_adapter.py
  - src/inference/evaluate_m_adapter.py
  - src/train/train_y.py
  - src/train/train_n.py
  - src/train/train_m.py
  - src/baselines/popularity.py
  - src/baselines/bpr_mf.py
  - src/baselines/sasrec.py
  - src/analysis/sample_efficiency_curve.py
---

# Project Walkthrough for Learning

## What This Project Does

This repository builds a reproducible LLM recommendation fine-tuning MVP on
MovieLens. MovieLens-1M is the current formal result dataset. MovieLens-100K is
kept for development checks, and MovieLens-32M is deferred to later stress-test
work.

The main task families are:

- Base: no tuning; prompt the base model directly.
- Y-K0: yes/no preference tuning.
- N-K0: next-item candidate-label tuning.
- M variants: one model trained on both Y and N, evaluated through separate
  M-Y and M-N interfaces.

Traditional baselines now include Popularity, BPR-MF, and SASRec.

## The Two Axes To Keep Straight

The implementation can be understood through two axes:

```text
Workflow axis:
STEP 1 config -> STEP 2 data -> STEP 3 candidates/metrics
-> STEP 4 base inference -> STEP 5 Y training -> STEP 6 N training
-> STEP 7 M training -> STEP 8 summaries/diagnostics

Model axis:
Base / Y-K0 / N-K0 / M variants / Popularity / BPR-MF / SASRec
```

Do not start by reading every model file. First understand how raw interactions
become fixed task samples and fixed ranking candidate records.

## Core Data Semantics

The strict history rule is the central contract:

```text
history = all interactions with timestamp < target_timestamp
```

Interactions with the same timestamp do not have observable order. The code may
sort by `movie_id` for deterministic output, but that sorting is not treated as
real temporal order.

Y and N mean different things:

- Y predicts whether a target rating is positive: `rating >= 4 -> Yes`.
- N predicts the next real interaction from the full sequence, regardless of
  rating.

N negatives are candidate distractors, not explicit dislikes.

## Current Formal Result State

MovieLens-1M Base/Y/N/M is complete. Phase 1.5, Phase 2A, Phase 2B, and Phase
2C diagnostics are complete. Baseline comparisons are complete for Popularity,
BPR-MF, and SASRec. The current high-level reports are linked from
`wiki/current_state.md`.

The most recent result stage completed a sample-efficiency curve comparing
N-K0 and SASRec on fixed `k5_popmatch_seed42` candidates. At closest N-task
sample exposure points, SASRec did not exceed N-K0 by HR@1. This narrows the
interpretation: SASRec is strong under high exposure and optimizer-step-aligned
diagnostics, but its advantage does not survive sample-exposure-aligned
diagnostics.

## Recommended Reading Order

Use this order when learning the codebase:

```text
1. wiki/current_state.md
2. wiki/guides/current_data_flow.md
3. configs/experiment.yaml
4. src/data/preprocess.py
5. src/data/split.py
6. src/data/build_next_item.py
7. src/eval/candidate_sets.py
8. src/eval/ranking_metrics.py
9. src/inference/base_zero_shot.py
10. src/train/train_n.py
11. src/baselines/sasrec.py
12. src/analysis/sample_efficiency_curve.py
```

After that, read the specific report for the question you care about.

## A Small Reimplementation Path

For learning, the simplest useful replica is an ID-based next-item model:

```text
1. Read MovieLens ratings and movies.
2. Build per-user full sequences sorted by timestamp.
3. Construct legal next-item samples under the strict history rule.
4. Split each user's legal N samples into train/validation/test.
5. Map movie ids to integer item ids.
6. Pad and truncate histories.
7. Add four random negatives plus the real next item.
8. Encode history with pooling, GRU, or a small sequence encoder.
9. Score candidates by dot product.
10. Train with cross entropy over candidate positions.
11. Evaluate HR@1, HR@5, NDCG@5, and MRR.
```

This path teaches the project's main recommendation semantics without adding
LLM prompt templates, QLoRA, adapter loading, or cloud GPU complexity.
