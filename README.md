# LlamaRec MVP 工作区

当前项目已完成 MovieLens-1M MVP 主链路，后续工作重心从“验证 Y/N/M 是否有效”调整为“诊断并缓解 Y/N 多任务干扰”。主任务命名统一为 Y / N / M：

- Base
- Y-K0：Yes/No Preference Tuning
- N-K0：Full-sequence Next-item Tuning
- M-K0：Y + N Multi-task Tuning

Y 表示 Preference Prediction，使用 target 评分得到 Yes/No 标签。

N 表示基于完整交互序列的 Next-item Prediction，也可以理解为 Next-interaction Prediction。N 的 ground truth 是用户真实发生的下一次 interaction，不按评分高低筛选。

M 使用同一个模型联合学习 Y 与 N，并分别以 M-Y 和 M-N 两种模式评测。

## MovieLens-1M MVP 主结论

MovieLens-1M 主结果已经固化到：

```text
outputs/results.csv
outputs/reports/movielens-1m_mvp_report.md
outputs/error_analysis/movielens-1m/test_error_analysis.md
wiki/reports/movielens_1m_mvp_results.md
```

核心结果：

```text
Base:  test AUC 0.6205 / test HR@1 0.3167
Y-K0:  test AUC 0.7691 / test HR@1 0.3048
N-K0:  test HR@1 0.7189 / test NDCG@5 0.8773 / test MRR 0.8356
M-K0:  test AUC 0.7234 / test HR@1 0.6717 / test NDCG@5 0.8562
```

当前结论边界：

- Y 与 N tuning 均明显优于 Base。
- Y 学习 `P(Like | History, Item)`，N 学习 `P(Next Item | History, Candidate Set)`，二者语义不同。
- Y-K0 的 `P(Yes)` 不能替代 N 的 candidate label probability。
- M-K0 在同一个模型中同时保留两类能力，但当前是能力折中，不是超过单任务的正迁移。
- M-Y 存在 Yes 偏置：test FP=3986、FN=156、No 样本 Mean P(Yes)=0.6054。
- 当前 `candidate_num = 5`，HR@5 没有区分度；ranking 结论主要看 HR@1、NDCG@5、MRR、mean margin 和 rank distribution。

## 数据划分原则

MVP 主数据来源是 `full_sequence`。`positive_sequence` 只作为辅助统计或 Phase 2 概念保留，不参与 MVP split，不决定 N target，也不决定 N history。

严格历史规则：

```text
history = 所有 timestamp < target_timestamp 的 interaction
```

同一 timestamp 内没有可观测先后顺序，不得用 movie_id、文件顺序或其他人为规则构造先后关系。

timestamp tie 不再导致整个用户退出数据集。

Y 可以在同一 timestamp 产生多个 target，这些 target 共享同一份严格历史。

N 只构造严格可确定的 next-item 样本。如果下一 timestamp bucket 中有多个 interaction，则跳过该歧义 N sample，而不是跳过整个用户。

当前 `344/943` 用户方案只允许用于开发阶段 smoke test，不作为正式主实验数据方案。

## 公平比较口径

Y 和 N 不要求拥有完全相同的用户集合：

```text
Base-Y / Y-K0 / M-Y
使用同一固定 Y validation/test set。

Base-N / N-K0 / M-N
使用同一固定 N validation/test set。
```

不要为了强制 Y/N 用户完全一致而大量删除用户。

## Multi-task Temporal Leakage

M 的训练数据必须遵循：

```text
Raw interactions
-> chronological split
-> Y_train / N_train
-> multi-task training
```

禁止先从完整数据生成全部 Y/N 样本后再混合训练。

只要某 interaction 已经位于该用户 validation/test 时间范围，就不得以任何形式进入 M 的训练数据。M 默认采用 Y/N 样本混合或交替训练：

```text
Y batch
N batch
Y batch
N batch
...
```

核心原则是：先切时间，再构造任务，再混合训练。

## 当前状态

STEP 1-8 已在 MovieLens-1M 上完成。STEP 2 的 full_sequence 数据层、STEP 3 的固定候选集与指标测试、STEP 4 的 Base zero-shot、STEP 5/6/7 的 Y-K0、N-K0、M-K0 训练与 adapter 评测、STEP 8 的统一汇总和基础 error analysis 都已具备可复现实验产物。

原“实现 Y/N/M 主流程”的 MVP 任务关闭。M-K0 多任务干扰诊断第一轮已经完成，当前进入 Phase 1.5：实验口径统一、分组诊断与 Ranking 稳健性验证。暂不启动 KAR、SASRec、Hard Negative、Bootstrap、MovieLens-32M full training、7B 模型、大规模 LoRA 搜索或完整多 seed。

当前 100K 开发产物摘要：

