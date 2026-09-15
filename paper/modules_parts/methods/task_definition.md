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

Y estimates P(Like | H_10,i), where ratings at least 4 map to Yes and lower ratings to No. The complete sequence, including low-rated events, supplies histories and targets. Native evaluation measures rating-derived class discrimination; independently scoring candidates through P(Yes) provides the bridge to next-interaction ranking.

**ZH**

Y估计P(Like | H_10,i)，评分不低于4映射为Yes，较低评分映射为No。包含低评分事件的完整序列用于构造历史与目标。原生评估衡量评分标签判别，通过P(Yes)独立评价候选则形成通向下一交互排序的桥接。

<!-- PARAGRAPH: methods.task.p02 -->
<!-- EVIDENCE: C1,M1,M4 -->

**EN**

N estimates P(NextInteraction = i | H_10,C), where C contains the observed next item and fixed distractors; the answer is the target's candidate label. Targets use all rating levels. A distractor is an alternative to the observed next event, not a confirmed dislike, and previously encountered items remain eligible.

**ZH**

N估计P(NextInteraction = i | H_10,C)，其中C包含观测下一物品和固定干扰候选，答案为目标的候选标签。目标覆盖全部评分等级。干扰候选是观测下一事件的备选项，而非确认的不喜欢；用户曾接触的物品仍可作为候选。

<!-- PARAGRAPH: methods.task.p03 -->
<!-- EVIDENCE: C1,M3,M4 -->

**EN**

M1 interleaves Y and N within one shared adapter while retaining task-specific prompts and answer spaces. M-Y and M-N denote its two scoring interfaces. Each is compared with the corresponding specialist at matched task exposure; M1 total exposure is the sum across tasks.

**ZH**

M1在一个共享adapter中交错使用Y与N，同时保留任务特定提示和答案空间。M-Y与M-N表示两条评分接口，各自与对应任务曝光匹配的专家比较；M1总曝光为两项任务曝光之和。
