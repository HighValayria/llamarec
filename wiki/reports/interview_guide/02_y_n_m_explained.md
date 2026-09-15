---
title: "02 y n m explained"
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
# 02 Y / N / M Explained

## Y-K0

### 它是什么

[FACT] Y-K0 是 Yes/No preference prediction。输入是用户 history 和一个 target item，输出只允许是 `Yes` 或 `No`。

概率语义：

```text
P(Like | History, Target Item)
```

### 输入是什么

[FACT] Y sample 的字段来自 `src/data/build_preference.py`：

- `history`: 同一用户中 `timestamp < target.timestamp` 的最近若干条交互，默认最多 10 条。
- `target`: 当前要判断的 item。
- `label`: `Yes` 或 `No`。
- `positive_rating_threshold`: 当前配置为 4。

### label 怎么构造

[FACT] `rating >= 4 -> Yes`，`rating < 4 -> No`。这个阈值来自 `configs/experiment.yaml` 的 `dataset.positive_rating_threshold: 4`。

[INTERPRETATION] 在 1-5 rating 数据里，4/5 通常代表明确正反馈。这个阈值不是说 3 一定讨厌，而是为了构造清晰的二分类偏好监督。

### 为什么 history 必须 timestamp < target

[FACT] 代码里 `_strict_history_before_target()` 只保留 `item["timestamp"] < target_timestamp`。如果用 `<=`，同 timestamp 的 target 或未来同桶 item 会进入 history。

### 同 timestamp 怎么处理

[FACT] Y 允许同一个 timestamp bucket 内多个 target 共享同一段严格历史。原因是 Y 问的是“这个 target 喜不喜欢”，不需要在同 timestamp 内建立先后顺序。

### 训练模型到底学什么

[FACT] `PreferenceTrainingDataset` 把 prompt 和答案拼成 causal LM 样本，但 labels 只在答案 token 位置不是 `-100`，所以 loss 只监督 `Yes/No` 答案，不监督复述 prompt。

### 推理时 P(Yes) 怎么得到

[FACT] `score_yesno()` 取 prompt 后下一 token 对 `Yes` 和 `No` 的 logit，softmax 得到 `p_yes/p_no`。如果答案不是 single token，代码会退回 sequence likelihood；`Yes/No` 会被 tokenization report 检查。

### AUC 怎么算

[FACT] `src/eval/binary_metrics.py` 用连续 `score = P(Yes)` 做 rank-sum AUC。AUC 不需要 threshold，它衡量正样本 score 是否整体高于负样本。

### 为什么 P(Yes) 可以给多个候选排序

[FACT] Y adapter evaluation 会对同一个 N candidate record 的每个候选分别构造一个 Y prompt，然后用每个候选的 `P(Yes)` 排序。

### 为什么这仍然不等于 next-item prediction

[FACT] Y ranking 的分数是 `P(Like | History, Candidate)`；N ranking 的分数是 `P(Candidate is next interaction | History, Candidate Set)`。一个用户可能喜欢很多候选，但下一次只会交互一个。

[INTERPRETATION] Y 更像“静态偏好判断”，N 更像“序列行为选择”。把喜欢程度最高的候选排第一，不保证它是下一次真实点击/评分/交互。

### 用户例子

假设同一用户按时间交互：

```text
A(5)
B(2)
C(4)
D(1)
E(5)
```

若每个 item timestamp 都严格递增，Y 样本可以理解为：

```text
target A, history [], label Yes
target B, history [A(5)], label No
target C, history [A(5), B(2)], label Yes
target D, history [A(5), B(2), C(4)], label No
target E, history [A(5), B(2), C(4), D(1)], label Yes
```

实际 train/valid/test 哪些样本进入哪一 split，由 timestamp bucket split 决定；上面只是语义例子。

## N-K0

### 它是什么

[FACT] N-K0 是 full-sequence next-item prediction。输入是 history 和候选集合，输出 A/B/C/D/E 中哪个 candidate 是下一次真实交互。

概率语义：

```text
P(Next Interaction Candidate Label | History, Candidate Set)
```

### N 的目标到底是什么

[FACT] ground truth 是 full sequence 的下一次真实 interaction，不是下一次喜欢的 item，也不是下一次 rating >= 4 的 item。

### 为什么不是“下一个喜欢的 item”

[FACT] `configs/experiment.yaml` 明确写了 N 的 `ground_truth_source: next_interaction_in_full_sequence`。`src/data/build_next_item.py` 也不检查 target rating。

