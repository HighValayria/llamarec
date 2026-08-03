---
title: MovieLens-1M MVP 主结果报告
type: report
status: current
authority: descriptive
source: mixed
created: 2026-08-02
updated: 2026-08-03
last_verified: 2026-08-03
related_code:
  - configs/experiment.yaml
  - configs/y.yaml
  - configs/n.yaml
  - configs/m.yaml
  - src/analysis/summarize_results.py
  - src/analysis/basic_error_analysis.py
  - src/inference/base_zero_shot.py
  - src/inference/evaluate_y_adapter.py
  - src/inference/evaluate_n_adapter.py
  - src/inference/evaluate_m_adapter.py
  - src/train/train_y.py
  - src/train/train_n.py
  - src/train/train_m.py
---

# MovieLens-1M MVP 主结果报告

## 实验范围

本报告记录当前 MVP 范围内的 MovieLens-1M 主结果：

- Base：不做 recommendation tuning 的 Llama-3.2-3B-Instruct。
- Y-K0：Yes/No Preference Tuning。
- N-K0：Full-sequence Next-item Tuning。
- M-K0：Y + N Multi-task Tuning，分别以 M-Y 与 M-N 接口评测。

当前仍不包含 KAR、SASRec、Hard Negative、Bootstrap、32M 主实验、多 seed 或 LoRA 大规模搜索。

云端对应产物：

```text
outputs/results.csv
outputs/reports/movielens-1m_mvp_report.md
outputs/error_analysis/movielens-1m/test_error_analysis.md
```

## 数据与训练设置

数据集为 MovieLens-1M，核心序列来源为 `full_sequence`。Y/N 划分均遵守严格历史规则：

```text
history = 所有 timestamp < target_timestamp 的 interaction
```

主数据统计：

```text
Y users: 6040
N users: 5675
Y samples: train 976284 / validation 12381 / test 11544
N samples: train 212725 / validation 5675 / test 5675
candidate_num: 5
```

训练预算：

```text
train pool: 200000 samples per single-task model
M train pool: 200000 Y + 200000 N samples
max_steps: 1500
seed: 42
base model: meta-llama/Llama-3.2-3B-Instruct
LoRA: QLoRA / NF4 / r=16 / alpha=32 / dropout=0.05
```

## 主结果

Test split：

| Model | AUC | F1 | Acc | HR@1 | NDCG@5 | MRR |
|---|---:|---:|---:|---:|---:|---:|
| Base | 0.6205 | 0.7055 | 0.6067 | 0.3167 | 0.6631 | 0.5525 |
| Y-K0 | **0.7691** | **0.7800** | **0.7115** | 0.3048 | 0.6504 | 0.5366 |
| N-K0 | - | - | - | **0.7189** | **0.8773** | **0.8356** |
| M-K0 | 0.7234 | 0.7630 | 0.6412 | 0.6717 | 0.8562 | 0.8074 |

Validation split：

| Model | AUC | F1 | Acc | HR@1 | NDCG@5 | MRR |
|---|---:|---:|---:|---:|---:|---:|
| Base | 0.6224 | 0.7092 | 0.6119 | 0.3170 | 0.6643 | 0.5541 |
| Y-K0 | **0.7702** | **0.7802** | **0.7140** | 0.3172 | 0.6578 | 0.5462 |
| N-K0 | - | - | - | **0.7216** | **0.8797** | **0.8387** |
| M-K0 | 0.7209 | 0.7610 | 0.6392 | 0.6747 | 0.8584 | 0.8103 |

HR@5 在当前 5-candidate 设置下没有区分度，因此结论主要依据 AUC、HR@1、NDCG@5 与 MRR。

## 研究问题回答

### RQ1：Recommendation tuning 是否优于 Base LLM？

是，但要按任务接口区分：

- Y-K0 将 test AUC 从 0.6205 提升到 0.7691。
- N-K0 将 test HR@1 从 0.3167 提升到 0.7189。
- M-K0 也显著优于 Base：test AUC 为 0.7234，test HR@1 为 0.6717。

因此，recommendation tuning 对显式偏好判断和 next-item ranking 都有明显收益。

### RQ2：显式偏好监督 Y 与序列行为监督 N 分别学到什么？

Y-K0 主要学习 preference boundary。它显著提升 binary metrics，但不提升 next-item ranking：

```text
Base HR@1: 0.3167
Y-K0 HR@1: 0.3048
```

这说明 `P(Like | History, Item)` 不能直接替代 `P(Next Item | History, Candidate Set)`。

N-K0 主要学习 behavioral sequence prediction。它在 ranking 指标上远高于 Base 和 Y-K0：

```text
N-K0 HR@1: 0.7189
N-K0 NDCG@5: 0.8773
N-K0 MRR: 0.8356
```

### RQ3：N 是否能够提升候选 Next-item Prediction？

是。N-K0 是当前 next-item ranking 的最强模型。Error analysis 中 N-K0 的 mean margin 为正：

```text
Base mean margin: -0.0776
N-K0 mean margin: 0.3705
```

这表示 N-K0 通常能把 ground truth candidate 推到最强负候选前面。

### RQ4：Y + N 联合训练是否产生正迁移？

当前结果更接近“互补但有折中”，不是超过单任务最优的正迁移。

M-K0 同时保持了较强的 binary 和 ranking 能力：

```text
M-K0 AUC: 0.7234
M-K0 HR@1: 0.6717
```

