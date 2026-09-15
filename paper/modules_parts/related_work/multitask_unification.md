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

Unified recommendation already links task design, shared modeling, and data allocation. P5 varies derived instances while comparing single- and multitask models; ITDR reports task-removal and data-subset studies; OpenOneRec specifies task-sampling weights and contrasts low-data, single-domain, and multidomain adaptation [@geng2022p5; @liu2025itdr; @zhou2025openonerec]. These are substantive data-aware multitask precedents. Our narrower question tracks specialist-shared relationships as corresponding-task cumulative exposure changes.

**ZH**

统一推荐已将任务设计、共享建模和数据分配联系起来。P5在比较单任务与多任务模型时改变衍生实例数，ITDR报告任务删除与数据子集实验，OpenOneRec明确任务采样权重并比较低数据、单域与多域适配 [@geng2022p5; @liu2025itdr; @zhou2025openonerec]。这些都是数据感知多任务研究的实质先例；本文更具体地追踪对应任务累计曝光变化时的专家-共享关系。

<!-- PARAGRAPH: rw.unified.p02 -->
<!-- EVIDENCE: C4,C5,M3,M4,S25,S22 -->

**EN**

Specialization also depends on the combined tasks or domains. Penha et al. vary added-task per-item caps when comparing specialized and shared search-recommendation models, while OneReason studies reinforcement-learning experts and a unified student [@penha2024bridging; @onerecteam2026onereason]. Rather than claiming the first data-aware specialist-shared comparison, we align cumulative exposure for each Y/N target task and then test how the resulting ranking relationship varies across candidate protocols.

**ZH**

专门化还取决于被组合的任务或领域。Penha等人在比较搜索推荐专家与共享模型时改变新增任务的单物品实例上限，OneReason则研究强化学习专家与统一学生 [@penha2024bridging; @onerecteam2026onereason]。本文不声称首次进行数据感知的专家-共享比较，而是对齐Y/N对应目标任务的累计曝光，再检验所得排序关系如何随候选协议变化。
