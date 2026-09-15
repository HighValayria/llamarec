---
title: "17 hard questions"
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
# 17 Hard Questions

这些回答的原则：不回避缺陷，先承认边界，再 defend 当前设计为什么仍然有价值。

## 1. 你说 Y 和 N 是不同能力，会不会只是评价指标不同？

简短回答：
不只是指标不同，训练目标、prompt、label 语义和推理分数都不同。

Defend：
[FACT] Y 训练 `Yes/No`，分数是 `P(Yes | history, item)`；N 训练候选 label，分数是 `P(label | history, candidate set)`。同样在 ranking metric 下，Y-K0 PopMatch HR@1 `0.1854`，N-K0 `0.5447`。所以差异不只是 binary vs ranking metric，而是监督语义本身。

## 2. N-K0 比 M1 强，是不是 M1 的预算还是不公平？

简短回答：
当前 N exposure 是对齐的，M1 的 N-task exposure 和 N-K0 都是 12000，但 M1 还有额外 Y exposure。

Defend：
[FACT] M1 optimizer steps 3000、total exposure 24000、N exposure 12000；N-K0 optimizer steps 1500、N exposure 12000。比较 N ranking 时，M1 不是 N 上训练更少，而是共享 adapter 同时承担 Y/N。

## 3. 为什么不直接 multi-label learning？

简短回答：
因为当前研究问题是比较推荐监督语义，不是先设计最复杂的统一目标。

Defend：
[INTERPRETATION] Multi-label 可能混合 preference 和 next-interaction 的 label semantics，让解释更难。Y/N/M 的好处是最小化变量：Y 是二分类偏好，N 是候选下一项，M 是两者混合。

## 4. PopMatch 是人为设计的，会不会对 LLM 有利？

简短回答：
它是人为 stress test，但不是只对 LLM 有利；SASRec 在远多 exposure 下也能超过当前 N-K0。

Defend：
[FACT] PopMatch 主要降低 popularity gap。MovieLens SASRec s3000 HR@1 `0.6243` 高于当前 N-K0 `0.5466`，但 exposure 约 `1.53M` 对 `12k`。这说明 PopMatch 并没有系统性偏向 LLM；它只是减少 Random-k5 的 popularity shortcut。

## 5. 为什么只采 4 个 negatives？

简短回答：
canonical k5 是主线起点，但项目也做了 k20/k50 candidate-size stress。

Defend：
[FACT] k5 方便和早期 LLMRank/TALLRec-style candidate evaluation 对齐；Phase 2A 扩展到 k20/k50，发现 candidate size 是强 stressor。当前材料不会把 k5 当成 full-catalog ranking。

## 6. 为什么不 full ranking？

简短回答：
Full-catalog ranking 成本和实现复杂度更高，当前阶段先用 fixed candidate ranking 做可控语义比较。

Defend：
[INTERPRETATION] 项目目标是监督语义，而不是部署级 retrieval。Fixed candidates 让 Base/Y/N/M/SASRec 在同一候选上比较。Full ranking 是重要 future work，尤其用于检验 large-candidate robustness。

## 7. SASRec exposure match 不是严格公平比较吧？

简短回答：
是的，它只是 N-task sample exposure diagnostic，不是 compute/FLOPs/capacity match。

Defend：
[FACT] 报告明确写不是 strict compute matching。它的价值是指出 optimizer-step alignment 明显不公平，并提供更合理的一个预算轴。

## 8. LLM 参数量比 SASRec 大很多，sample efficiency 有意义吗？

简短回答：
有意义，但不能替代 compute/capacity fairness。

Defend：
[INTERPRETATION] sample efficiency 回答“看同样 N-task 样本时谁更强”，不回答“同样 FLOPs 谁更强”。所以我会说 N-K0 has sample-exposure advantage，而不说它 compute-efficient。

## 9. LLM 是否只是记住电影知识？

简短回答：
不能排除，但当前实验没有直接证明这个机制。

Defend：
[HYPOTHESIS] 预训练知识或 title semantics 可能有帮助。需要 ID-only title ablation、shuffled title 或 unseen item diagnostic 才能验证。当前结论只依赖 observed metrics，不把机制说成事实。