```text
Y users: 943
N users: 902
Y samples: train 95867 / validation 1985 / test 2148
N samples: train 21995 / validation 902 / test 902
```

当前 100K 固定候选集摘要：

```text
valid candidates: 902 records
test candidates: 902 records
candidate_num: 5
files:
  data/candidates/movielens-100k/valid.jsonl
  data/candidates/movielens-100k/test.jsonl
```

当前 1M 主实验产物摘要：

```text
Y users: 6040
N users: 5675
Y samples: train 976284 / validation 12381 / test 11544
N samples: train 212725 / validation 5675 / test 5675
candidate_num: 5
valid candidates: 5675 records
test candidates: 5675 records
```

## M 多任务干扰诊断当前结论

M0/M1/M2 诊断已经完成，当前结果固化到：

```text
wiki/reports/m_multitask_interference_diagnosis_results.md
outputs/calibration/movielens-1m/m_diagnostics/threshold_calibration.md
```

诊断状态：

```text
M0: baseline，Y:N=200k:200k，max_steps=1500，已完成
M1: 延长训练，Y:N=200k:200k，max_steps=3000，已完成，当前最佳 M 诊断版本
M2: Y:N sampling ratio=2:1，已完成，未缓解干扰且损害 N
M3: 暂不启动
```

M1 的 validation best-F1 threshold 为 0.3208213008。应用到 test 后，M1 的 binary 表现为 AUC=0.7669、F1=0.7818、Accuracy=0.7029，已经接近 Y-K0；M1 的 ranking 表现为 HR@1=0.6950、NDCG@5=0.8674、MRR=0.8223，明显优于 M0 但仍低于 N-K0。

当前结论是：M0 的问题部分来自训练预算不足和阈值偏移；简单提高 Y 采样比例不是有效缓解方案。下一步优先做轻量 error analysis 和报告整理，不继续无目标长训练。

## Phase 1.5 当前入口

Phase 1.5 的执行顺序为：

```text
STEP A 仓库检查
STEP B 统一 binary 阈值报告
STEP C 分组 Error Analysis
STEP D candidate_num=20
STEP E candidate_num=50 可行性
STEP F 候选顺序稳健性
STEP G 总结
```

STEP A 已完成，结论见：

```text
wiki/reports/phase_1_5_step_a_repository_check.md
```

当前本地仓库没有 MovieLens-1M 全量云端 prediction 文件，因此正式分组分析需要先把云端 outputs 拉回本地，或将分析代码推送到 GitHub 后在云端运行。

当前 32M 本地 eval-only 产物摘要，已暂停作为当前主线：

```text
Y users: 200902
N users: 193491
Y samples: validation 314243 / test 285734
N samples: validation 193491 / test 193491
local_eval_only: true
```

32M 固定候选集摘要：

```text
valid candidates: 193491 records
test candidates: 193491 records
files:
  data/candidates/movielens-32m/valid.jsonl
  data/candidates/movielens-32m/test.jsonl
```

32M 本地未写完整 train JSONL；完整训练数据展开应在云服务器或更大磁盘环境中执行。MovieLens-32M Base validation/test 全量评测已在云端完成，但当前不再作为 MVP 主线。

本地开发使用：

```text
C:\Users\33967\AppData\Local\Programs\Python\Python312\python.exe
```

配置中的 Llama 模型路径只作为云服务器训练/推理时的 HuggingFace 模型 ID；本地开发不需要安装或加载模型权重。

## 目标 CLI 形态

以下命令是后续实现后的目标形态：

```bash
python -m src.data.build_step2 --config configs/experiment.yaml --dataset movielens-100k
python -m src.eval.candidate_sets --config configs/experiment.yaml --dataset movielens-100k
python -m src.inference.base_zero_shot --config configs/experiment.yaml --dataset movielens-100k --mode mock --limit 20

python -m src.data.build_step2 --config configs/experiment.yaml --dataset movielens-1m
python -m src.eval.candidate_sets --config configs/experiment.yaml --dataset movielens-1m
python -m src.inference.base_zero_shot --config configs/experiment.yaml --dataset movielens-1m --mode mock --limit 20

python -m src.data.build_step2 --config configs/experiment.yaml --dataset movielens-32m --eval-only
python -m src.eval.candidate_sets --config configs/experiment.yaml --dataset movielens-32m
python -m src.inference.base_zero_shot --config configs/experiment.yaml --dataset movielens-32m --mode mock --limit 20

python -m src.train.train_y --config configs/y.yaml
python -m src.train.train_n --config configs/n.yaml
python -m src.train.train_m --config configs/m.yaml
```

评测命令最终也应读取同一份固定配置和候选集：

```bash
python src/eval/summarize.py --config configs/experiment.yaml
```
