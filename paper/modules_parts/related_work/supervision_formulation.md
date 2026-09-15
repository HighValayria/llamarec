---
id: rw_supervision_formulation
title:
  en: Recommendation Supervision and Task Formulation
  zh: 推荐监督与任务形式
status: draft
---

<!-- PARAGRAPH: rw.tasks.p01 -->
<!-- EVIDENCE: S06,S07,S08,M1 -->

**EN**

Recommendation targets differ before any language interface. Matrix factorization fits ratings, implicit-feedback methods distinguish preference from confidence in observations, and sequential models predict a subsequent item [@koren2009mf; @hu2008implicit; @kang2018sasrec]. Their scores therefore concern assessments, observed behavior, or next-event selection. Separating target from modeling technique clarifies which capability a score supports.

**ZH**

在引入语言接口之前，推荐目标就有区别。矩阵分解拟合评分，隐式反馈方法区分偏好与行为观测置信度，序列模型则预测后续物品 [@koren2009mf; @hu2008implicit; @kang2018sasrec]。相应分数分别涉及评价、观测行为或下一事件选择。区分目标与建模技术，才能明确分数支持何种能力判断。

<!-- PARAGRAPH: rw.tasks.p02 -->
<!-- EVIDENCE: C1,M1,M4,S02,S15 -->

**EN**

A common language interface can retain these distinctions. P5 includes rating-threshold like/dislike questions and next-item interfaces; ITDR also combines rating and next-item tasks [@geng2022p5; @liu2025itdr]. Task distinction is therefore not new. Our framing compares their observed native and bridge capability profiles while treating target, task data, prompt, and scoring rule as one complete formulation rather than a single isolated semantic factor.

**ZH**

共同语言接口仍可保留这些区别。P5同时包含评分阈值下的喜欢与否问题及下一物品接口，ITDR也组合评分与下一物品任务 [@geng2022p5; @liu2025itdr]。任务区分本身并非本文首次提出；本文比较其原生与桥接能力结构，并将目标、任务数据、提示和评分规则视为完整形式，而非单一语义因素。
