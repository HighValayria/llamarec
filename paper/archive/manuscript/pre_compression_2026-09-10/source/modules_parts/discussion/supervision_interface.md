---
id: discussion_supervision_interface
title:
  en: Recommendation Ability Depends on the Supervision Interface
  zh: 推荐能力取决于监督接口
status: draft
---

<!-- PARAGRAPH: discussion.semantics.p01 -->
<!-- EVIDENCE: C1,C2,M1,M4 -->

**EN**

Recommendation capability is most informative when stated as an ability to answer a particular prediction question. Y measures whether an item is likely to receive a positive rating, whereas N selects the next observed interaction from candidates. The strong contrast between Y-native preference discrimination and its bridge ranking performance shows that these interfaces assess different aspects of recommendation behavior. A preference model can consequently be useful on its intended target while a next-interaction model is better suited to event selection.

**ZH**

将推荐能力表述为回答某个具体预测问题的能力，才能明确其含义。Y 衡量物品是否可能获得正评分，N 则从候选中选择下一次观测交互。Y 原生偏好判别与桥接排序表现之间的鲜明对照，说明这些接口评估的是推荐行为的不同方面。因此，偏好模型可以在预定目标上发挥作用，而下一交互模型更适合事件选择。

<!-- PARAGRAPH: discussion.semantics.p02 -->
<!-- EVIDENCE: C1,M1,M4 -->

**EN**

This distinction makes the supervision formulation part of benchmark interpretation. A benchmark's target, eligible events, prompt, and scoring rule jointly determine the capability reflected in its score. Reporting both native-task performance and a bridge evaluation exposes the relationship between capabilities that a single ranking number can obscure. The Y/N comparison thus supports a task-specific description of LLM recommendation ability, with preference and next-interaction prediction kept conceptually separate.

**ZH**

这一区别使监督形式成为解释基准结果时的一部分。基准的预测目标、符合条件的事件、提示和评分规则，共同决定其分数反映的能力。结合原生任务表现与桥接评估，可以呈现单一排序分数容易掩盖的能力关系。因此，Y/N 对照支持按任务描述 LLM 推荐能力，在概念上区分偏好预测与下一交互预测。
