---
title: "Current Project State"
type: current-state
status: current
authority: descriptive
source: mixed
created: 2026-07-28
updated: 2026-08-17
last_verified: 2026-08-17
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
  - src/baselines/popularity.py
  - src/baselines/bpr_mf.py
  - src/baselines/sasrec.py
  - src/analysis/grouped_error_analysis.py
  - src/analysis/baseline_result_summary.py
  - src/analysis/baseline_llm_comparison.py
  - src/analysis/candidate_set_diagnostics.py
  - src/analysis/prediction_file_audit.py
  - src/analysis/prediction_file_clean.py
  - src/analysis/phase2a_robustness_report.py
  - src/analysis/phase2b_result_synthesis.py
  - src/analysis/phase2c_popmatch_grouped.py
  - src/analysis/phase2c_result_summary.py
  - src/analysis/training_budget_audit.py
  - src/analysis/sasrec_grouped_diagnostics.py
  - src/analysis/sasrec_candidate_size_robustness.py
  - src/analysis/sample_exposure_matched_diagnostic.py
  - src/analysis/sample_efficiency_curve.py
  - src/analysis/cold_tail_slice_diagnostic.py
  - src/analysis/multiseed_stability_summary.py
  - tests/test_candidate_sets.py
  - tests/test_ranking_metrics.py
  - tests/test_base_zero_shot_local.py
  - tests/test_n_m_adapter_evaluation.py
  - tests/test_analysis_outputs.py
  - tests/test_popularity_baseline.py
  - tests/test_bpr_mf_baseline.py
  - tests/test_sasrec_baseline.py
  - tests/test_training_budget_audit.py
  - tests/test_sample_exposure_matched_diagnostic.py
  - tests/test_baseline_result_summary.py
  - tests/test_baseline_llm_comparison.py
  - wiki/modules/evaluation_layer.md
  - wiki/reports/phase-1-5-threshold-and-grouped-diagnostics.md
  - wiki/reports/phase-2a-ranking-robustness.md
  - wiki/reports/phase-2b-result-synthesis.md
  - wiki/reports/phase-2c-popmatch-hard-candidate-diagnosis.md
  - wiki/reports/baseline-popularity-comparison.md
  - wiki/reports/baseline-bpr-mf-comparison.md
  - wiki/reports/baseline-sasrec-comparison.md
  - wiki/reports/fair-budget-baseline-positioning.md
  - wiki/reports/sample-efficiency-training-efficiency.md
  - wiki/reports/cold-tail-item-slice-diagnostic.md
  - wiki/reports/multiseed-stability.md
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
- [Phase 2B Result Synthesis](reports/phase-2b-result-synthesis.md)
- [Phase 2C Popmatch Hard-Candidate Diagnosis](reports/phase-2c-popmatch-hard-candidate-diagnosis.md)
- [Baseline Popularity Comparison](reports/baseline-popularity-comparison.md)
- [Baseline BPR-MF Comparison](reports/baseline-bpr-mf-comparison.md)
- [Baseline SASRec Comparison](reports/baseline-sasrec-comparison.md)
- [Fair-Budget Baseline Positioning](reports/fair-budget-baseline-positioning.md)
- [Sample-Efficiency Training-Efficiency Curve](reports/sample-efficiency-training-efficiency.md)
- [Cold/Tail Item Slice Diagnostic](reports/cold-tail-item-slice-diagnostic.md)
- [Multi-seed Stability](reports/multiseed-stability.md)

The current best dedicated binary model is Y-K0. Among LLM runs, the current
best dedicated ranking model is N-K0 and the current best multi-task diagnostic
model is M1 (`diag_m1_1m_m_200k_3000`). SASRec is now the strongest specialized
non-LLM sequence baseline under the fixed popmatch comparison. A follow-up
diagnostic re-evaluated N-K0 and M1 adapters on the same popmatch test
candidate file and added SASRec 1500/3000 optimizer-step rows. SASRec remains
above N-K0/M1 in that optimizer-step-aligned diagnostic, but this is not a
strict compute-, sample-exposure-, or capacity-matched comparison against LLM
adapters.

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

## Phase 2B Status

Phase 2B result synthesis is complete. The stage added
`src/analysis/phase2b_result_synthesis.py`, which reads existing Phase 1.5 and
Phase 2A artifacts and writes paper-ready CSV/JSON/Markdown tables without
training models or recomputing inference.

Cloud output:

- `/root/llamarec/outputs/phase2b/result_synthesis/phase2b_result_synthesis.md`

The generated synthesis provides:

- validation-calibrated binary test metrics;
- canonical 5-candidate ranking test metrics;
- Phase 2A robustness test metrics;
- key robustness deltas;
- paper-ready claims and explicit claim boundaries.

Main Phase 2B claims:

