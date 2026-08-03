---
title: STEP 4 Base Zero-shot 指南
type: guide
status: current
authority: normative
source: agent
created: 2026-07-30
updated: 2026-08-01
last_verified: 2026-08-01
related_code:
  - configs/experiment.yaml
  - configs/y.yaml
  - configs/n.yaml
  - src/inference/base_zero_shot.py
  - src/inference/prompts.py
  - src/inference/scoring.py
  - src/inference/tokenization_check.py
  - src/inference/prediction_io.py
  - src/inference/README.md
  - tests/test_base_zero_shot_local.py
  - src/eval/binary_metrics.py
  - src/eval/ranking_metrics.py
  - wiki/guides/current_data_flow.md
  - wiki/modules/evaluation_layer.md
---

# STEP 4 Base Zero-shot 指南

## 这一步要做什么

STEP 4 的目标是得到 Base LLM 的零样本基线。

Base 的意思是：

```text
不做 recommendation tuning
不加载 LoRA adapter
不训练
只用原始 instruct LLM 推理
```

当前模型 ID 固定在配置中：

```text
meta-llama/Llama-3.2-3B-Instruct
```

本地开发不需要下载或加载这个模型。真正加载模型的部分通过 `--mode real` 在云服务器执行。

## 这一步为什么重要

后面 Y-K0、N-K0、M-K0 都要回答一个问题：

```text
recommendation tuning 是否比 Base LLM 更好？
```

如果没有 Base 结果，后面所有微调结果都没有参照系。

所以 STEP 4 先跑：

```text
Base-Y
Base-N
```

分别得到：

```text
Base-Y: AUC / F1 / Accuracy
Base-N: HR@1 / HR@5 / NDCG@5 / MRR
```

## 输入文件

STEP 4 只读已经固定好的数据产物。100K 与 32M 按数据集隔离。

Base-Y 二分类评测读：

```text
data/processed/{dataset}/preference_valid.jsonl
data/processed/{dataset}/preference_test.jsonl
```

32M 本地 eval-only 产物为 gzip：

```text
data/processed/movielens-32m/preference_valid.jsonl.gz
data/processed/movielens-32m/preference_test.jsonl.gz
```

Base-N 排序评测读：

```text
data/candidates/{dataset}/valid.jsonl
data/candidates/{dataset}/test.jsonl
```

不要在 STEP 4 重新切数据，也不要重新采候选。

## 输出目录

建议所有 Base 输出都放到：

```text
outputs/base/{dataset}/
```

建议产物：

```text
outputs/base/{dataset}/
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

其中：

```text
config_snapshot.yaml
  记录本次运行使用的配置快照。

tokenization_report.json
  记录 Yes / No / A / B / C / D / E 的 tokenizer 检查结果。

y_*_predictions.jsonl
  保存每条 Y 样本的 P(Yes)、P(No)、预测标签和真实标签。

n_*_predictions.jsonl
  保存每条候选集样本的 P(A)...P(E)、预测候选和 ground truth。

valid_metrics.json / test_metrics.json
  保存最终指标。

run_summary.json
  保存样本数、模型名、运行时间、设备、是否使用真实模型等运行摘要。
