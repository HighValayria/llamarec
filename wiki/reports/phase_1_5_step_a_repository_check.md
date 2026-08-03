---
title: Phase 1.5 STEP A 仓库检查报告
type: report
status: current
authority: descriptive
source: mixed
created: 2026-08-03
updated: 2026-08-03
last_verified: 2026-08-03
related_code:
  - configs/experiment.yaml
  - src/eval/candidate_sets.py
  - src/eval/ranking_metrics.py
  - src/inference/base_zero_shot.py
  - src/inference/evaluate_y_adapter.py
  - src/inference/evaluate_n_adapter.py
  - src/inference/evaluate_m_adapter.py
  - src/inference/scoring.py
  - src/inference/tokenization_check.py
  - src/analysis/basic_error_analysis.py
  - src/analysis/summarize_results.py
  - src/analysis/threshold_calibration.py
---

# Phase 1.5 STEP A 仓库检查报告

## 阶段定义

当前阶段定义为：

```text
Phase 1.5：实验口径统一、分组诊断与 Ranking 稳健性验证
```

本阶段不重新设计 Y/N/M 任务，不扩展 KAR，不启动 MovieLens-32M full training，也不进行无目标的 M 超参数搜索。当前目标是复用已有 MovieLens-1M prediction 文件，提高结论可信度和解释力。

## 已完成事实

当前已经完成：

```text
Base
Y-K0
N-K0
M0
M1
M2
```

其中：

| 实验 | 定义 | 定位 |
|---|---|---|
| M0 | Y:N=1:1，200k Y + 200k N，1500 steps | 原始 MVP 多任务 baseline |
| M1 | Y:N=1:1，200k Y + 200k N，3000 steps | 当前主要多任务结果 |
| M2 | Y:N=2:1，200k Y + 100k N，1500 steps | 诊断用 Y-heavy 对照，未缓解问题且损害 N |

后续主报告中应明确：

```text
M0 = 原始低预算多任务 baseline
M1 = compute-matched / extended-training multi-task model
```

M0 的 1500 total steps 在 Y/N 1:1 混合下，使每个任务获得的有效更新量约为单任务训练的一半，因此 M0 相对 Y-K0、N-K0 的退化不能全部解释为多任务冲突。M1 更接近：

```text
约 1500 Y updates
+
约 1500 N updates
```

当前允许的结论是：

```text
M1 在单个 adapter 中几乎保留了 Y-K0 的全部 AUC，
并保留了 N-K0 的大部分 ranking 能力，
但尚未超过对应单任务最优模型。
```

## 本地仓库与云端产物状态

本地仓库当前包含：

- MovieLens-1M STEP 2 处理数据。
- MovieLens-1M k=5 固定候选集。
- 本地 mock/test prediction 文件。
- 分析和评测代码。

本地仓库当前不包含：

- MovieLens-1M Base/Y/N/M0/M1/M2 全量云端 prediction 文件。
- MovieLens-1M 全量云端 metrics/output 目录。
- M1/M2 adapter 权重。

因此 Phase 1.5 的正式分析有两种可行执行路径：

1. 将云端 `outputs/base/y/n/m/movielens-1m` 中的 prediction 和 metrics 文件拉回本地后运行分析。
2. 将新增分析代码推送到 GitHub，在云端拉取后直接基于云端现有 outputs 运行。

本地可以完成代码开发、schema 检查、mock 测试和文档同步，但不能直接复现 1M 全量分组分析结果。

## Prediction 文件 schema 检查

### Y binary prediction

样例字段：

```text
model
task
split
user_id
target_movie_id
label
p_yes
p_no
score
predicted_label
prompt_hash
scoring_mode
adapter_dir（adapter 模型有）
```

缺少字段：

```text
target_rating
target_timestamp
history_length
user_activity
target_popularity
source_sample_index
```

结论：Y 分组分析不能只读 prediction 文件，需要离线回连 `preference_valid/test.jsonl`。由于评测脚本按样本文件顺序写出 prediction，推荐用顺序 zip join，并校验 `user_id` 与 `target_movie_id` 一致。

