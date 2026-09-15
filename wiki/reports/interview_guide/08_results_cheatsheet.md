---
title: "08 results cheatsheet"
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
# 08 Results Cheatsheet

目标：最多记 12 个数字。面试时先说方向，再说数字；不要把所有小数背到 10 位。

## 最小 12 个数字

1. MovieLens Y-K0 binary F1: `0.7831`

[FACT] Phase 2B validation-calibrated binary test F1。证明 Y-style preference tuning 对 Yes/No preference 有效。

2. MovieLens M1 binary F1: `0.7818`

[FACT] M1 几乎追上 Y-K0 binary。证明 multi-task adapter 保住了偏好能力。

3. MovieLens canonical Random-k5 N-K0 HR@1: `0.7189`

[FACT] canonical easy-negative ranking 下 N-K0 很强。注意它不是主 hard-candidate claim。

4. MovieLens canonical Random-k5 M1 HR@1: `0.6950`

[FACT] M1 ranking 低于 N-K0，gap 约 `0.0240`。

5. MovieLens PopMatch-k5 Y-K0 ranking HR@1: `0.1854`

[FACT] 用 `P(Yes)` 排 next-item candidate 很弱。证明 Y ranking 不等于 N ranking。

6. MovieLens PopMatch-k5 N-K0 HR@1: `0.5447`

[FACT] hard-candidate primary protocol 下最强 LLM ranking row。

7. MovieLens PopMatch-k5 M1 HR@1: `0.5244`

[FACT] M1 接近但低于 N-K0。支持 unified tradeoff。

8. MovieLens k50 N-K0 vs M1 HR@1: `0.1995` vs `0.1219`

[FACT] candidate size stress 下 N-K0-M1 差距变大，gap `0.0775`。

9. MovieLens SASRec closest exposure HR@1: `0.2700`

[FACT] SASRec 粗略 N-task exposure matched row 低于 N-K0。

10. MovieLens SASRec high exposure HR@1: `0.6243`

[FACT] SASRec s3000 高于当前低曝光 N-K0，但这是 much-higher-exposure anchor，不是双方 high-exposure 对齐。

11. MovieLens multi-seed N-K0 over M1 min HR@1 margin: `0.0104`

[FACT] seeds 42/43/44 上 N-K0 都高于 M1。

12. Amazon PopMatch-k5 N-K0/M1/SASRec-exp HR@1: `0.4669 / 0.4582 / 0.1757`

[FACT] Amazon seed42 方向复现：N-K0 略高于 M1，明显高于 closest-exposure SASRec。边界：Amazon 不是 multi-seed。

## 只剩 5 分钟时记 6 个数字

1. Y-K0 binary F1: `0.7831`
2. M1 binary F1: `0.7818`
3. PopMatch N-K0 HR@1: `0.5447`
4. PopMatch M1 HR@1: `0.5244`
5. SASRec exp-match vs high exposure HR@1: `0.2700` vs `0.6243`
6. Amazon PopMatch N-K0 vs M1 HR@1: `0.4669` vs `0.4582`

## 最重要的方向句

[FACT] Y-K0 binary strong, but Y-K0 `P(Yes)` ranking weak.

[FACT] N-K0 is the strongest LLM next-item ranking model.

[FACT] M1 is useful and unified, but does not beat N-K0 ranking.

[FACT] PopMatch makes ranking harder and more trustworthy than Random-k5.

[FACT] SASRec conclusion: N-K0 is higher at closest exposure; much-higher-exposure SASRec is higher than the current N-K0 checkpoint; the full budget-performance frontier is unmeasured.

[FACT] MovieLens has multi-seed stability; Amazon is seed42 directional validation only.

## 不要误读这些数字

- 不要把 Random-k5 的 `0.7189` 当最终 ranking claim；主 hard-candidate 数字是 PopMatch `0.5447`。
- 不要说 M1 positive transfer；它没有超过 Y-K0 binary 或 N-K0 ranking。
- 不要说 LLM universally beats SASRec；远多监督的 SASRec 超过当前 N-K0。
- 不要说 Amazon 复现了大 margin；N-K0 over M1 只有 `0.0087` HR@1。
- 不要说 Y-K0 ranking 失败代表 Y-K0 无用；它在 binary preference 上强。

## 数据集规模数字

MovieLens-1M:

- [FACT] PopMatch test samples: `5675`。

Amazon Musical Instruments:

- [FACT] users `57,439`
- [FACT] items `24,584`
- [FACT] interactions `511,792`
- [FACT] Y train/valid/test: `396,908 / 57,442 / 57,442`
- [FACT] N train/valid/test: `339,449 / 57,439 / 57,439`
- [FACT] PopMatch test samples: `57,439`

## Budget 数字

N-K0:

- [FACT] optimizer steps `1500`
- [FACT] effective batch `8`
- [FACT] N-task exposure `12000`

M1:

- [FACT] optimizer steps `3000`
- [FACT] effective batch `8`
- [FACT] N-task exposure `12000`
- [FACT] total exposure `24000`

SASRec closest:

- [FACT] optimizer steps `23`
- [FACT] effective batch `512`
- [FACT] N-task exposure `11776`

SASRec high:

- [FACT] optimizer steps `3000`
- [FACT] effective batch `512`
- [FACT] N-task exposure `1534656`

## 关键边界修正

[FACT] 当前没有做 `N-K0(≈1.53M exposure) vs SASRec(≈1.53M exposure)`。已完成的比较是：`N-K0(≈12k)` 明显高于 `SASRec closest(≈11.8k)`；同时 `SASRec high(≈1.53M)` 可以超过当前 `N-K0(≈12k)`。

[INTERPRETATION] 因此项目支持的是 N-K0 的 N-task sample efficiency，以及 SASRec 在获得大量额外 sequential supervision 后仍有增长空间；它不支持“双方 high-exposure 对齐后 SASRec 一定更强”。
