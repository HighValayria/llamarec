---
title: 训练层
type: module
status: current
authority: descriptive
source: mixed
created: 2026-08-01
updated: 2026-08-02
last_verified: 2026-08-02
related_code:
  - configs/y.yaml
  - configs/n.yaml
  - configs/m.yaml
  - src/train/preference_dataset.py
  - src/train/next_item_dataset.py
  - src/train/multitask_dataset.py
  - src/train/train_y.py
  - src/train/train_n.py
  - src/train/train_m.py
  - src/train/README.md
  - tests/test_y_training_data.py
  - tests/test_n_training_data.py
  - tests/test_m_training_data.py
---

# 训练层

## 当前范围

训练层当前覆盖：

- STEP 5：Y-K0 Yes/No Preference Tuning
- STEP 6：N-K0 Full-sequence Next-item Tuning
- STEP 7：M-K0 Y + N Multi-task Tuning

尚未实现 Hard Negative、KAR、多 seed 或其他 Phase 2 扩展。

MovieLens-1M 的 Base/Y/N/M MVP 训练与评测主链路已经完成。当前训练层的下一项工作不是新增 Phase 2 模块，而是支持 M 多任务干扰诊断。

## Y-K0 输入

Y-K0 读取 STEP 2 的偏好样本：

```text
data/processed/{dataset}/preference_train.jsonl
data/processed/{dataset}/preference_valid.jsonl
```

MovieLens-32M 若使用 gzip，则路径由 `configs/experiment.yaml` 自动解析为 `.jsonl.gz`。

## 训练目标

每条样本渲染为：

```text
History + Target movie -> Yes / No
```

训练时只在答案 token 上计算 loss：

```text
prompt tokens: label = -100
answer tokens: label = token id of Yes/No
```

这用于避免模型在训练中学习复述 prompt。

## 当前入口

```bash
python -m src.train.train_y --config configs/y.yaml
python -m src.train.train_n --config configs/n.yaml
python -m src.train.train_m --config configs/m.yaml
```

常用 smoke 命令：

```bash
python -m src.train.train_y \
  --config configs/y.yaml \
  --dataset movielens-100k \
  --run-name smoke_100k \
  --smoke \
  --max-train-samples 1000 \
  --max-valid-samples 1000 \
  --max-steps 100 \
  --eval-steps 25 \
  --save-steps 25 \
  --bf16 \
  --run-reload-check
```

样本上限约定：

```text
--max-train-samples 1000  # smoke / overfit
--max-valid-samples 1000

--max-train-samples -1    # 正式训练读取全量 train set
--max-valid-samples -1    # 正式 validation 读取全量 validation set
```

为了避免误把 smoke 当成正式训练，正式训练命令必须显式传入负数样本上限。

## 输出

默认输出目录：

```text
outputs/y/{dataset}/{run_name}/
```

主要产物：

```text
config_snapshot.yaml
run_summary.json
encoded_dataset_summary.json
metrics.json
adapter/
reload_check.json
```

其中 `reload_check.json` 可以通过两种方式生成：

```bash
# 训练结束后自动重载 adapter 检查
python -m src.train.train_y \
  --config configs/y.yaml \
  --dataset movielens-100k \
  --run-name smoke_100k \
  --run-reload-check

# 不重新训练，只检查已经保存的 adapter
python -m src.train.train_y \
  --config configs/y.yaml \
  --dataset movielens-100k \
  --reload-only \
  --adapter-dir outputs/y/movielens-100k/smoke_100k/adapter
```

`reload-only` 默认从 Y validation set 读取 1 条样本，验证 adapter 能否重新加载并输出 `P(Yes)/P(No)`。

## N-K0

N-K0 读取 STEP 2 的 next-item 样本：

```text
data/processed/{dataset}/next_item_train.jsonl
data/processed/{dataset}/next_item_valid.jsonl
```

训练目标是正确 candidate label：

```text
History + Candidate Set -> A / B / C / D / E
```

训练时同样只在答案 token 上计算 loss。训练后 `--run-reload-check` 会重载 adapter 并输出 `P(A)...P(E)`。

## M-K0

M-K0 同时读取 Y 与 N 训练样本，当前采用简单 1:1 交替：

```text
Y example
N example
Y example
N example
...
```

实现上取 `min(Y样本数, N样本数)` 对样本，以保持两类任务数量相同；训练 sampler 使用顺序采样以保留交替顺序。训练后 `--run-reload-check` 会分别检查：

```text
M-Y: P(Yes), P(No)
M-N: P(A), P(B), P(C), P(D), P(E)
```

当前 `train_m.py` 支持通过 CLI 修改 `--max-steps`、`--max-y-train-samples`、`--max-n-train-samples`、`--max-y-valid-samples` 和 `--max-n-valid-samples`。因此 M1 延长训练步数在入口层可配置。

当前 `train_m.py` 也支持通过 `--task-ratio-y` 和 `--task-ratio-n` 覆盖配置中的 `optimizer_step_ratio`。例如 M2 可以使用：

```bash
python -m src.train.train_m \
  --config configs/m.yaml \
  --dataset movielens-1m \
  --task-ratio-y 2 \
  --task-ratio-n 1
```

训练期 validation 会先记录 mixed eval dataset 的总 loss，再追加分任务 validation loss：

```text
eval_y_loss
eval_n_loss
```

训练后的 `evaluate_m_adapter.py` 仍用于分别输出 M-Y binary metrics 与 M-N ranking metrics；它和训练过程中的 per-task validation curve 互补，不能互相替代。

## 当前限制

- MovieLens-1M Base/Y/N/M MVP 主结果已完成，训练层主链路已验证。
- M-K0 当前低于对应单任务模型，下一步是诊断 M 多任务干扰。
- M1 延长训练可以通过 `--max-steps` 运行。
- M2 可以通过 `--task-ratio-y 2 --task-ratio-n 1` 运行；正式长训练前应先做小样本 smoke run，确认 `run_summary.json`、`metrics.json` 和 adapter reload check 正常。
- 若后续实现“先完整训练 Y，再完整训练 N”，必须标注为 sequential fine-tuning，不得标注为 multi-task joint training。
