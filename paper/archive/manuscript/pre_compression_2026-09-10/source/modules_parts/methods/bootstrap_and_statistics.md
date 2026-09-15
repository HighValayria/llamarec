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

We use paired user-level bootstrap intervals [@efron1993bootstrap] to characterize evaluation-sample uncertainty for fixed trained models. Predictions are aligned on the same targets, and users are sampled with replacement, carrying all examples of each selected user into both models' resampled data. This grouping accommodates multiple Y targets per user. Metric differences are computed on each shared resample, and the 2.5th and 97.5th percentiles form the 95% interval. Binary differences are M1-96 minus Y96, and ranking differences are N96 minus M1-96.

**ZH**

本文使用用户级配对 bootstrap 区间 [@efron1993bootstrap]，衡量固定已训练模型的评估样本不确定性。分析先对齐相同目标的预测，再以用户为单位有放回采样，将每位入选用户的全部样本同时带入两个模型的重采样数据。这种分组可以处理同一用户具有多个 Y 目标的情形。每次共享重采样均计算指标差值，取第 2.5 和第 97.5 百分位构成 95% 区间。二分类差值为 M1-96 减 Y96，排序差值为 N96 减 M1-96。

<!-- PARAGRAPH: methods.statistics.p02 -->
<!-- EVIDENCE: M6,C4,C5,C6,C9 -->

**EN**

Effect sizes and their intervals are interpreted together; zero-crossing intervals describe uncertainty in a model gap rather than establish equivalence. The full exposure trajectories use training seed42. Independent training seeds 43 and 44 replicate Y96, N96, and M1-96 at 96k, including validation and frozen-test evaluation under k5, k20, and k50 for the ranking interfaces. Cross-seed summaries use equal-weight means and sample standard deviations with n=3 training seeds and ddof=1; they describe training-run variability, not confidence intervals or statistical significance. Paired bootstrap intervals are available for seed42 only and concern within-seed evaluation-sample uncertainty. Training seeds are recorded separately from candidate-generation seed42; the replicated operating point does not constitute a multiseed exposure trajectory.

**ZH**

效应大小与区间共同用于结果解释；跨零区间描述模型差距的不确定性，并不证明等价。完整曝光轨迹使用训练seed42。独立训练seed43和44在96k复现Y96、N96与M1-96，其中排序接口覆盖k5、k20和k50的验证及冻结测试评估。跨种子汇总采用等权均值和样本标准差，n=3个训练seed，ddof=1；它们描述训练运行间变异，不是置信区间或显著性判断。配对bootstrap区间仅对应seed42，衡量单一训练seed内的评估样本不确定性。训练种子与候选生成seed42分开记录，运行点复现不构成多种子曝光轨迹。
