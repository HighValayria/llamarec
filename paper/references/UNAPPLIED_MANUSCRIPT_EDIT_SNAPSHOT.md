# 未采用的稿件修改备份

日期：2026-09-07。

用户明确要求本轮只收集论文证据，不修改稿件。本文件仅保存撤回前的局部修改，防止工作丢失；不是正式作者源、不是已批准修订，也不参与论文装配。正式双语稿应恢复到本轮文献核验前版本。是否采用以下内容，等待用户另行决定。

## 修改范围

- 贡献：p02、p03、p04；p01未改。
- 引言：仅intro.p04；其余段落未改。
- 相关工作：rw.llm.p02、rw.tasks.p01、rw.unified.p01/p02、rw.evaluation.p01/p02；入口综合段未改。
- 下面保存六个文件在回滚前的完整文本，便于后续精确比较。未引入新实验或新seed结论。

## paper/modules/00_contributions.md

```markdown
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

We distinguish rating-derived preference prediction from next-interaction prediction within a shared LLM adaptation setting. Native-task and bridge evaluations reveal the observed capability profiles associated with these supervision formulations. This empirical distinction makes the prediction interface explicit when interpreting recommendation ability.

**ZH**

本文在共同的 LLM 适配设置中区分评分产生的偏好预测与下一交互预测。原生任务和桥接评估揭示了这些监督形式各自对应的可观测能力结构。这一实证区分使解释推荐能力时的预测接口更加明确。

<!-- PARAGRAPH: contributions.p02 -->
<!-- EVIDENCE: C2,C3,C4,C5,M3 -->
<!-- EVIDENCE_PENDING: MS96 -->

**EN**

We characterize exposure-dependent capability and specialist-multitask relationships. In the MovieLens seed42 study, measured Y gains weaken while N ranking continues to improve across the evaluated exposure range. At matched per-task exposure, additional supervision substantially narrows the low-exposure specialist advantage on standard k5 validation, while the frozen test set retains a modest N advantage. These observations qualify specialization by the amount of task-specific adaptation.

**ZH**

本文刻画随曝光变化的能力及专家与多任务关系。在 MovieLens seed42 研究中，Y 的被测增益减弱，而 N 排序在已评估曝光范围内持续改善。在每任务曝光对齐时，额外监督明显缩小了标准 k5 验证集上低曝光时的专家优势，冻结测试集仍保留 N 的小幅优势。这些观察表明，专门化的比较结论需要结合任务特定适配量来解释。

<!-- PARAGRAPH: contributions.p03 -->
<!-- EVIDENCE: C5,C6,M5 -->
<!-- EVIDENCE_PENDING: MS96 -->

**EN**

We show that a small specialist-multitask gap on standard k5 can coexist with larger gaps under harder candidate protocols at the evaluated higher-exposure point. This result limits the robustness conclusion that can be drawn from a single candidate setting. Because the protocols are non-nested, the comparison establishes protocol sensitivity rather than an isolated causal effect of candidate-set size.

**ZH**

本文表明，在已评估的较高曝光点，标准 k5 上较小的专家与多任务差距，可以与较难候选协议下更大的差距并存。这一结果限定了单一候选设置能够支持的鲁棒性结论。由于协议非嵌套，该比较确认的是协议敏感性，而不是候选集合大小的独立因果效应。

<!-- PARAGRAPH: contributions.p04 -->
<!-- EVIDENCE: C7,C9,M3,M7 -->

**EN**

We assess downstream task-sample efficiency through an exposure-aware comparison of N-trained LlamaRec and SASRec. Under approximately matched cumulative N-task supervision, the evaluated points show N's ranking advantage alongside SASRec's continued improvement with additional supervision. This conditional comparison separates downstream task-sample exposure from pretraining investment and computational cost.

**ZH**

本文通过接受 N 任务训练的 LlamaRec 与 SASRec 的曝光感知比较，评估下游任务样本效率。在累计 N 任务监督近似匹配时，已评估运行点同时显示 N 的排序优势，以及 SASRec 随额外监督的持续改善。这一条件化比较将下游任务样本曝光与预训练投入、计算成本区分开来。
```

## paper/modules/01_introduction.md

