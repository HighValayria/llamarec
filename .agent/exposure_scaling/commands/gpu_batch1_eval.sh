#!/usr/bin/env bash
set -euo pipefail

# Batch 1 cloud evaluation on fixed k5_popmatch_seed42 candidates.
# Run after gpu_batch1_train.sh finishes and adapters exist.

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

require_dir() {
  local path="$1"
  if [[ ! -d "$path" ]]; then
    echo "MISSING: $path" >&2
    exit 2
  fi
}

require_file "$VALID_POPMATCH"
require_file "$TEST_POPMATCH"

Y24=outputs/y/movielens-1m/exposure_y_s3000
Y48=outputs/y/movielens-1m/exposure_y_s6000
N48=outputs/n/movielens-1m/exposure_n_s6000

require_dir "$Y24/adapter"
require_dir "$Y48/adapter"
require_dir "$N48/adapter"

python -m src.inference.evaluate_y_adapter \
  --config configs/y_local_model.yaml \
  --dataset movielens-1m \
  --adapter-dir "$Y24/adapter" \
  --mode real \
  --splits validation test \
  --batch-size 1 \
  --valid-candidates "$VALID_POPMATCH" \
  --test-candidates "$TEST_POPMATCH" \
  --output-dir "$Y24/popmatch_eval"

python -m src.inference.evaluate_y_adapter \
  --config configs/y_local_model.yaml \
  --dataset movielens-1m \
  --adapter-dir "$Y48/adapter" \
  --mode real \
  --splits validation test \
  --batch-size 1 \
  --valid-candidates "$VALID_POPMATCH" \
  --test-candidates "$TEST_POPMATCH" \
  --output-dir "$Y48/popmatch_eval"

python -m src.inference.evaluate_n_adapter \
  --config configs/n_local_model.yaml \
  --dataset movielens-1m \
  --adapter-dir "$N48/adapter" \
  --mode real \
  --splits validation test \
  --batch-size 1 \
  --valid-candidates "$VALID_POPMATCH" \
  --test-candidates "$TEST_POPMATCH" \
  --output-dir "$N48/popmatch_eval"

cat <<'MSG'

Evaluation batch finished. Use validation metrics first for the 96k decision;
test metrics are for final reporting after the validation decision is fixed.
MSG
