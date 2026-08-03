---
title: 当前项目状态
type: current-state
status: current
authority: descriptive
source: mixed
created: 2026-07-28
updated: 2026-08-03
last_verified: 2026-08-03
related_code:
  - task.md
  - README.md
  - configs/README.md
  - configs/experiment.yaml
  - configs/y.yaml
  - configs/n.yaml
  - configs/m.yaml
  - wiki/architecture/mvp_experiment_contract.md
  - wiki/modules/movielens_data_layer.md
  - wiki/modules/evaluation_layer.md
  - wiki/modules/inference_layer.md
  - wiki/modules/training_layer.md
  - wiki/guides/mvp_development_steps.md
  - wiki/guides/step2_data_layer_filling_guide.md
  - wiki/guides/current_data_flow.md
  - wiki/guides/step4_base_zero_shot_guide.md
  - wiki/reports/movielens_1m_mvp_results.md
  - wiki/reports/m_multitask_interference_diagnosis_results.md
  - wiki/reports/mvp_execution_status_and_findings.md
  - wiki/reports/phase_1_5_step_a_repository_check.md
---

# 当前项目状态

## 目标

在 MovieLens 上构建可靠、可复现、可继续扩展的 LLM 推荐微调 MVP。MovieLens-1M 上的 MVP 主链路已完成；当前进入 Phase 1.5，工作重心是实验口径统一、分组诊断与 Ranking 稳健性验证。主任务命名统一为 Y / N / M：

- Base
- Y-K0：Yes/No Preference Tuning
- N-K0：Full-sequence Next-item Tuning
- M-K0：Y + N Multi-task Tuning

MovieLens-100K 用于开发与流程验证。MovieLens-1M 是当前 MVP 主结果数据集。MovieLens-32M 暂停作为 Phase 2 或压力测试数据。

## 当前任务定义

Y 是 preference prediction：

```text
P(Like | History, Item)
```

N 是 behavioral sequence prediction：

```text
P(Next Item | History, Candidate Set)
```

N 的 ground truth 来自 full interaction sequence 中真实发生的下一次 interaction，不根据评分过滤。

M 是同一个模型联合学习 Y 与 N，并分别以 M-Y 和 M-N 两种模式评测。

## MovieLens-1M MVP 结论

MVP 主结果已经固化到 `outputs/results.csv`、`outputs/reports/movielens-1m_mvp_report.md`、`outputs/error_analysis/movielens-1m/test_error_analysis.md` 和 [MovieLens-1M MVP 主结果报告](reports/movielens_1m_mvp_results.md)。项目执行历程与总体发现汇总见 [MVP 执行历程、当前现状与主要发现](reports/mvp_execution_status_and_findings.md)。

核心结论：

- Y-K0 将 binary preference prediction 的 test AUC 从 0.6205 提升到 0.7691。
- N-K0 将 next-item ranking 的 test HR@1 从 0.3167 提升到 0.7189。
- Y 与 N 学习不同监督语义；Y-K0 的 `P(Yes)` 不能替代 N 的 candidate label probability。
- M-K0 同时显著优于 Base，但低于对应单任务模型：M-K0 test AUC 0.7234 低于 Y-K0 0.7691，M-K0 test HR@1 0.6717 低于 N-K0 0.7189。
- 当前 M-K0 是能力折中，而不是超过单任务的正迁移；不能声称 M 已产生全面正迁移。
- M-Y 存在 Yes 偏置：test FP=3986、FN=156、No 样本 Mean P(Yes)=0.6054。
- 当前 `candidate_num = 5`，HR@5 没有区分度；ranking 结论主要依据 HR@1、NDCG@5、MRR、mean margin 和 rank distribution。

## 当前后续重点

M-K0 多任务干扰诊断的第一轮已经完成，详见 [M 多任务干扰诊断结果](reports/m_multitask_interference_diagnosis_results.md)。当前进入 Phase 1.5，不继续跑 M3，不进入 KAR、Hard Negative、SASRec、7B、多 seed 或 32M full training。

诊断矩阵当前状态：

| 实验 | 定义 | 状态 |
|---|---|---|
| M0 | 200k Y + 200k N，max_steps=1500 | 已完成，MVP baseline |
| M1 | 200k Y + 200k N，max_steps=3000 | 已完成，当前最佳 M 诊断版本 |
| M2 | Y:N sampling ratio=2:1，200k Y + 100k N，max_steps=1500 | 已完成，未缓解干扰且损害 N |
| M3 | Y:N sampling ratio=1:2 | 不启动，当前解释收益不足 |

