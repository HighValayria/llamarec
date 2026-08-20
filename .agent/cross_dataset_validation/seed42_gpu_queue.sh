#!/usr/bin/env bash
set -euo pipefail

cd /root/llamarec

DATASET="amazon-musical-instruments"
MODEL_DIR="models/Llama-3.2-3B-Instruct"
RANDOM_VALID="data/candidates/${DATASET}/variants/random_k5_seed42/valid.jsonl"
RANDOM_TEST="data/candidates/${DATASET}/variants/random_k5_seed42/test.jsonl"
POPMATCH_VALID="data/candidates/${DATASET}/variants/popmatch_k5_seed42/valid.jsonl"
POPMATCH_TEST="data/candidates/${DATASET}/variants/popmatch_k5_seed42/test.jsonl"
ROOT_OUT="outputs/cross_dataset_validation/${DATASET}"
STATUS="${ROOT_OUT}/seed42_queue_status.txt"
RUN_LOG="${ROOT_OUT}/seed42_queue_steps.log"

mkdir -p "$ROOT_OUT"
: > "$STATUS"
: > "$RUN_LOG"

mark() {
  echo "$1 $(date)" | tee -a "$STATUS" "$RUN_LOG"
}

run_step() {
  local name="$1"
  shift
  mark "BEGIN ${name}"
  "$@" 2>&1 | tee -a "$RUN_LOG"
  mark "DONE ${name}"
}

mark "START"

git fetch origin main
git checkout main
git pull --ff-only origin main
source .venv/bin/activate

python - <<'PY'
from pathlib import Path
import yaml

root = Path("/root/llamarec")
model_dir = root / "models" / "Llama-3.2-3B-Instruct"
if not model_dir.is_dir():
    raise SystemExit(f"local model dir missing: {model_dir}")

experiment = yaml.safe_load((root / "configs" / "experiment.yaml").read_text(encoding="utf-8"))
experiment["model"]["base_model"]["name_or_path"] = "models/Llama-3.2-3B-Instruct"
(root / "configs" / "experiment.amazon_local.generated.yaml").write_text(
    yaml.safe_dump(experiment, sort_keys=False, allow_unicode=True),
    encoding="utf-8",
)

