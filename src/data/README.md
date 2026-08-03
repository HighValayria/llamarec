# 数据层

本目录负责 STEP 2：把 MovieLens 原始文件转换为 MVP 共用的数据层产物。

当前 MVP 的主序列来源统一为 `full_sequence`。`positive_sequence` 只保留为辅助统计或 Phase 2 概念，不参与 MVP split，也不决定 N 的 target 或 history。

## 当前文件

- `build_step2.py`：STEP 2 端到端入口，只做数据处理，不加载模型、不训练。
- `config.py`：配置读取与路径解析。
- `preprocess.py`：MovieLens 读取、full_sequence 构造、辅助 positive_sequence 构造。
- `split.py`：基于 full_sequence 的 Y/N 分口径时间划分。
- `build_preference.py`：Y / Yes-No Preference 样本构造。
- `build_next_item.py`：N / Full-sequence Next-item train/validation/test 样本构造。
- `negative_sampling.py`：N 候选集随机负采样。
- `stats.py`：统计与人工检查产物。
- `STEP2_ACCEPTANCE.md`：进入 STEP 3 前的验收清单。

## 运行方式

先处理 MovieLens-100K，并人工检查输出样本：

```bash
python -m src.data.build_step2 --config configs/experiment.yaml --dataset movielens-100k
```

100K 产物检查通过后，再用同一入口处理 MovieLens-32M：

```bash
python -m src.data.build_step2 --config configs/experiment.yaml --dataset movielens-32m
```

本地磁盘有限时，32M 可以先生成评测包：

```bash
python -m src.data.build_step2 --config configs/experiment.yaml --dataset movielens-32m --eval-only
```

`--eval-only` 只写 Y/N validation/test、`split.json`、`stats.json` 和人工检查样本，不写完整 train JSONL。当前本地 32M 已采用该模式；完整 train 展开应在云服务器或更大磁盘环境中单独执行。

## 必需检查

- `max(history_timestamp) < target_timestamp`
- target interaction 不得出现在自身 history 输入中
- 同 timestamp 的其他 interaction 不得进入 target history
- 未来交互不得进入任何 prompt
- Base-Y / Y-K0 / M-Y 必须共享固定 Y validation/test
- Base-N / N-K0 / M-N 必须共享固定 N validation/test
- seed 42 必须复现相同处理结果
