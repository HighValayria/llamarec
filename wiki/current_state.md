---
title: "Current Project State"
type: current-state
status: current
authority: descriptive
source: mixed
created: 2026-07-28
updated: 2026-08-06
last_verified: 2026-08-06
related_code:
  - task.md
  - README.md
  - configs/experiment.yaml
  - src/analysis/threshold_comparison.py
  - src/analysis/grouped_error_analysis.py
  - src/analysis/threshold_calibration.py
  - src/analysis/summarize_results.py
  - src/analysis/basic_error_analysis.py
  - tests/test_analysis_outputs.py
  - wiki/architecture/mvp_experiment_contract.md
  - wiki/modules/movielens_data_layer.md
  - wiki/modules/evaluation_layer.md
  - wiki/modules/inference_layer.md
  - wiki/modules/training_layer.md
  - wiki/reports/movielens_1m_mvp_results.md
  - wiki/reports/m_multitask_interference_diagnosis_results.md
  - wiki/reports/mvp_execution_status_and_findings.md
  - wiki/reports/phase_1_5_step_a_repository_check.md
  - wiki/reports/phase-1-5-threshold-and-grouped-diagnostics.md
---

# Current Project State

## Goal

The project builds a reliable and reproducible LLM recommendation fine-tuning
MVP on MovieLens. MovieLens-1M is the current formal result dataset.
MovieLens-100K is used for development and workflow validation. MovieLens-32M is
deferred to Phase 2 or stress-test work.

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

The current best dedicated binary model is Y-K0. The current best dedicated
ranking model is N-K0. The current best multi-task diagnostic model is M1
(`diag_m1_1m_m_200k_3000`).

## Phase 1.5 STEP B/C Status

Phase 1.5 STEP B/C is complete for the current Stage 1 scope.

STEP B created the unified binary threshold comparison entry point:

- `src/analysis/threshold_comparison.py`

It writes separate tables for:

- threshold-free AUC;
- fixed threshold `0.5`;
- validation-calibrated best-F1 threshold.

STEP C created the grouped diagnostics entry point:

- `src/analysis/grouped_error_analysis.py`

It joins predictions back to fixed Y samples, fixed N candidate records, and
full-sequence-derived user/movie statistics.

Cloud outputs:

- `/root/llamarec/outputs/calibration/movielens-1m/threshold_comparison/threshold_comparison.md`
- `/root/llamarec/outputs/error_analysis/movielens-1m/grouped/test_grouped_error_analysis.md`
- `/root/llamarec/outputs/error_analysis/movielens-1m/grouped/valid_grouped_error_analysis.md`

## Current Findings

Binary findings:

- On test, calibrated F1 is Y-K0 `0.7830635118`, M1 `0.7817788523`, M2
  `0.7734258800`, M0 `0.7687245753`, Base `0.7414450771`.
- On validation, calibrated F1 is Y-K0 `0.7857975746`, M1 `0.7816474504`, M2
  `0.7748727441`, M0 `0.7659929848`, Base `0.7422829168`.
- M1 nearly matches Y-K0 after validation threshold calibration.
- M1's fixed `0.5` threshold underestimates its binary capacity; its calibrated
  threshold is `0.3208213008`.

Ranking findings:

- On test, HR@1 is N-K0 `0.7189427313`, M1 `0.6949779736`, M0 `0.6717180617`,
  M2 `0.6548017621`, Base `0.3166519824`, Y-K0 `0.3048458150`.
- On validation, HR@1 is N-K0 `0.7215859031`, M1 `0.7064317181`, M0
  `0.6747136564`, M2 `0.6650220264`, Y-K0 `0.3171806167`, Base
  `0.3170044053`.
- M1 is the strongest multi-task ranking variant but remains below N-K0.
- Y-K0 ranking behaves like preference scoring, not next-interaction prediction.

Grouped diagnostic findings:

- Target popularity is a major ranking axis. N-K0 test HR@1 is `0.8167150694`
  for popularity `>500` but `0.1923076923` for popularity `<=10`.
- Validation confirms the same direction: N-K0 HR@1 is `0.8156407035` for
  popularity `>500` but `0.0666666667` for popularity `<=10`.
- Y-K0 ranking is rating-sensitive: validation HR@1 rises from `0.1077844311`
  for rating `1.0` to `0.4990006662` for rating `5.0`.

## Current Interpretation

M1 is the best current multi-task tradeoff. It nearly matches Y-K0 on calibrated
binary metrics and is the strongest M variant on ranking, but it does not exceed
N-K0. Therefore the current result is a useful multi-task compromise, not a claim
that M has fully surpassed the dedicated single-task models.

## Current Boundaries

Do not start M3, KAR, hard negatives, SASRec, 7B models, multi-seed experiments,
MovieLens-32M full training, candidate_num=20/50, or candidate-order robustness
inside this stage.

Future ranking robustness work should first define explicit candidate-size and
candidate-order protocols, separate output paths, and tokenizer label checks.

## Data Split Contract

The strict history rule remains:

```text
history = all interactions with timestamp < target_timestamp
```

Y and N do not require the exact same user set:

```text
Base-Y / Y-K0 / M-Y share the fixed Y validation/test set.
Base-N / N-K0 / M-N share the fixed N validation/test candidate set.
```

Y can produce multiple targets in the same timestamp bucket with the same strict
history. N only constructs strict, unambiguous next-item samples.