M1 的主要结论：

- validation best-F1 threshold 校准后，M1 test AUC=0.7669、F1=0.7818、Accuracy=0.7029，已经接近 Y-K0。
- M1 test HR@1=0.6950、NDCG@5=0.8674、MRR=0.8223，明显优于 M0，但仍低于 N-K0。
- M1 将 No 样本 Mean P(Yes) 从 M0 的 0.6054 降到 0.3830，说明 Yes 偏置得到明显缓解。
- M2 的 No 样本 Mean P(Yes)=0.6966，并且 HR@1 降到 0.6548，说明简单提高 Y 采样比例不是有效缓解方案。

Phase 1.5 的 STEP A 仓库检查已经固化到 [Phase 1.5 STEP A 仓库检查报告](reports/phase_1_5_step_a_repository_check.md)。STEP B 的统一 binary 阈值比较入口已经建立为 `src/analysis/threshold_comparison.py`，可在包含完整云端 prediction 文件的环境中生成 AUC、固定 0.5 threshold、validation-calibrated threshold 三张表。下一步应运行 STEP B 正式报告，并继续开发 STEP C 离线分组 error analysis。

## 当前数据划分规范

严格历史规则：

```text
history = 所有 timestamp < target_timestamp 的 interaction
```

timestamp tie 不再导致整个用户退出数据集。

Y 可以在同一 timestamp bucket 内产生多个 target，这些 target 共享同一份严格 history。

N 只构造严格可确定的 next-item sample。如果下一 timestamp bucket 中有多个 interaction，则跳过该歧义 N sample，而不是跳过整个 user。

Y 和 N 不要求拥有完全相同的用户集合：

```text
Base-Y / Y-K0 / M-Y 共享同一固定 Y validation/test set。
Base-N / N-K0 / M-N 共享同一固定 N validation/test set。
```

当前 `344/943` 用户方案只允许用于开发阶段 smoke test，不作为正式主实验数据方案。

## Multi-task Temporal Leakage

M 训练必须遵循：

```text
Raw interactions
-> chronological split
-> Y_train / N_train
-> multi-task training
```

禁止先从完整数据生成全部 Y/N 样本后再混合训练。任何已位于用户 validation/test 时间范围的 interaction，不得以任何形式进入 M 训练数据。

## 已建立

- Wiki 系统与 guard 工具。
- MVP 配置契约与目录脚手架。
- STEP 2 MovieLens 数据层入口、timestamp bucket split、Y/N 样本构造、统计、验收清单和测试。
- STEP 3 固定候选集生成、Ranking 指标、Binary 指标和测试。
- 当前数据流说明文档，解释 STEP 2/3 产物如何流向后续 Base/Y/N/M。
- STEP 4 Base zero-shot 输入、输出、prompt、tokenization 和云端运行指南。
- STEP 4 Base zero-shot 本地 dry-run 入口、mock scorer、真实 scorer、batch 推理、进度条、增量 prediction 输出、metrics 输出和测试。
- STEP 5 Y-K0 adapter 评测入口，支持 Y binary 评测以及用 `P(Yes)` 对固定 N 候选集排序。
- STEP 5 Y-K0 训练数据编码、QLoRA 训练入口、smoke 参数、adapter 保存、可选重载检查和 `reload-only` 补验入口。
- STEP 6 N-K0 训练数据编码、QLoRA 训练入口、smoke 参数、adapter 保存和候选概率 reload 检查入口。
- STEP 6 N-K0 adapter 评测入口，支持固定候选集上的 `P(A)...P(E)` ranking 评测。
- STEP 7 M-K0 交替多任务训练数据编码、QLoRA 训练入口、smoke 参数、adapter 保存和双接口 reload 检查入口。
- STEP 7 M-K0 adapter 双接口评测入口，分别输出 M-Y binary metrics 与 M-N ranking metrics。
- `configs` 已同步为 Base、Y-K0、N-K0、M-K0 配置外壳，其中序列任务配置文件为 `configs/n.yaml`。
- MovieLens-100K 已按新版 timestamp tie 策略重新生成开发产物。
- MovieLens-100K 固定候选集已生成到 `data/candidates/movielens-100k/valid.jsonl` 和 `data/candidates/movielens-100k/test.jsonl`。
- MovieLens-100K Base/Y/N/M 预算实验已在云端完整跑通，验证了 MVP 主链路。
- MovieLens-1M 原始格式读取、完整 STEP 2 数据产物、STEP 3 固定候选集、Base/Y/N/M 预算训练、统一评测和基础 error analysis 已完整跑通，成为当前 MVP 主结果数据集。
- MovieLens-32M 已生成本地 eval-only STEP 2/3/4 产物，但当前不再作为 MVP 主线。

