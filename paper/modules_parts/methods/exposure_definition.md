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

Task-sample exposure counts examples consumed for task q, including repetitions: E_q = sum_s sum_(x in B_s) 1[task(x)=q], where B_s is optimizer step s's batch. It measures received supervision, not unique interactions, because examples may repeat and task histories overlap.

**ZH**

任务样本曝光统计任务q累计消耗的样本，包括重复样本：E_q = sum_s sum_(x in B_s) 1[task(x)=q]，其中B_s为第s次优化器更新的batch。由于样本可重复且任务历史重叠，它衡量接受的监督量，而非唯一交互数。

<!-- PARAGRAPH: methods.exposure.p02 -->
<!-- EVIDENCE: M3,C3 -->

**EN**

With effective batch 8, specialist updates map directly to task exposure. Balanced M1-48 and M1-96 receive expected per-task exposures of 48k and 96k and totals of 96k and 192k; this accounting assumes correct resume data skipping. [TABLE: training_exposure_compact] separates optimizer steps, total exposure, and Y/N exposure.

**ZH**

有效batch为8时，专家模型更新数直接对应任务曝光。均衡M1-48与M1-96的预期每任务曝光分别为48k和96k，总曝光为96k和192k；该统计以续训正确跳过已读数据为前提。[TABLE: training_exposure_compact]分别列出优化器步数、总曝光和Y/N曝光。

<!-- PARAGRAPH: methods.exposure.p03 -->
<!-- EVIDENCE: C3,C7,M7 -->

**EN**

N200 consumes 200,000 examples, about 94.0% of the 212,725-example legal N training pool, and serves as a near-one-pass anchor. SASRec uses recorded actual consumption, including short final batches: 24,064, 48,128, 96,256, and 200,000 examples. These points approximately match N24/N48/N96/N200 rather than equate computation.

**ZH**

N200消耗200,000个样本，约占212,725个合法N训练样本的94.0%，作为接近单遍训练的参照。SASRec采用包含末尾不足完整batch在内的实际消费量：24,064、48,128、96,256和200,000个样本。这些点近似匹配N24/N48/N96/N200，并不对齐计算量。
