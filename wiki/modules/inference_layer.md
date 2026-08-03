---
title: 推理层
type: module
status: current
authority: descriptive
source: mixed
created: 2026-07-30
updated: 2026-08-01
last_verified: 2026-08-01
related_code:
  - src/inference/base_zero_shot.py
  - src/inference/evaluate_y_adapter.py
  - src/inference/evaluate_n_adapter.py
  - src/inference/evaluate_m_adapter.py
  - src/inference/prompts.py
  - src/inference/scoring.py
  - src/inference/tokenization_check.py
  - src/inference/prediction_io.py
  - src/inference/README.md
  - tests/test_base_zero_shot_local.py
  - tests/test_y_adapter_evaluation.py
  - tests/test_n_m_adapter_evaluation.py
  - wiki/guides/step4_base_zero_shot_guide.md
---

# 推理层

## 当前范围

推理层当前覆盖 STEP 4：Base LLM zero-shot 的本地 dry-run 与云端真实概率推理入口；同时覆盖 STEP 5/6/7：Y-K0、N-K0 与 M-K0 adapter 的独立评测入口。

本地不加载 `meta-llama/Llama-3.2-3B-Instruct`，也不进行训练。真实模型概率计算通过 `--mode real` 在云服务器执行。

## 输入

Y 使用 STEP 2 产物：

```text
data/processed/{dataset}/preference_valid.jsonl
data/processed/{dataset}/preference_test.jsonl
```

MovieLens-32M 本地评测包使用 gzip：

```text
data/processed/movielens-32m/preference_valid.jsonl.gz
data/processed/movielens-32m/preference_test.jsonl.gz
```

N 使用 STEP 3 固定候选集：

```text
data/candidates/{dataset}/valid.jsonl
data/candidates/{dataset}/test.jsonl
```

STEP 4 不重新切分数据，也不重新采样候选集。

## 核心接口

`render_yesno_prompt()` 将 Y 样本渲染为：

```text
History + Target -> Yes / No
```

Y history 可以包含历史 rating；target rating 不得出现在 prompt 中。

`render_candidate_prompt()` 将 N 候选集渲染为：

```text
History + Candidate Set -> 实际发生的下一个 Item
```

N prompt 不包含候选 rating。N 的语义仍是 next interaction prediction，不是喜欢程度排序。

`MockScorer` 在本地返回确定性的伪概率，用于验证 prediction schema、metrics 调用和输出路径。

`RealModelScorer` 在 `--mode real` 下加载 tokenizer 与 base model，并返回连续概率：

```text
Y: P(Yes), P(No)
N: P(A), P(B), P(C), P(D), P(E)
```

如果待比较答案均为单 token，则读取 prompt 后下一 token logits；如果存在多 token 答案，则使用完整答案 sequence likelihood。

`base_zero_shot.py` 支持 `--batch-size` / `--batch_size`。在 real 模式下，单 token 答案会按 batch 计算最后一个有效 prompt token 位置的 logits；prediction 文件按 batch 增量写出，并显示 Y/N 进度条。

`evaluate_y_adapter.py` 加载 base model + Y-K0 PEFT adapter，并进行两类评测：

```text
Y binary:
History + Target -> P(Yes), P(No)

N candidate ranking by Y:
History + Candidate_i -> P(Yes)
scores = [P(Yes for candidate A), ..., P(Yes for candidate E)]
```

因此 Y adapter 的 ranking 分数来自 `P(Yes)`，不是 `P(A)...P(E)`。该入口仍读取 STEP 3 固定候选集，不重新采样候选。

`evaluate_n_adapter.py` 加载 base model + N-K0 PEFT adapter，并只评测 N 的候选 next-item ranking：

```text
History + Candidate Set -> P(A), P(B), P(C), P(D), P(E)
```

N adapter 的分数直接来自 candidate label probability，不引入候选之间的完整排序监督，也不重新采样候选。

`evaluate_m_adapter.py` 加载 base model + M-K0 PEFT adapter，并分别评测两个推理接口：

```text
M-Y:
History + Target -> P(Yes), P(No)

M-N:
History + Candidate Set -> P(A), P(B), P(C), P(D), P(E)
```

M 的两个接口必须分别报告，不把其中一个接口的结果当作 M 的唯一结果。

## 输出

默认输出目录：

```text
outputs/base/{dataset}/
```

主要产物：

```text
config_snapshot.yaml
tokenization_report.json
y_valid_predictions.jsonl
y_test_predictions.jsonl
n_valid_predictions.jsonl
n_test_predictions.jsonl
valid_metrics.json
test_metrics.json
run_summary.json
```

mock 模式下的 metrics 只代表本地流程可运行，不代表真实模型效果。

Y adapter 默认输出到 adapter 所在 run 目录，主要产物为：

```text
evaluation_config_snapshot.yaml
evaluation_tokenization_report.json
y_valid_predictions.jsonl
y_test_predictions.jsonl
n_valid_predictions.jsonl
n_test_predictions.jsonl
valid_metrics.json
test_metrics.json
evaluation_summary.json
```

N adapter 默认输出到 adapter 所在 run 目录，主要产物为：

```text
evaluation_config_snapshot.yaml
evaluation_tokenization_report.json
n_valid_predictions.jsonl
n_test_predictions.jsonl
valid_metrics.json
test_metrics.json
evaluation_summary.json
```

M adapter 默认输出到 adapter 所在 run 目录，主要产物为：

```text
evaluation_config_snapshot.yaml
evaluation_tokenization_report.json
m_y_valid_predictions.jsonl
m_y_test_predictions.jsonl
m_n_valid_predictions.jsonl
m_n_test_predictions.jsonl
valid_metrics.json
test_metrics.json
evaluation_summary.json
```

## 当前限制

- `--mode real` 需要云服务器已安装 `torch`、`transformers`、`accelerate`，且当前账号有模型访问权限。
- `--batch-size` 过大可能触发显存不足；云端应先从 8 或 16 开始试，再根据 4090 显存占用调整。
- `tokenization_report.json` 在 mock 模式只记录待检查答案集合；在 real 模式会写入真实 token id。
- 当前已在 MovieLens-100K 和 MovieLens-32M eval-only 产物上完成 mock dry-run。
- MovieLens-32M Base validation/test 全量评测已在云端完成，但尚未汇总进最终 `outputs/results.csv`。
- Y/N/M adapter 评测入口已完成本地 mock 测试；真实 adapter 评测需要云端传入 `--mode real --adapter-dir ...`。
