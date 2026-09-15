---
id: discussion_exposure_interpretation
title:
  en: Exposure Changes What a Model Comparison Means
  zh: 曝光改变模型比较的含义
status: draft
---

<!-- PARAGRAPH: discussion.exposure.p01 -->
<!-- EVIDENCE: C2,C3,M3 -->

**EN**

Exposure determines where a model comparison lies along the observed adaptation trajectory. In the seed42 study, N continues to improve across its evaluated range, whereas Y's measured gains are limited or uneven across metrics. A comparison made at an early checkpoint therefore describes an early operating point whose relation to later performance depends on the task. The contrast motivates treating task-sample exposure as an experimental variable in the main analysis.

**ZH**

曝光决定了一次模型比较位于所观察适配轨迹的哪个位置。在 seed42 研究中，N 在其已评估范围内持续改善，Y 在不同指标上的被测增益则有限或不均匀。因此，较早检查点上的比较描述的是早期运行状态，它与后续表现的关系取决于任务。这一对照提示我们，应将任务样本曝光作为主要分析中的实验变量。

<!-- PARAGRAPH: discussion.exposure.p02 -->
<!-- EVIDENCE: C3,C5,C7,M3 -->

**EN**

Task-specific accounting is especially useful when training objectives consume examples differently. For multitask models, total exposure and per-task exposure answer different allocation questions; for the sequential baseline, actual example counts make the comparison interpretable across batch sizes. Reporting the evaluated exposure points alongside the performance trajectory clarifies how much task supervision supports a claimed advantage. This practice turns training budget from a background configuration into an explicit condition of the result.

**ZH**

当训练目标以不同方式消耗样本时，按任务统计尤其有用。对于多任务模型，总曝光与每任务曝光回答不同的分配问题；对于序列基线，实际样本计数使不同 batch size 下的比较具有明确含义。在性能轨迹旁报告已评估曝光点，可以说明一项优势建立在多少任务监督之上。这种做法将训练预算从背景配置变为结果的明确条件。
