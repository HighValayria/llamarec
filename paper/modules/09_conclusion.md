---
id: conclusion
title: {en: Conclusion, zh: 结论}
status: draft
---

<!-- PARAGRAPH: conclusion.p01 -->
<!-- EVIDENCE: C1,C2,C3,C4,C5,C6,C7,C8 -->

**EN**

This study examined LLM recommendation conclusions across complete supervision formulations, cumulative downstream task-sample exposure, and candidate protocols. Within one adaptation setting, rating-derived preference (Y), next-interaction prediction (N), and a shared adapter (M1) represent different prediction capabilities rather than a causally isolated semantic contrast.

**ZH**

本研究考察完整监督形式、累计下游任务样本曝光和候选协议下的LLM推荐结论。在共同适配设置中，评分产生的偏好Y、下一交互预测N和共享adapter M1代表不同预测能力，而非某个被因果隔离的语义对照。

<!-- PARAGRAPH: conclusion.p02 -->
<!-- EVIDENCE: C1,C2,C3,C4,C5,C6,C7,M3,M5,M7 -->

**EN**

On the common cross-task-safe subset, the seed42 specialist-M1 validation gap narrows from 48k to 96k across all three ranking metrics, while the test subset does not reproduce that narrowing. Independent seeds replicate only the 96k operating point, where ranking consistently favors N and M1 preserves comparable Y-side capability. Thus, specialist-shared performance is exposure and protocol conditioned rather than universally equivalent. Across four approximately matched downstream exposure points, N-trained LlamaRec leads SASRec, but SASRec continues improving and narrows the later gap; this is a task-sample exposure comparison, not a resource-efficiency claim.

**ZH**

在共同cross-task-safe子集上，seed42专家-M1验证差距在三个排序指标上均从48k到96k收窄，而测试子集没有复现这一收窄。独立训练seed只复现96k运行点；此时排序一致偏向N，M1则保持接近的Y侧能力。因此，专家-共享表现受曝光和协议限定，并非普遍等价。在四个下游曝光近似匹配点上，N训练的LlamaRec领先SASRec，但SASRec继续改善并缩小后期差距；这属于任务样本曝光比较，不是资源效率结论。

<!-- PARAGRAPH: conclusion.p03 -->
<!-- EVIDENCE: C1,C2,C3,C4,C5,C6,C7,C8 -->

**EN**

Claims about adapted language models for recommendation should therefore report the prediction formulation, cumulative downstream task-sample exposure, and candidate evaluation protocol together. These conditions define which capability and relative model performance the evidence supports.

**ZH**

因此，关于推荐适配语言模型的结论应同时报告预测形式、累计下游任务样本曝光和候选评估协议。这些条件共同界定现有证据支持何种能力与模型相对表现。
