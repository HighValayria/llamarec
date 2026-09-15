---
title: "00 project map"
type: report
status: current
authority: descriptive
source: agent
created: 2026-08-23
updated: 2026-08-23
last_verified: 2026-08-23
related_code:
  - configs/experiment.yaml
  - src/data/build_step2.py
  - src/data/split.py
  - src/data/build_preference.py
  - src/data/build_next_item.py
  - src/eval/candidate_sets.py
  - src/eval/ranking_metrics.py
  - src/eval/binary_metrics.py
  - src/train/train_y.py
  - src/train/train_n.py
  - src/train/train_m.py
  - src/inference/scoring.py
  - src/inference/evaluate_y_adapter.py
  - src/inference/evaluate_n_adapter.py
  - src/inference/evaluate_m_adapter.py
---
# 00 Project Map

## 一句话主线

[FACT] LlamaRec 研究的是：推荐里的“喜欢一个 item”和“下一次真实交互哪个 item”不是同一个能力，Y/N/M 三种监督用同一个 Llama adapter 框架检验这种语义差异，并用 PopMatch、SASRec、sample exposure、multi-seed 和 Amazon 复核结论边界。

## ASCII 主线图

```text
Raw Interaction Data
       |
       v
Strict Temporal Protocol
history = timestamp < target timestamp
       |
       v
 +-------------+---------------+--------------+
 |             |               |              |
 v             v               v              |
Y-K0          N-K0            M1              |
Preference    Next-item       Y + N           |
P(Yes)        candidate label  mixed adapter   |
 |             |               |              |
 +-------------+---------------+--------------+
                 |
                 v
              Evaluation
                 |
      +----------+-----------+
      |          |           |
      v          v           v
   Binary     Ranking     Robustness
   AUC/F1     HR/NDCG/MRR Random / PopMatch / k20 / k50
                           |
                           v
                    Baseline Comparison
                           |
              +------------+------------+
              |            |            |
              v            v            v
          Popularity      BPR-MF       SASRec
                                            |
                                            v
                                 Fair Sample Exposure
                                            |
                                 +----------+---------+
                                 |                    |
                                 v                    v
                         Multi-seed Stability   Amazon Cross-dataset
```

## 节点解释

Raw Interaction Data:
[FACT] 输入是用户-item-rating-timestamp 序列。MovieLens-1M 是主数据集，Amazon Musical Instruments 是第二数据集。Amazon 只使用 interaction `user_id/parent_asin/rating/timestamp` 和 metadata `parent_asin/title`。

Strict Temporal Protocol:
[FACT] 所有任务都遵守 `history = timestamp < target_timestamp`。这一步回答“有没有未来泄漏”和“同 timestamp 没有真实顺序怎么办”。

Y-K0:
[FACT] 把历史和 target item 转成 Yes/No preference 样本，`rating >= 4 -> Yes`。它回答“微调能不能让 LLM 更会判断用户是否喜欢某个 item”。

N-K0:
[FACT] 把历史和候选集合转成 next interaction 选择题，答案是 A/B/C/D/E 中真实下一次交互对应的 label。它回答“微调能不能让 LLM 更会预测下一次真实交互”。

M1:
[FACT] 一个 adapter 同时吃 Y 和 N，1:1 ratio interleaving。它回答“能不能用一个统一模型同时承担 preference 和 next-item ranking”。

Binary Evaluation:
[FACT] 用 AUC、Accuracy、F1、validation-calibrated F1 看 Yes/No preference。它回答“Y/M 的偏好判断是否可靠”。

Ranking Evaluation:
[FACT] 用 HR@1、NDCG@5、MRR 看真实 next interaction 在候选里的排序。它回答“模型能否把真实下一次交互排到前面”。

Robustness:
[FACT] Random-k5、PopMatch-k5、k20/k50、candidate order perturbation 检查结论是不是只依赖容易候选或固定位置。它回答“ranking 结果会不会是 candidate protocol 的假象”。

Popularity / BPR-MF / SASRec:
[FACT] baseline 检查 LLM ranking 是否只是 popularity shortcut，或者是否不如专门的序列推荐模型。

Fair Sample Exposure:
[FACT] SASRec 1500 optimizer steps 和 N-K0 1500 optimizer steps不是同一个样本曝光预算。它回答“比较是不是公平”。

Multi-seed:
[FACT] MovieLens seeds 42/43/44 固定 PopMatch candidate，改变训练 seed。它回答“主方向是不是 seed42 偶然结果”。

Amazon Cross-dataset:
[FACT] Amazon Musical Instruments seed42 复核 MovieLens 方向。它回答“是不是只在 MovieLens 成立”。边界是 Amazon 不是 multi-seed。

## 核心矛盾

[INTERPRETATION] 如果一个 LLM 能判断用户喜欢某电影，并不等于它能预测用户下一次会点哪部电影。偏好是属性判断，next interaction 是序列行为预测。LlamaRec 的贡献是把这两个常被混在一起的推荐目标拆开，用同一个模型框架、同一套 temporal protocol、同一批 hard-candidate/baseline 诊断去看它们到底学到什么。

## 面试主线

先讲问题：
“推荐能力不是单一能力。喜欢预测和下一次交互预测语义不同。”

再讲方法：
“我构造 Y、N、M 三种监督：Y 是 Yes/No preference，N 是 candidate-label next interaction，M 是 Y/N 混合。”

再讲验证：
“用 PopMatch 控制 popularity shortcut，用 k20/k50 增加候选难度，用 SASRec 和 sample exposure 做公平 baseline 定位，用 multi-seed 和 Amazon 看稳定性和外部有效性。”

最后讲边界：
“M1 是 unified tradeoff，不是 positive transfer；N-K0 在 closest exposure 下更强，远多监督的 SASRec 可以超过当前低曝光 N-K0；Amazon 目前是 seed42 directional replication。”
