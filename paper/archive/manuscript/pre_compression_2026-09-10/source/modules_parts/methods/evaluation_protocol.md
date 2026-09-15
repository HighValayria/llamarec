---
id: evaluation_protocol
title:
  en: Native Metrics and Candidate Protocols
  zh: 原生指标与候选协议
status: draft
---

<!-- PARAGRAPH: methods.evaluation.p01 -->
<!-- EVIDENCE: M4,M6,C1 -->

**EN**

Y-native evaluation reports AUC, F1, and accuracy on rating-derived binary targets. The 96k paired binary analysis applies a fixed 0.5 threshold for F1 and accuracy. Y-as-ranker scores each candidate independently by P(Yes), while N-native and M-N ranking use the candidate-label interface. Ranking metrics are HR@1, NDCG@5, and MRR for the single observed target. Across all candidate protocols, NDCG is truncated at 5 and MRR uses the target rank over the entire candidate set.

**ZH**

Y 原生评估在评分产生的二分类目标上报告 AUC、F1 和 Accuracy。96k 配对二分类分析对 F1 和 Accuracy 使用固定 0.5 阈值。Y-as-ranker 按 P(Yes) 对每个候选独立评分，N-native 与 M-N 排序使用候选标签接口。排序围绕唯一观测目标报告 HR@1、NDCG@5 和 MRR。各候选协议均将 NDCG 截断到前 5 名，MRR 则使用目标在整个候选集中的排名。

<!-- PARAGRAPH: methods.evaluation.p02 -->
<!-- EVIDENCE: M5,C6 -->

**EN**

Random-k5 contains one target and four randomly sampled distractors. PopMatch-k5 draws distractors with popularity close to the target using counts from the processed full interaction corpus. The implementation excludes the current target, orders eligible items by absolute popularity difference, and samples from a nearest-popularity pool up to 10 times the required distractor count. Candidate lists and their ordering are fixed within each model comparison. PopMatch reduces target-distractor popularity mismatch as a retrospective offline evaluation control, rather than a simulation of online retrieval.

**ZH**

Random-k5 包含一个目标与四个随机采样的干扰候选。PopMatch-k5 使用处理后的完整交互语料统计流行度，抽取流行度接近目标的干扰候选。实现排除当前目标，按流行度绝对差排列符合条件的物品，再从大小至多为所需干扰候选数 10 倍的近邻流行度池中采样。每组模型比较使用固定候选列表及其顺序。PopMatch 通过这种回顾性的离线评估控制减弱目标与干扰候选间的流行度失配，而非模拟在线检索。

<!-- PARAGRAPH: methods.evaluation.p03 -->
<!-- EVIDENCE: C6,M5 -->

**EN**

The hard-k20 and hard-k50 protocols evaluate N96 and M1-96 with 20 and 50 candidates, respectively. Each protocol uses a separately constructed candidate set, with the same examples and ordered candidates shared by the compared models. The sets are non-nested across protocols. This design tests model comparisons under additional candidate conditions, varying candidate composition together with count.

**ZH**

Hard-k20 和 hard-k50 协议分别使用 20 个和 50 个候选评估 N96 与 M1-96。各协议的候选集独立构造，参与比较的模型使用相同样本和有序候选。不同协议的候选集为非嵌套关系。这一设计在额外候选条件下检验模型比较，候选组成与数量随协议一同变化。
