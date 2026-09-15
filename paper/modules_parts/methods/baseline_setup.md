---
id: baseline_setup
title:
  en: Sequential Baseline and Comparison Scope
  zh: 序列基线与比较范围
status: draft
---

<!-- PARAGRAPH: methods.baseline.p01 -->
<!-- EVIDENCE: M7,C7,S08 -->

**EN**

SASRec [@kang2018sasrec] uses 64-dimensional item and position embeddings, 2 attention heads, 2 causal Transformer layers, a 256-dimensional feed-forward block with GELU, dropout 0.2, final LayerNorm, and a maximum history of 10. It scores an item by the dot product between the sequence representation and item embedding plus an item bias. Training uses full-item cross-entropy and AdamW with learning rate 0.001, weight decay 0, no scheduler, batch size 512, and seed42.

**ZH**

SASRec [@kang2018sasrec]采用64维物品与位置嵌入、2个注意力头、2层因果Transformer、宽度为256且使用GELU的前馈层、0.2 dropout、末端LayerNorm和最长10条历史。物品得分为序列表示与物品嵌入的点积加物品偏置。训练采用全物品交叉熵与AdamW，学习率0.001、weight decay为0、不使用scheduler，batch size为512，训练seed为42。

<!-- PARAGRAPH: methods.baseline.p02 -->
<!-- EVIDENCE: C7,C9,M7 -->

**EN**

S47, S94, S188, and S391 are predefined 47-, 94-, 188-, and 391-optimizer-step operating points, independently trained from scratch rather than selected as best validation checkpoints or by early stopping. Their recorded downstream task-sample exposures are 24,064, 48,128, 96,256, and 200,000, including the short final batch. They are paired with N24/N48/N96/N200 on the same seed42 PopMatch-k5 validation and test candidate sets. Validation is the main comparison and frozen test is report-only. This design aligns downstream task-sample exposure only, not pretraining, tokens, optimizer steps, FLOPs, wall-clock time, hardware, latency, parameter count, or computational resources.

**ZH**

S47、S94、S188与S391是预先指定的47、94、188和391个优化器步运行点，每个运行均独立从头训练，不是按验证集选择的最佳检查点，也不是早停结果。其记录的下游任务样本曝光分别为24,064、48,128、96,256和200,000，包含末尾不足完整batch的实际消费。它们分别与N24/N48/N96/N200配对，并使用相同的seed42 PopMatch-k5验证和测试候选集。验证集是主要比较，冻结测试仅作报告。该设计只对齐下游任务样本曝光，不对齐预训练、token、优化器步数、FLOPs、实际时间、硬件、延迟、参数量或计算资源。
