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

We characterize how the specialist-multitask relationship changes with cumulative per-task adaptation exposure. On a common cross-task-safe MovieLens subset, the seed42 standard-k5 validation gap narrows from 48k to 96k across all three ranking metrics. Two additional training seeds independently reproduce a small but consistently positive N advantage at the 96k operating point, while the common seed42 test subset does not reproduce the validation-side narrowing. At that operating point, M1 also maintains comparable measured Y-side preference performance. The full trajectory remains seed42-only, whereas the replicated operating point strengthens an exposure-specific account of specialization and unification without implying equivalence or positive transfer.

**ZH**

本文刻画专家与多任务模型的关系如何随累计每任务适配曝光变化。在MovieLens的共同cross-task-safe子集上，seed42标准k5验证差距在三个排序指标上均从48k到96k收窄。两个额外训练种子独立复现了96k时小幅但方向一致的N优势，而共同seed42测试子集没有复现验证侧的收窄。在这一运行点，M1也保持了与Y专家接近的被测偏好表现。完整轨迹仍仅来自seed42，运行点复现加强了结合具体曝光解释专门化与统一建模的证据，但不意味着等价或正迁移。

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
