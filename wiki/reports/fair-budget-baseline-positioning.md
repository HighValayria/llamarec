---
title: "Fair-Budget Baseline Positioning"
type: report
status: current
authority: descriptive
source: agent
created: 2026-08-12
updated: 2026-08-12
last_verified: 2026-08-12
related_code:
  - src/analysis/training_budget_audit.py
  - src/analysis/sasrec_grouped_diagnostics.py
  - src/analysis/sasrec_candidate_size_robustness.py
  - src/analysis/sample_exposure_matched_diagnostic.py
  - src/baselines/sasrec.py
  - tests/test_training_budget_audit.py
  - tests/test_sample_exposure_matched_diagnostic.py
  - tests/test_analysis_outputs.py
---

# Fair-Budget Baseline Positioning

## Question

Does SASRec's optimizer-step-aligned advantage over N-K0 and M1 still support a
fair baseline conclusion after accounting for sample exposure, candidate
difficulty, target popularity, and a rough N-sample-exposure match?

## Scope

This report covers a diagnostic stage on MovieLens-1M. It uses existing LLM
adapter outputs, fixed SASRec outputs, and four focused analysis scripts:

- `src/analysis/training_budget_audit.py`
- `src/analysis/sasrec_grouped_diagnostics.py`
- `src/analysis/sasrec_candidate_size_robustness.py`
- `src/analysis/sample_exposure_matched_diagnostic.py`

It does not claim strict compute matching, exact sample-exposure matching,
multi-seed stability, or architecture-level superiority.

## Evidence

Local code and tests were validated before wiki synchronization. The focused
local suite passed 8 tests covering the budget audit, grouped/candidate-size
analysis summaries, and sample-exposure matched diagnostic.

Cloud execution supplied the formal MovieLens-1M output rows for the grouped,
candidate-size, and exposure-match summaries. All formal rows used 5675 test
examples where applicable.

## Workstream A: Training Budget Audit

The audit makes the optimizer-step comparison visibly budget-sensitive:

| model | N exposure | total exposure | optimizer steps | effective batch |
|---|---:|---:|---:|---:|
| N-K0 | 12000 | 12000 | 1500 | 8 |
| M1 | 12000 | 24000 | 3000 | 8 |
| SASRec s1500 | 767424 | 767424 | 1500 | 512 |
| SASRec s3000 | 1534656 | 1534656 | 3000 | 512 |

SASRec s1500 sees `63.952x` the N-task sample exposure of N-K0. SASRec s3000
sees `127.888x` the N-task sample exposure of N-K0. M1 has the same N-task
exposure as N-K0 but twice the total sample exposure because it alternates Y
and N tasks.

LLM wall-clock time, GPU model, trainable adapter parameter count, exact token
count, and mean or median tokenized sequence length were not recoverable from
local evidence and must not be inferred.

## Workstream B: Target-Popularity Groups

The same `k5_popmatch_seed42` test candidate file was diagnosed by
target-popularity bucket. Bucket sizes were:

| target-popularity bucket | samples |
|---|---:|
| <=10 | 26 |
| 11-50 | 199 |
| 51-200 | 854 |
| 201-500 | 1497 |
| >500 | 3099 |

HR@1 by bucket:

| model | <=10 | 11-50 | 51-200 | 201-500 | >500 |
|---|---:|---:|---:|---:|---:|
| N-K0 | 0.5000 | 0.5327 | 0.5913 | 0.5885 | 0.5153 |
| M1 | 0.4615 | 0.4422 | 0.5609 | 0.5671 | 0.4985 |
| SASRec s1500 | 0.3077 | 0.5075 | 0.6464 | 0.6560 | 0.5847 |
| SASRec s3000 | 0.2692 | 0.5729 | 0.6792 | 0.6660 | 0.5954 |

SASRec is strongly popularity-dependent in this diagnostic. Its advantage is
concentrated in middle and head buckets. The coldest bucket does not support a
claim that the observed weakness is LLM-specific: N-K0 and M1 both outperform
SASRec there, although the `<=10` bucket has only 26 samples.

## Workstream C: Candidate-Size Robustness

Candidate-size expansion remains the dominant stressor, but SASRec degrades
less than N-K0 and M1 in the tested Phase 2A candidate-size variants:

| model | k5 HR@1 | k20 HR@1 | k50 HR@1 | k5-to-k50 delta |
|---|---:|---:|---:|---:|
| N-K0 | 0.7151 | 0.4164 | 0.1995 | -0.5156 |
| M1 | 0.6932 | 0.3711 | 0.1219 | -0.5713 |
| SASRec s1500 | 0.7623 | 0.5128 | 0.3681 | -0.3942 |
| SASRec s3000 | 0.7736 | 0.5325 | 0.3894 | -0.3841 |

The SASRec-vs-N-K0 HR@1 gap grows with candidate count. For SASRec s3000 it is
`+0.0585` at k5, `+0.1161` at k20, and `+0.1900` at k50.

This supports a robustness concern for LLM next-item ranking under larger
candidate sets. It does not by itself resolve the training-budget mismatch.

## Workstream D: Rough N-Sample-Exposure Match

The target N-task exposure was N-K0's 12000 examples. Exact SASRec matching was
not feasible with batch size 512 without changing the core training
configuration, so the diagnostic used 23 SASRec optimizer steps:

| model | N-task exposure | optimizer steps | effective batch | HR@1 | NDCG@5 | MRR |
|---|---:|---:|---:|---:|---:|---:|
| N-K0 | 12000 | 1500 | 8 | 0.5466 | 0.7885 | 0.7180 |
| SASRec-exp-match | 11776 | 23 | 512 | 0.2700 | 0.6349 | 0.5157 |
| M1 supplemental | 12000 | 3000 | 8 | 0.5239 | 0.7782 | 0.7043 |

SASRec-exp-match is `-1.8667%` below the target N exposure. Under this rough
N-task sample-exposure match, SASRec does not remain stronger than N-K0. Its
gap against N-K0 is HR@1 `-0.2767`, NDCG@5 `-0.1536`, and MRR `-0.2024`.

M1 is supplemental in this table because it has 12000 N-task examples but
24000 total examples after including Y-task exposure.

## Interpretation

The earlier optimizer-step-aligned diagnostic remains valid only under its
own boundary: with the same popmatch candidate file and aligned optimizer-step
counts, SASRec s1500/s3000 is above the corresponding N-K0/M1 rows.

The fair-budget positioning stage changes the higher-level interpretation:
that advantage is sensitive to budget definition. When N-task sample exposure
is roughly matched, SASRec is below N-K0 in this single diagnostic. Therefore
the durable claim should be about sample efficiency and budget sensitivity, not
about final SASRec superiority under matched conditions.

Safe wording:

```text
SASRec is a strong specialized sequence baseline and remains above N-K0/M1
under same-candidate, optimizer-step-aligned popmatch diagnostics, but this
advantage does not survive a single rough N-sample-exposure-matched diagnostic.
```

Unsafe wording:

```text
SASRec is proven better than LLM recommendation tuning under fair matched
conditions.
```

## Open Questions

- Multi-seed stability is still unknown.
- Exact compute matching remains open because wall-clock, GPU, trainable
  parameter, and token-count evidence is incomplete.
- The coldest target-popularity bucket is too small for a strong mechanism
  claim.
- A future stage may test stronger LLM sample efficiency, popularity-balanced
  training, or a stricter compute/capacity-matched comparison.
