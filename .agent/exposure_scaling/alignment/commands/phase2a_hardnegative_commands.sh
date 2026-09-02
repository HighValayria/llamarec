#!/usr/bin/env bash
set -euo pipefail

ROOT=${ROOT:-/root/llamarec}
cd "$ROOT"

export HF_HUB_OFFLINE=${HF_HUB_OFFLINE:-1}
export TRANSFORMERS_OFFLINE=${TRANSFORMERS_OFFLINE:-1}
export HF_HUB_DISABLE_TELEMETRY=${HF_HUB_DISABLE_TELEMETRY:-1}
export LLAMAREC_BASE_MODEL=${LLAMAREC_BASE_MODEL:-models/Llama-3.2-3B-Instruct}
export PYTHONUNBUFFERED=${PYTHONUNBUFFERED:-1}

DATASET=${DATASET:-movielens-1m}
N96_RUN=${N96_RUN:-outputs/n/movielens-1m/exposure_n_s12000}
M1_96_RUN=${M1_96_RUN:-outputs/m/movielens-1m/exposure_m1_s24000}
OUT_ROOT=${OUT_ROOT:-outputs/phase2a/current96_ranking_robustness}
VARIANTS=${VARIANTS:-k20_seed42 k50_seed42}

require_compute_approval() {
  if [[ "${RUN_HARDNEG_COMMANDS:-0}" != "1" ]]; then
    echo "Dry run only. Set RUN_HARDNEG_COMMANDS=1 or use a launch_* command."
    exit 2
  fi
}

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

candidate_file() {
  local variant="$1"
  local split="$2"
  local name="test"
  if [[ "$split" == "validation" ]]; then
    name="valid"
  fi
  echo "data/candidates/$DATASET/variants/$variant/$name.jsonl"
}

generate_candidates() {
  if [[ ! -f "data/candidates/$DATASET/variants/k20_seed42/valid.jsonl" || ! -f "data/candidates/$DATASET/variants/k20_seed42/test.jsonl" ]]; then
    python -m src.eval.candidate_sets \
      --config configs/experiment.yaml \
      --dataset "$DATASET" \
      --candidate-num 20 \
      --variant-name k20_seed42 \
      --seed 42
  fi

  if [[ ! -f "data/candidates/$DATASET/variants/k50_seed42/valid.jsonl" || ! -f "data/candidates/$DATASET/variants/k50_seed42/test.jsonl" ]]; then
    python -m src.eval.candidate_sets \
      --config configs/experiment.yaml \
      --dataset "$DATASET" \
      --candidate-num 50 \
      --variant-name k50_seed42 \
      --seed 42
  fi

  if [[ " ${VARIANTS} " == *" k20_perm_seed43 "* ]]; then
    if [[ ! -f "data/candidates/$DATASET/variants/k20_perm_seed43/valid.jsonl" || ! -f "data/candidates/$DATASET/variants/k20_perm_seed43/test.jsonl" ]]; then
      python -m src.eval.candidate_sets \
        --config configs/experiment.yaml \
        --dataset "$DATASET" \
        --order-variant \
        --variant-name k20_perm_seed43 \
        --seed 43 \
        --source-valid-candidates "data/candidates/$DATASET/variants/k20_seed42/valid.jsonl" \
        --source-test-candidates "data/candidates/$DATASET/variants/k20_seed42/test.jsonl"
    fi
  fi
}

eval_one_variant() {
  local split="$1"
  local variant="$2"
  local candidate
  candidate=$(candidate_file "$variant" "$split")
  require_file "$candidate"
  require_dir "$N96_RUN/adapter"
  require_dir "$M1_96_RUN/adapter"

  local n_out="$OUT_ROOT/n_k0_$variant"
  local m_out="$OUT_ROOT/m1_$variant"

  if [[ "$split" == "validation" ]]; then
    python -m src.inference.evaluate_n_adapter \
      --config configs/n_local_model.yaml \
      --dataset "$DATASET" \
      --adapter-dir "$N96_RUN/adapter" \
      --mode real \
      --splits validation \
      --batch-size 1 \
      --valid-candidates "$candidate" \
      --output-dir "$n_out"

    python -m src.inference.evaluate_m_adapter \
      --config configs/m_local_model.yaml \
      --dataset "$DATASET" \
      --adapter-dir "$M1_96_RUN/adapter" \
      --mode real \
      --splits validation \
      --batch-size 1 \
      --valid-candidates "$candidate" \
      --output-dir "$m_out"
  else
    python -m src.inference.evaluate_n_adapter \
      --config configs/n_local_model.yaml \
      --dataset "$DATASET" \
      --adapter-dir "$N96_RUN/adapter" \
      --mode real \
      --splits test \
      --batch-size 1 \
      --test-candidates "$candidate" \
      --output-dir "$n_out"

    python -m src.inference.evaluate_m_adapter \
      --config configs/m_local_model.yaml \
      --dataset "$DATASET" \
      --adapter-dir "$M1_96_RUN/adapter" \
      --mode real \
      --splits test \
      --batch-size 1 \
      --test-candidates "$candidate" \
      --output-dir "$m_out"
  fi
}

