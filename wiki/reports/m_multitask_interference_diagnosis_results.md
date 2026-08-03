---
title: M 多任务干扰诊断结果
type: report
status: current
authority: descriptive
source: mixed
created: 2026-08-03
updated: 2026-08-03
last_verified: 2026-08-03
related_code:
  - configs/m.yaml
  - src/train/multitask_dataset.py
  - src/train/train_m.py
  - src/inference/evaluate_m_adapter.py
  - src/analysis/basic_error_analysis.py
  - src/analysis/threshold_calibration.py
  - tests/test_m_training_data.py
  - tests/test_analysis_outputs.py
---

# M 多任务干扰诊断结果

## 结论摘要

MovieLens-1M 上的第一轮 M-K0 干扰诊断已经完成。当前不再继续启动 M3，也不进入 KAR、Hard Negative、SASRec、7B、多 seed 或 32M full training。

最重要的结论是：

- M0 的弱点不只是任务语义冲突，也包含训练步数不足和 Yes/No 阈值偏移。
- M1 将 M 的训练步数从 1500 增加到 3000 后，同时改善了 M-Y 和 M-N。
- M1 经过 validation best-F1 threshold 校准后，M-Y 已接近 Y-K0。
- M1 的 M-N 仍低于 N-K0，但显著高于 M0。
- M2 的 `Y:N=2:1` 没有缓解干扰，反而损害 N，并重新带来明显 Yes 偏置。

因此当前最稳妥的 M 版本是：

```text
M1:
Y:N = 1:1
train pool = 200k Y + 200k N
max_steps = 3000
binary reporting threshold = validation best-F1 threshold 0.3208213008
```

M1 可作为后续报告中的 M-K0 diagnostic best run，但需要和原始 M0 主结果区分，不应悄悄替换已经固化的 MVP baseline。

## 实验设置

| 实验 | run_name | Y:N ratio | train pool | max_steps | 目的 |
|---|---|---:|---|---:|---|
| M0 | `pool200k_1m_m_1500` | 1:1 | 200k Y + 200k N | 1500 | MVP baseline |
| M1 | `diag_m1_1m_m_200k_3000` | 1:1 | 200k Y + 200k N | 3000 | 判断 M0 是否未充分收敛 |
| M2 | `diag_m2_1m_m_y2n1_1500` | 2:1 | 200k Y + 100k N | 1500 | 检查提高 Y 采样比例是否缓解 M-Y 问题 |

M2 只修改 sampling ratio，不引入 loss weight。M3 原计划为 `Y:N=1:2`，但 M1/M2 已足以解释主要现象，因此本轮不启动。

## 默认 0.5 阈值下的 Test 结果

| 模型 | AUC | F1 | Accuracy | HR@1 | NDCG@5 | MRR |
|---|---:|---:|---:|---:|---:|---:|
| Y-K0 | 0.7691 | 0.7800 | 0.7115 | 0.3048 | 0.6504 | 0.5366 |
| N-K0 | - | - | - | 0.7189 | 0.8773 | 0.8356 |
| M0 | 0.7234 | 0.7630 | 0.6412 | 0.6717 | 0.8562 | 0.8074 |
| M1 | 0.7669 | 0.7276 | 0.6966 | 0.6950 | 0.8674 | 0.8223 |
| M2 | 0.7247 | 0.7675 | 0.6509 | 0.6548 | 0.8474 | 0.7958 |

M1 的 AUC 接近 Y-K0，但默认 0.5 阈值下 F1 较低，说明需要检查概率校准和阈值偏移，而不能只看 0.5 threshold 的 F1。

## Binary Error Analysis

| 模型 | FP | FN | Mean P(Yes) for Yes | Mean P(Yes) for No | 解释 |
|---|---:|---:|---:|---:|---|
| Base | 3157 | 1383 | 0.6878 | 0.5893 | Base 本身 Yes/No 区分弱 |
| Y-K0 | 2413 | 918 | 0.6891 | 0.4723 | Y 显著压低 No 样本 P(Yes) |
| M0 | 3986 | 156 | 0.6927 | 0.6054 | 明显 Yes 偏置，FP 过高 |
| M1 | 1358 | 2144 | 0.5401 | 0.3830 | Yes 偏置缓解，但 0.5 阈值过保守 |
| M2 | 3858 | 172 | 0.8413 | 0.6966 | 重新出现强 Yes 偏置 |

M1 的概率分布明显比 M0/M2 更健康：No 样本 Mean P(Yes) 从 M0 的 0.6054 降到 0.3830。但 M1 默认 0.5 阈值下 FN 很高，因此必须使用 validation 阈值校准来判断它的实际 preference prediction 能力。

## Threshold Calibration

阈值选择规则：

```text
在 validation 上选择 best-F1 threshold；
将同一个 threshold 应用到 test。
```

