---
title: "16 question bank"
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
# 16 Question Bank

每题都按“简短回答 + 深入回答”准备。简短回答用于面试现场先稳住，深入回答用于被继续追问时展开。

## A. 项目动机

### A1. 你这个项目到底解决什么问题？

简短回答：
它研究 LLM 推荐微调中 preference prediction 和 next-interaction prediction 是否是同一种能力。

深入回答：
[FACT] 项目把推荐任务拆成 Y-K0、N-K0 和 M1。Y-K0 学 `P(Like | History, Item)`，N-K0 学 `P(Next Interaction | History, Candidate Set)`，M1 混合两者。结果显示 Y-K0 binary 强但 next-item ranking 弱，N-K0 ranking 强，说明两种监督语义不同。

### A2. 为什么不直接做一个推荐模型，而要拆 Y/N？

简短回答：
因为“喜欢”和“下一次交互”不是同一个标签语义，混在一起会让结论不清楚。

深入回答：
[INTERPRETATION] 如果一个模型判断用户喜欢某个 item，并不意味着它能预测用户下一步会交互哪个 item。喜欢可能有多个候选都高，next interaction 只能有一个真实目标。拆开后才能解释模型到底学到 preference judgment 还是 sequential behavior prediction。

### A3. 这个项目的研究贡献是什么？

简短回答：
贡献是 supervision semantics、multi-task tradeoff 和 sample-exposure-aware baseline positioning。

深入回答：
[FACT] 项目没有提出新 architecture，而是用 Llama-3.2-3B + QLoRA 在严格时间协议下比较 Y/N/M，并用 PopMatch、k20/k50、SASRec、multi-seed、Amazon 验证边界。[INTERPRETATION] 贡献是把 LLM recommender 的任务语义和评测公平性讲清楚。

### A4. 为什么这个问题适合用 LLM 做？

简短回答：
LLM 可以用自然语言 item title 和 history prompt 接推荐任务，但是否真正学到推荐语义需要实验验证。

深入回答：
[FACT] 当前实现使用 item title 构造 prompt，Llama 输出 Yes/No 或候选 label。[HYPOTHESIS] LLM 可能利用预训练语义知识提升 sample efficiency，但项目没有做 text ablation，所以不能把机制说死。

## B. 数据构造

### B1. 原始数据是什么？

简短回答：
MovieLens-1M 是主数据集，Amazon Musical Instruments 是第二数据集。

深入回答：
[FACT] MovieLens 使用 user/movie/rating/timestamp 和 title metadata。Amazon 使用 interaction `user_id/parent_asin/rating/timestamp` 与 metadata `parent_asin/title`，不使用 review text、description、brand、price、images 或外部知识。

### B2. full_sequence 和 positive_sequence 有什么区别？

简短回答：
full_sequence 是主序列，positive_sequence 只是辅助统计。

深入回答：
[FACT] `src/data/preprocess.py` 保留所有 interaction 为 full_sequence；rating >= threshold 的子集写成 positive_sequence。当前 MVP split、Y/N history 和 N target 都来自 full_sequence，不由 positive_sequence 决定。

### B3. history length 是多少？

简短回答：
默认取最近 10 条严格历史。

深入回答：
[FACT] `configs/experiment.yaml` 的 `dataset.history_length` 是 10。Y/N builder 的 `_strict_history_before_target()` 都会先过滤 `timestamp < target_timestamp`，再取最后 10 条。

### B4. Amazon Books 为什么不能用，后来为什么换 Amazon Musical Instruments？

简短回答：
最初 Amazon Books 文件是 catalog metadata，不是 user-item interaction logs。

深入回答：
[FACT] Cross-dataset report 记录 Amazon Books catalog 被拒绝，因为没有足够的用户交互序列。后续改用用户提供的 Amazon Reviews 2023 5-core Musical Instruments，它有 user/item/rating/timestamp interaction。

