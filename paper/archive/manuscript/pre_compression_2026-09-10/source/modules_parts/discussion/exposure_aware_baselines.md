---
id: discussion_exposure_aware_baselines
title:
  en: Exposure-Aware Baseline Comparison
  zh: 曝光感知的基线比较
status: draft
---

<!-- PARAGRAPH: discussion.baseline.p01 -->
<!-- EVIDENCE: C7,M7 -->

**EN**

The four approximately matched seed42 exposure points show a downstream task-supervision advantage for the evaluated pretrained LLM relative to the SASRec baseline. N leads at every matched point, while SASRec's substantial improvement with additional supervision narrows the gap at the largest measured exposure. Both observations are central: one describes performance with limited task supervision, and the other describes the baseline's response to receiving more of it. Their coexistence gives a more informative account of the model comparison than a single checkpoint ranking.

**ZH**

四个近似匹配的 seed42 曝光点显示，相对于被评估的 SASRec 基线，预训练 LLM 在给定下游任务监督量时具有表现优势。N 在每个匹配点均领先，而 SASRec 随额外监督明显改善，使差距在最大的已测曝光点缩小。两项观察都很重要：前者描述有限任务监督下的表现，后者描述基线获得更多监督后的响应。将两者结合起来，比单一检查点排序更充分地解释了模型比较。

<!-- PARAGRAPH: discussion.baseline.p02 -->
<!-- EVIDENCE: C7,M3,M7 -->

**EN**

Task-sample exposure supplies a useful, partial axis of comparison across model families. The reported ranking performance under approximately matched downstream task-sample exposure describes adaptation from the LLM's pretrained starting point. Resource efficiency additionally requires accounting for pretraining, training computation, and serving.

**ZH**

任务样本曝光为不同模型系列提供了一个有用但局部的比较维度。所报告的近似匹配下游任务样本曝光下的排序表现，描述的是LLM从预训练初始条件开始的适配。资源效率还需要计入预训练、训练计算与服务成本。
