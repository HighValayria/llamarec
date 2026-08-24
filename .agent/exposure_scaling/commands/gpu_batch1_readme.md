# Batch 1 GPU Commands

Status: draft only. Do not run before explicit GPU approval.

The cloud readback confirms the formal LLM training setup:

```text
per_device_train_batch_size = 1
gradient_accumulation_steps = 8
world_size = 1
train_batch_size field = 1
lr_scheduler_type = SchedulerType.LINEAR
```

Exposure per optimizer step is therefore `1 * 8 * 1 = 8` task samples.

## First Batch

Run, in order:

1. `Y-K0 24k`: resume `pool200k_1m_y_1500/checkpoint-1500` to `max_steps=3000`.
2. `Y-K0 48k`: resume the 24k Y checkpoint to `max_steps=6000`.
3. `N-K0 48k`: resume from existing N 24k if present; otherwise resume N 12k to `max_steps=6000`.
4. Run fixed PopMatch validation first, then paper-grade test only after retained checkpoints are frozen.

Script draft: `.agent/exposure_scaling/commands/gpu_batch1_train.sh`.

## Why Not N 24k?

N-K0 24k already exists in the sample-efficiency curve as `sample_efficiency_n_s3000`, so repeating it is lower value than extending to 48k.

## Stop Rule After Batch 1

Inspect validation loss and validation PopMatch metrics for 12k/24k/48k. If 24k to 48k is still clearly improving, propose 96k. Do not use repeated test checks as the continuation trigger.
