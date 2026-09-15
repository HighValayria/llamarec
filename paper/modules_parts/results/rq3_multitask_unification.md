---
id: rq3_multitask_unification
title:
  en: Specialist and Multitask Models at Matched Per-Task Exposure
  zh: 每任务曝光对齐下的专家与多任务模型
status: draft
---

<!-- PARAGRAPH: results.rq3.p01 -->
<!-- EVIDENCE: C4,M3 -->

**EN**

At 96k expected exposure per task, M1 retains comparable measured Y-side preference capability across three training seeds. M1-Y validation AUC and F1 are slightly higher in each seed, whereas accuracy is lower by 0.00089 for seed44. [TABLE: specialist_multitask] reports the seed42 paired user bootstrap for this binary Y-side comparison: only the F1 interval is positive, while AUC and accuracy intervals cross zero. This supports capability preservation, not equivalence or positive transfer across training seeds.

**ZH**

在每任务预期曝光96k时，M1在三个训练seed上保持了与Y专家接近的被测偏好能力。各seed的M1-Y验证AUC与F1略高，但seed44的Accuracy低0.00089。[TABLE: specialist_multitask]报告这一Y侧二分类比较的seed42用户级配对bootstrap：仅F1区间为正，AUC与Accuracy区间跨零。这些证据支持能力保留，不证明等价或跨训练seed正迁移。

<!-- PARAGRAPH: results.rq3.p02 -->
<!-- EVIDENCE: C5,M3 -->

**EN**

On the common cross-task-safe validation subset in [TABLE: exposure_scaling], the seed42 standard-k5 N-specialist-M1 gap narrows from 48k to 96k per task across all three metrics. The HR@1 gap falls from +0.01072 to +0.00132; NDCG@5 and MRR show the same direction. Independent seeds 43 and 44 reproduce a small but consistently positive N advantage at 96k: [TABLE: ms96_delta_summary_compact] reports a three-seed validation HR@1 mean delta of +0.00708 with sample SD 0.00934 and 3/3 positive directions. The full exposure trajectory remains seed42-only.

**ZH**

在[TABLE: exposure_scaling]的共同cross-task-safe验证子集上，seed42标准k5的N专家-M1差距在三个指标上均从每任务48k到96k收窄。HR@1差距由+0.01072降至+0.00132，NDCG@5与MRR方向相同。seed43和44独立复现了96k时小幅但方向一致的N优势：[TABLE: ms96_delta_summary_compact]报告三seed验证HR@1平均差值为+0.00708、样本标准差为0.00934，且3/3方向为正。完整曝光轨迹仍仅来自seed42。

<!-- PARAGRAPH: results.rq3.p03 -->
<!-- EVIDENCE: C4,C5 -->

**EN**

Frozen tests retain an N advantage in every seed at 96k. [TABLE: ms96_delta_summary_compact] reports a three-seed HR@1 mean delta of +0.01072 with sample SD 0.00271 and 3/3 positive directions. On the common seed42 test subset in [TABLE: exposure_scaling], however, the HR@1 gap changes from +0.00939 at 48k to +0.01373 at 96k, and NDCG@5 and MRR likewise do not narrow. The validation-side exposure trajectory is therefore not reproduced on test.

**ZH**

96k冻结测试在每个seed上均保留N优势。[TABLE: ms96_delta_summary_compact]报告三seed的HR@1平均差值为+0.01072、样本标准差为0.00271，且3/3方向为正。然而，在[TABLE: exposure_scaling]的共同seed42测试子集上，HR@1差距由48k的+0.00939变为96k的+0.01373，NDCG@5与MRR同样未收窄。因此，验证侧的曝光轨迹没有在测试集复现。
