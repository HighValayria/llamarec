---
id: results
title:
  en: Results
  zh: 实验结果
status: draft
---

<!-- PARAGRAPH: results.p01 -->
<!-- EVIDENCE: C1,C2,C3,C4,C5,C6,C7,C8 -->

**EN**

The results connect the capabilities learned under Y and N supervision to their response to additional training exposure. We then examine how per-task exposure and candidate protocols condition the specialist-multitask comparison, and how exposure affects the N-SASRec relationship. MovieLens provides the full seed42 exposure trajectories and independent seed43/44 replications of Y96, N96, and M1-96 at the 96k operating point. Validation guided experimental decisions; after those decisions were frozen, test results provide report-only held-out generalization evidence. Amazon supplies an external check of the central ranking directions at earlier operating points.

**ZH**

结果将Y与N监督下形成的能力差异，与它们对额外训练曝光的响应联系起来，再考察每任务曝光和候选协议如何限定专家与多任务模型的比较，以及曝光如何影响N与SASRec的关系。MovieLens提供完整的seed42曝光轨迹，以及seed43/44在96k运行点上对Y96、N96和M1-96的独立复现。验证集指导实验决策；决策冻结后，测试结果作为仅报告的留出泛化证据。Amazon则在较早运行点上为核心排序方向提供外部检验。

<!-- INCLUDE: paper/modules_parts/results/rq1_supervision_semantics.md -->
<!-- INCLUDE: paper/modules_parts/results/rq2_exposure_response.md -->
<!-- INCLUDE: paper/modules_parts/results/rq3_multitask_unification.md -->
<!-- INCLUDE: paper/modules_parts/results/rq4_hard_candidate_robustness.md -->
<!-- INCLUDE: paper/modules_parts/results/rq5_sasrec_exposure.md -->
<!-- INCLUDE: paper/modules_parts/results/cross_dataset_validation.md -->
