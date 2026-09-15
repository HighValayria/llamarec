#!/usr/bin/env bash
set -euo pipefail

# Creates a local backup bundle for an accepted N96 replay checkpoint. The
# destination must be configured in resolved_n96_replay_config.yaml and must be
# independent of the rented GPU machine.

ROOT=${ROOT:-$(pwd)}
cd "$ROOT"

CONFIG="recovery/seed42_96_replay_plan/n96_launch/resolved_n96_replay_config.yaml"
FINAL="recovery_runs/seed42_96/n/canonical_replay_seed42/canonical_replay_n_s12000_seed42"

python - "$CONFIG" "$FINAL" <<'PY'
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tarfile
import yaml

config = yaml.safe_load(Path(sys.argv[1]).read_text(encoding="utf-8"))
final = Path(sys.argv[2])
dest_raw = config.get("independent_backup_destination")
if not dest_raw or dest_raw == "INDEPENDENT_BACKUP_DESTINATION_REQUIRED":
    raise SystemExit("INDEPENDENT_BACKUP_DESTINATION_NOT_CONFIGURED")
dest = Path(dest_raw)
dest.mkdir(parents=True, exist_ok=True)
if not final.exists():
    raise SystemExit(f"missing final run directory: {final}")

bundle = dest / "n96_seed42_canonical_replay_bundle.tar.gz"
with tarfile.open(bundle, "w:gz") as tar:
    tar.add(final, arcname=final.as_posix())
    for extra in [
        "recovery/seed42_96_replay_plan/n96_launch/resolved_n96_replay_config.yaml",
        "recovery/seed42_96_replay_plan/n96_launch/BASE_MODEL_MANIFEST.json",
        "recovery/seed42_96_replay_plan/n96_launch/BASE_MODEL_SHA256SUMS.txt",
        "recovery/seed42_96_replay_plan/manifests/expected_data_hashes.json",
        "recovery/seed42_96_replay_plan/manifests/expected_historical_metrics.json",
    ]:
        path = Path(extra)
        if path.exists():
            tar.add(path, arcname=path.as_posix())

sha_path = dest / "SHA256SUMS.txt"
h = hashlib.sha256()
with bundle.open("rb") as handle:
    for chunk in iter(lambda: handle.read(1024 * 1024), b""):
        h.update(chunk)
sha = h.hexdigest()
sha_path.write_text(f"{sha}  {bundle.name}\n", encoding="utf-8")
print(json.dumps({"backup_bundle": str(bundle), "sha256": sha}, indent=2))
PY

