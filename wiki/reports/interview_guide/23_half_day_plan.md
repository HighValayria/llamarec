---
title: "23 half day plan"
type: report
status: current
authority: descriptive
source: agent
created: 2026-08-24
updated: 2026-08-24
last_verified: 2026-08-24
related_code: []
---

# 23 Half Day Plan

目标：4 小时内达到“能讲故事、能讲实验、能 defend 关键质疑”。

## 0:00-0:20 全局恢复

看：

```text
26_final_one_page_cheatsheet.md
00_project_map.md
01_core_story.md
```

产出：

```text
自己画一遍项目主线图
说出一句话问题
```

## 0:20-1:00 Y/N/M 深挖

看：

```text
02_y_n_m_explained.md
03_data_and_leakage.md
```

练：

```text
A(5), B(2), C(4), D(1), E(5)
分别讲 Y samples 和 N transitions
```

检查：

```text
N 不是 next-liked-item
same timestamp policy
M1 不是 positive transfer
```

## 1:00-1:40 代码链路

看：

```text
04_code_walkthrough.md
05_llm_qlora_training.md
06_inference_and_metrics.md
```

目标：

```text
从 raw data -> split -> Y/N builders -> train -> adapter -> inference -> metrics
讲一遍，不看文件名也能讲出核心函数位置
```

## 1:40-2:20 实验逻辑

看：

```text
07_experiment_logic.md
08_results_cheatsheet.md
09_popmatch_and_robustness.md
```

必须背：

```text
Y-K0 binary F1 0.7831
N-K0 PopMatch HR@1 0.5447
M1 PopMatch HR@1 0.5244
Y-K0 P(Yes) ranking HR@1 0.1854
```

## 2:20-3:00 Baseline 和预算

看：

```text
10_sasrec_and_sample_efficiency.md
```

练：

```text
用“上课次数 vs 每节课题量 vs 总题量”解释 steps / batch / exposure
```

必须说准：

```text
closest exposure: N-K0 0.5466 vs SASRec 0.2700
high exposure SASRec: 0.6243
```

## 3:00-3:30 稳定性和相关方法

看：

```text
11_multiseed_and_crossdataset.md
12_related_methods_comparison.md
```

检查：

```text
MovieLens multi-seed yes
Amazon seed42 only
TALLRec/LLMRank/SASRec 区别
```

## 3:30-4:00 模拟面试

做：

```text
20_mock_interview.md Round 1 + Round 4
对照 21_mock_interview_answers.md
最后扫 25_interview_red_flags.md
```

最低达标：

```text
3 分钟讲稿不卡
能 defend PopMatch
能 defend SASRec fairness
能主动说 Amazon boundary
```
