---
id: task_definition
title:
  en: Preference, Next Interaction, and Multitask Interfaces
  zh: 偏好、下一交互与多任务接口
status: draft
---

<!-- PARAGRAPH: methods.task.p01 -->
<!-- EVIDENCE: C1,M1,M4 -->

**EN**

The Y task estimates P(Like | H_10,i), with the observed rating defining Like: a rating of at least 4 yields Yes and a lower rating yields No. The full interaction sequence, including lower-rated events, supplies the history and targets for sample construction. Each model prompt pairs the target item with at most the 10 most recent strictly earlier interactions. Y-native evaluation measures discrimination between the two rating-derived classes. Scoring candidate items independently through this interface provides a bridge from preference prediction to next-interaction ranking.

**ZH**

Y 任务估计 P(Like | H_10,i)，其中 Like 由观测评分定义：评分不低于 4 时答案为 Yes，低于 4 时为 No。样本构造从包含低评分事件的完整交互序列中确定历史和目标。每条模型提示将目标物品与最多 10 条严格更早的近期交互配对。Y 原生评估衡量对两类评分标签的区分能力。通过这一接口分别为候选评分，可以建立从偏好预测到下一交互排序的桥接评估。

<!-- PARAGRAPH: methods.task.p02 -->
<!-- EVIDENCE: C1,M1,M4 -->

**EN**

The N task estimates P(NextInteraction = i | H_10,C), where C contains the observed next-interaction target and a fixed set of distractors. Its answer is the candidate label associated with that target. Targets are constructed from the full interaction sequence across all rating levels, and the model receives the same 10-interaction recent-history limit as Y. A distractor denotes an alternative to the observed next event, not a confirmed dislike. Previously encountered items remain eligible as distractors under the candidate protocol.

**ZH**

N 任务估计 P(NextInteraction = i | H_10,C)，其中 C 包含观测到的下一交互目标和一组固定干扰候选。答案是目标物品对应的候选标签。目标从覆盖全部评分等级的完整交互序列中构造，模型输入采用与 Y 相同的最近 10 条历史限制。干扰候选表示相对于观测下一事件的其他选项，不是已确认的负偏好。候选协议允许用户曾经接触过的物品作为干扰候选。

<!-- PARAGRAPH: methods.task.p03 -->
<!-- EVIDENCE: C1,M3,M4 -->

**EN**

M1 interleaves Y and N examples within one shared adapter while retaining their task-specific prompts and answer spaces. M-Y denotes its preference scoring interface and M-N its candidate-selection interface. A matched per-task comparison pairs each interface with a specialist that has received the corresponding task exposure. Because M1 receives both types of examples, its total exposure is the sum of the two task exposures. This design evaluates how closely one adapted model approaches both specialized capability profiles.

**ZH**

M1 在一个共享 adapter 中交错使用 Y 和 N 样本，同时保留各自的任务提示与答案空间。M-Y 表示其偏好评分接口，M-N 表示其候选选择接口。每任务曝光对齐的比较，将各接口与获得对应任务曝光的专家配对。由于 M1 同时接收两类样本，其总曝光为两项任务曝光之和。这一设计评估同一个适配模型与两种专门能力结构的接近程度。
