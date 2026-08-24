#!/usr/bin/env bash
set -euo pipefail

ROOT=${ROOT:-/root/llamarec}
cd "$ROOT"

LOG_DIR=${LOG_DIR:-logs/exposure_scaling}
mkdir -p "$LOG_DIR"
TS=$(date +%Y%m%d_%H%M%S)
LOG="$LOG_DIR/gpu_batch1_eval_${TS}.log"
PID_FILE="$LOG.pid"

nohup bash .agent/exposure_scaling/commands/gpu_batch1_eval.sh > "$LOG" 2>&1 &
PID=$!
echo "$PID" > "$PID_FILE"

echo "started gpu_batch1_eval.sh"
echo "pid: $PID"
echo "log: $LOG"
echo "pid_file: $PID_FILE"
echo ""
echo "tailing log; press Ctrl-C to stop watching without stopping evaluation"
tail -n 80 -f "$LOG"
