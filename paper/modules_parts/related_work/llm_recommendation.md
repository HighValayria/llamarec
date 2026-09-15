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

Prompt-based recommendation places language models directly in recommendation requests. Zero-shot conversational recommendation and zero-shot ranking emphasize different outputs: interaction and item ordering [@he2023zeroshotconv; @hou2024zeroshotrankers]. Within the broader LLM-recommender literature [@zhao2024llmrec], this diversity makes the requested output part of what an evaluation measures and motivates task-specific capability claims.

**ZH**

基于提示的推荐使语言模型直接处理推荐请求。零样本对话推荐与零样本排序强调不同输出，即交互和物品排序 [@he2023zeroshotconv; @hou2024zeroshotrankers]。在更广泛的LLM推荐研究中 [@zhao2024llmrec]，这种差异使所要求的输出成为评估对象的一部分，也要求按任务陈述能力。

<!-- PARAGRAPH: rw.llm.p02 -->
<!-- EVIDENCE: S02,S03,S16,M2 -->

**EN**

Recommendation-specific adaptation makes the training interface part of the model's role. P5 expresses multiple task families as language pairs, TALLRec trains Yes/No recommendation responses, and InstructRec supports pointwise, pairwise, matching, and reranking requests [@geng2022p5; @bao2023tallrec; @zhang2023instructrec]. These precedents establish language-based adaptation across tasks. We compare the capabilities measured after complete preference and next-interaction formulations under a shared model setting.

**ZH**

推荐特定适配使训练接口成为模型职责的一部分。P5将多个任务族表述为语言输入输出对，TALLRec训练Yes/No推荐响应，InstructRec支持逐点、成对、匹配和重排序请求 [@geng2022p5; @bao2023tallrec; @zhang2023instructrec]。这些先例已覆盖多任务语言化适配；本文则在共同模型设置下比较完整偏好与下一交互形式适配后的被测能力。
