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

Recommendation targets differ even before a language interface is introduced. A basic matrix-factorization formulation fits observed ratings, whereas implicit-feedback collaborative filtering separates a preference indicator from confidence in behavioral observations [@koren2009mf; @hu2008implicit]. An unobserved interaction therefore need not represent an explicit dislike. Sequential recommendation instead uses a user's history to predict a subsequent item, as in SASRec [@kang2018sasrec]. These formulations give scores different operational meanings: fitting an assessment, modeling observed behavior, or selecting a next event. Distinguishing the target from the modeling technique clarifies the capability a reported score can support.

**ZH**

在引入语言接口之前，推荐目标就已存在区别。基础矩阵分解形式拟合已观测评分，隐式反馈协同过滤则区分偏好指示与行为观测的置信度 [@koren2009mf; @hu2008implicit]。因此，未观测到交互不必代表明确的不喜欢。序列推荐则根据用户历史预测后续物品，SASRec 即属此类 [@kang2018sasrec]。这些形式赋予分数不同的操作性含义：拟合评价、建模观测行为，或者选择下一事件。将目标与建模技术区分开，有助于明确一个被报告分数能够支持何种能力判断。

<!-- PARAGRAPH: rw.tasks.p02 -->
<!-- EVIDENCE: C1,M1,M4,S02,S15 -->

**EN**

A common language interface can retain these distinctions. P5 includes rating-derived like/dislike questions using a threshold of at least four, alongside next-item generation and candidate-selection interfaces [@geng2022p5]. ITDR likewise includes rating and next-item tasks within a multitask instruction dataset [@liu2025itdr]. These precedents show that unified task expression can accommodate different prediction questions. We examine their observed capability profiles through rating-derived preference and next-interaction formulations, including a bridge evaluation that uses preference scores to rank next-interaction candidates. The comparison concerns the complete target, task data, prompt, and scoring formulation within the shared adaptation setting.

**ZH**

共同语言接口可以保留这些区别。P5 同时包含以评分至少为四作为阈值的喜欢与否问题，以及下一物品生成和候选选择接口 [@geng2022p5]。ITDR 也在多任务指令数据中纳入评分与下一物品任务 [@liu2025itdr]。这些先例说明，统一的任务表达可以容纳不同预测问题。本文通过评分产生的偏好形式与下一交互形式考察其可观测能力结构，并以偏好分数排列下一交互候选，形成桥接评估。这一比较针对共同适配设置中的完整目标、任务数据、提示和评分形式。