| 模型 | threshold | Test AUC | Test F1 | Test Acc | Precision | Recall | FP | FN |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Base | 0.0953 | 0.6205 | 0.7414 | 0.5949 | 0.5952 | 0.9830 | 4561 | 116 |
| Y-K0 | 0.4073 | 0.7691 | 0.7831 | 0.6982 | 0.6807 | 0.9217 | 2950 | 534 |
| M0 | 0.5312 | 0.7234 | 0.7687 | 0.6651 | 0.6494 | 0.9418 | 3469 | 397 |
| M1 | 0.3208 | 0.7669 | 0.7818 | 0.7029 | 0.6906 | 0.9006 | 2752 | 678 |
| M2 | 0.6225 | 0.7247 | 0.7734 | 0.6833 | 0.6700 | 0.9147 | 3074 | 582 |

校准后，M1 的 preference prediction 已经非常接近 Y-K0：

```text
Y-K0 test F1 = 0.7831
M1   test F1 = 0.7818

Y-K0 test AUC = 0.7691
M1   test AUC = 0.7669
```

M1 的 test accuracy 还略高于 Y-K0：

```text
Y-K0 test Acc = 0.6982
M1   test Acc = 0.7029
```

但 M1 的 recall 低于 Y-K0，precision 高于 Y-K0。这说明 M1 不是完全复制 Y-K0，而是在校准后形成了更保守的 Yes/No 边界。

## Ranking 诊断

| 模型 | HR@1 | NDCG@5 | MRR | Mean Margin |
|---|---:|---:|---:|---:|
| Base | 0.3167 | 0.6631 | 0.5525 | -0.0776 |
| Y-K0 | 0.3048 | 0.6504 | 0.5366 | -0.0998 |
| N-K0 | 0.7189 | 0.8773 | 0.8356 | 0.3705 |
| M0 | 0.6717 | 0.8562 | 0.8074 | 0.2936 |
| M1 | 0.6950 | 0.8674 | 0.8223 | 0.3309 |
| M2 | 0.6548 | 0.8474 | 0.7958 | 0.2372 |

M1 比 M0 明显更接近 N-K0：

```text
M0 HR@1 = 0.6717
M1 HR@1 = 0.6950
N-K0 HR@1 = 0.7189
```

M2 的 ranking 全面低于 M0/M1，说明简单提高 Y 采样比例会损害 N 的 next-item prediction 能力。

## 对诊断问题的回答

### 1. M0 是否只是未充分收敛？

很大程度上是。M1 延长训练后：

- M-Y AUC 从 0.7234 提升到 0.7669。
- M-N HR@1 从 0.6717 提升到 0.6950。
- No 样本 Mean P(Yes) 从 0.6054 降到 0.3830。

这说明 M0 的干扰现象不能直接解释为不可缓解的任务冲突。

### 2. 提高 Y 采样比例是否能修复 M-Y？

不能。M2 的 `Y:N=2:1` 没有带来更好的综合结果：

- M2 AUC 仍只有 0.7247，显著低于 M1。
- M2 HR@1 下降到 0.6548。
- M2 的 No 样本 Mean P(Yes) 升到 0.6966，Yes 偏置重新变强。

因此本轮不再继续沿着简单 Y-heavy sampling 扩展。

### 3. 是否存在无法避免的 Y/N 冲突？

当前证据不足以声称存在无法避免的冲突。M1 已经让 M-Y 接近 Y-K0，同时让 M-N 更接近 N-K0。更准确的表述是：

```text
M 仍低于 N-K0 的 ranking 上限，
但 M0 的主要问题已被 M1 证明至少部分来自训练预算和阈值校准。
```

### 4. 当前是否需要继续跑 M3？

不需要。M3 的 `Y:N=1:2` 原本用于在 M1/M2 不能解释时补充 N-heavy 对照。现在 M1/M2 已经给出清晰方向：

- 延长 1:1 训练有效。
- 简单 Y-heavy 无效且损害 N。
- M1 是当前最强 M 版本。

继续跑 M3 的解释价值低于它的 GPU 成本。

## 当前行动建议

1. 把 M1 记录为当前 M 诊断最佳版本。
2. 后续二分类报告同时给出默认 0.5 threshold 和 validation-calibrated threshold，避免混淆模型排序能力与阈值选择。
3. 暂停新的 M 长训练，不启动 M3。
4. 如果继续改进 M，优先做不需要大规模重训的分析，例如按评分、历史长度、候选位置、target rating 和用户活跃度分组的 error analysis。
5. 若必须继续训练，优先围绕 M1 做更小步的训练预算或学习率诊断，而不是新增 Phase 2 模块。

## 结论边界

当前可以说：

```text
M1 显著缓解了 M0 的多任务干扰；
M1 在校准后几乎恢复 Y-K0 的 preference prediction；
M1 的 next-item ranking 明显优于 M0，但仍低于 N-K0；
M2 说明简单提高 Y 采样比例不是有效缓解方案。
```

当前不能说：

```text
M 已经全面超过单任务模型；
M 已经证明产生正迁移；
M2 证明 Y 监督越多越好；
应该进入 KAR / Hard Negative / SASRec / 7B / 多 seed。
```
