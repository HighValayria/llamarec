---
title: "Evaluation Layer"
type: module
status: current
authority: normative
source: mixed
created: 2026-07-30
updated: 2026-08-09
last_verified: 2026-08-09
related_code:
  - configs/experiment.yaml
  - src/eval/candidate_sets.py
  - src/eval/ranking_metrics.py
  - src/eval/binary_metrics.py
  - src/inference/base_zero_shot.py
  - src/inference/evaluate_y_adapter.py
  - src/inference/evaluate_n_adapter.py
  - src/inference/evaluate_m_adapter.py
  - src/inference/tokenization_check.py
  - src/baselines/popularity.py
  - src/analysis/grouped_error_analysis.py
  - src/analysis/baseline_result_summary.py
  - src/analysis/baseline_llm_comparison.py
  - src/analysis/candidate_set_diagnostics.py
  - src/analysis/prediction_file_audit.py
  - src/analysis/prediction_file_clean.py
  - src/analysis/phase2a_robustness_report.py
  - src/analysis/phase2c_popmatch_grouped.py
  - src/analysis/phase2c_result_summary.py
  - tests/test_candidate_sets.py
  - tests/test_ranking_metrics.py
  - tests/test_base_zero_shot_local.py
  - tests/test_n_m_adapter_evaluation.py
  - tests/test_analysis_outputs.py
  - tests/test_popularity_baseline.py
  - tests/test_baseline_result_summary.py
  - tests/test_baseline_llm_comparison.py
---

# Evaluation Layer

## Scope

The evaluation layer owns fixed N candidate-set generation, ranking metrics,
binary metrics, and offline analysis/reporting entry points. It does not train
models.

## Canonical Candidate Sets

The canonical MovieLens candidate files are:

```text
data/candidates/{dataset}/valid.jsonl
data/candidates/{dataset}/test.jsonl
```

Each candidate record includes:

- `history`
- `target`
- `candidate_movie_ids`
- `ground_truth_movie_id`
- `ground_truth_index`
- `label`
- `label_set`
- `candidate_generation`

For canonical MVP and Phase 1.5 evaluation, candidate_num is 5 and labels are
`A` through `E`.

## Phase 2A Candidate Variants

Phase 2A added explicit candidate variants without overwriting canonical files.
Named variants are written under:

```text
data/candidates/{dataset}/variants/{variant_name}/valid.jsonl
data/candidates/{dataset}/variants/{variant_name}/test.jsonl
```

Supported variant types:

- size variants, such as `k20_seed42` and `k50_seed42`;
- order-permutation variants, such as `k5_perm_seed43` and
  `k20_perm_seed43`.

Size variants use spreadsheet-style labels when the configured labels are too
short: `A`...`Z`, `AA`, `AB`, and so on. Order variants preserve the candidate
movie ID set and update `ground_truth_index`, `label`, and
`candidate_generation` provenance.

Base/Y/N/M evaluation entry points accept candidate-file overrides, so each
model comparison must use the same explicit variant files:

```text
--valid-candidates path/to/valid.jsonl
--test-candidates path/to/test.jsonl
```

Base also accepts `--output-dir` so variant outputs do not overwrite canonical
Base results.

## Phase 2C Popularity-Matched Candidates

Phase 2C added a `popularity_matched` candidate method for hard-candidate
diagnosis. It writes named variants under the same explicit variant path as
Phase 2A and does not overwrite canonical candidate files.

The generator keeps the same fixed N validation/test samples, but selects
negative candidates whose popularity is close to the target item. Generated
records preserve the standard candidate schema and include candidate-generation
metadata describing the method and popularity matching.

The validated MovieLens-1M Phase 2C variant is:

```text
k5_popmatch_seed42
```

Each validation/test split has 5675 candidate records. Candidate diagnostics
recorded mean absolute target-negative popularity gaps of `50.8842731278` on
validation and `44.0282819383` on test.

## Tokenizer Label Checks

Real-mode inference writes tokenization reports from the actual answer labels
being scored. For N and M-N candidate-label scoring, labels are read from the
candidate files, not only from `configs/experiment.yaml`.

If all labels are single-token, real inference uses next-token logits. If any
label is multi-token, scoring falls back to sequence likelihood and the report
lists those labels in `use_sequence_likelihood_for`.

