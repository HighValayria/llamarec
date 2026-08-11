---
title: "Evaluation Layer"
type: module
status: current
authority: normative
source: mixed
created: 2026-07-30
updated: 2026-08-11
last_verified: 2026-08-11
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
  - src/baselines/bpr_mf.py
  - src/baselines/sasrec.py
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
  - tests/test_bpr_mf_baseline.py
  - tests/test_sasrec_baseline.py
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

`src/baselines/bpr_mf.py` implements the current trainable matrix-factorization
baseline. It trains from `next_item_train` targets with BPR loss, scores only
the fixed candidate items supplied by the N candidate files, and writes
N-compatible prediction JSONL plus split metrics. Its outputs include model and
mapping artifacts in addition to metrics and prediction files.

The BPR-MF entry point accepts the same candidate-file overrides:

```text
--valid-candidates path/to/valid.jsonl
--test-candidates path/to/test.jsonl
```

BPR-MF prediction files are overwritten on each run. They do not append to
existing JSONL files.

`src/baselines/sasrec.py` implements the current trainable sequence baseline.
It trains from strict N train histories and targets, scores only fixed candidate
items supplied by N candidate files, and writes N-compatible prediction JSONL
plus split metrics. It supports:

```text
--valid-candidates path/to/valid.jsonl
--test-candidates path/to/test.jsonl
--device auto|cpu|cuda
--model-dir outputs/baselines/{dataset}/sasrec_fixed_canonical_k5_e10
```

The `--model-dir` mode evaluates an existing trained SASRec model against a
new fixed candidate condition without retraining. This is the preferred way to
compare canonical and popmatch candidates for the same SASRec model. The
implementation uses right padding with a causal Transformer encoder and raises
an error on non-finite training logits, losses, or candidate scores. Earlier
pre-fix SASRec outputs with NaN epoch losses are invalid and must not be used.

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

MovieLens-1M baseline comparison generated canonical k5 and
`k5_popmatch_seed42` outputs for Popularity, BPR-MF, and fixed SASRec
baselines. Popularity results are recorded in
[Baseline Popularity Comparison](../reports/baseline-popularity-comparison.md),
BPR-MF results are recorded in
[Baseline BPR-MF Comparison](../reports/baseline-bpr-mf-comparison.md), and
SASRec results are recorded in
[Baseline SASRec Comparison](../reports/baseline-sasrec-comparison.md).
Canonical random k5 candidates expose a popularity shortcut; popmatch k5 is the
fair comparison condition for Phase 2C LLM rows. Under popmatch k5, fixed
SASRec e10 is above N-K0 and M1, while capped 200k SASRec e1 is below them and
capped 200k SASRec e3 is above them. These SASRec comparisons are not strict
compute- or capacity-matched claims against LLM adapters.