```markdown
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
<!-- EVIDENCE: C1,M1,S07,S08 -->

**EN**

Recommendation, however, encompasses several prediction questions. Whether a user likes an item concerns a preference judgment, while which item the user will interact with next concerns the identity of a subsequent event. The distinction between feedback-oriented and sequential modeling is reflected in research on implicit-feedback collaborative filtering and self-attentive sequential recommendation [@hu2008implicit; @kang2018sasrec]. For an adapted language model, the prediction target is expressed through training examples, prompts, and a scoring interface. Different choices define different opportunities to demonstrate recommendation capability. This diversity raises the question of how closely performance on one supervision formulation corresponds to performance on another.

**ZH**

推荐包含不止一种预测问题。用户是否喜欢一个物品，关注的是偏好判断；用户下一次将与哪个物品交互，关注的是后续事件的身份。面向反馈与面向序列的建模区别，也体现在隐式反馈协同过滤和自注意力序列推荐等研究方向中 [@hu2008implicit; @kang2018sasrec]。对于适配后的语言模型，预测目标通过训练样本、提示和评分接口表达。不同选择定义了展示推荐能力的不同方式。由此需要追问：一种监督形式下的表现，与另一种监督形式下的表现有多大对应关系？

<!-- PARAGRAPH: intro.p03 -->
<!-- EVIDENCE: M3,C3,C5 -->

**EN**

Even for a fixed prediction target, a checkpoint represents a particular amount of adaptation. We use task-sample exposure to describe the cumulative number of training examples consumed for a task, including repeated examples. An early checkpoint captures performance after limited supervision, while later checkpoints reveal how that formulation responds to additional exposure. The distinction is especially relevant for a mixed-task training stream, where a total example budget is divided among tasks. Comparing a specialist with a shared model therefore requires specifying the supervision received by the corresponding task. Exposure provides a way to examine whether an apparent model advantage persists as adaptation proceeds.

**ZH**

即使预测目标固定，一个检查点也只代表特定程度的适配。本文用任务样本曝光描述某项任务累计消耗的训练样本数，其中包括重复使用的样本。较早检查点反映有限监督后的表现，后续检查点则揭示该监督形式对额外曝光的响应。对于混合任务训练流，这一区别尤为重要，因为总样本预算需要分配到不同任务。因此，比较专家与共享模型时，需要说明对应任务实际获得的监督量。曝光由此提供了一个考察方式：随着适配继续进行，原先观察到的模型优势是否仍然存在？

<!-- PARAGRAPH: intro.p04 -->
<!-- EVIDENCE: C6,C7,M3,M5,S02,S10,S12,S15,S16 -->

**EN**

Evaluation conditions further qualify these relationships: sampled ranking metrics and candidate construction can change model comparisons [@krichene2020sampled; @dallmann2021sampling]. Related work already provides substantial pieces of this picture. P5 compares unified and single-task recommendation models, ITDR examines task composition and fine-tuning data scale, and InstructRec evaluates difficult candidates [@geng2022p5; @liu2025itdr; @zhang2023instructrec]. Building on these precedents, we ask how capability differences and specialist-multitask relationships evolve with cumulative per-task exposure in a common recommendation-tuning setting, and which observed ranking relationships persist under alternative candidate protocols. This question connects supervision formulation, adaptation amount, and evaluation without treating any one of these dimensions as a new research topic.

**ZH**

评估条件进一步限定这些关系：采样排序指标与候选构造能够改变模型比较 [@krichene2020sampled; @dallmann2021sampling]。已有研究已提供这一问题的重要组成部分。P5 比较统一模型与单任务推荐模型，ITDR 考察任务组成及微调数据规模，InstructRec 评估困难候选 [@geng2022p5; @liu2025itdr; @zhang2023instructrec]。承接这些先例，本文提出：在共同推荐调优设置中，能力差异及专家与多任务模型的关系如何随累计每任务曝光变化？哪些已观察到的排序关系能够在其他候选协议下保持？这一问题将监督形式、适配量与评估联系起来，而不把其中任何单一维度视为新的研究主题。

<!-- PARAGRAPH: intro.p05 -->
<!-- EVIDENCE: C1,C2,C3,C4,C5,C6,C7,C8,M3 -->

**EN**

We conduct a controlled empirical study within a shared LLM adaptation setting. The study contrasts rating-derived preference supervision, denoted Y, with next-interaction supervision, denoted N, and examines a shared multitask adapter, M1, that supports both interfaces. It traces task-specific performance across training exposures and compares specialist and multitask models at matched per-task exposure. Standard and harder candidate protocols examine the reach of the resulting ranking relationships. An exposure-aware comparison with SASRec aligns approximately the downstream N-task supervision received by the models. MovieLens provides the detailed analysis, and Amazon Musical Instruments supplies an external ranking-side check.

**ZH**

本文在共同的 LLM 适配设置中开展受控实证研究。研究对比由评分产生的偏好监督 Y 与下一交互监督 N，并考察同时支持两种接口的共享多任务 adapter M1。我们追踪不同训练曝光下的任务表现，并在每任务曝光对齐时比较专家与多任务模型。标准候选协议及较难候选协议用于检验所得排序关系的适用范围。与 SASRec 的曝光感知比较，则近似对齐模型获得的下游 N 任务监督。MovieLens 提供详细分析，Amazon Musical Instruments 提供外部排序侧检验。

<!-- PARAGRAPH: intro.p06 -->
<!-- EVIDENCE: C1,C2,C3,C4,C5,C6,C7,C8 -->
<!-- EVIDENCE_PENDING: MS96 -->

**EN**

The observed capability profiles distinguish preference discrimination from next-interaction selection. In the MovieLens seed42 exposure study, measured Y gains weaken as exposure increases, while N ranking continues to improve throughout the evaluated range. Higher per-task exposure substantially narrows the specialist-multitask gap on standard k5 validation, with the frozen test set retaining a modest N advantage. Harder candidate protocols reveal a remaining ranking advantage for the N specialist. At approximately matched downstream task-sample exposure, N-trained LlamaRec outperforms the evaluated SASRec baseline at every measured point, while SASRec also improves strongly with additional supervision. Amazon reproduces the key ranking-side directions at the evaluated operating point.

**ZH**

观察到的能力结构区分了偏好判别与下一交互选择。在 MovieLens 的 seed42 曝光研究中，Y 的被测增益随曝光增加而减弱，N 排序则在整个已评估范围内持续改善。更高的每任务曝光明显缩小了标准 k5 验证集上的专家与多任务差距，冻结测试集仍保留 N 的小幅优势。较难候选协议进一步显示 N 专家仍有排序优势。在下游任务样本曝光近似匹配时，接受 N 任务训练的 LlamaRec 在每个已测点均优于被评估的 SASRec 基线，SASRec 也随额外监督显著改善。Amazon 在已评估运行点上重现了关键排序侧方向。

<!-- PARAGRAPH: intro.p07 -->
<!-- EVIDENCE: C1,C2,C3,C4,C5,C6,C7,M3,M5 -->

**EN**

The study contributes an empirical account of recommendation capability that keeps supervision formulation, adaptation exposure, and evaluation conditions connected. It distinguishes preference and next-interaction capability profiles and characterizes their exposure-dependent behavior, including the specialist-multitask comparison at matched per-task exposure. It further identifies candidate-protocol sensitivity as part of that comparison and develops an exposure-aware assessment against a specialized sequential baseline. Together, these contributions provide evidence and methodological guidance for interpreting recommendation-tuned LLMs in explicitly specified experimental settings.

**ZH**

本研究通过将监督形式、适配曝光和评估条件联系起来，为推荐能力提供实证解释。研究区分偏好与下一交互的能力结构，刻画其随曝光变化的行为，并纳入每任务曝光对齐下的专家与多任务比较。同时，研究将候选协议敏感性明确为模型比较的一部分，并针对专门序列基线开展曝光感知评估。这些贡献共同为解释明确实验条件下的推荐调优 LLM 提供证据与方法学参考。
```

