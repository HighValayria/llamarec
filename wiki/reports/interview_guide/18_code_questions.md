---
title: "18 code questions"
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
# 18 Code Questions

这些问题按真实 repo 文件和函数组织。面试官如果指着代码问，先回答“它在 pipeline 的位置”，再回答“为什么这样写”。

## 1. `build_user_sequences()` 为什么按 `(timestamp, movie_id)` 排序？

file:
`src/data/preprocess.py`

function:
`build_user_sequences()`

answer:
[FACT] timestamp 是真实顺序，`movie_id` 只作为同 timestamp 时的稳定 tie-breaker。它不表示同 timestamp 内有真实先后顺序。后续 split 仍然把同 timestamp 当 bucket 处理，避免把稳定排序误当因果顺序。

## 2. 为什么 Amazon `parent_asin` 被映射成 `movie_id`？

file:
`src/data/preprocess.py`

function:
`_iter_amazon_reviews_2023_ratings()`

answer:
[FACT] 代码把 `parent_asin` 保留为 `parent_asin`，同时赋给内部 `movie_id`。这样可以复用既有 MovieLens split、candidate、training、inference、SASRec 代码，不需要把所有模块改成 generic item_id。

## 3. 为什么 `positive_sequences` 不参与 N target？

file:
`src/data/preprocess.py`

function:
`build_user_sequences()`

answer:
[FACT] 文件注释明确说 MVP 主数据来源是 full_sequence，positive_sequence 只是辅助统计产物。N 的 ground truth 是下一次真实交互，不是下一次 positive item。

## 4. strict split 的核心函数在哪里？

file:
`src/data/split.py`

function:
`build_full_sequence_leave_two_out_split()`

answer:
[FACT] 这个函数为 Y 和 N 构造各自的 timestamp-bucket split，并返回 `strict_history_rule: history_timestamp_lt_target_timestamp`。Y 用最后两个 timestamp buckets 做 validation/test；N 用最后两个 legal next-item samples。

## 5. 为什么 N 只跳过 ambiguous sample，不跳过 user？

file:
`src/data/split.py`

function:
`_legal_next_item_targets()`

answer:
[FACT] `_legal_next_item_targets()` 对每个 timestamp bucket 检查 size。第一个 bucket 跳过；如果后续 bucket size 不是 1，就只增加 ambiguous count 并 continue。其他 singleton buckets 仍然产生合法 N samples。

## 6. `validate_split_no_leakage()` 检查什么？

file:
`src/data/split.py`

function:
`validate_split_no_leakage()`

answer:
[FACT] 它检查 split 来源是 full_sequence，确认 Y/N validation/test target 与预期 bucket/sample 对齐，并调用 `_assert_history_before_target()` 保证 history 最大 timestamp 小于 target timestamp，target 不在自身 history 中。

## 7. Y label 在哪里构造？

file:
`src/data/build_preference.py`

function:
`_make_preference_sample()`

answer:
[FACT] `label = "Yes" if target["rating"] >= threshold else "No"`。threshold 来自 config 的 positive rating threshold，当前是 4。

## 8. 为什么 Y 的 history 用 timestamp 而不是 list index？

file:
`src/data/build_preference.py`

function:
`_strict_history_before_target()`

answer:
[FACT] 它先取 `target_timestamp`，再过滤 `item["timestamp"] < target_timestamp`。这样同 timestamp 的 item 不会因为排序 index 靠前而进入 history。

## 9. N target 为什么不看 rating？

file:
`src/data/build_next_item.py`

function:
`build_next_item_samples()`

answer:
[FACT] 函数从 `legal_targets` 里取 target index，不检查 `target["rating"]`。这实现了 full-sequence next interaction，而不是 next positive item。

## 10. N candidate 的 label 怎么对应？

file:
`src/data/build_next_item.py`

function:
`build_next_item_samples()`

answer:
[FACT] 构造 `candidate_movie_ids` 后找到 `ground_truth_index`，再设置 `label = label_set[ground_truth_index]`。也就是说答案 A/B/C/D/E 完全由 ground truth 在当前 shuffled candidate list 的位置决定。

## 11. negative sampling 为什么只排除 ground truth？

file:
`src/data/negative_sampling.py`

function:
`sample_random_negatives_from_all_movies()`

answer:
[FACT] excluded 默认只有当前 target item。注释明确说 N 的负候选只表示“不是本样本真实 next item”，不要按用户正反馈过滤，也不要解释成不喜欢。

## 12. PopMatch 的核心代码是什么？

file:
`src/eval/candidate_sets.py`

function:
`sample_popularity_matched_negatives()`

answer:
[FACT] 它计算 target popularity，然后按 `abs(movie_pop - target_pop)` 对 negative pool 排序，在最接近的 hard pool 中随机采样 n 个 negatives。

## 13. candidate record 如何保证和 ground truth 一致？

file:
`src/eval/candidate_sets.py`

function:
`validate_candidate_record()`

answer:
[FACT] 它检查 candidate 不重复、ground truth 出现一次、`ground_truth_index` 等于 candidates 中 ground truth 的位置、`label` 等于 label_set 对应位置，并检查 history timestamp 小于 target timestamp。

## 14. Y prompt 为什么不会泄漏 target rating？

file:
`src/inference/prompts.py`

function:
`render_yesno_prompt()`, `assert_no_target_rating_in_yesno_prompt()`

answer:
[FACT] prompt 的 history 可以 include ratings，但 target section 只写 title，不写 target rating。assert 函数检查 target section 中没有 target rating 字符串。

## 15. N prompt 为什么不包含 candidate rating？

file:
`src/inference/prompts.py`

