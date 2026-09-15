#!/usr/bin/env bash
set -euo pipefail

if [[ "${RUN_REPLAY_EVAL:-0}" != "1" ]]; then
  echo "Refusing to run evaluation. Set RUN_REPLAY_EVAL=1 after approval."
  exit 2
fi

ROOT=${ROOT:-$(pwd)}
cd "$ROOT"

BASE="recovery_runs/seed42_96/n/canonical_replay_seed42/canonical_replay_n_s12000_seed42"

python -m src.inference.evaluate_n_adapter \
  --config configs/n_local_model.yaml \
  --dataset movielens-1m \
  --adapter-dir "$BASE/adapter" \
  --mode real \
  --splits validation test \
  --batch-size 1 \
  --valid-candidates data/candidates/movielens-1m/variants/k5_popmatch_seed42/valid.jsonl \
  --test-candidates data/candidates/movielens-1m/variants/k5_popmatch_seed42/test.jsonl \
  --output-dir "$BASE/popmatch_eval"
