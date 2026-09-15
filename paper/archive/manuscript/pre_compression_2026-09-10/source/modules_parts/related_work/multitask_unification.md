---
id: rw_multitask_unification
title:
  en: Multitask and Unified Recommendation Modeling
  zh: 多任务与统一推荐建模
status: draft
---

<!-- PARAGRAPH: rw.unified.p01 -->
<!-- EVIDENCE: S02,S15,S21 -->

**EN**

Unified recommendation research already connects task design, shared modeling, and training-data allocation. P5 compares single-task and multitask models and, in its extended appendix, varies the number of derived training instances per interaction [@geng2022p5]. ITDR reports task-removal ablations and separate data-subset experiments, linking instruction composition and data sensitivity without a full crossed design [@liu2025itdr]. OpenOneRec specifies SFT task-sampling weights and compares low-data, full single-domain, and full multidomain adaptation settings [@zhou2025openonerec]. These studies provide substantive precedents for examining specialized performance and supervision allocation together. They motivate a more specific question about how specialist-shared relationships evolve when cumulative supervision for the corresponding task is made explicit.

**ZH**

统一推荐研究已经将任务设计、共享建模与训练数据分配联系起来。P5 比较单任务与多任务模型，并在扩展附录中改变每条交互所衍生的训练实例数 [@geng2022p5]。ITDR 分别报告任务删除消融和数据子集实验，将指令构成与数据敏感性联系起来，但未采用完整交叉设计 [@liu2025itdr]。OpenOneRec 明确 SFT 任务采样权重，并比较低数据、全量单域和全量多域适配设置 [@zhou2025openonerec]。这些研究为共同考察专门任务表现与监督分配提供了实质先例，也引出一个更具体的问题：明确对应任务的累计监督后，专家与共享模型的关系如何演变？

<!-- PARAGRAPH: rw.unified.p02 -->
<!-- EVIDENCE: C4,C5,M3,M4,S25,S22 -->

**EN**

The meaning of specialization also depends on which tasks or domains are combined. Penha et al. adapt Flan-T5 for search and recommendation, comparing specialized and shared models while varying per-item training-instance caps for the added task [@penha2024bridging]. This examines auxiliary-task data allocation, including its popularity distribution, rather than tracking matched cumulative exposure for the target task. OneReason studies domain-specific reinforcement-learning experts and a unified student, providing a different setting for retaining specialized performance [@onerecteam2026onereason]. Our comparison follows Y/N task specialists and a shared adapter at matched corresponding-task exposure. It then examines how the resulting ranking relationship carries across candidate protocols.

**ZH**

专门化的含义也取决于组合了哪些任务或领域。Penha 等人将 Flan-T5 适配到搜索与推荐，比较专门与共享模型，并改变新增任务中每个物品的训练实例上限 [@penha2024bridging]。这一设计考察的是辅助任务数据分配及其流行度分布，而非追踪目标任务累计曝光对齐下的关系。OneReason 研究领域特定的强化学习专家与统一学生，为专门表现的保留提供另一种研究设置 [@onerecteam2026onereason]。本文则在对应任务曝光对齐时，追踪 Y/N 任务专家与共享 adapter 的比较，并进一步考察所得排序关系在不同候选协议下的表现。
