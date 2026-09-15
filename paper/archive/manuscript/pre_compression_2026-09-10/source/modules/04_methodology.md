---
id: methodology
title:
  en: Methodology
  zh: 研究方法
status: draft
---

<!-- PARAGRAPH: methodology.p01 -->
<!-- EVIDENCE: M1,M2,M3,M4 -->

**EN**

The experimental pipeline converts timestamped interactions into prediction examples, adapts a shared base model through task-specific prompts, and evaluates the resulting response likelihoods. Sample construction uses each user's complete chronological sequence; prompt construction retains a bounded recent history. Y prompts request a rating-derived preference judgment, whereas N prompts request the next-interaction candidate. The corresponding scoring interfaces yield a binary preference score or an ordering over candidates.

**ZH**

实验流程将带时间戳的交互转换为预测样本，通过任务特定提示适配共同底座，再评估得到的响应似然。样本构造使用每位用户完整的时间序列，提示构造则保留长度受限的近期历史。Y 提示要求作出基于评分的偏好判断，N 提示要求选择下一交互候选。相应评分接口输出二分类偏好分数或候选排序。

<!-- INCLUDE: paper/modules_parts/methods/temporal_split.md -->
<!-- INCLUDE: paper/modules_parts/methods/training_setup.md -->
