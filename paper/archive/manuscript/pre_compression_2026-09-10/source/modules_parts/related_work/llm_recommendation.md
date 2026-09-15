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

Recommendation-specific adaptation makes the training interface part of the model's recommendation role. P5 expresses several task families as language input-output pairs in a shared encoder-decoder model [@geng2022p5]. TALLRec adapts an LLM to produce Yes/No responses from a recommendation instruction, preference history, and target item [@bao2023tallrec]. InstructRec uses shared instruction following to accommodate pointwise, pairwise, matching, and reranking requests [@zhang2023instructrec]. These frameworks establish language-based adaptation across different requests and expected responses. Our empirical study examines how the complete supervision formulation relates to the capability measured after adaptation, using a common model setting to compare preference and next-interaction tasks.

**ZH**

推荐特定适配使训练接口成为模型推荐职责的一部分。P5 在共享编码器与解码器模型中，将多个任务族表达为语言输入输出对 [@geng2022p5]。TALLRec 根据推荐指令、偏好历史和目标物品，适配 LLM 以生成 Yes/No 响应 [@bao2023tallrec]。InstructRec 通过共享的指令遵循支持逐点、成对、匹配和重排序请求 [@zhang2023instructrec]。这些框架已经建立了面向不同请求和预期响应的语言化适配方式。本文的实证研究考察完整监督形式与适配后被测能力的关系，在共同模型设置下比较偏好与下一交互任务。
