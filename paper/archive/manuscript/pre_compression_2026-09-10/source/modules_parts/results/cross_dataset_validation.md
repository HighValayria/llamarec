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

The main ranking-side directions reappear on Amazon Musical Instruments at the evaluated seed42 operating points. Across 57,439 PopMatch-k5 test examples, N-K0 achieves 0.4669 HR@1, compared with 0.2298 for Y-as-ranker, 0.4582 for M1, and 0.1757 for the exposure-matched SASRec reference. NDCG@5 and MRR are 0.7420 and 0.6570 for N-K0, 0.7384 and 0.6521 for M1, and 0.5685 and 0.4295 for SASRec. The N-M HR@1 margin is +0.00870, alongside larger gaps over Y-as-ranker and SASRec. These external test results reproduce the observed ranking order in a second domain. [TABLE: cross_dataset]

**ZH**

在已评估的 seed42 运行点上，主要排序侧方向再次出现在 Amazon Musical Instruments 中。在 57,439 个 PopMatch-k5 测试样本上，N-K0 的 HR@1 为 0.4669，Y-as-ranker 为 0.2298，M1 为 0.4582，曝光匹配的 SASRec 参照为 0.1757。N-K0 的 NDCG@5 与 MRR 为 0.7420 和 0.6570，M1 为 0.7384 和 0.6521，SASRec 为 0.5685 和 0.4295。N-M 的 HR@1 差距为 +0.00870，对 Y-as-ranker 和 SASRec 的优势则更大。这些外部测试结果在第二个领域中重现了所观察的排序关系。[TABLE: cross_dataset]

<!-- PARAGRAPH: results.amazon.p02 -->
<!-- EVIDENCE: C8,C1,C7 -->

**EN**

Amazon thus extends the ranking-side comparison of Y, N, M1, and the low-exposure SASRec reference beyond MovieLens. Its support concerns the earlier operating points evaluated there; detailed exposure trajectories and higher-exposure multitask comparisons remain specific to MovieLens. This distinction sets the scope of the cross-dataset interpretation developed below.

**ZH**

由此，Amazon 将 Y、N、M1 与低曝光 SASRec 参照的排序侧比较延伸到 MovieLens 之外。其支撑限于该数据集已评估的较早运行点；详细曝光轨迹与更高曝光下的多任务比较仍来自 MovieLens。这一区分明确了下文跨数据集解释的适用范围。
