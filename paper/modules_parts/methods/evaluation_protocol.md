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

Y-native evaluation reports AUC, F1, and accuracy; paired 96k F1/accuracy use threshold 0.5. Y-as-ranker independently scores candidates by P(Yes), whereas N-native and M-N use candidate-label likelihoods. Ranking reports HR@1, NDCG@5, and MRR; NDCG is truncated at 5 and MRR uses the complete candidate ranking.

**ZH**

Y原生评估报告AUC、F1和Accuracy，96k配对分析的F1/Accuracy阈值为0.5。Y-as-ranker按P(Yes)独立评价候选，N-native与M-N使用候选标签似然。排序报告HR@1、NDCG@5与MRR；NDCG截断到5，MRR使用完整候选排序。

<!-- PARAGRAPH: methods.evaluation.p02 -->
<!-- EVIDENCE: M5,C6 -->

**EN**

Random-k5 has one target and four random distractors. PopMatch-k5 draws distractors near the target's full-corpus popularity from a pool up to 10 times the needed size, excluding the target. Fixed ordered lists are shared within comparisons. This retrospective control reduces one popularity mismatch; it is not online retrieval.

**ZH**

Random-k5包含一个目标和四个随机干扰候选。PopMatch-k5依据全语料流行度，从至多为所需数量10倍的近邻池抽取干扰候选并排除目标。比较内部共享固定有序列表。这一回顾性控制减弱一项流行度失配，但不模拟在线检索。

<!-- PARAGRAPH: methods.evaluation.p03 -->
<!-- EVIDENCE: C6,M5 -->

**EN**

Hard-k20 and hard-k50 evaluate N96 and M1-96 on shared examples and ordered candidates within each protocol. Their candidate sets are separately constructed and non-nested, so count and composition change together. They test protocol-conditioned robustness rather than isolate candidate size.

**ZH**

Hard-k20与hard-k50在各协议内部以共享样本和有序候选评估N96与M1-96。候选集分别构造且非嵌套，因此数量与组成共同变化。它们检验协议条件下的稳健性，而非隔离候选规模。

<!-- PARAGRAPH: methods.evaluation.p04 -->
<!-- EVIDENCE: M1,M10,C10 -->

**EN**

To ensure cross-task holdout integrity for the shared adapter, M1-N comparisons are restricted to a cross-task-safe subset of N evaluation examples. For an example e=(u,t), we retain it only when its target was not consumed as an M1 Y-training target, did not enter the history of any later M1 Y-training example, and no M1 Y-training target for user u has a timestamp at or after t. The M1 N-training branch has 0 target or history overlap with the retained N holdouts. N and M1-N are evaluated on exactly the same retained examples. Training follows the task-specific streams; this additional criterion is an evaluation-side restriction, not a joint temporal cutoff used during training.

**ZH**

为保证共享adapter的跨任务留出完整性，M1-N比较仅在N评估样本的cross-task-safe subset上进行。对于样本e=(u,t)，仅当其目标未被M1的Y训练分支作为训练目标消费、未进入任何更晚M1 Y训练样本的历史，且用户u不存在时间戳不早于t的M1 Y训练目标时，才予以保留。M1的N训练分支与保留N留出集的目标及历史重叠均为0。N与M1-N在完全相同的保留样本上评估。训练仍采用各任务自己的训练流；这一附加准则只作用于评估侧，并非训练时采用的联合时间截断。

<!-- PARAGRAPH: methods.evaluation.p05 -->
<!-- EVIDENCE: M10,C10 -->

**EN**

Cross-task-safe coverage is 5,494/5,675 (96.81%) on M1-48 validation, 5,600/5,675 (98.68%) on its test, 5,318/5,675 (93.71%) on M1-96 validation, and 5,535/5,675 (97.53%) on its test [TABLE: hard_candidate_compact]. For the seed42 comparison from 48k to 96k, we use the intersection of the M1-48 and M1-96 masks, giving the same 5,318 validation and 5,535 test examples at both exposure points.

**ZH**

cross-task-safe subset在M1-48验证集上保留5,494/5,675（96.81%），测试集保留5,600/5,675（98.68%）；在M1-96验证集上保留5,318/5,675（93.71%），测试集保留5,535/5,675（97.53%）[TABLE: hard_candidate_compact]。seed42的48k至96k比较取M1-48与M1-96 mask的交集，使两个曝光点在相同的5,318个验证样本和5,535个测试样本上比较。
