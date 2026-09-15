---
id: discussion
title: {en: Discussion, zh: 讨论}
status: draft
---

<!-- PARAGRAPH: discussion.p01 -->
<!-- EVIDENCE: C1,C2,C3,C4,C5,C6,C7,C8 -->

**EN**

The findings tie three parts of a recommendation comparison to one another: supervision formulation defines the prediction question, task exposure locates the adaptation point, and candidate protocol defines the measured ranking conditions. Their implications differ from the numerical results and are organized below by the study's contribution hierarchy.

**ZH**

这些发现将推荐比较中的三个方面联系起来：监督形式定义预测问题，任务曝光确定适配运行点，候选协议界定排序测量条件。下文按研究贡献层级讨论其含义，而不重复结果数值。

<!-- INCLUDE: paper/modules_parts/discussion/supervision_interface.md -->
<!-- INCLUDE: paper/modules_parts/discussion/exposure_interpretation.md -->
<!-- INCLUDE: paper/modules_parts/discussion/evaluation_protocol.md -->
<!-- INCLUDE: paper/modules_parts/discussion/exposure_aware_baselines.md -->

<!-- PARAGRAPH: discussion.external.p01 -->
<!-- EVIDENCE: C1,C2,C3,C5,C6,C7,C8 -->

**EN**

MovieLens supplies the detailed within-domain exposure and protocol analysis, whereas Amazon checks ranking directions only at available earlier seed42 points. The two domains therefore provide complementary detailed and directional evidence; untested cross-domain trajectories remain outside the present claims.

**ZH**

MovieLens提供详细的领域内曝光与协议分析，Amazon仅在现有较早seed42运行点检验排序方向。两个领域由此分别提供详细证据与方向证据，未经检验的跨域轨迹不属于本文结论。

<!-- PARAGRAPH: discussion.synthesis.p01 -->
<!-- EVIDENCE: C1,C2,C3,C4,C5,C6,C7 -->

**EN**

Recommendation capability and relative performance should thus be interpreted within the evaluated formulation, cumulative per-task exposure, and candidate protocol. The cross-model trajectory adds that an observed N advantage can coexist with continued improvement of the sequential baseline.

**ZH**

因此，推荐能力与相对表现应结合已评估的监督形式、累计每任务曝光和候选协议解释。跨模型轨迹还表明，已观测的N优势可以与序列基线的持续改善同时存在。
