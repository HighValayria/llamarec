#!/usr/bin/env bash
set -euo pipefail

# Seed43/44 Y96 + N96 + M1-96 queue for LlamaRec exposure multiseed strengthening.
# Runs one GPU job at a time. Validation is run first; test is report-only via a separate command.

ROOT=${ROOT:-/root/llamarec}
cd "$ROOT"

export HF_HUB_OFFLINE=${HF_HUB_OFFLINE:-1}
export TRANSFORMERS_OFFLINE=${TRANSFORMERS_OFFLINE:-1}
export HF_HUB_DISABLE_TELEMETRY=${HF_HUB_DISABLE_TELEMETRY:-1}
export LLAMAREC_BASE_MODEL=${LLAMAREC_BASE_MODEL:-models/Llama-3.2-3B-Instruct}
export PYTHONUNBUFFERED=${PYTHONUNBUFFERED:-1}

DATASET=${DATASET:-movielens-1m}
SEEDS=${SEEDS:-43 44}
LOG_DIR=${LOG_DIR:-logs/exposure_scaling}
K5_VALID=${K5_VALID:-data/candidates/$DATASET/variants/k5_popmatch_seed42/valid.jsonl}
K5_TEST=${K5_TEST:-data/candidates/$DATASET/variants/k5_popmatch_seed42/test.jsonl}
HARD_VARIANTS=${HARD_VARIANTS:-k20_seed42 k50_seed42}
HARD_OUT_ROOT=${HARD_OUT_ROOT:-outputs/phase2a/multiseed96_ranking_robustness}

