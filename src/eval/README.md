# STEP 3 评测层

本目录负责固定候选集与指标实现，必须早于任何模型训练完成。

## 当前文件

- `candidate_sets.py`：从 N validation/test 样本生成固定候选集。
- `ranking_metrics.py`：HR@1、HR@5、NDCG@5、MRR。
- `binary_metrics.py`：AUC、F1、Accuracy。

## 固定候选集

候选集按数据集分目录保存：

```text
data/candidates/{dataset}/valid.jsonl
data/candidates/{dataset}/test.jsonl
```

每条记录包含：

- `user_id`
- `history`
- `target`
- `candidate_movie_ids`
- `ground_truth_movie_id`
- `ground_truth_index`
- `label`
- `label_set`

生成命令：

```bash
python -m src.eval.candidate_sets --config configs/experiment.yaml --dataset movielens-100k
python -m src.eval.candidate_sets --config configs/experiment.yaml --dataset movielens-32m
```

候选集只生成一次。后续 Base-N、N-K0、M-N，以及使用 P(Yes) 做候选排序的 Y 接口，都必须读取同一份固定候选文件，不能在评测时重新采样。

当前已生成：

```text
movielens-100k: valid 902 / test 902
movielens-32m:  valid 193491 / test 193491
```

## 指标语义

Ranking metrics 只说明真实 next interaction 在候选集中的排序位置，不直接解释为“用户喜欢程度排序”。

对于 5 个候选、ground truth 排在第 3 位的人工案例：

```text
HR@1 = 0
HR@5 = 1
NDCG@5 = 1 / log2(4) = 0.5
MRR = 1 / 3
```

这个案例已经由 `tests/test_ranking_metrics.py` 覆盖。
