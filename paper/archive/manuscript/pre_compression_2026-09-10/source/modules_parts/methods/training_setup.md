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

The adapted models use Llama-3.2-3B-Instruct [@meta2024llama32] with QLoRA and a frozen 4-bit NF4 base representation [@dettmers2023qlora]. Low-rank adapters [@hu2022lora] have rank 16, scaling alpha 32, and dropout 0.05. Adapters cover all attention and MLP linear projections within transformer blocks: q_proj, k_proj, v_proj, o_proj, gate_proj, up_proj, and down_proj. Gradient checkpointing is enabled, and the configured maximum sequence length is 2,048 tokens.

**ZH**

适配模型使用 Llama-3.2-3B-Instruct [@meta2024llama32]，采用 QLoRA，并冻结 4-bit NF4 量化的底座表示 [@dettmers2023qlora]。低秩 adapter [@hu2022lora] 的 rank 为 16，缩放参数 alpha 为 32，dropout 为 0.05。Adapter 覆盖 transformer block 内全部 attention 和 MLP 线性投影：q_proj、k_proj、v_proj、o_proj、gate_proj、up_proj 和 down_proj。训练启用 gradient checkpointing，配置的最大序列长度为 2,048 token。

<!-- PARAGRAPH: methods.training.p02 -->
<!-- EVIDENCE: M2,M3 -->

**EN**

Each example is encoded in the model's instruction-chat format with the target answer as the assistant response. Prompt and padding positions are masked from the loss, leaving supervision on response tokens. Y examples supervise Yes or No, and N examples supervise the target's label among the training candidates. M1 interleaves Y and N examples at a 1:1 ratio with the same response-only loss, sharing adapter parameters while identifying the task through its prompt.

**ZH**

每个样本按模型的指令对话格式编码，将目标答案作为 assistant 响应。提示与 padding 位置在损失中被屏蔽，仅对响应 token 施加监督。Y 样本监督 Yes 或 No，N 样本监督目标在训练候选中的标签。M1 以 1:1 比例交错使用 Y 和 N 样本，并采用相同的响应部分损失；两项任务共享 adapter 参数，由提示标识当前任务。

<!-- PARAGRAPH: methods.training.p03 -->
<!-- EVIDENCE: M4 -->

**EN**

Inference scores the likelihoods of the allowed answers. For Y, the Yes and No likelihoods are normalized over the two-answer set to obtain a preference score; Y-as-ranker orders candidates by independently computed preference scores. N conditions on the candidate list and normalizes candidate-label likelihoods to produce an ordering. Multi-token answers are scored by their complete sequence log-likelihood. M-Y and M-N reuse these scoring routes with the shared multitask adapter.

**ZH**

推理对允许答案的似然进行评分。Y 将 Yes 和 No 的似然在这两个答案间归一化，得到偏好分数；Y-as-ranker 按独立计算的偏好分数排列候选。N 以候选列表为条件，将候选标签似然归一化形成排序。多 token 答案按完整序列的对数似然评分。M-Y 与 M-N 在共享多任务 adapter 上复用这两条评分路径。

<!-- PARAGRAPH: methods.training.p04 -->
<!-- EVIDENCE: M2,M3 -->

**EN**

The exposure analysis uses a single-device micro-batch of 1 and 8 gradient-accumulation steps, giving 8 task examples per optimizer update. Checkpoints are indexed by cumulative optimizer steps and task-sample exposure. Reported comparisons evaluate these checkpoints on fixed candidate sets, with validation guiding training decisions and test evaluation following the frozen selection. The exposure accounting below specifies the expected per-task allocation for resumed multitask runs.

**ZH**

曝光分析采用单设备 micro-batch 为 1、梯度累积步数为 8 的设置，每次优化器更新消耗 8 个任务样本。检查点按累计优化器步数和任务样本曝光标识。报告中的比较在固定候选集上评估这些检查点，验证集指导训练决策，测试评估在选择冻结后进行。下文的曝光统计明确了多任务续训运行的预期每任务分配。
