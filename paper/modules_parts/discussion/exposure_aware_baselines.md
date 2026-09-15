---
id: discussion_exposure_aware_baselines
title:
  en: Exposure-Aligned Cross-Model Baseline Comparison
  zh: 曝光对齐下的跨模型基线比较
status: draft
---

<!-- PARAGRAPH: discussion.baseline.p01 -->
<!-- EVIDENCE: C7,M7 -->

**EN**

Across four approximately matched seed42 points, N leads the evaluated SASRec baseline, while SASRec improves substantially and narrows the largest-exposure gap. The former describes performance under limited downstream task supervision; the latter describes the baseline's response to receiving more supervision. Both are needed to interpret the cross-model comparison.

**ZH**

在四个seed42曝光近似匹配点上，N领先被评估的SASRec基线，同时SASRec明显改善并缩小最大曝光点的差距。前者描述有限下游任务监督下的表现，后者描述基线获得更多监督后的响应；两者缺一不可。

<!-- PARAGRAPH: discussion.baseline.p02 -->
<!-- EVIDENCE: C7,M3,M7 -->

**EN**

Task-sample exposure is a useful but partial cross-model axis. It describes adaptation from the LLM's pretrained starting point and does not match pretraining, tokens, updates, FLOPs, time, serving, or deployment cost. The evidence supports an exposure-aligned performance comparison, not general resource efficiency.

**ZH**

任务样本曝光是有用但局部的跨模型比较轴。它描述LLM从预训练起点进行的适配，并不匹配预训练、token、更新、FLOPs、时间、服务或部署成本。现有证据支持曝光对齐的表现比较，而非一般资源效率结论。
