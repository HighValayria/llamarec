---
id: rq1_supervision_semantics
title:
  en: Different Supervision and Observed Recommendation Capabilities
  zh: 不同监督与可观测推荐能力
status: draft
---

<!-- PARAGRAPH: results.rq1.p01 -->
<!-- EVIDENCE: C1,C2 -->

**EN**

Y and N show distinct measured capability profiles. Y96 reaches 0.7844 validation AUC on native MovieLens preference prediction. Through the P(Yes) bridge, its PopMatch-k5 validation HR@1 is 0.2211, compared with 0.6238 for N96 at the same nominal task-sample exposure. Native preference metrics, the Y-as-ranker trajectory, and validation/frozen-test Y96-N96 endpoints appear in [TABLE: supervision_semantics_compact].

**ZH**

Y与N呈现不同的被测能力结构。Y96在MovieLens原生偏好预测上的验证AUC为0.7844；通过P(Yes)桥接后，其PopMatch-k5验证HR@1为0.2211，而相同名义任务样本曝光下N96为0.6238。原生偏好指标、Y-as-ranker轨迹以及验证与冻结测试上的Y96-N96端点见[TABLE: supervision_semantics_compact]。

<!-- PARAGRAPH: results.rq1.p02 -->
<!-- EVIDENCE: C1,M1,M4 -->

**EN**

This contrast separates rating-derived preference discrimination from selecting the next observed event. Because target construction, task data, prompts, and scoring interfaces differ jointly, it compares complete supervision formulations rather than isolating one semantic cause.

**ZH**

这一对照区分了评分产生的偏好判别与下一观测事件选择。由于目标构造、任务数据、提示和评分接口共同变化，比较针对完整监督形式，而非隔离某个语义因素的因果作用。
