#!/usr/bin/env bash
set -euo pipefail

# Creates the canonical replay Python environment. Does not download models.

ROOT=${ROOT:-$(pwd)}
cd "$ROOT"

PYTHON_BIN=${PYTHON_BIN:-python3.10}
VENV_DIR=${VENV_DIR:-.venv_seed42_96_replay}

"$PYTHON_BIN" -m venv "$VENV_DIR"
source "$VENV_DIR/bin/activate"
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r recovery/seed42_96_replay_plan/requirements_replay.txt

python - <<'PY'
import sys
import torch
import transformers
import peft
import bitsandbytes
import accelerate
print("python", sys.version)
print("torch", torch.__version__)
print("cuda_available", torch.cuda.is_available())
print("cuda", torch.version.cuda)
print("transformers", transformers.__version__)
print("peft", peft.__version__)
print("bitsandbytes", bitsandbytes.__version__)
print("accelerate", accelerate.__version__)
PY
