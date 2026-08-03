---
title: MVP 执行历程、当前现状与主要发现
type: report
status: current
authority: descriptive
source: mixed
created: 2026-08-03
updated: 2026-08-03
last_verified: 2026-08-03
related_code:
  - task.md
  - README.md
  - configs/experiment.yaml
  - configs/y.yaml
  - configs/n.yaml
  - configs/m.yaml
  - src/data/build_step2.py
  - src/eval/candidate_sets.py
  - src/inference/base_zero_shot.py
  - src/inference/evaluate_y_adapter.py
  - src/inference/evaluate_n_adapter.py
  - src/inference/evaluate_m_adapter.py
  - src/train/train_y.py
  - src/train/train_n.py
  - src/train/train_m.py
  - src/analysis/summarize_results.py
  - src/analysis/basic_error_analysis.py
  - src/analysis/threshold_calibration.py
---

# MVP 执行历程、当前现状与主要发现

## 目的

本文汇总当前 LlamaRec MVP 从任务冻结到 MovieLens-1M 主结果与 M 多任务诊断的执行历程、当前项目状态和主要发现。它面向后续接手开发、写实验报告或决定 Phase 2 的读者。

更细节的结果见：

- [MovieLens-1M MVP 主结果报告](movielens_1m_mvp_results.md)
- [M 多任务干扰诊断结果](m_multitask_interference_diagnosis_results.md)
- [当前项目状态](../current_state.md)

## 当前任务范围

当前 MVP 只包含 K0 实验，不包含知识增强或复杂推荐模块：

| 名称 | 含义 | 训练目标 | 评测接口 |
|---|---|---|---|
| Base | 不做 recommendation tuning 的 Llama-3.2-3B-Instruct | 无微调 | Y 与 N 两类 zero-shot 打分 |
| Y-K0 | Yes/No Preference Tuning | `P(Like | History, Item)` | Yes/No binary 与用 `P(Yes)` 排候选 |
| N-K0 | Full-sequence Next-item Tuning | `P(Next Item | History, Candidate Set)` | `P(A)...P(E)` ranking |
| M-K0 | Y + N Multi-task Tuning | 同一模型联合学习 Y 与 N | M-Y binary 与 M-N ranking |

`K0` 表示当前不加入 knowledge augmentation。KAR、SASRec、Hard Negative、Bootstrap、7B、多 seed、32M full training 等都属于 Phase 2 或更晚阶段。

## 执行历程

### 1. 任务冻结与命名迁移

项目最初围绕 Base、Y、R、M 组织。后来正式迁移为：

```text
Y = Yes/No Preference Prediction
N = Full-sequence Next-item Prediction
M = Y + N Multi-task
```

关键变化是：N 不再预测“下一个正反馈物品”，而是预测完整交互序列中真实发生的下一次 interaction。即使下一次 interaction 的评分较低，它仍然是 N 的 ground truth。

因此当前的核心区别是：

```text
Y = preference prediction
N = behavioral sequence prediction
```

N 的 ranking metrics 衡量“真实下一次交互是否排前”，不直接等价于“喜欢程度排序”。

### 2. 数据切分和无泄漏规则确定

当前统一使用 `full_sequence` 作为 MVP 核心数据来源。严格历史规则为：

```text
history = 所有 timestamp < target_timestamp 的 interaction
```

同一 timestamp 内没有可观测先后顺序，因此不能用文件顺序、movie_id 或排序后行号伪造顺序。

timestamp tie 的最终处理方式：

- Y 可以在同一 timestamp bucket 内产生多个 target，这些 target 共享同一份严格 history。
- N 只构造严格可确定的 next-item sample；如果下一 timestamp bucket 含有多个 interaction，则跳过该 N sample，而不是跳过整个 user。

M 的无泄漏规范是：

```text
Raw interactions
-> chronological split
-> Y_train / N_train
-> multi-task training
```

禁止先从完整数据生成所有 Y/N 样本后再混合训练，因为这样可能让某个任务的训练样本包含另一个任务 validation/test 时间边界之后的信息。

### 3. STEP 1-3：配置、数据层、固定候选集

先建立统一实验配置，再构建 MovieLens 数据层和固定 candidate set。候选集规则为：

