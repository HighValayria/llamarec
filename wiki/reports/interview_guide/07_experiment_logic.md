---
title: "07 experiment logic"
type: report
status: current
authority: descriptive
source: agent
created: 2026-08-24
updated: 2026-08-24
last_verified: 2026-08-24
related_code:
  - src/analysis/phase2b_result_synthesis.py
  - src/analysis/phase2c_result_summary.py
  - src/analysis/sample_efficiency_curve.py
  - src/analysis/multiseed_stability_summary.py
---

# 07 Experiment Logic

## 读实验的固定模板

每个实验都按这个顺序讲：

```text
Experiment -> Motivation -> Design -> Result -> Interpretation -> Boundary
```

## 1. Base vs Y-K0

Motivation:

```text
Preference tuning 是否有效？
```

Design:

```text
Base: no tuning
Y-K0: Yes/No preference tuning
metric: binary AUC/F1
```

Result:

[FACT] MovieLens Y-K0 validation-calibrated binary F1 `0.7831`，Base F1 `0.7414`。

Interpretation:

[INTERPRETATION] Y-style supervision 确实提升 preference prediction。

Boundary:

```text
这不等于 Y-K0 擅长 next-item ranking
```

## 2. Base vs N-K0

Motivation:

```text
Next-item tuning 是否有效？
```

Design:

```text
Base candidate-label scoring vs N-K0 candidate-label adapter
fixed candidate files
ranking metrics
```

Result:

[FACT] MovieLens PopMatch Base HR@1 `0.3149`，N-K0 `0.5447`。

Interpretation:

[INTERPRETATION] N-style supervision 提升 next-interaction ranking。

## 3. Y-K0 ranking vs N-K0

Motivation:

```text
Preference score 能不能直接替代 next-item score？
```

Design:

```text
Y-K0: 用 P(Yes) 给 candidates 排序
N-K0: 用 candidate label probability 排序
同一 PopMatch candidate file
```

Result:

[FACT] MovieLens PopMatch Y-K0 HR@1 `0.1854`，N-K0 `0.5447`。

Interpretation:

[INTERPRETATION] `P(Like)` 和 `P(Next Interaction)` 是不同语义。

## 4. N-K0 vs M1

Motivation:

```text
统一模型会不会损失 specialist 能力？
```

Design:

```text
N-K0: ranking specialist
M1: Y/N 1:1 multi-task adapter
```

Result:

[FACT] MovieLens PopMatch N-K0 HR@1 `0.5447`，M1 `0.5244`。Multi-seed 下 N-K0 始终高于 M1。

Interpretation:

[INTERPRETATION] M1 是 unified tradeoff，不是 positive transfer。

## 5. M0 -> M1

Motivation:

```text
早期 multi-task 表现差，到底是任务冲突还是 budget 不公平？
```

Design:

```text
从早期 M0 诊断转向 M1 1:1 Y/N exposure 控制
```

Interpretation:

[INTERPRETATION] 不能把 M0 差直接解释成任务天然冲突；M1 说明更公平的混合设置能保住两类能力。

Boundary:

```text
当前支持 tradeoff，不支持 M1 超越 specialist
```

## 6. Candidate order perturbation

Motivation:

```text
LLM 是否对 candidate position 有偏置？
```

Design:

```text
保留 candidates ids，重新打乱 label/order
```

Result:

[FACT] k20 最大绝对 HR@1 delta 约 `0.0065`。

Interpretation:

[INTERPRETATION] candidate order 有影响，但相对 candidate-size stress 小。

## 7. k5 -> k20 -> k50

Motivation:

```text
候选数量增加是否暴露更真实排序难度？
```

Design:

```text
candidate count 5, 20, 50
same ranking metrics
```

Result:

[FACT] MovieLens k50 N-K0 HR@1 `0.1995`，M1 `0.1219`。

Interpretation:

[INTERPRETATION] candidate-size expansion 是强 stressor，且 N-K0 对 M1 优势变大。

## 8. Random-k5 -> PopMatch-k5

Motivation:

```text
Random negatives 是否太容易？Popularity shortcut 是否污染 ranking？
```

Design:

```text
Random-k5 vs popularity-matched negatives
same target N samples
```

Result:

[FACT] MovieLens random test popularity gap 约 `663.6`，PopMatch `44.0`。

Interpretation:

[INTERPRETATION] PopMatch 更适合作主 ranking evidence。

## 9. Popularity / BPR-MF

Motivation:

```text
LLM 是否只是靠 item popularity 或简单协同过滤？
```

Result:

[FACT] BPR-MF Random-k5 HR@1 `0.5611`，PopMatch HR@1 `0.3352`。

Interpretation:

[INTERPRETATION] Random-k5 有明显 shortcut；PopMatch 下 Popularity/BPR 不能解释 N-K0 表现。

## 10. SASRec

Motivation:

```text
强 sequence recommender 能否超过 LLM next-item adapter？比较是否公平？
```

Design:

```text
same PopMatch candidates
step-aligned rows
sample-exposure matched rows
high-exposure anchors
```

Result:

[FACT] MovieLens closest exposure：N-K0 `0.5466`，SASRec `0.2700`。SASRec s3000 在约 `1.53M` exposure 下是 `0.6243`，高于当前约 `12k` exposure 的 N-K0。

Interpretation:

[INTERPRETATION] LLM-vs-SASRec 支持 sample-efficiency 结论，不支持 universal winner，也不支持双方 high-exposure 对齐后的强弱结论。

## 11. Cold/tail diagnostic

Motivation:

```text
SASRec high-exposure anchor 相对当前 N-K0 的优势来自 cold/tail 还是 head/middle？
```

Result:

[FACT] coldest bucket `<=10` 只有 26 samples；SASRec high-exposure anchor 相对当前 N-K0 的优势主要在 middle/head buckets。

Boundary:

```text
不能说 LLM 已证明擅长 cold-start
```

## 12. Multi-seed

Motivation:

```text
seed42 是否偶然？
```

Result:

[FACT] MovieLens seeds 42/43/44 下 N-K0 > M1，N-K0 > SASRec exp-match，SASRec high > current N-K0(12k exposure)。

Boundary:

```text
不是显著性检验，不是 compute-matched claim
```

## 13. Amazon cross-dataset

Motivation:

```text
MovieLens-only 外部有效性不足
```

Result:

[FACT] Amazon PopMatch N-K0 `0.4669`，M1 `0.4582`，SASRec-exp `0.1757`。

Boundary:

```text
seed42 only；N-K0 over M1 margin small
```
