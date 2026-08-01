"""STEP 6：N-K0 next-item candidate label 训练数据编码。"""

from __future__ import annotations

from typing import Any

from src.inference.prompts import (
    assert_no_candidate_rating_in_candidate_prompt,
    render_candidate_prompt,
)
from src.train.preference_dataset import (
    IGNORE_INDEX,
    _encode_prompt_and_answer,
    _left_trim_to_length,
)


class NextItemTrainingDataset:
    """把 N 样本编码为 causal LM 训练样本。"""

    def __init__(
        self,
        records: list[dict[str, Any]],
        tokenizer: Any,
        movie_lookup: dict[str, dict[str, str]],
        max_seq_length: int,
        use_chat_format: bool,
    ) -> None:
        if not records:
            raise ValueError("N 训练数据为空。")
        self.examples = [
            encode_next_item_record(
                record=record,
                tokenizer=tokenizer,
                movie_lookup=movie_lookup,
                max_seq_length=max_seq_length,
                use_chat_format=use_chat_format,
            )
            for record in records
        ]

    def __len__(self) -> int:
        return len(self.examples)

    def __getitem__(self, index: int) -> dict[str, list[int]]:
        return self.examples[index]


def encode_next_item_record(
    record: dict[str, Any],
    tokenizer: Any,
    movie_lookup: dict[str, dict[str, str]],
    max_seq_length: int,
    use_chat_format: bool,
) -> dict[str, list[int]]:
    """编码单条 N 样本，并只在 A-E 答案 token 上计算 loss。"""

    label_set = [str(label) for label in record.get("label_set", [])]
    label = str(record["label"])
    if label not in label_set:
        raise ValueError(f"N 标签必须属于 label_set，实际为: {label!r}")
    if label_set and len(label_set) != len(record.get("candidate_movie_ids", [])):
        raise ValueError("label_set 长度必须与 candidate_movie_ids 一致。")

    prompt = render_candidate_prompt(record, movie_lookup)
    assert_no_candidate_rating_in_candidate_prompt(prompt)
    prefix_ids, full_ids = _encode_prompt_and_answer(
        tokenizer=tokenizer,
        prompt=prompt,
        answer=label,
        use_chat_format=use_chat_format,
    )
    if len(full_ids) <= len(prefix_ids):
        raise ValueError("完整训练序列没有包含 N 答案 token。")

    labels = [IGNORE_INDEX] * len(full_ids)
    for position in range(len(prefix_ids), len(full_ids)):
        labels[position] = full_ids[position]

    input_ids, labels = _left_trim_to_length(
        input_ids=full_ids,
        labels=labels,
        max_seq_length=max_seq_length,
    )
    if not any(label_id != IGNORE_INDEX for label_id in labels):
        raise ValueError("截断后没有保留任何 N 答案 token，无法训练。")

    return {
        "input_ids": input_ids,
        "attention_mask": [1] * len(input_ids),
        "labels": labels,
    }
