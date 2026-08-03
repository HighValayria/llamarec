# 训练模块

训练模块从 STEP 5 开始使用。当前已经覆盖：

- Y-K0：Yes/No Preference Tuning
- N-K0：Full-sequence Next-item Tuning
- M-K0：Y + N Multi-task Tuning

## 当前文件

- `preference_dataset.py`：把 Y 样本编码为 causal LM 训练样本，并只在 `Yes/No` 答案 token 上计算 loss。
- `next_item_dataset.py`：把 N 样本编码为 candidate label 训练样本，并只在 `A-E` 答案 token 上计算 loss。
- `multitask_dataset.py`：按可配置 Y/N 采样比例编码 M 样本，默认 1:1。
- `train_y.py`：Y-K0 训练 CLI，支持 QLoRA、checkpoint、validation、adapter 保存和可选重载检查。
- `train_n.py`：N-K0 训练 CLI，支持 candidate label reload check。
- `train_m.py`：M-K0 训练 CLI，支持 mixed validation、Y-only/N-only validation loss、可配置 Y/N 采样比例和双接口 reload check。

## Smoke test 门槛

- 先使用 500-1000 条样本。
- 验证 LoRA 注入与可训练参数数量。
- 验证 loss 下降。
- 验证小样本过拟合行为。
- 验证 adapter 保存与重载。
- 验证重载后打分仍能返回概率。

Smoke test 失败时，不得启动正式训练。

## Y-K0 smoke 命令

云端示例：

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

MovieLens-32M 的正式 Y 训练需要先确认 `preference_train.jsonl.gz` 已在云端生成；本地目前只保留 32M eval-only 产物。

## M 诊断 smoke 命令

M1/M2 长训练前，先在云端用小样本确认 ratio 和分任务 validation 字段生效：

```bash
python -m src.train.train_m \
  --config configs/m.yaml \
  --dataset movielens-1m \
  --run-name smoke_m_ratio_y2n1 \
  --smoke \
  --max-y-train-samples 200 \
  --max-n-train-samples 200 \
  --max-y-valid-samples 50 \
  --max-n-valid-samples 50 \
  --task-ratio-y 2 \
  --task-ratio-n 1 \
  --max-steps 10 \
  --eval-steps 5 \
  --save-steps 5 \
  --per-device-train-batch-size 1 \
  --per-device-eval-batch-size 1 \
  --gradient-accumulation-steps 2 \
  --bf16 \
  --run-reload-check
```

检查产物：

```text
outputs/m/{dataset}/{run_name}/run_summary.json
outputs/m/{dataset}/{run_name}/encoded_dataset_summary.json
outputs/m/{dataset}/{run_name}/metrics.json
outputs/m/{dataset}/{run_name}/reload_check.json
```

`metrics.json` 应包含 mixed `eval_loss`，以及分任务 `eval_y_loss` 和 `eval_n_loss`。
