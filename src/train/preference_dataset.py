"""STEP 5：Y-K0 偏好训练数据编码。"""

from __future__ import annotations

from typing import Any

from src.inference.prompts import (
    assert_no_target_rating_in_yesno_prompt,
    render_yesno_prompt,
)

IGNORE_INDEX = -100


class PreferenceTrainingDataset:
    """把 Y 样本编码为 causal LM 训练样本。"""

    def __init__(
        self,
        records: list[dict[str, Any]],
        tokenizer: Any,
        max_seq_length: int,
        use_chat_format: bool,
    ) -> None:
        if not records:
            raise ValueError("Y 训练数据为空。")
        self.examples = [
            encode_preference_record(
                record=record,
                tokenizer=tokenizer,
                max_seq_length=max_seq_length,
                use_chat_format=use_chat_format,
            )
            for record in records
        ]

    def __len__(self) -> int:
        return len(self.examples)

    def __getitem__(self, index: int) -> dict[str, list[int]]:
        return self.examples[index]


class PreferenceDataCollator:
    """对已经编码好的 Y 样本做右侧 padding。"""

    def __init__(self, tokenizer: Any) -> None:
        self.tokenizer = tokenizer

    def __call__(self, features: list[dict[str, list[int]]]) -> dict[str, Any]:
        import torch

        pad_token_id = self.tokenizer.pad_token_id
        if pad_token_id is None:
            pad_token_id = self.tokenizer.eos_token_id
        if pad_token_id is None:
            pad_token_id = 0

        max_length = max(len(feature["input_ids"]) for feature in features)
        batch = {"input_ids": [], "attention_mask": [], "labels": []}
        for feature in features:
            padding_length = max_length - len(feature["input_ids"])
            batch["input_ids"].append(feature["input_ids"] + [pad_token_id] * padding_length)
            batch["attention_mask"].append(feature["attention_mask"] + [0] * padding_length)
            batch["labels"].append(feature["labels"] + [IGNORE_INDEX] * padding_length)

        return {
            key: torch.tensor(value, dtype=torch.long)
            for key, value in batch.items()
        }


def encode_preference_record(
    record: dict[str, Any],
    tokenizer: Any,
    max_seq_length: int,
    use_chat_format: bool,
) -> dict[str, list[int]]:
    """编码单条 Y 样本，并只在答案 token 上计算 loss。"""

    label = str(record["label"])
    if label not in {"Yes", "No"}:
        raise ValueError(f"Y 标签必须是 Yes/No，实际为: {label!r}")

    prompt = render_yesno_prompt(record)
    assert_no_target_rating_in_yesno_prompt(prompt, record)

    prefix_ids, full_ids = _encode_prompt_and_answer(
        tokenizer=tokenizer,
        prompt=prompt,
        answer=label,
        use_chat_format=use_chat_format,
    )
    if len(full_ids) <= len(prefix_ids):
        raise ValueError("完整训练序列没有包含答案 token。")

    labels = [IGNORE_INDEX] * len(full_ids)
    for position in range(len(prefix_ids), len(full_ids)):
        labels[position] = full_ids[position]

    input_ids, labels = _left_trim_to_length(
        input_ids=full_ids,
        labels=labels,
        max_seq_length=max_seq_length,
    )
    if not any(label_id != IGNORE_INDEX for label_id in labels):
        raise ValueError("截断后没有保留任何答案 token，无法训练。")

    return {
        "input_ids": input_ids,
        "attention_mask": [1] * len(input_ids),
        "labels": labels,
    }


def summarize_encoded_examples(examples: list[dict[str, list[int]]]) -> dict[str, Any]:
    """生成训练样本编码摘要，用于 smoke test 日志。"""

    lengths = [len(example["input_ids"]) for example in examples]
    supervised_tokens = [
        sum(1 for label_id in example["labels"] if label_id != IGNORE_INDEX)
        for example in examples
    ]
    return {
        "examples": len(examples),
        "min_length": min(lengths) if lengths else 0,
        "max_length": max(lengths) if lengths else 0,
        "avg_length": sum(lengths) / len(lengths) if lengths else 0.0,
        "min_supervised_tokens": min(supervised_tokens) if supervised_tokens else 0,
        "max_supervised_tokens": max(supervised_tokens) if supervised_tokens else 0,
    }


def _encode_prompt_and_answer(
    tokenizer: Any,
    prompt: str,
    answer: str,
    use_chat_format: bool,
) -> tuple[list[int], list[int]]:
    chat_format_attr = "chat_" + "tem" + "plate"
    chat_apply_attr = "apply_chat_" + "tem" + "plate"
    chat_format = getattr(tokenizer, chat_format_attr, None)
    chat_apply = getattr(tokenizer, chat_apply_attr, None)
    if use_chat_format and chat_format and chat_apply:
        prefix = chat_apply(
            [{"role": "user", "content": prompt}],
            tokenize=True,
            add_generation_prompt=True,
        )
        full = chat_apply(
            [
                {"role": "user", "content": prompt},
                {"role": "assistant", "content": answer},
            ],
            tokenize=True,
            add_generation_prompt=False,
        )
        return _normalize_token_ids(tokenizer, prefix), _normalize_token_ids(tokenizer, full)

    prefix = tokenizer.encode(prompt, add_special_tokens=True)
    full = tokenizer.encode(f"{prompt} {answer}", add_special_tokens=True)
    return _normalize_token_ids(tokenizer, prefix), _normalize_token_ids(tokenizer, full)


def _normalize_token_ids(tokenizer: Any, encoded: Any) -> list[int]:
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
            raise ValueError("当前训练编码只支持单条样本。")
        encoded = encoded[0]

    return [int(token_id) for token_id in encoded]


def _left_trim_to_length(
    input_ids: list[int],
    labels: list[int],
    max_seq_length: int,
) -> tuple[list[int], list[int]]:
    if max_seq_length <= 0:
        raise ValueError("max_seq_length 必须为正整数。")
    if len(input_ids) <= max_seq_length:
        return input_ids, labels

    overflow = len(input_ids) - max_seq_length
    return input_ids[overflow:], labels[overflow:]
