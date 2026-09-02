#!/usr/bin/env bash
set -euo pipefail

ROOT=${ROOT:-/root/llamarec}
cd "$ROOT"

export HF_HUB_OFFLINE=${HF_HUB_OFFLINE:-1}
export TRANSFORMERS_OFFLINE=${TRANSFORMERS_OFFLINE:-1}
export HF_HUB_DISABLE_TELEMETRY=${HF_HUB_DISABLE_TELEMETRY:-1}
export LLAMAREC_BASE_MODEL=${LLAMAREC_BASE_MODEL:-models/Llama-3.2-3B-Instruct}
export PYTHONUNBUFFERED=${PYTHONUNBUFFERED:-1}

VALID_CAND=${VALID_CAND:-data/candidates/movielens-1m/variants/k5_popmatch_seed42/valid.jsonl}
TEST_CAND=${TEST_CAND:-data/candidates/movielens-1m/variants/k5_popmatch_seed42/test.jsonl}
Y48_CKPT=${Y48_CKPT:-outputs/y/movielens-1m/exposure_y_s6000/checkpoints/checkpoint-6000}
Y96_RUN=${Y96_RUN:-outputs/y/movielens-1m/exposure_y_s12000}

require_file() {
  local path="$1"
  if [[ ! -e "$path" ]]; then
    echo "MISSING: $path" >&2
    exit 2
  fi
}

require_dir() {
  local path="$1"
  if [[ ! -d "$path" ]]; then
    echo "MISSING: $path" >&2
    exit 2
  fi
}

require_resume_state() {
  local ckpt="$1"
  for f in trainer_state.json optimizer.pt scheduler.pt rng_state.pth; do
    require_file "$ckpt/$f"
  done
}

require_gpu_approval() {
  if [[ "${RUN_Y_COMMANDS:-0}" != "1" ]]; then
    echo "Dry run only. Set RUN_Y_COMMANDS=1 or use: bash $0 launch_y96"
    exit 2
  fi
}

summary() {
  python .agent/exposure_scaling/alignment/commands/eval_coverage_summary.py
}

run_y96() {
  require_gpu_approval
  require_resume_state "$Y48_CKPT"
  python -m src.train.train_y \
    --config configs/y_local_model.yaml \
    --dataset movielens-1m \
    --run-name exposure_y_s12000 \
    --max-train-samples 200000 \
    --max-valid-samples 200000 \
    --max-steps 12000 \
    --per-device-train-batch-size 1 \
    --gradient-accumulation-steps 8 \
    --learning-rate 0.0002 \
    --eval-steps 1000000 \
    --save-steps 3000 \
    --disable-internal-eval \
    --resume-from-checkpoint "$Y48_CKPT"

  require_file "$VALID_CAND"
  require_dir "$Y96_RUN/adapter"
  python -m src.inference.evaluate_y_adapter \
    --config configs/y_local_model.yaml \
    --dataset movielens-1m \
    --adapter-dir "$Y96_RUN/adapter" \
    --mode real \
    --splits validation \
    --batch-size 1 \
    --valid-candidates "$VALID_CAND" \
    --output-dir "$Y96_RUN/popmatch_eval_valid_only"

  echo "Y96 train/validation eval finished. Use binary validation first for Y-native convergence; ranking is Y-as-ranker only."
}

launch_y96() {
  mkdir -p logs/exposure_scaling
  local ts log
  ts=$(date +%Y%m%d_%H%M%S)
  log="logs/exposure_scaling/y96_train_then_valid_eval_${ts}.log"
  RUN_Y_COMMANDS=1 nohup bash "$0" y96 > "$log" 2>&1 &
  echo $! > "$log.pid"
  echo "LOG=$log PID=$(cat "$log.pid")"
  echo "tailing log; press Ctrl-C to stop watching without stopping training"
  tail -n 80 -f "$log"
}

case "${1:-usage}" in
  summary) summary ;;
  y96) run_y96 ;;
  launch_y96) launch_y96 ;;
  usage|*)
    echo "Usage:"
    echo "  bash $0 summary"
    echo "  bash $0 launch_y96"
    echo "  RUN_Y_COMMANDS=1 bash $0 y96"
    ;;
esac

