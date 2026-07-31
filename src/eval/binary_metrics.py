"""STEP 3：Y Yes/No 二分类指标。"""

from __future__ import annotations

from typing import Any


def binary_metrics(
    records: list[dict[str, Any]],
    threshold: float = 0.5,
) -> dict[str, float | None]:
    """计算 AUC、F1、Accuracy。

    每条记录需要包含：
    - `score`: P(Yes) 或其他越大越偏向 Yes 的连续分数；
    - `label`: `Yes`/`No` 或 1/0。
    """

    labels = [_label_to_int(record["label"]) for record in records]
    scores = [float(record["score"]) for record in records]
    predictions = [1 if score >= threshold else 0 for score in scores]

    return {
        "AUC": auc(scores, labels),
        "F1": f1_score(predictions, labels),
        "Accuracy": accuracy(predictions, labels),
    }


def auc(scores: list[float], labels: list[int]) -> float | None:
    """用 rank-sum 计算二分类 AUC，支持同分平均排名。"""

    if len(scores) != len(labels):
        raise ValueError("scores 和 labels 长度不一致")
    if not scores:
        return None

    positive_count = sum(1 for label in labels if label == 1)
    negative_count = sum(1 for label in labels if label == 0)
    if positive_count == 0 or negative_count == 0:
        return None

    ranked = sorted(zip(scores, labels), key=lambda item: item[0])
    rank_sum_positive = 0.0
    rank = 1
    index = 0
    while index < len(ranked):
        tie_end = index
        while tie_end < len(ranked) and ranked[tie_end][0] == ranked[index][0]:
            tie_end += 1

        average_rank = (rank + rank + (tie_end - index) - 1) / 2
        for tied_index in range(index, tie_end):
            if ranked[tied_index][1] == 1:
                rank_sum_positive += average_rank

        rank += tie_end - index
        index = tie_end

    return (
        rank_sum_positive - positive_count * (positive_count + 1) / 2
    ) / (positive_count * negative_count)


def f1_score(predictions: list[int], labels: list[int]) -> float:
    """计算正类 Yes 的 F1。"""

    if len(predictions) != len(labels):
        raise ValueError("predictions 和 labels 长度不一致")

    true_positive = sum(1 for pred, label in zip(predictions, labels) if pred == label == 1)
    false_positive = sum(1 for pred, label in zip(predictions, labels) if pred == 1 and label == 0)
    false_negative = sum(1 for pred, label in zip(predictions, labels) if pred == 0 and label == 1)

    denominator = 2 * true_positive + false_positive + false_negative
    if denominator == 0:
        return 0.0
    return 2 * true_positive / denominator


def accuracy(predictions: list[int], labels: list[int]) -> float:
    """计算 Accuracy。"""

    if len(predictions) != len(labels):
        raise ValueError("predictions 和 labels 长度不一致")
    if not labels:
        return 0.0
    correct = sum(1 for pred, label in zip(predictions, labels) if pred == label)
    return correct / len(labels)


def _label_to_int(label: Any) -> int:
    if isinstance(label, str):
        normalized = label.strip().lower()
        if normalized == "yes":
            return 1
        if normalized == "no":
            return 0
    if label in {1, True}:
        return 1
    if label in {0, False}:
        return 0
    raise ValueError(f"无法解析二分类标签: {label!r}")
