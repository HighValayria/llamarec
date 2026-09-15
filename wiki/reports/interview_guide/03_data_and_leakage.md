---
title: "03 data and leakage"
type: report
status: current
authority: descriptive
source: agent
created: 2026-08-24
updated: 2026-08-24
last_verified: 2026-08-24
related_code:
  - configs/experiment.yaml
  - src/data/preprocess.py
  - src/data/build_step2.py
  - src/data/split.py
  - src/data/build_preference.py
  - src/data/build_next_item.py
  - src/eval/candidate_sets.py
---

# 03 Data And Leakage

## 一句话

[FACT] LlamaRec 的数据协议核心是：所有 prompt history 都只能来自 `timestamp < target_timestamp` 的 full-sequence interactions；Y 和 N 可以有不同 split 形态，但都不能让 target、同 timestamp item 或 future item 进入 prompt。

## 数据从哪里来

MovieLens-1M:

```text
ratings.dat -> user_id / movie_id / rating / timestamp
movies.dat  -> movie_id / title / genres
```

Amazon Musical Instruments:

```text
interaction CSV -> user_id / parent_asin / rating / timestamp
metadata parquet -> parent_asin / title
```

[FACT] Amazon 不使用 review text、description、brand/category/price、images 或外部商品知识。

## full_sequence 是主序列

代码：`src/data/preprocess.py`

[FACT] `build_user_sequences()` 输出：

```text
full_sequences: all interactions sorted by (timestamp, movie_id)
positive_sequences: rating >= threshold 的辅助序列
```

面试说法：

> full_sequence 是所有 Y/N/M 的主数据源；positive_sequence 只是统计辅助，不决定 N target。

## split 的核心规则

代码：`src/data/split.py`

```text
history = all interactions with timestamp < target_timestamp
```

[FACT] split 方法名是 `timestamp_bucket_strict_history_per_task`。

Y split:

```text
last timestamp bucket        -> test
second-last timestamp bucket -> validation
earlier buckets              -> train
```

N split:

```text
legal next-item samples 中最后一个        -> test
倒数第二个 legal next-item sample          -> validation
更早 legal samples                         -> train
```

## same timestamp policy

Y:

```text
同 timestamp bucket 内多个 target 可以共享同一段 strict history
```

N:

```text
如果 next timestamp bucket 有多个 item，无法确定唯一 next item
只跳过这个 ambiguous N sample，不跳过整个 user
```

[INTERPRETATION] 这样既防泄漏，又不因为局部 timestamp tie 浪费整个用户序列。

## How We Prevent Leakage

### 1. 不允许 `timestamp <= target`

错误：

```text
history includes timestamp <= target_timestamp
```

风险：

```text
target 本身或同 timestamp item 可能进入 history
```

正确：

```text
history timestamp < target timestamp
```

### 2. 不先全量构造再随便 split

风险：

```text
如果先把所有 target 都构造成样本，再随机 split，train prompt 可能含有 validation/test 之后的信息
```

当前做法：

```text
先按用户内 timestamp bucket 定义 train/validation/test target 区域
再构造 Y/N samples
```

### 3. M 先 split 再 mix

[FACT] M1 的 Y/N records 来自已经构造好的 Y train 和 N train。

风险：

```text
如果先把 Y/N 混在一起再切分，可能让同一用户后续 target 泄漏到另一个任务的 train prompt
```

### 4. target 不在自身 history

[FACT] `validate_split_no_leakage()` 和 Y/N sample validators 都检查 target identity 不在 history identities 中。

### 5. candidate files 固定

[FACT] validation/test candidate jsonl 生成一次，Base/Y/N/M/SASRec 共用。

风险：

```text
如果每个模型各自重新采 negatives，指标差异可能来自候选难度不同
```

### 6. validation threshold 不能从 test 调

[INTERPRETATION] binary F1 threshold 必须从 validation 决定，再应用到 test；否则 test label 被用于调参。

## negative candidate 从哪里采

Random-k5:

```text
all_items - {current ground truth item}
```

[FACT] 不排除用户看过的其他 item，不按正反馈过滤。

PopMatch-k5:

```text
all_items - {current ground truth item}
-> 按 popularity 接近 target 排序
-> 从 hard pool 随机采 negatives
```

边界：

[FACT] 当前 PopMatch 是 fixed-candidate evaluation protocol，不是 hard-negative training。

## 面试红线

不要说：

```text
N 的 negative 表示用户不喜欢
N target 是 next positive item
same timestamp 可以按 movie_id 顺序当真实顺序
```

要说：

```text
N negative 只是非当前 ground truth
N target 是下一次真实 interaction
movie_id tie-breaker 只保证稳定输出，不代表真实顺序
```
