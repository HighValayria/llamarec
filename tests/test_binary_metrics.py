"""STEP 3 测试：Y 二分类指标。"""

from src.eval.binary_metrics import accuracy, auc, binary_metrics, f1_score


def test_binary_metrics_simple_case():
    records = [
        {"score": 0.9, "label": "Yes"},
        {"score": 0.8, "label": "Yes"},
        {"score": 0.4, "label": "No"},
        {"score": 0.1, "label": "No"},
    ]

    metrics = binary_metrics(records, threshold=0.5)

    assert metrics["AUC"] == 1.0
    assert metrics["F1"] == 1.0
    assert metrics["Accuracy"] == 1.0


def test_auc_handles_ties_with_average_ranks():
    assert auc(scores=[0.5, 0.5], labels=[1, 0]) == 0.5


def test_f1_and_accuracy_partial_case():
    predictions = [1, 1, 0, 0]
    labels = [1, 0, 1, 0]

    assert f1_score(predictions, labels) == 0.5
    assert accuracy(predictions, labels) == 0.5