## C. 时间切分 / Leakage

### C1. 最核心防泄漏规则是什么？

简短回答：
history 必须满足 `timestamp < target_timestamp`。

深入回答：
[FACT] `src/data/split.py` 和 Y/N builders 都用严格小于。这样 target 自己、同 timestamp item、未来 item 都不会进入 prompt。

### C2. 为什么不能用 `timestamp <= target_timestamp`？

简短回答：
因为同 timestamp 内没有真实先后顺序，用 `<=` 会把 target 或同桶未来信息放进 history。

深入回答：
[INTERPRETATION] 很多评分数据只记录秒级或批量时间，同 timestamp 的多条交互无法排序。如果把它们当作已知历史，就等于让模型看到 target bucket 的信息。

### C3. same timestamp 怎么处理？

简短回答：
Y 共享严格历史，N 跳过 ambiguous next-item sample。

深入回答：
[FACT] split policy 是 `skip_entire_user_on_tie: false`。Y 同 timestamp bucket 可以有多个 target；N 只有当 next bucket 是 singleton 才构造样本，否则跳过该 N 样本。

### C4. 为什么 candidate files 要固定？

简短回答：
为了 Base/Y/N/M 在同一候选集合上比较，避免评测时重新负采样造成不可比。

深入回答：
[FACT] `src/eval/candidate_sets.py` 生成 validation/test jsonl，后续评测入口通过 candidate override 读取同一文件。[INTERPRETATION] 如果每个模型用不同 negatives，ranking metric 可能反映候选难度而不是模型能力。

## D. LLM / LoRA / QLoRA

### D1. 为什么选 Llama-3.2-3B-Instruct？

简短回答：
3B 能在单卡 24GB 预算下系统跑 Y/N/M、baseline 和多 seed。

深入回答：
[FACT] repo config 使用 `meta-llama/Llama-3.2-3B-Instruct`，runtime profile 是 single RTX 4090 24GB。[INTERPRETATION] 项目目标是系统比较监督语义，不是只做一次最大模型演示。

### D2. QLoRA 是什么？

简短回答：
把 base model 4-bit 量化加载，只训练 LoRA adapter。

深入回答：
[FACT] 配置 `load_in_4bit: true`、`quant_type: nf4`，训练代码用 `BitsAndBytesConfig` 加载 base model，再 `prepare_model_for_kbit_training()` 和 `get_peft_model()`。

### D3. LoRA r=16、alpha=32、dropout=0.05 是什么意思？

简短回答：
r 是低秩维度，alpha 是缩放系数，dropout 是 adapter 训练正则。

深入回答：
[FACT] `configs/experiment.yaml` 设置 r 16、alpha 32、dropout 0.05，target modules 包括 attention projection 和 MLP projection。[INTERPRETATION] 这是参数效率和训练稳定性的折中，没有做 LoRA sweep。

### D4. 训练结束保存的是什么？

简短回答：
保存 PEFT adapter 和 tokenizer，不保存完整全参数 base model。

深入回答：
[FACT] `train_y.py/train_n.py/train_m.py` 都调用 `trainer.save_model(output_dir / "adapter")` 和 `tokenizer.save_pretrained(...)`。推理时先加载 base model，再 `PeftModel.from_pretrained(base_model, adapter_dir)`。

## E. Y/N/M

### E1. Y-K0 学什么？

简短回答：
学用户是否喜欢 target item。

深入回答：
[FACT] Y prompt 包含 history 和 target title，答案是 Yes/No。label 由 target rating 是否 >=4 得到。概率语义是 `P(Like | History, Item)`。

### E2. N-K0 学什么？

简短回答：
学真实下一次 interaction 在候选集合中的 label。

深入回答：
[FACT] N 的 ground truth 是 full_sequence 下一次真实交互，不按 rating 过滤。模型输出候选标签 A/B/C/D/E。

### E3. M1 是什么？

