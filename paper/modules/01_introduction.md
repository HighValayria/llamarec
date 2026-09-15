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

Language-model-based recommendation spans zero-shot conversation, candidate ranking, and recommendation-specific adaptation [@he2023zeroshotconv; @hou2024zeroshotrankers; @bao2023tallrec]. Recommendation-as-language-processing further offers a shared language interface for model inputs and predictions [@geng2022p5]. Because language models can interact, rank, or adapt to a task, interpreting what recommendation-specific supervision teaches them is a central empirical problem [@zhao2024llmrec].

**ZH**

基于语言模型的推荐涵盖零样本对话、候选排序和推荐特定适配 [@he2023zeroshotconv; @hou2024zeroshotrankers; @bao2023tallrec]。将推荐表述为语言处理，也为模型输入与预测提供了共同语言接口 [@geng2022p5]。语言模型可以承担交互、排序或任务适配等职责，因此，推荐特定监督究竟教会模型何种能力，是一个核心实证问题 [@zhao2024llmrec]。

<!-- PARAGRAPH: intro.p02 -->
<!-- EVIDENCE: C1,M1,S02,S07,S08 -->

**EN**

Recommendation includes different prediction questions. Whether a user likes an item is a preference judgment; which item appears next is a subsequent-event prediction. Feedback and sequential models operationalize different targets, while language frameworks can express both through a common interface [@hu2008implicit; @kang2018sasrec; @geng2022p5]. For an adapted model, task data, prompt, target, and scoring interface jointly define the complete supervision formulation and the capability observed.

**ZH**

推荐包含不同的预测问题。用户是否喜欢某个物品属于偏好判断，下一次出现哪个物品则属于后续事件预测。反馈模型与序列模型将不同目标具体化，语言框架可以用共同接口表达两者 [@hu2008implicit; @kang2018sasrec; @geng2022p5]。对于适配模型，任务数据、提示、目标与评分接口共同构成完整监督形式，并决定被观察的能力。

<!-- PARAGRAPH: intro.p03 -->
<!-- EVIDENCE: M3,C3,C5,S02,S15 -->

**EN**

A checkpoint also represents a specific amount of adaptation. We define task-sample exposure as the cumulative number of examples consumed for a task, including repetitions. Unified recommendation studies already examine task performance and changes in data amount or composition [@geng2022p5; @liu2025itdr]. Our complementary question is how specialist-shared relationships evolve as the corresponding task receives more cumulative supervision, with total and per-task exposure separated for mixed-task training.

**ZH**

一个检查点也代表特定程度的适配。本文将任务样本曝光定义为某任务累计消耗的样本数，包括重复样本。统一推荐研究已考察任务表现以及数据量或构成的变化 [@geng2022p5; @liu2025itdr]。本文进一步研究对应任务获得更多累计监督时，专家与共享模型的关系如何演变，并在混合任务训练中区分总曝光和每任务曝光。

<!-- PARAGRAPH: intro.p04 -->
<!-- EVIDENCE: C6,C7,M5,S10,S11,S12,S02,S15,S21,S25 -->

**EN**

Evaluation conditions add another boundary. Sampled metrics, sampling strategies, and candidate construction can change measured performance and model orderings [@krichene2020sampled; @canamares2020target; @pereira2025sampling]. Task formulation and data allocation likewise intersect in unified recommendation and shared search-recommendation models [@geng2022p5; @liu2025itdr; @zhou2025openonerec; @penha2024bridging]. These precedents motivate jointly examining cumulative per-task supervision, specialist-shared modeling, and candidate protocol without treating any one as an isolated cause.

**ZH**

评估条件构成另一项边界。采样指标、采样策略和候选构造能够改变测得的表现及模型次序 [@krichene2020sampled; @canamares2020target; @pereira2025sampling]。在统一推荐和搜索推荐共享模型中，任务形式与数据分配也相互关联 [@geng2022p5; @liu2025itdr; @zhou2025openonerec; @penha2024bridging]。这些先例促使本文联合考察累计每任务监督、专家与共享建模及候选协议，而不把其中任何一项视为孤立原因。

<!-- PARAGRAPH: intro.p05 -->
<!-- EVIDENCE: C1,C2,C3,C4,C5,C6,C7,C8,M3 -->

**EN**

We conduct a controlled study with rating-derived preference supervision (Y), next-interaction supervision (N), and one shared Y+N adapter (M1). We trace task-specific exposure, compare specialists with M1 at matched per-task exposure, test alternative candidate protocols, and compare N-trained LlamaRec with SASRec at approximately matched downstream supervision. MovieLens supplies detailed trajectories; Amazon Musical Instruments provides an external ranking-side check.

**ZH**

本文开展一项受控研究，比较评分产生的偏好监督Y、下一交互监督N和共享Y+N adapter M1。研究追踪任务特定曝光，在每任务曝光对齐时比较专家与M1，检验不同候选协议，并在下游监督近似匹配时比较N训练的LlamaRec与SASRec。MovieLens提供详细轨迹，Amazon Musical Instruments提供外部排序侧检验。

<!-- PARAGRAPH: intro.p06 -->
<!-- EVIDENCE: C1,C2,C3,C4,C5,C6,C7,C8 -->

**EN**

The complete Y and N formulations produce distinct measured capability profiles. In the seed42 MovieLens trajectory, Y gains are limited or uneven, whereas N improves through the evaluated range. On a common cross-task-safe subset, the standard-k5 validation specialist-M1 gap narrows from 48k to 96k per task across all three metrics; two additional seeds reproduce a small positive N advantage at 96k, but the common seed42 test subset does not reproduce the narrowing. Alternative protocols retain an N advantage with protocol-dependent magnitude. N-trained LlamaRec leads SASRec at four approximately matched exposure points, while SASRec improves and the gap narrows at 200k. Amazon supports safe earlier-point ranking directions only.

**ZH**

完整Y与N形式呈现不同的被测能力结构。在MovieLens的seed42轨迹中，Y的增益有限或不均匀，N则在已评估范围内持续改善。在共同cross-task-safe子集上，标准k5验证中的专家-M1差距在三个指标上均从每任务48k到96k收窄；另外两个seed复现了96k时小幅的N优势，但共同seed42测试子集没有复现收窄。其他候选协议也保持N方向，幅度随协议变化。N训练的LlamaRec在四个曝光近似匹配点领先SASRec，同时SASRec持续改善，差距在200k缩小。Amazon仅支持满足安全条件的较早运行点排序方向。

<!-- PARAGRAPH: intro.p07 -->
<!-- EVIDENCE: C1,C2,C3,C4,C5,C6,C7,M3,M5 -->

**EN**

Our primary contribution is an exposure-conditioned account of specialist-shared modeling. The secondary contribution is a four-point cumulative downstream-exposure comparison between the LLM and a sequential baseline. Candidate-protocol analysis supplies a supporting boundary, while supervision-formulation distinctions frame the capabilities being compared. Together, they show that conclusions depend on what is supervised, how much task supervision is consumed, and how candidates are evaluated.

**ZH**

本文的主贡献是结合曝光刻画专家与共享建模关系；次贡献是在四个累计下游曝光点比较LLM与序列基线；候选协议分析提供支撑性边界，监督形式区分则界定被比较的能力。三者共同表明，结论取决于监督内容、累计任务监督量和候选评估方式。
