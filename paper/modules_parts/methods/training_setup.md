---
id: training_setup
title:
  en: Shared Adaptation and Response Scoring
  zh: 共享适配流程与响应评分
status: draft
---

<!-- PARAGRAPH: methods.training.p01 -->
<!-- EVIDENCE: M2,M4 -->

**EN**

We adapt Llama-3.2-3B-Instruct [@meta2024llama32] with QLoRA over a frozen 4-bit NF4 base [@dettmers2023qlora]. Rank 16 LoRA adapters [@hu2022lora] use alpha 32 and dropout 0.05 across q/k/v/o and gate/up/down projections. Gradient checkpointing is enabled and maximum sequence length is 2,048.

**ZH**

本文以QLoRA适配Llama-3.2-3B-Instruct [@meta2024llama32]，底座采用冻结4-bit NF4表示 [@dettmers2023qlora]。rank 16的LoRA adapter [@hu2022lora]使用alpha 32、dropout 0.05，覆盖q/k/v/o及gate/up/down投影。训练启用gradient checkpointing，最大序列长度为2,048。

<!-- PARAGRAPH: methods.training.p02 -->
<!-- EVIDENCE: M2,M3 -->

**EN**

Examples use instruction-chat format with the answer as the assistant response. Prompt and padding tokens are masked, giving response-only loss. Y supervises Yes/No and N supervises the target candidate label. M1 shares adapter parameters and interleaves Y/N examples 1:1, with the prompt identifying the task.

**ZH**

样本采用指令对话格式，答案作为assistant响应。提示与padding token被屏蔽，仅响应部分参与损失。Y监督Yes/No，N监督目标候选标签。M1共享adapter参数，以1:1交错Y/N样本，并由提示标识任务。

<!-- PARAGRAPH: methods.training.p03 -->
<!-- EVIDENCE: M4 -->

**EN**

Inference scores allowed-answer likelihoods. Y normalizes Yes/No likelihoods and Y-as-ranker orders independently scored candidates. N normalizes candidate-label likelihoods conditioned on the list. Multi-token answers use complete-sequence log-likelihood; M-Y and M-N reuse these routes.

**ZH**

推理对允许答案的似然评分。Y归一化Yes/No似然，Y-as-ranker据独立候选分数排序；N在候选列表条件下归一化候选标签似然。多token答案使用完整序列对数似然，M-Y与M-N复用相应路径。

<!-- PARAGRAPH: methods.training.p04 -->
<!-- EVIDENCE: M2,M3 -->

**EN**

One-device micro-batch 1 with 8 accumulation steps yields 8 examples per optimizer update. Checkpoints are indexed by cumulative steps and task exposure and evaluated on fixed candidates. Validation guides training decisions; test follows frozen selection. Multitask per-task allocation is specified below.

**ZH**

单设备micro-batch为1、梯度累积为8，每次优化器更新消耗8个样本。检查点按累计步数和任务曝光标识，并在固定候选上评估。验证集指导训练决策，测试在选择冻结后进行；多任务每任务分配见下文。