```text
1 ground-truth item + 4 random candidates
candidate_num = 5
```

Base、Y、N、M 后续评测都读取同一固定 validation/test candidate set，不在模型评测时重新采样。

MovieLens-1M 当前主数据统计：

```text
Y users: 6040
N users: 5675
Y samples: train 976284 / validation 12381 / test 11544
N samples: train 212725 / validation 5675 / test 5675
valid candidates: 5675 records
test candidates: 5675 records
candidate_num: 5
```

### 4. STEP 4：Base LLM Zero-shot

Base 不做 recommendation tuning。实现了两个推理接口：

```text
score_yesno()      -> P(Yes), P(No)
score_candidates() -> P(A), P(B), P(C), P(D), P(E)
```

过程中确认 Llama-3.2-3B-Instruct 的 `Yes`、`No`、`A`、`B`、`C`、`D`、`E` 均为单 token，因此可以使用单 token logits 做连续打分。

Base 在 MovieLens-1M test 上的表现：

```text
Binary AUC = 0.6205
Binary F1  = 0.7055
HR@1       = 0.3167
NDCG@5     = 0.6631
MRR        = 0.5525
```

### 5. STEP 5：Y-K0

Y-K0 构造：

```text
history + target movie -> Yes / No
```

训练链路完成了 smoke test、adapter 保存、adapter 重载、Y binary 评测和用 `P(Yes)` 对 N 固定候选集排序的评测。

MovieLens-1M test 主结果：

```text
AUC  = 0.7691
F1   = 0.7800
Acc  = 0.7115
HR@1 = 0.3048
```

Y-K0 明显提升 preference prediction，但不能提升 next-item ranking。

### 6. STEP 6：N-K0

N-K0 构造：

```text
history + candidate set -> 实际发生的下一个 item label
```

训练目标是正确候选标签，例如 `A` 到 `E`，不人为定义负候选之间的完整排序。

MovieLens-1M test 主结果：

```text
HR@1   = 0.7189
NDCG@5 = 0.8773
MRR    = 0.8356
```

N-K0 是当前 next-item ranking 的最强单任务模型。

### 7. STEP 7：M-K0

M-K0 使用同一模型联合学习 Y 和 N，默认采用 Y/N 混合或交替训练，并分别以 M-Y 和 M-N 两个接口评测。

M0 是 MVP 主结果中的原始 M baseline：

```text
Y:N train pool = 200k:200k
max_steps = 1500
```

M0 MovieLens-1M test 主结果：

```text
AUC    = 0.7234
F1     = 0.7630
Acc    = 0.6412
HR@1   = 0.6717
NDCG@5 = 0.8562
MRR    = 0.8074
```

M0 同时优于 Base，但低于 Y-K0 和 N-K0，说明它保留了两类能力，但还不是超过单任务模型的正迁移。

### 8. STEP 8：统一评测和基础 Error Analysis

统一生成了：

```text
outputs/results.csv
outputs/reports/movielens-1m_mvp_report.md
outputs/error_analysis/movielens-1m/test_error_analysis.md
```

基础 error analysis 发现，M0 的 M-Y 接口存在明显 Yes 偏置：

```text
M0 test FP = 3986
M0 test FN = 156
Mean P(Yes) for Yes = 0.6927
Mean P(Yes) for No  = 0.6054
```

这促使项目从“验证 Y/N/M 是否有效”转向“诊断并缓解 Y/N 多任务干扰”。

### 9. M 多任务干扰诊断

第一轮 M 诊断已经完成：

| 实验 | 设置 | 状态 | 结论 |
|---|---|---|---|
| M0 | 1:1，200k Y + 200k N，1500 steps | 已完成 | MVP baseline，有 Yes 偏置 |
| M1 | 1:1，200k Y + 200k N，3000 steps | 已完成 | 当前最佳 M 诊断版本 |
| M2 | 2:1，200k Y + 100k N，1500 steps | 已完成 | 未缓解干扰且损害 N |
| M3 | 1:2 | 不启动 | 当前解释收益不足 |

M1 默认 0.5 threshold 下：

