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

Y-native validation AUC rises from 0.7761 at 24k to 0.7844 at 96k. F1 and the Y-as-ranker metrics do not improve uniformly, so the measured Y response is limited or uneven rather than demonstrably saturated.

**ZH**

Y原生验证AUC从24k时的0.7761升至96k时的0.7844。F1与Y-as-ranker指标并未一致改善，因此Y的被测响应有限或不均匀，不能据此认定已经饱和。

<!-- PARAGRAPH: results.rq2.p02 -->
<!-- EVIDENCE: C3 -->

**EN**

N-native PopMatch-k5 validation HR@1 rises from 0.5774 at N24 to 0.6516 at N200, an absolute gain of 0.0742; the test trajectory has the same direction. [FIGURE: n_native_exposure] shows the validation trend, while [TABLE: n_vs_sasrec_exposure] retains the exact HR@1 values for both splits.

**ZH**

N原生PopMatch-k5验证HR@1从N24的0.5774升至N200的0.6516，绝对增量为0.0742；测试轨迹方向相同。[FIGURE: n_native_exposure]展示验证趋势，[TABLE: n_vs_sasrec_exposure]保留两个划分的精确HR@1数值。

<!-- PARAGRAPH: results.rq2.p03 -->
<!-- EVIDENCE: C2,C3,M3 -->

**EN**

Y and N therefore have different observed exposure-response profiles. This comparison concerns within-interface trajectories, not the numerical magnitudes of AUC and HR@1, and motivates matching corresponding task exposure in the specialist-multitask analysis.

**ZH**

Y与N由此呈现不同的已观测曝光响应。这里比较的是各自接口内的轨迹，而非AUC与HR@1的数值大小，并据此在专家与多任务分析中对齐对应任务曝光。
