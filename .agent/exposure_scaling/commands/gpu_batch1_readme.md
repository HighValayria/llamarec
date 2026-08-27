# Batch 1 GPU Commands

Status: cloud-ready after commit sync.

The cloud readback confirms the formal LLM training setup:

```text
per_device_train_batch_size = 1
gradient_accumulation_steps = 8
world_size = 1
train_batch_size field = 1
lr_scheduler_type = SchedulerType.LINEAR
```

Exposure per optimizer step is therefore `1 * 8 * 1 = 8` task samples.

## Cloud Run

After pulling the latest commit on the GPU host:

```bash
cd /root/llamarec
git pull origin main
bash -n .agent/exposure_scaling/commands/gpu_batch1_train.sh
bash -n .agent/exposure_scaling/commands/gpu_batch1_eval.sh
bash .agent/exposure_scaling/commands/gpu_batch1_train_nohup.sh
```

The nohupped launcher prints the PID and log path, then tails the log. Pressing
Ctrl-C stops only the tail process, not the training job. To resume watching:

```bash
tail -n 80 -f logs/exposure_scaling/gpu_batch1_train_*.log
```

After training finishes:

```bash
bash .agent/exposure_scaling/commands/gpu_batch1_eval_nohup.sh
```


## Cache Preflight

Before launching training, the nohupped launcher now runs:

```bash
bash .agent/exposure_scaling/commands/gpu_cache_preflight.sh
```

This forces `HF_HUB_OFFLINE=1` and `TRANSFORMERS_OFFLINE=1`, then verifies the
configured base model through `local_files_only=True`. It prints the active user,
cache environment variables, Hugging Face cache scan results, tokenizer/config
resolution, and whether all indexed weight shards exist. If the cloud would need
to download anything, this preflight fails before the GPU job starts.

## First Batch

Run, in order:

1. `Y-K0 24k`: resume `pool200k_1m_y_1500/checkpoint-1500` to `max_steps=3000`.
2. `Y-K0 48k`: resume the 24k Y checkpoint to `max_steps=6000`.
3. `N-K0 48k`: resume from existing N 24k if present; otherwise resume N 12k to `max_steps=6000`.
4. Run fixed PopMatch validation first, then paper-grade test only after retained checkpoints are frozen.

## Model Path Behavior

This batch uses repo-local config files:

- `configs/y_local_model.yaml`
- `configs/n_local_model.yaml`
- `configs/m_local_model.yaml`

Those configs set `model.base_model.name_or_path` to
`models/Llama-3.2-3B-Instruct`, matching the GPU host directory shown by
`ls models`. With `HF_HUB_OFFLINE=1` and `TRANSFORMERS_OFFLINE=1`, any accidental
fallback to Hugging Face download should fail before training starts.

## Why Not N 24k?

N-K0 24k already exists in the sample-efficiency curve as `sample_efficiency_n_s3000`, so repeating it is lower value than extending to 48k.

## Stop Rule After Batch 1

Inspect validation loss and validation PopMatch metrics for 12k/24k/48k. If 24k to 48k is still clearly improving, propose 96k. Do not use repeated test checks as the continuation trigger.