简短回答：
一个 adapter 混合 Y 和 N 训练，能走两个推理接口。

深入回答：
[FACT] `MultitaskTrainingDataset` 按 Y/N ratio interleaving。M1 默认 1:1。评测时 M-Y 用 Yes/No logits，M-N 用 candidate label logits。

### E4. 为什么 M1 是 tradeoff 而不是 positive transfer？

简短回答：
因为 M1 保住两种能力，但没有超过对应 specialist。

深入回答：
[FACT] MovieLens PopMatch N-K0 HR@1 `0.5447`，M1 `0.5244`；multi-seed 下 N-K0 始终高于 M1。Binary 上 M1 接近 Y-K0，但不是明确超过。

## F. Ranking Inference

### F1. 为什么不用生成字符串做评测？

简短回答：
因为 AUC/ranking 需要连续分数，生成字符串太粗。

深入回答：
[FACT] `score_yesno()` 和 `score_candidates()` 直接取答案 token logits 并 softmax。连续概率能做 AUC、排序和 margin 分析。

### F2. Y ranking 怎么做？

简短回答：
对每个候选单独问 Y prompt，用 `P(Yes)` 排序。

深入回答：
[FACT] `evaluate_y_adapter.py` 的 `candidate_sort_by_p_yes` 对 N candidate record 里的每个 candidate 构造 target preference sample，再收集 `candidate_p_yes`。

### F3. N ranking 怎么做？

简短回答：
同一个 prompt 里列出候选，取 A/B/C/D/E 的 label probability 排序。

深入回答：
[FACT] `evaluate_n_adapter.py` 调用 `predict_candidate_label_records()`，输出 `label_probabilities` 和与候选顺序对齐的 `scores`。

### F4. k50 为什么需要 tokenizer check？

简短回答：
因为候选 label A 到 AX 最好都是 single token，才能用下一 token logits 直接比较。

深入回答：
[FACT] 项目有 `tokenization_check.py`，Phase 2A 报告确认 k50 labels A through AX 对配置 tokenizer 是 single-token，因此能继续走 single-token candidate-label logits path。

## G. Metrics

### G1. AUC 为什么重要？

简短回答：
AUC 不依赖 threshold，适合评价连续 `P(Yes)` 排序质量。

深入回答：
[FACT] `binary_metrics.py` 用 rank-sum AUC。它回答正样本是否整体比负样本分数高，不需要在 test 上选阈值。

### G2. 为什么不能在 test 上调 threshold？

简短回答：
因为 test 只能用于最终评估，在 test 上调 threshold 会泄漏 test label。

深入回答：
[INTERPRETATION] validation-calibrated F1 的意义是阈值从 validation 决定，再应用到 test。这样 F1 不会把 test 当调参集。

### G3. HR@1、NDCG@5、MRR 分别看什么？

简短回答：
HR@1 看第一名是否命中，NDCG@5 看 top5 内位置折扣，MRR 看真实 item 的倒数排名。

深入回答：
[FACT] `ranking_metrics.py` 中 MRR 是 `1/rank`，NDCG@k 是 top-k 内 `1/log2(rank+1)`，HR@1 是 rank <= 1。

### G4. Amazon accuracy 为什么容易误导？

简短回答：
因为 Amazon Y label 很偏，Yes 占比高。

深入回答：
[FACT] Cross-dataset report 记录 Amazon Y labels：Yes `437,418`，No `74,374`。高 positive rate 下只看 Accuracy 容易高估模型，所以 binary 需要 AUC/F1 和校准边界。

## H. PopMatch

### H1. 为什么 Random-k5 太容易？

简短回答：
random negatives 可能远比 target 冷，模型靠 popularity 就能做对。

深入回答：
[FACT] MovieLens canonical random candidate target-negative popularity gap 约 `663.6`，PopMatch test gap 降到 `44.0`。这说明 random protocol 存在明显 popularity shortcut。

