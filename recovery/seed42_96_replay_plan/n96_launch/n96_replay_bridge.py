"""Replay-only N96 training bridge.

This file is intentionally isolated under recovery artifacts. It does not
modify historical training entrypoints. It reuses the existing N dataset,
masking, model-loading, and collator code while making reproducibility-critical
TrainingArguments explicit for canonical replay.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import inspect
import json
from pathlib import Path
import subprocess
from typing import Any

import yaml

from src.data.preprocess import load_movies
from src.inference.prediction_io import write_json, write_yaml
from src.train.next_item_dataset import NextItemTrainingDataset
from src.train.preference_dataset import PreferenceDataCollator, summarize_encoded_examples
from src.train.train_n import _load_next_item_records
from src.train.train_y import (
    _load_tokenizer_and_model,
    _normalize_sample_limit,
    _set_training_seed,
    _trainable_parameter_summary,
    _use_chat_format,
    load_training_config,
)


def run_stage(config_path: Path, stage_name: str, launch_command: str) -> dict[str, Any]:
    replay = _read_yaml(config_path)
    stage = _resolve_stage(replay, stage_name)
    repo_root = Path.cwd()
    output_dir = repo_root / replay["output_root"] / stage["run_name"]
    output_dir.mkdir(parents=True, exist_ok=False)

    _configure_runtime(replay)
    seed = int(replay["training_arguments"]["seed"])
    _set_training_seed(seed)

    training_config = load_training_config(replay["base_training_config"])
    dataset_key = replay["dataset"]
    train_records = _load_next_item_records(
        config=training_config,
        dataset_key=dataset_key,
        split_name="train",
        limit=_normalize_sample_limit(int(replay["data"]["max_train_samples"])),
    )
    valid_records = _load_next_item_records(
        config=training_config,
        dataset_key=dataset_key,
        split_name="validation",
        limit=_normalize_sample_limit(int(replay["data"]["max_valid_samples"])),
    )
    if len(train_records) != int(replay["data"]["max_train_samples"]):
        raise RuntimeError(f"expected 200000 train records, got {len(train_records)}")

    _write_inputs(output_dir, replay, training_config, stage, train_records, valid_records, launch_command)

    movie_lookup = load_movies(dataset_key, training_config)
    tokenizer, model = _load_tokenizer_and_model(training_config)
    train_dataset = NextItemTrainingDataset(
        records=train_records,
        tokenizer=tokenizer,
        movie_lookup=movie_lookup,
        max_seq_length=int(training_config["model"]["max_seq_length"]),
        use_chat_format=_use_chat_format(training_config),
    )
    valid_dataset = NextItemTrainingDataset(
        records=valid_records,
        tokenizer=tokenizer,
        movie_lookup=movie_lookup,
        max_seq_length=int(training_config["model"]["max_seq_length"]),
        use_chat_format=_use_chat_format(training_config),
    )
    write_json(
        output_dir / "encoded_dataset_summary.json",
        {
            "train": summarize_encoded_examples(train_dataset.examples),
            "validation": summarize_encoded_examples(valid_dataset.examples),
        },
    )

    trainer = _build_explicit_trainer(
        replay=replay,
        stage=stage,
        model=model,
        tokenizer=tokenizer,
        train_dataset=train_dataset,
        valid_dataset=valid_dataset,
        output_dir=output_dir,
    )
    resume = stage.get("resume_from_checkpoint")
    if resume:
        resume_path = repo_root / resume
        _require_resume_checkpoint(resume_path)
        resume_arg = str(resume_path)
    else:
        resume_arg = None
    train_result = trainer.train(resume_from_checkpoint=resume_arg)
    trainer.save_model(str(output_dir / "adapter"))
    tokenizer.save_pretrained(str(output_dir / "adapter"))

    validation_metrics = {"skipped": True, "reason": "canonical_replay_eval_disabled_during_training"}
    metrics = {
        "model": "n_k0",
        "dataset": dataset_key,
        "output_dir": str(output_dir),
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "seed": seed,
        "train_samples": len(train_records),
        "validation_samples": len(valid_records),
        "stage": stage,
        "train": dict(train_result.metrics),
        "validation": validation_metrics,
        "trainable_parameters": _trainable_parameter_summary(model),
    }
    write_json(output_dir / "metrics.json", metrics)
    _write_runtime_manifest(output_dir, replay, stage, launch_command)
    return metrics


def _build_explicit_trainer(
    replay: dict[str, Any],
    stage: dict[str, Any],
    model: Any,
    tokenizer: Any,
    train_dataset: NextItemTrainingDataset,
    valid_dataset: NextItemTrainingDataset,
    output_dir: Path,
) -> Any:
    import torch
    from transformers import Trainer, TrainingArguments

    t = replay["training_arguments"]
    kwargs = {
        "output_dir": str(output_dir / "checkpoints"),
        "per_device_train_batch_size": int(t["per_device_train_batch_size"]),
        "per_device_eval_batch_size": int(t["per_device_eval_batch_size"]),
        "gradient_accumulation_steps": int(t["gradient_accumulation_steps"]),
        "learning_rate": float(t["learning_rate"]),
        "num_train_epochs": 1.0,
        "max_steps": int(stage["max_steps"]),
        "logging_steps": int(t["logging_steps"]),
        "save_steps": int(t["save_steps"]),
        "eval_steps": int(t["eval_steps"]),
        "save_strategy": str(t["save_strategy"]),
        "save_total_limit": int(t["save_total_limit"]),
        "report_to": str(t["report_to"]),
        "remove_unused_columns": bool(t["remove_unused_columns"]),
        "gradient_checkpointing": bool(t["gradient_checkpointing"]),
        "optim": str(t["optim"]),
        "adam_beta1": float(t["adam_beta1"]),
        "adam_beta2": float(t["adam_beta2"]),
        "adam_epsilon": float(t["adam_epsilon"]),
        "weight_decay": float(t["weight_decay"]),
        "max_grad_norm": float(t["max_grad_norm"]),
        "lr_scheduler_type": str(t["lr_scheduler_type"]),
        "warmup_steps": int(t["warmup_steps"]),
        "warmup_ratio": float(t["warmup_ratio"]),
        "bf16": bool(t["bf16"]),
        "fp16": bool(t["fp16"]),
        "seed": int(t["seed"]),
        "data_seed": int(t["data_seed"]),
        "dataloader_num_workers": int(t["dataloader_num_workers"]),
    }
    signature = inspect.signature(TrainingArguments.__init__)
    eval_value = str(t["eval_strategy"])
    if "eval_strategy" in signature.parameters:
        kwargs["eval_strategy"] = eval_value
    else:
        kwargs["evaluation_strategy"] = eval_value
    if "tf32" in signature.parameters:
        kwargs["tf32"] = bool(t["tf32"])

    effective = {key: _json_safe(value) for key, value in kwargs.items()}
    write_json(output_dir / "resolved_training_arguments.json", effective)
    args = TrainingArguments(**kwargs)
    return Trainer(
        model=model,
        args=args,
        train_dataset=train_dataset,
        eval_dataset=valid_dataset,
        data_collator=PreferenceDataCollator(tokenizer),
    )


def _configure_runtime(replay: dict[str, Any]) -> None:
    import torch

    policy = replay["runtime_policy"]
    torch.backends.cuda.matmul.allow_tf32 = bool(policy["torch_backends_cuda_matmul_allow_tf32"])
    torch.backends.cudnn.allow_tf32 = bool(policy["torch_backends_cudnn_allow_tf32"])
    torch.backends.cudnn.benchmark = bool(policy["torch_backends_cudnn_benchmark"])
    torch.use_deterministic_algorithms(bool(policy["torch_use_deterministic_algorithms"]))


def _write_inputs(
    output_dir: Path,
    replay: dict[str, Any],
    training_config: dict[str, Any],
    stage: dict[str, Any],
    train_records: list[dict[str, Any]],
    valid_records: list[dict[str, Any]],
    launch_command: str,
) -> None:
    snapshot = dict(training_config)
    snapshot.pop("_repo_root", None)
    write_yaml(output_dir / "config_snapshot.yaml", snapshot)
    write_yaml(output_dir / "resolved_replay_config.yaml", replay)
    write_json(
        output_dir / "run_summary.json",
        {
            "model": "n_k0",
            "dataset": replay["dataset"],
            "created_at_utc": datetime.now(timezone.utc).isoformat(),
            "label": replay["label"],
            "seed": int(replay["training_arguments"]["seed"]),
            "data_seed": int(replay["training_arguments"]["data_seed"]),
            "stage": stage,
            "max_train_samples": int(replay["data"]["max_train_samples"]),
            "max_valid_samples": int(replay["data"]["max_valid_samples"]),
            "train_records_loaded": len(train_records),
            "valid_records_loaded": len(valid_records),
            "output_dir": str(output_dir),
            "launch_command": launch_command,
            "git_commit": _git(["rev-parse", "HEAD"]),
        },
    )
    (output_dir / "launch_command.txt").write_text(launch_command + "\n", encoding="utf-8")


def _write_runtime_manifest(output_dir: Path, replay: dict[str, Any], stage: dict[str, Any], launch_command: str) -> None:
    manifest = {
        "schema": "n96_replay_runtime_manifest_v1",
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "label": replay["label"],
        "stage": stage,
        "git_commit": _git(["rev-parse", "HEAD"]),
        "git_status_short": _git(["status", "--short"]),
        "launch_command": launch_command,
        "training_arguments": replay["training_arguments"],
        "runtime_policy": replay["runtime_policy"],
        "base_model_manifest": replay["base_model"]["manifest"],
        "data_hash_manifest": replay["data"]["expected_hash_manifest"],
    }
    write_json(output_dir / "run_manifest.json", manifest)


def _require_resume_checkpoint(path: Path) -> None:
    required = ["trainer_state.json", "optimizer.pt", "scheduler.pt", "rng_state.pth"]
    missing = [name for name in required if not (path / name).exists()]
    if missing:
        raise FileNotFoundError(f"resume checkpoint missing {missing}: {path}")


def _resolve_stage(replay: dict[str, Any], stage_name: str) -> dict[str, Any]:
    for stage in replay["chain"]["stages"]:
        if stage["name"] == stage_name:
            return dict(stage)
    raise KeyError(f"unknown stage {stage_name!r}")


def _read_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def _git(args: list[str]) -> str:
    return subprocess.check_output(["git", *args], text=True, encoding="utf-8").strip()


def _json_safe(value: Any) -> Any:
    try:
        json.dumps(value)
        return value
    except TypeError:
        return str(value)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run one N96 canonical replay training stage")
    parser.add_argument("--config", default="recovery/seed42_96_replay_plan/n96_launch/resolved_n96_replay_config.yaml")
    parser.add_argument("--stage", required=True, choices=["n_s3000", "n_s6000", "n_s12000"])
    parser.add_argument("--launch-command", required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = run_stage(Path(args.config), args.stage, args.launch_command)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
