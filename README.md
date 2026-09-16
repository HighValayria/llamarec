# LlamaRec Recovery Workspace

This repository contains the LlamaRec MovieLens experiments, recovery plans, replay scripts, and accepted recovery artifacts. The current active work is **paper weight recovery**, not new model exploration.

## Current Status

As of 2026-09-16, the original paper-dependent trained weights are lost. Recovery work is therefore labeled:

```text
CANONICAL RECOVERY / REPLAY RUN
```

These runs are **not** the original historical checkpoints and are **not** bitwise reproductions. Frozen historical metrics and preserved paper evidence must not be overwritten.

### Seed42-96 Recovery Matrix

```text
N96 seed42   ACCEPTED
Y96 seed42   READY TO RESTART AFTER LATEST PULL
M1-96 seed42 NOT STARTED
```

N96 seed42 has completed:

```text
training                    YES
checkpoint-12000 exists     YES
validation evaluation       YES
test evaluation             YES
historical metric gate      PASS
independent backup          YES
GitHub artifact upload      YES
```

N96 final target:

```text
12000 optimizer steps x effective batch 8 = 96000 N examples exposure
```

N96 replay metrics:

```text
validation HR@1   0.6311894273
validation NDCG@5 0.8330488502
validation MRR    0.7769720999

test HR@1         0.6072246696
test NDCG@5       0.8211210947
test MRR          0.7611189427
```

The preregistered N96 comparison tolerance is `+/-0.01` absolute metric delta against frozen historical references. The comparison script returned:

```text
REPLAY_ACCEPTED
```

## Recovery Artifacts

Accepted N96 artifacts are stored under:

```text
recovery_runs/seed42_96/n/canonical_replay_seed42/
```

Important contents include:

```text
canonical_replay_n_s3000_seed42/checkpoints/checkpoint-3000
canonical_replay_n_s6000_seed42/checkpoints/checkpoint-6000
canonical_replay_n_s12000_seed42/checkpoints/checkpoint-12000
canonical_replay_n_s12000_seed42/adapter
canonical_replay_n_s12000_seed42/popmatch_eval
canonical_replay_n_s12000_seed42/n96_historical_comparison.json
```

The PopMatch-k5 evaluation output includes validation/test metrics and per-sample prediction files:

```text
n_valid_predictions.jsonl
n_test_predictions.jsonl
valid_metrics.json
test_metrics.json
```

Base-model provenance is preserved as manifests, not as full base-model weights:

```text
recovery/seed42_96_replay_plan/n96_launch/BASE_MODEL_MANIFEST.json
recovery/seed42_96_replay_plan/n96_launch/BASE_MODEL_SHA256SUMS.txt
```

The recovered base model revision used for N96 recovery is:

```text
0cb88a4f764b7a12671c53f0838cd831a0843b95
```

Large recovery binaries are tracked with Git LFS:

```text
*.safetensors
*.pt
*.pth
*.bin
*.tar.gz
*.zst
```

Do not commit full base-model directories such as:

```text
models/Llama-3.2-3B-Instruct/
```

## Recovery Plan Entry Points

Canonical recovery files live under:

```text
recovery/seed42_96_replay_plan/
```

Main documents:

```text
REPLAY_MASTER_PLAN.md
REPLAY_ACCEPTANCE_POLICY.md
environment_replay.md
requirements_replay.txt
```

Replay configs:

```text
configs/n96_replay.yaml
configs/y96_replay.yaml
configs/m1_96_replay.yaml
```

Shared commands:

```text
commands/setup_environment.sh
commands/preflight.sh
commands/train_y96.sh
commands/eval_y96.sh
commands/train_m1_96.sh
commands/eval_m1_96.sh
```

N96 has a dedicated finalized launch package:

```text
n96_launch/run_n96_preflight.sh
n96_launch/train_n96_canonical.sh
n96_launch/eval_n96_canonical.sh
n96_launch/compare_n96_historical.py
n96_launch/backup_n96.sh
```

## Server Setup Notes

Expected repository location on the GPU server:

```bash
cd /root/llamarec
```

Expected Python environment:

```bash
source .venv_seed42_96_replay/bin/activate
```

Expected pinned package versions include:

```text
Python        3.10 runtime on server
PyTorch       2.4.1
transformers 4.45.2
peft          0.13.2
bitsandbytes 0.44.1
accelerate    0.34.2
numpy         1.26.4
```

