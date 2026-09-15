#!/usr/bin/env bash
set -euo pipefail

# Hash-freezes an already-downloaded official base model. This script does not
# download anything.

ROOT=${ROOT:-$(pwd)}
cd "$ROOT"

MODEL_DIR=${BASE_MODEL_DIR:-models/Llama-3.2-3B-Instruct}
REVISION=${BASE_MODEL_REVISION:-}
OUT_DIR="recovery/seed42_96_replay_plan/n96_launch"
MANIFEST="$OUT_DIR/BASE_MODEL_MANIFEST.json"
SUMS="$OUT_DIR/BASE_MODEL_SHA256SUMS.txt"

if [[ -z "$REVISION" ]]; then
  echo "BASE_MODEL_REVISION must be set to the exact upstream revision/commit." >&2
  exit 2
fi
if [[ ! -d "$MODEL_DIR" ]]; then
  echo "Missing base model directory: $MODEL_DIR" >&2
  exit 2
fi

python - "$MODEL_DIR" "$REVISION" "$MANIFEST" "$SUMS" <<'PY'
import hashlib
import json
from pathlib import Path
import sys

model_dir = Path(sys.argv[1])
revision = sys.argv[2]
manifest_path = Path(sys.argv[3])
sums_path = Path(sys.argv[4])

critical_names = {
    "config.json",
    "generation_config.json",
    "tokenizer.json",
    "tokenizer_config.json",
    "special_tokens_map.json",
    "chat_template.jinja",
    "model.safetensors.index.json",
}
critical_suffixes = {".safetensors"}
files = []
for path in sorted(p for p in model_dir.rglob("*") if p.is_file()):
    rel = path.relative_to(model_dir).as_posix()
    if path.name in critical_names or path.suffix in critical_suffixes:
        h = hashlib.sha256(path.read_bytes()).hexdigest()
        files.append({"path": rel, "bytes": path.stat().st_size, "sha256": h})

config_path = model_dir / "config.json"
if not config_path.exists():
    raise SystemExit("config.json is required")
config = json.loads(config_path.read_text(encoding="utf-8"))
identity_ok = "llama" in str(config.get("model_type", "")).lower()
if not identity_ok:
    raise SystemExit(f"unexpected model_type: {config.get('model_type')!r}")

tokenizer_config = {}
tc_path = model_dir / "tokenizer_config.json"
if tc_path.exists():
    tokenizer_config = json.loads(tc_path.read_text(encoding="utf-8"))

manifest = {
    "schema": "base_model_manifest_v1",
    "source": "meta-llama/Llama-3.2-3B-Instruct",
    "local_path": model_dir.as_posix(),
    "upstream_revision": revision,
    "identity_check": {
        "model_type": config.get("model_type"),
        "architectures": config.get("architectures"),
        "passed": identity_ok,
    },
    "tokenizer": {
        "tokenizer_class": tokenizer_config.get("tokenizer_class"),
        "padding_side": tokenizer_config.get("padding_side"),
        "chat_template_sha256": next((f["sha256"] for f in files if f["path"] == "chat_template.jinja"), None),
    },
    "files": files,
}
manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
sums_path.write_text("".join(f"{f['sha256']}  {model_dir.as_posix()}/{f['path']}\n" for f in files), encoding="utf-8")
print(f"BASE_MODEL_FREEZE_OK files={len(files)}")
PY