require_compute_approval() {
  if [[ "${RUN_MULTISEED96:-0}" != "1" ]]; then
    echo "Dry run only. Use: bash $0 launch_validation"
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

require_resume_state() {
  local ckpt="$1"
  for f in trainer_state.json training_args.bin optimizer.pt scheduler.pt rng_state.pth; do
    require_file "$ckpt/$f"
  done
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

y12_ckpt() { echo "outputs/y/$DATASET/pool200k_1m_y_1500_seed$1/checkpoints/checkpoint-1500"; }
n12_ckpt() { echo "outputs/n/$DATASET/pool200k_1m_n_1500_seed$1/checkpoints/checkpoint-1500"; }
m12_ckpt() { echo "outputs/m/$DATASET/diag_m1_1m_m_200k_3000_seed$1/checkpoints/checkpoint-3000"; }
y96_run() { echo "outputs/y/$DATASET/exposure_y_s12000_seed$1"; }
n96_run() { echo "outputs/n/$DATASET/exposure_n_s12000_seed$1"; }
m96_run() { echo "outputs/m/$DATASET/exposure_m1_s24000_seed$1"; }

preflight() {
  echo "== local-only cache preflight =="
  bash .agent/exposure_scaling/commands/gpu_cache_preflight.sh
  echo
  echo "== required candidate files =="
  require_file "$K5_VALID"
  require_file "$K5_TEST"
  for variant in $HARD_VARIANTS; do
    require_file "$(candidate_file "$variant" validation)"
    require_file "$(candidate_file "$variant" test)"
  done
  echo "candidate files OK"
  echo
  echo "== required resume checkpoints =="
  for seed in $SEEDS; do
    require_resume_state "$(y12_ckpt "$seed")"
    require_resume_state "$(n12_ckpt "$seed")"
    require_resume_state "$(m12_ckpt "$seed")"
    echo "seed$seed resume checkpoints OK"
  done
}

train_y96() {
  local seed="$1"
  local out
  out=$(y96_run "$seed")
  echo "== seed$seed Y96 train: $out =="
  python -m src.train.train_y \
    --config configs/y_local_model.yaml \
    --dataset "$DATASET" \
    --run-name "exposure_y_s12000_seed$seed" \
    --seed "$seed" \
    --max-train-samples 200000 \
    --max-valid-samples 200000 \
    --max-steps 12000 \
    --per-device-train-batch-size 1 \
    --gradient-accumulation-steps 8 \
    --learning-rate 0.0002 \
    --eval-steps 1000000 \
    --save-steps 3000 \
    --disable-internal-eval \
    --resume-from-checkpoint "$(y12_ckpt "$seed")"
  require_dir "$out/adapter"
}

train_n96() {
  local seed="$1"
  local out
  out=$(n96_run "$seed")
  echo "== seed$seed N96 train: $out =="
  python -m src.train.train_n \
    --config configs/n_local_model.yaml \
    --dataset "$DATASET" \
    --run-name "exposure_n_s12000_seed$seed" \
    --seed "$seed" \
    --max-train-samples 200000 \
    --max-valid-samples 200000 \
    --max-steps 12000 \
    --per-device-train-batch-size 1 \
    --gradient-accumulation-steps 8 \
    --learning-rate 0.0002 \
    --eval-steps 1000000 \
    --save-steps 3000 \
    --disable-internal-eval \
    --bf16 \
    --resume-from-checkpoint "$(n12_ckpt "$seed")"
  require_dir "$out/adapter"
}

train_m196() {
  local seed="$1"
  local out
  out=$(m96_run "$seed")
  echo "== seed$seed M1-96 train: $out =="
  python -m src.train.train_m \
    --config configs/m_local_model.yaml \
    --dataset "$DATASET" \
    --run-name "exposure_m1_s24000_seed$seed" \
    --seed "$seed" \
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
    --resume-from-checkpoint "$(m12_ckpt "$seed")"
  require_dir "$out/adapter"
}

eval_y_k5() {
  local seed="$1"
  local out
  out=$(y96_run "$seed")
  echo "== seed$seed Y96 k5 validation eval =="
  python -m src.inference.evaluate_y_adapter \
    --config configs/y_local_model.yaml \
    --dataset "$DATASET" \
    --adapter-dir "$out/adapter" \
    --mode real \
    --splits validation \
    --batch-size 1 \
    --valid-candidates "$K5_VALID" \
    --output-dir "$out/popmatch_eval"
}

eval_n_k5() {
  local seed="$1"
  local out
  out=$(n96_run "$seed")
  echo "== seed$seed N96 k5 validation eval =="
  python -m src.inference.evaluate_n_adapter \
    --config configs/n_local_model.yaml \
    --dataset "$DATASET" \
    --adapter-dir "$out/adapter" \
    --mode real \
    --splits validation \
    --batch-size 1 \
    --valid-candidates "$K5_VALID" \
    --output-dir "$out/popmatch_eval"
}

eval_m_k5() {
  local seed="$1"
  local out
  out=$(m96_run "$seed")
  echo "== seed$seed M1-96 k5 validation eval =="
  python -m src.inference.evaluate_m_adapter \
    --config configs/m_local_model.yaml \
    --dataset "$DATASET" \
    --adapter-dir "$out/adapter" \
    --mode real \
    --splits validation \
    --batch-size 1 \
    --valid-candidates "$K5_VALID" \
    --output-dir "$out/popmatch_eval"
}

eval_hard_variant() {
  local seed="$1"
  local split="$2"
  local variant="$3"
  local cand
  cand=$(candidate_file "$variant" "$split")
  require_file "$cand"
  require_dir "$(n96_run "$seed")/adapter"
  require_dir "$(m96_run "$seed")/adapter"

  local n_out="$HARD_OUT_ROOT/seed$seed/n_k0_$variant"
  local m_out="$HARD_OUT_ROOT/seed$seed/m1_$variant"
  echo "== seed$seed $variant $split N96/M1-96 eval =="
  if [[ "$split" == "validation" ]]; then
    python -m src.inference.evaluate_n_adapter \
      --config configs/n_local_model.yaml \
      --dataset "$DATASET" \
      --adapter-dir "$(n96_run "$seed")/adapter" \
      --mode real \
      --splits validation \
      --batch-size 1 \
      --valid-candidates "$cand" \
      --output-dir "$n_out"
    python -m src.inference.evaluate_m_adapter \
      --config configs/m_local_model.yaml \
      --dataset "$DATASET" \
      --adapter-dir "$(m96_run "$seed")/adapter" \
      --mode real \
      --splits validation \
      --batch-size 1 \
      --valid-candidates "$cand" \
      --output-dir "$m_out"
  else
    python -m src.inference.evaluate_n_adapter \
      --config configs/n_local_model.yaml \
      --dataset "$DATASET" \
      --adapter-dir "$(n96_run "$seed")/adapter" \
      --mode real \
      --splits test \
      --batch-size 1 \
      --test-candidates "$cand" \
      --output-dir "$n_out"
    python -m src.inference.evaluate_m_adapter \
      --config configs/m_local_model.yaml \
      --dataset "$DATASET" \
      --adapter-dir "$(m96_run "$seed")/adapter" \
      --mode real \
      --splits test \
      --batch-size 1 \
      --test-candidates "$cand" \
      --output-dir "$m_out"
  fi
}

run_seed_validation() {
  local seed="$1"
  train_y96 "$seed"
  eval_y_k5 "$seed"
  train_n96 "$seed"
  eval_n_k5 "$seed"
  train_m196 "$seed"
  eval_m_k5 "$seed"
  for variant in $HARD_VARIANTS; do
    eval_hard_variant "$seed" validation "$variant"
  done
}

run_validation() {
  require_compute_approval
  preflight
  for seed in $SEEDS; do
    run_seed_validation "$seed"
  done
  summarize
  echo "Seed43/44 Y96 N96 M1-96 training plus validation eval finished. Use validation first; tests remain report-only."
}

run_tests() {
  require_compute_approval
  if [[ "${RUN_MULTISEED96_TESTS:-0}" != "1" ]]; then
    echo "Refusing report-only tests unless RUN_MULTISEED96_TESTS=1 is set. Use: bash $0 launch_tests"
    exit 2
  fi
  preflight
  for seed in $SEEDS; do
    echo "== seed$seed report-only k5 tests =="
    python -m src.inference.evaluate_y_adapter \
      --config configs/y_local_model.yaml \
      --dataset "$DATASET" \
      --adapter-dir "$(y96_run "$seed")/adapter" \
      --mode real \
      --splits test \
      --batch-size 1 \
      --test-candidates "$K5_TEST" \
      --output-dir "$(y96_run "$seed")/popmatch_eval"
    python -m src.inference.evaluate_n_adapter \
      --config configs/n_local_model.yaml \
      --dataset "$DATASET" \
      --adapter-dir "$(n96_run "$seed")/adapter" \
      --mode real \
      --splits test \
      --batch-size 1 \
      --test-candidates "$K5_TEST" \
      --output-dir "$(n96_run "$seed")/popmatch_eval"
    python -m src.inference.evaluate_m_adapter \
      --config configs/m_local_model.yaml \
      --dataset "$DATASET" \
      --adapter-dir "$(m96_run "$seed")/adapter" \
      --mode real \
      --splits test \
      --batch-size 1 \
      --test-candidates "$K5_TEST" \
      --output-dir "$(m96_run "$seed")/popmatch_eval"
    for variant in $HARD_VARIANTS; do
      eval_hard_variant "$seed" test "$variant"
    done
  done
  summarize
  echo "Seed43/44 report-only tests finished. Do not use tests to change training decisions."
}

summarize() {
  export DATASET SEEDS HARD_OUT_ROOT
  python - <<'PY'
import json
import os
from pathlib import Path

seeds = [s.strip() for s in os.environ.get("SEEDS", "43 44").split()]
dataset = os.environ.get("DATASET", "movielens-1m")
hard_root = Path(os.environ.get("HARD_OUT_ROOT", "outputs/phase2a/multiseed96_ranking_robustness"))
print("== multiseed96 k5 validation ==")
print("run\tseed\tsplit\tsamples\tAUC\tF1\tAccuracy\tHR@1\tNDCG@5\tMRR")
for seed in seeds:
    rows = [
        ("Y96", Path(f"outputs/y/{dataset}/exposure_y_s12000_seed{seed}/popmatch_eval/valid_metrics.json")),
        ("N96", Path(f"outputs/n/{dataset}/exposure_n_s12000_seed{seed}/popmatch_eval/valid_metrics.json")),
        ("M1-96", Path(f"outputs/m/{dataset}/exposure_m1_s24000_seed{seed}/popmatch_eval/valid_metrics.json")),
    ]
    for run, path in rows:
        if not path.exists():
            print(f"{run}\t{seed}\tvalidation\tMISSING\tMISSING\tMISSING\tMISSING\tMISSING\tMISSING\tMISSING")
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        binary = data.get("binary", {})
        ranking = data.get("ranking", {})
        samples = binary.get("samples") or ranking.get("samples")
        print("\t".join(str(x) for x in [
            run, seed, "validation", samples,
            binary.get("AUC", ""), binary.get("F1", ""), binary.get("Accuracy", ""),
            ranking.get("HR@1", ""), ranking.get("NDCG@5", ""), ranking.get("MRR", ""),
        ]))
print()
print("== multiseed96 hard-candidate validation ==")
print("run\tseed\tvariant\tsamples\tHR@1\tNDCG@5\tMRR")
for seed in seeds:
    for path in sorted((hard_root / f"seed{seed}").glob("*/valid_metrics.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        ranking = data.get("ranking", {})
        name = path.parent.name
        if name.startswith("n_k0_"):
            run = "N96"
            variant = name[len("n_k0_"):]
        elif name.startswith("m1_"):
            run = "M1-96"
            variant = name[len("m1_"):]
        else:
            run = name
            variant = ""
        print("\t".join(str(x) for x in [run, seed, variant, ranking.get("samples"), ranking.get("HR@1"), ranking.get("NDCG@5"), ranking.get("MRR")]))
PY
}

progress() {
  echo "== time =="
  date
  echo
  echo "== process =="
  pgrep -af "src.train.train_[ynm]|evaluate_[ynm]_adapter|multiseed96_queue" || true
  echo
  echo "== newest logs =="
  ls -lt "$LOG_DIR"/multiseed96_*.log 2>/dev/null | head -5 || true
  echo
  echo "== latest log tail =="
  local log
  log=$(ls -t "$LOG_DIR"/multiseed96_*.log 2>/dev/null | head -n 1 || true)
  if [[ -n "$log" ]]; then
    echo "LOG=$log"
    tail -n 80 "$log"
  else
    echo "no multiseed96 log found"
  fi
  echo
  echo "== outputs =="
  for seed in $SEEDS; do
    for d in "$(y96_run "$seed")" "$(n96_run "$seed")" "$(m96_run "$seed")"; do
      if [[ -d "$d" ]]; then
        find "$d" -maxdepth 3 -type f \( -name 'metrics.json' -o -name 'valid_metrics.json' -o -name 'test_metrics.json' -o -name 'adapter_model.safetensors' \) -printf '%TY-%Tm-%Td %TH:%TM:%TS %p\n' | sort | tail -12
      else
        echo "MISSING_DIR $d"
      fi
    done
  done
}

launch_validation() {
  mkdir -p "$LOG_DIR"
  local ts log
  ts=$(date +%Y%m%d_%H%M%S)
  log="$LOG_DIR/multiseed96_validation_${ts}.log"
  RUN_MULTISEED96=1 nohup bash "$0" validation > "$log" 2>&1 &
  echo $! > "$log.pid"
  echo "LOG=$log PID=$(cat "$log.pid")"
  echo "tailing log; press Ctrl-C to stop watching without stopping training/evaluation"
  tail -n 80 -f "$log"
}

launch_tests() {
  mkdir -p "$LOG_DIR"
  local ts log
  ts=$(date +%Y%m%d_%H%M%S)
  log="$LOG_DIR/multiseed96_report_only_tests_${ts}.log"
  RUN_MULTISEED96=1 RUN_MULTISEED96_TESTS=1 nohup bash "$0" tests > "$log" 2>&1 &
  echo $! > "$log.pid"
  echo "LOG=$log PID=$(cat "$log.pid")"
  echo "tailing log; press Ctrl-C to stop watching without stopping report-only tests"
  tail -n 80 -f "$log"
}

case "${1:-usage}" in
  preflight) preflight ;;
  validation) run_validation ;;
  tests) run_tests ;;
  summarize) summarize ;;
  progress) progress ;;
  launch_validation) launch_validation ;;
  launch_tests) launch_tests ;;
  usage|*)
    echo "Usage:"
    echo "  bash $0 preflight"
    echo "  bash $0 launch_validation"
    echo "  bash $0 progress"
    echo "  bash $0 summarize"
    echo "  bash $0 launch_tests"
    echo "Optional: SEEDS='43 44' HARD_VARIANTS='k20_seed42 k50_seed42' bash $0 launch_validation"
    ;;
esac
