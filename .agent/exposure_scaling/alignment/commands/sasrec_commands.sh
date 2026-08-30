#!/usr/bin/env bash
set -euo pipefail

ROOT=${ROOT:-/root/llamarec}
cd "$ROOT"

VALID_CAND=${VALID_CAND:-data/candidates/movielens-1m/variants/k5_popmatch_seed42/valid.jsonl}
TEST_CAND=${TEST_CAND:-data/candidates/movielens-1m/variants/k5_popmatch_seed42/test.jsonl}
DEVICE=${DEVICE:-cuda}

inventory() {
  echo "== SASRec model/eval inventory =="
  for d in \
    outputs/baselines/movielens-1m/sample_efficiency_sasrec_s6 \
    outputs/baselines/movielens-1m/sample_efficiency_sasrec_s12 \
    outputs/baselines/movielens-1m/sasrec_exp_match_k5_popmatch_seed42_s23 \
    outputs/baselines/movielens-1m/sample_efficiency_sasrec_s47 \
    outputs/baselines/movielens-1m/sasrec_fixed_popmatch_k5_200k_s1500 \
    outputs/baselines/movielens-1m/sasrec_fixed_popmatch_k5_200k_s3000 \
    outputs/baselines/movielens-1m/alignment_sasrec_s94 \
    outputs/baselines/movielens-1m/alignment_sasrec_s188 \
    outputs/baselines/movielens-1m/alignment_sasrec_s391
  do
    if [[ -d "$d" ]]; then
      printf '%s\tmodel_pt=%s\trun_summary=%s\n' "$d" "$([[ -f "$d/model.pt" ]] && echo yes || echo no)" "$([[ -f "$d/run_summary.json" ]] && echo yes || echo no)"
    else
      printf '%s\tMISSING\n' "$d"
    fi
  done
  echo
  echo "== existing alignment metrics =="
  find outputs/baselines/movielens-1m -maxdepth 3 -type f \( -name 'valid_metrics.json' -o -name 'test_metrics.json' \) | sort
}

require_compute_approval() {
  if [[ "${RUN_SASREC_COMMANDS:-0}" != "1" ]]; then
    echo "Dry run only. Set RUN_SASREC_COMMANDS=1 or use: bash $0 launch_minimal"
    exit 2
  fi
}

eval_existing_or_warn() {
  local label="$1"
  local model_dir="$2"
  local out_dir="$3"
  if [[ ! -f "$model_dir/model.pt" ]]; then
    echo "WARN: skip $label because $model_dir/model.pt is missing"
    return 0
  fi
  python -m src.baselines.sasrec \
    --dataset movielens-1m \
    --batch-size 512 \
    --max-train-samples 200000 \
    --max-steps 1 \
    --model-dir "$model_dir" \
    --valid-candidates "$VALID_CAND" \
    --test-candidates "$TEST_CAND" \
    --output-dir "$out_dir" \
    --device "$DEVICE"
}

train_eval_point() {
  local label="$1"
  local steps="$2"
  local out_dir="outputs/baselines/movielens-1m/alignment_sasrec_${label}"
  if [[ -f "$out_dir/run_summary.json" && -f "$out_dir/valid_metrics.json" && -f "$out_dir/test_metrics.json" ]]; then
    echo "SKIP: $label already has run_summary + valid/test metrics in $out_dir"
    return 0
  fi
  python -m src.baselines.sasrec \
    --dataset movielens-1m \
    --batch-size 512 \
    --max-train-samples 200000 \
    --max-steps "$steps" \
    --valid-candidates "$VALID_CAND" \
    --test-candidates "$TEST_CAND" \
    --output-dir "$out_dir" \
    --device "$DEVICE"
}

minimal() {
  require_compute_approval
  inventory
  eval_existing_or_warn s23 outputs/baselines/movielens-1m/sasrec_exp_match_k5_popmatch_seed42_s23 outputs/baselines/movielens-1m/alignment_sasrec_s23_popmatch_eval
  eval_existing_or_warn s47 outputs/baselines/movielens-1m/sample_efficiency_sasrec_s47 outputs/baselines/movielens-1m/alignment_sasrec_s47_popmatch_eval
  eval_existing_or_warn s1500 outputs/baselines/movielens-1m/sasrec_fixed_popmatch_k5_200k_s1500 outputs/baselines/movielens-1m/alignment_sasrec_s1500_popmatch_eval
  eval_existing_or_warn s3000 outputs/baselines/movielens-1m/sasrec_fixed_popmatch_k5_200k_s3000 outputs/baselines/movielens-1m/alignment_sasrec_s3000_popmatch_eval
  train_eval_point s94 94
  train_eval_point s188 188
  train_eval_point s391 391
  echo "SASRec alignment batch finished. Compare validation first; test remains report-only."
}

launch_minimal() {
  mkdir -p logs/exposure_scaling
  local ts log
  ts=$(date +%Y%m%d_%H%M%S)
  log="logs/exposure_scaling/sasrec_alignment_minimal_${ts}.log"
  RUN_SASREC_COMMANDS=1 nohup bash "$0" minimal > "$log" 2>&1 &
  echo $! > "$log.pid"
  echo "LOG=$log PID=$(cat "$log.pid")"
  echo "tailing log; press Ctrl-C to stop watching without stopping jobs"
  tail -n 80 -f "$log"
}

case "${1:-usage}" in
  inventory) inventory ;;
  minimal) minimal ;;
  launch_minimal) launch_minimal ;;
  usage|*)
    echo "Usage:"
    echo "  bash $0 inventory"
    echo "  bash $0 launch_minimal"
    echo "  RUN_SASREC_COMMANDS=1 bash $0 minimal"
    ;;
esac