```text
AUC    = 0.7669
F1     = 0.7276
Acc    = 0.6966
HR@1   = 0.6950
NDCG@5 = 0.8674
MRR    = 0.8223
```

M1 使用 validation best-F1 threshold 后：

```text
threshold = 0.3208213008
test F1   = 0.7818
test Acc  = 0.7029
```

这说明默认 0.5 threshold 低估了 M1 的 binary 能力。M1 在校准后接近 Y-K0，同时 M-N 明显优于 M0，但仍低于 N-K0。

M2 的结果表明，简单提高 Y 采样比例不是有效方案：

```text
M2 AUC    = 0.7247
M2 HR@1   = 0.6548
M2 No 样本 Mean P(Yes) = 0.6966
```

## 当前现状

### 代码链路

当前已经具备从数据处理到训练评测的 MVP 主链路：

- `src.data.build_step2`：MovieLens full-sequence 数据层、Y/N 样本构造和统计。
- `src.eval.candidate_sets`：固定 N candidate set。
- `src.inference.base_zero_shot`：Base zero-shot Y/N 推理。
- `src.train.train_y`、`src.train.train_n`、`src.train.train_m`：Y/N/M QLoRA 训练入口。
- `src.inference.evaluate_y_adapter`、`src.inference.evaluate_n_adapter`、`src.inference.evaluate_m_adapter`：adapter 评测入口。
- `src.analysis.summarize_results`：结果汇总表。
- `src.analysis.basic_error_analysis`：基础错误分析。
- `src.analysis.threshold_calibration`：Y/M-Y 二分类阈值校准。

### 数据集状态

MovieLens-100K：

- 用于开发、smoke test 和流程验证。
- Base/Y/N/M 预算实验已经跑通。

MovieLens-1M：

- 当前 MVP 主结果数据集。
- STEP 2/3/Base/Y/N/M/统一评测/M 诊断均已完成。

MovieLens-32M：

- 已生成 eval-only 产物，并完成 Base validation/test 全量评测。
- 因运行成本过高，暂停作为当前主线，保留为 Phase 2 或压力测试候选。

### 当前最佳结果视图

| 模型 | Binary AUC | Binary F1 | Binary Acc | HR@1 | NDCG@5 | MRR | 说明 |
|---|---:|---:|---:|---:|---:|---:|---|
| Base | 0.6205 | 0.7055 | 0.6067 | 0.3167 | 0.6631 | 0.5525 | 无微调 |
| Y-K0 | 0.7691 | 0.7800 | 0.7115 | 0.3048 | 0.6504 | 0.5366 | preference 最强单任务 |
| N-K0 | - | - | - | 0.7189 | 0.8773 | 0.8356 | ranking 最强单任务 |
| M0 | 0.7234 | 0.7630 | 0.6412 | 0.6717 | 0.8562 | 0.8074 | MVP 原始 M baseline |
| M1 | 0.7669 | 0.7818 | 0.7029 | 0.6950 | 0.8674 | 0.8223 | 当前最佳 M 诊断版本，binary 为校准后结果 |
| M2 | 0.7247 | 0.7734 | 0.6833 | 0.6548 | 0.8474 | 0.7958 | Y-heavy，无效且损害 N |

M1 是诊断阶段的 best M run。写论文或主报告时，应明确区分：

```text
M0 = 原 MVP 主实验 baseline
M1 = M 干扰诊断后得到的 better M run
```

## 主要发现

### 发现 1：Recommendation tuning 明显优于 Base

Y-K0 和 N-K0 都显著优于 Base：

```text
Base AUC 0.6205 -> Y-K0 AUC 0.7691
Base HR@1 0.3167 -> N-K0 HR@1 0.7189
```

这说明 LLM 可以通过轻量 LoRA/QLoRA recommendation tuning 学到任务相关的偏好判断和行为序列预测能力。

### 发现 2：Y 和 N 学到的是不同东西

Y-K0 提升 binary preference prediction，但不提升 next-item ranking：

```text
Base HR@1 = 0.3167
Y-K0 HR@1 = 0.3048
```

N-K0 明显提升 next-item ranking，但它的语义不是“喜欢程度排序”，而是“下一次真实交互排序”。

因此不能把 `P(Yes)` 直接当作 N 的候选排序分数，也不能把 N 的 NDCG 解释为喜欢程度排序。