## paper/modules_parts/related_work/llm_recommendation.md

```markdown
---
id: rw_llm_recommendation
title:
  en: LLMs for Recommendation
  zh: 面向推荐的语言模型
status: draft
---

<!-- PARAGRAPH: rw.llm.p01 -->
<!-- EVIDENCE: S01,S04,S05 -->

**EN**

Prompt-based recommendation places a language model in direct interaction with a recommendation request. Zero-shot conversational recommendation and zero-shot ranking illustrate different uses of this interface, centering respectively on a conversational setting and an ordering task [@he2023zeroshotconv; @hou2024zeroshotrankers]. These directions sit within the broader study of recommender systems in the LLM era [@zhao2024llmrec]. Their coexistence makes the requested output part of what a recommendation evaluation measures, motivating a task-specific account of model capability.

**ZH**

基于提示的推荐使语言模型直接处理推荐请求。零样本对话推荐与零样本排序体现了这一接口的不同用途，分别关注对话场景和排序任务 [@he2023zeroshotconv; @hou2024zeroshotrankers]。这些方向共同处于 LLM 时代推荐系统的研究范畴内 [@zhao2024llmrec]。它们的并存使所要求的输出成为推荐评估对象的一部分，也促使我们按具体任务解释模型能力。

<!-- PARAGRAPH: rw.llm.p02 -->
<!-- EVIDENCE: S02,S03,S16,M2 -->

**EN**

Recommendation-specific adaptation makes the training request and response explicit. P5 mixes text-to-text examples across rating, sequential recommendation, and other task families in a shared T5 model [@geng2022p5]. TALLRec combines instruction and recommendation tuning with LoRA; its recommendation examples pair liked/disliked item histories and a target item with a Yes/No response [@bao2023tallrec]. InstructRec instead organizes user preferences, intentions, and task forms into instructions for a shared sequence-to-sequence model [@zhang2023instructrec]. These implementations demonstrate why instruction tuning must be described through its input, target, and training objective, rather than treated as a single recommendation capability.

**ZH**

推荐特定适配将训练请求和响应明确化。P5 在共享 T5 模型中混合评分、序列推荐及其他任务族的文本到文本样本 [@geng2022p5]。TALLRec 结合指令调优、推荐调优与 LoRA，其推荐样本将喜欢及不喜欢的物品历史、目标物品与 Yes/No 响应配对 [@bao2023tallrec]。InstructRec 则将用户偏好、意图和任务形式组织为共享序列到序列模型的指令 [@zhang2023instructrec]。这些实现说明，描述指令调优需要明确输入、目标与训练目标函数，而不能将其视为一种单一推荐能力。
```

