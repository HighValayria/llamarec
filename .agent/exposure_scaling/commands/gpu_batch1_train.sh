#!/usr/bin/env bash
set -euo pipefail

# Batch 1 cloud training for LLM Exposure Scaling & Convergence Validation.
# Uses repo-local base model configs: models/Llama-3.2-3B-Instruct.
# Assumes cloud readback confirmed:
#   per_device_train_batch_size=1
#   gradient_accumulation_steps=8
#   world_size=1
#   lr_scheduler_type=linear

ROOT=${ROOT:-/root/llamarec}
cd "$ROOT"

export HF_HUB_OFFLINE=${HF_HUB_OFFLINE:-1}
export TRANSFORMERS_OFFLINE=${TRANSFORMERS_OFFLINE:-1}
export HF_HUB_DISABLE_TELEMETRY=${HF_HUB_DISABLE_TELEMETRY:-1}
export LLAMAREC_BASE_MODEL=${LLAMAREC_BASE_MODEL:-models/Llama-3.2-3B-Instruct}

VALID_POPMATCH=data/candidates/movielens-1m/variants/k5_popmatch_seed42/valid.jsonl
TEST_POPMATCH=data/candidates/movielens-1m/variants/k5_popmatch_seed42/test.jsonl

require_file() {
  local path="$1"
  if [[ ! -e "$path" ]]; then
    echo "MISSING: $path" >&2
    exit 2
  fi
}

require_resume_state() {
  local ckpt="$1"
  require_file "$ckpt/trainer_state.json"
  require_file "$ckpt/training_args.bin"
  require_file "$ckpt/optimizer.pt"
  require_file "$ckpt/scheduler.pt"
  require_file "$ckpt/rng_state.pth"
}

# Existing resume anchors.
Y12=outputs/y/movielens-1m/pool200k_1m_y_1500/checkpoints/checkpoint-1500
N12=outputs/n/movielens-1m/pool200k_1m_n_1500/checkpoints/checkpoint-1500
N24=outputs/n/movielens-1m/sample_efficiency_n_s3000/checkpoints/checkpoint-3000

require_resume_state "$Y12"
require_resume_state "$N12"
if [[ -d "$N24" ]]; then
  require_resume_state "$N24"
  N_RESUME="$N24"
else
  echo "WARN: N 24k checkpoint not found; falling back to N 12k resume for N 48k." >&2
  N_RESUME="$N12"
fi

# Y-K0 24k: 3000 steps * 8 samples/step = 24000 Y exposure.
python -m src.train.train_y \
  --config configs/y_local_model.yaml \
  --dataset movielens-1m \
  --run-name exposure_y_s3000 \
  --max-train-samples 200000 \
  --max-valid-samples 200000 \
  --max-steps 3000 \
  --per-device-train-batch-size 1 \
  --gradient-accumulation-steps 8 \
  --learning-rate 0.0002 \
  --bf16 \
  --resume-from-checkpoint "$Y12"

Y24=outputs/y/movielens-1m/exposure_y_s3000/checkpoints/checkpoint-3000
require_resume_state "$Y24"

# Y-K0 48k: 6000 steps * 8 samples/step = 48000 Y exposure.
python -m src.train.train_y \
  --config configs/y_local_model.yaml \
  --dataset movielens-1m \
  --run-name exposure_y_s6000 \
  --max-train-samples 200000 \
  --max-valid-samples 200000 \
  --max-steps 6000 \
  --per-device-train-batch-size 1 \
  --gradient-accumulation-steps 8 \
  --learning-rate 0.0002 \
  --bf16 \
  --resume-from-checkpoint "$Y24"

# N-K0 48k: 6000 steps * 8 samples/step = 48000 N exposure.
python -m src.train.train_n \
  --config configs/n_local_model.yaml \
  --dataset movielens-1m \
  --run-name exposure_n_s6000 \
  --max-train-samples 200000 \
  --max-valid-samples 200000 \
  --max-steps 6000 \
  --per-device-train-batch-size 1 \
  --gradient-accumulation-steps 8 \
  --learning-rate 0.0002 \
  --bf16 \
  --resume-from-checkpoint "$N_RESUME"

cat <<'MSG'

Training batch finished. Next required step:
Run fixed PopMatch validation/test evaluation for Y exposure_y_s3000, Y exposure_y_s6000,
and N exposure_n_s6000. Do not decide 96k from test metrics; use validation first.
MSG
