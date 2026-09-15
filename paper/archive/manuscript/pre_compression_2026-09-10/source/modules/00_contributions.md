---
id: contributions
title:
  en: Contribution Working Version
  zh: 贡献工作版
status: draft
---

<!-- PARAGRAPH: contributions.p01 -->
<!-- EVIDENCE: C1,M1,M4 -->

**EN**

We frame recommendation capability through the prediction question defined by supervision. Within a shared LLM adaptation setting, rating-derived preference prediction and next-interaction prediction yield distinct observed capability profiles in native-task and bridge evaluations. This framing links capability claims to their training and scoring interfaces.

**ZH**

本文通过监督所定义的预测问题来界定推荐能力。在共同的 LLM 适配设置中，评分产生的偏好预测与下一交互预测，在原生任务和桥接评估中呈现不同的可观测能力结构。这一界定将能力声明与相应训练及评分接口联系起来。

<!-- PARAGRAPH: contributions.p02 -->
<!-- EVIDENCE: C2,C3,C4,C5,M3 -->

**EN**

We characterize how the specialist-multitask relationship changes with cumulative per-task adaptation exposure. The MovieLens seed42 trajectory traces task-specific performance and compares the shared adapter with specialists at matched exposure for the corresponding task. From 48k to 96k, the standard-k5 validation ranking gap narrows substantially; two additional training seeds independently reproduce the resulting 96k small-gap regime, while the frozen test set consistently retains a modest N advantage. At that operating point, M1 also maintains comparable measured Y-side preference performance. Read alongside the task-specific exposure responses, this change shows why a specialist advantage at a lower supervision budget does not fully characterize the shared model's capabilities after further adaptation. The full trajectory remains seed42-only, whereas the replicated operating point strengthens the exposure-specific account of specialization and unification.

**ZH**

本文刻画专家与多任务模型的关系如何随累计每任务适配曝光变化。MovieLens的seed42轨迹追踪各任务表现，并在对应任务曝光对齐时比较共享adapter与专家。从48k到96k，标准k5验证集的排序差距明显缩小；两个额外训练种子独立复现了96k的小差距区间，冻结测试集则一致保留N的小幅优势。在这一运行点，M1也保持了与Y专家接近的被测偏好表现。结合各任务的曝光响应，这一变化说明，较低监督预算下的专家优势不足以完整刻画共享模型进一步适配后的能力。完整轨迹仍仅来自seed42，而运行点复现加强了结合具体曝光解释专门化与统一建模的证据。

<!-- PARAGRAPH: contributions.p03 -->
<!-- EVIDENCE: C5,C6,M5 -->

**EN**

We show that the higher-exposure specialist-multitask relationship is also protocol-conditioned. Across three training seeds, k20 exposes a substantially larger remaining N-specialist advantage than standard k5 on validation and frozen test. The k50 protocol also favors N consistently, but with a smaller gap than k20 and seed-dependent magnitude. These separate, non-nested protocols establish the reach of the standard-k5 comparison. Their joint changes in candidate count, composition, and sampling method make protocol identity part of the result without isolating a candidate-size effect.

**ZH**

本文表明，较高曝光下的专家与多任务模型关系也受协议条件限定。三个训练种子的验证与冻结测试结果均显示，k20揭示的剩余N专家优势明显大于标准k5。k50也一致偏向N，但差距小于k20，幅度随seed变化。这些独立、非嵌套协议明确了标准k5比较的适用范围。候选数量、组成与采样方法共同变化，使协议身份成为结果的一部分，但未单独识别候选规模效应。

<!-- PARAGRAPH: contributions.p04 -->
<!-- EVIDENCE: C7,C9,M3,M7 -->

**EN**

We trace N-trained LlamaRec and SASRec across four approximately matched downstream task-sample exposure points, spanning 24k to 200k in the MovieLens study. N retains a ranking advantage at the measured points, while SASRec improves strongly with additional supervision. This trajectory places the observed LLM advantage alongside the sequential baseline's response to supervision and supports an exposure-specific interpretation of their relative performance.

**ZH**

本文在 MovieLens 研究中，沿四个近似匹配的下游任务样本曝光点追踪接受 N 任务训练的 LlamaRec 与 SASRec，覆盖 24k 至 200k。N 在已测点保有排序优势，SASRec 则随额外监督明显改善。这一轨迹将观察到的 LLM 优势与序列基线对监督量的响应并列考察，支持结合具体曝光解释二者的相对表现。
