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

We study recommendation supervision through the prediction target it defines. Let an interaction be a user-item event with an observed rating and timestamp, and let H(u,t) denote the user's interactions strictly before time t. We use the full interaction sequence for sample construction and retain at most the 10 most recent strictly earlier interactions as model input, denoted H_10(u,t). The input pairs this truncated recent history with either an individual item i or a candidate set C. A rating-based preference label and the identity of the next observed interaction answer different questions even when they originate from the same sequence.

**ZH**

本文从预测目标出发研究推荐监督。一次交互由用户、物品、观测评分和时间戳构成，H(u,t) 表示用户在时刻 t 之前发生的交互。完整交互序列用于样本构造，模型输入则最多保留严格早于目标时刻的最近 10 条交互，记为 H_10(u,t)。这一截断后的近期历史与单个物品 i 或候选集 C 共同构成输入。即使来自同一序列，基于评分的偏好标签与下一次观测交互的物品身份回答的也是不同问题。

<!-- INCLUDE: paper/modules_parts/methods/task_definition.md -->

<!-- PARAGRAPH: problem.p02 -->
<!-- EVIDENCE: C1,C2,C3,C4,C5,C6,C7 -->

**EN**

This formulation leads to five research questions. RQ1 examines the observed capability profiles associated with preference and next-interaction supervision, and RQ2 examines how those profiles change with task-sample exposure. RQ3 asks how closely M1 approaches the two specialists at matched per-task exposure, while RQ4 tests the reach of the standard PopMatch-k5 relationship under harder candidate protocols. RQ5 examines how exposure conditions the comparison between the N-trained LLM and SASRec. Together, these questions define an empirical study of supervision formulations, training exposure, and evaluation methodology.

**ZH**

这一问题定义对应五个研究问题。RQ1 考察偏好监督与下一交互监督各自对应的可观测能力结构，RQ2 考察这些能力如何随任务样本曝光变化。RQ3 研究每任务曝光对齐时 M1 与两种专家的接近程度，RQ4 检验标准 PopMatch-k5 下的模型关系能否延续到较难候选协议。RQ5 考察曝光如何影响接受 N 任务训练的 LLM 与 SASRec 的比较。这些问题共同构成一项关于监督形式、训练曝光和评估方法的实证研究。
