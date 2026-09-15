#!/usr/bin/env bash
set -euo pipefail

if [[ "${RUN_N96_REPLAY_EVAL:-0}" != "1" ]]; then
  echo "Refusing to run inference/evaluation. Set RUN_N96_REPLAY_EVAL=1 after training approval."
  exit 2
fi

ROOT=${ROOT:-$(pwd)}
cd "$ROOT"

FINAL="recovery_runs/seed42_96/n/canonical_replay_seed42/canonical_replay_n_s12000_seed42"

python -m src.inference.evaluate_n_adapter \
  --config configs/n_local_model.yaml \
  --dataset movielens-1m \
  --adapter-dir "$FINAL/adapter" \
  --mode real \
  --splits validation test \
  --batch-size 1 \
  --valid-candidates data/candidates/movielens-1m/variants/k5_popmatch_seed42/valid.jsonl \
  --test-candidates data/candidates/movielens-1m/variants/k5_popmatch_seed42/test.jsonl \
  --output-dir "$FINAL/popmatch_eval"
