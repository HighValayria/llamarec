"""STEP 6：N-K0 Full-sequence Next-item Tuning 训练入口。"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any

from src.data.config import resolve_configured_output_path, resolve_repo_path_from_config
from src.data.preprocess import load_movies
from src.inference.prediction_io import read_jsonl, write_json, write_yaml
from src.inference.prompts import render_candidate_prompt
from src.inference.scoring import build_adapter_scorer
from src.train.next_item_dataset import NextItemTrainingDataset
from src.train.preference_dataset import summarize_encoded_examples
from src.train.train_y import (
    _build_trainer,
    _load_tokenizer_and_model,
    _normalize_sample_limit,
    _release_cuda_cache,
    _resolve_training_seed,
    _set_training_seed,
    _trainable_parameter_summary,
    _use_chat_format,
    load_training_config,
)


def run_n_training(args: argparse.Namespace) -> dict[str, Any]:
    """运行 N-K0 训练。"""

    config = load_training_config(args.config)
    dataset_key = args.dataset or config["dataset"]["formal"]
    resolved_seed = _resolve_training_seed(args, config)
    if getattr(args, "reload_only", False):
        return _run_reload_only(args=args, config=config, dataset_key=dataset_key)
    _set_training_seed(resolved_seed)

    output_dir = _resolve_output_dir(config, dataset_key, args)
    output_dir.mkdir(parents=True, exist_ok=True)

    train_records = _load_next_item_records(
        config=config,
        dataset_key=dataset_key,
        split_name="train",
        limit=_normalize_sample_limit(args.max_train_samples),
    )
    valid_records = _load_next_item_records(
        config=config,
        dataset_key=dataset_key,
        split_name="validation",
        limit=_normalize_sample_limit(args.max_valid_samples),
    )
    if not train_records:
        raise ValueError("N 训练记录为空，不能启动训练。")
    if not valid_records:
        raise ValueError("N validation 记录为空，不能启动训练。")

    _write_run_inputs(
        output_dir=output_dir,
        config=config,
        args=args,
        dataset_key=dataset_key,
        train_records=train_records,
        valid_records=valid_records,
    )

    movie_lookup = load_movies(dataset_key, config)
    tokenizer, model = _load_tokenizer_and_model(config)
    train_dataset = NextItemTrainingDataset(
        records=train_records,
        tokenizer=tokenizer,
        movie_lookup=movie_lookup,
        max_seq_length=int(config["model"]["max_seq_length"]),
        use_chat_format=_use_chat_format(config),
    )
    valid_dataset = NextItemTrainingDataset(
        records=valid_records,
        tokenizer=tokenizer,
        movie_lookup=movie_lookup,
        max_seq_length=int(config["model"]["max_seq_length"]),
        use_chat_format=_use_chat_format(config),
    )
    write_json(
        output_dir / "encoded_dataset_summary.json",
        {
            "train": summarize_encoded_examples(train_dataset.examples),
            "validation": summarize_encoded_examples(valid_dataset.examples),
        },
    )

    trainer = _build_trainer(
        args=args,
        config=config,
        model=model,
        tokenizer=tokenizer,
        train_dataset=train_dataset,
        valid_dataset=valid_dataset,
        output_dir=output_dir,
    )

    train_result = trainer.train(
        resume_from_checkpoint=args.resume_from_checkpoint or None
    )
    trainer.save_model(str(output_dir / "adapter"))
    tokenizer.save_pretrained(str(output_dir / "adapter"))

    validation_metrics = trainer.evaluate()
    metrics = {
        "model": "n_k0",
        "dataset": dataset_key,
        "output_dir": str(output_dir),
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "seed": resolved_seed,
        "train_samples": len(train_records),
        "validation_samples": len(valid_records),
        "train": dict(train_result.metrics),
        "validation": validation_metrics,
        "trainable_parameters": _trainable_parameter_summary(model),
    }
    write_json(output_dir / "metrics.json", metrics)

    if args.run_reload_check:
        trainer = None
        model = None
        _release_cuda_cache()
        reload_report = _run_reload_candidate_check(
            config=config,
            adapter_dir=output_dir / "adapter",
            sample=valid_records[0],
            movie_lookup=movie_lookup,
        )
        write_json(output_dir / "reload_check.json", reload_report)

    return metrics


def _run_reload_only(
    args: argparse.Namespace,
    config: dict[str, Any],
    dataset_key: str,
) -> dict[str, Any]:
    adapter_dir = _resolve_adapter_dir(config, dataset_key, args)
    if not adapter_dir.exists():
        raise FileNotFoundError(f"adapter 目录不存在：{adapter_dir}")

    valid_records = _load_next_item_records(
        config=config,
        dataset_key=dataset_key,
        split_name=args.reload_split,
        limit=1,
    )
    if not valid_records:
        raise ValueError(f"N {args.reload_split} 记录为空，不能执行重载检查。")

    movie_lookup = load_movies(dataset_key, config)
    reload_report = _run_reload_candidate_check(
        config=config,
        adapter_dir=adapter_dir,
        sample=valid_records[0],
        movie_lookup=movie_lookup,
    )
    output_dir = adapter_dir.parent if adapter_dir.name == "adapter" else adapter_dir
    write_json(output_dir / "reload_check.json", reload_report)
    return {
        "model": "n_k0",
        "dataset": dataset_key,
        "mode": "reload_only",
        "split": args.reload_split,
        "adapter_dir": str(adapter_dir),
        "reload_check": reload_report,
    }


def _load_next_item_records(
    config: dict[str, Any],
    dataset_key: str,
    split_name: str,
    limit: int | None,
) -> list[dict[str, Any]]:
    path = resolve_configured_output_path(
        config,
        dataset_key,
        "next_item_samples",
        split_name,
    )
    if not path.exists():
        raise FileNotFoundError(f"N {split_name} 数据不存在: {path}。")
    return read_jsonl(path, limit=limit)


def _run_reload_candidate_check(
    config: dict[str, Any],
    adapter_dir: Path,
    sample: dict[str, Any],
    movie_lookup: dict[str, dict[str, str]],
) -> dict[str, Any]:
    scorer = build_adapter_scorer("real", config=config, adapter_dir=adapter_dir)
    prompt = render_candidate_prompt(sample, movie_lookup)
    label_set = list(sample.get("label_set", ["A", "B", "C", "D", "E"]))
    score = scorer.score_candidates(prompt, label_set)
    return {
        "adapter_dir": str(adapter_dir),
        "sample_user_id": sample["user_id"],
        "label": sample["label"],
        "label_probabilities": score["label_probabilities"],
        "predicted_label": score["predicted_label"],
        "checked": True,
    }


def _write_run_inputs(
    output_dir: Path,
    config: dict[str, Any],
    args: argparse.Namespace,
    dataset_key: str,
    train_records: list[dict[str, Any]],
    valid_records: list[dict[str, Any]],
) -> None:
    snapshot = dict(config)
    snapshot.pop("_repo_root", None)
    write_yaml(output_dir / "config_snapshot.yaml", snapshot)
    write_json(
        output_dir / "run_summary.json",
        {
            "model": "n_k0",
            "dataset": dataset_key,
            "created_at_utc": datetime.now(timezone.utc).isoformat(),
            "seed": _resolve_training_seed(args, config),
            "max_train_samples": args.max_train_samples,
            "max_valid_samples": args.max_valid_samples,
            "train_records_loaded": len(train_records),
            "valid_records_loaded": len(valid_records),
            "output_dir": str(output_dir),
            "smoke": args.smoke,
        },
    )


def _resolve_output_dir(
    config: dict[str, Any],
    dataset_key: str,
    args: argparse.Namespace,
) -> Path:
    if args.output_dir:
        output_dir = Path(args.output_dir)
        if not output_dir.is_absolute():
            output_dir = Path(config["_repo_root"]) / output_dir
    else:
        raw_path = config.get("outputs", {}).get("n", "outputs/n/{dataset}")
        output_dir = resolve_repo_path_from_config(config, raw_path, dataset_key=dataset_key)
    if args.run_name:
        output_dir = output_dir / args.run_name
    return output_dir


def _resolve_adapter_dir(
    config: dict[str, Any],
    dataset_key: str,
    args: argparse.Namespace,
) -> Path:
    raw_adapter_dir = getattr(args, "adapter_dir", None)
    if raw_adapter_dir:
        adapter_dir = Path(raw_adapter_dir)
        if not adapter_dir.is_absolute():
            adapter_dir = Path(config["_repo_root"]) / adapter_dir
        return adapter_dir
    return _resolve_output_dir(config, dataset_key, args) / "adapter"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="训练 N-K0 Full-sequence Next-item Tuning")
    parser.add_argument("--config", default="configs/n.yaml", help="N-K0 配置路径")
    parser.add_argument("--dataset", default=None, help="数据集 key，默认使用 dataset.formal")
    parser.add_argument("--output-dir", default=None, help="覆盖输出目录")
    parser.add_argument("--run-name", default=None, help="追加到输出目录下的运行名")
    parser.add_argument("--seed", type=int, default=None, help="训练随机种子；默认读取配置 seed.random_seed")
    parser.add_argument("--smoke", action="store_true", help="标记本次为 smoke/overfit 运行")
    parser.add_argument("--max-train-samples", type=int, default=1000, help="最多读取训练样本数；负数表示全量")
    parser.add_argument("--max-valid-samples", type=int, default=1000, help="最多读取验证样本数；负数表示全量")
    parser.add_argument("--per-device-train-batch-size", type=int, default=1)
    parser.add_argument("--per-device-eval-batch-size", type=int, default=1)
    parser.add_argument("--gradient-accumulation-steps", type=int, default=8)
    parser.add_argument("--learning-rate", type=float, default=2e-4)
    parser.add_argument("--num-train-epochs", type=float, default=1.0)
    parser.add_argument("--max-steps", type=int, default=-1)
    parser.add_argument("--logging-steps", type=int, default=10)
    parser.add_argument("--eval-steps", type=int, default=50)
    parser.add_argument("--save-steps", type=int, default=50)
    parser.add_argument("--bf16", action="store_true", help="启用 bf16 训练")
    parser.add_argument("--fp16", action="store_true", help="启用 fp16 训练")
    parser.add_argument("--resume-from-checkpoint", default=None)
    parser.add_argument("--run-reload-check", action="store_true", help="训练后重载 adapter 并输出 P(A-E)")
    parser.add_argument("--reload-only", action="store_true", help="不训练，只重载已有 adapter 并输出 P(A-E)")
    parser.add_argument("--adapter-dir", default=None, help="reload-only 使用的 adapter 目录")
    parser.add_argument("--reload-split", default="validation", choices=["validation", "test"], help="reload-only 取样 split")
    return parser.parse_args()


def main() -> None:
    summary = run_n_training(parse_args())
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
