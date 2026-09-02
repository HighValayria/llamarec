#!/usr/bin/env bash
set -euo pipefail

ROOT="${ROOT:-/root/llamarec}"
BOOTSTRAP_REPLICATES="${BOOTSTRAP_REPLICATES:-5000}"
OUT="${OUT:-.agent/exposure_scaling/analysis_handoff}"

cd "$ROOT"

echo "NO TRAINING: this command only reads existing artifacts."
echo "NO CHECKPOINT: no model checkpoint will be created."
echo "NO INFERENCE: no model forward pass will be launched."
echo "OUT=$OUT"
echo "BOOTSTRAP_REPLICATES=$BOOTSTRAP_REPLICATES"

python .agent/exposure_scaling/alignment/commands/seed42_deep_analysis.py \
  --root . \
  --output-dir "$OUT" \
  --bootstrap-replicates "$BOOTSTRAP_REPLICATES"

echo "Seed42 deep analysis finished. Outputs: $OUT"