## paper/modules_parts/related_work/supervision_formulation.md

```markdown
---
id: rw_supervision_formulation
title:
  en: Recommendation Supervision and Task Formulation
  zh: 推荐监督与任务形式
status: draft
---

<!-- PARAGRAPH: rw.tasks.p01 -->
<!-- EVIDENCE: S06,S07,S08,M1 -->

**EN**

Prediction targets are distinct from the techniques used to model them. The basic matrix-factorization formulation fits observed ratings, whereas implicit-feedback factorization separates inferred preference from confidence in a behavioral observation [@koren2009mf; @hu2008implicit]. SASRec uses the subsequent observed item as the sequential prediction target [@kang2018sasrec]. Thus, an explicit rating, evidence of an interaction, and the identity of the next event have different operational meanings. These distinctions motivate specifying what supervision and evaluation measure without assuming that any observed behavior directly reveals a user's rating.

**ZH**

预测目标与建模技术是不同的选择。基础矩阵分解形式拟合已观测评分，隐式反馈矩阵分解则区分推断出的偏好与对行为观测的置信度 [@koren2009mf; @hu2008implicit]。SASRec 将后续观测物品作为序列预测目标 [@kang2018sasrec]。因此，显式评分、交互证据和下一事件的身份具有不同的操作性含义。这些区别促使研究明确监督与评估究竟测量什么，而不假定任意观测行为都直接揭示用户评分。

<!-- PARAGRAPH: rw.tasks.p02 -->
<!-- EVIDENCE: C1,M1,M4,S02 -->

**EN**

Preference prediction, next-event prediction, and candidate ranking also differ at the interface level. A preference question assigns a score to an item, a next-event question identifies a subsequent interaction, and a candidate-ranking interface orders alternatives for a specified target. A language-oriented formulation offers a common way to express recommendation requests while leaving these prediction questions distinct [@geng2022p5]. We examine their empirical consequences through rating-derived preference and next-interaction formulations, including a bridge evaluation that uses preference scores to rank next-interaction candidates. This comparison concerns the complete target, task data, prompt, and scoring formulation within the shared adaptation setting.

**ZH**

偏好预测、下一事件预测和候选排序在接口层面也有所区别。偏好问题为物品赋予分数，下一事件问题识别后续交互，候选排序接口则围绕指定目标排列备选项。语言化形式为表达推荐请求提供共同方式，同时保留这些预测问题之间的区别 [@geng2022p5]。本文通过评分产生的偏好形式与下一交互形式考察其经验后果，并以偏好分数排列下一交互候选，形成桥接评估。这一比较针对共同适配设置中的完整目标、任务数据、提示和评分形式。
```

