---
title: M 多任务干扰诊断计划
type: report
status: superseded
authority: normative
source: user-requested
created: 2026-08-02
updated: 2026-08-03
last_verified: 2026-08-03
superseded_by: wiki/reports/m_multitask_interference_diagnosis_results.md
related_code:
  - task.md
  - README.md
  - configs/m.yaml
  - src/train/multitask_dataset.py
  - src/train/train_m.py
  - src/inference/evaluate_m_adapter.py
  - src/analysis/summarize_results.py
  - src/analysis/basic_error_analysis.py
---

# M 多任务干扰诊断计划

> 本计划已执行完成，并由 [M 多任务干扰诊断结果](m_multitask_interference_diagnosis_results.md) 接替为当前报告入口。保留本文仅用于追溯当时的实验设计和云端命令。

## 背景

MovieLens-1M MVP 主结果已经完成。当前结论不是“继续验证 Y/N/M 是否有效”，而是：

```text
Y 与 N 均有效；
M-K0 同时保留两类能力；
但 M-K0 低于对应单任务模型，存在 Y/N 多任务干扰。
```

当前 M-K0 test 结果：

```text
M-Y AUC  = 0.7234 < Y-K0 AUC  0.7691
M-N HR@1 = 0.6717 < N-K0 HR@1 0.7189
```

M-Y 的主要异常是 Yes 偏置：

```text
FP = 3986
FN = 156
Mean P(Yes) for Yes = 0.6927
Mean P(Yes) for No  = 0.6054
```

## 诊断问题

下一阶段只回答以下问题：

1. M-K0 是否只是尚未充分收敛？
2. M-Y 的 Yes 偏置是否来自 Y/N 采样比例或任务更新数失衡？
3. 若调整采样比例后仍无法同时改善 Y 与 N，是否存在梯度或容量冲突？
4. 当前结果是否可能由 future leakage 或评测口径不公平导致？

不要在这些诊断完成前启动 KAR、Hard Negative、SASRec、MovieLens-32M full training、7B 模型、多 seed 或大规模超参数搜索。

## 最小实验矩阵

| 实验 | Y:N ratio | train pool | max_steps | 目的 | 状态 |
|---|---:|---|---:|---|---|
| M0 | 1:1 | 200k Y + 200k N | 1500 | 当前 baseline | 已完成 |
| M1 | 1:1 | 200k Y + 200k N | 3000 | 判断是否未收敛 | 已完成，当前最佳 M 诊断版本 |
| M2 | 2:1 | 200k Y + 100k N | 1500 | 检查 Y 相对权重提高后 Yes 偏置是否缓解 | 已完成，结论为无效且损害 N |
| M3 | 1:2 | 优先保持总预算可比 | 1500 或与 M1 对齐 | 可选 N-heavy 对照 | 不启动 |

M2 本轮只采用 sampling ratio，不同时调整 loss weight。

## 必须记录的指标

每个实验都要保留：

```text
Experiment
Y:N ratio
max_steps
Y AUC
Y F1
Y Acc
Y FP
Y FN
Mean P(Yes) for Yes
Mean P(Yes) for No
N HR@1
N NDCG@5
N MRR
N mean margin
```

训练过程中还必须分别记录 Y validation 和 N validation。混合总 loss 只能作为辅助信息，不能单独用于判断 M 是否收敛。

## 当前代码支持情况

当前 `src/train/train_m.py` 支持：

- 修改 `--max-steps`，因此 M1 的训练步数可以配置。
- 修改 `--max-y-train-samples` 与 `--max-n-train-samples`，用于固定训练样本池。
- 通过 `--task-ratio-y` 与 `--task-ratio-n` 修改 M 的 Y/N 采样比例，因此 M2 的 `Y:N=2:1` 可以直接配置。
- 在默认 mixed validation 外额外记录 Y-only 与 N-only validation loss，指标前缀为 `eval_y_*` 与 `eval_n_*`。
- 训练后保存 adapter，并可用 `src/inference/evaluate_m_adapter.py` 分别评测 M-Y 与 M-N。
- 可用 `src.analysis.threshold_calibration` 做 M-Y 阈值校准：在 validation 上选择 best-F1 threshold，再应用到 test。

正式启动 M1/M2 长训练前，建议先在 100K 或 1M 小样本上做一次 smoke run，检查：

