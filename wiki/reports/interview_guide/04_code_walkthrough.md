---
title: "04 code walkthrough"
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
# 04 Code Walkthrough

这份导读按 pipeline 讲，不按文件名堆叠。每一步都先说明“它在项目里干什么”，再给代码证据。

## Pipeline

```text
raw dataset
  |
  v
preprocessing
  |
  v
strict temporal split
  |
  +--> Y builder
  |
  +--> N builder
          |
          v
     candidate files
          |
          v
train Y / train N / train M
          |
          v
adapter checkpoint
          |
          v
inference
          |
          v
metrics
```

## 1. Raw Dataset

文件：

- `configs/experiment.yaml`
- `src/data/preprocess.py`

输入：

- MovieLens ratings + movie metadata。
- Amazon Musical Instruments interaction CSV + parquet metadata。

输出：

- 标准化后的 interaction records，内部字段复用 `movie_id/title/rating/timestamp`。

核心逻辑：

- `raw_files` 配置不同数据集的 raw path 和格式。
- Amazon 的 `parent_asin` 被映射到内部 `movie_id`，便于复用 MovieLens pipeline。
- Amazon 只读 `user_id/parent_asin/rating/timestamp/title`，不读 review text 或 description。
- `build_user_sequences()` 按 `(timestamp, movie_id)` 稳定排序，并加 `sequence_index`。

## 2. Preprocessing

文件：

- `src/data/preprocess.py`
- `src/data/build_step2.py`

函数：

- `load_ratings()`
- `load_movies()`
- `build_user_sequences()`
- `run_step2()`

输入：

- 标准化 ratings。

输出：

- `data/processed/{dataset}/full_sequences.jsonl`
- `data/processed/{dataset}/positive_sequences.jsonl`

核心逻辑：

- `full_sequences` 保留所有 interaction，不按 rating 过滤。
- `positive_sequences` 只是辅助统计，不决定 N history 或 target。
- `run_step2()` 是本地 CPU 数据处理入口，不加载 LLM。

## 3. Strict Temporal Split

文件：

- `src/data/split.py`

函数：

- `build_full_sequence_leave_two_out_split()`
- `validate_split_no_leakage()`
- `build_legal_next_item_targets_for_user()`

输入：

- `full_sequences`

输出：

- `data/processed/{dataset}/split.json`

核心逻辑：

- 全局规则：`history_timestamp_lt_target_timestamp`。
- Y split：最后一个 timestamp bucket 做 test，倒数第二个做 validation，更早 bucket 做 train。
- N split：枚举合法 singleton next-item target，最后两个合法样本分别做 validation/test。
- 同 timestamp 不删除整个 user；Y 共享严格历史，N 只跳过 ambiguous next bucket。
- `validate_split_no_leakage()` 检查 history 最大 timestamp 必须小于 target timestamp，target 不能出现在自己的 history 中。

## 4. Y Builder

文件：

- `src/data/build_preference.py`

函数：

- `build_preference_samples()`
- `_make_preference_sample()`
- `_strict_history_before_target()`

输入：

- `full_sequences`
- `split`
- `positive_rating_threshold`

输出：

- `preference_train.jsonl`
- `preference_valid.jsonl`
- `preference_test.jsonl`

核心逻辑：

- target 的 `rating >= 4` 标为 `Yes`，否则 `No`。
- history 是 target 之前、timestamp 严格更小的最近 10 条。
- Y train 只用 validation bucket 之前的 targets。
- Y validation/test 可以包含同 timestamp bucket 的多个 targets，它们共享同一段严格历史。

## 5. N Builder

文件：

- `src/data/build_next_item.py`

函数：

- `build_next_item_samples()`
- `validate_next_item_sample()`
- `_build_candidate_ids()`

输入：

- `full_sequences`
- `split["n"]`
- item universe

输出：

- `next_item_train.jsonl`
- `next_item_valid.jsonl`
- `next_item_test.jsonl`

核心逻辑：

- `build_legal_next_item_targets_for_user()` 先枚举合法 N target。
- 第一 timestamp bucket 没有 history，不产生 N 样本。
- 如果 target bucket size 不等于 1，跳过该 N sample。
- target rating 不参与 N target 选择。
- 每条 N 样本包含 `candidate_movie_ids`、`ground_truth_index` 和 label set。

## 6. Candidate Files

文件：

- `src/eval/candidate_sets.py`
- `src/data/negative_sampling.py`

函数：

- `build_fixed_candidate_sets()`
- `_build_candidate_records()`
- `sample_popularity_matched_negatives()`
- `sample_random_negatives_from_all_movies()`

输入：

- N validation/test samples。

输出：

- `data/candidates/{dataset}/valid.jsonl`
- `data/candidates/{dataset}/test.jsonl`
- variants such as `data/candidates/{dataset}/variants/k5_popmatch_seed42/test.jsonl`

核心逻辑：

- candidate files 只为评测固定生成一次，Base/Y/N/M 都读同一份。
- random negative 只排除当前 ground truth，不把 negative 解释成“不喜欢”。
- PopMatch 先按 target popularity 距离排序，在最接近的一小段 hard pool 中随机采样。
- candidate label 用 A/B/C/D/E；k20/k50 会自动生成 spreadsheet labels。

## 7. Prompts

文件：

- `src/inference/prompts.py`

函数：

- `render_yesno_prompt()`
- `render_candidate_prompt()`

Y prompt：

- history 包含 rating。
- target section 不包含 target rating。
- 答案限定 `Yes/No`。

N prompt：

- history 不包含 rating。
- candidates 不包含 candidate rating。
- 答案限定 candidate labels。