## paper/modules_parts/related_work/multitask_unification.md

```markdown
---
id: rw_multitask_unification
title:
  en: Multitask and Unified Recommendation Modeling
  zh: 多任务与统一推荐建模
status: draft
---

<!-- PARAGRAPH: rw.unified.p01 -->
<!-- EVIDENCE: S02,S15,S21 -->

**EN**

Shared recommendation models already support heterogeneous tasks. P5's comparison with separately trained task models shows that the benefit of joint training differs across its task families [@geng2022p5]. ITDR uses LoRA for a multi-task instruction dataset and examines task-removal ablations and training-subset scale [@liu2025itdr]. OpenOneRec combines binary engagement prediction with generative recommendation and other tasks, reporting explicit sampling weights for multi-task supervised fine-tuning [@zhou2025openonerec]. These studies establish task composition and allocation as concrete design choices. Reporting such choices, however, answers a different question from tracing a shared adapter against task specialists across matched cumulative per-task exposures.

**ZH**

共享推荐模型已经能够支持异质任务。P5 与分别训练的任务模型进行比较，表明联合训练的收益在不同任务族之间有所区别 [@geng2022p5]。ITDR 对多任务指令数据使用 LoRA，并考察任务删除消融和训练子集规模 [@liu2025itdr]。OpenOneRec 将二元参与行为预测、生成式推荐及其他任务结合起来，报告多任务监督微调的明确采样权重 [@zhou2025openonerec]。这些研究已经将任务组成与分配作为具体设计选择。不过，报告这些选择，与在累计每任务曝光对齐时追踪共享 adapter 相对任务专家的表现，回答的是不同问题。

<!-- PARAGRAPH: rw.unified.p02 -->
<!-- EVIDENCE: C4,C5,M3,M4,S18,S22 -->

**EN**

Unification also refers to different modeling levels. The original OneRec integrates retrieval and ranking through session generation and preference alignment, rather than defining a rating-derived preference task alongside next-item prediction [@deng2025onerec]. OneReason compares mixed-domain reinforcement learning with domain-specialized teachers and subsequent integration into a shared model [@onerecteam2026onereason]. Its specialization question concerns domains and reasoning policies. Our empirical comparison instead concerns a shared supervised adapter and task specialists: each interface is compared at the corresponding task exposure, and the resulting relationship is examined across exposure levels and candidate protocols.

**ZH**

统一还可以发生在不同建模层次。早期 OneRec 通过会话生成和偏好对齐整合召回与排序，并不是在下一物品预测之外定义评分派生偏好任务 [@deng2025onerec]。OneReason 比较混域强化学习、领域专门教师及其向共享模型的后续整合 [@onerecteam2026onereason]，其中的专门化问题涉及领域与推理策略。本文的实证比较则针对共享监督适配器与任务专家：在对应任务曝光下比较各接口，并考察所得关系如何随曝光水平与候选协议变化。
```

## paper/modules_parts/related_work/evaluation_baselines.md

