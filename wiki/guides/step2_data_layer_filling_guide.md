---
title: STEP 2 数据层填充指南
type: guide
status: current
authority: normative
source: agent
created: 2026-07-28
updated: 2026-07-30
last_verified: 2026-07-30
related_code:
  - task.md
  - README.md
  - configs/experiment.yaml
  - wiki/modules/movielens_data_layer.md
---

# STEP 2 数据层填充指南

## 目的

本指南说明如何按当前 Y/N/M 任务定义构建 MovieLens 数据层。STEP 2 代码已经同步为新的 timestamp tie 策略，并已重新生成 MovieLens-100K 开发产物。

## 总体流程

```text
原始 MovieLens 文件
  -> 标准化 interaction
  -> 用户内 full_sequence
  -> timestamp bucket
  -> chronological split
  -> Y_train / Y_valid / Y_test
  -> N_train / N_valid / N_test
  -> 统计与人工检查样本
```

核心规则：

```text
history = 所有 timestamp < target_timestamp 的 interaction
```

## timestamp tie

同一 timestamp 内没有可观测先后顺序。

禁止：

```text
用 movie_id 排序构造先后
用原始文件顺序构造先后
用排序后的行号构造先后
```

timestamp tie 不再导致整个用户退出数据集。

## Y 样本

Y target 可以来自 full_sequence 中任意 interaction。

同一 timestamp bucket 内的多个 Y target 共享同一份严格 history：

```text
history = timestamp < target_timestamp
```

Y split：

```text
最后一个 timestamp bucket       -> Y test
倒数第二个 timestamp bucket     -> Y validation
更早 timestamp buckets          -> Y train
```

## N 样本

N 只构造严格可确定的 next-item sample。

如果下一 timestamp bucket 中有多个 interaction，则该位置 ground truth 有歧义：

```text
跳过该 N sample
不跳过整个 user
```

构造完某用户所有合法 N samples 后：

```text
最后一个合法 N sample       -> N test
倒数第二个合法 N sample     -> N validation
更早合法 N samples          -> N train
```

如果合法 N samples 不足，才从 N 任务跳过该用户。

## M 训练无泄漏

M 的训练数据必须先切时间，再构造任务：

```text
Raw interactions
-> chronological split
-> Y_train / N_train
-> multi-task training
```

禁止先从完整数据生成全部 Y/N 样本后再混合训练。

只要某 interaction 位于用户 validation/test 时间范围，就不得进入 M 的任何训练样本。

## 人工检查重点

生成 MovieLens-100K 产物后先停下来，人工检查：

- 同 timestamp interaction 是否没有互相进入 history
- Y 同 bucket 多 target 是否共享严格 history
- N 是否只保留 singleton target bucket 的合法 next-item sample
- N 是否只跳过歧义 sample，而不是整个 user
- Y/N validation/test 是否按各自任务口径固定
- M 的 Y_train/N_train 是否都来自训练时间区域

## 进入 STEP 3 前的停止条件

MovieLens-100K 至少应具备：

- Y train/validation/test 文件
- N train/validation/test 或固定候选所需的 N valid/test 定义
- timestamp bucket size 分布
- singleton bucket 占比
- 合法 N sample 数分布
- Y/N 用户数和样本数
- 跳过用户与保留用户的基础对比统计
- 通过 leakage 和 reproducibility 检查
