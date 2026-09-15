---
id: discussion
title: {en: Discussion, zh: 讨论}
status: draft
---

<!-- PARAGRAPH: discussion.p01 -->
<!-- EVIDENCE: C1,C2,C3,C4,C5,C6,C7,C8 -->

**EN**

The findings make supervision interface, training exposure, and evaluation protocol central to the interpretation of LLM recommendation performance. Each specifies a different part of the comparison: the prediction question, the amount of task supervision, and the conditions under which ranking is measured. Considering them together explains why model relationships can change across otherwise plausible experimental settings. The following discussion develops the implications for capability assessment, multitask learning, and baseline comparison.

**ZH**

这些发现表明，监督接口、训练曝光与评估协议是解释 LLM 推荐表现的关键。三者分别确定比较中的不同部分：预测问题、任务监督量，以及测量排序表现的条件。将它们结合起来，有助于解释模型关系为何会在不同且各有依据的实验设置中发生变化。下文进一步讨论这对能力评估、多任务学习和基线比较的意义。

<!-- INCLUDE: paper/modules_parts/discussion/supervision_interface.md -->
<!-- INCLUDE: paper/modules_parts/discussion/exposure_interpretation.md -->
<!-- INCLUDE: paper/modules_parts/discussion/conditional_unification.md -->
<!-- INCLUDE: paper/modules_parts/discussion/evaluation_protocol.md -->
<!-- INCLUDE: paper/modules_parts/discussion/exposure_aware_baselines.md -->
<!-- INCLUDE: paper/modules_parts/discussion/external_validity.md -->

<!-- PARAGRAPH: discussion.synthesis.p01 -->
<!-- EVIDENCE: C1,C2,C3,C4,C5,C6,C7 -->

**EN**

Together, the findings support an account of recommendation capability and relative performance that remains tied to the evaluated setting. Supervision formulation specifies the prediction capability being trained and measured, cumulative per-task exposure locates the comparison along the observed adaptation trajectory, and candidate protocol defines the ranking conditions. The SASRec trajectory extends this interpretation across model families: N's advantage at the measured points coexists with continued baseline improvement.

**ZH**

这些发现共同支持在已评估设置内解释推荐能力与模型相对表现。监督形式明确被训练和测量的预测能力，累计每任务曝光确定比较在已观测适配轨迹上的位置，候选协议则界定排序评估的条件。SASRec轨迹将这一解释延伸到不同模型系列之间：N在已测点上的优势，与基线持续改善的表现同时存在。