function:
`render_candidate_prompt()`, `assert_no_candidate_rating_in_candidate_prompt()`

answer:
[FACT] candidate prompt 只列候选 title 和 label，assert 检查 candidate section 不包含 `rating:`。N 要预测 next interaction，不把 candidate rating 作为泄漏特征。

## 16. 训练时为什么只监督答案 token？

file:
`src/train/preference_dataset.py`

function:
`encode_preference_record()`

answer:
[FACT] labels 先全部设为 `IGNORE_INDEX = -100`，然后只把 prefix 之后的 answer token 位置设为真实 token id。这样 causal LM loss 只作用在 Yes/No 答案上。

## 17. N 训练答案为什么是 A/B/C 而不是 item title？

file:
`src/train/next_item_dataset.py`

function:
`encode_next_item_record()`

answer:
[FACT] 函数要求 `record["label"]` 属于 `label_set`，并把 label 作为答案 token。这样训练和推理都可以直接比较 candidate label logits，避免生成长 item title 的不稳定性。

## 18. M1 的 1:1 interleaving 在哪里实现？

file:
`src/train/multitask_dataset.py`

function:
`MultitaskTrainingDataset.__init__()`

answer:
[FACT] 它先用 `count_ratio_examples()` 计算 cycle count，然后每个 cycle 放 `task_ratio_y` 个 Y example 和 `task_ratio_n` 个 N example。默认 M1 是 1:1。

## 19. 为什么 M 训练用 SequentialSampler？

file:
`src/train/train_m.py`

function:
`_build_sequential_trainer()`

answer:
[FACT] 内部 `SequentialTrainer` 覆盖 `_get_train_sampler()`，返回 `SequentialSampler`。这保留 `MultitaskTrainingDataset` 已经构造好的 Y/N ratio order，避免 Trainer 随机打乱破坏任务交错计划。

## 20. QLoRA 在哪里配置？

file:
`src/train/train_y.py`

function:
`_load_tokenizer_and_model()`

answer:
[FACT] 代码用 `BitsAndBytesConfig(load_in_4bit, bnb_4bit_quant_type, bnb_4bit_compute_dtype, bnb_4bit_use_double_quant=True)` 4-bit 加载 base model，再 `prepare_model_for_kbit_training()`，最后用 `LoraConfig` 和 `get_peft_model()` 插入 LoRA。

## 21. seed 在哪里设置？

file:
`src/train/train_y.py`

function:
`_set_training_seed()`

answer:
[FACT] 它设置 Python `random`、NumPy、Torch、CUDA 和 Transformers seed。`run_y_training/run_n_training/run_m_training` 都在加载模型前调用它。

## 22. adapter 保存在哪里？

file:
`src/train/train_y.py`, `src/train/train_n.py`, `src/train/train_m.py`

function:
`run_y_training()`, `run_n_training()`, `run_m_training()`

answer:
[FACT] 三个训练入口都调用 `trainer.save_model(str(output_dir / "adapter"))`，并保存 tokenizer 到同一 adapter 目录。

## 23. Y 的 P(Yes) 推理在哪里？

file:
`src/inference/scoring.py`

function:
`RealModelScorer.score_yesno()`

answer:
[FACT] 它调用 `_answer_log_scores(prompt, ["Yes", "No"])`，softmax 后得到 `p_yes/p_no` 和 predicted label。

## 24. N 的 candidate logits 推理在哪里？

file:
`src/inference/scoring.py`

function:
`RealModelScorer.score_candidates()`

answer:
[FACT] 它对 label set 计算 log scores，softmax 成 `label_probabilities`，再取概率最大的 label 作为 predicted label。

## 25. single-token logits 路径在哪里？

file:
`src/inference/scoring.py`

function:
`_answer_log_scores()`, `_single_token_log_scores_batch()`

answer:
[FACT] 如果所有答案 token ids 长度都是 1，就走下一 token logits；否则退回 `_sequence_log_likelihood()`。这就是为什么 k50 label 需要 tokenization check。

## 26. Y adapter 如何用来做 N candidate ranking？

file:
`src/inference/evaluate_y_adapter.py`

function:
`_predict_n_records_by_preference()`

answer:
[FACT] 它对每条 N candidate record 的每个 candidate 构造一个 Y-style sample，分别算 `P(Yes)`，再把 `candidate_p_yes` 作为 ranking scores。

## 27. N/M adapter 如何聚合 ranking metric？

file:
`src/inference/evaluate_n_adapter.py`

function:
`predict_candidate_label_records()`

answer:
[FACT] 它渲染 N prompt，调用 `_score_candidates_batch()`，把每个 label 的概率按 label_set 顺序转成 `scores`，metric record 包含 `scores` 和 `ground_truth_index`。

## 28. M adapter 为什么能同时评估 Y 和 N？

file:
`src/inference/evaluate_m_adapter.py`

function:
`run_m_adapter_evaluation()`

answer:
[FACT] 同一个 scorer 被用于 `_predict_y_samples()` 和 `predict_candidate_label_records()`，分别输出 `m_y_*_predictions.jsonl` 和 `m_n_*_predictions.jsonl`。

## 29. AUC 怎么实现？

file:
`src/eval/binary_metrics.py`

function:
`auc()`

answer:
[FACT] 它按 score 排序，处理 ties 平均排名，用 rank-sum 公式计算 AUC。若正负类缺失则返回 None。

## 30. HR/NDCG/MRR 怎么实现？

file:
`src/eval/ranking_metrics.py`

function:
`ranking_metrics_for_rank()`

answer:
[FACT] HR@1 是 rank <= 1；MRR 是 `1/rank`；NDCG@k 是 rank <= k 时 `1/log2(rank+1)`，否则 0。