summarize_current96() {
  python -m src.analysis.phase2a_robustness_report \
    --input-dir "$OUT_ROOT" \
    --output-dir "$OUT_ROOT" \
    --dataset "$DATASET"

  OUT_ROOT_PY="$OUT_ROOT" python - <<'PY'
import json
from pathlib import Path
import os
root = Path(os.environ["OUT_ROOT_PY"])
for split_file, split_name in [("valid_metrics.json", "VALID"), ("test_metrics.json", "TEST")]:
    print(f"== {split_name} k20/k50 current96 ==")
    print("run\tvariant\tsamples\tHR@1\tNDCG@5\tMRR")
    for path in sorted(root.glob(f"*/{split_file}")):
        metrics = json.loads(path.read_text(encoding="utf-8"))
        ranking = metrics.get("ranking", {})
        run_dir = path.parent.name
        if run_dir.startswith("n_k0_"):
            run = "N96"
            variant = run_dir[len("n_k0_"):]
        elif run_dir.startswith("m1_"):
            run = "M1-96"
            variant = run_dir[len("m1_"):]
        else:
            run = run_dir
            variant = ""
        print("\t".join(str(x) for x in [run, variant, ranking.get("samples"), ranking.get("HR@1"), ranking.get("NDCG@5"), ranking.get("MRR")]))
    print()
PY
}

run_validation() {
  require_compute_approval
  generate_candidates
  for variant in $VARIANTS; do
    eval_one_variant validation "$variant"
  done
  summarize_current96
  echo "Current96 k20/k50 validation robustness finished. Keep test report-only."
}

run_test() {
  require_compute_approval
  if [[ "${RUN_HARDNEG_TESTS:-0}" != "1" ]]; then
    echo "Refusing report-only test eval unless RUN_HARDNEG_TESTS=1 is set. Use launch_test after validation decisions are frozen."
    exit 2
  fi
  generate_candidates
  for variant in $VARIANTS; do
    eval_one_variant test "$variant"
  done
  summarize_current96
  echo "Current96 k20/k50 report-only test robustness finished. Do not use these metrics to change training decisions."
}

launch_validation() {
  mkdir -p logs/exposure_scaling
  local ts log
  ts=$(date +%Y%m%d_%H%M%S)
  log="logs/exposure_scaling/current96_k20_k50_validation_${ts}.log"
  RUN_HARDNEG_COMMANDS=1 nohup bash "$0" validation > "$log" 2>&1 &
  echo $! > "$log.pid"
  echo "LOG=$log PID=$(cat "$log.pid")"
  echo "tailing log; press Ctrl-C to stop watching without stopping evaluation"
  tail -n 80 -f "$log"
}

launch_test() {
  mkdir -p logs/exposure_scaling
  local ts log
  ts=$(date +%Y%m%d_%H%M%S)
  log="logs/exposure_scaling/current96_k20_k50_test_${ts}.log"
  RUN_HARDNEG_COMMANDS=1 RUN_HARDNEG_TESTS=1 nohup bash "$0" test > "$log" 2>&1 &
  echo $! > "$log.pid"
  echo "LOG=$log PID=$(cat "$log.pid")"
  echo "tailing log; press Ctrl-C to stop watching without stopping evaluation"
  tail -n 80 -f "$log"
}

inventory() {
  echo "== candidate files =="
  for variant in k20_seed42 k50_seed42 k20_perm_seed43; do
    for split in validation test; do
      f=$(candidate_file "$variant" "$split")
      if [[ -f "$f" ]]; then
        printf '%s\t%s\n' "$f" "OK"
      else
        printf '%s\t%s\n' "$f" "MISSING"
      fi
    done
  done
  echo
  echo "== current96 adapters =="
  printf '%s\t%s\n' "$N96_RUN/adapter" "$([[ -d "$N96_RUN/adapter" ]] && echo OK || echo MISSING)"
  printf '%s\t%s\n' "$M1_96_RUN/adapter" "$([[ -d "$M1_96_RUN/adapter" ]] && echo OK || echo MISSING)"
  echo
  echo "== existing robustness metrics =="
  find "$OUT_ROOT" -maxdepth 2 -type f \( -name 'valid_metrics.json' -o -name 'test_metrics.json' \) 2>/dev/null | sort || true
}

case "${1:-usage}" in
  inventory) inventory ;;
  generate_candidates) generate_candidates ;;
  validation) run_validation ;;
  test) run_test ;;
  summarize) summarize_current96 ;;
  launch_validation) launch_validation ;;
  launch_test) launch_test ;;
  usage|*)
    echo "Usage:"
    echo "  bash $0 inventory"
    echo "  bash $0 launch_validation"
    echo "  bash $0 launch_test"
    echo "  VARIANTS='k20_seed42 k50_seed42 k20_perm_seed43' bash $0 launch_validation"
    echo "  RUN_HARDNEG_COMMANDS=1 bash $0 validation"
    echo "  RUN_HARDNEG_COMMANDS=1 RUN_HARDNEG_TESTS=1 bash $0 test"
    ;;
esac
