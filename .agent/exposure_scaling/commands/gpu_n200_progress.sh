#!/usr/bin/env bash
set -euo pipefail

ROOT=${ROOT:-/root/llamarec}
cd "$ROOT"
LOG=$(ls -t logs/exposure_scaling/gpu_n200_train_then_eval_*.log 2>/dev/null | head -n 1 || true)
if [[ -z "$LOG" ]]; then
  echo "No N200 combined log found under logs/exposure_scaling/."
  exit 1
fi
PID=$(cat "$LOG.pid" 2>/dev/null || true)
echo "LOG=$LOG"
echo "PID=${PID:-<missing>}"
if [[ -n "$PID" ]]; then
  ps -fp "$PID" || true
fi
echo
echo "== GPU =="
nvidia-smi || true
echo
echo "== latest log =="
tail -n 120 "$LOG"
