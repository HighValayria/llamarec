---
title: MovieLens 数据层
type: module
status: current
authority: normative
source: mixed
created: 2026-07-28
updated: 2026-08-02
last_verified: 2026-08-02
related_code:
  - task.md
  - README.md
  - configs/experiment.yaml
  - src/data/build_step2.py
  - src/data/config.py
  - src/data/preprocess.py
  - src/data/split.py
  - src/data/build_preference.py
  - src/data/build_next_item.py
  - src/data/negative_sampling.py
  - src/data/stats.py
  - wiki/architecture/mvp_experiment_contract.md
---

# MovieLens 数据层

## 范围

数据层将 MovieLens-100K、MovieLens-1M 和 MovieLens-32M 标准化为用户内 timestamp 升序的完整交互序列，并构造 Y/N/M 所需的训练、验证、测试产物。当前后续主线使用 MovieLens-1M；MovieLens-32M 暂停作为 Phase 2 或压力测试数据。

## 核心序列

MVP 的核心序列是：

```text
full_sequence
```

`full_sequence` 保留用户所有真实评分交互，不按评分过滤。

`positive_sequence` 可以输出为辅助统计，但必须明确：

```text
positive_sequence 不参与 MVP split；
positive_sequence 不决定 N target；
positive_sequence 不决定 N history。
```

## timestamp bucket 与严格历史

数据层按用户内 timestamp bucket 理解时间：

```text
bucket(t) = 该用户 timestamp == t 的所有 interaction
```

对任意 target：

```text
history = 所有 timestamp < target_timestamp 的 interaction
```

同一 timestamp 内的 interaction 不得互相作为 history，也不得用人为排序制造先后关系。

## Y 样本

Y 样本：

```text
History + Target -> Yes / No
```

同一 timestamp bucket 内可以有多个 Y target，它们共享同一份严格历史。

Y split 按 timestamp bucket 划分：

```text
最后一个 timestamp bucket       -> Y test targets
倒数第二个 timestamp bucket     -> Y validation targets
更早 timestamp buckets          -> Y train targets
```

## N 样本

N 样本：

```text
History + Candidate Set -> 实际发生的下一个 Item
```

N 只使用严格可确定的 next item。若下一 timestamp bucket 包含多个 interaction，则该位置没有单一 ground truth，跳过这个 N sample，不跳过整个用户。

合法 N samples 按时间划分：

```text
最后一个合法 N sample       -> N test
倒数第二个合法 N sample     -> N validation
更早合法 N samples          -> N train
```

若某用户合法 N samples 不足，则只从 N 任务中跳过该用户；不影响该用户是否能提供 Y 样本。

## 公平性

公平性按任务接口分别保证：

```text
Base-Y / Y-K0 / M-Y 共享同一 Y validation/test set。
Base-N / N-K0 / M-N 共享同一 N validation/test set。
```

Y/N 不要求完全相同用户集合。

## Multi-task 数据来源

M 的训练数据必须遵循：

```text
Raw interactions
-> chronological split
-> Y_train / N_train
-> multi-task training
```

任意已处于该用户 validation/test 时间范围的 interaction，不得以任何形式进入 M 训练数据。

## 输出统计

STEP 2 必须输出：

- timestamp bucket size 分布
- singleton timestamp bucket 占比
- 每个用户可构造合法 N sample 数
- Y/N train、validation、test 用户数与样本数
- 因合法 N sample 不足跳过的用户数
- 保留用户与跳过用户的 interaction 数、rating 分布对比

## 当前状态

STEP 2 代码已同步为新 timestamp tie 策略。MovieLens-100K 已完成开发产物；MovieLens-1M 已完成完整 STEP 2 产物与 STEP 3 固定候选集；MovieLens-32M 已生成本地 eval-only 评测包但不再作为当前主线。

当前 100K 开发产物摘要：

```text
Y users: 943
N users: 902
Y samples: train 95867 / validation 1985 / test 2148
N samples: train 21995 / validation 902 / test 902
```

MovieLens-100K 的人工检查已通过，STEP 3 固定候选集与指标已建立。

当前 1M 主实验产物摘要：

```text
Y users: 6040
N users: 5675
Y samples: train 976284 / validation 12381 / test 11544
N samples: train 212725 / validation 5675 / test 5675
valid candidates: 5675 records
test candidates: 5675 records
```

当前 32M eval-only 产物摘要：

```text
Y users: 200902
N users: 193491
Y samples: validation 314243 / test 285734
N samples: validation 193491 / test 193491
```

32M eval-only 只写 validation/test、`split.json`、`stats.json` 和人工检查样本，不写完整 train JSONL。完整 32M 训练文件应在云服务器或更大磁盘环境中生成。