for name in ("y", "n", "m"):
    child = yaml.safe_load((root / "configs" / f"{name}.yaml").read_text(encoding="utf-8"))
    child["inherits"] = "configs/experiment.amazon_local.generated.yaml"
    (root / "configs" / f"{name}.amazon_local.generated.yaml").write_text(
        yaml.safe_dump(child, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )

print("LOCAL_MODEL_CONFIG_OK")
PY

for path in "$RANDOM_VALID" "$RANDOM_TEST" "$POPMATCH_VALID" "$POPMATCH_TEST"; do
  test -s "$path"
done

python - <<'PY'
import torch
print("torch", torch.__version__)
print("cuda_available", torch.cuda.is_available())
print("device_count", torch.cuda.device_count())
if torch.cuda.is_available():
    print("device_name", torch.cuda.get_device_name(0))
else:
    raise SystemExit("CUDA is required for the seed42 GPU queue")
PY

run_step "base random-k5 test" \
  python -m src.inference.base_zero_shot \
    --config configs/experiment.amazon_local.generated.yaml \
    --dataset "$DATASET" \
    --mode real \
    --splits test \
    --batch-size 8 \
    --valid-candidates "$RANDOM_VALID" \
    --test-candidates "$RANDOM_TEST" \
    --output-dir "outputs/base/${DATASET}/seed42_random_k5_eval"

run_step "base popmatch-k5 test" \
  python -m src.inference.base_zero_shot \
    --config configs/experiment.amazon_local.generated.yaml \
    --dataset "$DATASET" \
    --mode real \
    --splits test \
    --batch-size 8 \
    --valid-candidates "$POPMATCH_VALID" \
    --test-candidates "$POPMATCH_TEST" \
    --output-dir "outputs/base/${DATASET}/seed42_popmatch_k5_eval"

run_step "y-k0 train seed42 s1500" \
  python -m src.train.train_y \
    --config configs/y.amazon_local.generated.yaml \
    --dataset "$DATASET" \
    --output-dir "outputs/y/${DATASET}/amazon_y_1500_seed42" \
    --seed 42 \
    --max-steps 1500 \
    --bf16

run_step "y-k0 random-k5 test" \
  python -m src.inference.evaluate_y_adapter \
    --config configs/y.amazon_local.generated.yaml \
    --dataset "$DATASET" \
    --adapter-dir "outputs/y/${DATASET}/amazon_y_1500_seed42/adapter" \
    --mode real \
    --splits test \
    --batch-size 8 \
    --valid-candidates "$RANDOM_VALID" \
    --test-candidates "$RANDOM_TEST" \
    --output-dir "outputs/y/${DATASET}/amazon_y_1500_seed42_random_k5_eval"

run_step "y-k0 popmatch-k5 test" \
  python -m src.inference.evaluate_y_adapter \
    --config configs/y.amazon_local.generated.yaml \
    --dataset "$DATASET" \
    --adapter-dir "outputs/y/${DATASET}/amazon_y_1500_seed42/adapter" \
    --mode real \
    --splits test \
    --batch-size 8 \
    --valid-candidates "$POPMATCH_VALID" \
    --test-candidates "$POPMATCH_TEST" \
    --output-dir "outputs/y/${DATASET}/amazon_y_1500_seed42_popmatch_k5_eval"

run_step "n-k0 train seed42 s1500" \
  python -m src.train.train_n \
    --config configs/n.amazon_local.generated.yaml \
    --dataset "$DATASET" \
    --output-dir "outputs/n/${DATASET}/amazon_n_1500_seed42" \
    --seed 42 \
    --max-steps 1500 \
    --bf16

run_step "n-k0 random-k5 test" \
  python -m src.inference.evaluate_n_adapter \
    --config configs/n.amazon_local.generated.yaml \
    --dataset "$DATASET" \
    --adapter-dir "outputs/n/${DATASET}/amazon_n_1500_seed42/adapter" \
    --mode real \
    --splits test \
    --batch-size 8 \
    --valid-candidates "$RANDOM_VALID" \
    --test-candidates "$RANDOM_TEST" \
    --output-dir "outputs/n/${DATASET}/amazon_n_1500_seed42_random_k5_eval"

run_step "n-k0 popmatch-k5 test" \
  python -m src.inference.evaluate_n_adapter \
    --config configs/n.amazon_local.generated.yaml \
    --dataset "$DATASET" \
    --adapter-dir "outputs/n/${DATASET}/amazon_n_1500_seed42/adapter" \
    --mode real \
    --splits test \
    --batch-size 8 \
    --valid-candidates "$POPMATCH_VALID" \
    --test-candidates "$POPMATCH_TEST" \
    --output-dir "outputs/n/${DATASET}/amazon_n_1500_seed42_popmatch_k5_eval"

run_step "m1 train seed42 s3000" \
  python -m src.train.train_m \
    --config configs/m.amazon_local.generated.yaml \
    --dataset "$DATASET" \
    --output-dir "outputs/m/${DATASET}/amazon_m1_3000_seed42" \
    --seed 42 \
    --max-steps 3000 \
    --bf16

run_step "m1 random-k5 test" \
  python -m src.inference.evaluate_m_adapter \
    --config configs/m.amazon_local.generated.yaml \
    --dataset "$DATASET" \
    --adapter-dir "outputs/m/${DATASET}/amazon_m1_3000_seed42/adapter" \
    --mode real \
    --splits test \
    --batch-size 8 \
    --valid-candidates "$RANDOM_VALID" \
    --test-candidates "$RANDOM_TEST" \
    --output-dir "outputs/m/${DATASET}/amazon_m1_3000_seed42_random_k5_eval"

run_step "m1 popmatch-k5 test" \
  python -m src.inference.evaluate_m_adapter \
    --config configs/m.amazon_local.generated.yaml \
    --dataset "$DATASET" \
    --adapter-dir "outputs/m/${DATASET}/amazon_m1_3000_seed42/adapter" \
    --mode real \
    --splits test \
    --batch-size 8 \
    --valid-candidates "$POPMATCH_VALID" \
    --test-candidates "$POPMATCH_TEST" \
    --output-dir "outputs/m/${DATASET}/amazon_m1_3000_seed42_popmatch_k5_eval"

run_step "sasrec exp-match seed42 s23 popmatch-k5 test" \
  python -m src.baselines.sasrec \
    --config configs/experiment.amazon_local.generated.yaml \
    --dataset "$DATASET" \
    --splits test \
    --output-dir "outputs/baselines/${DATASET}/sasrec_exp_match_k5_seed42_s23_popmatch_eval" \
    --valid-candidates "$POPMATCH_VALID" \
    --test-candidates "$POPMATCH_TEST" \
    --seed 42 \
    --max-steps 23 \
    --batch-size 512 \
    --device cuda

run_step "sasrec exp-match seed42 s23 random-k5 test" \
  python -m src.baselines.sasrec \
    --config configs/experiment.amazon_local.generated.yaml \
    --dataset "$DATASET" \
    --splits test \
    --output-dir "outputs/baselines/${DATASET}/sasrec_exp_match_k5_seed42_s23_random_eval" \
    --valid-candidates "$RANDOM_VALID" \
    --test-candidates "$RANDOM_TEST" \
    --model-dir "outputs/baselines/${DATASET}/sasrec_exp_match_k5_seed42_s23_popmatch_eval" \
    --device cuda

mark "ALL_DONE"

echo "== expected metric files =="
find outputs/base/"${DATASET}" outputs/y/"${DATASET}" outputs/n/"${DATASET}" outputs/m/"${DATASET}" outputs/baselines/"${DATASET}" \
  -path "*/test_metrics.json" -printf "%p %s bytes\n" | sort
