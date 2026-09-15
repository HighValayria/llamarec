---
id: exposure_definition
title:
  en: Task-Sample Exposure and Matching
  zh: 任务样本曝光与对齐
status: draft
---

<!-- PARAGRAPH: methods.exposure.p01 -->
<!-- EVIDENCE: M3,C3 -->

**EN**

Task-sample exposure counts the training examples consumed for a specified task, including repeated examples. If B_s is the set of examples consumed by optimizer step s, exposure for task q is E_q = sum_s sum_(x in B_s) 1[task(x)=q]. Repeated consumption and overlapping task histories make this a measure of supervision received, distinct from the number of unique raw interactions. We use this quantity to align task supervision across models.

**ZH**

任务样本曝光统计指定任务累计消耗的训练样本数，重复使用的样本也计入。令 B_s 为第 s 次优化器更新消耗的样本集合，则任务 q 的曝光为 E_q = sum_s sum_(x in B_s) 1[task(x)=q]。由于存在重复消耗和相互重叠的任务历史，该量衡量模型接受的监督量，与唯一原始交互数不同。本文据此对齐不同模型的任务监督。

<!-- PARAGRAPH: methods.exposure.p02 -->
<!-- EVIDENCE: M3,C3 -->

**EN**

With an effective batch of 8, 3,000, 6,000, and 12,000 single-task updates correspond to 24k, 48k, and 96k exposure; N200 uses 25,000 updates and 200k exposure. M1-48 and M1-96 use 12,000 and 24,000 total updates, corresponding to 48k and 96k expected examples per task under balanced mixing. M1-96 therefore receives 192k total task examples when compared with the 96k single-task specialists. Its per-task accounting assumes that resumed training correctly skips already consumed data. [TABLE: training_exposure] separates optimizer steps, total exposure, and expected per-task exposure.

**ZH**

在有效 batch 为 8 时，单任务的 3,000、6,000 和 12,000 次更新分别对应 24k、48k 和 96k 曝光；N200 使用 25,000 次更新，对应 200k 曝光。M1-48 与 M1-96 分别进行总计 12,000 和 24,000 次更新，在均衡混合下预期每任务接收 48k 和 96k 个样本。因此，与 96k 单任务专家比较时，M1-96 的任务样本总量为 192k。其每任务统计以续训时正确跳过已消耗数据为前提。[TABLE: training_exposure] 分别列出优化器步数、总曝光和预期每任务曝光。

<!-- PARAGRAPH: methods.exposure.p03 -->
<!-- EVIDENCE: C3,C7,M7 -->

**EN**

N200 provides a near-full-pool one-pass anchor: its 200,000 examples amount to approximately 94.0% of the 212,725 legal N training examples. SASRec alignment uses actual consumed-example counts, including the short final batch. Its S47, S94, S188, and S391 points consume 24,064, 48,128, 96,256, and 200,000 examples, respectively. The first three are approximately 0.27% above their LLM targets, while S391 matches N200 at the recorded exposure.

**ZH**

N200 提供一个接近完整样本池的单遍训练参照点：其 200,000 个样本相当于 212,725 个合法 N 训练样本的约 94.0%。SASRec 对齐采用实际消耗样本数，其中包括不足完整 batch 的末尾批次。S47、S94、S188 和 S391 分别消耗 24,064、48,128、96,256 和 200,000 个样本。前三点比对应 LLM 目标高约 0.27%，S391 则在记录曝光上与 N200 对齐。