The server base model should be available at:

```text
/root/llamarec/models/Llama-3.2-3B-Instruct
```

The local Windows source for that model was:

```text
F:\Models\Llama-3.2-3B-Instruct
```

Before launching any recovery run on the server, pull latest main:

```bash
git pull --ff-only origin main
```

## Y96 Next Step

Y96 seed42 replay previously failed before the training loop because `transformers==4.45.2` does not accept `dtype=` in `from_pretrained`. The repository now contains the compatibility fix in `src/train/train_y.py`, using `torch_dtype=` instead.

After pulling latest main on the server, restart Y96 with:

```bash
cd /root/llamarec
source .venv_seed42_96_replay/bin/activate

git pull --ff-only origin main

if [ -d recovery_runs/seed42_96/y/canonical_replay_seed42 ]; then
  mkdir -p recovery_runs_failed_prestart
  mv recovery_runs/seed42_96/y/canonical_replay_seed42 \
     recovery_runs_failed_prestart/y_canonical_replay_seed42_failed_dtype_$(date +%Y%m%d_%H%M%S)
fi

mkdir -p logs
nohup env \
  PYTHONPATH=/root/llamarec \
  RUN_REPLAY_TRAINING=1 \
  HF_HUB_OFFLINE=1 \
  TRANSFORMERS_OFFLINE=1 \
  TOKENIZERS_PARALLELISM=false \
  bash recovery/seed42_96_replay_plan/commands/train_y96.sh \
  > logs/y96_seed42_replay.nohup.log 2>&1 &

tail -f logs/y96_seed42_replay.nohup.log
```

Y96 target chain:

```text
0 -> checkpoint-1500 -> checkpoint-3000 -> checkpoint-6000 -> checkpoint-12000
```

Y96 final target:

```text
12000 optimizer steps x effective batch 8 = 96000 Y examples exposure
```

Do not start M1-96 until Y96 has completed, been evaluated, and been backed up.

## Data And Candidate Assets

MovieLens-1M processed data expected by recovery runs:

```text
data/processed/movielens-1m/preference_train.jsonl
data/processed/movielens-1m/preference_valid.jsonl
data/processed/movielens-1m/preference_test.jsonl
data/processed/movielens-1m/next_item_train.jsonl
data/processed/movielens-1m/next_item_valid.jsonl
data/processed/movielens-1m/next_item_test.jsonl
```

PopMatch-k5 seed42 candidates:

```text
data/candidates/movielens-1m/variants/k5_popmatch_seed42/valid.jsonl
data/candidates/movielens-1m/variants/k5_popmatch_seed42/test.jsonl
```

Expected hashes are recorded in:

```text
recovery/seed42_96_replay_plan/manifests/expected_data_hashes.json
```

Historical frozen metric references are recorded in:

```text
recovery/seed42_96_replay_plan/manifests/expected_historical_metrics.json
```

## Historical MVP Background

The earlier MovieLens-1M MVP established the Y/N/M task framing:

```text
Y-K0: Yes/No Preference Tuning
N-K0: Full-sequence Next-item Tuning
M-K0: Y + N Multi-task Tuning
```

Y predicts `P(Like | History, Item)` using Yes/No labels derived from ratings. N predicts `P(Next Item | History, Candidate Set)` using strict chronological next-item targets. M combines both tasks and is evaluated separately as M-Y and M-N.

Legacy MVP headline results are preserved for context only:

```text
Base: test AUC 0.6205 / test HR@1 0.3167
Y-K0: test AUC 0.7691 / test HR@1 0.3048
N-K0: test HR@1 0.7189 / test NDCG@5 0.8773 / test MRR 0.8356
M-K0: test AUC 0.7234 / test HR@1 0.6717 / test NDCG@5 0.8562
```

Those older MVP numbers are not the active recovery acceptance gate. For seed42-96 recovery, use the recovery manifests, recovered artifacts, and frozen historical references listed above.

## Safety Rules

Do not overwrite accepted recovery artifacts.

Do not modify frozen historical metrics or paper evidence.

Do not commit full base-model weights.

Do not start Y96, M1-96, evaluation, or retraining without an explicit run command and the correct environment variable gate.

Do not treat recovery checkpoints as original historical checkpoints.

When uploading recovery outputs, include checkpoint state, adapter files, metrics, per-sample predictions, provenance manifests, and hash files. Use Git LFS for binary artifacts.