### N ranking prediction

Base/N/M 的 label-probability ranking 样例字段：

```text
model
task
split
user_id
candidate_movie_ids
ground_truth_index
ground_truth_movie_id
label
label_probabilities
scores
predicted_label
prompt_hash
scoring_mode
adapter_dir（adapter 模型有）
```

Y-K0 by `P(Yes)` ranking 样例字段：

```text
model
task
inference_mode
split
user_id
candidate_movie_ids
ground_truth_index
ground_truth_movie_id
label
candidate_p_yes
candidate_p_no
scores
prompt_hashes
scoring_modes
adapter_dir
```

缺少字段：

```text
target_rating
target_timestamp
history_length
target_popularity
mean/median rank
margin
predicted_index
```

结论：N 分组分析需要回连固定 candidate set。candidate records 已包含：

```text
history
target.rating
target.timestamp
target.title
source_sample_index
candidate_generation
```

推荐用 prediction 与 candidate records 顺序 zip join，并校验：

```text
user_id
ground_truth_movie_id
candidate_movie_ids
ground_truth_index
```

## 候选集生成逻辑检查

当前候选集生成入口为：

```text
src/eval/candidate_sets.py
```

现状：

- 读取配置中的 `candidates.candidate_num`。
- 使用 `label_set[:candidate_num]`。
- 固定随机种子，validation/test 使用不同 seed offset。
- 每条记录包含 1 个 ground truth 和 `candidate_num - 1` 个随机负候选。
- 候选顺序会 shuffle。
- 校验 ground truth 恰好出现一次、负候选不重复、history 严格早于 target。

发现的问题：

1. 输出路径目前只能从配置 `candidates.save_files.validation/test` 读取，默认会覆盖 k=5 文件；Phase 1.5 需要新增可指定输出路径或 suffix 的入口，避免覆盖现有 k=5 candidate set。
2. `_candidate_summary()` 位置分布初始化写死为 5 个位置；k=20/50 时 summary 不完整。
3. 当前 CLI 没有 `--candidate-num`、`--label-set`、`--output-dir` 或 `--suffix`。
4. 当前无法生成“同一候选 item 集合，仅改变排列”的 permutation 版本。

## 动态 candidate_num 与指标支持检查

当前 ranking 指标在 `src/eval/ranking_metrics.py` 中支持任意 `k` 的单一 cutoff：

```text
HR@1
HR@k
NDCG@k
MRR
```

不足：

- 不支持同时输出 HR@5、HR@10、NDCG@5、NDCG@10。
- 不输出 mean rank、median rank、mean margin。
- `aggregate_ranking_metrics()` 默认 `k=5`，评测脚本未根据 candidate_num 动态选择多个 cutoff。

结论：candidate_num=20/50 之前，需要扩展 ranking metrics 和评测汇总，而不是只把 `candidate_num` 改大。

## Candidate scoring 与 tokenizer 标签支持检查

当前 Base/N/M 的候选 scoring 使用：

```text
P(label)
```

其中 label 来自 candidate record 的 `label_set`。如果所有 label 都是单 token，则使用 single-token logits；如果存在多 token label，scorer 会退回 sequence likelihood。

现状：

- 已验证 Llama-3.2-3B-Instruct 中 `Yes`、`No`、`A`、`B`、`C`、`D`、`E` 是单 token。
- 当前配置只包含 A-E。
- 当前本地环境不加载 Llama tokenizer，因此无法在本地确认 A-T 或 50 个候选标签是否都是单 token。

风险：

- k=20 可以尝试 A-T，但必须在云端 tokenizer report 中验证。
- k=50 不能默认使用数字标签的首 token 打分；如果 label 多 token，必须使用完整 sequence likelihood 或另选稳定单 token 标签方案。

结论：

```text
先可靠实现 k=20；
k=50 先做 tokenizer feasibility；
如果 50 个稳定单 token 标签不可获得，不强行全量运行。
```

## 阈值校准与二分类口径检查

当前已有：

```text
src/analysis/threshold_calibration.py
```

它支持：

