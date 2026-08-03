---
title: 评测层
type: module
status: current
authority: normative
source: mixed
created: 2026-07-30
updated: 2026-07-30
last_verified: 2026-07-30
related_code:
  - src/eval/candidate_sets.py
  - src/eval/ranking_metrics.py
  - src/eval/binary_metrics.py
  - tests/test_candidate_sets.py
  - tests/test_ranking_metrics.py
  - tests/test_binary_metrics.py
  - configs/experiment.yaml
---

# 评测层

## 范围

评测层负责 STEP 3：固定 validation/test 候选集，以及 Ranking / Binary 指标实现。

本层不加载 LLM，不训练模型。

## 固定候选集

当前候选集来源是对应数据集的 N validation/test 样本。候选集生成后按数据集写入：

```text
data/candidates/{dataset}/valid.jsonl
data/candidates/{dataset}/test.jsonl
```

候选集记录包含 `history`、`target`、`candidate_movie_ids`、`ground_truth_movie_id`、`ground_truth_index`、`label` 和 `label_set`。

候选集只生成一次。后续 Base-N / N-K0 / M-N 必须读取同一份固定文件；Y 接口若用 `P(Yes)` 对候选排序，也必须读取同一份候选文件。

## 指标

Ranking 指标：

```text
HR@1
HR@5
NDCG@5
MRR
```

这些指标只表示真实 next interaction 在候选集中的排序位置，不直接解释为喜欢程度排序。

Binary 指标：

```text
AUC
F1
Accuracy
```

## 当前状态

```text
movielens-100k valid candidates: 902 records
movielens-100k test candidates: 902 records
movielens-32m valid candidates: 193491 records
movielens-32m test candidates: 193491 records
candidate_num: 5
```

100K ground truth 位置分布：

```text
validation: index0 166 / index1 196 / index2 188 / index3 174 / index4 178
test:       index0 190 / index1 195 / index2 173 / index3 171 / index4 173
```

32M ground truth 位置分布：

```text
validation: index0 38826 / index1 38529 / index2 38882 / index3 38487 / index4 38767
test:       index0 38407 / index1 38527 / index2 38852 / index3 38701 / index4 39004
```

## 验证

`tests/test_ranking_metrics.py` 覆盖人工案例：

```text
ground truth rank = 3
HR@1 = 0
HR@5 = 1
NDCG@5 = 0.5
MRR = 1 / 3
```

`tests/test_candidate_sets.py` 覆盖候选唯一性、ground truth 恰好出现一次、位置非固定和 seed 复现。
