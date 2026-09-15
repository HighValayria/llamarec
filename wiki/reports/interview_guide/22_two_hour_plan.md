---
title: "22 two hour plan"
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
# 22 Two Hour Plan

目标：2 小时内能讲项目，不从头读代码。

## 0-10 分钟：先恢复全局图

看：

- `26_final_one_page_cheatsheet.md`
- `00_project_map.md`

必须能回答：

1. 项目一句话是什么？
2. Y/N/M 分别是什么？
3. 为什么 PopMatch、SASRec、multi-seed、Amazon 都在主线里？

## 10-30 分钟：吃透 Y/N/M

看：

- `02_y_n_m_explained.md`

练习：

用 A(5), B(2), C(4), D(1), E(5) 说出：

- Y 样本怎么构造。
- N transition 为什么包含 B 和 D。
- M1 1:1 是什么，不是什么。

检查题：

1. 为什么 N 不是 next-liked-item？
2. Y 的 `P(Yes)` 为什么能排序但不等于 N ranking？
3. M1 为什么不是 positive transfer？

## 30-45 分钟：记最小数字

看：

- `08_results_cheatsheet.md`

只背 6 个：

1. Y-K0 binary F1 `0.7831`
2. M1 binary F1 `0.7818`
3. MovieLens PopMatch N-K0 HR@1 `0.5447`
4. MovieLens PopMatch M1 HR@1 `0.5244`
5. SASRec exp-match/high HR@1 `0.2700 / 0.6243`
6. Amazon PopMatch N-K0/M1 HR@1 `0.4669 / 0.4582`

检查题：

这些数字分别证明什么？哪些不能过度解释？

## 45-70 分钟：代码链路

看：

- `04_code_walkthrough.md`

只讲主干：

```text
preprocess -> split -> build_preference/build_next_item
-> candidate_sets -> train_y/train_n/train_m
-> scoring/evaluate_* -> metrics
```

检查题：

1. strict temporal split 在哪个文件？
2. Y label 在哪里构造？
3. N legal target 在哪里决定？
4. candidate file 为什么固定？
5. adapter 推理在哪里加载？

## 70-90 分钟：PopMatch + SASRec exposure

重看：

- `00_project_map.md`
- `08_results_cheatsheet.md`

必须能说：

- Random-k5 为什么容易。
- PopMatch 怎么控制 popularity shortcut。
- SASRec step-aligned 为什么不公平。
- sample exposure 和 compute/FLOPs 为什么不是一回事。
- high exposure SASRec 超过当前 N-K0如何不破坏 N-K0 sample-efficiency claim。

## 90-105 分钟：练 3 分钟稿

看：

- `14_interview_3min.md`

做法：

1. 第一次照着读。
2. 第二次只看小标题说。
3. 第三次计时，控制在 3-4 分钟。

必须包含：

- motivation
- Y/N/M
- leakage
- PopMatch
- SASRec exposure
- multi-seed/Amazon boundary

## 105-120 分钟：练 15 分钟开场和 red flags

看：

- `15_interview_15min.md`
- `26_final_one_page_cheatsheet.md`

最后 5 分钟只检查这些不要说错：

1. 不要说 N 是 next liked item。
2. 不要说 Y ranking 和 N ranking 是同一个任务。
3. 不要说 M1 positive transfer。
4. 不要说 LLM universally beats SASRec。
5. 不要说 sample exposure match 等于 compute match。
6. 不要说 Amazon 已经 multi-seed。
7. 不要说 Random-k5 是主 ranking protocol。
8. 不要说项目证明 LLM 擅长 cold-start。
9. 不要说 candidate order 完全没有影响。
10. 不要说项目提出了新 architecture。

## 两小时结束时的最低标准

你应该能做到：

- 30 秒讲清项目。
- 3 分钟讲出完整研究逻辑。
- 用例子解释 Y/N/M。
- 从数据到 metrics 讲代码链路。
- 被问 SASRec fairness 时不慌。
- 主动说出 Amazon 和 cold/tail 的边界。
