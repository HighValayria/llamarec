---
id: abstract
title: {en: Abstract, zh: 摘要}
status: draft
---

<!-- PARAGRAPH: abstract.p01 -->
<!-- EVIDENCE: C1,C2,C3,C4,C5,C6,C7,C8,M3,M5,M7 -->

**EN**

Empirical conclusions about large language models (LLMs) for recommendation can depend on what is supervised, how much downstream supervision a model consumes, and how candidates are evaluated. We study these dependencies using Llama-3.2-3B-Instruct with QLoRA, taking MovieLens-1M as the main dataset and Amazon Musical Instruments as a directional ranking-side check. We compare rating-derived preference prediction (Y), next-interaction prediction (N), and a shared Y+N multitask adapter (M1), trace task-sample exposure, evaluate alternative candidate protocols, and compare N-trained LlamaRec with SASRec at approximately matched downstream exposures. The complete Y and N formulations yield distinct measured capability profiles. In the MovieLens seed42 trajectory, Y's measured gains through 96k are limited or uneven, whereas N ranking improves across measured validation and test points through 200k. On a common cross-task-safe subset, the standard-k5 N-specialist-M1 validation gap narrows from 48k to 96k per task across all three metrics, although test does not reproduce the narrowing. At 96k, three training seeds retain a small but consistently positive N advantage, while M1 preserves comparable Y-side preference capability. Alternative candidate protocols materially change the remaining specialist-multitask gap. N-trained LlamaRec leads the evaluated SASRec baseline at four approximately matched downstream task-sample exposure points, but SASRec improves strongly and the gap narrows at 200k. Safe ranking directions also appear on Amazon at earlier seed42 operating points. These results show that recommendation capability and relative model performance are conditional on prediction formulation, cumulative downstream exposure, and candidate evaluation protocol.

**ZH**

关于大语言模型推荐的经验结论，可能取决于模型接受何种监督、消耗多少下游监督，以及如何评估候选物品。本文采用Llama-3.2-3B-Instruct与QLoRA，以MovieLens-1M为主要数据集，并以Amazon Musical Instruments作为排序侧方向性检验。研究比较评分产生的偏好预测Y、下一交互预测N和共享Y+N多任务adapter M1，追踪任务样本曝光，考察不同候选协议，并在下游曝光近似匹配时比较接受N任务训练的LlamaRec与SASRec。完整的Y与N预测形式呈现不同的被测能力结构。在MovieLens seed42轨迹中，Y到96k的被测增益有限或不均匀，N排序则在验证集和测试集的已测点持续改善至200k。在共同cross-task-safe子集上，标准k5的N专家-M1验证差距在三个指标上均从每任务48k到96k收窄，但测试集没有复现这一收窄。96k时，三个训练seed均保留小幅且方向一致的N优势，M1同时保持与Y专家接近的被测偏好能力。其他候选协议明显改变了剩余的专家与多任务差距。接受N任务训练的LlamaRec在四个下游任务样本曝光近似匹配点均领先被评估的SASRec基线，但SASRec随监督增加明显改善，200k时差距缩小。Amazon的较早seed42运行点也呈现满足安全条件的排序方向。这些结果表明，对推荐能力和模型相对表现的解释应结合预测形式、累计下游曝光和候选评估协议。