## 进行中

- Phase 1.5 STEP B：`threshold_comparison.py` 已实现并通过本地 toy 测试，正式 MovieLens-1M 报告需要在云端完整 prediction 文件环境中运行。随后进入 STEP C 分组 error analysis。当前不建议继续启动新的 M 长训练。

## 已知问题 / 漂移

- MovieLens-100K 结果已完成，主要作为流程验证和对照参考。
- MovieLens-1M 已完成 STEP 2/3 和真实 Base/Y/N/M 云端预算实验；结果汇总与基础 error analysis 产物已生成。
- MovieLens-32M Base LLM validation/test 全量评测已完成，但因运行成本过高，32M 不再作为当前 MVP 主线。
- M1 已显著缓解 M0 的多任务干扰，但 M-N 仍低于 N-K0，因此当前仍不能声称 M 全面超过单任务模型。
- `src/train/multitask_dataset.py` 已支持通过 `task_ratio_y/task_ratio_n` 编码 1:1、2:1 或 1:2 的 Y/N 顺序样本。
- `src/train/train_m.py` 已支持 `--task-ratio-y`、`--task-ratio-n` 和分任务 validation loss，训练日志中应出现 `eval_y_loss` 与 `eval_n_loss`。
- error analysis 当前为基础版本，覆盖 binary confusion、ranking rank/margin/position sanity check 和代表性错误样本；下一步应扩展为分组诊断，而不是新模型训练。
- `src/analysis/threshold_calibration.py` 已用于 M-Y 校准诊断：M1 的 validation best-F1 threshold 为 0.3208213008，应用到 test 后 F1=0.7818，说明默认 0.5 threshold 低估了 M1 的 binary 表现。

## 当前 100K 开发产物摘要

```text
Y users: 943
N users: 902
Y samples: train 95867 / validation 1985 / test 2148
N samples: train 21995 / validation 902 / test 902
```

## 当前 100K 候选集摘要

```text
valid candidates: 902 records
test candidates: 902 records
candidate_num: 5
validation ground_truth_index: 0=166 / 1=196 / 2=188 / 3=174 / 4=178
test ground_truth_index: 0=190 / 1=195 / 2=173 / 3=171 / 4=173
```

## 当前 32M eval-only 产物摘要

```text
Y users: 200902
N users: 193491
Y samples: validation 314243 / test 285734
N samples: validation 193491 / test 193491
local_eval_only: true
```

## 当前 32M 候选集摘要

```text
valid candidates: 193491 records
test candidates: 193491 records
candidate_num: 5
validation ground_truth_index: 0=38826 / 1=38529 / 2=38882 / 3=38487 / 4=38767
test ground_truth_index: 0=38407 / 1=38527 / 2=38852 / 3=38701 / 4=39004
```

## 当前 1M 主实验产物摘要

```text
Y users: 6040
N users: 5675
Y samples: train 976284 / validation 12381 / test 11544
N samples: train 212725 / validation 5675 / test 5675
valid candidates: 5675 records
test candidates: 5675 records
candidate_num: 5
validation ground_truth_index: 0=1090 / 1=1104 / 2=1128 / 3=1155 / 4=1198
test ground_truth_index: 0=1097 / 1=1140 / 2=1207 / 3=1111 / 4=1120
```

## 当前 STEP 4 本地 dry-run 摘要

```text
mode: mock
limit: 20 per split/task
100K outputs: outputs/base/movielens-100k
32M outputs: outputs/base/movielens-32m
validation: Y predictions 20 / N predictions 20 for each dataset
test: Y predictions 20 / N predictions 20 for each dataset
```

这些结果只用于验证文件流和指标流，不代表真实 Base LLM 性能。

## 重要约束