- Y-K0 gives the strongest validation-calibrated binary F1 on the test split.
- M1 nearly matches Y-K0 on calibrated binary F1.
- N-K0 is the strongest canonical next-item ranking model.
- M1 is the strongest multi-task ranking variant but remains below N-K0.
- The N-K0 advantage over M1 grows under k50 candidate-size stress.
- Candidate order perturbation has small effects relative to candidate-size
  expansion.

## Phase 2C Status

Phase 2C popmatch hard-candidate diagnosis is complete. The stage added
popularity-matched candidate generation and reusable audit, cleaning, grouped
diagnostic, and result-summary scripts. It did not train new models.

Cloud output:

- `/root/llamarec/outputs/phase2c/movielens-1m/result_summary/phase2c_popmatch_result_summary.md`

The `k5_popmatch_seed42` variant contains 5675 validation and 5675 test
candidate records. Mean absolute target-negative popularity gap is
`50.8842731278` on validation and `44.0282819383` on test, compared with about
`690.6044` and `663.5850` for the canonical random validation/test candidate
sets during diagnosis.

Main Phase 2C findings:

- N-K0 remains the strongest next-item ranking model under popularity-matched
  hard candidates.
- M1 remains close to N-K0 but does not surpass it on ranking. On test, N-K0
  exceeds M1 by HR@1 `+0.0202643172`, NDCG@5 `+0.0092964437`, and MRR
  `+0.0124199706`.
- Y-K0 remains binary-strong but weak as next-item ranking, preserving the Y/N
  semantic boundary.
- N-K0's ranking advantage over M1 appears across target-popularity buckets;
  the coldest `<=10` bucket favors N-K0 but has only 26 samples.

## Baseline Comparison Status

The traditional baseline work now includes deterministic Popularity baselines,
an in-repository PyTorch BPR-MF baseline, and an in-repository PyTorch SASRec
sequence baseline on MovieLens-1M. The baseline analysis path uses
`src/analysis/baseline_result_summary.py` and
`src/analysis/baseline_llm_comparison.py` to compare canonical and popmatch
candidate conditions.

Cloud output:

- `/root/llamarec/outputs/baselines/movielens-1m/llm_comparison/baseline_llm_comparison.md`

Two training-only popularity definitions were evaluated: `n_train_targets` and
`preference_train_targets`. On canonical random k5 candidates, Popularity is
strong: N-train Popularity test HR@1 is `0.5663436123`, and preference-train
Popularity test HR@1 is `0.5295154185`. Under popmatch k5, the same baselines
drop to HR@1 `0.3226431718` and `0.0918061674`.

BPR-MF was trained from `next_item_train` targets with embedding dimension 64,
10 epochs, batch size 4096, learning rate 0.01, and seed 42. It reaches test
HR@1 `0.5610572687`, NDCG@5 `0.8066675971`, and MRR `0.7411424376` on
canonical random k5 candidates. Under `k5_popmatch_seed42`, BPR-MF drops to
HR@1 `0.3351541850`, NDCG@5 `0.6757962567`, and MRR `0.5690719530`.

SASRec was implemented after BPR-MF. Pre-fix SASRec outputs were invalidated
because a left-padding plus causal-mask interaction produced NaN losses and
degenerate fixed-label predictions. The fixed implementation uses right padding,
non-finite guards, and eval-only `--model-dir` scoring so the same trained
canonical model can be evaluated against popmatch candidates. Fixed SASRec e10
reaches test HR@1 `0.7793832599`, NDCG@5 `0.9044029047`, and MRR
`0.8718942731` on canonical random k5 candidates. The same fixed e10 model
evaluated on `k5_popmatch_seed42` reaches HR@1 `0.6394713656`, NDCG@5
`0.8345499558`, and MRR `0.7791659325`.

The capped 200k SASRec check reduces, but does not eliminate, the training
budget mismatch with N-K0. With `max_train_samples=200000`, SASRec e1 remains
below N-K0/M1 on popmatch HR@1 (`0.4623788546`), while SASRec e3 exceeds them
on popmatch HR@1 (`0.5991189427`). These rows show that a specialized sequence
recommender is a strong control; they do not prove an architecture-level result
against LLM recommendation tuning under matched compute and capacity.

The stricter follow-up found that the old N-K0 prediction candidates did not
match `k5_popmatch_seed42/test.jsonl` by content, so old canonical
`test_metrics.json` rows must not be reused as popmatch evidence. N-K0 and M1
were re-evaluated in adapter eval-only mode on the actual popmatch test
candidate file. SASRec was evaluated from the same 200k N train pool at 1500
and 3000 optimizer steps:

