#!/usr/bin/env bash
set -euo pipefail

ROOT=${ROOT:-/root/llamarec}
cd "$ROOT"

LOG_DIR=${LOG_DIR:-logs/exposure_scaling}
mkdir -p "$LOG_DIR"
export HF_HUB_OFFLINE=${HF_HUB_OFFLINE:-1}
export TRANSFORMERS_OFFLINE=${TRANSFORMERS_OFFLINE:-1}
export HF_HUB_DISABLE_TELEMETRY=${HF_HUB_DISABLE_TELEMETRY:-1}
export LLAMAREC_BASE_MODEL=${LLAMAREC_BASE_MODEL:-models/Llama-3.2-3B-Instruct}
export PYTHONUNBUFFERED=${PYTHONUNBUFFERED:-1}
TS=$(date +%Y%m%d_%H%M%S)
LOG="$LOG_DIR/gpu_n96_train_${TS}.log"
PREFLIGHT_LOG="$LOG_DIR/gpu_cache_preflight_n96_${TS}.log"
PID_FILE="$LOG.pid"

echo "running local-only cache preflight"
bash .agent/exposure_scaling/commands/gpu_cache_preflight.sh | tee "$PREFLIGHT_LOG"
echo "preflight_log: $PREFLIGHT_LOG"
echo ""

nohup bash .agent/exposure_scaling/commands/gpu_n96_train.sh > "$LOG" 2>&1 &
PID=$!
echo "$PID" > "$PID_FILE"

echo "started gpu_n96_train.sh"
echo "pid: $PID"
echo "log: $LOG"
echo "pid_file: $PID_FILE"
echo ""
echo "tailing log; press Ctrl-C to stop watching without stopping training"
tail -n 80 -f "$LOG"
