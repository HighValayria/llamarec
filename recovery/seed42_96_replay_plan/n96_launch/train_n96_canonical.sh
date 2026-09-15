#!/usr/bin/env bash
set -euo pipefail

# Final launch script for N96 canonical replay. Refuses to train without
# explicit approval via RUN_N96_REPLAY_TRAINING=1.

if [[ "${RUN_N96_REPLAY_TRAINING:-0}" != "1" ]]; then
  echo "TRAINING_STARTED=NO"
  echo "Refusing to train. Set RUN_N96_REPLAY_TRAINING=1 only after approval."
  exit 2
fi

ROOT=${ROOT:-$(pwd)}
cd "$ROOT"

bash recovery/seed42_96_replay_plan/n96_launch/run_n96_preflight.sh

export PYTHONHASHSEED=42
export HF_HUB_DISABLE_TELEMETRY=1
export TOKENIZERS_PARALLELISM=false
export CUBLAS_WORKSPACE_CONFIG=:4096:8
export CUDA_DEVICE_ORDER=PCI_BUS_ID
export HF_HUB_OFFLINE=1
export TRANSFORMERS_OFFLINE=1

CONFIG="recovery/seed42_96_replay_plan/n96_launch/resolved_n96_replay_config.yaml"
BRIDGE="recovery/seed42_96_replay_plan/n96_launch/n96_replay_bridge.py"

python "$BRIDGE" --config "$CONFIG" --stage n_s3000 --launch-command "python $BRIDGE --config $CONFIG --stage n_s3000"
python "$BRIDGE" --config "$CONFIG" --stage n_s6000 --launch-command "python $BRIDGE --config $CONFIG --stage n_s6000"
python "$BRIDGE" --config "$CONFIG" --stage n_s12000 --launch-command "python $BRIDGE --config $CONFIG --stage n_s12000"
