---
id: discussion_evaluation_protocol
title:
  en: Evaluation Protocol Reveals Different Capability Gaps
  zh: 评估协议揭示不同的能力差距
status: draft
---

<!-- PARAGRAPH: discussion.protocol.p01 -->
<!-- EVIDENCE: C5,C6,M5 -->

**EN**

Across three training seeds at 96k, k20 reveals a substantially larger N advantage than standard k5 on validation and frozen test, whereas k50 retains the direction with a smaller gap than k20 and seed-dependent magnitude. The k50 gap is not uniformly larger than k5. This variation shows why a standard-k5 comparison alone does not characterize how much specialist performance is retained under other candidate conditions. The relevant relationship is protocol-conditioned, not a monotonic gap increase with candidate count.

**ZH**

三个训练种子在96k时的验证与冻结测试均显示，k20下的N优势明显大于标准k5；k50保持优势方向，但差距小于k20，幅度随seed变化。k50差距并不总大于k5。这种变化说明，仅凭标准k5下的比较，无法刻画其他候选条件下保留了多少专家表现。这里的关系受协议限定，而非差距随候选数量单调增加。

<!-- PARAGRAPH: discussion.protocol.p02 -->
<!-- EVIDENCE: C5,C6,M5 -->

**EN**

Reporting a model comparison together with each candidate protocol's construction rules makes its scope explicit. Fixed candidates within a protocol support paired model comparisons; results across protocols describe sensitivity to the evaluated conditions. Because the independently constructed, non-nested sets jointly vary candidate count, composition, sampling method, and difficulty, this sensitivity concerns the protocols as a whole rather than an isolated factor.

**ZH**

将模型比较与各候选协议的构造规则一并报告，可以明确结果的适用范围。协议内部固定候选支持模型间的配对比较，跨协议结果则描述对被测条件的敏感性。这些独立构造、非嵌套的集合同时改变了候选数量、组成、采样方法与难度，因此，这种敏感性针对协议整体，而非某个被单独识别的因素。
