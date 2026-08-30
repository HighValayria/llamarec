# M1 Exposure Audit

Date: 2026-08-30
Stage: LLM Exposure Scaling & Convergence Validation
Subtask: M1 + SASRec Exposure Alignment

## Scope

This audit only resolves M1 exposure accounting and runnable planning. It does not start GPU jobs.

## Code Evidence

- `src/train/train_m.py` resolves `task_ratio_y/task_ratio_n` from CLI or config and defaults to `1:1` when neither is supplied.
- `src/train/train_m.py` uses a custom Trainer whose `_get_train_sampler` returns `SequentialSampler`, so the multitask dataset order is preserved.
- `src/train/multitask_dataset.py` builds deterministic task cycles. With ratio `1:1`, examples are interleaved as `Y,N,Y,N,...` until the smaller effective task count is exhausted.
- `src/train/train_m.py` supports `--resume-from-checkpoint`, so M1 can resume from the current `checkpoint-3000` if optimizer/scheduler/RNG state exists.

## Current M1 Run

Known current M1 checkpoint:

`outputs/m/movielens-1m/diag_m1_1m_m_200k_3000/checkpoints/checkpoint-3000`

Observed current M1 exposure:

| item | value |
|---|---:|
| max_steps | 3000 |
| per_device_train_batch_size | 1 |
| gradient_accumulation_steps | 8 |
| world_size | 1 |
| effective examples / optimizer step | 8 |
| task ratio | 1:1 |
| Y examples / optimizer step | 4 |
| N examples / optimizer step | 4 |
| Y exposure | 12000 |
| N exposure | 12000 |
| total exposure | 24000 |

## Pool Use

Stage-local accounting records formal per-task caps of 200000 examples for Y and N.

- Available Y pool: 976284 examples; formal cap: 200000.
- Available N pool: 212725 examples; formal cap: 200000.
- With M1 ratio 1:1 and caps `max_y_train_samples=200000`, `max_n_train_samples=200000`, the constructed M1 train dataset contains 200000 Y examples and 200000 N examples, total 400000.
- M1-200 at 50000 optimizer steps consumes exactly 400000 total examples, i.e. 200000 Y + 200000 N. Under this configuration it is one full interleaved pass, not repeated-pool exposure.

## Exposure Formula

For the current M1 settings:

```text
total_exposure = optimizer_steps * 8
per_task_exposure = optimizer_steps * 4
optimizer_steps = per_task_exposure / 4
```

Therefore matching N-task exposure `X` requires M1 to consume `X` N examples and `X` Y examples, total `2X` examples. This is the correct comparison for asking whether N-K0 still beats M1 at matched N-task exposure.

## Resume Status

M1 continuation should require these files before launch:

- `trainer_state.json`
- `optimizer.pt`
- `scheduler.pt`
- `rng_state.pth`
- adapter files in the checkpoint directory

If any are missing, do not call it a clean continuation; either regenerate from the last complete state or explicitly mark the run as fresh/restarted.
