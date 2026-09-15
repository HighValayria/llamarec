---
title: "15 interview 15min"
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
# 15 Interview 10-15min

## 10-15 分钟讲稿

我先讲这个项目的核心动机。LLM recommender 里一个常见模糊点是：我们到底在训练模型判断用户“喜不喜欢”一个 item，还是训练它预测用户“下一次会交互”哪个 item。这两个问题在表面上都像推荐，但语义不一样。喜欢预测是 preference judgment，next-item prediction 是 sequential behavior prediction。我的项目就是把这两种监督拆开，用同一个 Llama 微调框架系统比较它们学到的能力。

具体来说，我设计了三个任务接口。第一个是 Y-K0，也就是 Yes/No preference prediction。输入是用户历史和一个 target item，target 的 rating 如果大于等于 4，就标成 Yes，否则 No。它学的概率可以理解为 `P(Like | History, Item)`。第二个是 N-K0，也就是 full-sequence next-item prediction。输入是用户历史和一组候选，ground truth 是用户 full sequence 里的下一次真实 interaction，不管这个 interaction 的 rating 是 5 还是 1。模型要输出 A/B/C/D/E 这样的 candidate label。第三个是 M1，一个 Y+N 的 multi-task adapter，把 Y 样本和 N 样本按 1:1 interleaving 混合训练。

数据构造上，我非常注意 temporal leakage。项目的硬规则是：history 只能包含 `timestamp < target timestamp` 的交互。不能用 `<=`，因为同 timestamp 内没有可观测先后顺序；如果把同 timestamp target 放进 history，就是泄漏。Y 任务里，同一个 timestamp bucket 可以有多个 target，它们共享同一段严格历史，因为 Y 只是问这个 item 喜不喜欢。N 任务不同，它必须有唯一的下一次真实 interaction，所以如果下一个 timestamp bucket 里有多个 item，这个 N sample 就 ambiguous，会跳过这个样本，但不会跳过整个 user。

然后是样本语义。举个简单例子：用户序列是 A(5)、B(2)、C(4)、D(1)、E(5)。Y 样本会是 target A label Yes，target B label No，target C label Yes，target D label No，target E label Yes，每个 target 的 history 是严格更早的交互。N 样本则是 A -> B，A,B -> C，A,B,C -> D，A,B,C,D -> E。这里 B rating=2、D rating=1 仍然是合法 next interaction，因为 N 不是 next liked item。

模型训练上，我用的是 `meta-llama/Llama-3.2-3B-Instruct`，4-bit QLoRA。选择 3B 是因为它在单卡 24GB 机器上比较可控，能做系统实验，而不是只做一个昂贵大模型 demo。4-bit quantization 是把 base model 以 NF4 量化加载，LoRA adapter 插到 q/k/v/o projection 和 MLP projection 这些 linear modules 上。配置里 LoRA `r=16`，`alpha=32`，dropout `0.05`。训练时 base model 不是全参数更新，保存的是 PEFT adapter 和 tokenizer。这样可以在有限预算下跑 Y、N、M、多 seed 和 baseline 诊断。

训练数据编码也很重要。Y 的训练 prompt 是 history + target + Yes/No question，代码会确保 target rating 不出现在 prompt 里。N 的 prompt 是 history + candidates，candidate 区域不带 rating。Dataset class 会把 prompt 和答案拼起来，但 labels 里只有答案 token 不是 `-100`，所以 loss 只监督 Yes/No 或 A/B/C/D/E 答案，而不是让模型学复述整个 prompt。

推理上我没有只看生成字符串，而是取连续概率。Y 的 `score_yesno()` 对 Yes 和 No token logits 做 softmax 得到 `P(Yes)`，所以可以算 AUC。N 的 `score_candidates()` 对 A/B/C/D/E label logits 做 softmax，用 candidate label probability 排序。这个设计也让 Y ranking 和 N ranking 的差异变得很清楚：Y ranking 是对每个候选单独算 `P(Yes)`，N ranking 是在同一个候选集合中算每个 label 是 next interaction 的概率。

核心结果第一部分是 Y 和 N 的差异。MovieLens 上，Y-K0 的 binary F1 大约 `0.7831`，说明 preference tuning 有效。但 Y-K0 如果拿 `P(Yes)` 给 next-item candidate 排序，在 PopMatch-k5 上 HR@1 只有 `0.1854`；N-K0 在同一 protocol 上是 `0.5447`。这说明 `P(Like)` 不能直接替代 `P(Next Item)`。这就是 RQ1 的核心：两个监督目标诱导的推荐能力不同。

