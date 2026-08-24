#!/usr/bin/env bash
set -euo pipefail

ROOT=${ROOT:-/root/llamarec}
cd "$ROOT"

export HF_HUB_OFFLINE=${HF_HUB_OFFLINE:-1}
export TRANSFORMERS_OFFLINE=${TRANSFORMERS_OFFLINE:-1}
export HF_HUB_DISABLE_TELEMETRY=${HF_HUB_DISABLE_TELEMETRY:-1}

python - <<'PY'
import json
import os
import platform
import sys
from pathlib import Path

MODEL_ID = os.environ.get("LLAMAREC_BASE_MODEL", "meta-llama/Llama-3.2-3B-Instruct")

print("== runtime ==")
print(f"python={sys.executable}")
print(f"platform={platform.platform()}")
print(f"cwd={Path.cwd()}")
print(f"home={Path.home()}")
print(f"user={os.environ.get('USER') or os.environ.get('USERNAME')}")
print(f"model_id={MODEL_ID}")

print("\n== env ==")
for key in [
    "HF_HOME",
    "HF_HUB_CACHE",
    "TRANSFORMERS_CACHE",
    "XDG_CACHE_HOME",
    "HF_HUB_OFFLINE",
    "TRANSFORMERS_OFFLINE",
    "HF_TOKEN",
]:
    value = os.environ.get(key)
    if key == "HF_TOKEN" and value:
        value = "<set>"
    print(f"{key}={value or '<unset>'}")

print("\n== packages ==")
try:
    import transformers
    print(f"transformers={transformers.__version__}")
except Exception as exc:
    print(f"transformers_import_error={exc!r}")
    raise
try:
    import huggingface_hub
    print(f"huggingface_hub={huggingface_hub.__version__}")
except Exception as exc:
    print(f"huggingface_hub_import_error={exc!r}")
try:
    import torch
    print(f"torch={torch.__version__}")
    print(f"cuda_available={torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"cuda_device={torch.cuda.get_device_name(0)}")
except Exception as exc:
    print(f"torch_import_error={exc!r}")

cache_candidates = []
if os.environ.get("HF_HUB_CACHE"):
    cache_candidates.append(Path(os.environ["HF_HUB_CACHE"]))
if os.environ.get("HF_HOME"):
    cache_candidates.append(Path(os.environ["HF_HOME"]) / "hub")
if os.environ.get("TRANSFORMERS_CACHE"):
    cache_candidates.append(Path(os.environ["TRANSFORMERS_CACHE"]))
if os.environ.get("XDG_CACHE_HOME"):
    cache_candidates.append(Path(os.environ["XDG_CACHE_HOME"]) / "huggingface" / "hub")
cache_candidates.append(Path.home() / ".cache" / "huggingface" / "hub")
cache_candidates.append(Path("/root/.cache/huggingface/hub"))

seen = set()
cache_candidates = [p for p in cache_candidates if not (str(p) in seen or seen.add(str(p)))]
print("\n== cache dirs ==")
for path in cache_candidates:
    print(f"{path} exists={path.exists()}")

print("\n== huggingface cache scan ==")
try:
    from huggingface_hub import scan_cache_dir
    found = False
    for cache_dir in cache_candidates:
        if not cache_dir.exists():
            continue
        try:
            info = scan_cache_dir(cache_dir)
        except Exception as exc:
            print(f"scan_failed cache={cache_dir}: {exc!r}")
            continue
        for repo in info.repos:
            if repo.repo_id == MODEL_ID:
                found = True
                print(f"repo_found cache={cache_dir} repo={repo.repo_id} size_on_disk={repo.size_on_disk} nb_files={repo.nb_files}")
                for rev in sorted(repo.revisions, key=lambda item: item.commit_hash):
                    print(f"  revision={rev.commit_hash} refs={sorted(rev.refs)} files={rev.nb_files} size={rev.size_on_disk}")
    if not found:
        print("repo_found=false")
except Exception as exc:
    print(f"scan_cache_dir_unavailable={exc!r}")

print("\n== local-only transformers resolution ==")
from transformers import AutoConfig, AutoTokenizer
try:
    from transformers.utils import cached_file
except Exception:
    from transformers.utils.hub import cached_file

config = AutoConfig.from_pretrained(MODEL_ID, local_files_only=True)
print(f"config_ok model_type={getattr(config, 'model_type', None)}")

tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, use_fast=True, local_files_only=True)
print(f"tokenizer_ok class={tokenizer.__class__.__name__} vocab_size={getattr(tokenizer, 'vocab_size', '<unknown>')}")

resolved = {}
for filename in [
    "model.safetensors.index.json",
    "pytorch_model.bin.index.json",
    "model.safetensors",
    "pytorch_model.bin",
    "tokenizer.json",
    "tokenizer.model",
    "config.json",
]:
    try:
        path = cached_file(MODEL_ID, filename, local_files_only=True)
        resolved[filename] = path
        print(f"cached_file_ok {filename} -> {path}")
    except Exception as exc:
        print(f"cached_file_missing {filename}: {exc.__class__.__name__}: {exc}")

index_path = resolved.get("model.safetensors.index.json") or resolved.get("pytorch_model.bin.index.json")
if index_path:
    index_file = Path(index_path)
    payload = json.loads(index_file.read_text(encoding="utf-8"))
    shard_names = sorted(set(payload.get("weight_map", {}).values()))
    missing = [name for name in shard_names if not (index_file.parent / name).exists()]
    print(f"weight_index_ok index={index_file.name} shards={len(shard_names)} missing_shards={len(missing)}")
    if missing:
        print("missing_shards_list=" + json.dumps(missing[:20], ensure_ascii=False))
        raise SystemExit(3)
elif not (resolved.get("model.safetensors") or resolved.get("pytorch_model.bin")):
    print("weight_files_not_confirmed=true")
    raise SystemExit(4)
else:
    print("single_weight_file_ok=true")

print("\npreflight_ok=true")
PY
