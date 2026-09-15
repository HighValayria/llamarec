---
title: "11 multiseed and crossdataset"
type: report
status: current
authority: descriptive
source: agent
created: 2026-08-24
updated: 2026-08-24
last_verified: 2026-08-24
related_code:
  - src/analysis/multiseed_stability_summary.py
  - src/train/train_y.py
  - src/train/train_n.py
  - src/train/train_m.py
  - src/baselines/sasrec.py
  - src/data/preprocess.py
  - src/data/build_step2.py
---

# 11 Multi-seed And Cross-dataset

## 为什么需要 multi-seed

[INTERPRETATION] 单个 seed 可能受初始化、data order、dropout、CUDA 随机性影响。只看 seed42，无法判断结果方向是否稳定。

[FACT] 当前 MovieLens multi-seed 固定 `k5_popmatch_seed42` candidate files，只改变 training seed 42/43/44。

## seed 设置在哪里

[FACT] 训练入口支持 `--seed`，并在 model initialization 前设置：

```text
Python random
NumPy
Torch
CUDA
Transformers set_seed
```

代码：`src/train/train_y.py::_set_training_seed()`，N/M 训练复用它。

## candidate seed vs training seed

candidate seed:

```text
决定 validation/test candidate files
```

training seed:

```text
决定模型训练随机性
```

[FACT] Multi-seed stability 中 candidate protocol 固定为 `k5_popmatch_seed42`。

面试说法：

> 我固定 candidate seed，是为了把候选集难度固定住，只看训练随机性对模型结果的影响。

## MovieLens multi-seed 三个核心发现

1. Y-K0 binary stable

[FACT] Y-K0 binary F1 range `0.0098`。

2. N-K0 > M1 stable

[FACT] seeds 42/43/44 下 N-K0 HR@1 都高于 M1，最小 margin `0.0104`。

3. budget-sensitive SASRec stable

[FACT] N-K0 都高于 SASRec exp-match，最小 margin `0.2767`；SASRec high s3000 都高于 N-K0，最小 margin `0.0777`。

## multi-seed 不能证明什么

不能说：

```text
严格统计显著
compute/capacity matched
Amazon 也 multi-seed
```

要说：

```text
three-seed stability diagnostic
fixed candidate protocol
supports direction, not final significance proof
```

## 为什么需要第二数据集

[INTERPRETATION] MovieLens-1M 比较密集，且是电影领域。只在 MovieLens 成立的结果，外部有效性不足。

Amazon Musical Instruments 更稀疏，用于 compact cross-dataset validation。

## Amazon 数据协议

[FACT] Amazon 使用：

```text
user_id
parent_asin
rating
timestamp
title
```

[FACT] 不使用：

```text
review text
description
brand/category/price
images
external product knowledge
```

## Amazon 规模

[FACT]

```text
users:        57,439
items:        24,584
interactions: 511,792
Y train:      396,908
Y valid/test: 57,442 / 57,442
N train:      339,449
N valid/test: 57,439 / 57,439
```

## 为什么 Amazon Books 最开始不能用

[FACT] 最初 Amazon Books source 是 product catalog metadata，不是 user-item interaction logs，因此不能构造用户序列、Y/N split 或 next-item samples。

## Amazon PopMatch 主结果

[FACT] Amazon PopMatch-k5 seed42：

```text
Base HR@1:          0.3573
Y-K0 ranking HR@1: 0.2298
N-K0 HR@1:         0.4669
M1 HR@1:           0.4582
SASRec-exp HR@1:   0.1757
```

Interpretation:

[INTERPRETATION] 方向复现：N-K0 > M1，且 N-K0 >> closest-exposure SASRec。

Boundary:

[FACT] N-K0 over M1 margin small: HR@1 `+0.0087`。Amazon seed42 only。

## 面试模板

问：Amazon 结果能说明什么？

答：

> 它说明 MovieLens 上的主方向在第二数据集 seed42 下方向复现，尤其是 N-K0 高于 M1、N-K0 高于 closest-exposure SASRec。但 Amazon 只有 seed42，N-M margin 也小，所以不能说 cross-dataset multi-seed stability 或大幅优势。
