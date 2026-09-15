---
id: introduction
title:
  en: Introduction
  zh: 引言
status: draft
---

<!-- PARAGRAPH: intro.p01 -->
<!-- EVIDENCE: S01,S02,S03,S04,S05 -->

**EN**

Language-model-based recommendation encompasses zero-shot conversational recommendation, candidate ranking, and recommendation-specific adaptation [@he2023zeroshotconv; @hou2024zeroshotrankers; @bao2023tallrec]. Alongside prompt-based use, recommendation-as-language-processing formulations provide a unified language-oriented view of model inputs and predictions [@geng2022p5]. These approaches place language models in different recommendation roles, from interacting with users to ordering items or adapting to a recommendation task. The broader study of recommender systems in the LLM era makes the assessment of these models an important empirical question [@zhao2024llmrec]. Understanding what recommendation-specific adaptation teaches a language model is central to interpreting its performance.

**ZH**

基于语言模型的推荐涵盖零样本对话推荐、候选排序和推荐特定适配等路径 [@he2023zeroshotconv; @hou2024zeroshotrankers; @bao2023tallrec]。在基于提示的使用方式之外，将推荐表述为语言处理的工作，也为模型输入与预测提供了统一的语言化视角 [@geng2022p5]。这些方法使语言模型承担不同推荐职责，包括与用户交互、排列物品以及适配推荐任务。LLM 时代推荐系统研究的展开，使如何评估这些模型成为一个重要的实证问题 [@zhao2024llmrec]。理解推荐特定适配究竟教会了语言模型什么，是解释其表现的关键。

<!-- PARAGRAPH: intro.p02 -->
<!-- EVIDENCE: C1,M1,S02,S07,S08 -->

**EN**

Recommendation, however, encompasses several prediction questions. Whether a user likes an item concerns a preference judgment, while which item the user will interact with next concerns the identity of a subsequent event. Feedback-oriented and sequential models operationalize different targets, and language-based frameworks can express several such tasks through a common interface [@hu2008implicit; @kang2018sasrec; @geng2022p5]. For an adapted language model, the target is instantiated together with task data, prompts, and a scoring interface. These choices define what the model is trained to predict and how its capability is observed. The empirical question is how performance under one complete supervision formulation relates to performance under another.

**ZH**

推荐包含不止一种预测问题。用户是否喜欢一个物品，关注的是偏好判断；用户下一次将与哪个物品交互，关注的是后续事件的身份。面向反馈与面向序列的模型将不同目标具体化，语言化框架也可以通过共同接口表达多种此类任务 [@hu2008implicit; @kang2018sasrec; @geng2022p5]。对于适配后的语言模型，目标与任务数据、提示和评分接口共同构成具体形式。这些选择定义了模型接受何种预测训练，以及其能力如何被观察。相应的实证问题是：一种完整监督形式下的表现，与另一种形式下的表现具有怎样的关系？

<!-- PARAGRAPH: intro.p03 -->
<!-- EVIDENCE: M3,C3,C5,S02,S15 -->

**EN**

A checkpoint also represents a particular amount of adaptation. We use task-sample exposure to denote the cumulative number of training examples consumed for a task, including repeated examples. Existing unified recommendation studies already examine task-specific performance and variations in training-data amount or task composition [@geng2022p5; @liu2025itdr]. A complementary comparison follows the relationship between a specialist and a shared model as the corresponding task receives additional cumulative supervision. In a mixed-task stream, this requires distinguishing total training exposure from the exposure allocated to each task. Making that quantity explicit allows us to ask whether a model advantage observed at a lower budget persists as adaptation proceeds.

**ZH**

一个检查点也代表特定程度的适配。本文用任务样本曝光表示某项任务累计消耗的训练样本数，其中包括重复使用的样本。已有统一推荐研究已考察各任务表现，以及训练数据量或任务构成的变化 [@geng2022p5; @liu2025itdr]。一个互补的比较角度，是追踪对应任务获得额外累计监督时，专家与共享模型之间的关系。在混合任务训练流中，这要求区分训练总曝光与分配给每项任务的曝光。明确这一数量之后，才能考察较低预算下观察到的模型优势是否随适配继续进行而保持。

<!-- PARAGRAPH: intro.p04 -->
<!-- EVIDENCE: C6,C7,M5,S10,S11,S12,S02,S15,S21,S25 -->

**EN**

Evaluation conditions further shape model comparisons. Work on sampled metrics and candidate-set construction shows that sampling can alter measured performance and relative model orderings [@krichene2020sampled; @canamares2020target; @dallmann2021sampling]. Task formulation and training-data allocation also intersect in unified recommendation, task ablations, and shared search-recommendation models [@geng2022p5; @liu2025itdr; @zhou2025openonerec; @penha2024bridging]. Existing studies thus address partially overlapping questions about task formulation, training-data allocation, and candidate evaluation. Building on these connections, we examine how specialist-multitask and LLM-sequential-baseline relationships change with cumulative per-task supervision, and which relationships persist under alternative candidate conditions.

**ZH**

