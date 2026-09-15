---
title: "26 final one page cheatsheet"
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
# 26 Final One Page Cheatsheet

## 5 分钟恢复全项目

```text
问题
  推荐能力不是单一能力：
  喜欢一个 item != 下一次真实交互哪个 item
        |
        v
Y / N
  Y-K0: history + target -> Yes/No
       P(Like | History, Item), rating >= 4 是 Yes
  N-K0: history + candidates -> A/B/C/...
       target 是 full sequence 下一次真实 interaction
        |
        v
M
  M1: 一个 adapter, Y/N 1:1 interleaving
  能同时做 binary + ranking
  但当前是 unified tradeoff, 不是 positive transfer
        |
        v
困难候选
  Random-k5 太容易，有 popularity shortcut
  PopMatch-k5 匹配 target/negative popularity
  k20/k50 增加候选数，暴露更真实排序难度
        |
        v
Baseline
  Popularity / BPR-MF 控制 popularity 和 matrix factorization shortcut
  SASRec 是强 specialized sequential baseline
        |
        v
Sample Exposure
  optimizer steps != sample exposure != compute/FLOPs
  N-K0: 1500 steps, effective batch 8, N exposure 12000
  SASRec s1500: batch 512, N exposure 767424
        |
        v
Robustness
  candidate order 影响较小
  candidate size 影响很大
  cold/tail 只是诊断，coldest bucket n=26
        |
        v
Multi-seed
  MovieLens seeds 42/43/44:
  N-K0 > M1
  N-K0 > SASRec closest exposure
  SASRec high exposure > current N-K0(12k exposure)
        |
        v
Cross-dataset
  Amazon Musical Instruments seed42:
  N-K0 > M1, margin small
  N-K0 >> SASRec closest exposure
  不是 Amazon multi-seed
        |
        v
Final Conclusion
  Supervision semantics matter.
  N-style supervision is better for next-item ranking.
  M1 unifies but trades off.
  LLM-vs-SASRec is budget-regime dependent.
```

## 必背 6 数字

- Y-K0 binary F1: `0.7831`
- M1 binary F1: `0.7818`
- MovieLens PopMatch N-K0 HR@1: `0.5447`
- MovieLens PopMatch M1 HR@1: `0.5244`
- SASRec closest/high exposure HR@1: `0.2700 / 0.6243`
- Amazon PopMatch N-K0/M1 HR@1: `0.4669 / 0.4582`

## 最稳贡献表述

[FACT] Y-K0 is strong for binary preference; N-K0 is strong for next-item ranking.

[FACT] Y-K0 `P(Yes)` ranking is weak, so preference score is not a replacement for next-item score.

[FACT] M1 preserves both interfaces but does not beat N-K0 ranking.

[FACT] PopMatch and k20/k50 show candidate difficulty matters.

[FACT] SASRec is strong after much larger sequential exposure, but the project did not train N-K0 to the same 1.53M exposure.

[INTERPRETATION] The project is best framed as supervision-semantics and evaluation-fairness study for LLM recommendation tuning.

## 一句话

LlamaRec 证明了推荐里的 preference prediction 和 next-interaction prediction 会让同一个 LLM adapter 学到不同能力：Y 更适合喜欢判断，N 更适合 next-item ranking，M1 是统一折中；这些结论在 hard candidates、MovieLens multi-seed 和 Amazon seed42 下方向稳定，但和 SASRec 的强弱必须按 sample exposure budget 讲。

## 最容易说错

1. N 不是 next-liked-item。
2. Y ranking 不是 N ranking。
3. M1 不是 positive transfer。
4. LLM 没有 universally beat SASRec。
5. sample exposure match 不是 compute/FLOPs match。
6. Amazon 不是 multi-seed。
7. Random-k5 不是主 ranking protocol。
8. cold/tail 不是 cold-start 已解决。
9. candidate order 不是完全无影响，只是相对小。
10. 项目不是新 architecture，核心是 supervision semantics + protocol evidence。
