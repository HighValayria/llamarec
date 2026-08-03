---
title: MVP 开发步骤
type: guide
status: current
authority: normative
source: mixed
created: 2026-07-28
updated: 2026-08-02
last_verified: 2026-08-02
related_code:
  - task.md
  - README.md
  - wiki/architecture/mvp_experiment_contract.md
---

# MVP 开发步骤

## 目的

使用本指南回看 MVP 推进顺序，避免在未确认的情况下扩大实验范围。MovieLens-1M MVP 主链路已于 2026-08-02 完成；后续工作转入 M 多任务干扰诊断。

## 流程

1. 固定实验配置。
2. 构建 MovieLens full_sequence 数据层。
3. 构建固定 candidate set 和 ranking metrics 测试。
4. 构建 Base LLM zero-shot 推理。
5. 构建 Y-K0 smoke test、训练、保存/加载和评测。
6. 构建 N-K0 smoke test、训练、保存/加载和评测。
7. 构建 M-K0 的 Y/N 多任务训练和两种推理模式。
8. 运行统一评测和基础错误分析。

当前 STEP 1-8 已完成。后续若重新生成数据、候选集或新数据集，仍不要跳过 STEP 1-3。

进入 M-K0 前必须确认多任务数据遵守：

```text
Raw interactions
-> chronological split
-> Y_train / N_train
-> multi-task training
```

不得先从完整数据生成所有 Y/N 样本后再混合训练。

## 验证

每个 step 进入下一步前，必须具备可执行检查或清楚标记的人工检查产物。核心数据逻辑和指标逻辑必须由测试覆盖，不能只写在说明文字里。

## 失败模式

如果结果不符合预期，在增加新模块前，优先检查数据泄漏、任务构造、标签分布、候选难度、候选位置偏置、tokenization、loss mask、训练预算和多任务干扰。

当前已观察到的主要失败模式是 M-K0 多任务干扰：M-K0 同时优于 Base，但低于 Y-K0 与 N-K0 两个对应单任务模型；M-Y 还存在 Yes 偏置。下一阶段应优先执行 M1/M2 诊断，而不是进入 KAR、Hard Negative、SASRec、7B、多 seed 或 32M full training。
