---
id: bootstrap_and_statistics
title:
  en: Statistical Analysis and Training Seeds
  zh: 统计分析与训练种子
status: draft
---

<!-- PARAGRAPH: methods.statistics.p01 -->
<!-- EVIDENCE: M6,C4,C5,C6 -->

**EN**

Paired user-level bootstrap intervals [@efron1993bootstrap] describe evaluation-sample uncertainty for the fixed seed42 Y96 and M1-Y96 models. Predictions share targets; users are resampled with replacement and all their examples enter both models' resamples. Each resample yields the binary M1-Y minus Y96 metric difference, whose 2.5th and 97.5th percentiles form the 95% interval. These intervals support only the Y-side binary comparison; cross-task-safe M1-N ranking results are reported without bootstrap intervals.

**ZH**

用户级配对bootstrap区间 [@efron1993bootstrap]描述固定seed42 Y96与M1-Y96模型的评估样本不确定性。预测按相同目标对齐，以用户为单位有放回采样，并将入选用户的全部样本同时带入两个模型。每次重采样计算M1-Y减Y96的二分类指标差值，第2.5与97.5百分位构成95%区间。这些区间只支撑Y侧二分类比较；cross-task-safe M1-N排序结果不报告bootstrap区间。

<!-- PARAGRAPH: methods.statistics.p02 -->
<!-- EVIDENCE: M6,C4,C5,C6,C9 -->

**EN**

Zero-crossing Y-side intervals indicate uncertainty, not equivalence. Full trajectories use training seed42; seeds 43/44 independently replicate Y96, N96, and M1-96 at 96k on validation and frozen test under k5/k20/k50. Cross-task-safe ranking summaries report point estimates, equal-weight means, sample SD with n=3 and ddof=1, and per-seed directions. They describe training-run variability, not confidence intervals, significance, equivalence, or a multiseed trajectory. Candidate-generation seed42 is recorded separately from the three training seeds.

**ZH**

Y侧跨零区间表示不确定，并不证明等价。完整轨迹使用训练seed42；seed43/44在96k独立复现Y96、N96与M1-96，并覆盖验证、冻结测试及k5/k20/k50。cross-task-safe排序汇总报告点估计、n=3且ddof=1的等权均值与样本标准差，以及逐seed方向。它们描述训练运行间变异，不是置信区间、显著性判断、等价性判断或多seed轨迹。候选生成seed42与三个训练seed分别记录。