```markdown
---
id: rw_evaluation_baselines
title:
  en: Evaluation and Baseline Comparison
  zh: 评估与基线比较
status: draft
---

<!-- PARAGRAPH: rw.evaluation.p01 -->
<!-- EVIDENCE: M5,S10,S11,S12,S16 -->

**EN**

Candidate construction and metric estimation jointly shape offline ranking comparisons. Krichene and Rendle show that sampled ranking metrics need not preserve the relative ordering of models, even in expectation [@krichene2020sampled]. Cañamares and Castells study the target set as the set of candidate items to score, not merely the held-out relevant item [@canamares2020target]. Dallmann et al. empirically compare full-catalog, uniform, and popularity-based sampling for neural sequential models and observe disagreements in model ordering [@dallmann2021sampling]. InstructRec also evaluates difficult retrieved candidates, establishing a recommendation-LLM precedent for such checks [@zhang2023instructrec]. This evidence motivates reporting candidate protocols explicitly; it does not isolate the cause of a gap between our non-nested protocols.

**ZH**

候选构造与指标估计共同影响离线排序比较。Krichene 和 Rendle 表明，采样排序指标即使在期望上也不一定保留模型的相对次序 [@krichene2020sampled]。Cañamares 和 Castells 所研究的目标集合，是需要评分的候选物品集合，而不只是持出的相关物品 [@canamares2020target]。Dallmann 等对神经序列模型的全库、均匀及流行度采样进行实证比较，观察到模型次序不一致 [@dallmann2021sampling]。InstructRec 也评估困难检索候选，为推荐 LLM 的这类检验提供已有先例 [@zhang2023instructrec]。这些证据支持明确报告候选协议，但不能隔离本文非嵌套协议之间差距的成因。

<!-- PARAGRAPH: rw.evaluation.p02 -->
<!-- EVIDENCE: C7,M7,S03,S08,S13,S14,S21,S23 -->

**EN**

Baseline quality and supervision budgets require separate scrutiny. SASRec provides the sequential reference, while reproducibility analyses and iALS re-evaluation demonstrate the importance of baseline tuning and evaluation practice [@kang2018sasrec; @dacrema2019progress; @rendle2022ials]. Budget-aware comparisons also have direct precedents: TALLRec compares with sequential baselines at matched selected-sample counts, and OpenOneRec examines low-data transfer [@bao2023tallrec; @zhou2025openonerec]. Sequential scaling research separately studies interaction-pool size and repeated training [@zhang2023seqscaling]. Our N/SASRec comparison uses approximately matched cumulative downstream task-sample exposure. This measures a conditional form of downstream task-sample efficiency, not equivalence in pretraining, information, or computational cost.

**ZH**

基线质量与监督预算需要分别审视。SASRec 提供序列参照，复现分析和 iALS 重新评估则说明基线调优与评价实践的重要性 [@kang2018sasrec; @dacrema2019progress; @rendle2022ials]。预算感知比较也已有直接先例：TALLRec 在选取样本数匹配时与序列基线比较，OpenOneRec 考察低数据量迁移 [@bao2023tallrec; @zhou2025openonerec]。序列规模研究还分别考察交互样本池大小与重复训练 [@zhang2023seqscaling]。本文的 N/SASRec 比较采用近似匹配的累计下游任务样本曝光，测量的是一种条件化的下游任务样本效率，而不是预训练、信息量或计算成本的等价性。
```

## 引用缺口处理建议

以下是证据审查结论，不表示正文已经应用。原正文中的引用待补标记保留，直至用户授权稿件修改。

- JOINT_CONDITIONING_COVERAGE：PARTIALLY_RESOLVED；建议 REWRITTEN_TO_SUPPORTED_CLAIM。承认前人已研究组成部分，改成共同设置下曝光与关系变化的正面研究问题；不再声明全领域缺少研究。 仍不确定：领域穷尽性仍OPEN，非当前句子的前提；有限检索不能证明首创。
- INSTRUCTION_TASK_DETAILS：RESOLVED；建议 RESOLVED_WITH_CITATION。用原文具体输入、响应、共享模型及训练形式替换泛化句。 仍不确定：不推断所有指令推荐采用同一目标或loss。
- RATING_TARGETS：RESOLVED；建议 RESOLVED_WITH_CITATION。原文区分已知评分拟合、隐式偏好/置信度与后续物品目标。 仍不确定：本文Y的阈值和N的选择接口仍由本地方法定义，不外推给所有文献。
- UNIFIED_TASK_ALLOCATION：RESOLVED；建议 REWRITTEN_TO_SUPPORTED_CLAIM。具体承认单任务对照、LoRA任务消融、显式SFT分配；将本文定位为每任务曝光条件下的共享adapter比较。 仍不确定：不证明以前无人对齐曝光；OneRec家族分开记录。
- SAMPLING_EFFECT_DETAILS：RESOLVED；建议 REWRITTEN_TO_SUPPORTED_CLAIM。加入排序可改变的有限结论，纠正Cañamares target set；承认已有hard候选LLM评价。 仍不确定：KDD全文未取得；既有理论不解释本文非嵌套协议的纯数量因果。
- EXPOSURE_BUDGET_COMPARISONS：RESOLVED；建议 REWRITTEN_TO_SUPPORTED_CLAIM。承认K-shot、低数据迁移和重复训练先例；本文只写downstream task-sample efficiency。 仍不确定：不声称总信息、预训练或算力匹配。
