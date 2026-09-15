---
id: abstract
title: {en: Abstract, zh: 摘要}
status: draft
---

<!-- PARAGRAPH: abstract.p01 -->
<!-- EVIDENCE: C1,C2,C3,C4,C5,C6,C7,C8,M3,M5,M7 -->

**EN**

Empirical conclusions about large language models (LLMs) for recommendation can depend on what is supervised, how much downstream supervision a model consumes, and how candidates are evaluated. We study these dependencies using Llama-3.2-3B-Instruct with QLoRA, taking MovieLens-1M as the main dataset and Amazon Musical Instruments as a directional ranking-side check. We compare rating-derived preference prediction (Y), next-interaction prediction (N), and a shared Y+N multitask adapter (M1), trace task-sample exposure, evaluate alternative candidate protocols, and compare N-trained LlamaRec with SASRec at approximately matched downstream exposures. The complete Y and N formulations yield distinct measured capability profiles. In the MovieLens seed42 trajectory, Y's measured gains through 96k are limited or uneven, whereas N ranking improves across measured validation and test points through 200k. Under standard k5 evaluation, the N-specialist-M1 validation gap narrows substantially from 48k to 96k per task. The 96k small-gap regime is reproduced across three training seeds; held-out tests nevertheless retain a modest N advantage, while M1 preserves comparable Y-side preference capability. Alternative candidate protocols materially change the remaining specialist-multitask gap. N-trained LlamaRec leads the evaluated SASRec baseline at four approximately matched downstream task-sample exposure points, but SASRec improves strongly and the gap narrows at 200k. Key ranking directions also appear on Amazon at earlier seed42 operating points. These results show that recommendation capability and relative model performance are conditional on prediction formulation, cumulative downstream exposure, and candidate evaluation protocol.

**ZH**

关于大语言模型推荐的经验结论，可能取决于模型接受何种监督、消耗多少下游监督，以及如何评估候选物品。本文采用 Llama-3.2-3B-Instruct 与 QLoRA，以 MovieLens-1M 为主要数据集，并以 Amazon Musical Instruments 作为排序侧方向性检验。研究比较评分产生的偏好预测 Y、下一交互预测 N 和共享 Y+N 多任务 adapter M1，追踪任务样本曝光，考察不同候选协议，并在下游曝光近似匹配时比较接受 N 任务训练的 LlamaRec 与 SASRec。完整的 Y 与 N 预测形式呈现不同的被测能力结构。在 MovieLens seed42 轨迹中，Y 到 96k 的被测增益有限或不均匀，N 排序则在验证集和测试集的已测点持续改善至 200k。标准 k5 验证中，N 专家与 M1 的差距从每任务 48k 到 96k 明显缩小。在 96k 运行点，三个训练种子复现了小差距区间，留出测试仍保留 N 的小幅优势。M1 在该运行点同时保持了与 Y 专家接近的被测偏好能力。其他候选协议明显改变了剩余的专家与多任务差距。接受 N 任务训练的 LlamaRec 在四个下游任务样本曝光近似匹配点均领先被评估的 SASRec 基线，但 SASRec 随监督增加明显改善，200k 时差距缩小。Amazon 的较早 seed42 运行点也呈现相同的关键排序方向。这些结果表明，对推荐能力和模型相对表现的解释应结合预测形式、累计下游曝光和候选评估协议。