1. `run_summary.json` 中的 `task_ratio`、`interleaved_*_task_counts` 与实验定义一致。
2. `metrics.json` 中包含 `eval_loss`、`eval_y_loss`、`eval_n_loss`。
3. `encoded_dataset_summary.json` 中的 Y/N 样本数与目标 ratio 一致。
4. adapter 仍能通过 reload check。

## 泄漏与公平性检查

M 训练仍必须满足：

```text
Raw interactions
-> chronological split
-> Y_train / N_train
-> multi-task training
```

任何位于用户 validation/test 时间范围的 interaction 都不得进入 M 训练数据。当前数据层和 M 训练入口读取的是 `preference_train` 与 `next_item_train`，没有发现直接 future leakage 迹象。

公平比较口径保持不变：

```text
Base-Y / Y-K0 / M-Y 使用同一固定 Y validation/test set。
Base-N / N-K0 / M-N 使用同一固定 N validation/test set。
```

## 云端命令

以下命令需要先在小样本 smoke run 中确认新 ratio 与分任务 validation 字段生效。

M1 训练与评测：

```bash
cd /root/llamarec
source .venv/bin/activate

python -m src.train.train_m \
  --config configs/m.yaml \
  --dataset movielens-1m \
  --run-name diag_m1_1m_m_200k_3000 \
  --max-y-train-samples 200000 \
  --max-n-train-samples 200000 \
  --max-y-valid-samples 10000 \
  --max-n-valid-samples 10000 \
  --max-steps 3000 \
  --eval-steps 500 \
  --save-steps 500 \
  --per-device-train-batch-size 1 \
  --per-device-eval-batch-size 1 \
  --gradient-accumulation-steps 8 \
  --bf16 \
  --run-reload-check

python -m src.inference.evaluate_m_adapter \
  --config configs/m.yaml \
  --dataset movielens-1m \
  --mode real \
  --adapter-dir outputs/m/movielens-1m/diag_m1_1m_m_200k_3000/adapter \
  --splits validation test \
  --batch-size 16 \
  --output-dir outputs/m/movielens-1m/diag_m1_1m_m_200k_3000
```

M2 训练与评测：

```bash
python -m src.train.train_m \
  --config configs/m.yaml \
  --dataset movielens-1m \
  --run-name diag_m2_1m_m_y2n1_1500 \
  --max-y-train-samples 200000 \
  --max-n-train-samples 200000 \
  --task-ratio-y 2 \
  --task-ratio-n 1 \
  --max-y-valid-samples 10000 \
  --max-n-valid-samples 10000 \
  --max-steps 1500 \
  --eval-steps 500 \
  --save-steps 500 \
  --per-device-train-batch-size 1 \
  --per-device-eval-batch-size 1 \
  --gradient-accumulation-steps 8 \
  --bf16 \
  --run-reload-check

python -m src.inference.evaluate_m_adapter \
  --config configs/m.yaml \
  --dataset movielens-1m \
  --mode real \
  --adapter-dir outputs/m/movielens-1m/diag_m2_1m_m_y2n1_1500/adapter \
  --splits validation test \
  --batch-size 16 \
  --output-dir outputs/m/movielens-1m/diag_m2_1m_m_y2n1_1500
```

更新汇总与 error analysis：

```bash
python -m src.analysis.summarize_results \
  --config configs/experiment.yaml \
  --dataset movielens-1m \
  --y-run pool200k_1m_y_1500 \
  --n-run pool200k_1m_n_1500 \
  --m-run diag_m1_1m_m_200k_3000 \
  --output-csv outputs/results_m1.csv \
  --report-path outputs/reports/movielens-1m_m1_report.md

python -m src.analysis.basic_error_analysis \
  --config configs/experiment.yaml \
  --dataset movielens-1m \
  --y-run pool200k_1m_y_1500 \
  --n-run pool200k_1m_n_1500 \
  --m-run diag_m1_1m_m_200k_3000 \
  --split test \
  --output-dir outputs/error_analysis/movielens-1m/m1_test
```

M0/M1/M2 threshold calibration：

```bash
python -m src.analysis.threshold_calibration \
  --config configs/experiment.yaml \
  --dataset movielens-1m \
  --y-run pool200k_1m_y_1500 \
  --m-runs pool200k_1m_m_1500 diag_m1_1m_m_200k_3000 diag_m2_1m_m_y2n1_1500 \
  --m-labels M0 M1 M2 \
  --output-dir outputs/calibration/movielens-1m/m_diagnostics
```

校准结果用于判断：M1 的 AUC 已接近 Y-K0 时，默认 `0.5` threshold 下 F1 偏低是否主要来自概率校准或阈值偏移。
