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

Y and N show distinct observed capability profiles. Y96 achieves MovieLens validation AUC, F1, and accuracy of 0.7844, 0.7783, and 0.7235 on native preference prediction; the corresponding test values are 0.7854, 0.7780, and 0.7221. On PopMatch-k5 next-interaction ranking, the same Y model reaches 0.2211 HR@1 and 0.6031 NDCG@5 through P(Yes). N96 achieves 0.6238 HR@1 and 0.8303 NDCG@5 at the same nominal task-sample exposure. The test ranking contrast is also large, with HR@1 of 0.2065 for Y96 and 0.6100 for N96. [TABLE: binary_exposure] and [TABLE: semantics_bridge] show native preference discrimination alongside this cross-interface ranking comparison.

**ZH**

Y 与 N 呈现出不同的可观测能力结构。Y96 在 MovieLens 原生偏好预测上的验证 AUC、F1 和 Accuracy 分别为 0.7844、0.7783 和 0.7235，对应测试值为 0.7854、0.7780 和 0.7221。在 PopMatch-k5 下一交互排序中，同一个 Y 模型通过 P(Yes) 达到 0.2211 HR@1 和 0.6031 NDCG@5。N96 在相同名义任务样本曝光下达到 0.6238 HR@1 和 0.8303 NDCG@5。测试集上的排序差距同样较大，Y96 与 N96 的 HR@1 分别为 0.2065 和 0.6100。[TABLE: binary_exposure] 与 [TABLE: semantics_bridge] 将原生偏好判别表现与跨接口排序对照一并列出。

<!-- PARAGRAPH: results.rq1.p02 -->
<!-- EVIDENCE: C1,M1,M4 -->

**EN**

The contrast separates preference discrimination from identifying the next observed event: Y performs its native rating-derived task, while N is trained directly for candidate selection. The comparison concerns complete supervision formulations, which differ in target construction, task datasets, prompt form, and scoring interface. This distinction raises a further question: how does each capability respond when the model receives more supervision?

**ZH**

这一对照区分了偏好判别与识别下一观测事件：Y 完成的是原生评分标签任务，N 则直接接受候选选择训练。比较对象是完整的监督形式，其目标构造、任务数据集、提示形式和评分接口均有差异。这一区别进一步引出一个问题：模型接受更多监督后，各项能力将如何变化？