第二部分是 M1。M1 的目的不是单纯超过所有 single-task，而是看能否统一两个任务。结果是它确实保住了很多 binary 能力，比如 MovieLens binary F1 接近 Y-K0；ranking 也强，PopMatch HR@1 是 `0.5244`，但仍低于 N-K0 的 `0.5447`。multi-seed 里 N-K0 也始终高于 M1，最小 HR@1 margin 是 `0.0104`。所以我把 M1 叫 unified tradeoff，而不是 positive transfer。

第三部分是 candidate difficulty。Random-k5 太容易，因为 random negatives 往往比 target 冷很多，模型或者 baseline 可能靠 popularity shortcut 做对。PopMatch 的做法是从 popularity 接近 target 的 item 里选 negatives。MovieLens 上，PopMatch 把 test target-negative mean absolute popularity gap 从大约 `663.6` 降到 `44.0`。在这个更难设置下，N-K0 仍然高于 M1，说明主 ranking 结论不只是 random negative 的副产品。k20/k50 又进一步增加候选数量，N-K0 和 M1 都明显下降，但 N-K0 的优势变大，k50 HR@1 是 `0.1995` vs `0.1219`。

第四部分是 baseline。Popularity 和 BPR-MF 在 Random-k5 上看起来很强，但 PopMatch 下明显下降，这说明 random candidates 的 popularity shortcut 很严重。SASRec 是更强、更合适的序列推荐 baseline。这里最容易被问的是公平性：一开始如果只按 optimizer steps 对齐，SASRec 1500/3000 steps 比 N-K0/M1 强。但这个比较隐藏了 sample exposure mismatch。N-K0 1500 steps、effective batch 8，对应 N exposure 12000；SASRec 1500 steps、batch 512，对应 exposure 767424，是 63.952 倍。按 closest N-task exposure 粗匹配时，SASRec 23 steps exposure 11776，HR@1 `0.2700`，低于 N-K0 `0.5466`。但SASRec s3000 HR@1 `0.6243`，高于当前约 `12k` exposure 的 N-K0。所以最终结论是：LLM 在 matched N-task exposure 下有 sample-efficiency 优势；SASRec 用远多 sequential supervision 可以超过当前 N-K0；但双方 high-exposure 对齐没做。

第五部分是 cold/tail。这个分析的目的不是宣称 LLM 擅长 cold-start，而是看 SASRec high-exposure anchor 相对当前 N-K0 的优势来自哪里。MovieLens PopMatch 的 coldest bucket `<=10` 只有 26 个样本，所以不能做强结论。诊断显示 SASRec high-exposure anchor 相对当前 N-K0 的整体优势主要在 middle/head buckets，不是 coldest bucket；但因为 coldest sample size 太小，我不会说项目证明了 LLM 擅长 cold-start。

第六部分是 multi-seed。seed 会影响 model initialization、data order、dropout 等，所以只看 seed42 不够。MovieLens seeds 42/43/44 的结果显示：Y-K0 binary F1 range 约 `0.0098`；N-K0 在所有 seed 上高于 M1；N-K0 在所有 seed 上高于 closest-exposure SASRec；high-exposure SASRec checkpoints 在所有 seed 上高于当前低曝光 N-K0。这让“远多监督的 SASRec anchor 可超过当前 N-K0”更稳定，但仍然不等于显著性检验、compute-matched 结论或 high-exposure head-to-head。

最后是 Amazon cross-dataset。MovieLens 比较密集，Amazon Musical Instruments 更稀疏，所以用它看外部有效性。Amazon 保留了 `57,439` users、`24,584` items、`511,792` interactions。PopMatch-k5 下 seed42 结果方向复现：N-K0 HR@1 `0.4669`，M1 `0.4582`，SASRec exp-match `0.1757`。但是 N-K0 over M1 的 margin 只有 `0.0087`，而且 Amazon 只有 seed42，所以我只说 directional cross-dataset replication，不说 Amazon multi-seed stability 或大幅优势。

如果总结贡献，我会说三点。第一，项目把 recommendation-tuned LLM 中的 preference prediction 和 next-interaction prediction 明确分开，并用结果证明它们不是同一种能力。第二，multi-task adapter 能统一两个接口，但目前是 tradeoff 而不是替代 specialist。第三，项目没有停在 easy random negatives，而是通过 PopMatch、candidate-size stress、baseline、sample exposure、multi-seed 和 Amazon，把 claim 的可靠性和边界讲清楚。

## 结尾防守句

[INTERPRETATION] 这个项目最有价值的地方不是提出新 architecture，而是把 LLM recommendation 的监督语义、评测 protocol 和 baseline fairness 拆清楚。它告诉我们：想讨论 LLM recommender，必须先说清楚你训练的是喜欢、下一次交互，还是一个多任务折中；也必须说清楚 candidates 和 training budget 是什么。