### 发现 3：M 可以保留双能力，但原始 M0 存在干扰

M0 同时优于 Base：

```text
M0 AUC  = 0.7234 > Base 0.6205
M0 HR@1 = 0.6717 > Base 0.3167
```

但 M0 低于对应单任务模型：

```text
M0 AUC  = 0.7234 < Y-K0 0.7691
M0 HR@1 = 0.6717 < N-K0 0.7189
```

所以当前不能声称 M0 产生了超过单任务的正迁移。更准确的表述是：M0 在同一模型中保留两类能力，但存在多任务折中。

### 发现 4：M0 的问题部分来自训练预算与阈值偏移

M1 延长训练后显著改善：

```text
M0 AUC 0.7234 -> M1 AUC 0.7669
M0 HR@1 0.6717 -> M1 HR@1 0.6950
M0 No 样本 Mean P(Yes) 0.6054 -> M1 0.3830
```

M1 校准后 F1=0.7818，已经接近 Y-K0 的 0.7831。这说明 M0 的干扰现象不能简单归因于不可缓解的任务冲突。

### 发现 5：简单提高 Y 采样比例不是有效方案

M2 使用 `Y:N=2:1` 后：

- AUC 仍明显低于 M1。
- HR@1 低于 M0/M1。
- No 样本 Mean P(Yes) 升到 0.6966，Yes 偏置重新变强。

因此后续不应继续沿着“更多 Y 样本就更好”的方向盲目扩展。

### 发现 6：阈值校准对 M-Y 解释非常重要

M1 默认 0.5 threshold 下 F1=0.7276，但 validation-calibrated threshold 后 F1=0.7818。这里的差距说明：

```text
AUC / 排序能力
和
固定阈值下的分类表现
必须分开解释。
```

后续报告 binary metrics 时，建议同时保留：

- 默认 0.5 threshold。
- validation best-F1 threshold。
- AUC。
- precision / recall / FP / FN。

### 发现 7：candidate_num=5 限制了 ranking 解释力

当前候选集为 1 个 ground truth + 4 个随机候选，因此：

```text
HR@5 恒为 1.0
```

ranking 结论应主要看：

- HR@1
- NDCG@5
- MRR
- mean margin
- rank distribution

若要进一步增强 ranking 结论，可以优先生成 candidate_num=20 或 50 的固定 validation/test candidate set，并在不重训模型的情况下重新推理。

## 当前不应推进的方向

在当前结论整理与轻量诊断完成前，不建议启动：

- KAR knowledge augmentation
- SASRec
- Hard Negative
- Bootstrap
- MovieLens-32M full training
- 7B 模型
- 多 seed
- 大规模 LoRA 超参数搜索

这些方向不是被否定，而是当前解释收益低于成本。先把 1M 上的主结果、M1 诊断和错误模式讲清楚更重要。

## 建议的下一步

优先级从高到低：

1. 基于现有 prediction 文件做分组 error analysis：target rating、用户历史长度、用户活跃度、候选位置、是否低分 next interaction。
2. 在报告中明确区分 M0 baseline 与 M1 diagnostic best run。
3. 为 binary metrics 同时报告 AUC、0.5 threshold 和 validation-calibrated threshold。
4. 考虑不重训模型，生成更大 candidate set 做 ranking robustness check。
5. 只有当分组诊断无法解释剩余差距时，再决定是否继续训练或进入 Phase 2。

## 当前结论边界

可以支持的表述：

```text
Y-K0 显著提升 preference prediction。
N-K0 显著提升 full-sequence next-item prediction。
Y 和 N 的监督语义不同，不能互相替代。
M0 同时获得两类能力，但存在多任务折中。
M1 显著缓解 M0 的干扰，并在校准后接近 Y-K0 的 binary 表现。
M1 的 ranking 仍低于 N-K0。
```

不应支持的表述：

```text
M 已经全面超过单任务模型。
M 已经证明产生正迁移。
N 的 ranking 等价于喜欢程度排序。
Y 的 P(Yes) 可以替代 N candidate probability。
当前结果已经完成多 seed 稳健性验证。
32M 上必然复现 1M 结论。
```