```

## 必须实现的两个推理接口

### score_yesno

输入：

```text
一条 Y 样本：
History + Target
```

输出：

```json
{
  "p_yes": 0.61,
  "p_no": 0.39,
  "predicted_label": "Yes"
}
```

这个接口服务于：

```text
Base-Y
Y-K0 binary eval
M-Y binary eval
Y/M 的候选 P(Yes) 排序
```

### score_candidates

输入：

```text
一条固定候选集样本：
History + A/B/C/D/E candidates
```

输出：

```json
{
  "label_probabilities": {
    "A": 0.10,
    "B": 0.18,
    "C": 0.52,
    "D": 0.12,
    "E": 0.08
  },
  "predicted_label": "C"
}
```

这个接口服务于：

```text
Base-N
N-K0 ranking eval
M-N ranking eval
```

## 不能只用 generate

不要只让模型生成一个词，然后把生成结果当作分数。

错误做法：

```text
模型生成 C
所以只记录 predicted_label = C
```

正确做法：

```text
计算 P(A), P(B), P(C), P(D), P(E)
用这些连续分数排序
```

Y 也是一样：

```text
计算 P(Yes), P(No)
```

这些连续概率后面才能用于 AUC、NDCG、MRR 等指标。

## tokenizer 检查

在正式打分前，必须检查这些答案字符串的 tokenization：

```text
Yes
No
A
B
C
D
E
```

如果某个答案是单 token，可以用下一 token logits 直接取这个 token 的概率。

如果某个答案不是单 token，必须用完整答案 sequence likelihood：

```text
log P(answer | prompt)
= answer token 1 的 logprob
+ answer token 2 的 logprob
+ ...
```

然后在候选答案之间做 softmax：

```text
P(Yes) = softmax(log P(Yes), log P(No))
P(A)   = softmax(log P(A), ..., log P(E))
```

不要错误地只读第一个 token 的 logit。

## Prompt 结构

Prompt 要尽量短、稳定、可复用。当前建议使用纯文本任务说明，不在 STEP 4 引入复杂 few-shot。

### Y prompt

用途：

```text
History + Target -> Yes / No
```

建议结构：

```text
Task: Preference Prediction

User history:
1. Movie title (rating: 4)
2. Movie title (rating: 2)
...

Target movie:
Movie title

Question:
Would the user like the target movie?

Answer with exactly one option:
Yes
No

Answer:
```

注意：

```text
Y 的 history 可以包含 rating，因为 Y 是偏好判断。
Target 的 rating 不能出现在 prompt 中，因为它是标签来源。
```

### N prompt

用途：

```text
History + Candidate Set -> 实际发生的下一个 Item
```

建议结构：

```text
Task: Next-item Prediction

User history:
1. Movie title
2. Movie title
...

Candidates:
A. Movie title
B. Movie title
C. Movie title
D. Movie title
E. Movie title

Question:
Which candidate is the user's next interaction?

Answer with exactly one option:
A
B
C
D
E

Answer:
```

注意：

```text
N 的语义是 next interaction，不是最喜欢的电影。
Candidate 的 rating 不能出现在 prompt 中。
```

## 本地 dry-run 当前已经做什么

因为本地不加载 Llama，本地只做这些检查：

```text
1. 能读取 preference_valid/test.jsonl。
2. 能读取 data/candidates/{dataset}/valid/test.jsonl。
3. 能把样本渲染成 prompt。
4. prompt 中没有 target rating 泄漏。
5. mock scorer 能输出合法概率。
6. prediction jsonl 字段完整。
7. binary_metrics.py 能吃 Y prediction。
8. ranking_metrics.py 能吃 N prediction。
```

当前 `MockScorer` 使用确定性伪概率，只用于让输出 schema 和指标调用跑通。

本地 dry-run 的目的不是得到真实结果，而是确保云端跑真实模型时不会因为路径、字段、格式、指标接口出错而浪费 GPU 时间。

## 云端真实运行做什么

云服务器上才做：

```text
1. 下载或加载 meta-llama/Llama-3.2-3B-Instruct。
2. 加载 tokenizer。
3. 检查 Yes/No/A/B/C/D/E 的 tokenization。
4. 对 Y valid/test 计算 P(Yes), P(No)。
5. 对 fixed candidates valid/test 计算 P(A)...P(E)。
6. 写 predictions。
7. 调用指标函数写 metrics。
```

云端运行仍然不训练模型。

当前 `RealModelScorer` 已经接入真实概率推理：

```text
单 token 答案：读取下一 token logits。
多 token 答案：使用完整答案 sequence likelihood。
对候选答案分数做 softmax 后写入 prediction 文件。
```

当前 CLI 支持 `--batch-size`，也兼容 `--batch_size`。real 模式下建议先从 8 或 16 开始，确认显存稳定后再提高。

云端应先跑小样本，再扩大规模：

```bash
python -m src.inference.base_zero_shot --config configs/experiment.yaml --dataset movielens-32m --mode real --splits validation --limit 20 --batch-size 8
python -m src.inference.base_zero_shot --config configs/experiment.yaml --dataset movielens-32m --mode real --splits validation --limit 5000 --batch-size 16
python -m src.inference.base_zero_shot --config configs/experiment.yaml --dataset movielens-32m --mode real --splits validation test --batch-size 16
```

只有前两条确认输出字段、概率分布、metrics 和显存占用都正常后，才运行全量。

## 当前实现文件

当前已经建立：

```text
src/inference/prompts.py
src/inference/tokenization_check.py
src/inference/scoring.py
src/inference/base_zero_shot.py
src/inference/prediction_io.py
```

职责：

```text
prompts.py
  只负责把 Y/N 样本渲染成 prompt。