- 用 validation 选择 best-F1 threshold。
- 将同一 threshold 应用到 test。
- 比较 Base、Y-K0 和多个 M runs。

不足：

- 当前 Markdown 输出是单表，混合展示 AUC、threshold、F1、Accuracy、Precision、Recall。
- Phase 1.5 需要拆成三类表：
  - 表 A：阈值无关指标，只含 AUC。
  - 表 B：默认 threshold=0.5。
  - 表 C：validation-calibrated threshold。
- 当前文档中已经记录了 Y-K0 `F1=0.7800` 和 `calibrated F1=0.7831`，M1 `F1@0.5=0.7276` 和 `calibrated F1=0.7818`；后续报告不得把不同阈值口径混在同一列。

结论：优先扩展或新增 threshold comparison 输出，而不是只复用旧 calibration Markdown。

## 结果汇总代码检查

当前已有：

```text
src/analysis/summarize_results.py
src/analysis/basic_error_analysis.py
```

现状：

- `summarize_results.py` 只支持 Base/Y/N/M 四类模型，并默认 M 只有一个 run。
- `basic_error_analysis.py` 支持基础 binary confusion、ranking rank/margin/position sanity check 和错误样本导出。

不足：

- 不支持同时纳入 M0/M1/M2。
- 不支持分组 error analysis。
- 不支持 target popularity、history length、user activity 等元数据 join。
- 不支持 N-K0 正确但 M1 错误、M1 正确但 N-K0 错误等 pairwise 差异导出。

结论：需要新增 `grouped_error_analysis.py`，不要把所有逻辑塞进现有基础脚本。

## 多 seed 可执行性检查

当前训练配置中存在：

```text
seed.random_seed = 42
```

但训练入口目前没有显式传入：

```text
seed
data_seed
```

给 `TrainingArguments`。M 训练使用 `SequentialSampler`，而 Y/N 单任务训练默认使用 Trainer sampler。候选集生成和数据处理由配置 seed 控制。

结论：

- 后续多 seed 前，需要补齐训练入口的 seed 传递和记录。
- 当前阶段只做可执行性检查，不启动 42/43/44 多 seed 训练。

## 拟修改文件

STEP B：统一 binary 阈值报告

```text
src/analysis/threshold_comparison.py
tests/test_analysis_outputs.py
src/analysis/README.md
```

STEP C：分组 Error Analysis

```text
src/analysis/grouped_error_analysis.py
tests/test_grouped_error_analysis.py
src/analysis/README.md
```

STEP D/F：candidate_num=20 与候选顺序稳健性

```text
src/eval/candidate_sets.py
src/eval/ranking_metrics.py
src/inference/base_zero_shot.py
src/inference/evaluate_y_adapter.py
src/inference/evaluate_n_adapter.py
src/inference/evaluate_m_adapter.py
tests/test_candidate_sets.py
tests/test_ranking_metrics.py
tests/test_base_zero_shot_local.py
tests/test_n_m_adapter_evaluation.py
tests/test_y_adapter_evaluation.py
```

STEP E：candidate_num=50 可行性

```text
src/inference/tokenization_check.py
src/inference/scoring.py（如需要显式报告 sequence-likelihood fallback）
src/analysis/README.md
```

文档同步：

```text
README.md
task.md
wiki/current_state.md
wiki/reports/phase_1_5_step_a_repository_check.md
wiki/reports/mvp_execution_status_and_findings.md
wiki/history/2026-08.md
```

## STEP A 结论

1. Phase 1.5 可以基于现有代码推进，但正式 1M 分析需要云端全量 prediction 文件。
2. 现有 prediction schema 不含分组字段，必须做离线 metadata enrichment。
3. k=20/50 不能通过简单改配置完成，需要扩展 candidate set 输出、评测指标和推理入口。
4. k=20 的标签方案需要云端 tokenizer 验证；k=50 暂不能保证可靠。
5. Binary 阈值口径需要拆成 AUC、0.5 threshold、validation-calibrated threshold 三张表。
6. 当前不应启动新训练；下一步应进入 STEP B 和 STEP C 的离线分析代码开发。