但 M-K0 的 binary 不如 Y-K0，ranking 不如 N-K0：

```text
Y-K0 AUC: 0.7691 > M-K0 AUC: 0.7234
N-K0 HR@1: 0.7189 > M-K0 HR@1: 0.6717
```

因此当前不能声称 M 超越单任务最优，只能说 M 在同一模型中保留了两类能力。

### RQ5：M 是否能够同时保持偏好判断能力和序列预测能力？

能够部分保持。M-K0 的两个接口都显著优于 Base，但存在多任务干扰迹象：

- M-Y 的 AUC 明显低于 Y-K0。
- M-N 的 HR@1 明显低于 N-K0。
- M-Y 的 false positive 较高，显示出偏向 Yes 的倾向。

## 基础 Error Analysis

Binary test：

| Model | FP | FN | Mean P(Yes) for Yes | Mean P(Yes) for No |
|---|---:|---:|---:|---:|
| Base | 3157 | 1383 | 0.6878 | 0.5893 |
| Y-K0 | 2413 | 918 | 0.6891 | 0.4723 |
| M-K0 | 3986 | 156 | 0.6927 | 0.6054 |

Y-K0 的主要改进来自降低 No 样本的 `P(Yes)`，从而改善 preference boundary。

M-K0 的 FN 很低但 FP 很高，说明 M-Y 接口明显偏向 Yes。后续若优化 M，应优先检查任务混合比例、任务前缀、label prior 和 loss mask，而不是直接添加 Phase 2 模块。

Ranking test：

| Model | HR@1 | Mean Margin | Rank Distribution |
|---|---:|---:|---|
| Base | 0.3167 | -0.0776 | 1:1797 / 2:1247 / 3:1108 / 4:822 / 5:701 |
| Y-K0 | 0.3048 | -0.0998 | 1:1730 / 2:1201 / 3:928 / 4:838 / 5:978 |
| N-K0 | 0.7189 | 0.3705 | 1:4080 / 2:947 / 3:364 / 4:213 / 5:71 |
| M-K0 | 0.6717 | 0.2936 | 1:3812 / 2:1094 / 3:432 / 4:231 / 5:106 |

N-K0 和 M-K0 的 predicted position distribution 较均匀，没有明显固定候选位置偏置。

## 当前结论边界

这是一轮单 seed、固定 1500 steps、200k pool 的 MVP 结果。它足以判断任务方向，但不应包装为最终论文完整实验矩阵。

当前可支持的结论：

- Y supervision 对 preference prediction 有显著帮助。
- N supervision 对 next-interaction candidate ranking 有显著帮助。
- Y 与 N 的监督语义不同，Y 的 `P(Yes)` 排序不能替代 N ranking。
- M 能同时获得两类能力，但当前不是单任务最优。

当前不应声称：

- M 已产生超过单任务的正迁移。
- HR@5 有实际区分力。
- 当前结果已经完成多 seed 稳健性验证。
- 32M 上也会完全复现当前趋势。

## 下一步建议

优先级从高到低：

1. 保留当前 1M 结果为 MVP 主结果，停止无目标扩展。
2. 将原“实现 Y/N/M 主流程”的任务标记为完成。
3. M 多任务干扰诊断第一轮已经完成，当前结论见 [M 多任务干扰诊断结果](m_multitask_interference_diagnosis_results.md)。
4. 暂停 M3 和新的长训练，不启动 KAR、SASRec、Hard Negative、32M full training、多 seed 或 7B。
5. 下一步优先做轻量分组 error analysis，并评估是否可以仅重新生成更大的固定 validation/test candidate set，例如 candidate_num=20 或 50，然后不重训模型直接推理。

## M 多任务干扰诊断矩阵

当前 M0 作为 baseline，不重新定义：

```text
M0:
Y:N train pool = 200k:200k
max_steps = 1500
```

第一轮 M 诊断已经完成：

| 实验 | Y:N ratio | max_steps | 目的 |
|---|---:|---:|---|
| M1 | 1:1 | 3000 | 已完成，显著缓解 M0，当前最佳 M 诊断版本 |
| M2 | 2:1 | 1500 | 已完成，未缓解干扰且损害 N |
| M3 | 1:2 | - | 不启动 |

M1 的 validation best-F1 threshold 为 0.3208213008。应用到 test 后，M1 F1=0.7818、Accuracy=0.7029，已经接近 Y-K0；M1 ranking 的 HR@1=0.6950，明显优于 M0 但仍低于 N-K0。

若后续继续 M 训练，仍必须分别记录 Y validation 和 N validation，不能只看混合总 loss。

统一比较表至少包含：

```text
Experiment
Y:N ratio
max_steps
Y AUC / F1 / Acc
Y FP / FN
Mean P(Yes) for Yes
Mean P(Yes) for No
N HR@1 / NDCG@5 / MRR
N mean margin
```

解释时需要区分：

- 未收敛：增加 steps 后 Y/N 同时改善。
- 任务失衡：调整 sampling ratio 后一个任务明显恢复。
- 梯度或能力冲突：一个任务改善会稳定损害另一个任务。
- 灾难性遗忘：按任务顺序训练时，后一个任务覆盖前一个任务。
- 未来信息泄漏：训练样本越过 validation/test 时间边界。

本轮 M 实验仍应采用混合或交替训练。如果后续做“先 Y 后 N”，只能称为 sequential fine-tuning，不能称为 multi-task joint training。
