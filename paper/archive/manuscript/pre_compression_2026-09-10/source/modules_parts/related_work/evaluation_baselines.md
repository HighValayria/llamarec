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

Candidate construction can change the conclusions drawn from offline ranking evaluation. Sampled metrics need not preserve the model ordering of exact metrics, and uniform, popularity-based, and full-catalog evaluation can yield different comparisons [@krichene2020sampled; @dallmann2021sampling]. In the terminology of Cañamares and Castells, the target set is the set of items scored for evaluation, whose construction includes unrated alternatives alongside test items [@canamares2020target]. Harder candidate evaluation also has precedents in adapted language models: InstructRec evaluates reranking with difficult retrieved candidates [@zhang2023instructrec]. Our analysis applies this concern to the higher-exposure N-specialist versus multitask relationship. Separate non-nested candidate protocols characterize its evaluation dependence, with candidate size and composition varying together.

**ZH**

候选构造能够改变离线排序评估得出的结论。采样指标不必保留精确指标对应的模型次序，均匀采样、流行度采样与全库评估也可能产生不同的比较结果 [@krichene2020sampled; @dallmann2021sampling]。在 Cañamares 和 Castells 的术语中，target set 指评估时待评分的物品集合，其构造在测试物品之外还包含未评分的备选项 [@canamares2020target]。适配语言模型的较难候选评估也已有先例：InstructRec 使用检索得到的困难候选评价重排序 [@zhang2023instructrec]。本文将这一关注具体用于较高曝光下 N 专家与多任务模型的关系。独立、非嵌套候选协议刻画这种关系对评估的依赖，其中候选数量与组成共同变化。

<!-- PARAGRAPH: rw.evaluation.p02 -->
<!-- EVIDENCE: C7,M3,M7,S08,S13,S14,S03,S23 -->

**EN**

Training conditions provide a complementary basis for interpreting baseline comparisons. SASRec supplies a specialized sequential reference, while reproducibility analyses and iALS re-evaluation demonstrate the importance of baseline tuning [@kang2018sasrec; @dacrema2019progress; @rendle2022ials]. TALLRec already compares an adapted LLM with baselines including SASRec at matched selected-example budgets and studies a range of few-shot sample counts [@bao2023tallrec]. Sequential recommendation scaling research also examines both data-pool size and repeated training [@zhang2023seqscaling]. Selected-example count, cumulative sample consumption, and computation describe different resources. Our comparison follows N-trained LlamaRec and SASRec across four approximately matched cumulative downstream task-exposure points from 24k to 200k, relating the observed LLM advantage to the baseline's continued gains under additional supervision.

**ZH**

训练条件为解释基线比较提供了互补依据。SASRec 提供专门的序列参照，可复现性分析与 iALS 再评估则展示了基线调优的重要性 [@kang2018sasrec; @dacrema2019progress; @rendle2022ials]。TALLRec 已在选出训练样本数相同的预算下，将适配后的 LLM 与包括 SASRec 在内的基线比较，并研究不同少样本数量 [@bao2023tallrec]。序列推荐缩放研究也已考察数据池大小与重复训练 [@zhang2023seqscaling]。选出样本数、累计样本消费和计算量描述的是不同资源。本文沿四个从 24k 至 200k 的近似匹配累计下游任务曝光点，追踪接受 N 任务训练的 LlamaRec 与 SASRec，将观察到的 LLM 优势与基线在额外监督下的持续收益联系起来。
