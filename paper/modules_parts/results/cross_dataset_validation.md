---
id: cross_dataset_validation
title:
  en: Cross-Dataset Directional Validation
  zh: 跨数据集方向性检验
status: draft
---

<!-- PARAGRAPH: results.amazon.p01 -->
<!-- EVIDENCE: C8 -->

**EN**

At the evaluated earlier seed42 operating points on Amazon Musical Instruments, N reaches 0.4669 HR@1 on 57,439 PopMatch-k5 test examples, compared with 0.3573 for Base, 0.2298 for Y-as-ranker, and 0.1757 for SASRec. [TABLE: cross_dataset] reports these four cross-task-safe or task-specific model results with HR@1, NDCG@5, and MRR.

**ZH**

在Amazon Musical Instruments已评估的较早seed42运行点上，N在57,439个PopMatch-k5测试样本中达到0.4669 HR@1，Base、Y-as-ranker与SASRec分别为0.3573、0.2298和0.1757。[TABLE: cross_dataset]报告这四个满足跨任务安全或任务特定条件的模型结果，包括HR@1、NDCG@5与MRR。

<!-- PARAGRAPH: results.amazon.p02 -->
<!-- EVIDENCE: C8,C1,C7 -->

**EN**

Amazon therefore provides ranking-side directional support at available earlier points, not a second exposure curve, three-seed 96k replication, hard-candidate study, or native-preference validation.

**ZH**

因此，Amazon仅在现有较早运行点提供排序侧方向性支撑，不构成第二条曝光曲线、三seed的96k复现、较难候选研究或原生偏好验证。
