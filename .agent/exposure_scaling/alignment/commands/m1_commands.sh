#!/usr/bin/env bash
set -euo pipefail

ROOT=${ROOT:-/root/llamarec}
cd "$ROOT"

export HF_HUB_OFFLINE=1
export TRANSFORMERS_OFFLINE=1
export HF_HUB_DISABLE_TELEMETRY=1
export LLAMAREC_BASE_MODEL=${LLAMAREC_BASE_MODEL:-models/Llama-3.2-3B-Instruct}

VALID_CAND=${VALID_CAND:-data/candidates/movielens-1m/variants/k5_popmatch_seed42/valid.jsonl}
TEST_CAND=${TEST_CAND:-data/candidates/movielens-1m/variants/k5_popmatch_seed42/test.jsonl}
M1_12_CKPT=${M1_12_CKPT:-outputs/m/movielens-1m/diag_m1_1m_m_200k_3000/checkpoints/checkpoint-3000}
M1_48_CKPT=${M1_48_CKPT:-outputs/m/movielens-1m/exposure_m1_s12000/checkpoints/checkpoint-12000}
M1_48_RUN=${M1_48_RUN:-outputs/m/movielens-1m/exposure_m1_s12000}
M1_96_RUN=${M1_96_RUN:-outputs/m/movielens-1m/exposure_m1_s24000}

require_resume_state() {
  local ckpt="$1"
  for f in trainer_state.json optimizer.pt scheduler.pt rng_state.pth; do
    if [[ ! -f "$ckpt/$f" ]]; then
      echo "ERROR: missing resume file $ckpt/$f" >&2
      exit 2
    fi
  done
}

require_gpu_approval() {
  if [[ "${RUN_M1_COMMANDS:-0}" != "1" ]]; then
    echo "Dry run only. Set RUN_M1_COMMANDS=1 or use: bash $0 launch_m1_48"
    exit 2
  fi
}

run_m1_48() {
  require_gpu_approval
  require_resume_state "$M1_12_CKPT"
  python -m src.train.train_m \
    --config configs/m_local_model.yaml \
    --dataset movielens-1m \
    --run-name exposure_m1_s12000 \
    --max-y-train-samples 200000 \
    --max-n-train-samples 200000 \
    --max-y-valid-samples 200000 \
    --max-n-valid-samples 200000 \
    --task-ratio-y 1 \
    --task-ratio-n 1 \
    --max-steps 12000 \
    --per-device-train-batch-size 1 \
    --gradient-accumulation-steps 8 \
    --learning-rate 0.0002 \
    --eval-steps 1500 \
    --save-steps 1500 \
    --resume-from-checkpoint "$M1_12_CKPT"

  python -m src.inference.evaluate_m_adapter \
    --config configs/m_local_model.yaml \
    --dataset movielens-1m \
    --adapter-dir outputs/m/movielens-1m/exposure_m1_s12000/adapter \
    --mode real \
    --splits validation test \
    --batch-size 1 \
    --valid-candidates "$VALID_CAND" \
    --test-candidates "$TEST_CAND" \
    --output-dir outputs/m/movielens-1m/exposure_m1_s12000/popmatch_eval

  echo "M1-48 train/eval finished. Compare validation against N48 first; test is report-only."
}


run_m1_96() {
  require_gpu_approval
  require_resume_state "$M1_48_CKPT"
  python -m src.train.train_m \
    --config configs/m_local_model.yaml \
    --dataset movielens-1m \
    --run-name exposure_m1_s24000 \
    --max-y-train-samples 200000 \
    --max-n-train-samples 200000 \
    --max-y-valid-samples 200000 \
    --max-n-valid-samples 200000 \
    --task-ratio-y 1 \
    --task-ratio-n 1 \
    --max-steps 24000 \
    --per-device-train-batch-size 1 \
    --gradient-accumulation-steps 8 \
    --learning-rate 0.0002 \
    --eval-steps 1000000 \
    --save-steps 3000 \
    --disable-internal-eval \
    --resume-from-checkpoint "$M1_48_CKPT"

  python -m src.inference.evaluate_m_adapter \
    --config configs/m_local_model.yaml \
    --dataset movielens-1m \
    --adapter-dir outputs/m/movielens-1m/exposure_m1_s24000/adapter \
    --mode real \
    --splits validation \
    --batch-size 1 \
    --valid-candidates "$VALID_CAND" \
    --output-dir outputs/m/movielens-1m/exposure_m1_s24000/popmatch_eval_valid_only

  echo "M1-96 train/validation eval finished. Compare validation against N96 first; test is report-only and has not been run."
}


