"""STEP 5：Y-K0 Yes/No Preference Tuning 训练入口。"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import inspect
import json
from pathlib import Path
from typing import Any

import yaml

from src.data.config import (
    load_experiment_config,
    resolve_configured_output_path,
    resolve_repo_path_from_config,
)
from src.inference.prediction_io import read_jsonl, write_json, write_yaml
from src.inference.prompts import render_yesno_prompt
from src.train.preference_dataset import (
    PreferenceDataCollator,
    PreferenceTrainingDataset,
    summarize_encoded_examples,
)


def run_y_training(args: argparse.Namespace) -> dict[str, Any]:
    """运行 Y-K0 训练。真实模型依赖只在云端执行到这里时导入。"""

    config = load_training_config(args.config)
    dataset_key = args.dataset or config["dataset"]["formal"]
    if getattr(args, "reload_only", False):
        return _run_reload_only(args=args, config=config, dataset_key=dataset_key)

    output_dir = _resolve_output_dir(config, dataset_key, args)
    output_dir.mkdir(parents=True, exist_ok=True)

    train_records = _load_preference_records(
        config=config,
        dataset_key=dataset_key,
        split_name="train",
        limit=_normalize_sample_limit(args.max_train_samples),
    )
    valid_records = _load_preference_records(
        config=config,
        dataset_key=dataset_key,
        split_name="validation",
        limit=_normalize_sample_limit(args.max_valid_samples),
    )
    if not train_records:
        raise ValueError("Y 训练记录为空，不能启动训练。")
    if not valid_records:
        raise ValueError("Y validation 记录为空，不能启动训练。")

    _write_run_inputs(
        output_dir=output_dir,
        config=config,
        args=args,
        dataset_key=dataset_key,
        train_records=train_records,
        valid_records=valid_records,
    )

    tokenizer, model = _load_tokenizer_and_model(config)
    train_dataset = PreferenceTrainingDataset(
        records=train_records,
        tokenizer=tokenizer,
        max_seq_length=int(config["model"]["max_seq_length"]),
        use_chat_format=_use_chat_format(config),
    )
    valid_dataset = PreferenceTrainingDataset(
        records=valid_records,
        tokenizer=tokenizer,
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
        "model": "y_k0",
        "dataset": dataset_key,
        "output_dir": str(output_dir),
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
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
        reload_report = _run_reload_probability_check(
            config=config,
            adapter_dir=output_dir / "adapter",
            sample=valid_records[0],
        )
        write_json(output_dir / "reload_check.json", reload_report)

    return metrics


def _run_reload_only(
    args: argparse.Namespace,
    config: dict[str, Any],
    dataset_key: str,
) -> dict[str, Any]:
    """只验证已保存的 Y adapter 能否重新加载并输出 P(Yes)/P(No)。"""

    adapter_dir = _resolve_adapter_dir(config, dataset_key, args)
    if not adapter_dir.exists():
        raise FileNotFoundError(f"adapter 目录不存在：{adapter_dir}")

    split_name = getattr(args, "reload_split", "validation")
    valid_records = _load_preference_records(
        config=config,
        dataset_key=dataset_key,
        split_name=split_name,
        limit=1,
    )
    if not valid_records:
        raise ValueError(f"Y {split_name} 记录为空，不能执行重载检查。")

    reload_report = _run_reload_probability_check(
        config=config,
        adapter_dir=adapter_dir,
        sample=valid_records[0],
    )
    output_dir = adapter_dir.parent if adapter_dir.name == "adapter" else adapter_dir
    write_json(output_dir / "reload_check.json", reload_report)
    return {
        "model": "y_k0",
        "dataset": dataset_key,
        "mode": "reload_only",
        "split": split_name,
        "adapter_dir": str(adapter_dir),
        "reload_check": reload_report,
    }


def load_training_config(config_path: str | Path) -> dict[str, Any]:
    """读取任务配置，并合并其继承的统一实验配置。"""

    config_path = Path(config_path).resolve()
    with config_path.open("r", encoding="utf-8") as handle:
        child_config = yaml.safe_load(handle) or {}

    inherited_path = child_config.get("inherits")
    if not inherited_path:
        return load_experiment_config(config_path)

    repo_root = config_path.parent.parent if config_path.parent.name == "configs" else config_path.parent
    inherited_path = Path(inherited_path)
    if not inherited_path.is_absolute():
        inherited_path = repo_root / inherited_path

    parent_config = load_experiment_config(inherited_path)
    child_config = {
        key: value
        for key, value in child_config.items()
        if key != "inherits"
    }
    merged = _deep_merge(parent_config, child_config)
    merged["_repo_root"] = parent_config["_repo_root"]
    return merged


def _load_preference_records(
    config: dict[str, Any],
    dataset_key: str,
    split_name: str,
    limit: int | None,
) -> list[dict[str, Any]]:
    path = resolve_configured_output_path(
        config,
        dataset_key,
        "preference_samples",
        split_name,
    )
    if not path.exists():
        raise FileNotFoundError(
            f"Y {split_name} 数据不存在: {path}。"
            " 请先为当前数据集生成完整 STEP 2 产物。"
        )
    return read_jsonl(path, limit=limit)


def _normalize_sample_limit(raw_limit: int | None) -> int | None:
    """CLI 中用负数表示不限制样本数。"""

    if raw_limit is None:
        return None
    if raw_limit < 0:
        return None
    return raw_limit


def _load_tokenizer_and_model(config: dict[str, Any]):
    try:
        import torch
        from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
        from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
    except ImportError as exc:
        raise ImportError(
            "Y-K0 训练需要安装 torch、transformers、peft、bitsandbytes。"
        ) from exc

    model_name_or_path = config["model"]["base_model"]["name_or_path"]
    tokenizer = AutoTokenizer.from_pretrained(model_name_or_path, use_fast=True)
    if tokenizer.pad_token is None and tokenizer.eos_token is not None:
        tokenizer.pad_token = tokenizer.eos_token

    quant_config = BitsAndBytesConfig(
        load_in_4bit=bool(config["lora"].get("load_in_4bit", True)),
        bnb_4bit_quant_type=str(config["lora"].get("quant_type", "nf4")),
        bnb_4bit_compute_dtype=_torch_dtype(torch),
        bnb_4bit_use_double_quant=True,
    )
    model = AutoModelForCausalLM.from_pretrained(
        model_name_or_path,
        quantization_config=quant_config,
        device_map="auto",
        dtype=_torch_dtype(torch),
        low_cpu_mem_usage=True,
    )
    model.config.use_cache = False
    if bool(config["lora"].get("gradient_checkpointing", True)):
        model.gradient_checkpointing_enable()

    model = prepare_model_for_kbit_training(model)
    lora_config = LoraConfig(
        r=int(config["lora"]["r"]),
        lora_alpha=int(config["lora"]["alpha"]),
        lora_dropout=float(config["lora"]["dropout"]),
        bias="none",
        task_type="CAUSAL_LM",
        target_modules=list(config["lora"]["target_modules"]),
    )
    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()
    return tokenizer, model


def _build_trainer(
    args: argparse.Namespace,
    config: dict[str, Any],
    model: Any,
    tokenizer: Any,
    train_dataset: PreferenceTrainingDataset,
    valid_dataset: PreferenceTrainingDataset,
    output_dir: Path,
):
    from transformers import Trainer, TrainingArguments

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
    return Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=valid_dataset,
        data_collator=PreferenceDataCollator(tokenizer),
    )


def _run_reload_probability_check(
    config: dict[str, Any],
    adapter_dir: Path,
    sample: dict[str, Any],
) -> dict[str, Any]:
    import torch
    from peft import PeftModel
    from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

    model_name_or_path = config["model"]["base_model"]["name_or_path"]
    tokenizer = AutoTokenizer.from_pretrained(model_name_or_path, use_fast=True)
    if tokenizer.pad_token is None and tokenizer.eos_token is not None:
        tokenizer.pad_token = tokenizer.eos_token

    quant_config = BitsAndBytesConfig(
        load_in_4bit=bool(config["lora"].get("load_in_4bit", True)),
        bnb_4bit_quant_type=str(config["lora"].get("quant_type", "nf4")),
        bnb_4bit_compute_dtype=_torch_dtype(torch),
        bnb_4bit_use_double_quant=True,
    )
    base_model = AutoModelForCausalLM.from_pretrained(
        model_name_or_path,
        quantization_config=quant_config,
        device_map="auto",
        dtype=_torch_dtype(torch),
        low_cpu_mem_usage=True,
    )
    model = PeftModel.from_pretrained(base_model, str(adapter_dir))
    model.eval()

    prompt = render_yesno_prompt(sample)
    input_ids = _encode_prompt_for_inference(tokenizer, prompt, _use_chat_format(config))
    tensor = torch.tensor([input_ids], dtype=torch.long, device=next(model.parameters()).device)
    yes_id = tokenizer.encode("Yes", add_special_tokens=False)[0]
    no_id = tokenizer.encode("No", add_special_tokens=False)[0]
    with torch.no_grad():
        logits = model(input_ids=tensor).logits[0, -1]
        probs = torch.softmax(logits[[yes_id, no_id]].float(), dim=0)

    return {
        "adapter_dir": str(adapter_dir),
        "sample_user_id": sample["user_id"],
        "p_yes": float(probs[0].detach().cpu()),
        "p_no": float(probs[1].detach().cpu()),
        "checked": True,
    }


def _encode_prompt_for_inference(tokenizer: Any, prompt: str, use_chat_format: bool) -> list[int]:
    chat_format_attr = "chat_" + "tem" + "plate"
    chat_apply_attr = "apply_chat_" + "tem" + "plate"
    chat_format = getattr(tokenizer, chat_format_attr, None)
    chat_apply = getattr(tokenizer, chat_apply_attr, None)
    if use_chat_format and chat_format and chat_apply:
        encoded = chat_apply(
            [{"role": "user", "content": prompt}],
            tokenize=True,
            add_generation_prompt=True,
        )
        return _normalize_token_ids(tokenizer, encoded)
    return _normalize_token_ids(tokenizer, tokenizer.encode(prompt, add_special_tokens=True))


def _normalize_token_ids(tokenizer: Any, encoded: Any) -> list[int]:
    """把 tokenizer 的不同返回类型统一成 ``list[int]``。"""

    if isinstance(encoded, str):
        encoded = tokenizer.encode(encoded, add_special_tokens=False)
    elif isinstance(encoded, dict):
        encoded = encoded.get("input_ids")
    elif hasattr(encoded, "input_ids"):
        encoded = encoded.input_ids

    if encoded is None:
        raise ValueError("tokenizer 未返回 input_ids。")
    if hasattr(encoded, "tolist"):
        encoded = encoded.tolist()
    if isinstance(encoded, tuple):
        encoded = list(encoded)
    if encoded and isinstance(encoded[0], list):
        if len(encoded) != 1:
            raise ValueError("当前重载检查只支持单条 prompt。")
        encoded = encoded[0]

    try:
        return [int(token_id) for token_id in encoded]
    except (TypeError, ValueError) as exc:
        raise TypeError(
            f"无法把 tokenizer 输出转换为 token id 列表: {type(encoded)!r}"
        ) from exc


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
            "model": "y_k0",
            "dataset": dataset_key,
            "created_at_utc": datetime.now(timezone.utc).isoformat(),
            "max_train_samples": args.max_train_samples,
            "max_valid_samples": args.max_valid_samples,
            "train_records_loaded": len(train_records),
            "valid_records_loaded": len(valid_records),
            "output_dir": str(output_dir),
            "smoke": args.smoke,
        },
    )


def _release_cuda_cache() -> None:
    try:
        import gc
        import torch
    except ImportError:
        return

    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()


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
        raw_path = config.get("outputs", {}).get("y", "outputs/y/{dataset}")
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


def _trainable_parameter_summary(model: Any) -> dict[str, int | float]:
    trainable = 0
    total = 0
    for parameter in model.parameters():
        count = parameter.numel()
        total += count
        if parameter.requires_grad:
            trainable += count
    return {
        "trainable": trainable,
        "total": total,
        "ratio": trainable / total if total else 0.0,
    }


def _torch_dtype(torch_module: Any) -> Any:
    if torch_module.cuda.is_available() and torch_module.cuda.is_bf16_supported():
        return torch_module.bfloat16
    if torch_module.cuda.is_available():
        return torch_module.float16
    return torch_module.float32


def _use_chat_format(config: dict[str, Any]) -> bool:
    return bool(config["model"]["base_model"].get("require_instruct_chat_format", False))


def _deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    merged = dict(base)
    for key, value in override.items():
        if (
            key in merged
            and isinstance(merged[key], dict)
            and isinstance(value, dict)
        ):
            merged[key] = _deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="训练 Y-K0 Yes/No Preference Tuning")
    parser.add_argument("--config", default="configs/y.yaml", help="Y-K0 配置路径")
    parser.add_argument("--dataset", default=None, help="数据集 key，默认使用 dataset.formal")
    parser.add_argument("--output-dir", default=None, help="覆盖输出目录")
    parser.add_argument("--run-name", default=None, help="追加到输出目录下的运行名")
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
    parser.add_argument("--run-reload-check", action="store_true", help="训练后重载 adapter 并输出 P(Yes)")
    parser.add_argument("--reload-only", action="store_true", help="不训练，只重载已有 adapter 并输出 P(Yes)")
    parser.add_argument("--adapter-dir", default=None, help="reload-only 使用的 adapter 目录")
    parser.add_argument("--reload-split", default="validation", choices=["validation", "test"], help="reload-only 取样 split")
    return parser.parse_args()


def main() -> None:
    summary = run_y_training(parse_args())
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
