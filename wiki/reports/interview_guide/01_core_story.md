---
title: "01 core story"
type: report
status: current
authority: descriptive
source: agent
created: 2026-08-23
updated: 2026-08-23
last_verified: 2026-08-23
related_code:
  - configs/experiment.yaml
  - src/data/build_step2.py
  - src/data/split.py
  - src/data/build_preference.py
  - src/data/build_next_item.py
  - src/eval/candidate_sets.py
  - src/eval/ranking_metrics.py
  - src/eval/binary_metrics.py
  - src/train/train_y.py
  - src/train/train_n.py
  - src/train/train_m.py
  - src/inference/scoring.py
  - src/inference/evaluate_y_adapter.py
  - src/inference/evaluate_n_adapter.py
  - src/inference/evaluate_m_adapter.py
---
# 01 Core Story

## 1 Sentence

[FACT] LlamaRec 用同一个 Llama-3.2-3B-Instruct + QLoRA 框架比较 Y-style preference supervision、N-style next-interaction supervision 和 Y/N multi-task supervision，证明“喜欢预测”和“下一次交互预测”是不同推荐语义，并把这个结论放到 hard candidates、SASRec sample exposure、多 seed 和 Amazon 第二数据集下检验边界。

## 30 Second Version

这个项目不是简单做一个 LLM recommender，而是在问一个更具体的问题：推荐里的“用户喜不喜欢这个 item”和“用户下一次实际会交互哪个 item”是不是同一种能力。

我把任务拆成 Y-K0 和 N-K0：Y 是 history + target item 输出 Yes/No，学 `P(Like | history, item)`；N 是 history + candidates 输出 A/B/C/D/E，学真实 next interaction。然后做 M1，把 Y 和 N 1:1 混合到一个 adapter 里。

结果是：Y-K0 最适合二分类偏好，N-K0 最适合 next-item ranking，M1 能统一两种能力但 ranking 低于 N-K0。这个结论在 PopMatch hard candidates、MovieLens multi-seed 和 Amazon seed42 上方向成立；和 SASRec 比较时必须按 sample exposure 讲，不能说 LLM 全面胜出。

## 3 Minute Version

我这个项目的核心问题是：推荐能力不是一个单一概念。很多 LLM recommendation 工作会把“判断用户是否喜欢一个 item”和“预测用户下一次会交互哪个 item”混在一起，但这两个目标其实语义不同。

所以我构造了三类监督。第一类是 Y-K0，也就是 Yes/No preference prediction。输入是用户历史和一个 target item，target rating 大于等于 4 就是 Yes，否则 No。它学到的是 `P(Like | History, Item)`。第二类是 N-K0，也就是 next-item prediction。输入是用户历史和一组候选，ground truth 是 full sequence 里下一次真实交互，不管 rating 是高还是低。模型输出 A/B/C/D/E 这样的候选标签。第三类是 M1，一个 adapter 混合 Y 和 N 训练，目标是看能不能用一个模型统一这两种能力。

数据上我用了严格时间协议：history 必须是 `timestamp < target timestamp`，同 timestamp 没有可观察顺序。Y 允许同 timestamp bucket 里的多个 target 共享同一段严格历史；N 如果下一 timestamp bucket 有多个 item，就只跳过那个 ambiguous next-item 样本，不跳过整个 user。

实验结果的主线很清楚。Y-K0 在 binary preference 上最好或接近最好，MovieLens validation-calibrated F1 大约 `0.7831`。但如果把 Y 的 `P(Yes)` 拿来给候选排序，它在 PopMatch-k5 上 HR@1 只有 `0.1854`，明显弱于 N-K0 的 `0.5447`。这说明 preference score 不能直接替代 next-item score。M1 在 binary 上接近 Y，但 ranking 低于 N-K0，MovieLens PopMatch HR@1 是 `0.5244` vs `0.5447`。所以我会把它解释成 unified tradeoff，而不是 positive transfer。

为了避免结果只是因为候选太简单，我做了 PopMatch。Random negatives 很容易让 popularity shortcut 起作用，所以 PopMatch 选 popularity 接近 target 的 negatives。MovieLens 上 PopMatch 把 random candidate 的 target-negative popularity gap 从六百多降到四十多，N-K0 仍然高于 M1。k20/k50 进一步说明候选数增加后任务更难，而且 N-K0 与 M1 的差距变大。

然后是 baseline。Popularity 和 BPR-MF 在 Random-k5 看起来很强，但 PopMatch 下明显掉。SASRec 是最强的传统序列 baseline；如果只按 optimizer steps 对齐，SASRec 很强甚至超过 N-K0。但这个比较不公平，因为 SASRec batch size 512，N-K0 effective batch 8。按 N-task sample exposure 粗匹配时，MovieLens N-K0 HR@1 `0.5466`，SASRec exp-match `0.2700`；但SASRec s3000 在约 `1.53M` exposure 下能到 `0.6243`，超过当前约 `12k` exposure 的 N-K0。所以正确结论是：matched exposure 下 N-K0 更 sample-efficient；远多监督的 SASRec 可超过当前 N-K0；完整 high-budget head-to-head 还没做。

稳定性上，MovieLens seeds 42/43/44 下 N-K0 都高于 M1，也都高于 closest-exposure SASRec；远多监督的 SASRec checkpoints 也稳定高于当前低曝光 N-K0，但属于另一个预算 regime。Amazon Musical Instruments seed42 方向复现：PopMatch 下 N-K0 `0.4669`，M1 `0.4582`，SASRec exp-match `0.1757`。不过 Amazon 只有 seed42，所以只能说 directional cross-dataset replication。

## 当前最核心一句话

[INTERPRETATION] 这个项目真正证明的不是“LLM recommender 更强”，而是“不同推荐监督会塑造不同能力；next-interaction supervision 对 ranking 更合适，multi-task 能统一但有 tradeoff，而与 SASRec 的强弱取决于样本曝光预算”。

## 三类信息边界

[FACT] N-K0 在 MovieLens PopMatch-k5 上 HR@1 `0.5447`，M1 是 `0.5244`，Y-K0 P(Yes) ranking 是 `0.1854`。

[INTERPRETATION] 这支持 Y 和 N 学到不同 recommendation semantics。

[HYPOTHESIS] LLM 的 sample efficiency 可能部分来自预训练知识或语言化 item titles，但当前实验没有直接做 text-information ablation，不能当成已验证机制。