For Phase 2A MovieLens-1M k50, labels `A` through `AX` were verified as
single-token for the configured Llama tokenizer.

## Metrics

Binary metrics:

```text
AUC
F1
Accuracy
```

Ranking metrics always include:

```text
HR@1
MRR
```

Ranking metrics also include top-k HR/NDCG values appropriate for the candidate
count. For the current protocol this can include:

```text
HR@5, HR@10, HR@20, HR@50
NDCG@5, NDCG@10, NDCG@20, NDCG@50
```

Ranking metrics describe the rank of the true next interaction within the
candidate set. They do not directly measure general preference ranking.

## Traditional Baselines

Traditional baselines must use the same fixed N candidate files as Base-N,
N-K0, and M-N for each evaluated condition. They must not regenerate negatives
during scoring.

`src/baselines/popularity.py` implements the current deterministic Popularity
baseline. It scores each candidate item by training-only item frequency and
writes N-compatible prediction JSONL plus split metrics.

Supported popularity sources:

- `n_train_targets`: counts targets from `next_item_train`.
- `preference_train_targets`: counts targets from `preference_train`.

The baseline entry point accepts candidate-file overrides:

```text
--valid-candidates path/to/valid.jsonl
--test-candidates path/to/test.jsonl
```

The baseline prediction files are overwritten on each run. They do not append
to existing JSONL files.

## Analysis Outputs

`src/analysis/grouped_error_analysis.py` joins predictions back to metadata and
supports dynamic ranking columns for larger candidate sets. When using it for a
candidate variant, ranking prediction paths and candidate-file overrides must
point to the same variant to avoid mixing canonical and variant evaluation
contexts.

`src/analysis/phase2a_robustness_report.py` is the preferred Phase 2A summary
entry point. It reads only explicit Phase 2A variant metric directories and
writes:

```text
phase2a_ranking_robustness_metrics.csv
phase2a_ranking_robustness_metrics.json
phase2a_ranking_robustness_comparison.csv
phase2a_ranking_robustness_report.md
```

This report avoids mixing canonical Base/Y outputs into candidate-variant
comparisons.

`src/analysis/candidate_set_diagnostics.py` summarizes candidate-set
popularity gaps for canonical or variant files.

`src/analysis/prediction_file_audit.py` audits prediction JSONL outputs for row
counts, unique candidate keys, duplicate writes, split counts, and rank
conflicts.

`src/analysis/prediction_file_clean.py` writes de-duplicated prediction copies
to a separate output directory and rejects files with conflicting duplicate
scores or ranks.

`src/analysis/phase2c_popmatch_grouped.py` reports popmatch ranking metrics by
target-popularity bucket.

`src/analysis/phase2c_result_summary.py` consolidates Phase 2C candidate
diagnostics, overall metrics, and grouped deltas into final JSON and Markdown
artifacts.

`src/analysis/baseline_result_summary.py` summarizes baseline ranking metrics
across canonical and variant candidate conditions.

`src/analysis/baseline_llm_comparison.py` combines baseline rows with Phase 2C
LLM popmatch rows and writes comparison JSON/Markdown tables.

## Current Validated State

MovieLens-1M Phase 2A generated:

- `k20_seed42`
- `k50_seed42`
- `k5_perm_seed43`
- `k20_perm_seed43`

Each validation/test split has 5675 candidate records. Phase 2A robustness
results are recorded in
[Phase 2A Ranking Robustness](../reports/phase-2a-ranking-robustness.md).

MovieLens-1M Phase 2C generated:

- `k5_popmatch_seed42`

Each validation/test split has 5675 candidate records. Phase 2C popmatch
results are recorded in
[Phase 2C Popmatch Hard-Candidate Diagnosis](../reports/phase-2c-popmatch-hard-candidate-diagnosis.md).
Under this popularity-matched candidate stress test, N-K0 remains above M1 on
next-item ranking.

MovieLens-1M Popularity baseline comparison generated canonical k5 and
`k5_popmatch_seed42` outputs for both N-train and preference-train popularity
sources. Results are recorded in
[Baseline Popularity Comparison](../reports/baseline-popularity-comparison.md).
Canonical random k5 candidates expose a popularity shortcut; popmatch k5 is the
fair comparison condition for Phase 2C LLM rows.
