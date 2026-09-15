---
title: "24 one day plan"
type: report
status: current
authority: descriptive
source: agent
created: 2026-08-24
updated: 2026-08-24
last_verified: 2026-08-24
related_code: []
---

# 24 One Day Plan

目标：6-8 小时，把项目从“能讲”推进到“能连续 defend 15 分钟”。

## Block 1: 0:00-1:00 主线和 Y/N/M

看：

```text
26_final_one_page_cheatsheet.md
00_project_map.md
01_core_story.md
02_y_n_m_explained.md
```

输出：

```text
手写一页：问题 -> Y/N -> M -> evaluation -> baseline -> conclusion
```

## Block 2: 1:00-2:00 数据和代码

看：

```text
03_data_and_leakage.md
04_code_walkthrough.md
```

练：

```text
讲 raw dataset 到 metrics 的代码链路
```

检查题：

```text
strict_history 在哪里实现？
N legal target 怎么枚举？
candidate file 为什么固定？
```

## Block 3: 2:00-3:00 LLM 训练与推理

看：

```text
05_llm_qlora_training.md
06_inference_and_metrics.md
18_code_questions.md
```

练：

```text
解释 QLoRA
解释 score_yesno / score_candidates
解释 labels=-100
```

## Block 4: 3:00-4:00 实验和数字

看：

```text
07_experiment_logic.md
08_results_cheatsheet.md
```

输出：

```text
Experiment -> Motivation -> Design -> Result -> Interpretation
每个实验用 2 句话讲
```

## Block 5: 4:00-5:00 PopMatch 和 baseline

看：

```text
09_popmatch_and_robustness.md
10_sasrec_and_sample_efficiency.md
```

练：

```text
回答：PopMatch 是不是 hard-negative training？
回答：SASRec high exposure 超过当前 N-K0是否推翻结论？
```

## Block 6: 5:00-6:00 稳定性和相关工作

看：

```text
11_multiseed_and_crossdataset.md
12_related_methods_comparison.md
```

输出：

```text
TALLRec vs 本项目
LLMRank vs 本项目
SASRec vs LLM adapter
Amazon boundary
```

## Block 7: 6:00-7:00 问答训练

做：

```text
16_question_bank.md 每类挑 2 题
17_hard_questions.md 全部扫一遍
19_flashcards.md 随机抽 20 张
```

## Block 8: 7:00-8:00 mock interview

做：

```text
20_mock_interview.md Round 1-5 各选 5 题
录音
对照 21_mock_interview_answers.md
最后看 25_interview_red_flags.md
```

最终达标：

```text
30 秒、3 分钟、15 分钟三个版本都能讲
能解释所有核心数字的 motivation
能承认限制但不崩盘
```
