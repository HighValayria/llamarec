"""STEP 3：N candidate ranking 指标。

这里的 ranking 只评估真实 next interaction 在候选集里的排序位置，不直接解释为
用户喜欢程度排序。
"""

from __future__ import annotations

import math
from typing import Any


def ground_truth_rank(scores: list[float], ground_truth_index: int) -> int:
    """返回 ground truth 的 1-based 排名，分数越大排名越靠前。"""

    if not scores:
        raise ValueError("scores 不能为空")
    if ground_truth_index < 0 or ground_truth_index >= len(scores):
        raise IndexError("ground_truth_index 超出 scores 范围")

    ranked_indices = sorted(
        range(len(scores)),
        key=lambda index: (-float(scores[index]), index),
    )
    return ranked_indices.index(ground_truth_index) + 1


def ranking_metrics_for_rank(rank: int, k: int = 5) -> dict[str, float]:
    """基于单个 ground truth rank 计算 HR/NDCG/MRR。"""

    if rank <= 0:
        raise ValueError("rank 必须是 1-based 正整数")

    return {
        "HR@1": 1.0 if rank <= 1 else 0.0,
        f"HR@{k}": 1.0 if rank <= k else 0.0,
        f"NDCG@{k}": (1.0 / math.log2(rank + 1)) if rank <= k else 0.0,
        "MRR": 1.0 / rank,
    }


def ranking_metrics_for_scores(
    scores: list[float],
    ground_truth_index: int,
    k: int = 5,
) -> dict[str, float]:
    """基于候选分数计算单条样本的 ranking 指标。"""

    rank = ground_truth_rank(scores, ground_truth_index)
    return ranking_metrics_for_rank(rank, k=k)


def aggregate_ranking_metrics(records: list[dict[str, Any]], k: int = 5) -> dict[str, float]:
    """聚合多条预测记录的 ranking 指标。

    每条记录需要包含：
    - `scores`: 与候选顺序一致的分数列表；
    - `ground_truth_index`: 正确候选位置。
    """

    if not records:
        return {"HR@1": 0.0, f"HR@{k}": 0.0, f"NDCG@{k}": 0.0, "MRR": 0.0}

    totals = {"HR@1": 0.0, f"HR@{k}": 0.0, f"NDCG@{k}": 0.0, "MRR": 0.0}
    for record in records:
        metrics = ranking_metrics_for_scores(
            [float(score) for score in record["scores"]],
            int(record["ground_truth_index"]),
            k=k,
        )
        for key, value in metrics.items():
            totals[key] += value

    return {key: value / len(records) for key, value in totals.items()}
