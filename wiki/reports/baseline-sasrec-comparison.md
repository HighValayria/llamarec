---
title: "Baseline SASRec Comparison"
type: report
status: current
authority: descriptive
source: mixed
created: 2026-08-11
updated: 2026-08-12
last_verified: 2026-08-12
related_code:
  - src/baselines/sasrec.py
  - src/analysis/baseline_result_summary.py
  - src/analysis/baseline_llm_comparison.py
  - src/analysis/training_budget_audit.py
  - src/analysis/sample_exposure_matched_diagnostic.py
  - src/inference/evaluate_n_adapter.py
  - src/inference/evaluate_m_adapter.py
  - tests/test_sasrec_baseline.py
  - tests/test_training_budget_audit.py
  - tests/test_sample_exposure_matched_diagnostic.py
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

It also records a follow-up optimizer-step-aligned diagnostic. That diagnostic
uses eval-only N-K0 and M1 adapter scoring on the same popmatch test candidate
file as SASRec.

It does not claim a strict compute-, sample-exposure-, or capacity-matched
comparison between SASRec and LLM adapters. N-K0 used a 200k N train pool with
QLoRA, M1 used 200k Y plus 200k N examples with 1:1 sampling, and SASRec is a
small specialized sequence model with batch size 512.

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
/root/llamarec/outputs/baselines/movielens-1m/sasrec_fixed_canonical_k5_200k_s1500
/root/llamarec/outputs/baselines/movielens-1m/sasrec_fixed_popmatch_k5_200k_s1500_eval
/root/llamarec/outputs/baselines/movielens-1m/sasrec_fixed_canonical_k5_200k_s3000
/root/llamarec/outputs/baselines/movielens-1m/sasrec_fixed_popmatch_k5_200k_s3000_eval
/root/llamarec/outputs/n/movielens-1m/pool200k_1m_n_1500_popmatch_eval
/root/llamarec/outputs/m/movielens-1m/diag_m1_1m_m_200k_3000_popmatch_eval
/root/llamarec/outputs/baselines/movielens-1m/summary/baseline_ranking_summary.md
/root/llamarec/outputs/baselines/movielens-1m/llm_comparison/baseline_llm_comparison.md
```

N-K0 and M1 run summaries:

- N-K0 `pool200k_1m_n_1500`: 200000 N train records loaded, 5675 validation
  records loaded. Trainer state records `global_step=1500`, `max_steps=1500`,
  `train_batch_size=1`, and `epoch=0.06`.
- M1 `diag_m1_1m_m_200k_3000`: 200000 Y train records and 200000 N train
  records loaded, 1:1 task ratio, 400000 interleaved train samples. Trainer
  state records `global_step=3000`, `max_steps=3000`, `train_batch_size=1`,
  and `epoch=0.06`.
- N-K0 and M1 use the same QLoRA adapter setup: Llama-3.2-3B-Instruct, LoRA
  r=16, alpha=32, dropout=0.05, 4-bit NF4, and q/k/v/o/gate/up/down target
  modules.

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

### Optimizer-step-aligned popmatch diagnostic

The original N-K0 and M1 run summaries do not record candidate-file paths, and
the old N-K0 prediction candidates failed content-level equality against
`data/candidates/movielens-1m/variants/k5_popmatch_seed42/test.jsonl`. The old
N-K0/M1 `test_metrics.json` rows therefore must not be reused as popmatch
evidence.

N-K0 and M1 were re-evaluated in real adapter eval-only mode on the actual
`k5_popmatch_seed42` test candidate file:

```text
python -m src.inference.evaluate_n_adapter ... --mode real \
  --adapter-dir outputs/n/movielens-1m/pool200k_1m_n_1500/adapter \
  --splits test \
  --test-candidates data/candidates/movielens-1m/variants/k5_popmatch_seed42/test.jsonl

python -m src.inference.evaluate_m_adapter ... --mode real \
  --adapter-dir outputs/m/movielens-1m/diag_m1_1m_m_200k_3000/adapter \
  --splits test \
  --test-candidates data/candidates/movielens-1m/variants/k5_popmatch_seed42/test.jsonl
```

SASRec was also extended with `--max-steps` and evaluated at 1500 and 3000
optimizer steps from a 200k N train pool.

Same popmatch test candidate file:

| model | alignment | HR@1 | NDCG@5 | MRR | samples |
|---|---|---:|---:|---:|---:|
| N-K0 popmatch eval | 200k N loaded, 1500 LLM optimizer steps | 0.5466079295 | 0.7884963692 | 0.7180411160 | 5675 |
| M1 popmatch eval | 200k Y + 200k N loaded, 3000 LLM optimizer steps | 0.5238766520 | 0.7781912330 | 0.7042525698 | 5675 |
| SASRec s1500 popmatch | 200k N pool, 1500 optimizer steps, batch 512 | 0.6088105727 | 0.8198039644 | 0.7595506608 | 5675 |
| SASRec s3000 popmatch | 200k N pool, 3000 optimizer steps, batch 512 | 0.6243171806 | 0.8283562609 | 0.7708663730 | 5675 |

Under this same-candidate, optimizer-step-aligned diagnostic, SASRec remains
above N-K0 and M1 on N-ranking metrics. SASRec s1500 exceeds N-K0 by HR@1
`+0.0622026432`, NDCG@5 `+0.0313075952`, and MRR `+0.0415095448`. SASRec
s3000 exceeds M1 by HR@1 `+0.1004405286`, NDCG@5 `+0.0501650279`, and MRR
`+0.0666138032`.

This diagnostic is still not strict sample-exposure or compute matching:
SASRec uses batch size 512, LLM trainer states record `train_batch_size=1`, M1
splits its training across Y and N tasks, and the model families have very
different parameterization and token-level costs.

### Fair-budget follow-up

A later fair-budget positioning diagnostic audited sample exposure and added a
rough N-task sample-exposure match. It found that optimizer-step alignment
corresponds to much larger SASRec sample exposure: SASRec s1500 uses 767424 N
exposures at batch size 512, or `63.952x` N-K0's 12000 N-task exposures.

Under a rough N-task sample-exposure match, SASRec used 23 optimizer steps and
11776 N exposures, `-1.8667%` from the 12000 target. On
`k5_popmatch_seed42`, that SASRec-exp-match row scored HR@1 `0.2700`,
NDCG@5 `0.6349`, and MRR `0.5157`, below the N-K0 popmatch eval row's HR@1
`0.5466`, NDCG@5 `0.7885`, and MRR `0.7180`.

Therefore this report's optimizer-step-aligned SASRec advantage should be read
as budget-sensitive. The durable follow-up report is
[Fair-Budget Baseline Positioning](fair-budget-baseline-positioning.md).

## Implications

SASRec is now the strongest specialized non-LLM next-item baseline evaluated in
this repository. It is a stronger control than Popularity or BPR-MF.

The safe claim is:

```text
Under the current non-budget/capacity-matched setting, fixed SASRec becomes
stronger than N-K0 and M1 on popmatch k5 by epoch 3, while a one-epoch capped
200k SASRec run remains below them.
```

The follow-up optimizer-step diagnostic supports a narrower additional claim:

```text
On the same k5_popmatch_seed42 test candidate file, and when aligning only
optimizer-step count, SASRec s1500/s3000 remains above the corresponding N-K0
and M1 eval-only rows.
```

The fair-budget follow-up adds the complementary boundary:

```text
Under one rough N-task sample-exposure match, SASRec-exp-match is below N-K0;
therefore the optimizer-step-aligned advantage should not be treated as a
strict matched-budget result.
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
