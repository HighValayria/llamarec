#!/usr/bin/env bash
set -euo pipefail

# N-K0 near-full-pool cloud training: 200k N-task exposure.
# Validation-first decision on 2026-08-29: N48 -> N96 still improved, so continue N only.

ROOT=${ROOT:-/root/llamarec}
cd "$ROOT"

export HF_HUB_OFFLINE=${HF_HUB_OFFLINE:-1}
export TRANSFORMERS_OFFLINE=${TRANSFORMERS_OFFLINE:-1}
export HF_HUB_DISABLE_TELEMETRY=${HF_HUB_DISABLE_TELEMETRY:-1}
export LLAMAREC_BASE_MODEL=${LLAMAREC_BASE_MODEL:-models/Llama-3.2-3B-Instruct}
export PYTHONUNBUFFERED=${PYTHONUNBUFFERED:-1}

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

N96=outputs/n/movielens-1m/exposure_n_s12000/checkpoints/checkpoint-12000
require_resume_state "$N96"

# N-K0 200k: 25000 steps * 8 samples/step = 200000 N exposure.
python -m src.train.train_n \
  --config configs/n_local_model.yaml \
  --dataset movielens-1m \
  --run-name exposure_n_s25000 \
  --max-train-samples 200000 \
  --max-valid-samples 200000 \
  --max-steps 25000 \
  --per-device-train-batch-size 1 \
  --gradient-accumulation-steps 8 \
  --learning-rate 0.0002 \
  --bf16 \
  --resume-from-checkpoint "$N96"

N200=outputs/n/movielens-1m/exposure_n_s25000/checkpoints/checkpoint-25000
require_resume_state "$N200"

cat <<'MSG'

N200 training finished. Next step: fixed PopMatch validation/test evaluation.
MSG
