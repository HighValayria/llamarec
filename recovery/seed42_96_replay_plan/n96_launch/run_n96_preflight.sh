#!/usr/bin/env bash
set -euo pipefail

# Final N96 launch preflight. Does not train, infer, or download.

ROOT=${ROOT:-$(pwd)}
cd "$ROOT"

CONFIG="recovery/seed42_96_replay_plan/n96_launch/resolved_n96_replay_config.yaml"

python - "$CONFIG" <<'PY'
import hashlib
import importlib
import json
import os
from pathlib import Path
import subprocess
import sys

import yaml

config = yaml.safe_load(Path(sys.argv[1]).read_text(encoding="utf-8"))
errors = []

def err(msg):
    errors.append(msg)

def sha256(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

required_versions = {
    "torch": "2.4.1",
    "transformers": "4.45.2",
    "peft": "0.13.2",
    "bitsandbytes": "0.44.1",
    "accelerate": "0.34.2",
    "numpy": "1.26.4",
    "scipy": "1.13.1",
    "sklearn": "1.5.2",
}
for module_name, expected_prefix in required_versions.items():
    try:
        module = importlib.import_module(module_name)
        actual = getattr(module, "__version__", "UNKNOWN")
    except Exception as exc:
        err(f"PACKAGE_IMPORT_FAILED {module_name}: {exc}")
        continue
    if not str(actual).startswith(expected_prefix):
        err(f"PACKAGE_VERSION_MISMATCH {module_name} expected_prefix={expected_prefix} actual={actual}")

try:
    import torch
    if not torch.cuda.is_available():
        err("CUDA_UNAVAILABLE")
    elif torch.cuda.get_device_properties(0).total_memory < 20 * 1024**3:
        err(f"GPU_MEMORY_TOO_SMALL bytes={torch.cuda.get_device_properties(0).total_memory}")
except Exception as exc:
    err(f"CUDA_CHECK_FAILED {exc}")

data_manifest = json.loads(Path(config["data"]["expected_hash_manifest"]).read_text(encoding="utf-8"))
for item in data_manifest["files"]:
    path = Path(item["path"])
    if not path.exists():
        err(f"MISSING_DATA_FILE {path}")
        continue
    actual_hash = sha256(path)
    if actual_hash != item["sha256"]:
        err(f"SHA256_MISMATCH {path} expected={item['sha256']} actual={actual_hash}")
    if item.get("records") is not None:
        records = sum(1 for _ in path.open("r", encoding="utf-8"))
        if records != item["records"]:
            err(f"ROW_COUNT_MISMATCH {path} expected={item['records']} actual={records}")

base_manifest = Path(config["base_model"]["manifest"])
base_sums = Path(config["base_model"]["sha256sums"])
if not base_manifest.exists():
    err(f"BASE_MODEL_MANIFEST_MISSING {base_manifest}")
if not base_sums.exists():
    err(f"BASE_MODEL_SHA256SUMS_MISSING {base_sums}")
if base_manifest.exists():
    payload = json.loads(base_manifest.read_text(encoding="utf-8"))
    if payload.get("source") != config["base_model"]["source"]:
        err("BASE_MODEL_SOURCE_MISMATCH")
    if not payload.get("upstream_revision"):
        err("BASE_MODEL_REVISION_MISSING")
    for item in payload.get("files", []):
        file_path = Path(payload["local_path"]) / item["path"]
        if not file_path.exists():
            err(f"BASE_MODEL_FILE_MISSING {file_path}")
        elif sha256(file_path) != item["sha256"]:
            err(f"BASE_MODEL_HASH_MISMATCH {file_path}")

backup = str(config.get("independent_backup_destination", ""))
if not backup or backup == "INDEPENDENT_BACKUP_DESTINATION_REQUIRED":
    err("INDEPENDENT_BACKUP_DESTINATION_NOT_CONFIGURED")

git_commit = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
git_status = subprocess.check_output(["git", "status", "--short"], text=True).strip()
if git_status:
    allowed_prefixes = ("?? recovery/seed42_96/", "?? recovery/seed42_96_replay_plan/")
    unexpected = [line for line in git_status.splitlines() if not line.startswith(allowed_prefixes)]
    if unexpected:
        err("UNEXPECTED_GIT_STATUS " + "; ".join(unexpected))

for stage in config["chain"]["stages"]:
    out = Path(config["output_root"]) / stage["run_name"]
    if out.exists() and any(out.iterdir()):
        err(f"OUTPUT_DIR_NOT_EMPTY {out}")
    resume = stage.get("resume_from_checkpoint")
    if resume and not Path(resume).parent.parent.exists():
        # The actual checkpoint is only expected after previous stages finish.
        pass

if errors:
    print("\n".join(errors))
    raise SystemExit(2)

print(json.dumps({"status": "N96_PREFLIGHT_OK", "git_commit": git_commit}, indent=2))
PY
