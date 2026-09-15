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

N-trained LlamaRec leads SASRec at all four approximately matched seed42 downstream task-sample exposure points. On validation, the HR@1 gap narrows from +0.2957 at 96k to +0.1767 at 200k. [TABLE: n_vs_sasrec_exposure] retains exact exposures and validation/frozen-test values; [FIGURE: n_vs_sasrec_exposure] shows the validation trajectories.

**ZH**

接受N任务训练的LlamaRec在四个seed42下游任务样本曝光近似匹配点均领先SASRec。验证HR@1差距从96k时的+0.2957缩小到200k时的+0.1767。[TABLE: n_vs_sasrec_exposure]保留精确曝光以及验证与冻结测试数值，[FIGURE: n_vs_sasrec_exposure]展示验证轨迹。

<!-- PARAGRAPH: results.rq5.p02 -->
<!-- EVIDENCE: C7 -->

**EN**

SASRec nevertheless improves strongly with additional supervision. The comparison therefore pairs N's lead with the baseline's continuing response and aligns only downstream task-sample exposure, not pretraining, tokens, updates, FLOPs, time, or end-to-end resource efficiency.

**ZH**

SASRec仍随额外监督明显改善。因此，这一比较同时保留N的领先与基线的持续响应，并且只对齐下游任务样本曝光，不对齐预训练、token、更新次数、FLOPs、时间或端到端资源效率。
