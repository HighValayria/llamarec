---
title: "20 mock interview"
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
# 20 Mock Interview

使用方式：先不要看 `21_mock_interview_answers.md`。每轮挑 8-10 题口答，录音，回放检查是否踩 red flags。

## Round 1: 基础项目讲解

1. 你用 30 秒讲一下这个项目。
2. 这个项目和普通 LLM recommender demo 最大区别是什么？
3. Y-K0、N-K0、M1 分别是什么？
4. 为什么你认为 preference prediction 和 next-item prediction 不一样？
5. 你如何用一个简单用户序列解释 Y 和 N 的差别？
6. 这个项目用的是什么 base model 和 fine-tuning 方法？
7. 你最终最稳的 conclusion 是什么？
8. 这个项目有没有提出新 architecture？
9. 你最想让面试官记住哪三个点？
10. 如果只允许你说一个数字，你会说哪个，为什么？

## Round 2: 推荐系统深挖

1. N-K0 为什么不是 next-liked-item prediction？
2. 负候选在这个项目里是什么意思？
3. 为什么 random negatives 可能太容易？
4. PopMatch 怎么构造？
5. Popularity baseline 在 Random-k5 和 PopMatch 下说明了什么？
6. BPR-MF 起什么作用？
7. SASRec 和 LLM 在输入表示上有什么本质区别？
8. 为什么 full-catalog ranking 没做？这会怎样影响 claim？
9. k20/k50 结果说明什么？
10. candidate order perturbation 说明什么？
11. cold/tail 分析的目的是什么？
12. 为什么不能说 LLM 已经证明擅长 cold-start？

## Round 3: LLM / QLoRA 深挖

1. 为什么选 Llama-3.2-3B-Instruct？
2. QLoRA 是什么？
3. 4-bit quantization 量化的是谁？
4. LoRA r=16 和 alpha=32 怎么解释？
5. all target modules 包括哪些？
6. base model 权重是否更新？
7. 训练结束保存什么？
8. 推理时 adapter 怎么加载？
9. 为什么训练 loss 只算答案 token？
10. `score_yesno()` 为什么比生成字符串更适合评测？
11. `score_candidates()` 怎么得到候选排序？
12. 为什么 k50 label tokenization 要检查？

## Round 4: 实验严谨性挑战

1. 你如何防止 temporal leakage？
2. same timestamp 为什么危险？
3. 为什么 Y 同 timestamp 可以保留，N ambiguous sample 要跳过？
4. 为什么 candidate files 要固定？
5. test threshold 为什么不能在 test 上调？
6. AUC 和 F1 的作用区别是什么？
7. N-K0 比 M1 强，会不会只是因为 M1 训练预算不公平？
8. SASRec step-aligned 为什么不公平？
9. closest-exposure SASRec 是否严格公平？
10. 远多监督的 SASRec 超过当前 N-K0 是否推翻 LLM sample-efficiency claim？
11. MovieLens multi-seed 证明了什么，没证明什么？
12. Amazon seed42 复现意味着什么，不能意味着什么？
13. PopMatch 是否可能引入新 bias？
14. 你有没有做显著性检验？
15. 这个结果可信吗？你会怎么 defend？

## Round 5: 研究能力 / 开放问题

1. 如果让你重新做，你第一优先级补什么？
2. 如何做 strict compute matching？
3. 如何验证 LLM 是否利用预训练电影/商品知识？
4. 如何改进 M1？
5. 如何提升 large candidate ranking？
6. 如果 N-K0 在 Amazon multi-seed 不稳定，你会怎么调整 claim？
7. 如果 high-exposure SASRec 在 Amazon 也远超 N-K0，你会怎么写结论？
8. 为什么当前项目适合写成 empirical study？
9. 你觉得这个项目最大的限制是什么？
10. 你会如何扩展到真实推荐系统？
11. 你会如何加入 retrieval stage？
12. 你会如何比较 TALLRec？
13. 你会如何比较 LLMRank？
14. 你会如何向非推荐背景面试官解释 sample exposure？
15. 你从这个项目学到的研究方法是什么？
