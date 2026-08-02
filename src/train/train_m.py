"""STEP 7：M-K0 Y + N Multi-task Tuning 训练入口。"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import inspect
import json
from pathlib import Path
from typing import Any

from src.data.config import resolve_repo_path_from_config
from src.data.preprocess import load_movies
from src.inference.prediction_io import write_json, write_yaml
from src.inference.prompts import render_candidate_prompt, render_yesno_prompt
from src.inference.scoring import build_adapter_scorer
from src.train.multitask_dataset import (
    MultitaskTrainingDataset,
    count_ratio_examples,
    summarize_multitask_examples,
)
from src.train.next_item_dataset import NextItemTrainingDataset
from src.train.preference_dataset import (
    PreferenceDataCollator,
    PreferenceTrainingDataset,
    summarize_encoded_examples,
)
from src.train.train_n import _load_next_item_records
from src.train.train_y import (
    _load_preference_records,
    _load_tokenizer_and_model,
    _normalize_sample_limit,
    _release_cuda_cache,
    _trainable_parameter_summary,
    _use_chat_format,
    load_training_config,
)


def run_m_training(args: argparse.Namespace) -> dict[str, Any]:
    """运行 M-K0 多任务训练。"""

    config = load_training_config(args.config)
    dataset_key = args.dataset or config["dataset"]["formal"]
    if getattr(args, "reload_only", False):
        return _run_reload_only(args=args, config=config, dataset_key=dataset_key)
    task_ratio = _resolve_task_ratio(args, config)

    output_dir = _resolve_output_dir(config, dataset_key, args)
    output_dir.mkdir(parents=True, exist_ok=True)

    y_train_records = _load_preference_records(
        config=config,
        dataset_key=dataset_key,
        split_name="train",
        limit=_normalize_sample_limit(args.max_y_train_samples),
    )
    n_train_records = _load_next_item_records(
        config=config,
        dataset_key=dataset_key,
        split_name="train",
        limit=_normalize_sample_limit(args.max_n_train_samples),
    )
    y_valid_records = _load_preference_records(
        config=config,
        dataset_key=dataset_key,
        split_name="validation",
        limit=_normalize_sample_limit(args.max_y_valid_samples),
    )
    n_valid_records = _load_next_item_records(
        config=config,
        dataset_key=dataset_key,
        split_name="validation",
        limit=_normalize_sample_limit(args.max_n_valid_samples),
    )

    _validate_multitask_inputs(y_train_records, n_train_records, y_valid_records, n_valid_records)
    _write_run_inputs(
        output_dir=output_dir,
        config=config,
        args=args,
        dataset_key=dataset_key,
        y_train_records=y_train_records,
        n_train_records=n_train_records,
        y_valid_records=y_valid_records,
        n_valid_records=n_valid_records,
        task_ratio=task_ratio,
    )

    movie_lookup = load_movies(dataset_key, config)
    tokenizer, model = _load_tokenizer_and_model(config)
    train_dataset = MultitaskTrainingDataset(
        preference_records=y_train_records,
        next_item_records=n_train_records,
        tokenizer=tokenizer,
        movie_lookup=movie_lookup,
        max_seq_length=int(config["model"]["max_seq_length"]),
        use_chat_format=_use_chat_format(config),
        task_ratio_y=task_ratio["y"],
        task_ratio_n=task_ratio["n"],
    )
    valid_dataset = MultitaskTrainingDataset(
        preference_records=y_valid_records,
        next_item_records=n_valid_records,
        tokenizer=tokenizer,
        movie_lookup=movie_lookup,
        max_seq_length=int(config["model"]["max_seq_length"]),
        use_chat_format=_use_chat_format(config),
        task_ratio_y=task_ratio["y"],
        task_ratio_n=task_ratio["n"],
    )
    y_valid_dataset = PreferenceTrainingDataset(
        records=y_valid_records,
        tokenizer=tokenizer,
        max_seq_length=int(config["model"]["max_seq_length"]),
        use_chat_format=_use_chat_format(config),
    )
    n_valid_dataset = NextItemTrainingDataset(
        records=n_valid_records,
        tokenizer=tokenizer,
        movie_lookup=movie_lookup,
        max_seq_length=int(config["model"]["max_seq_length"]),
        use_chat_format=_use_chat_format(config),
    )
    write_json(
        output_dir / "encoded_dataset_summary.json",
        {
            "train": summarize_multitask_examples(train_dataset.examples),
            "validation": summarize_multitask_examples(valid_dataset.examples),
            "validation_y": summarize_encoded_examples(y_valid_dataset.examples),
            "validation_n": summarize_encoded_examples(n_valid_dataset.examples),
            "task_ratio": task_ratio,
        },
    )

    trainer = _build_sequential_trainer(
        args=args,
        config=config,
        model=model,
        tokenizer=tokenizer,
        train_dataset=train_dataset,
        valid_dataset=valid_dataset,
        y_valid_dataset=y_valid_dataset,
        n_valid_dataset=n_valid_dataset,
        output_dir=output_dir,
    )
    train_result = trainer.train(
        resume_from_checkpoint=args.resume_from_checkpoint or None
    )
    trainer.save_model(str(output_dir / "adapter"))
    tokenizer.save_pretrained(str(output_dir / "adapter"))

    validation_metrics = trainer.evaluate()
    metrics = {
        "model": "m_k0",
        "dataset": dataset_key,
        "output_dir": str(output_dir),
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "train_samples": len(train_dataset),
        "validation_samples": len(valid_dataset),
        "train_task_counts": train_dataset.task_counts,
        "validation_task_counts": valid_dataset.task_counts,
        "task_ratio": task_ratio,
        "train": dict(train_result.metrics),
        "validation": validation_metrics,
        "trainable_parameters": _trainable_parameter_summary(model),
    }
    write_json(output_dir / "metrics.json", metrics)

    if args.run_reload_check:
        trainer = None
        model = None
        _release_cuda_cache()
        reload_report = _run_reload_multitask_check(
            config=config,
            adapter_dir=output_dir / "adapter",
            y_sample=y_valid_records[0],
            n_sample=n_valid_records[0],
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

    y_records = _load_preference_records(
        config=config,
        dataset_key=dataset_key,
        split_name=args.reload_split,
        limit=1,
    )
    n_records = _load_next_item_records(
        config=config,
        dataset_key=dataset_key,
        split_name=args.reload_split,
        limit=1,
    )
    _validate_multitask_inputs(y_records, n_records, y_records, n_records)
    movie_lookup = load_movies(dataset_key, config)
    reload_report = _run_reload_multitask_check(
        config=config,
        adapter_dir=adapter_dir,
        y_sample=y_records[0],
        n_sample=n_records[0],
        movie_lookup=movie_lookup,
    )
    output_dir = adapter_dir.parent if adapter_dir.name == "adapter" else adapter_dir
    write_json(output_dir / "reload_check.json", reload_report)
    return {
        "model": "m_k0",
        "dataset": dataset_key,
        "mode": "reload_only",
        "split": args.reload_split,
        "adapter_dir": str(adapter_dir),
        "reload_check": reload_report,
    }


def _validate_multitask_inputs(
    y_train_records: list[dict[str, Any]],
    n_train_records: list[dict[str, Any]],
    y_valid_records: list[dict[str, Any]],
    n_valid_records: list[dict[str, Any]],
) -> None:
    if not y_train_records or not n_train_records:
        raise ValueError("M 训练需要同时存在 Y train 与 N train。")
    if not y_valid_records or not n_valid_records:
        raise ValueError("M validation 需要同时存在 Y validation 与 N validation。")


def _resolve_task_ratio(args: argparse.Namespace, config: dict[str, Any]) -> dict[str, int]:
    """从 CLI 或配置读取 M 的 Y/N 采样比例。"""

    ratio_config = config.get("optimizer_step_ratio") or {}
    if not ratio_config:
        ratio_config = config.get("tasks", {}).get("m", {}).get("optimizer_step_ratio", {})
    y_ratio = args.task_ratio_y if args.task_ratio_y is not None else ratio_config.get("y", 1)
    n_ratio = args.task_ratio_n if args.task_ratio_n is not None else ratio_config.get("n", 1)
    try:
        y_ratio = int(y_ratio)
        n_ratio = int(n_ratio)
    except (TypeError, ValueError) as exc:
        raise ValueError("M 任务采样比例必须是正整数。") from exc
    if y_ratio <= 0 or n_ratio <= 0:
        raise ValueError("M 任务采样比例必须是正整数。")
    return {"y": y_ratio, "n": n_ratio}


def _build_sequential_trainer(
    args: argparse.Namespace,
    config: dict[str, Any],
    model: Any,
    tokenizer: Any,
    train_dataset: MultitaskTrainingDataset,
    valid_dataset: MultitaskTrainingDataset,
    y_valid_dataset: PreferenceTrainingDataset,
    n_valid_dataset: NextItemTrainingDataset,
    output_dir: Path,
):
    from torch.utils.data import SequentialSampler
    from transformers import Trainer, TrainingArguments

    class SequentialTrainer(Trainer):
        def _get_train_sampler(self, train_dataset=None):
            return SequentialSampler(
                _select_train_sampler_dataset(train_dataset, self.train_dataset)
            )

        def evaluate(
            self,
            eval_dataset=None,
            ignore_keys=None,
            metric_key_prefix: str = "eval",
        ):
            metrics = super().evaluate(
                eval_dataset=eval_dataset,
                ignore_keys=ignore_keys,
                metric_key_prefix=metric_key_prefix,
            )
            if not _should_run_per_task_validation(eval_dataset, metric_key_prefix):
                return metrics

            y_metrics = super().evaluate(
                eval_dataset=self.y_valid_dataset,
                ignore_keys=ignore_keys,
                metric_key_prefix="eval_y",
            )
            n_metrics = super().evaluate(
                eval_dataset=self.n_valid_dataset,
                ignore_keys=ignore_keys,
                metric_key_prefix="eval_n",
            )
            metrics.update(y_metrics)
            metrics.update(n_metrics)
            return metrics

    training_kwargs = {
        "output_dir": str(output_dir / "checkpoints"),
        "per_device_train_batch_size": args.per_device_train_batch_size,
        "per_device_eval_batch_size": args.per_device_eval_batch_size,
        "gradient_accumulation_steps": args.gradient_accumulation_steps,
        "learning_rate": args.learning_rate,
        "num_train_epochs": args.num_train_epochs,
        "max_steps": args.max_steps,
        "logging_steps": args.logging_steps,
        "save_steps": args.save_steps,
        "eval_steps": args.eval_steps,
        "save_strategy": "steps",
        "save_total_limit": int(config["training"]["checkpointing"]["save_total_limit"]),
        "report_to": "none",
        "remove_unused_columns": False,
        "gradient_checkpointing": bool(config["lora"].get("gradient_checkpointing", True)),
    }
    signature = inspect.signature(TrainingArguments.__init__)
    if "eval_strategy" in signature.parameters:
        training_kwargs["eval_strategy"] = "steps"
    else:
        training_kwargs["evaluation_strategy"] = "steps"
    if "bf16" in signature.parameters:
        training_kwargs["bf16"] = args.bf16
    if "fp16" in signature.parameters:
        training_kwargs["fp16"] = args.fp16

    training_args = TrainingArguments(**training_kwargs)
    trainer = SequentialTrainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=valid_dataset,
        data_collator=PreferenceDataCollator(tokenizer),
    )
    trainer.y_valid_dataset = y_valid_dataset
    trainer.n_valid_dataset = n_valid_dataset
    return trainer


def _select_train_sampler_dataset(passed_dataset: Any, fallback_dataset: Any) -> Any:
    """兼容不同 transformers 版本的 train sampler 参数。"""

    return passed_dataset if passed_dataset is not None else fallback_dataset


def _should_run_per_task_validation(eval_dataset: Any, metric_key_prefix: str) -> bool:
    """只在默认 mixed validation 时追加 Y-only/N-only validation。"""

    return eval_dataset is None and metric_key_prefix == "eval"


def _run_reload_multitask_check(
    config: dict[str, Any],
    adapter_dir: Path,
    y_sample: dict[str, Any],
    n_sample: dict[str, Any],
    movie_lookup: dict[str, dict[str, str]],
) -> dict[str, Any]:
    scorer = build_adapter_scorer("real", config=config, adapter_dir=adapter_dir)
    y_score = scorer.score_yesno(render_yesno_prompt(y_sample))
    n_score = scorer.score_candidates(
        render_candidate_prompt(n_sample, movie_lookup),
        list(n_sample.get("label_set", ["A", "B", "C", "D", "E"])),
    )
    return {
        "adapter_dir": str(adapter_dir),
        "y": {
            "sample_user_id": y_sample["user_id"],
            "label": y_sample["label"],
            "p_yes": y_score["p_yes"],
            "p_no": y_score["p_no"],
            "predicted_label": y_score["predicted_label"],
        },
        "n": {
            "sample_user_id": n_sample["user_id"],
            "label": n_sample["label"],
            "label_probabilities": n_score["label_probabilities"],
            "predicted_label": n_score["predicted_label"],
        },
        "checked": True,
    }


def _write_run_inputs(
    output_dir: Path,
    config: dict[str, Any],
    args: argparse.Namespace,
    dataset_key: str,
    y_train_records: list[dict[str, Any]],
    n_train_records: list[dict[str, Any]],
    y_valid_records: list[dict[str, Any]],
    n_valid_records: list[dict[str, Any]],
    task_ratio: dict[str, int],
) -> None:
    snapshot = dict(config)
    snapshot.pop("_repo_root", None)
    train_counts = count_ratio_examples(
        y_count=len(y_train_records),
        n_count=len(n_train_records),
        task_ratio_y=task_ratio["y"],
        task_ratio_n=task_ratio["n"],
    )
    valid_counts = count_ratio_examples(
        y_count=len(y_valid_records),
        n_count=len(n_valid_records),
        task_ratio_y=task_ratio["y"],
        task_ratio_n=task_ratio["n"],
    )
    write_yaml(output_dir / "config_snapshot.yaml", snapshot)
    write_json(
        output_dir / "run_summary.json",
        {
            "model": "m_k0",
            "dataset": dataset_key,
            "created_at_utc": datetime.now(timezone.utc).isoformat(),
            "max_y_train_samples": args.max_y_train_samples,
            "max_n_train_samples": args.max_n_train_samples,
            "max_y_valid_samples": args.max_y_valid_samples,
            "max_n_valid_samples": args.max_n_valid_samples,
            "y_train_records_loaded": len(y_train_records),
            "n_train_records_loaded": len(n_train_records),
            "y_valid_records_loaded": len(y_valid_records),
            "n_valid_records_loaded": len(n_valid_records),
            "task_ratio": task_ratio,
            "interleaved_train_samples": train_counts["total"],
            "interleaved_valid_samples": valid_counts["total"],
            "interleaved_train_task_counts": {
                "Y": train_counts["Y"],
                "N": train_counts["N"],
            },
            "interleaved_valid_task_counts": {
                "Y": valid_counts["Y"],
                "N": valid_counts["N"],
            },
            "interleaved_train_cycles": train_counts["cycle_count"],
            "interleaved_valid_cycles": valid_counts["cycle_count"],
            "output_dir": str(output_dir),
            "smoke": args.smoke,
            "task_schedule": "ratio_ordered_y_n_examples",
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
        raw_path = config.get("outputs", {}).get("m", "outputs/m/{dataset}")
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
    parser = argparse.ArgumentParser(description="训练 M-K0 Y + N Multi-task Tuning")
    parser.add_argument("--config", default="configs/m.yaml", help="M-K0 配置路径")
    parser.add_argument("--dataset", default=None, help="数据集 key，默认使用 dataset.formal")
    parser.add_argument("--output-dir", default=None, help="覆盖输出目录")
    parser.add_argument("--run-name", default=None, help="追加到输出目录下的运行名")
    parser.add_argument("--smoke", action="store_true", help="标记本次为 smoke/overfit 运行")
    parser.add_argument("--max-y-train-samples", type=int, default=1000, help="最多读取 Y train 样本数；负数表示全量")
    parser.add_argument("--max-n-train-samples", type=int, default=1000, help="最多读取 N train 样本数；负数表示全量")
    parser.add_argument("--max-y-valid-samples", type=int, default=1000, help="最多读取 Y validation 样本数；负数表示全量")
    parser.add_argument("--max-n-valid-samples", type=int, default=1000, help="最多读取 N validation 样本数；负数表示全量")
    parser.add_argument("--task-ratio-y", type=int, default=None, help="M 训练中每个周期的 Y 样本数；默认读取配置")
    parser.add_argument("--task-ratio-n", type=int, default=None, help="M 训练中每个周期的 N 样本数；默认读取配置")
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
    parser.add_argument("--run-reload-check", action="store_true", help="训练后重载 adapter 并检查 Y/N 两种接口")
    parser.add_argument("--reload-only", action="store_true", help="不训练，只重载已有 adapter 并检查 Y/N 两种接口")
    parser.add_argument("--adapter-dir", default=None, help="reload-only 使用的 adapter 目录")
    parser.add_argument("--reload-split", default="validation", choices=["validation", "test"], help="reload-only 取样 split")
    return parser.parse_args()


def main() -> None:
    summary = run_m_training(parse_args())
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
