---
id: rq5_sasrec_exposure
title:
  en: Exposure-Aware Comparison with SASRec
  zh: 曝光感知的 SASRec 比较
status: draft
---

<!-- PARAGRAPH: results.rq5.p01 -->
<!-- EVIDENCE: C7,M7 -->

**EN**

At all four evaluated approximately matched seed42 task-sample exposure points, N-trained LlamaRec achieves higher ranking accuracy than the evaluated SASRec baseline. On PopMatch-k5 validation, N24, N48, N96, and N200 achieve 0.5774, 0.6030, 0.6238, and 0.6516 HR@1, compared with 0.2731, 0.2930, 0.3281, and 0.4749 for S47, S94, S188, and S391. The absolute differences are +0.3043, +0.3100, +0.2957, and +0.1767. NDCG@5 and MRR show the same ordering, as do all four corresponding test comparisons. [TABLE: n_vs_sasrec_exposure] and [FIGURE: n_vs_sasrec_exposure] relate this advantage to the actual supervision exposure received by each model.

**ZH**

在四个已评估、任务样本曝光近似对齐的 seed42 运行点上，接受 N 任务训练的 LlamaRec 都具有高于被评估 SASRec 基线的排序准确性。在 PopMatch-k5 验证集上，N24、N48、N96 和 N200 的 HR@1 分别为 0.5774、0.6030、0.6238 和 0.6516，对应 S47、S94、S188 和 S391 的数值为 0.2731、0.2930、0.3281 和 0.4749。绝对差值依次为 +0.3043、+0.3100、+0.2957 和 +0.1767。NDCG@5 与 MRR 呈现相同排序，四个对应测试比较也均如此。[TABLE: n_vs_sasrec_exposure] 与 [FIGURE: n_vs_sasrec_exposure] 将这一优势与各模型实际获得的监督曝光联系起来。

<!-- PARAGRAPH: results.rq5.p02 -->
<!-- EVIDENCE: C7 -->

**EN**

SASRec also improves strongly with additional supervision, narrowing the HR@1 gap at 200k relative to 96k. On the test set at 200k, N200 reaches 0.6282 and S391 reaches 0.4511. Together, these observations distinguish strong ranking at limited task exposure from the ability to keep improving with more supervision. This comparison aligns task supervision rather than compute. Amazon then tests whether the main ranking directions extend beyond MovieLens.

**ZH**

SASRec 也随额外监督明显改善，使 200k 时的 HR@1 差距小于 96k。200k 测试比较中，N200 达到 0.6282，S391 达到 0.4511。综合这些观察，有限任务曝光下的较强排序表现，与随更多监督继续改善的能力，是需要分别考虑的两个方面。这里对齐的是任务监督，而非计算量。随后通过 Amazon 检验主要排序方向能否延伸到 MovieLens 之外。