- 若重新生成数据或候选集，不得跳过 STEP 1-3。
- M 诊断完成前，不增加 KAR、SASRec、Hard Negative、Bootstrap、额外数据集、7B 模型、超参数搜索或多 seed 实验。
- M 默认仍采用混合或交替训练；如果后续实现“先 Y 后 N”的训练，只能标注为 sequential fine-tuning，不能标注为 multi-task joint training。

## 近期语义变更

2026-07-30：更新 timestamp tie 策略。严格 history 保留，但 tie 不再导致整个用户删除；Y 可保留同 timestamp 多 target，N 只跳过歧义 next-item sample。

2026-07-30：更新公平性口径。Base-Y/Y-K0/M-Y 共享固定 Y validation/test，Base-N/N-K0/M-N 共享固定 N validation/test；Y/N 不强制相同用户集合。

2026-07-30：新增 Multi-task Temporal Leakage 规范，M 必须先时间切分，再构造 Y_train/N_train，再混合或交替训练。

2026-07-30：STEP 2 代码迁移到 timestamp bucket split。MovieLens-100K 重新生成后，Y 覆盖 943 用户，N 覆盖 902 用户，N validation/test 均为 902 样本。

2026-07-30：STEP 3 建立固定候选集与指标测试。MovieLens-100K valid/test 候选集各 902 条，Ranking/Binary 指标具备可执行测试。

2026-07-30：STEP 4 建立 Base zero-shot 本地 dry-run。当时可以在 mock 模式下生成 Y/N prediction、metrics、config snapshot 和 tokenization report；真实模型 scorer 尚未接入，该限制已由 2026-07-31 的真实 scorer 接入解除。

2026-07-30：将候选集和模型输出迁移为按数据集隔离路径，避免 100K 与 32M 相互覆盖。

2026-07-30：MovieLens-32M 已完成本地 eval-only STEP 2/3/4。当前保留 Y/N validation/test、固定候选集、Base mock dry-run、split 和 stats；完整 train JSONL 未在本地保留。

2026-07-31：STEP 4 真实 Base scorer 已接入。`--mode real` 可在云端加载 `meta-llama/Llama-3.2-3B-Instruct`，对 Y 输出 `P(Yes)/P(No)`，对 N 输出 `P(A)...P(E)`；若答案为多 token，会退回完整 sequence likelihood。

2026-08-01：STEP 4 Base zero-shot 增加 `--batch-size` / `--batch_size`，真实 scorer 支持批量单 token logits 推理；prediction 改为分批增量写出，并显示 Y/N 进度条。

2026-08-01：STEP 5 Y-K0 训练代码链路建立。新增 Y 训练数据编码、QLoRA 训练 CLI、smoke 参数、adapter 保存和可选重载检查；尚未执行云端 smoke/overfit。

2026-08-01：MovieLens-32M Base validation/test 全量评测完成。Y-K0 MovieLens-100K smoke training 已完成，训练后 reload check 的 tokenizer 输出兼容问题已修复，并新增 `--reload-only` 入口用于不重训补验 adapter 加载与 `P(Yes)/P(No)` 输出。

2026-08-01：新增 Y-K0 adapter 评测入口。`evaluate_y_adapter.py` 可加载 base model + PEFT adapter，对 Y validation/test 输出 `P(Yes)/P(No)` 与 binary metrics，并用 `P(Yes)` 对固定 N candidate set 排序后输出 Ranking metrics。

2026-08-01：新增 N-K0 与 M-K0 训练入口。`train_n.py` 支持 candidate label 训练与 `P(A)...P(E)` reload 检查；`train_m.py` 支持 Y/N 1:1 交替训练与 M-Y/M-N 双接口 reload 检查。当前仅通过本地编码测试，尚未完成云端 smoke。

2026-08-02：MovieLens-100K Base/Y/N/M 预算实验已完整跑通；后续主数据集由 MovieLens-32M 调整为 MovieLens-1M。MovieLens-1M 已完成原始格式读取、STEP 2 数据产物和 STEP 3 固定候选集。

2026-08-02：MovieLens-1M Base/Y/N/M 主结果已完成并固化。Y-K0 与 N-K0 均显著优于 Base；M-K0 同时保留两类能力但低于对应单任务模型，当前结论从“验证 Y/N/M 是否有效”转为“诊断并缓解 Y/N 多任务干扰”。