## 10. Amazon 上 N-M 只差 0.0087，还能算复现吗？

简短回答：
可以算方向复现，但不能说大 margin 或稳定复现。

Defend：
[FACT] Amazon PopMatch N-K0 HR@1 `0.4669`，M1 `0.4582`，margin `0.0087`。报告边界就是 directional cross-dataset replication, seed42 only。

## 11. 为什么没有 Amazon multi-seed？

简短回答：
当前阶段范围是 compact cross-dataset validation，Amazon multi-seed 是 future robustness。

Defend：
[FACT] 当前材料明确不允许说 Amazon multi-seed。MovieLens 已有 seeds 42/43/44；Amazon 只用于第二数据集方向验证。

## 12. 为什么没有显著性检验？

简短回答：
当前有 multi-seed stability，但不是正式显著性检验。

Defend：
[INTERPRETATION] 三 seed 能降低偶然性，但统计显著性需要更多 seeds 或 paired tests。论文级下一步应补 bootstrap 或 paired randomization。

## 13. 为什么不比较 GRU4Rec / BERT4Rec？

简短回答：
可以补，但 SASRec 已经是强 sequence baseline，足以暴露关键 budget issue。

Defend：
[INTERPRETATION] 项目重点不是穷尽所有 baseline，而是把 LLM supervision semantics 和 budget-sensitive SASRec positioning 讲清楚。更多 baseline 会增强完整性，但不是当前结论成立的前提。

## 14. 为什么不做严格 FLOPs match？

简短回答：
因为当前证据不足以恢复 LLM token count、wall-clock、GPU 等完整 compute 账。

Defend：
[FACT] fair-budget report 明确 LLM wall-clock、GPU、token count 等不可恢复，不应推断。诚实做法是承认没做 strict FLOPs matching。

## 15. 为什么不直接用 embedding similarity？

简短回答：
embedding similarity 是另一类模型，不回答 Y/N 监督语义在 LLM 中造成什么能力差异。

Defend：
[INTERPRETATION] 可以作为 future baseline，但它不会替代当前对 LLM prompt + adapter training 的研究问题。

## 16. Y prompt 里 history 带 rating，会不会泄漏？

简短回答：
不会泄漏 target rating；history rating 是过去已发生交互信息。

Defend：
[FACT] `assert_no_target_rating_in_yesno_prompt()` 检查 target section 没有 target rating。History 中的 past rating 是用户历史偏好信号，符合 `timestamp < target`。

## 17. N prompt 不带 history rating，会不会不公平？

简短回答：
这是当前 N 任务定义的一部分，目的是预测 next interaction 而非喜欢程度。

Defend：
[INTERPRETATION] N 的目标是 next interaction，避免让 candidate selection 混入 rating preference signal。可以做 ablation 加 history rating，但当前 Y/N 差异已经在明确定义下成立。

## 18. PopMatch popularity 是从 full sequence 统计，会不会泄漏 test popularity？

简短回答：
这是一个需要谨慎表述的 protocol 边界。

Defend：
[FACT] 当前代码 `_load_movie_popularity()` 从 full sequences 统计 popularity。材料中把 PopMatch 定位为 hard-candidate diagnostic，而不是线上无泄漏 candidate generator。若做部署级或更严格论文版本，应改成 train-only popularity。

## 19. 为什么 M1 没有超过 N-K0，还说 multi-task 有价值？

简短回答：
因为它用一个 adapter 同时保住 binary 和 ranking，虽然 ranking 不是最强。

Defend：
[FACT] M1 binary 接近 Y-K0，ranking 接近 N-K0 但低于 N-K0。这对需要单一模型服务两种接口的场景有价值，但不能说它替代 specialist。

## 20. 这个项目是不是只是 prompt engineering？

简短回答：
不是，核心是监督数据构造、adapter tuning、fixed candidate evaluation 和 baseline diagnostics。

Defend：
[FACT] 项目训练 Y/N/M adapters，构造 strict temporal split、fixed candidates、PopMatch、SASRec exposure curves 和 multi-seed。Prompt 是接口层，不是全部贡献。
