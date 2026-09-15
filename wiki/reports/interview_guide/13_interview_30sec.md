---
title: "13 interview 30sec"
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
# 13 Interview 30sec

面试官问：“你这个项目做了什么？”

## 30 秒回答

我做的是一个 LLM 推荐微调项目，但核心不是单纯追求一个最高分，而是研究推荐里的两种监督语义：用户“喜不喜欢一个 item”和“下一次真实会交互哪个 item”是不是同一种能力。

我构造了三个模型接口：Y-K0 做 Yes/No preference prediction，学 `P(Like | history, item)`；N-K0 做 next-item candidate ranking，输出 A/B/C/D/E；M1 把 Y 和 N 1:1 混合到一个 adapter 里。

结果是 Y-K0 最适合二分类偏好，N-K0 最适合 next-item ranking，M1 是统一折中但 ranking 没超过 N-K0。进一步用 PopMatch hard candidates、SASRec sample-exposure comparison、MovieLens multi-seed 和 Amazon seed42 验证后，结论边界是：不同监督确实学到不同能力，baseline 强弱取决于样本曝光预算，不能简单说 LLM 全面超过 SASRec。

## 压缩版

一句话说：我用 Llama-3.2-3B + QLoRA 比较 preference supervision、next-item supervision 和 multi-task supervision，发现喜欢预测和下一次交互预测不是同一种推荐能力；N 更适合 ranking，M 是 tradeoff，和 SASRec 的比较必须按 sample exposure 讲。

