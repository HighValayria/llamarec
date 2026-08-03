# 源码地图

MVP 实现按 STEP 顺序推进。每一步通过验收前，不提前填充后续阶段。

## STEP 顺序

1. 固定实验配置：`configs/experiment.yaml`
2. MovieLens 数据层：`src/data/`
3. 固定候选集与指标：`src/eval/`
4. Base LLM 零样本推理：`src/inference/`
5. Y-K0 训练与评测：`src/train/`
6. N-K0 训练与评测：`src/train/`
7. M-K0 交替任务训练：`src/train/`
8. 统一评测与错误分析：`src/analysis/`

## 当前任务命名

- Y：Yes/No Preference Prediction
- N：Full-sequence Next-item Prediction
- M：Y + N Multi-task

Ranking 只作为 N 的候选集评测方式，不再作为独立训练任务名称。

## 实现规则

每个脚本都必须加载共享配置，并把结构化产物写入 `outputs/` 或
`data/processed/` 中约定的位置。