[FACT] Y prompt 是 preference 问题；N prompt 是 next interaction 选择题。不要把两个 prompt 的答案语义混成一个。

## 8. Train Y

文件：

- `configs/y.yaml`
- `src/train/train_y.py`
- `src/train/preference_dataset.py`

入口：

```text
python -m src.train.train_y
```

输入：

- `preference_train.jsonl`
- `preference_valid.jsonl`

输出：

- `outputs/y/{dataset}/{run}/adapter`
- `metrics.json`
- `run_summary.json`

核心逻辑：

- `PreferenceTrainingDataset` 只在答案 token 上计算 loss，其余 prompt token label 为 `-100`。
- `_load_tokenizer_and_model()` 加载 Llama-3.2-3B-Instruct，4-bit NF4 quantization，再套 LoRA。
- `trainer.save_model(output_dir / "adapter")` 保存 adapter，不保存完整 base model。
- seed 在模型初始化前设置 Python/NumPy/Torch/CUDA/Transformers。

## 9. Train N

文件：

- `configs/n.yaml`
- `src/train/train_n.py`
- `src/train/next_item_dataset.py`

入口：

```text
python -m src.train.train_n
```

输入：

- `next_item_train.jsonl`
- `next_item_valid.jsonl`

输出：

- N adapter。

核心逻辑：

- `NextItemTrainingDataset` 使用 `render_candidate_prompt()`。
- 答案是 `record["label"]`，必须属于 `label_set`。
- loss 只落在 A/B/C/... 答案 token 上。

## 10. Train M

文件：

- `configs/m.yaml`
- `src/train/train_m.py`
- `src/train/multitask_dataset.py`

入口：

```text
python -m src.train.train_m
```

输入：

- Y train/valid records。
- N train/valid records。

输出：

- 一个 M adapter。

核心逻辑：

- `MultitaskTrainingDataset` 按 `task_ratio_y/task_ratio_n` 顺序交错编码。
- M1 默认 1:1。
- `count_ratio_examples()` 决定实际 Y/N 样本数；当前正式解释中 M1 是 N exposure 12000、total exposure 24000。
- evaluation 时同一个 adapter 分别走 M-Y 和 M-N 接口。

## 11. QLoRA Training Config

文件：

- `configs/experiment.yaml`
- `src/train/train_y.py`

当前 repo 配置：

- base model: `meta-llama/Llama-3.2-3B-Instruct`
- max sequence length: `2048`
- method: QLoRA
- `load_in_4bit: true`
- quant type: `nf4`
- LoRA `r=16`
- LoRA `alpha=32`
- LoRA dropout `0.05`
- target modules: `q_proj/k_proj/v_proj/o_proj/gate_proj/up_proj/down_proj`
- gradient checkpointing: enabled
- BF16 when supported

CLI defaults:

- per-device train batch size: `1`
- gradient accumulation: `8`
- learning rate: `2e-4`
- smoke max samples: `1000`

Formal result reports:

- N-K0 anchor: optimizer steps `1500`, effective batch `8`, N-task exposure `12000`。
- M1: optimizer steps `3000`, effective batch `8`, N-task exposure `12000`, total exposure `24000`。

## 12. Adapter Checkpoint

文件：

- `src/train/train_y.py`
- `src/train/train_n.py`
- `src/train/train_m.py`
- `src/inference/scoring.py`

训练结束保存：

- PEFT adapter weights。
- tokenizer files。

推理加载：

- `AdapterModelScorer` 先以 4-bit 加载 base model。
- 再 `PeftModel.from_pretrained(base_model, adapter_dir)` 加载 adapter。

[FACT] base model 权重不是全参数更新对象；训练的是 LoRA adapter 参数。

## 13. Inference

文件：

- `src/inference/scoring.py`
- `src/inference/evaluate_y_adapter.py`
- `src/inference/evaluate_n_adapter.py`
- `src/inference/evaluate_m_adapter.py`

Y scoring：

- `score_yesno(prompt)`
- 取 Yes/No logits。
- softmax 得 `P(Yes)`。

N scoring：

- `score_candidates(prompt, label_set)`
- 取 A/B/C/... logits。
- softmax 得 candidate label probabilities。

Y-as-ranking：

- `evaluate_y_adapter.py` 对每个 candidate 单独算 `P(Yes)`。
- 这不是 N candidate-label objective。

M scoring：

- M-Y 用 `score_yesno()`。
- M-N 复用 N 的 `predict_candidate_label_records()`。

## 14. Metrics

文件：

- `src/eval/binary_metrics.py`
- `src/eval/ranking_metrics.py`

Binary:

- AUC: rank-sum on continuous score。
- F1/Accuracy: 默认 threshold 0.5；报告中也有 validation-calibrated F1。

Ranking:

- `ground_truth_rank()` 按 score 降序排序，tie 用 index 稳定打破。
- HR@1: ground truth 排第一就是 1。
- NDCG@5: ground truth 在 top 5 内按 `1/log2(rank+1)` 衰减。
- MRR: `1/rank`。

## 代码追问最容易问的 8 个点

1. 为什么 `_strict_history_before_target()` 用 timestamp 而不是 index？
2. 为什么 N 的低 rating target 仍然合法？
3. 为什么 candidate negative 只排除 ground truth？
4. PopMatch popularity 从哪里来，以及这个 protocol 的 claim boundary 是什么？
5. 为什么 `PreferenceTrainingDataset` label mask 只监督答案 token？
6. 为什么 single-token label 很重要？
7. 为什么 M1 用 interleaving 而不是 sequential fine-tuning？
8. 为什么 optimizer steps 不能直接等于 sample exposure？