### H2. PopMatch 怎么做？

简短回答：
按 target popularity 找 popularity 接近的 negative pool，再随机采样。

深入回答：
[FACT] `sample_popularity_matched_negatives()` 根据 `abs(negative_pop - target_pop)` 排序，从前 `n * candidate_pool_multiplier` 的 hard pool 采样。

### H3. PopMatch 为什么更适合作主 ranking claim？

简短回答：
它减少 target 和 negative 的 popularity 差距，更难靠 popularity shortcut。

深入回答：
[INTERPRETATION] next-item ranking claim 应该尽量评价模型区分行为相关候选的能力，而不是区分热门和冷门 item 的能力。PopMatch 更接近这个目的。

### H4. PopMatch 会不会偏向 LLM？

简短回答：
不能排除 protocol 偏好某类模型，但它至少削弱了 random negative 的 popularity shortcut。

深入回答：
[FACT] PopMatch 下 N-K0 和 M1 仍高于 Popularity/BPR-MF；远多监督的 SASRec checkpoint 也能高于当前 N-K0。[INTERPRETATION] 这说明 PopMatch 不是单方面给 LLM 放水，而是更难的 same-candidate setting。

## I. SASRec / Baseline

### I1. SASRec 是什么？

简短回答：
SASRec 是基于 self-attention 的序列推荐模型，用 item ID 序列预测下一项。

深入回答：
[INTERPRETATION] 它不像 LLM 用自然语言 title prompt，而是学习 item embedding 和序列 attention。它是强 specialized sequential baseline。

### I2. Popularity baseline 解决什么问题？

简短回答：
检查模型是不是只靠热门 item 排序。

深入回答：
[FACT] Random-k5 下 popularity 很强，PopMatch 下明显下降。这个对照证明 random candidate 容易受 popularity shortcut 影响。

### I3. BPR-MF 解决什么问题？

简短回答：
检查矩阵分解协同过滤能否解释 LLM ranking。

深入回答：
[FACT] BPR-MF Random-k5 HR@1 `0.5611`，PopMatch HR@1 `0.3352`。它比 Popularity 更强但仍不能解释 N-K0/M1 的 PopMatch 表现。

### I4. 为什么 SASRec 比较最难讲？

简短回答：
因为它强，但 step-aligned 不等于 exposure-aligned。

深入回答：
[FACT] SASRec s1500 exposure `767424`，N-K0 exposure `12000`。Closest exposure 下 SASRec HR@1 `0.2700`，SASRec s3000 HR@1 `0.6243` 且 exposure 约 `1.53M`。所以结论必须按 sample exposure 讲，不能说双方 high-exposure 对齐过。

## J. Sample Efficiency

### J1. training step 和 sample exposure 有什么区别？

简短回答：
step 是优化器更新次数，sample exposure 是模型实际看过多少训练样本。

深入回答：
[FACT] N-K0 1500 steps effective batch 8，所以 exposure 12000；SASRec 1500 steps batch 512，所以 exposure 767424。

### J2. 为什么不能说 SASRec 1500 steps 和 N-K0 1500 steps 公平？

简短回答：
因为 batch size 差 64 倍，SASRec 看过的样本多得多。

深入回答：
[FACT] Fair-budget report 计算 SASRec s1500 是 N-K0 N-task exposure 的 `63.952x`。

### J3. closest-exposure SASRec 怎么构造？

简短回答：
用 batch 512 找接近 N-K0 12000 exposure 的 step 数，所以是 23 steps、11776 exposure。

深入回答：
[FACT] 表格记录 SASRec exp-match optimizer steps `23`、effective batch `512`、N exposure `11776`，比目标低 `1.8667%`。

### J4. 最准确的 sample efficiency 结论是什么？

简短回答：
N-K0 在 closest exposure 下更强；远多监督的 SASRec 可以超过当前 N-K0。

