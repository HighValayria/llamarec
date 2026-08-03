# 配置说明

本目录保存实验定义。所有共享实验语义都应放在
`configs/experiment.yaml` 中；任务专属配置文件只选择任务模式、输入输出路径
或未来实现钩子。

## 当前配置文件

- `experiment.yaml`：Base/Y/N/M 共享的 MVP 实验契约。
- `y.yaml`：Y-K0 / Yes-No Preference Tuning 外壳。
- `n.yaml`：N-K0 / Full-sequence Next-item Tuning 外壳。
- `m.yaml`：M-K0 / Y+N Multi-task Tuning 外壳。

## 当前规则

不要在脚本中硬编码数据划分、候选数量、负采样方式、模型名、LoRA 设置或指标定义。
脚本应从 `configs/experiment.yaml` 或继承它的任务配置中读取这些信息。

候选集与模型输出按数据集隔离：

```text
data/candidates/{dataset}/valid.jsonl
data/candidates/{dataset}/test.jsonl
outputs/base/{dataset}/
outputs/y/{dataset}/
outputs/n/{dataset}/
outputs/m/{dataset}/
```

MovieLens-32M 的 processed JSONL 默认写成 `.jsonl.gz`，以避免本地磁盘被展开后的训练样本耗尽。
当前后续主数据集是 MovieLens-1M；MovieLens-32M 暂停作为 Phase 2 或压力测试数据。

## STEP 1 用户确认项

进入 STEP 2 前，请确认或修改：

- `model.base_model.name_or_path`
- `runtime.device_profile`
- `runtime.local_python`
- `paths.raw_movielens_100k`
- `paths.raw_movielens_1m`
- `paths.raw_movielens_32m`

Base 模型路径是云端执行使用的象征性 HuggingFace 路径。本地开发不需要下载 Llama 模型。

MVP 范围保持冻结为 Base、Y-K0、N-K0 和 M-K0。MovieLens-1M 主结果已经完成；下一阶段只围绕 M-K0 多任务干扰诊断。

当前 `configs/m.yaml` 中的 `optimizer_step_ratio` 会作为 M 训练的默认 Y/N 采样比例。也可以在 CLI 中用 `--task-ratio-y` 和 `--task-ratio-n` 显式覆盖，例如 M2 使用 `--task-ratio-y 2 --task-ratio-n 1`。M1 仍通过 CLI 修改 `--max-steps`。
