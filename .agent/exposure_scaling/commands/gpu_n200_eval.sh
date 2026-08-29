#!/usr/bin/env bash
set -euo pipefail

# N-K0 near-full-pool cloud evaluation on fixed k5_popmatch_seed42 candidates.

ROOT=${ROOT:-/root/llamarec}
cd "$ROOT"

export HF_HUB_OFFLINE=${HF_HUB_OFFLINE:-1}
export TRANSFORMERS_OFFLINE=${TRANSFORMERS_OFFLINE:-1}
export HF_HUB_DISABLE_TELEMETRY=${HF_HUB_DISABLE_TELEMETRY:-1}
export LLAMAREC_BASE_MODEL=${LLAMAREC_BASE_MODEL:-models/Llama-3.2-3B-Instruct}
export PYTHONUNBUFFERED=${PYTHONUNBUFFERED:-1}

VALID_POPMATCH=data/candidates/movielens-1m/variants/k5_popmatch_seed42/valid.jsonl
TEST_POPMATCH=data/candidates/movielens-1m/variants/k5_popmatch_seed42/test.jsonl
N200=outputs/n/movielens-1m/exposure_n_s25000

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
require_dir "$N200/adapter"

python -m src.inference.evaluate_n_adapter \
  --config configs/n_local_model.yaml \
  --dataset movielens-1m \
  --adapter-dir "$N200/adapter" \
  --mode real \
  --splits validation test \
  --batch-size 1 \
  --valid-candidates "$VALID_POPMATCH" \
  --test-candidates "$TEST_POPMATCH" \
  --output-dir "$N200/popmatch_eval"

cat <<'MSG'

N200 evaluation finished. Compare N24/N48/N96/N200 validation first; test remains report-only.
MSG
