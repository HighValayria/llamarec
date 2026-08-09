---
title: "Current Project State"
type: current-state
status: current
authority: descriptive
source: mixed
created: 2026-07-28
updated: 2026-08-09
last_verified: 2026-08-09
related_code:
  - task.md
  - README.md
  - configs/experiment.yaml
  - src/eval/candidate_sets.py
  - src/eval/ranking_metrics.py
  - src/inference/base_zero_shot.py
  - src/inference/evaluate_y_adapter.py
  - src/inference/evaluate_n_adapter.py
  - src/inference/evaluate_m_adapter.py
  - src/inference/tokenization_check.py
  - src/analysis/grouped_error_analysis.py
  - src/analysis/phase2a_robustness_report.py
  - tests/test_candidate_sets.py
  - tests/test_ranking_metrics.py
  - tests/test_base_zero_shot_local.py
  - tests/test_n_m_adapter_evaluation.py
  - tests/test_analysis_outputs.py
  - wiki/modules/evaluation_layer.md
  - wiki/reports/phase-1-5-threshold-and-grouped-diagnostics.md
  - wiki/reports/phase-2a-ranking-robustness.md
---

# Current Project State

## Goal

The project builds a reliable and reproducible LLM recommendation fine-tuning
MVP on MovieLens. MovieLens-1M is the current formal result dataset.
MovieLens-100K is used for development and workflow validation. MovieLens-32M is
deferred to later stress-test work.

The active task definitions are:

- Base: no tuning.
- Y-K0: Yes/No preference tuning, `P(Like | History, Item)`.
- N-K0: full-sequence next-item tuning, `P(Next Item | History, Candidate Set)`.
- M-K0 / M variants: one model jointly trained on Y and N, evaluated through
  separate M-Y and M-N interfaces.

N ground truth is the next real interaction in the full sequence. It is not the
next liked item and is not filtered by rating.

## Current Result State

The MovieLens-1M MVP chain has completed for Base, Y-K0, N-K0, and M variants.
Core reports are:

- [MovieLens-1M MVP Results](reports/movielens_1m_mvp_results.md)
- [M Multi-task Interference Diagnosis Results](reports/m_multitask_interference_diagnosis_results.md)
- [MVP Execution Status and Findings](reports/mvp_execution_status_and_findings.md)
- [Phase 1.5 STEP A Repository Check](reports/phase_1_5_step_a_repository_check.md)
- [Phase 1.5 Threshold and Grouped Diagnostics](reports/phase-1-5-threshold-and-grouped-diagnostics.md)
- [Phase 2A Ranking Robustness](reports/phase-2a-ranking-robustness.md)

The current best dedicated binary model is Y-K0. The current best dedicated
ranking model is N-K0. The current best multi-task diagnostic model is M1
(`diag_m1_1m_m_200k_3000`).

## Phase 2A Status

Phase 2A ranking robustness is complete for Base, N-K0, and M1 on MovieLens-1M.
The implemented protocol covers:

- candidate-size variants `k20_seed42` and `k50_seed42`;
- order-permutation variants `k5_perm_seed43` and `k20_perm_seed43`;
- explicit candidate-file overrides for Base/Y/N/M evaluation;
- dynamic ranking metrics for larger candidate sets;
- tokenizer label checks from actual candidate files;
- explicit-variant CSV/JSON/Markdown reporting through
  `src/analysis/phase2a_robustness_report.py`.

Cloud output:

- `/root/llamarec/outputs/phase2a/ranking_robustness/phase2a_ranking_robustness_report.md`

Main Phase 2A findings:

- Order sensitivity is small. At k20, HR@1 changes are Base `-0.0010572687`,
  N-K0 `+0.0065198238`, and M1 `+0.0047577093`.
- Candidate-size expansion is the dominant stressor. HR@1 drops sharply from
  k5 permutation to k20 and again from k20 to k50.
- N-K0 remains above M1 for every tested robustness variant. The N-K0 minus M1
  HR@1 gap grows from `+0.0218502203` on k5 permutation to `+0.0775330396` on
  k50.
- k50 labels `A` through `AX` are single-token for the configured Llama
  tokenizer, so k50 can use the same single-token candidate-label logits path as
  k5/k20.
- Popularity remains a major robustness axis. On k20 test, N-K0 HR@1 is
  `0.0769230769` for popularity `<=10` and `0.5327525008` for popularity
  `>500`; M1 has the same cold-item weakness and lower popular-item HR@1.

## Prior Findings

Phase 1.5 showed:

- On binary calibrated F1, Y-K0 is best and M1 nearly matches it.
- On canonical 5-candidate ranking, N-K0 is best and M1 is the strongest M
  variant but remains below N-K0.
- Y-K0 ranking behaves like preference scoring, not next-interaction prediction.
- Target popularity is a major ranking diagnostic axis.

## Current Interpretation

M1 is the best current multi-task tradeoff. It nearly matches Y-K0 on calibrated
binary metrics and is the strongest M variant on ranking, but it does not exceed
N-K0. Phase 2A strengthens this interpretation: as candidate sets become larger,
the dedicated next-item model N-K0 is more robust than M1.

## Current Boundaries

Do not start M3, KAR, hard negatives, SASRec, 7B models, multi-seed experiments,
or MovieLens-32M full training without a new scoped stage.

Reasonable next work:

- write the paper/report interpretation around M1 as a tradeoff rather than a
  replacement for N-K0;
- optionally run Y-K0 explicit-variant robustness as a preference-ranking
  control;
- design a later phase focused on cold-item robustness or stronger next-item
  supervision.

## Data Split Contract

The strict history rule remains:

```text
history = all interactions with timestamp < target_timestamp
```

Y and N do not require the exact same user set:

```text
Base-Y / Y-K0 / M-Y share the fixed Y validation/test set.
Base-N / N-K0 / M-N share the fixed N validation/test candidate set for each
evaluated candidate variant.
```

Y can produce multiple targets in the same timestamp bucket with the same strict
history. N only constructs strict, unambiguous next-item samples.
