"""STEP 7：M-K0 Y+N 多任务训练数据编码。"""

from __future__ import annotations

from typing import Any

from src.train.next_item_dataset import encode_next_item_record
from src.train.preference_dataset import encode_preference_record, summarize_encoded_examples


class MultitaskTrainingDataset:
    """把 Y 与 N 样本按 1:1 顺序交替编码。"""

    def __init__(
        self,
        preference_records: list[dict[str, Any]],
        next_item_records: list[dict[str, Any]],
        tokenizer: Any,
        movie_lookup: dict[str, dict[str, str]],
        max_seq_length: int,
        use_chat_format: bool,
    ) -> None:
        pair_count = min(len(preference_records), len(next_item_records))
        if pair_count <= 0:
            raise ValueError("M 训练需要同时存在 Y 与 N 样本。")

        self.examples = []
        for index in range(pair_count):
            y_example = encode_preference_record(
                record=preference_records[index],
                tokenizer=tokenizer,
                max_seq_length=max_seq_length,
                use_chat_format=use_chat_format,
            )
            y_example["task"] = "Y"
            self.examples.append(y_example)

            n_example = encode_next_item_record(
                record=next_item_records[index],
                tokenizer=tokenizer,
                movie_lookup=movie_lookup,
                max_seq_length=max_seq_length,
                use_chat_format=use_chat_format,
            )
            n_example["task"] = "N"
            self.examples.append(n_example)

        self.task_counts = {"Y": pair_count, "N": pair_count}

    def __len__(self) -> int:
        return len(self.examples)

    def __getitem__(self, index: int) -> dict[str, Any]:
        return self.examples[index]


def summarize_multitask_examples(examples: list[dict[str, Any]]) -> dict[str, Any]:
    """生成 M 数据集摘要，并保留 Y/N 样本数。"""

    base_summary = summarize_encoded_examples(examples)
    task_counts = {"Y": 0, "N": 0}
    for example in examples:
        task = example.get("task")
        if task in task_counts:
            task_counts[task] += 1
    return {**base_summary, "task_counts": task_counts}