[INTERPRETATION] 推荐系统要预测行为序列时，低 rating 的交互仍然是用户实际发生的下一步行为。如果过滤掉低 rating，就把 next interaction 改成 next positive，任务语义变了。

### 候选集合怎么构造

[FACT] N sample 自带 `candidate_movie_ids`、`ground_truth_movie_id`、`ground_truth_index`、`label_set`。正式 evaluation 读取固定 candidate files，不在评测时重新采样。

[FACT] random negative 只排除当前 ground truth；不排除用户看过/喜欢过的 item。PopMatch negative 从 popularity 接近 target 的 item 中采样。

### 模型输出为什么是 candidate token

[FACT] prompt 列出候选：

```text
A. title1
B. title2
C. title3
...
Answer with exactly one option:
A
B
C
...
Answer:
```

训练时答案就是 label，比如 `C`。这样 inference 可以直接取 A/B/C/... 的下一 token logits。

### score_candidates() 到底在算什么

[FACT] `score_candidates()` 对 label set 计算答案 log score，single-token 时直接取下一 token logits，再 softmax 成 `label_probabilities`。排序分数就是 `[P(A), P(B), ...]`。

### timestamp bucket 为什么重要

[FACT] 同 timestamp 内没有可观察先后顺序。N 必须知道唯一“下一次”是谁，所以如果下一 timestamp bucket 有多个 item，代码只跳过那个 ambiguous N sample。

### 为什么只 skip sample 而不是整个 user

[FACT] `split.py` 的 tie policy 是 `skip_entire_user_on_tie: false`，N policy 是 `skip only ambiguous next-item samples`。

[INTERPRETATION] 一个用户可能只有某些 timestamp bucket ambiguous，其他 bucket 仍然能产生合法 transition。跳过整个 user 会浪费可用监督。

### 用户例子

对于：

```text
A(5)
B(2)
C(4)
D(1)
E(5)
```

所有合法 N transition 是：

```text
A -> B
A,B -> C
A,B,C -> D
A,B,C,D -> E
```

[FACT] 即使 `B rating=2`、`D rating=1`，它们仍然是合法 next interaction target。N 不问“喜欢不喜欢”，问“下一次发生了什么”。

## M1

### 它是什么

[FACT] M1 是一个 Y + N multi-task adapter。它不是两个模型，也不是先 Y 后 N；它把 Y 样本和 N 样本按比例交错编码到一个训练数据集。

### Y/N 怎么混合

[FACT] `MultitaskTrainingDataset` 用 `task_ratio_y` 和 `task_ratio_n` 计算 cycle。默认 M1 是 1:1：每个 cycle 先放 1 个 Y example，再放 1 个 N example。

### 为什么不是先训练 Y 再训练 N

[INTERPRETATION] sequential training 容易出现 catastrophic forgetting：后训练的任务会覆盖前一个任务的 adapter 行为。M1 采用 interleaving 是为了让同一个 adapter 在训练过程中持续看到两种监督。

### M1 的 1:1 到底是什么意思

[FACT] 1:1 指 interleaved train examples 的 Y/N 样本比例。不是 loss 权重自动相等，也不是总 compute 严格等于 single-task。

### 为什么 M1 3000 steps 不能简单理解成比 N-K0 训练多一倍

[FACT] 结果报告显示 M1 3000 optimizer steps 下 N-task exposure 是 12000，total exposure 是 24000；N-K0 1500 steps 下 N-task exposure 是 12000。因为 M1 的 steps 分给 Y 和 N 两类任务。

### M1 的 N-task exposure 实际是多少

[FACT] 当前正式表格中 MovieLens M1：N-task sample exposure `12000`，total supervision exposure `24000`，optimizer steps `3000`，effective batch `8`。

### 为什么 M1 可以同时做 binary preference + next-item ranking

[FACT] evaluation 里同一个 M adapter 分别走两个接口：M-Y 用 `score_yesno()` 得到 `P(Yes)`，M-N 用 `score_candidates()` 得到候选标签概率。

### 为什么当前结果支持 unified tradeoff 而不是 positive transfer

[FACT] M1 接近 Y-K0 的 binary 能力，但 MovieLens PopMatch ranking HR@1 `0.5244` 低于 N-K0 `0.5447`；multi-seed 下 N-K0 也始终高于 M1。

[INTERPRETATION] 如果是 positive transfer，M1 应该至少在 N ranking 上超过 N-K0，或在 Y binary 上超过 Y-K0。当前证据更像“一套 adapter 同时保住两种能力，但每个专业任务仍有 specialist 上限”。

