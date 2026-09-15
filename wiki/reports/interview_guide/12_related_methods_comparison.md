---
title: "12 related methods comparison"
type: report
status: current
authority: descriptive
source: agent
created: 2026-08-24
updated: 2026-08-24
last_verified: 2026-08-24
related_code:
  - configs/experiment.yaml
  - src/inference/prompts.py
  - src/train/train_y.py
  - src/train/train_n.py
  - src/train/train_m.py
  - src/baselines/sasrec.py
---

# 12 Related Methods Comparison

## 一句话定位

[INTERPRETATION] 本项目不是发明新推荐架构，而是把 LLM recommendation 里的 supervision semantics 拆清楚：TALLRec 更接近 Y-style preference tuning，LLMRank 更偏 zero-shot ranking factor analysis，SASRec 是 specialized sequence baseline。

## TALLRec vs 本项目

TALLRec 主要做什么：

```text
把 recommendation 转成 instruction-following / Yes-No preference style task
用 LLM 微调做推荐判断
```

本项目继承什么：

```text
Y-K0 的 Yes/No preference interface
history + target item -> Yes/No
```

本项目新增什么：

```text
N-K0: full-sequence next-interaction candidate-label task
M1: Y/N multi-task tradeoff
PopMatch/k20/k50 robustness
sample-exposure-aware SASRec comparison
multi-seed + Amazon validation
```

关键区别：

```text
TALLRec-style Yes/No 不等于 next-item prediction
```

面试句：

> 我不是只复现 TALLRec 的 Yes/No 设定，而是把 Yes/No preference 和 next-interaction candidate prediction 拆开比较。

## LLMRank vs 本项目

LLMRank 主要研究：

```text
LLM zero-shot ranking
candidate order
history presentation
popularity / item information 等因素
```

本项目相似处：

```text
candidate order perturbation
candidate size stress
popularity/hard candidate protocol
LLM ranking behavior analysis
```

本项目不同处：

```text
核心不是 zero-shot ranking factor analysis
而是 tuning supervision semantics:
Y-style preference vs N-style next interaction vs M-style multi-task
```

已做的类似分析：

```text
candidate order
candidate size k20/k50
popularity control PopMatch
hard candidate comparison
```

未系统做：

```text
history shuffle
history length ablation
heterogeneous multi-recall candidates
bootstrap aggregation
text-information ablation
```

面试句：

> LLMRank 更像研究 LLM 在 ranking prompt 里的行为因素；我的项目问题已经变成“不同监督语义会让 tuned LLM 学到什么能力”。

## SASRec vs LLM adapter

SASRec:

```text
architecture: self-attention sequence recommender
input: item ID sequence
representation: learned item embeddings
pretraining: none / task-specific recommender training
scoring: item/candidate scores from sequence model
strength: high-exposure sequential supervision 下很强
```

LLM adapter:

```text
architecture: pretrained causal LM + LoRA adapter
input: natural-language prompt with titles/history
representation: pretrained language features + adapter
scoring: answer token probabilities
strength: closest N-task sample exposure 下更 sample-efficient
```

关键结论：

```text
N-K0 stronger at closest N-task sample exposure
SASRec stronger at high sequential exposure
```

## Popularity / BPR-MF vs LLM

Popularity:

```text
只测热门程度 shortcut
```

BPR-MF:

```text
经典协同过滤 / matrix factorization baseline
```

LLM:

```text
language prompt + adapter tuning
```

解释：

[INTERPRETATION] Popularity/BPR 的作用不是证明 LLM 一定更强，而是证明 Random-k5 的 easy-negative shortcut 很严重，PopMatch 更有必要。

## 面试红线

不要说：

```text
本项目提出了新 architecture
本项目就是 TALLRec
本项目就是 LLMRank
SASRec 被 LLM 全面击败
```

要说：

```text
本项目的核心是 supervision semantics + robust evaluation
TALLRec 提供了 Y-style 背景
LLMRank 提供了 ranking behavior 背景
SASRec 是强 sequence baseline；当前结论是 N-K0 sample-efficient，且远多监督的 SASRec anchor 可超过当前 N-K0，完整 high-budget head-to-head 未测
```