tokenization_check.py
  只负责检查 Yes/No/A/B/C/D/E 的 tokenizer 输出。

scoring.py
  实现 score_yesno 和 score_candidates。

base_zero_shot.py
  CLI 入口：读取数据、调用 scorer、写 predictions 和 metrics。

prediction_io.py
  统一 prediction jsonl 和 metrics json 的读写。
```

## 建议的 CLI

本地 dry-run：

```bash
python -m src.inference.base_zero_shot --config configs/experiment.yaml --dataset movielens-100k --mode mock --limit 20
```

云端真实运行：

```bash
python -m src.inference.base_zero_shot --config configs/experiment.yaml --dataset movielens-100k --mode real --batch-size 16
```

如果只想先跑 validation：

```bash
python -m src.inference.base_zero_shot --config configs/experiment.yaml --dataset movielens-100k --mode real --splits validation --batch-size 16
```

## Prediction 文件字段

### Y prediction

每行建议：

```json
{
  "model": "base",
  "task": "Y",
  "split": "validation",
  "user_id": "196",
  "target_movie_id": "94",
  "label": "No",
  "p_yes": 0.34,
  "p_no": 0.66,
  "predicted_label": "No",
  "prompt_hash": "..."
}
```

### N prediction

每行建议：

```json
{
  "model": "base",
  "task": "N",
  "split": "validation",
  "user_id": "196",
  "candidate_movie_ids": ["1082", "1027", "94", "1415", "1337"],
  "ground_truth_index": 2,
  "ground_truth_movie_id": "94",
  "label_probabilities": {
    "A": 0.10,
    "B": 0.18,
    "C": 0.52,
    "D": 0.12,
    "E": 0.08
  },
  "scores": [0.10, 0.18, 0.52, 0.12, 0.08],
  "predicted_label": "C",
  "prompt_hash": "..."
}
```

`scores` 的顺序必须和 `candidate_movie_ids` / `label_set` 一致。

## Metrics 文件字段

建议 `valid_metrics.json`：

```json
{
  "model": "base",
  "dataset": "movielens-100k",
  "split": "validation",
  "binary": {
    "AUC": 0.0,
    "F1": 0.0,
    "Accuracy": 0.0,
    "samples": 1985
  },
  "ranking": {
    "HR@1": 0.0,
    "HR@5": 0.0,
    "NDCG@5": 0.0,
    "MRR": 0.0,
    "samples": 902
  }
}
```

真实指标值由模型推理后填入。

## Base 完成标准

STEP 4 完成需要满足：

```text
1. tokenization_report.json 已生成。
2. Y valid/test predictions 已生成。
3. N valid/test predictions 已生成。
4. Y binary metrics 已生成。
5. N ranking metrics 已生成。
6. 所有输出保存到 outputs/base/{dataset}。
7. 没有重新采样候选集。
8. 没有训练或保存 adapter。
```

完成后才能进入：

```text
STEP 5：Y-K0 small smoke / overfit / formal training
```
