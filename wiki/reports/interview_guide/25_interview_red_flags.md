---
title: "25 interview red flags"
type: report
status: current
authority: descriptive
source: agent
created: 2026-08-24
updated: 2026-08-24
last_verified: 2026-08-24
related_code:
  - configs/experiment.yaml
  - src/data/split.py
  - src/data/build_next_item.py
  - src/eval/candidate_sets.py
  - src/train/multitask_dataset.py
  - src/baselines/sasrec.py
---

# 25 Interview Red Flags

这些是面试里最容易一句话翻车的地方。每条都给“不要说”和“要说”。

## 1. N 是 next-liked-item

不要说：

```text
N 预测用户下一个喜欢的 item
```

要说：

```text
N 预测 full sequence 里的下一次真实 interaction，不按 rating 过滤
```

## 2. Y ranking 和 N ranking 是同一个任务

不要说：

```text
Y 的 P(Yes) 排序就是 next-item ranking
```

要说：

```text
Y ranking 是 preference score ranking；N ranking 是 candidate-label next-interaction ranking
```

## 3. M1 是 positive transfer

不要说：

```text
M1 证明多任务正迁移
```

要说：

```text
M1 是 unified tradeoff，保住两种能力，但 ranking 没超过 N-K0
```

## 4. LLM 全面打败 SASRec

不要说：

```text
LLM beats SASRec
```

要说：

```text
closest N-task sample exposure 下 N-K0 更强；远多监督的 SASRec 可超过当前低曝光 N-K0，但双方 high-exposure head-to-head 未做
```

## 5. sample exposure match 等于 compute match

不要说：

```text
我做了公平 compute match
```

要说：

```text
我做的是 N-task sample exposure diagnostic，不是 FLOPs/token/wall-clock/capacity match
```

## 6. Amazon 已经 multi-seed

不要说：

```text
Amazon 多 seed 也稳定
```

要说：

```text
Amazon 是 seed42 directional validation；MovieLens 才有 seeds 42/43/44
```

## 7. Random-k5 是最可靠 ranking protocol

不要说：

```text
Random-k5 是主结论
```

要说：

```text
Random-k5 是 easy-negative reference；PopMatch-k5 是主 hard-candidate evidence
```

## 8. LLM 已经证明擅长 cold-start

不要说：

```text
LLM 擅长 cold-start
```

要说：

```text
cold/tail 只是 diagnostic，coldest bucket 只有 26 samples，不能做强结论
```

## 9. candidate order 完全没有影响

不要说：

```text
candidate order 没影响
```

要说：

```text
candidate order 有影响但较小；candidate-size expansion 是更强 stressor
```

## 10. 本项目提出新 architecture

不要说：

```text
我提出了新的推荐模型架构
```

要说：

```text
我做的是 LLM recommendation supervision semantics 和 evaluation protocol 的系统经验研究
```

## 11. PopMatch 是 hard-negative training

不要说：

```text
我用 PopMatch hard negatives 训练了模型
```

要说：

```text
PopMatch 是 hard-candidate evaluation；训练模型没变，只换 fixed candidate files
```

## 12. negative candidate 表示用户不喜欢

不要说：

```text
negative candidates 是用户不喜欢的 item
```

要说：

```text
negative candidates 只是本样本中不是真实 next item 的候选，不等价于 dislike
```

## 13. 同 timestamp 可以按 movie_id 当真实顺序

不要说：

```text
同 timestamp 用 movie_id 排序后就有顺序了
```

要说：

```text
movie_id 只是稳定 tie-breaker，不表示真实时间顺序；N ambiguous bucket 会跳过
```

## 14. Y-K0 ranking 弱说明 Y-K0 没用

不要说：

```text
Y-K0 不行
```

要说：

```text
Y-K0 binary preference 强，但 P(Yes) 不适合直接替代 next-item ranking
```

## 15. 高 exposure SASRec 超过当前 N-K0推翻项目

不要说：

```text
SASRec 超过当前 N-K0说明前面都错了
```

要说：

```text
这正是项目的 budget-sensitive conclusion：不同预算 regime 下赢家不同
```

## 16. Amazon N-K0 over M1 是大优势

不要说：

```text
Amazon 上 N-K0 明显大幅超过 M1
```

要说：

```text
Amazon 上方向复现但 margin 小，HR@1 +0.0087
```

## 17. AUC/F1 可以随便混用

不要说：

```text
AUC 和 F1 都差不多
```

要说：

```text
AUC 不依赖 threshold，F1 依赖 threshold；test 上不能调 threshold
```

## 18. LLM sample efficiency 来自预训练知识是事实

不要说：

```text
结果证明 LLM 靠预训练知识赢
```

要说：

```text
这是一种 hypothesis；当前没有 text ablation 或 ID-only ablation 直接验证
```

## 19. PopMatch 完全解决公平性

不要说：

```text
PopMatch 后评测完全公平
```

要说：

```text
PopMatch 控制 popularity shortcut，但不是 full-catalog ranking，也不是所有难度都覆盖
```

## 20. 代码里所有结果都可以从 wiki 背

不要说：

```text
我主要根据文档理解代码
```

要说：

```text
我能从 preprocess/split/builders/train/eval 代码链路解释这些结果是怎么来的
```

## 关键边界修正

[FACT] 当前没有做 `N-K0(≈1.53M exposure) vs SASRec(≈1.53M exposure)`。已完成的比较是：`N-K0(≈12k)` 明显高于 `SASRec closest(≈11.8k)`；同时 `SASRec high(≈1.53M)` 可以超过当前 `N-K0(≈12k)`。

[INTERPRETATION] 因此项目支持的是 N-K0 的 N-task sample efficiency，以及 SASRec 在获得大量额外 sequential supervision 后仍有增长空间；它不支持“双方 high-exposure 对齐后 SASRec 一定更强”。
