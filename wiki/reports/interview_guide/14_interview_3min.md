---
title: "14 interview 3min"
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
# 14 Interview 3min

## 3 分钟讲稿

这个项目的出发点是：LLM 做推荐时，很多工作会把“用户是否喜欢这个 item”和“用户下一次会交互哪个 item”混在一起。但我认为这是两个不同的问题。喜欢是 preference prediction，下一次交互是 sequential behavior prediction。所以这个项目主要想回答：不同监督目标会不会让同一个 LLM 学到不同推荐能力？如果不同，multi-task 能不能统一？这些结论在 hard candidates、传统 baseline、不同训练预算和第二数据集上是否仍然成立？

方法上，我用了 Llama-3.2-3B-Instruct 做 4-bit QLoRA 微调，构造三类任务。Y-K0 是 Yes/No preference prediction：输入用户历史和一个 target item，rating 大于等于 4 是 Yes，否则 No。N-K0 是 next-item prediction：输入用户历史和一组候选，ground truth 是 full sequence 里下一次真实交互，不管 rating 高低，模型输出 A/B/C/D/E。M1 是一个 Y+N 的 multi-task adapter，1:1 interleaving，可以分别通过 Y 接口做二分类，也可以通过 N 接口做 ranking。

数据上我特别强调 strict temporal protocol。history 永远只能包含 `timestamp < target timestamp` 的交互。同 timestamp 没有真实顺序，所以 Y 允许同 bucket 多个 target 共享严格历史；N 如果下一个 bucket 有多个 item，就只跳过这个 ambiguous next-item 样本，不跳过整个用户。这个设计主要是为了避免 target 泄漏和未来交互泄漏。

结果上，Y 和 N 的语义边界很明显。MovieLens 上 Y-K0 的 binary F1 大约是 `0.7831`，M1 也接近 `0.7818`。但如果把 Y-K0 的 `P(Yes)` 拿来给 next-item candidates 排序，在 PopMatch-k5 上 HR@1 只有 `0.1854`，而 N-K0 是 `0.5447`。这说明 preference score 不能直接替代 next-item score。

M1 的结论也很关键。M1 在 binary 上保住了能力，ranking 也很强，但 MovieLens PopMatch-k5 HR@1 是 `0.5244`，低于 N-K0 的 `0.5447`。multi-seed 下 N-K0 也都高于 M1。所以我不会说 M1 有 positive transfer，而会说它是 unified tradeoff：一个模型能同时做两类任务，但 specialist 仍然更强。

为了避免 ranking 只是因为随机负样本太容易，我做了 PopMatch。Random-k5 会让 popularity shortcut 很明显，所以 PopMatch 选 popularity 接近 target 的 negatives。MovieLens 上 PopMatch 把 target-negative popularity gap 从六百多降到四十多，N-K0 仍然高于 M1。k20/k50 进一步说明候选数量增加后任务更难，N-K0 对 M1 的优势还变大。

baseline 方面，Popularity 和 BPR-MF 在 Random-k5 看起来强，但 PopMatch 下掉很多。SASRec 是最强传统序列 baseline。一个重要发现是：如果只按 optimizer steps 对齐，SASRec 会显得更强；但这是因为 SASRec batch size 512，而 LLM effective batch 8。按 N-task sample exposure 粗匹配时，MovieLens N-K0 HR@1 是 `0.5466`，SASRec exp-match 是 `0.2700`；但SASRec s3000 在约 `1.53M` exposure 下可以到 `0.6243`，超过当前约 `12k` exposure 的 N-K0。所以正确结论是：matched exposure 下 N-K0 更 sample-efficient；远多监督的 SASRec 可超过当前 N-K0；完整 high-budget head-to-head 还没做。

最后，我做了稳定性和外部验证。MovieLens seeds 42/43/44 下，N-K0 都高于 M1，也高于 closest-exposure SASRec；远多监督的 SASRec checkpoints 也稳定高于当前低曝光 N-K0，但这是另一个预算 regime。Amazon Musical Instruments seed42 下方向也复现：PopMatch-k5 N-K0 HR@1 `0.4669`，M1 `0.4582`，SASRec exp-match `0.1757`。不过 Amazon 只有 seed42，所以只能说 directional replication，不能说 multi-seed cross-dataset stability。

我会把这个项目的贡献总结成三点：第一，明确区分了 preference supervision 和 next-interaction supervision；第二，说明 multi-task 能统一但带 tradeoff；第三，给出了 hard-candidate 和 sample-exposure-aware baseline 比较，避免把 easy negative 或不公平预算下的结果说过头。
