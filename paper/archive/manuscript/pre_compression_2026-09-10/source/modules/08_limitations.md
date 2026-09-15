---
id: limitations
title: {en: Limitations, zh: 局限性}
status: draft
---

<!-- PARAGRAPH: limitations.training.p01 -->
<!-- EVIDENCE: C2,C3,C4,C5,C6,M3,M6 -->

**EN**

The 96k operating point has independent training-run replication across seeds 42, 43, and 44, whereas the full MovieLens exposure trajectories remain seed42-only. This coverage supports the observed Y96/N96/M1-96 relationship at 96k, not a multiseed exposure curve through N200. Three-run means and sample standard deviations describe training-run variability, while seed42 paired bootstrap intervals describe evaluation-sample uncertainty for fixed trained models; neither establishes cross-seed significance. Validation guided selection, and frozen test results provide held-out generalization evidence. The analysis specifies neither an equivalence margin nor multiplicity-adjusted inference across all comparisons. The evaluated ranges end at 96k for Y and 200k for N, leaving later behavior and convergence unresolved. Exposure varies sample coverage and optimization history together. M1 per-task counts are schedule-based expectations conditional on correct resume data skipping, with no retained per-example sampler trace.

**ZH**

96k运行点已有seed42、43和44的独立训练复现，完整MovieLens曝光轨迹仍仅来自seed42。这一覆盖支持96k时观察到的Y96/N96/M1-96关系，不构成直到N200的多种子曝光曲线。三次运行的均值与样本标准差描述训练运行间变异，seed42配对bootstrap区间则描述固定已训练模型的评估样本不确定性；二者均不提供跨种子显著性结论。验证集指导选择，冻结测试结果提供留出泛化证据。分析未设定等价界限，也未对所有比较实施多重性校正推断。Y与N的已评估范围分别止于96k和200k，后续行为及收敛情况仍未确定。曝光同时改变样本覆盖与优化历程。M1每任务计数是基于调度的预期值，以续训正确跳过已读数据为条件，现有记录缺少逐样本采样轨迹。

<!-- PARAGRAPH: limitations.evaluation.p01 -->
<!-- EVIDENCE: C1,C5,C6,M1,M5 -->

**EN**

The evaluation protocols define the reach of the reported capability comparisons. Popularity-matched k5 and randomly sampled k20/k50 are non-nested, so candidate count, composition, sampling method, and difficulty vary jointly. PopMatch uses full-corpus popularity and is therefore retrospective; it reduces a target-distractor mismatch while leaving other popularity-related effects possible. Y and N also differ jointly in target construction, task datasets, prompts, and scoring interfaces, so the capability contrast concerns the supervision formulations as a whole. The reported candidate-ranking comparisons use sampled sets, not exhaustive full-catalog evaluation.

**ZH**

评估协议决定了所报告能力比较的适用范围。流行度匹配k5与随机采样k20/k50为非嵌套关系，候选数量、组成、采样方法及难度共同变化。PopMatch使用全语料流行度，因此属于回顾性评估；它减弱目标与干扰候选间的一项失配，其他流行度相关影响仍可能存在。Y与N的目标构造、任务数据集、提示及评分接口也共同变化，因此能力对照针对完整监督形式。本文报告的候选排序比较使用采样集合，并非穷尽全目录的评估。

<!-- PARAGRAPH: limitations.cross_dataset.p01 -->
<!-- EVIDENCE: C8,C2,C3,C4,C5,C6 -->

**EN**

Cross-dataset support is concentrated on the ranking-side directions. Amazon results use seed42 at earlier operating points and cover the available test ranking comparisons. They do not replicate exposure trajectories, the three-seed 96k operating point, or hard-candidate robustness in that domain. A corresponding native preference validation is also needed before extending the MovieLens preference findings across datasets. The detailed exposure and protocol findings therefore remain specific to the MovieLens study.

**ZH**

跨数据集支撑集中在排序侧方向上。Amazon 结果使用较早运行点的 seed42，覆盖现有测试排序比较。这些结果未在该领域复现曝光轨迹、三种子的96k运行点或较难候选鲁棒性。将 MovieLens 偏好发现推广到第二个数据集，也需要对应的原生偏好验证。因此，详细的曝光与协议发现仍限定于 MovieLens 研究。

<!-- PARAGRAPH: limitations.compute.p01 -->
<!-- EVIDENCE: C7,M2,M3,M7 -->

**EN**

Task-sample matching leaves important resource differences between the models. The LLM comparison starts from a pretrained base, whereas the evaluated SASRec baseline learns its sequence representation from the recommendation data. Exposure counts neither match pretraining nor equate token counts, parameter updates, FLOPs, or wall-clock training time. Serving latency and end-to-end deployment cost are outside the measured outcomes. These findings concern ranking performance under approximately matched downstream task-sample exposure in the evaluated implementations and training regimes.

**ZH**

任务样本匹配仍保留了模型间重要的资源差异。LLM 从预训练底座出发，被评估的 SASRec 基线则从推荐数据学习序列表示。曝光计数既不匹配预训练，也不对齐 token 数、参数更新次数、FLOPs 或实际训练时间。服务延迟与端到端部署成本不在已测结果之内。这些发现针对被评估实现和训练条件下，近似匹配下游任务样本曝光时的排序表现。
