# Exposure Accounting Audit

## Definition

Task-sample exposure is the number of task training examples actually consumed during optimization. It is not unique coverage, raw interaction count, token count, FLOPs, or wall-clock compute.

## Evidence Status

Local evidence directly verifies code/config/data counts and existing stage-local result tables. The formal cloud LLM run directories and `trainer_state.json` files are not present in this local workspace, so resume readiness and exact saved optimizer/scheduler/RNG state remain gated by a cloud checkpoint inventory.

## MovieLens-1M Pools

| pool | available train samples | formal loaded cap | cap coverage of available |
|---|---:|---:|---:|
| Y preference | 976284 | 200000 | 20.4858% |
| N next-item | 212725 | 200000 | 94.0170% |

## Current LLM Anchors

| model | optimizer steps | effective batch | total exposure | Y exposure | N exposure | loaded pool coverage | available pool coverage | repetition |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| Y-K0 current | 1500 | 8 | 12000 | 12000 | 0 | 6.0% of Y cap | 1.2292% of Y available | none expected before first loaded-pool pass |
| N-K0 current | 1500 | 8 | 12000 | 0 | 12000 | 6.0% of N cap | 5.6411% of N available | none expected before first loaded-pool pass |
| M1 current | 3000 | 8 | 24000 | 12000 | 12000 | 6.0% of each cap | Y 1.2292%; N 5.6411% | none under sequential 1:1 prefix |

The "current approximately 12k" statement is confirmed for Y-K0 and N-K0 as 12,000 task-sample exposure, and for M1 as 12,000 Y plus 12,000 N exposure (24,000 total).

## Existing SASRec Points

| point | steps | effective batch | N exposure | unique N samples | repeated samples | loaded cap coverage | available N coverage | HR@1 | NDCG@5 | MRR |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| sasrec_s6 | 6 | 512 | 3072 | 3072 | 0 | 1.536% | 1.4441% | 0.2112775330 | 0.6011741153 | 0.4713597651 |
| sasrec_s12 | 12 | 512 | 6144 | 6144 | 0 | 3.072% | 2.8882% | 0.2421145374 | 0.6176512047 | 0.4930631424 |
| sasrec_s23 | 23 | 512 | 11776 | 11776 | 0 | 5.888% | 5.5367% | 0.2699559471 | 0.6348928207 | 0.5156622614 |
| sasrec_s47 | 47 | 512 | 24064 | 24064 | 0 | 12.032% | 11.3123% | 0.2840528634 | 0.6429537473 | 0.5261879589 |
| sasrec_s1500 | 1500 | 512 | 767424 | 200000 | 567424 | 100% | 94.017% | 0.6088105727 | 0.8198039644 | 0.7595506608 |
| sasrec_s3000 | 3000 | 512 | 1534656 | 200000 | 1334656 | 100% | 94.017% | 0.6243171806 | 0.8283562609 | 0.7708663730 |

## Scheduler / Resume Audit

- LLM TrainingArguments do not explicitly set `lr_scheduler_type`.
- Hugging Face defaults should be treated as total-step-dependent unless the cloud package version or run config proves otherwise.
- Rerunning from scratch with larger `max_steps` changes the LR trajectory relative to the original 12k prefix.
- Preferred route: strict resume from current checkpoints, preserving optimizer, scheduler, trainer, and RNG state.
- Resume is not yet proven because formal cloud checkpoint directories are not present locally.

Required cloud check before training:

```bash
find /root/llamarec/outputs/{y,n,m}/movielens-1m -maxdepth 3 \
  \( -name trainer_state.json -o -name optimizer.pt -o -name scheduler.pt -o -name 'rng_state*.pth' \) \
  -print
```

## Token Exposure

Not completed in this local audit. Formal `encoded_dataset_summary.json` files are expected in cloud run directories, but are not present locally. If easy to recover on cloud, record mean input tokens and total approximate input tokens as supporting diagnostics only.
