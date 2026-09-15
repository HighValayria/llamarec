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

SASRec [@kang2018sasrec] supplies a sequential baseline using item and position embeddings with causal sequence encoding. The evaluated repository implementation trains a next-target classifier with full-item cross-entropy and scores the fixed evaluation candidates from its sequence representation. Exposure-aligned runs use a batch size of 512, with actual consumption recorded for the final batch. This implementation and its recorded training regime define the SASRec baseline evaluated here.

**ZH**

SASRec [@kang2018sasrec] 通过物品嵌入、位置嵌入和因果序列编码提供序列推荐基线。被评估的仓库实现以全物品交叉熵训练下一目标分类器，再利用序列表示为固定评估候选评分。曝光对齐运行采用 batch size 512，并记录末尾 batch 的实际消耗量。本文的 SASRec 基线对应这一实现及其记录的训练设置。

<!-- PARAGRAPH: methods.baseline.p02 -->
<!-- EVIDENCE: C7,C9,M7 -->

**EN**

The principal comparison pairs N and SASRec at four approximately matched N-task exposures on the same PopMatch-k5 candidates within each data split. Validation guides the exposure decisions, and the corresponding frozen test comparisons assess the selected operating points. Earlier high-exposure SASRec runs provide a separate reference for performance under substantially more repeated supervision. The comparison aligns task-sample exposure; computational scope is discussed separately.

**ZH**

主要比较在四个近似对齐的 N 任务曝光点上进行，N 与 SASRec 在各数据划分中使用相同的 PopMatch-k5 候选。验证集指导曝光决策，对应的冻结测试比较评估所选运行点。较早的高曝光 SASRec 运行则为大量重复监督下的表现提供独立参照。这里对齐的是任务样本曝光，计算范围另行讨论。
