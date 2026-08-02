"""STEP 7：M-K0 Y+N 多任务训练数据编码。"""

from __future__ import annotations

from typing import Any

from src.train.next_item_dataset import encode_next_item_record
from src.train.preference_dataset import encode_preference_record, summarize_encoded_examples


class MultitaskTrainingDataset:
    """把 Y 与 N 样本按给定比例顺序交替编码。"""

    def __init__(
        self,
        preference_records: list[dict[str, Any]],
        next_item_records: list[dict[str, Any]],
        tokenizer: Any,
        movie_lookup: dict[str, dict[str, str]],
        max_seq_length: int,
        use_chat_format: bool,
        task_ratio_y: int = 1,
        task_ratio_n: int = 1,
    ) -> None:
        task_ratio_y, task_ratio_n = validate_task_ratio(task_ratio_y, task_ratio_n)
        ratio_counts = count_ratio_examples(
            y_count=len(preference_records),
            n_count=len(next_item_records),
            task_ratio_y=task_ratio_y,
            task_ratio_n=task_ratio_n,
        )
        if ratio_counts["cycle_count"] <= 0:
            raise ValueError("M 训练需要同时存在 Y 与 N 样本。")

        self.examples = []
        y_index = 0
        n_index = 0
        for _ in range(ratio_counts["cycle_count"]):
            for _ in range(task_ratio_y):
                y_example = encode_preference_record(
                    record=preference_records[y_index],
                    tokenizer=tokenizer,
                    max_seq_length=max_seq_length,
                    use_chat_format=use_chat_format,
                )
                y_example["task"] = "Y"
                self.examples.append(y_example)
                y_index += 1

            for _ in range(task_ratio_n):
                n_example = encode_next_item_record(
                    record=next_item_records[n_index],
                    tokenizer=tokenizer,
                    movie_lookup=movie_lookup,
                    max_seq_length=max_seq_length,
                    use_chat_format=use_chat_format,
                )
                n_example["task"] = "N"
                self.examples.append(n_example)
                n_index += 1

        self.task_counts = {"Y": y_index, "N": n_index}
        self.task_ratio = {"Y": task_ratio_y, "N": task_ratio_n}
        self.cycle_count = ratio_counts["cycle_count"]

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


def validate_task_ratio(task_ratio_y: int, task_ratio_n: int) -> tuple[int, int]:
    """校验 Y/N 采样比例，避免静默退回错误实验语义。"""

    try:
        y_ratio = int(task_ratio_y)
        n_ratio = int(task_ratio_n)
    except (TypeError, ValueError) as exc:
        raise ValueError("M 任务采样比例必须是正整数。") from exc
    if y_ratio <= 0 or n_ratio <= 0:
        raise ValueError("M 任务采样比例必须是正整数。")
    return y_ratio, n_ratio


def count_ratio_examples(
    y_count: int,
    n_count: int,
    task_ratio_y: int,
    task_ratio_n: int,
) -> dict[str, int]:
    """计算给定样本池和比例下会实际编码多少 Y/N 样本。"""

    y_ratio, n_ratio = validate_task_ratio(task_ratio_y, task_ratio_n)
    cycle_count = min(y_count // y_ratio, n_count // n_ratio)
    return {
        "cycle_count": cycle_count,
        "Y": cycle_count * y_ratio,
        "N": cycle_count * n_ratio,
        "total": cycle_count * (y_ratio + n_ratio),
    }
