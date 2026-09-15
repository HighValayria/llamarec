---
title: "06 inference and metrics"
type: report
status: current
authority: descriptive
source: agent
created: 2026-08-24
updated: 2026-08-24
last_verified: 2026-08-24
related_code:
  - src/inference/scoring.py
  - src/inference/prompts.py
  - src/inference/evaluate_y_adapter.py
  - src/inference/evaluate_n_adapter.py
  - src/inference/evaluate_m_adapter.py
  - src/inference/tokenization_check.py
  - src/eval/binary_metrics.py
  - src/eval/ranking_metrics.py
---

# 06 Inference And Metrics

## 一句话

[FACT] 项目评测不靠生成字符串，而是直接读取答案 token logits：Y 取 `Yes/No` logits 得 `P(Yes)`，N 取 `A/B/C/...` logits 得候选 label probabilities。

## score_yesno()

代码：`src/inference/scoring.py`

流程：

```text
Y prompt
  |
  v
Llama / adapter forward
  |
  v
取 Answer: 后下一 token logits
  |
  v
只取 Yes / No token 对应 logits
  |
  v
softmax
  |
  v
P(Yes), P(No)
```

为什么不用生成字符串：

[INTERPRETATION] 生成字符串只能给离散答案；AUC、排序、阈值校准都需要连续 score。

## score_candidates()

代码：`src/inference/scoring.py`

流程：

```text
N prompt with candidates A/B/C/D/E
  |
  v
取下一 token logits
  |
  v
只取 candidate labels 的 logits
  |
  v
softmax
  |
  v
P(A), P(B), P(C), ...
```

排序：

```text
scores = [P(A), P(B), P(C), ...]
ground_truth_index = 真实 next item 的候选位置
```

## single token 为什么重要

[FACT] 如果所有答案都是 single token，代码走 `real_single_token_logits`。

如果答案不是 single token：

```text
退回 sequence likelihood
```

所以 k50 的 A 到 AX 要做 tokenizer check。

面试说法：

> candidate label 最好是 single token，这样每个候选分数来自同一位置的下一 token logits，比较干净。

## Y ranking vs N ranking

Y-as-ranking:

```text
对每个 candidate 单独问：用户会喜欢它吗？
score = P(Yes)
```

N ranking:

```text
在同一个 candidate set 中问：哪个是下一次 interaction？
score = P(candidate label)
```

[FACT] Y-K0 PopMatch HR@1 `0.1854`，N-K0 PopMatch HR@1 `0.5447`。

[INTERPRETATION] 这说明 `P(Like)` 不是 `P(Next Interaction)` 的替代品。

## M inference

[FACT] 同一个 M adapter 有两个评测接口：

```text
M-Y: score_yesno() -> binary metrics
M-N: score_candidates() -> ranking metrics
```

## Binary metrics

代码：`src/eval/binary_metrics.py`

AUC:

```text
使用 continuous score = P(Yes)
rank-sum AUC
不需要 threshold
```

F1 / Accuracy:

```text
score >= threshold -> Yes
score < threshold  -> No
```

面试重点：

> AUC 看排序能力，不需要 threshold；F1/Accuracy 依赖 threshold，所以 threshold 不能在 test 上调。

## validation-calibrated F1

流程：

```text
validation set 上选 threshold
        |
        v
test set 固定使用这个 threshold
```

[INTERPRETATION] 这样避免 test label 泄漏到 threshold selection。

## Ranking metrics

代码：`src/eval/ranking_metrics.py`

HR@1:

```text
ground truth rank == 1 -> 1 else 0
```

NDCG@5:

```text
rank <= 5 -> 1 / log2(rank + 1)
rank > 5  -> 0
```

MRR:

```text
1 / rank
```

例子：

```text
GT rank = 1: HR@1=1, NDCG@5=1.000, MRR=1.000
GT rank = 2: HR@1=0, NDCG@5=0.631, MRR=0.500
GT rank = 5: HR@1=0, NDCG@5=0.387, MRR=0.200
GT rank = 6: HR@1=0, NDCG@5=0,     MRR=0.167
```

## Amazon Accuracy 为什么容易误导

[FACT] Amazon Y labels 中 Yes 明显占多数：Yes `437,418`，No `74,374`。

[INTERPRETATION] 正类比例高时，Accuracy 可能被多数类主导，所以 Amazon binary metrics 目前应谨慎当 diagnostic，不要当 paper-grade calibrated claim。

## 面试模板

如果问“为什么不用完整 autoregressive generation？”

> 因为我的答案空间是封闭的 Yes/No 或 A/B/C/D/E。直接取答案 token logits 更稳定、更便宜，也能得到连续概率，用于 AUC 和 ranking。

如果问“Y ranking 和 N ranking 数学意义为什么不同？”

> Y 是对每个候选分别估计喜欢概率；N 是在候选集合内估计哪个 label 是下一次真实交互。前者不归一到 candidate set 的 next-item 事件，后者是 candidate-label 竞争。
