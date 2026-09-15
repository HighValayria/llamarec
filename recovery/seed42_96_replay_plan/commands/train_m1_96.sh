#!/usr/bin/env bash
set -euo pipefail

if [[ "${RUN_REPLAY_TRAINING:-0}" != "1" ]]; then
  echo "Refusing to start training. Set RUN_REPLAY_TRAINING=1 after approval."
  exit 2
fi

ROOT=${ROOT:-$(pwd)}
cd "$ROOT"

bash recovery/seed42_96_replay_plan/commands/preflight.sh

export PYTHONHASHSEED=42
export HF_HUB_DISABLE_TELEMETRY=1
export TOKENIZERS_PARALLELISM=false
export CUBLAS_WORKSPACE_CONFIG=:4096:8
export CUDA_DEVICE_ORDER=PCI_BUS_ID

BASE="recovery_runs/seed42_96/m1/canonical_replay_seed42"
mkdir -p "$BASE"

python -m src.train.train_m --config configs/m_local_model.yaml --dataset movielens-1m --output-dir "$BASE/canonical_replay_m1_s3000_seed42" --seed 42 --max-y-train-samples 200000 --max-n-train-samples 200000 --max-y-valid-samples 200000 --max-n-valid-samples 200000 --task-ratio-y 1 --task-ratio-n 1 --max-steps 3000 --per-device-train-batch-size 1 --gradient-accumulation-steps 8 --learning-rate 0.0002 --bf16 --eval-steps 1000000 --save-steps 3000 --disable-internal-eval

python -m src.train.train_m --config configs/m_local_model.yaml --dataset movielens-1m --output-dir "$BASE/canonical_replay_m1_s12000_seed42" --seed 42 --max-y-train-samples 200000 --max-n-train-samples 200000 --max-y-valid-samples 200000 --max-n-valid-samples 200000 --task-ratio-y 1 --task-ratio-n 1 --max-steps 12000 --per-device-train-batch-size 1 --gradient-accumulation-steps 8 --learning-rate 0.0002 --bf16 --eval-steps 1000000 --save-steps 3000 --disable-internal-eval --resume-from-checkpoint "$BASE/canonical_replay_m1_s3000_seed42/checkpoints/checkpoint-3000"

python -m src.train.train_m --config configs/m_local_model.yaml --dataset movielens-1m --output-dir "$BASE/canonical_replay_m1_s24000_seed42" --seed 42 --max-y-train-samples 200000 --max-n-train-samples 200000 --max-y-valid-samples 200000 --max-n-valid-samples 200000 --task-ratio-y 1 --task-ratio-n 1 --max-steps 24000 --per-device-train-batch-size 1 --gradient-accumulation-steps 8 --learning-rate 0.0002 --bf16 --eval-steps 1000000 --save-steps 3000 --disable-internal-eval --resume-from-checkpoint "$BASE/canonical_replay_m1_s12000_seed42/checkpoints/checkpoint-12000"
