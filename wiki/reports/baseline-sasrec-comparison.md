---
title: "Baseline SASRec Comparison"
type: report
status: current
authority: descriptive
source: mixed
created: 2026-08-11
updated: 2026-08-11
last_verified: 2026-08-11
related_code:
  - src/baselines/sasrec.py
  - src/analysis/baseline_result_summary.py
  - src/analysis/baseline_llm_comparison.py
  - tests/test_sasrec_baseline.py
  - tests/test_baseline_result_summary.py
  - tests/test_baseline_llm_comparison.py
  - scripts/run_sasrec_movielens_1m.sh
---

# Baseline SASRec Comparison

## Question

Can a specialized sequential recommender baseline explain or constrain the
MovieLens-1M next-item ranking results observed for N-K0 and M1 under the same
fixed N candidate-set contracts?

## Scope

This report covers the in-repository PyTorch SASRec-style baseline on
MovieLens-1M canonical k5 candidates and the Phase 2C `k5_popmatch_seed42`
candidate variant.

It does not claim a strict compute- or capacity-matched comparison between
SASRec and LLM adapters. N-K0 used a 200k N train pool with QLoRA, M1 used
200k Y plus 200k N examples with 1:1 sampling, and the strongest SASRec row is
a specialized sequence model trained for multiple epochs.

## Evidence

Implementation:

- `src/baselines/sasrec.py`
- `tests/test_sasrec_baseline.py`
- `src/analysis/baseline_result_summary.py`
- `src/analysis/baseline_llm_comparison.py`

Cloud artifacts:

```text
/root/llamarec/outputs/baselines/movielens-1m/sasrec_fixed_canonical_k5_e10
/root/llamarec/outputs/baselines/movielens-1m/sasrec_fixed_popmatch_k5_e10_eval
/root/llamarec/outputs/baselines/movielens-1m/sasrec_fixed_canonical_k5_200k_e1
/root/llamarec/outputs/baselines/movielens-1m/sasrec_fixed_popmatch_k5_200k_e1_eval
/root/llamarec/outputs/baselines/movielens-1m/sasrec_fixed_canonical_k5_200k_e3
/root/llamarec/outputs/baselines/movielens-1m/sasrec_fixed_popmatch_k5_200k_e3_eval
/root/llamarec/outputs/baselines/movielens-1m/summary/baseline_ranking_summary.md
/root/llamarec/outputs/baselines/movielens-1m/llm_comparison/baseline_llm_comparison.md
```

N-K0 and M1 run summaries:

- N-K0 `pool200k_1m_n_1500`: 200000 N train records loaded, 5675 validation
  records loaded.
- M1 `diag_m1_1m_m_200k_3000`: 200000 Y train records and 200000 N train
  records loaded, 1:1 task ratio, 400000 interleaved train samples.

## Findings

### Implementation correction

The first SASRec implementation used left padding with a causal Transformer
mask. Cloud budget-curve run summaries showed `epoch_losses=[nan,...]` and
identical e1/e3/e5/e10 metrics, which indicated invalid degenerate outputs.
Those pre-fix SASRec results are invalid and must not be used.

The fixed implementation uses right padding while selecting the last real
history position for scoring. It raises an error on non-finite training logits,
training loss, or candidate scores. It also supports `--model-dir` eval-only
mode so the same trained canonical SASRec model can be evaluated against
popmatch candidates without retraining.

### Fixed e10 results

The fixed e10 SASRec run used:

| setting | value |
|---|---:|
| train_examples | 212725 |
| max_sequence_length | 10 |
| embedding_dim | 64 |
| num_heads | 2 |
| num_layers | 2 |
| dropout | 0.2 |
| epochs | 10 |
| batch_size | 512 |
| learning_rate | 0.001 |
| seed | 42 |
| device | cuda |

Test metrics:

| condition | HR@1 | NDCG@5 | MRR | samples |
|---|---:|---:|---:|---:|
| fixed e10 canonical k5 | 0.7793832599 | 0.9044029047 | 0.8718942731 | 5675 |
| fixed e10 popmatch k5 eval | 0.6394713656 | 0.8345499558 | 0.7791659325 | 5675 |

The popmatch row uses `--model-dir` from the fixed e10 canonical run, so it is
the same trained model evaluated on the popularity-matched candidate condition.

### Budget curve

Fixed SASRec budget curve with full N train examples:

| epochs | canonical HR@1 | popmatch HR@1 | popmatch NDCG@5 | popmatch MRR |
|---:|---:|---:|---:|---:|
| 1 | 0.6764757709 | 0.4724229075 | 0.7517749804 | 0.6692540382 |
| 3 | 0.7538325991 | 0.5985903084 | 0.8149669269 | 0.7530983847 |
| 5 | 0.7732158590 | 0.6269603524 | 0.8285084626 | 0.7711306902 |
| 10 | 0.7793832599 | 0.6394713656 | 0.8345499558 | 0.7791659325 |

With the same 200k N train-sample cap as N-K0:

| condition | canonical HR@1 | popmatch HR@1 | popmatch NDCG@5 | popmatch MRR |
|---|---:|---:|---:|---:|
| 200k e1 | 0.6711894273 | 0.4623788546 | 0.7471518703 | 0.6630602056 |
| 200k e3 | 0.7476651982 | 0.5991189427 | 0.8144620177 | 0.7524728341 |

For reference, Phase 2C popmatch test rows were:

| model | HR@1 | NDCG@5 | MRR |
|---|---:|---:|---:|
| N-K0 | 0.5446696035 | 0.7877973813 | 0.7170837004 |
| M1 | 0.5244052863 | 0.7785009376 | 0.7046637298 |

SASRec e1 is below N-K0 and M1 on popmatch. SASRec e3, e5, and e10 are above
them on HR@1, NDCG@5, and MRR. The capped 200k e1/e3 checks reduce the train
pool mismatch but still do not make the comparison strict compute- or
capacity-matched.

## Implications

SASRec is now the strongest specialized non-LLM next-item baseline evaluated in
this repository. It is a stronger control than Popularity or BPR-MF.

The safe claim is:

```text
Under the current non-budget/capacity-matched setting, fixed SASRec becomes
stronger than N-K0 and M1 on popmatch k5 by epoch 3, while a one-epoch capped
200k SASRec run remains below them.
```

The unsafe claims are:

```text
SASRec is inherently better than LLM recommendation tuning.
LLM next-item tuning fails against sequence recommenders.
N-K0/M1 are worse methods than SASRec under matched training conditions.
```

## Open questions

- A strict compute/capacity-matched LLM-vs-SASRec study remains future work.
- Multi-seed stability has not been tested for SASRec.
- The current SASRec runs use one architecture and one seed; hyperparameter
  sensitivity is not characterized.
