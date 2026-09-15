---
id: rw_evaluation_baselines
title:
  en: Evaluation and Baseline Comparison
  zh: 评估与基线比较
status: draft
---

<!-- PARAGRAPH: rw.evaluation.p01 -->
<!-- EVIDENCE: C5,C6,M5,S10,S11,S12,S16 -->

**EN**

Candidate construction can alter offline ranking conclusions: sampled metrics need not preserve exact-metric orderings, and sampling strategy can affect measurements and model rankings [@krichene2020sampled; @pereira2025sampling]. Target-set construction and difficult retrieved candidates provide related precedents [@canamares2020target; @zhang2023instructrec]. Candidate sensitivity is therefore established. We use separate non-nested protocols to delimit the higher-exposure specialist-multitask relationship, without isolating candidate count from composition or sampling.

**ZH**

候选构造能够改变离线排序结论：采样指标不必保留精确指标的模型次序，采样策略也会影响测量结果和模型排序 [@krichene2020sampled; @pereira2025sampling]。target set构造与困难检索候选已有相关先例 [@canamares2020target; @zhang2023instructrec]。因此候选敏感性并非新发现；本文以独立非嵌套协议限定较高曝光下的专家-多任务关系，不把候选数量与组成或采样方式隔离开来。

<!-- PARAGRAPH: rw.evaluation.p02 -->
<!-- EVIDENCE: C7,M3,M7,S08,S13,S14,S03,S23 -->

**EN**

Training conditions complement evaluation scope. SASRec is a sequential reference, while replicability and standardized-evaluation studies underscore careful tuning and the competitiveness of conventional baselines [@kang2018sasrec; @milogradskii2024bpr; @shehzad2025gnn]. TALLRec already compares an adapted LLM with SASRec under selected-example budgets, while sequence-scaling work studies data-pool size and repetition [@bao2023tallrec; @zhang2023seqscaling]. Our contribution is not the first budget-aware comparison: it follows both models over four approximately matched cumulative downstream-consumption points, a quantity distinct from selected examples and computation.

**ZH**

训练条件补充了评估范围。SASRec提供序列参照，复现性与标准化评价研究强调谨慎调优以及传统基线的竞争力 [@kang2018sasrec; @milogradskii2024bpr; @shehzad2025gnn]。TALLRec已按选出样本预算比较适配LLM与SASRec，序列缩放研究也考察数据池规模和重复训练 [@bao2023tallrec; @zhang2023seqscaling]。本文并非首次开展预算感知比较，其贡献是在四个累计下游消费近似匹配点追踪两类模型；这一口径不同于选出样本数和计算量。
