---
id: discussion_exposure_interpretation
title:
  en: Exposure and Specialist-Shared Modeling
  zh: 曝光与专家-共享建模
status: draft
---

<!-- PARAGRAPH: discussion.exposure.p01 -->
<!-- EVIDENCE: C2,C3,M3 -->

**EN**

Exposure locates a comparison along the observed adaptation trajectory. Seed42 shows continued N improvement but limited or uneven Y gains, so an early checkpoint need not describe the later model relationship. Treating task exposure as an experimental variable prevents an operating point from being mistaken for a stable property of the task.

**ZH**

曝光确定比较位于已观测适配轨迹的哪个位置。seed42显示N持续改善，而Y增益有限或不均匀，因此早期检查点不必代表后续模型关系。把任务曝光作为实验变量，可以避免将某个运行点误解为任务的稳定属性。

<!-- PARAGRAPH: discussion.exposure.p02 -->
<!-- EVIDENCE: C3,C5,C7,M3 -->

**EN**

Task-specific accounting distinguishes M1's total exposure from the supervision allocated to each interface and makes SASRec comparisons interpretable across batch sizes. This axis is cumulative downstream consumption, including repetitions, rather than unique data or computation. Stating it beside performance makes the budget condition of each advantage visible.

**ZH**

按任务统计可以区分M1总曝光与分配给各接口的监督，也使不同batch size下的SASRec比较具有明确口径。这一轴表示包含重复样本的累计下游消费，而非唯一数据量或计算量。将其与表现并列报告，可明确每项优势的预算条件。

<!-- PARAGRAPH: discussion.exposure.p03 -->
<!-- EVIDENCE: C4,C5,C6,M3,M4 -->

**EN**

The standard-k5 validation trajectory and independent 96k replications together show that specialist-shared relations are conditional on adaptation point. M1 retains comparable Y-side capability at 96k, while frozen tests still favor N. A shared adapter should therefore be assessed by capability retained at a stated exposure and protocol, not by an unconditional success/failure label. The full trajectory remains seed42-only.

**ZH**

标准k5验证轨迹与96k独立复现共同表明，专家-共享关系受适配运行点限定。M1在96k保留接近的Y侧能力，冻结测试仍偏向N。因此，共享adapter应按明确曝光和协议下保留的能力评估，而不宜作无条件成败判断；完整轨迹仍仅来自seed42。
