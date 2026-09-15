#!/usr/bin/env bash
set -euo pipefail

# Verifies immutable data/candidate assets. Does not train or run inference.

ROOT=${ROOT:-$(pwd)}
cd "$ROOT"

python - <<'PY'
import hashlib
import json
from pathlib import Path

manifest = Path("recovery/seed42_96_replay_plan/manifests/expected_data_hashes.json")
payload = json.loads(manifest.read_text(encoding="utf-8"))
errors = []

for item in payload["files"]:
    path = Path(item["path"])
    if not path.exists():
        errors.append(f"MISSING {path}")
        continue
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    actual_hash = h.hexdigest()
    if actual_hash != item["sha256"]:
        errors.append(f"SHA256_MISMATCH {path} expected={item['sha256']} actual={actual_hash}")
    expected_records = item.get("records")
    if expected_records is not None:
        with path.open("r", encoding="utf-8") as handle:
            actual_records = sum(1 for _ in handle)
        if actual_records != expected_records:
            errors.append(f"RECORD_COUNT_MISMATCH {path} expected={expected_records} actual={actual_records}")

required_configs = [
    "recovery/seed42_96_replay_plan/configs/n96_replay.yaml",
    "recovery/seed42_96_replay_plan/configs/y96_replay.yaml",
    "recovery/seed42_96_replay_plan/configs/m1_96_replay.yaml",
]
for name in required_configs:
    if not Path(name).exists():
        errors.append(f"MISSING_CONFIG {name}")

for forbidden in ["outputs", "paper/evidence", "paper/tables", "revision_202609", "recovery/provenance"]:
    if str(Path("recovery_runs/seed42_96")).startswith(forbidden):
        errors.append(f"FORBIDDEN_OUTPUT_ROOT {forbidden}")

if errors:
    print("\n".join(errors))
    raise SystemExit(2)

print("SEED42_96_REPLAY_PREFLIGHT_OK")
PY