深入回答：
[INTERPRETATION] 这说明当前证据支持 N-K0 sample efficiency；不能说 LLM 普遍更强，也不能说 SASRec 在双方 high-exposure 对齐后一定更强。

## K. Multi-task

### K1. M1 为什么能同时做二分类和 ranking？

简短回答：
因为同一个 adapter 见过 Y 和 N 两种答案格式，评测时走两个接口。

深入回答：
[FACT] `evaluate_m_adapter.py` 对 Y samples 调 `score_yesno()`，对 N candidate records 复用 N 的 candidate-label prediction。

### K2. M0 为什么表现差？

简短回答：
主要问题包括任务混合和 per-task budget 不公平，后续 M1 改成更公平的 1:1 exposure 解释。

深入回答：
[FACT] 当前材料的安全说法是 M1 是最佳 multi-task diagnostic model，M0 历史表现差不能简单解释成任务本质冲突。[INTERPRETATION] 因为早期设置可能把 task conflict 和 budget mismatch 混在一起。

### K3. M1 为什么不等于训练更多？

简短回答：
M1 的 3000 steps 分给 Y 和 N，N exposure 和 N-K0 anchor 一样是 12000。

深入回答：
[FACT] M1 total exposure 24000，但 N-task exposure 12000。比较 N ranking 时不能说 M1 在 N 上训练了两倍。

### K4. 如果想改进 M1，你会怎么做？

简短回答：
我会尝试 task weighting、curriculum、adapter routing 或 task-specific heads，但要保留相同 temporal/candidate protocol。

深入回答：
[HYPOTHESIS] 当前 M1 tradeoff 可能来自共享 adapter 容量或梯度冲突。可以用 task-balanced sampling、uncertainty weighting、separate LoRA modules、Mixture-of-Adapters 检验，但这些是 future work，不是当前已完成结果。

## L. Multi-seed

### L1. 为什么 seed42 不够？

简短回答：
训练 seed 会影响初始化、数据顺序、dropout 和 CUDA 随机性。

深入回答：
[FACT] 训练入口支持 `--seed`，并在 model init 前设置 Python/NumPy/Torch/CUDA/Transformers seed。multi-seed 是为了确认方向不是偶然。

### L2. candidate seed 和 training seed 为什么要区分？

简短回答：
candidate seed 决定评测候选，training seed 决定模型训练随机性。

深入回答：
[FACT] Multi-seed report 固定 `k5_popmatch_seed42` candidate protocol，只改变训练 seeds 42/43/44。这样比较的是模型训练稳定性，不混入候选集变化。

### L3. Multi-seed 最核心发现是什么？

简短回答：
N-K0 > M1，N-K0 > SASRec exp-match，远多监督的 SASRec checkpoint > 当前 N-K0 都稳定。

深入回答：
[FACT] N-K0 over M1 最小 HR@1 margin `0.0104`；N-K0 over SASRec exp-match 最小 margin `0.2767`；SASRec high s3000 over N-K0 最小 margin `0.0777`。

### L4. 这是不是显著性检验？

简短回答：
不是，只是三 seed 稳定性诊断。

深入回答：
[FACT] 报告明确说这是 stability diagnostic，不是 strict statistical significance，也不是 compute/capacity matched comparison。

## M. Cross-dataset

### M1. 为什么需要 Amazon？

简短回答：
MovieLens-only 外部有效性不足，需要第二数据集看方向是否复现。

深入回答：
[INTERPRETATION] MovieLens 较密集，Amazon 更稀疏。若 Y/N 语义边界和 sample-exposure方向在 Amazon 也成立，项目结论更可信。

### M2. Amazon 的正式规模是多少？

简短回答：
57,439 users、24,584 items、511,792 interactions。

深入回答：
[FACT] Y split 是 396,908 / 57,442 / 57,442，N split 是 339,449 / 57,439 / 57,439。PopMatch validation/test 各 57,439 records。

