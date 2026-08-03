# STEP 2 验收清单

进入 STEP 3 前必须完成这些检查。

## 原始输入

- `movielens-100k` 将 `u.data` 读作无表头 tab 分隔评分文件。
- `movielens-100k` 将 `u.item` 读作竖线分隔电影元数据。
- `movielens-32m` 将 `ratings.csv` 和 `movies.csv` 读作带表头 CSV 文件。
- 所有标准化后的评分记录都暴露 `user_id`、`movie_id`、`rating` 和 `timestamp`。

## 序列

- 每个用户的完整交互序列都按 `timestamp` 升序排列。
- 同一 `timestamp` 内的排序只用于稳定输出，不表示真实先后顺序。
- 每个用户的辅助正反馈序列只包含评分 `>= positive_rating_threshold` 的记录。
- 辅助正反馈序列只用于统计或 Phase 2，不参与 MVP split、N target 或 N history。

## 划分

- `timestamp tie` 不再导致整个用户退出数据集。
- Y split 按 timestamp bucket 划分：
  - 最后一个 timestamp bucket -> Y test targets
  - 倒数第二个 timestamp bucket -> Y validation targets
  - 更早 timestamp buckets -> Y train targets
- 同一 timestamp bucket 内可以有多个 Y target，它们共享同一份严格 history。
- N split 先枚举严格可确定的合法 next-item sample。
- 如果某个 N 位置的下一 timestamp bucket 有多个 interaction，则跳过该 N sample，而不是跳过整个用户。
- N 的最后一个合法 sample 为 test，倒数第二个合法 sample 为 validation，更早合法 sample 为 train。
- Y 与 N 不要求用户集合完全一致。

## 泄漏检查

- `max(history_timestamp) < target_timestamp`
- target interaction 不在自身 history 输入中。
- 同一 timestamp 的其他 interaction 不得进入 target history。
- 未来交互不出现在 prompt 输入中。
- `stats.json` 必须记录因合法 N sample 不足而从 N 任务跳过的用户数。

## 必需产物

- `data/processed/{dataset}/full_sequences.jsonl`
- `data/processed/{dataset}/positive_sequences.jsonl`
- `data/processed/{dataset}/split.json`
- `data/processed/{dataset}/preference_samples.jsonl`
- `data/processed/{dataset}/preference_train.jsonl`
- `data/processed/{dataset}/preference_valid.jsonl`
- `data/processed/{dataset}/preference_test.jsonl`
- `data/processed/{dataset}/next_item_train.jsonl`
- `data/processed/{dataset}/next_item_valid.jsonl`
- `data/processed/{dataset}/next_item_test.jsonl`
- `data/processed/{dataset}/stats.json`
- `data/processed/{dataset}/inspection_samples.md`

## 必需统计

- 总用户数。
- timestamp bucket size 分布：`size=1 / size=2 / size=3 / size>=4`。
- singleton timestamp bucket 占比。
- 每个用户可构造的合法 N sample 数。
- Y train/validation/test 用户数与样本数。
- N train/validation/test 用户数与样本数。
- 因合法 N sample 不足最终跳过的用户数。
- N 保留用户与跳过用户的 interaction 数、rating 分布等基本对比。

## 人工停止点

先运行 MovieLens-100K：

```bash
python -m src.data.build_step2 --config configs/experiment.yaml --dataset movielens-100k
```

生成 100K 产物后，先停下来人工检查至少 20 个样本，再运行 MovieLens-32M 处理。
