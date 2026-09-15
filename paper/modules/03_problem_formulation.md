---
id: problem_formulation
title:
  en: Problem Formulation
  zh: 问题定义
status: draft
---

<!-- PARAGRAPH: problem.p01 -->
<!-- EVIDENCE: C1,M1 -->

**EN**

Let an interaction be a user-item event with a rating and timestamp, and let H(u,t) contain a user's interactions strictly before t. Samples use the complete sequence, while model input retains at most the 10 most recent strictly earlier interactions, H_10(u,t), paired with an item i or candidate set C. A rating-derived preference label and the next observed item answer different questions even when drawn from the same sequence.

**ZH**

一次交互由用户、物品、评分和时间戳构成，H(u,t)表示用户在t之前发生的交互。样本构造使用完整序列，模型输入最多保留严格早于目标时刻的最近10条交互H_10(u,t)，并与物品i或候选集C配对。即使来自同一序列，评分产生的偏好标签与下一观测物品回答的也是不同问题。

<!-- INCLUDE: paper/modules_parts/methods/task_definition.md -->

<!-- PARAGRAPH: problem.p02 -->
<!-- EVIDENCE: C1,C2,C3,C4,C5,C6,C7 -->

**EN**

RQ1 compares the observed Y and N capability profiles; RQ2 traces their response to task-sample exposure. RQ3 asks how closely M1 approaches both specialists at matched per-task exposure, and RQ4 tests how the standard PopMatch-k5 relationship changes under alternative candidate protocols. RQ5 follows the exposure-conditioned comparison between N-trained LlamaRec and SASRec.

**ZH**

RQ1比较Y与N的可观测能力结构，RQ2追踪其对任务样本曝光的响应。RQ3考察每任务曝光对齐时M1与两种专家的接近程度，RQ4考察标准PopMatch-k5关系在其他候选协议下如何变化。RQ5追踪曝光条件下N训练的LlamaRec与SASRec之间的比较。