评估条件进一步影响模型比较。关于采样指标和候选集合构造的研究表明，采样能够改变测得的表现及模型相对次序 [@krichene2020sampled; @canamares2020target; @dallmann2021sampling]。在统一推荐、任务消融和搜索推荐共享模型中，任务形式与训练数据分配也已发生交叉 [@geng2022p5; @liu2025itdr; @zhou2025openonerec; @penha2024bridging]。因此，已有研究围绕任务形式、训练数据分配和候选评估考察了部分重合的问题。在这些关联的基础上，本文研究专家与多任务模型、LLM 与序列基线的关系如何随累计每任务监督变化，以及哪些关系能在不同候选条件下保持。

<!-- PARAGRAPH: intro.p05 -->
<!-- EVIDENCE: C1,C2,C3,C4,C5,C6,C7,C8,M3 -->

**EN**

We conduct a controlled empirical study within a shared LLM adaptation setting. The study contrasts rating-derived preference supervision, denoted Y, with next-interaction supervision, denoted N, and examines a shared multitask adapter, M1, that supports both interfaces. It traces task-specific performance across training exposures and compares specialist and multitask models at matched per-task exposure. Standard and harder candidate protocols examine the reach of the resulting ranking relationships. An exposure-aware comparison with SASRec aligns approximately the downstream N-task supervision received by the models. MovieLens provides the detailed analysis, and Amazon Musical Instruments supplies an external ranking-side check.

**ZH**

本文在共同的 LLM 适配设置中开展受控实证研究。研究对比由评分产生的偏好监督 Y 与下一交互监督 N，并考察同时支持两种接口的共享多任务 adapter M1。我们追踪不同训练曝光下的任务表现，并在每任务曝光对齐时比较专家与多任务模型。标准候选协议及较难候选协议用于检验所得排序关系的适用范围。与 SASRec 的曝光感知比较，则近似对齐模型获得的下游 N 任务监督。MovieLens 提供详细分析，Amazon Musical Instruments 提供外部排序侧检验。

<!-- PARAGRAPH: intro.p06 -->
<!-- EVIDENCE: C1,C2,C3,C4,C5,C6,C7,C8 -->

**EN**

The observed capability profiles distinguish preference discrimination from next-interaction selection. In the MovieLens seed42 exposure study, measured Y gains are limited or uneven across metrics, while N ranking continues to improve throughout the evaluated range. From 48k to 96k per task, the specialist-multitask gap narrows substantially on standard k5 validation. Independent 96k runs with seeds 43 and 44 reproduce the small-gap regime while maintaining comparable Y-side preference performance; the frozen test set consistently retains a modest N advantage across all three training seeds. Alternative candidate protocols preserve an N advantage, with a substantially larger gap under k20 than standard k5. At all four approximately matched downstream task-sample exposure points, N-trained LlamaRec outperforms the evaluated SASRec baseline, while SASRec improves strongly and the gap narrows at 200k relative to 96k. Amazon reproduces the key ranking-side directions at its evaluated earlier operating point.

**ZH**

观察到的能力结构区分了偏好判别与下一交互选择。在MovieLens的seed42曝光研究中，Y在不同指标上的被测增益有限或不均匀，N排序则在整个已评估范围内持续改善。每任务曝光从48k提高到96k时，标准k5验证集上的专家与多任务差距明显缩小。seed43和44的独立96k运行复现了小差距区间，也保持了与Y专家接近的偏好表现；三个训练种子的冻结测试结果均保留N的小幅优势。其他候选协议仍保留N优势，其中k20的差距明显大于标准k5。在四个下游任务样本曝光近似匹配点上，接受N任务训练的LlamaRec均优于被评估的SASRec基线；SASRec也明显改善，使200k时的差距小于96k。Amazon在已评估的较早运行点上重现了关键排序侧方向。

<!-- PARAGRAPH: intro.p07 -->
<!-- EVIDENCE: C1,C2,C3,C4,C5,C6,C7,M3,M5 -->

**EN**

The central contribution is an exposure-conditioned account of specialization and unification: a model relationship observed at a lower supervision budget can change substantially after further task-specific adaptation. A second contribution traces the LLM-sequential-baseline comparison over explicit cumulative downstream exposure points. Candidate-protocol analysis establishes an important boundary on the higher-exposure specialist-multitask relationship, while the distinction between supervision formulations defines the capabilities being compared. Together, these linked comparisons show how recommendation conclusions depend on what is supervised, how much task supervision is consumed, and which candidate conditions are evaluated within the studied setting.

**ZH**

本研究的核心贡献，是结合曝光刻画专门化与统一建模：较低监督预算下观察到的模型关系，可能在进一步任务特定适配后明显改变。第二项主贡献沿明确的累计下游曝光点追踪 LLM 与序列基线的比较。候选协议分析为较高曝光下的专家与多任务关系确定重要边界，监督形式的区分则界定了被比较的能力。这些相互关联的比较共同展示，在本研究设置中，推荐结论如何依赖监督什么、累计消耗多少任务监督，以及采用何种候选评估条件。