| model | alignment | popmatch HR@1 | popmatch NDCG@5 | popmatch MRR |
|---|---|---:|---:|---:|
| N-K0 popmatch eval | 200k N loaded, 1500 LLM optimizer steps | 0.5466079295 | 0.7884963692 | 0.7180411160 |
| M1 popmatch eval | 200k Y + 200k N loaded, 3000 LLM optimizer steps | 0.5238766520 | 0.7781912330 | 0.7042525698 |
| SASRec s1500 popmatch | 200k N pool, 1500 optimizer steps, batch 512 | 0.6088105727 | 0.8198039644 | 0.7595506608 |
| SASRec s3000 popmatch | 200k N pool, 3000 optimizer steps, batch 512 | 0.6243171806 | 0.8283562609 | 0.7708663730 |

This supports the narrow claim that SASRec is stronger under the same-candidate
popmatch, optimizer-step-aligned diagnostic. It still does not match sample
exposure or compute: SASRec uses batch size 512, LLM trainer states record
`train_batch_size=1`, and M1's 3000 steps are split across Y and N tasks.

Main baseline interpretation:

- canonical random k5 candidates expose a popularity shortcut;
- popmatch k5 is the fair comparison point for Phase 2C LLM ranking results;
- popularity and BPR-MF alone do not explain N-K0/M1 popmatch ranking
  performance;
- fixed SASRec is a stronger specialized non-LLM sequence baseline than
  Popularity or BPR-MF;
- SASRec comparisons must carry non-budget/capacity-matched claim boundaries.

## Fair-Budget Baseline Positioning Status

The fair-budget baseline positioning stage audited whether the
optimizer-step-aligned SASRec advantage remains stable under fairer budget and
difficulty diagnostics. The durable report is
[Fair-Budget Baseline Positioning](reports/fair-budget-baseline-positioning.md).

Main findings:

- Optimizer-step alignment hides a large sample-exposure mismatch. N-K0 used
  12000 N-task processed examples at 1500 optimizer steps with effective batch
  8. SASRec s1500 used 767424 N-task exposures at the same optimizer-step count
  with batch size 512, or `63.952x` N-K0's N-task exposure.
- M1 should be described separately from N-only rows: it used 12000 N-task
  examples but 24000 total examples after including Y-task exposure.
- In target-popularity groups on `k5_popmatch_seed42`, SASRec's advantage is
  concentrated in middle/head buckets. In the coldest `<=10` bucket, N-K0
  HR@1 is `0.5000`, M1 is `0.4615`, SASRec s1500 is `0.3077`, and SASRec
  s3000 is `0.2692`, with only 26 samples.
- Under Phase 2A candidate-size variants, SASRec degrades less than N-K0/M1 as
  candidate count grows. The SASRec s3000 minus N-K0 HR@1 gap grows from
  `+0.0585` at k5 to `+0.1900` at k50.
- Under a rough N-task sample-exposure match, SASRec used 23 optimizer steps
  and 11776 N exposures, `-1.8667%` from the 12000 target. It scored HR@1
  `0.2700`, NDCG@5 `0.6349`, and MRR `0.5157`, below N-K0's HR@1 `0.5466`,
  NDCG@5 `0.7885`, and MRR `0.7180`.

The safe interpretation is now budget-sensitive: SASRec remains a strong
specialized sequence baseline under same-candidate, optimizer-step-aligned
diagnostics, but that advantage does not survive the single rough
N-sample-exposure-matched diagnostic. This motivates further sample-efficiency
and matched-compute analysis rather than a final architecture-level claim.

## Sample-Efficiency Training-Efficiency Status

The sample-efficiency stage completed a 10-row N-task exposure curve on
MovieLens-1M fixed `k5_popmatch_seed42` candidates. The durable report is
[Sample-Efficiency Training-Efficiency Curve](reports/sample-efficiency-training-efficiency.md),
and the tracked artifact commit is `6b29fcd Record sample efficiency final
curve`.

At closest N-task exposure points, SASRec does not exceed N-K0 by HR@1:

| comparison | N-K0 exposure | SASRec exposure | mismatch % | delta HR@1 |
|---|---:|---:|---:|---:|
| sasrec_s6_minus_n_s375 | 3000 | 3072 | 2.4 | -0.2200881058 |
| sasrec_s12_minus_n_s750 | 6000 | 6144 | 2.4 | -0.2801762115 |
| sasrec_s23_minus_n_s1500 | 12000 | 11776 | -1.8666666667 | -0.2766519824 |
| sasrec_s47_minus_n_s3000 | 24000 | 24064 | 0.2666666667 | -0.2771806168 |

The high-exposure SASRec anchors remain above N-K0, but they use much larger
N-task exposure. The safe interpretation is therefore that SASRec is a strong
specialized sequence baseline whose apparent advantage is highly sensitive to
the budget axis. The current sample-exposure curve supports further cold-item,
tail-item, multi-seed, and stricter compute/capacity diagnostics rather than a
final architecture-level claim.

