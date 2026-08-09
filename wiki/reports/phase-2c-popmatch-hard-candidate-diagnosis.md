---
title: "Phase 2C Popmatch Hard-Candidate Diagnosis"
type: report
status: current
authority: descriptive
source: mixed
created: 2026-08-09
updated: 2026-08-09
last_verified: 2026-08-09
related_code:
  - src/eval/candidate_sets.py
  - src/analysis/candidate_set_diagnostics.py
  - src/analysis/prediction_file_audit.py
  - src/analysis/prediction_file_clean.py
  - src/analysis/phase2c_popmatch_grouped.py
  - src/analysis/phase2c_result_summary.py
  - tests/test_candidate_sets.py
  - tests/test_analysis_outputs.py
---

# Phase 2C Popmatch Hard-Candidate Diagnosis

## Scope

Phase 2C is a diagnosis and consolidation stage. It evaluates existing Base,
Y-K0, N-K0, and M1 models under popularity-matched hard candidates before
approving any new training or Phase 3 method changes.

This stage does not train new models. It reuses the MovieLens-1M split,
candidate-file override contract, and existing cloud adapters.

## Generated Artifacts

Candidate variant:

```text
data/candidates/movielens-1m/variants/k5_popmatch_seed42/valid.jsonl
data/candidates/movielens-1m/variants/k5_popmatch_seed42/test.jsonl
```

Cloud summary output:

```text
/root/llamarec/outputs/phase2c/movielens-1m/result_summary/phase2c_popmatch_result_summary.md
```

Supporting outputs:

```text
/root/llamarec/outputs/phase2c/movielens-1m/candidate_set_diagnostics/k5_popmatch_seed42/
/root/llamarec/outputs/phase2c/movielens-1m/popmatch_eval/
/root/llamarec/outputs/phase2c/movielens-1m/popmatch_eval_clean/
/root/llamarec/outputs/phase2c/movielens-1m/popmatch_grouped/
```

## Candidate Diagnostics

The popularity-matched candidate generator keeps the same fixed N validation
and test samples but chooses negatives with popularity close to the target item.

| split | method | samples | mean_abs_popularity_gap |
|---|---|---:|---:|
| validation | popularity_matched | 5675 | 50.8842731278 |
| test | popularity_matched | 5675 | 44.0282819383 |

For comparison during local/cloud diagnosis, the canonical random candidate
mean absolute popularity gap was about `690.6044` on validation and `663.5850`
on test. The popmatch candidate set is therefore a real popularity-controlled
stress test, not another random candidate draw.

## Overall Test Metrics

| model | HR@1 | NDCG@5 | MRR | AUC | F1 |
|---|---:|---:|---:|---:|---:|
| Base | 0.3148898678 | 0.6636020792 | 0.5531365639 | 0.6217848091 | 0.6978069304 |
| N-K0 | 0.5446696035 | 0.7877973813 | 0.7170837004 |  |  |
| M1 | 0.5244052863 | 0.7785009376 | 0.7046637298 | 0.7664120559 | 0.7275700935 |
| Y-K0 | 0.1853744493 | 0.5801737577 | 0.4442819383 | 0.7690355691 | 0.7799656403 |

N-K0 remains above M1 under popularity-matched hard candidates:

| metric | N-K0 minus M1 |
|---|---:|
| HR@1 | 0.0202643172 |
| NDCG@5 | 0.0092964437 |
| MRR | 0.0124199706 |

## Target Popularity Groups

N-K0 remains above M1 in every target-popularity bucket on HR@1.

| bucket | samples | N-K0 minus M1 HR@1 | N-K0 minus M1 NDCG@5 | N-K0 minus M1 MRR |
|---|---:|---:|---:|---:|
| <=10 | 26 | 0.0384615385 | 0.0132142521 | 0.0179487179 |
| 11-50 | 199 | 0.0904522613 | 0.0325529390 | 0.0443886097 |
| 51-200 | 854 | 0.0304449649 | 0.0130928978 | 0.0176034349 |
| 201-500 | 1497 | 0.0133600534 | 0.0076992916 | 0.0101870407 |
| >500 | 3099 | 0.0161342369 | 0.0074954948 | 0.0099709584 |

The largest observed HR@1 gap is in the `11-50` bucket. The coldest `<=10`
bucket also favors N-K0, but it has only 26 samples and should be interpreted
cautiously.

## Interpretation

Phase 2C does not overturn the Phase 2B result boundary. N-K0 remains the
strongest next-item ranking model under popularity-matched hard candidates.
M1 remains close to N-K0 and preserves useful binary behavior, but it does not
surpass N-K0 on ranking.

Y-K0 remains strong for binary preference prediction but weak as next-item
ranking. This further supports the semantic boundary between Y
(`P(Like | History, Item)`) and N (`P(Next Item | History, Candidate Set)`).

The N-K0 versus M1 ranking gap is broadly distributed across target popularity
buckets rather than being confined to the coldest items.

## Implementation Notes

Phase 2C added reusable analysis tooling:

- `src/eval/candidate_sets.py`: `popularity_matched` candidate generation.
- `src/analysis/candidate_set_diagnostics.py`: candidate-set popularity-gap
  diagnostics.
- `src/analysis/prediction_file_audit.py`: duplicate prediction output audit.
- `src/analysis/prediction_file_clean.py`: safe non-destructive duplicate
  cleaning into a separate output directory.
- `src/analysis/phase2c_popmatch_grouped.py`: target-popularity grouped ranking
  diagnostics.
- `src/analysis/phase2c_result_summary.py`: final Phase 2C Markdown/JSON
  summary generation.

Cloud popmatch adapter outputs contained duplicate prediction writes for
Y-K0/N-K0/M1. Auditing showed duplicated keys with zero ranking rank conflicts,
and cleaned copies were generated before grouped diagnostics.

## Claim Boundaries

- Do not claim that M1 surpasses N-K0.
- Do not treat Y-K0 ranking as next-interaction ranking.
- Do not infer that cold-item ranking is solved; the coldest bucket is small.
- Do not start hard-negative training or Phase 3 method changes from this report
  alone.

## Verification

Local targeted tests:

```text
C:\Users\33967\AppData\Local\Programs\Python\Python312\python.exe -m pytest tests\test_candidate_sets.py tests\test_analysis_outputs.py --basetemp .pytest_tmp_phase2c
22 passed
```

Stage guard before wiki sync:

```text
C:\Users\33967\AppData\Local\Programs\Python\Python312\python.exe tools\stage_guard.py
0 error(s), 0 warning(s)
```
