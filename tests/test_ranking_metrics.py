"""STEP 3 测试：ranking 指标人工案例。"""

from src.eval.ranking_metrics import (
    aggregate_ranking_metrics,
    ground_truth_rank,
    ranking_metrics_for_rank,
    ranking_metrics_for_scores,
)


def test_manual_case_ground_truth_rank_third():
    metrics = ranking_metrics_for_rank(rank=3, k=5)

    assert metrics["HR@1"] == 0.0
    assert metrics["HR@5"] == 1.0
    assert metrics["NDCG@5"] == 0.5
    assert metrics["MRR"] == 1 / 3


def test_scores_case_ground_truth_rank_third():
    # ground_truth_index=2 的分数排第三：0.9、0.8、0.7。
    scores = [0.9, 0.8, 0.7, 0.2, 0.1]

    assert ground_truth_rank(scores, ground_truth_index=2) == 3
    assert ranking_metrics_for_scores(scores, ground_truth_index=2)["NDCG@5"] == 0.5


def test_aggregate_ranking_metrics():
    records = [
        {"scores": [0.9, 0.1, 0.0, 0.0, 0.0], "ground_truth_index": 0},
        {"scores": [0.9, 0.8, 0.7, 0.2, 0.1], "ground_truth_index": 2},
    ]

    metrics = aggregate_ranking_metrics(records)

    assert metrics["HR@1"] == 0.5
    assert metrics["HR@5"] == 1.0
    assert metrics["MRR"] == (1.0 + 1 / 3) / 2
