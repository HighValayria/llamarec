---
id: rq2_exposure_response
title:
  en: Task-Specific Response to Training Exposure
  zh: 不同任务对训练曝光的响应
status: draft
---

<!-- PARAGRAPH: results.rq2.p01 -->
<!-- EVIDENCE: C2 -->

**EN**

Y-native validation AUC shows a smaller gain in the later exposure interval, rising from 0.7761 at 24k to 0.7816 at 48k and 0.7844 at 96k. Validation F1 changes from 0.7792 to 0.7848 and then 0.7783, while Y-as-ranker validation NDCG@5 stays within 0.5995-0.6031. Y's measured validation response is therefore limited and uneven across metrics. [TABLE: binary_exposure] [TABLE: semantics_bridge]

**ZH**

Y 原生验证 AUC 在后一曝光区间的增量较小，从 24k 的 0.7761 上升至 48k 的 0.7816 和 96k 的 0.7844。验证 F1 从 0.7792 变为 0.7848，再变为 0.7783，而 Y-as-ranker 的验证 NDCG@5 始终处于 0.5995-0.6031 之间。因此，在这些验证指标上，Y 的被测增益较为有限，且变化并不一致。[TABLE: binary_exposure] [TABLE: semantics_bridge]

<!-- PARAGRAPH: results.rq2.p02 -->
<!-- EVIDENCE: C3 -->

**EN**

N-native ranking continues to improve through the longer exposure range. PopMatch-k5 validation HR@1 rises from 0.5774 at N24 to 0.6030 at N48, 0.6238 at N96, and 0.6516 at N200, an absolute increase of 0.0742 between the endpoints. NDCG@5 and MRR improve at each reported point, reaching 0.8432 and 0.7904 at N200. Test HR@1 follows the same direction, increasing through 0.5612, 0.5870, 0.6100, and 0.6282. The two splits therefore consistently show continued gains over the measured N trajectory. [TABLE: exposure_scaling] [FIGURE: n_native_exposure]

**ZH**

N 原生排序在更长的曝光范围内持续改善。PopMatch-k5 验证 HR@1 从 N24 的 0.5774 上升至 N48 的 0.6030、N96 的 0.6238 和 N200 的 0.6516，两端绝对增量为 0.0742。NDCG@5 与 MRR 在每个报告点也都上升，在 N200 分别达到 0.8432 和 0.7904。测试 HR@1 呈现相同方向，依次增至 0.5612、0.5870、0.6100 和 0.6282。因此，两个划分均显示 N 在已测轨迹上持续获益。[TABLE: exposure_scaling] [FIGURE: n_native_exposure]

<!-- PARAGRAPH: results.rq2.p03 -->
<!-- EVIDENCE: C2,C3,M3 -->

**EN**

Y and N consequently exhibit different exposure-response profiles: Y shows limited or uneven measured gains through 96k, while N ranking continues to improve on both splits through 200k. The comparison concerns response profiles, not the numerical magnitudes of AUC and HR@1. These trajectories make exposure relevant to the interpretation of a model gap, because comparisons at different operating points can describe different degrees of adaptation. The next comparison therefore examines specialists and M1 after matching the exposure received by each task.

**ZH**

因此，Y 与 N 呈现不同的曝光响应形态：Y 到 96k 的被测增益有限或不均匀，N 排序则在两个划分上均持续改善到 200k。这里比较的是响应形态，不是 AUC 与 HR@1 的数值大小。上述轨迹表明，解释模型差距时需要考虑曝光，因为不同运行点可能对应不同程度的适配。由此，接下来的比较在每项任务所获曝光对齐后，考察专家与 M1 的关系。
