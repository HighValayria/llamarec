---
title: "10 sasrec and sample efficiency"
type: report
status: current
authority: descriptive
source: agent
created: 2026-08-24
updated: 2026-08-24
last_verified: 2026-08-24
related_code:
  - src/baselines/popularity.py
  - src/baselines/bpr_mf.py
  - src/baselines/sasrec.py
  - src/analysis/training_budget_audit.py
  - src/analysis/sample_exposure_matched_diagnostic.py
  - src/analysis/sample_efficiency_curve.py
  - src/analysis/cold_tail_slice_diagnostic.py
---

# 10 SASRec And Sample Efficiency

## 为什么需要 baseline

[INTERPRETATION] 如果只报告 LLM Y/N/M，很难判断：模型是真的学到序列推荐，还是只靠 popularity、简单协同过滤，或者候选太容易。

所以 baseline 分三层：

```text
Popularity -> 检查热门 item shortcut
BPR-MF     -> 检查经典协同过滤
SASRec     -> 检查强序列推荐模型
```

## Popularity baseline

它回答：

```text
只按 item 热门程度排序能做到多强？
```

[FACT] Random-k5 下 Popularity 很强；PopMatch 下明显下降。

面试解释：

> 如果 Popularity 在 Random-k5 很强，说明 random negatives 和 target 的 popularity 差异太大，ranking 任务可能太容易。

## BPR-MF baseline

它回答：

```text
经典 matrix factorization / collaborative filtering 能解释多少？
```

[FACT] MovieLens BPR-MF Random-k5 HR@1 `0.5611`，PopMatch HR@1 `0.3352`。

解释：

[INTERPRETATION] BPR-MF 比 Popularity 更强，但 PopMatch 下仍不足以解释 N-K0/M1 的表现。

## SASRec 是什么

简短版：

> SASRec 是 self-attention sequential recommender。它用 item ID embedding 序列预测下一项，不使用 LLM 的自然语言 prompt。

对比 LLM：

```text
SASRec:
  input = item ID sequence
  representation = learned item embeddings
  model = recommender-specific Transformer/self-attention
  output = next item/candidate score

LLM adapter:
  input = natural-language prompt with titles
  representation = pretrained language model + LoRA adapter
  output = Yes/No or candidate label token probability
```

## 为什么 step-aligned 不公平

表面比较：

```text
N-K0 1500 optimizer steps
SASRec 1500 optimizer steps
```

问题：

```text
N-K0 effective batch = 8
SASRec batch = 512
```

[FACT] N-K0 1500 steps -> N exposure `12000`。

[FACT] SASRec s1500 -> N exposure `767424`，是 N-K0 的 `63.952x`。

面试模板：

> 同样 step 数不等于同样训练预算。step 是更新次数，batch size 决定每步看多少样本，sample exposure 才是总共看过多少训练样本。

## sample exposure 怎么算

公式：

```text
sample_exposure = optimizer_steps * effective_batch
```

N-K0:

```text
1500 * 8 = 12000
```

M1:

```text
3000 * 8 = 24000 total
其中 Y/N 1:1，所以 N-task exposure = 12000
```

SASRec closest:

```text
23 * 512 = 11776
```

SASRec high:

```text
3000 * 512 = 1534656
```

## closest-exposure SASRec

目标：

```text
让 SASRec 看过的 N-task 样本数接近 N-K0 的 12000
```

[FACT] 使用 23 steps，exposure `11776`，比目标低 `1.8667%`。

结果：

```text
MovieLens N-K0 HR@1:           0.5466
MovieLens SASRec exp-match:    0.2700
```

解释：

[INTERPRETATION] 在这个 N-task sample exposure 轴上，N-K0 更 sample-efficient。

## high-exposure SASRec anchor

[FACT] SASRec s3000 exposure `1534656`，HR@1 `0.6243`。

[FACT] 当前没有训练或评测 `N-K0(≈1.53M N-task exposure)`，所以没有完成双方 high-exposure head-to-head comparison。

解释：

[INTERPRETATION] 给 SASRec 远多 sequential supervision 后，它可以超过当前这个约 `12000` N-task exposure 的 N-K0 checkpoint。这个结果很重要，因为它阻止我们说“LLM 普遍比 SASRec 强”，但它也不能支持“high-exposure 下 SASRec 一定比 LLM 强”。

## 正确总结

不要说：

```text
LLM beats SASRec
SASRec beats LLM
high-exposure 下 SASRec 比 LLM 强
```

要说：

```text
At approximately matched N-task exposure, N-K0 substantially outperforms SASRec.
With substantially more sequential supervision, SASRec can eventually surpass the current N-K0 checkpoint.
We have not measured N-K0 at the same 1.53M exposure, so this is sample-efficiency evidence, not a complete budget-performance frontier.
```

## cold/tail baseline 结论

[FACT] coldest target-popularity bucket `<=10` 只有 26 samples。

[FACT] SASRec high-exposure anchor 相对当前 N-K0 的优势主要在 middle/head buckets；coldest bucket 中 N-K0 高于 SASRec rows，但样本太少。

面试说法：

> 这个诊断说明 SASRec high-exposure anchor 相对当前 N-K0 的 overall advantage 不是 coldest bucket 驱动的。但 coldest bucket 太小，不能宣称 LLM 擅长 cold-start。

## MovieLens multi-seed baseline 结论

[FACT] seeds 42/43/44 下：

```text
N-K0 > SASRec exp-match
SASRec high s3000 > current N-K0(12k exposure)
```

解释：

[INTERPRETATION] 预算敏感方向稳定：matched sample-exposure 下 N-K0 强；远多监督的 SASRec checkpoint 可超过当前 N-K0。但这不是双方 high-exposure 对齐后的结论。

## Amazon baseline 结论

[FACT] Amazon PopMatch-k5 seed42：

```text
N-K0 HR@1:          0.4669
SASRec exp-match:   0.1757
Delta:              +0.2912
```

边界：

```text
Amazon high-exposure SASRec not evaluated
Amazon seed42 only
```

## 刁钻问题模板

问：LLM 参数量比 SASRec 大这么多，sample efficiency 有意义吗？

答：

> 有意义，但它回答的是样本曝光维度，不回答 compute/FLOPs 维度。我的结论会限定为 N-task sample exposure 下的 data efficiency，不会说 compute-efficient 或 architecture universally superior。

问：SASRec high exposure anchor 超过当前 N-K0 是不是推翻你的结论？

答：

> 不推翻，反而帮我们收紧结论。它说明 specialized recommender 在足够多 sequential supervision 下可以超过当前低曝光 N-K0；我的安全结论是 sample-efficiency，而不是完整 high-budget frontier。
