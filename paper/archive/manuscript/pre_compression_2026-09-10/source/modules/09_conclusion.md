---
id: conclusion
title: {en: Conclusion, zh: 结论}
status: draft
---

<!-- PARAGRAPH: conclusion.p01 -->
<!-- EVIDENCE: C1,C2,C3,C4,C5,C6,C7,C8 -->

**EN**

This study examined how conclusions about LLM recommendation change across complete supervision formulations, cumulative downstream task-sample exposure, and candidate evaluation protocols. Within a shared adaptation setting, we contrasted rating-derived preference prediction (Y), next-interaction prediction (N), and a multitask adapter (M1); traced task-specific exposure responses; and compared N-trained LlamaRec with SASRec at approximately matched downstream exposure.

**ZH**

本研究考察在完整监督形式、累计下游任务样本曝光和候选评估协议发生变化时，关于 LLM 推荐的结论如何随之改变。在共同的适配设置中，研究对比了由评分产生的偏好预测 Y、下一交互预测 N 和共享多任务 adapter M1，追踪不同任务的曝光响应，并在下游曝光近似匹配时比较接受 N 任务训练的 LlamaRec 与 SASRec。

<!-- PARAGRAPH: conclusion.p02 -->
<!-- EVIDENCE: C1,C2,C3,C4,C5,M3 -->

**EN**

Supervision formulation produced distinct measured capability profiles: Y addressed whether a candidate was liked, whereas N selected the next observed interaction from a candidate set. Their contrast therefore concerns complete prediction formulations rather than a causally isolated semantic factor. Across the full MovieLens seed42 exposure trajectory, Y's measured gains through 96k were limited or uneven across metrics, while N's ranking performance continued to improve across the evaluated exposure points through 200k on both validation and test. The same trajectory showed substantial narrowing of the N-specialist and M1 gap on standard-k5 validation from 48k to 96k per task. Independent seeds 43 and 44 reproduced the resulting 96k small-gap regime, while frozen tests across all three seeds retained a modest N advantage. At that operating point, M1 also preserved comparable measured Y-side preference capability. Within this evaluated setting, the specialist advantage observed at lower task-sample exposure need not characterize the shared model's relative performance after further adaptation; the full exposure trajectory remains supported by seed42 alone.

**ZH**

不同监督形式形成了不同的被测能力结构：Y 回答候选物品是否受到用户喜欢，N 则从候选集合中选择下一次观测交互。因此，两者的差异对应完整预测形式，而不是对某个语义因素的因果隔离。在 MovieLens seed42 的完整曝光轨迹中，Y 到 96k 时在不同指标上的被测增益有限或不均匀，而 N 的排序表现则在验证集和测试集的已测曝光点上持续改善至 200k。该轨迹还显示，每任务曝光从 48k 提高到 96k 后，标准 k5 验证集上的 N 专家与 M1 差距明显缩小。seed43 和 seed44 的独立运行复现了 96k 的小差距区间，三个种子的冻结测试结果仍保留 N 的小幅优势；同一运行点上的 M1 也保持了与 Y 专家接近的被测偏好能力。在这一已评估设置中，低任务样本曝光下观察到的专家优势不能直接代表共享模型经过进一步适配后的相对表现；完整曝光轨迹的证据仍仅来自 seed42。

<!-- PARAGRAPH: conclusion.p03 -->
<!-- EVIDENCE: C5,C6,C7,C8,M5,M7 -->

**EN**

This closer standard-k5 relationship was not invariant to the candidate protocol. At 96k, k20 exposed a much larger N-specialist advantage across all three training seeds and both data splits. The independently constructed k50 protocol also favored N, but by less than k20 and with seed-dependent magnitude; because count, composition, sampling method, and difficulty changed together, the observed differences attach to the protocols as a whole rather than to candidate count alone. The cross-family comparison was likewise tied to its operating points. N-trained LlamaRec led the evaluated SASRec baseline at all four approximately matched downstream task-sample exposures, but SASRec improved substantially with additional supervision and the gap was smaller at 200k than at 96k. Amazon Musical Instruments reproduced the key ranking directions, namely N over Y-as-ranker, M1, and the evaluated SASRec reference, only at its available earlier seed42 operating points, providing directional external support rather than a second full trajectory.

**ZH**

标准 k5 下较为接近的模型关系并未在不同候选协议间保持不变。在 96k 时，三个训练种子和两个数据划分的 k20 结果都呈现出明显更大的 N 专家优势。独立构造的 k50 协议同样偏向 N，但差距小于 k20，幅度也随种子变化；由于候选数量、组成、采样方法和难度同时改变，观察到的差异对应协议整体，不能单独归于候选数量。跨模型系列的比较同样取决于具体运行点。在四个下游任务样本曝光近似匹配点上，接受 N 任务训练的 LlamaRec 均领先被评估的 SASRec 基线，但 SASRec 随额外监督明显改善，200k 时的差距也小于 96k。Amazon Musical Instruments 只在现有较早的 seed42 运行点上重现了 N 领先 Y-as-ranker、M1 和被评估 SASRec 参照的关键排序方向，因此提供的是外部方向性支撑，而不是第二条完整曝光轨迹。

<!-- PARAGRAPH: conclusion.p04 -->
<!-- EVIDENCE: C1,C2,C3,C4,C5,C6,C7,C8 -->

**EN**

Taken together, these findings support interpreting adapted language models for recommendation in relation to the conditions under which their performance is observed. Claims about recommendation capability and relative model performance should therefore be reported together with the prediction formulation, cumulative downstream task-sample exposure, and candidate evaluation protocol.

**ZH**

综合这些发现，对适配语言模型推荐表现的解释应结合产生相应结果的具体条件。关于推荐能力和模型相对表现的结论，应同时说明预测形式、累计下游任务样本曝光和候选评估协议。
