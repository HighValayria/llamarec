---
title: "LlamaRec Interview Guide"
type: report
status: current
authority: descriptive
source: agent
created: 2026-08-23
updated: 2026-08-24
last_verified: 2026-08-24
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
  - src/baselines/sasrec.py
---
# LlamaRec Interview Mastery

本目录是 LlamaRec 项目的面试速成材料。目标不是复写论文，而是让你在很短时间内讲清楚项目：任务定义、数据构造、训练和推理链路、实验结论、baseline 边界、hard-candidate protocol，以及被追问时哪些话能说、哪些话不能说。

以后新增面试材料也放在本目录：`wiki/reports/interview_guide/`。

## 如果只有 30 分钟

1. 先看 `26_final_one_page_cheatsheet.md`：恢复项目全局脑图。
2. 再看 `01_core_story.md`：背住一句话、30 秒、3 分钟版本。
3. 快速扫 `08_results_cheatsheet.md`：只记 6 个最关键数字。
4. 最后看 `13_interview_30sec.md` 和 `14_interview_3min.md`，直接练出口。

## 如果有 2 小时

按这个顺序：

1. `00_project_map.md`
2. `01_core_story.md`
3. `02_y_n_m_explained.md`
4. `03_data_and_leakage.md`
5. `04_code_walkthrough.md`
6. `05_llm_qlora_training.md`
7. `06_inference_and_metrics.md`
8. `08_results_cheatsheet.md`
9. `09_popmatch_and_robustness.md`
10. `10_sasrec_and_sample_efficiency.md`
11. `22_two_hour_plan.md`

重点不是把文件读完，而是能主动回答：Y 和 N 为什么不是同一个推荐能力？M1 为什么是 unified tradeoff 而不是 positive transfer？PopMatch 为什么比 Random-k5 更能检验 ranking？SASRec 为什么必须按 sample exposure 讲？

## 如果有半天

先完成 2 小时路径，然后补：

1. `07_experiment_logic.md`：把实验设计讲成因果链，而不是报表。
2. `11_multiseed_and_crossdataset.md`：把 MovieLens multi-seed 和 Amazon seed42 的证据边界讲清楚。
3. `12_related_methods_comparison.md`：把 LlamaRec 和 SASRec/BPR/PopSeq/KAR/LLM4Rec 类方法区分开。
4. `15_interview_15min.md`：练一遍完整长讲稿。
5. `25_interview_red_flags.md`：把不能说的话提前排雷。

## 如果明天就面试

优先吃透这 10 件事：

1. [FACT] 项目核心问题：偏好预测和 next-interaction prediction 是否让 LLM 学到同一种推荐能力。
2. [FACT] Y-K0 学的是 `P(Like | history, target item)`，标签由 `rating >= 4` 得到。
3. [FACT] N-K0 学的是 `P(next interaction label | history, candidates)`，target 是下一次真实交互，不按 rating 过滤。
4. [FACT] M1 用一个 adapter 混合 Y/N 训练，能做二分类和 ranking，但 ranking 没超过 N-K0。
5. [FACT] 严格历史规则是 `history timestamp < target timestamp`，不能用 `<=`。
6. [FACT] Y 的 `P(Yes)` 可以给候选排序，但数学意义不是 next-item candidate-label ranking。
7. [FACT] PopMatch-k5 是主 ranking claim protocol；Random-k5 太容易暴露 popularity shortcut。
8. [FACT] MovieLens closest exposure 下 N-K0 HR@1 `0.5466`，SASRec exp-match HR@1 `0.2700`；SASRec s3000 在约 `1.53M` exposure 下 HR@1 `0.6243`，高于当前约 `12k` exposure 的 N-K0，但没有做 `N-K0(1.53M) vs SASRec(1.53M)`。
9. [FACT] MovieLens multi-seed 支持主方向；Amazon 只有 seed42，不能说 cross-dataset multi-seed。
10. [INTERPRETATION] 最稳结论是 supervision semantics + budget-sensitive baseline positioning，不是“LLM 全面打败 SASRec”。

## 文件清单

- `00_project_map.md`: 项目主线图和节点解释。
- `01_core_story.md`: 一句话、30 秒、3 分钟项目故事。
- `02_y_n_m_explained.md`: Y-K0 / N-K0 / M1 彻底讲解。
- `03_data_and_leakage.md`: 数据构造、时间切分、history 规则和 leakage 排雷。
- `04_code_walkthrough.md`: 从原始数据到评测的代码链路。
- `05_llm_qlora_training.md`: Llama 3.2 3B、QLoRA、三类 adapter 训练配置。
- `06_inference_and_metrics.md`: 推理打分、binary/ranking 指标、candidate set 协议。
- `07_experiment_logic.md`: RQ、实验矩阵、protocol 与 claim 的对应关系。
- `08_results_cheatsheet.md`: 最小数字集。
- `09_popmatch_and_robustness.md`: PopMatch、hard candidates、k20/k50、candidate order 专题。
- `10_sasrec_and_sample_efficiency.md`: SASRec baseline、sample exposure、fair/high budget 定位。
- `11_multiseed_and_crossdataset.md`: MovieLens multi-seed 与 Amazon seed42 证据边界。
- `12_related_methods_comparison.md`: 与传统推荐、序列推荐、LLM 推荐、KAR/LLM4Rec 类工作的差异。
- `13_interview_30sec.md`: 30 秒讲稿。
- `14_interview_3min.md`: 3 分钟讲稿。
- `15_interview_15min.md`: 10-15 分钟讲稿。
- `16_question_bank.md`: 高频问答库。
- `17_hard_questions.md`: 刁钻问题与防守回答。
- `18_code_questions.md`: 代码层追问。
- `19_flashcards.md`: 快速记忆卡。
- `20_mock_interview.md`: 模拟面试题。
- `21_mock_interview_answers.md`: 模拟面试参考答案。
- `22_two_hour_plan.md`: 2 小时突击安排。
- `23_half_day_plan.md`: 半天突击安排。
- `24_one_day_plan.md`: 一天突击安排。
- `25_interview_red_flags.md`: 面试危险说法、边界话术和自检清单。
- `26_final_one_page_cheatsheet.md`: 面试前 5 分钟脑图。

## 证据来源

本目录内容来自当前代码、配置、冻结实验表格、已授权读取的 wiki 报告，以及本阶段对数据/训练/推理/评测链路的核对。没有启动新的训练、推理或 GPU 实验。所有新增访谈指南文件都应继续放在 `wiki/reports/interview_guide/`。
