#!/usr/bin/env bash
set -euo pipefail

if [[ "${RUN_REPLAY_EVAL:-0}" != "1" ]]; then
  echo "Refusing to run evaluation. Set RUN_REPLAY_EVAL=1 after approval."
  exit 2
fi

ROOT=${ROOT:-$(pwd)}
cd "$ROOT"

BASE="recovery_runs/seed42_96/m1/canonical_replay_seed42/canonical_replay_m1_s24000_seed42"

python -m src.inference.evaluate_m_adapter \
  --config configs/m_local_model.yaml \
  --dataset movielens-1m \
  --adapter-dir "$BASE/adapter" \
  --mode real \
  --splits validation test \
  --batch-size 1 \
  --valid-candidates data/candidates/movielens-1m/variants/k5_popmatch_seed42/valid.jsonl \
  --test-candidates data/candidates/movielens-1m/variants/k5_popmatch_seed42/test.jsonl \
  --output-dir "$BASE/popmatch_eval"
