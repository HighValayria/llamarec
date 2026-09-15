---
id: limitations
title: {en: Limitations, zh: 局限性}
status: draft
---

<!-- PARAGRAPH: limitations.training.p01 -->
<!-- EVIDENCE: C2,C3,C4,C5,C6,M3,M6 -->

**EN**

Only the 96k operating point has independent training seeds 42/43/44; full MovieLens trajectories remain seed42-only. Cross-task-safe ranking means and sample SD describe n=3 training-run variability and have no bootstrap intervals, whereas the retained seed42 paired bootstrap describes evaluation-sample uncertainty only for the fixed Y-side models. Neither establishes cross-seed significance. Validation guided selection and frozen test provides held-out reporting. No equivalence margin or all-comparison multiplicity adjustment was used. Behavior beyond Y96/N200 is unknown, and exposure changes coverage and optimization history together. M1 per-task counts are schedule expectations conditional on correct resume skipping, without a retained per-example trace.

**ZH**

只有96k运行点包含训练seed42/43/44的独立复现，完整MovieLens轨迹仍仅来自seed42。cross-task-safe排序均值与样本标准差描述n=3训练运行间变异且没有bootstrap区间，保留的seed42配对bootstrap只描述固定Y侧模型的评估样本不确定性；二者均不提供跨seed显著性结论。验证集指导选择，冻结测试用于留出报告。研究未设等价界限，也未对全部比较作多重性校正。Y96/N200之外的行为未知，曝光还同时改变覆盖和优化历程。M1每任务计数为以正确续训跳过为条件的调度预期，缺少逐样本轨迹。

<!-- PARAGRAPH: limitations.evaluation.p01 -->
<!-- EVIDENCE: C1,C5,C6,M1,M5 -->

**EN**

Shared-model ranking comparisons use high-coverage cross-task-safe subsets rather than the entire N holdouts because Y and N use different task-specific temporal splits. This evaluation-side restriction ensures that an N target is not exposed through the shared adapter's Y-training stream; M1 was not trained under a joint temporal cutoff. Retained coverage ranges from 93.71% to 98.68%, so the conclusions apply to these retained populations. PopMatch-k5 and random k20/k50 are non-nested: count, composition, sampling, and difficulty vary jointly. PopMatch uses full-corpus popularity retrospectively, and sampled ranking is not exhaustive full-catalog evaluation.

**ZH**

由于Y与N使用不同的任务特定时间划分，共享模型的排序比较采用高覆盖率cross-task-safe子集，而不是完整N留出集。这一评估侧限制确保N目标不会经共享adapter的Y训练流被接触；M1并未在联合时间截断下训练。保留覆盖率为93.71%至98.68%，因此相关结论适用于这些保留人群。PopMatch-k5与随机k20/k50非嵌套，候选数量、组成、采样和难度共同变化。PopMatch回顾性使用全语料流行度，采样候选排序也并非穷尽全目录评估。

<!-- PARAGRAPH: limitations.cross_dataset.p01 -->
<!-- EVIDENCE: C8,C2,C3,C4,C5,C6 -->

**EN**

Amazon support is limited to seed42 ranking directions at earlier test operating points. It does not replicate exposure trajectories, the three-seed 96k point, hard-candidate robustness, or native preference validation. Detailed exposure and protocol conclusions therefore remain specific to MovieLens.

**ZH**

Amazon支撑限于较早测试运行点的seed42排序方向，未复现曝光轨迹、三seed的96k运行点、较难候选稳健性或原生偏好验证。因此，详细曝光与协议结论仍限定于MovieLens。

<!-- PARAGRAPH: limitations.compute.p01 -->
<!-- EVIDENCE: C7,M2,M3,M7 -->

**EN**

Task-sample matching does not remove resource differences. The LLM starts pretrained; SASRec learns sequence representations from recommendation data. Exposure matches neither pretraining nor tokens, updates, FLOPs, wall-clock time, serving latency, or deployment cost. Claims concern ranking under approximately matched downstream task-sample exposure in the evaluated implementations and regimes.

**ZH**

任务样本匹配不消除资源差异。LLM从预训练底座开始，SASRec从推荐数据学习序列表示。曝光不对齐预训练、token、更新、FLOPs、实际时间、服务延迟或部署成本。本文结论仅涉及被评估实现和训练条件下，下游任务样本曝光近似匹配时的排序表现。