### M3. Amazon 主结果是什么？

简短回答：
PopMatch 下 N-K0 略高于 M1，明显高于 SASRec exp-match。

深入回答：
[FACT] Amazon PopMatch HR@1：N-K0 `0.4669`，M1 `0.4582`，SASRec exp-match `0.1757`。N-K0 over M1 margin 只有 `0.0087`，所以要说 narrow directional replication。

### M4. Amazon 的边界是什么？

简短回答：
只有 seed42，不能说 Amazon multi-seed 或泛化到所有 Amazon 类目。

深入回答：
[FACT] Cross-dataset report 明确 disallowed claims 包括 Amazon multi-seed stability、large N-K0 over M1 advantage、generalization to all Amazon categories。

## N. Limitations

### N1. 最大限制是什么？

简短回答：
不是严格 compute/FLOPs/capacity matched。

深入回答：
[FACT] sample-efficiency report 明确不等于 strict compute matching、capacity matching、wall-clock matching 或 token-exposure matching。

### N2. 有没有证明 LLM 擅长 cold-start？

简短回答：
没有，只做了 cold/tail diagnostic。

深入回答：
[FACT] coldest bucket `<=10` 只有 26 samples。N-K0 在该 bucket 强，但样本太小，不能上升为 cold-start 结论。

### N3. 有没有证明 LLM 利用预训练知识？

简短回答：
没有，这是合理假设但未直接验证。

深入回答：
[HYPOTHESIS] LLM 可能利用 title semantics 或预训练知识，但没有 text ablation、ID-only prompt 或 shuffled-title experiment，因此不能当事实。

### N4. 为什么没有更多 baseline？

简短回答：
当前已覆盖 Popularity、BPR-MF、SASRec，更多 baseline 是后续扩展。

深入回答：
[INTERPRETATION] SASRec 已经是强 sequence baseline，足够暴露 budget-sensitive conclusion。GRU4Rec/BERT4Rec 等可以补，但不会改变当前 Y/N supervision semantics 的核心实验设计。

## O. 下一步优化

### O1. 如果重新做，你最想补什么？

简短回答：
补 strict compute/token exposure matching、Amazon multi-seed 和 text ablation。

深入回答：
[INTERPRETATION] 这三项分别解决 baseline fairness、cross-dataset stability 和 LLM mechanism 证据不足。

### O2. 如何改进 N-K0 的 large candidate robustness？

简短回答：
用 harder negatives、larger candidate training、retrieval reranking 或 candidate calibration。

深入回答：
[HYPOTHESIS] k20/k50 下性能下降说明训练/eval candidate size mismatch 和 label竞争更难。可用 hard-negative training 或 multi-stage retrieval + rerank。

### O3. 如何改进 M1？

简短回答：
尝试 task weighting、separate adapters 或 routing。

深入回答：
[HYPOTHESIS] 当前 tradeoff 可能来自共享 adapter 容量或任务梯度冲突。可比较 shared LoRA、task-specific LoRA、adapter fusion、动态 sampling。

### O4. 如何让实验更论文级？

简短回答：
补显著性、compute accounting、更多数据集和更明确的 ablation。

深入回答：
[INTERPRETATION] 当前证据已经支撑 supervision semantics 和 budget-sensitive claims；要提升说服力，需要更强统计和机制层证据。

## 关键边界修正

[FACT] 当前没有做 `N-K0(≈1.53M exposure) vs SASRec(≈1.53M exposure)`。已完成的比较是：`N-K0(≈12k)` 明显高于 `SASRec closest(≈11.8k)`；同时 `SASRec high(≈1.53M)` 可以超过当前 `N-K0(≈12k)`。

[INTERPRETATION] 因此项目支持的是 N-K0 的 N-task sample efficiency，以及 SASRec 在获得大量额外 sequential supervision 后仍有增长空间；它不支持“双方 high-exposure 对齐后 SASRec 一定更强”。
