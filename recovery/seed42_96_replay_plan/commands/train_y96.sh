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

BASE="recovery_runs/seed42_96/y/canonical_replay_seed42"
mkdir -p "$BASE"

python -m src.train.train_y --config configs/y_local_model.yaml --dataset movielens-1m --output-dir "$BASE/canonical_replay_y_s1500_seed42" --seed 42 --max-train-samples 200000 --max-valid-samples 200000 --max-steps 1500 --per-device-train-batch-size 1 --gradient-accumulation-steps 8 --learning-rate 0.0002 --bf16 --eval-steps 1000000 --save-steps 1500 --disable-internal-eval

python -m src.train.train_y --config configs/y_local_model.yaml --dataset movielens-1m --output-dir "$BASE/canonical_replay_y_s3000_seed42" --seed 42 --max-train-samples 200000 --max-valid-samples 200000 --max-steps 3000 --per-device-train-batch-size 1 --gradient-accumulation-steps 8 --learning-rate 0.0002 --bf16 --eval-steps 1000000 --save-steps 3000 --disable-internal-eval --resume-from-checkpoint "$BASE/canonical_replay_y_s1500_seed42/checkpoints/checkpoint-1500"

python -m src.train.train_y --config configs/y_local_model.yaml --dataset movielens-1m --output-dir "$BASE/canonical_replay_y_s6000_seed42" --seed 42 --max-train-samples 200000 --max-valid-samples 200000 --max-steps 6000 --per-device-train-batch-size 1 --gradient-accumulation-steps 8 --learning-rate 0.0002 --bf16 --eval-steps 1000000 --save-steps 3000 --disable-internal-eval --resume-from-checkpoint "$BASE/canonical_replay_y_s3000_seed42/checkpoints/checkpoint-3000"

python -m src.train.train_y --config configs/y_local_model.yaml --dataset movielens-1m --output-dir "$BASE/canonical_replay_y_s12000_seed42" --seed 42 --max-train-samples 200000 --max-valid-samples 200000 --max-steps 12000 --per-device-train-batch-size 1 --gradient-accumulation-steps 8 --learning-rate 0.0002 --bf16 --eval-steps 1000000 --save-steps 3000 --disable-internal-eval --resume-from-checkpoint "$BASE/canonical_replay_y_s6000_seed42/checkpoints/checkpoint-6000"