## Cold/Tail Item Slice Diagnostic Status

The cold/tail slice stage completed a target-popularity bucket diagnostic on
MovieLens-1M fixed `k5_popmatch_seed42` test candidates. The durable report is
[Cold/Tail Item Slice Diagnostic](reports/cold-tail-item-slice-diagnostic.md),
and the tracked artifact commit is `3d76f3f Record cold tail slice diagnostic`.

The bucket sizes were 26 samples for `<=10`, 199 for `11-50`, 854 for
`51-200`, 1497 for `201-500`, and 3099 for `>500`.

Main findings:

- N-K0 exceeds M1 by HR@1 in every target-popularity bucket.
- SASRec exp-match and SASRec s47 are below N-K0 in every bucket.
- High-exposure SASRec s1500 and s3000 remain below N-K0 in the coldest
  `<=10` bucket, with HR@1 deltas `-0.1923` and `-0.2308`.
- High-exposure SASRec exceeds N-K0 in middle/head buckets. SASRec s3000 minus
  N-K0 HR@1 is `+0.0402` in `11-50`, `+0.0878` in `51-200`, `+0.0775` in
  `201-500`, and `+0.0800` in `>500`.

The safe interpretation is that SASRec's high-exposure popmatch advantage is
not cold-tail driven; it appears mainly in middle/head target-popularity
buckets. The coldest bucket has only 26 samples and should be treated as a
diagnostic signal, not a final statistical claim.

## Multi-seed Stability Status

The multi-seed stability stage completed seed42/43/44 checks for Y-K0, N-K0,
M1, SASRec exp-match, and SASRec high s3000 on MovieLens-1M fixed
`k5_popmatch_seed42` candidates. The durable report is
[Multi-seed Stability](reports/multiseed-stability.md), and the tracked
artifact commit is `22b9089 Record multiseed stability results`.

The stage also added explicit training seed support for Y/N/M adapter training:
`src/train/train_y.py`, `src/train/train_n.py`, and `src/train/train_m.py` now
accept `--seed`, seed Python/NumPy/torch/CUDA/transformers before model
initialization, pass `seed` and `data_seed` to `TrainingArguments` where
supported, and record the resolved seed in metrics and `run_summary.json`.

Main findings:

- Y-K0 binary F1 is available across three seeds, with range `0.0097766064`.
- N-K0 remains above M1 by HR@1 across all three seeds. The minimum HR@1 margin
  is `0.0103964758`.
- N-K0 remains above roughly exposure-matched SASRec s23 by HR@1 across all
  three seeds. The minimum HR@1 margin is `0.2766519824`.
- SASRec high s3000 remains above N-K0 by HR@1 across all three seeds. The
  minimum HR@1 margin is `0.0777092511`, but this remains a separate
  high-exposure budget regime.
- All multi-seed rows use the fixed `k5_popmatch_seed42` candidate protocol.

The safe interpretation is that the main ranking and sample-efficiency
directions are stable across seeds 42/43/44. The result does not convert the
high-exposure SASRec advantage into a matched-budget claim.

## Current Interpretation

M1 is the best current multi-task tradeoff. It nearly matches Y-K0 on calibrated
binary metrics and is the strongest M variant on ranking, but it does not exceed
N-K0 among LLM ranking runs. Phase 2A strengthens this interpretation: as
candidate sets become larger, the dedicated next-item LLM model N-K0 is more
robust than M1. Phase 2B packages this into the LLM-centered paper-ready result
interpretation. Phase 2C further preserves the same boundary under
popularity-matched hard candidates: M1 is a useful compromise, not a
single-task replacement. Traditional baselines now add two controls: canonical
random candidate results are heavily affected by popularity, and a specialized
sequence model can outperform the LLM next-item rows under the current
same-candidate popmatch, optimizer-step-aligned diagnostic. The fair-budget
baseline positioning stage narrows that interpretation: the SASRec advantage
is sensitive to budget definition and does not hold in the single rough
N-sample-exposure-matched diagnostic or in the completed closest-exposure
sample-efficiency curve. The cold/tail diagnostic further shows that
high-exposure SASRec's popmatch advantage is concentrated outside the coldest
target-popularity bucket. The multi-seed stability stage confirms that these
main directions are stable across seeds 42/43/44 under the fixed popmatch
candidate protocol.

## Current Boundaries

Do not start M3, KAR, hard negatives, 7B models, MovieLens-32M full training,
or a strict compute/capacity-matched LLM-vs-SASRec study without a new scoped
stage.

Reasonable next work:

- plan stricter compute/capacity-matched comparisons between LLM adapters and
  specialized sequence recommenders;
- design a later phase focused on cold-item robustness, stronger next-item
  supervision, or hard-negative training.

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