run_m1_test_only() {
  require_gpu_approval
  if [[ "${RUN_M1_TESTS:-0}" != "1" ]]; then
    echo "Refusing to run report-only test eval unless RUN_M1_TESTS=1 is set."
    echo "Use: bash $0 launch_m1_tests"
    exit 2
  fi
  if [[ "${INCLUDE_M1_48_TEST:-1}" == "1" ]]; then
    if [[ ! -d "$M1_48_RUN/adapter" ]]; then
      echo "ERROR: missing adapter $M1_48_RUN/adapter" >&2
      exit 2
    fi
    python -m src.inference.evaluate_m_adapter \
      --config configs/m_local_model.yaml \
      --dataset movielens-1m \
      --adapter-dir "$M1_48_RUN/adapter" \
      --mode real \
      --splits test \
      --batch-size 1 \
      --test-candidates "$TEST_CAND" \
      --output-dir "$M1_48_RUN/popmatch_eval"
  fi

  if [[ "${INCLUDE_M1_96_TEST:-1}" == "1" ]]; then
    if [[ ! -d "$M1_96_RUN/adapter" ]]; then
      echo "ERROR: missing adapter $M1_96_RUN/adapter" >&2
      exit 2
    fi
    python -m src.inference.evaluate_m_adapter \
      --config configs/m_local_model.yaml \
      --dataset movielens-1m \
      --adapter-dir "$M1_96_RUN/adapter" \
      --mode real \
      --splits test \
      --batch-size 1 \
      --test-candidates "$TEST_CAND" \
      --output-dir "$M1_96_RUN/popmatch_eval"
  fi

  echo "M1 report-only test eval finished. Do not use these metrics to change training decisions."
}

launch_m1_tests() {
  mkdir -p logs/exposure_scaling
  local ts log
  ts=$(date +%Y%m%d_%H%M%S)
  log="logs/exposure_scaling/m1_report_only_tests_${ts}.log"
  RUN_M1_COMMANDS=1 RUN_M1_TESTS=1 nohup bash "$0" m1_tests > "$log" 2>&1 &
  echo $! > "$log.pid"
  echo "LOG=$log PID=$(cat "$log.pid")"
  echo "tailing log; press Ctrl-C to stop watching without stopping evaluation"
  tail -n 80 -f "$log"
}
launch_m1_96() {
  mkdir -p logs/exposure_scaling
  local ts log
  ts=$(date +%Y%m%d_%H%M%S)
  log="logs/exposure_scaling/m1_96_train_then_valid_eval_${ts}.log"
  RUN_M1_COMMANDS=1 nohup bash "$0" m1_96 > "$log" 2>&1 &
  echo $! > "$log.pid"
  echo "LOG=$log PID=$(cat "$log.pid")"
  echo "tailing log; press Ctrl-C to stop watching without stopping training"
  tail -n 80 -f "$log"
}
launch_m1_48() {
  mkdir -p logs/exposure_scaling
  local ts log
  ts=$(date +%Y%m%d_%H%M%S)
  log="logs/exposure_scaling/m1_48_train_then_eval_${ts}.log"
  RUN_M1_COMMANDS=1 nohup bash "$0" m1_48 > "$log" 2>&1 &
  echo $! > "$log.pid"
  echo "LOG=$log PID=$(cat "$log.pid")"
  echo "tailing log; press Ctrl-C to stop watching without stopping training"
  tail -n 80 -f "$log"
}

case "${1:-usage}" in
  m1_48) run_m1_48 ;;
  m1_96) run_m1_96 ;;
  m1_tests) run_m1_test_only ;;
  launch_m1_48) launch_m1_48 ;;
  launch_m1_96) launch_m1_96 ;;
  launch_m1_tests) launch_m1_tests ;;
  usage|*)
    echo "Usage:"
    echo "  bash $0 launch_m1_48"
    echo "  bash $0 launch_m1_96"
    echo "  bash $0 launch_m1_tests"
    echo "  RUN_M1_COMMANDS=1 bash $0 m1_48"
    echo "  RUN_M1_COMMANDS=1 bash $0 m1_96"
    echo "  RUN_M1_COMMANDS=1 RUN_M1_TESTS=1 bash $0 m1_tests"
    ;;
esac
