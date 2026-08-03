---
title: 面向学习的当前工程讲解
type: guide
status: current
authority: descriptive
source: user-requested
created: 2026-08-01
updated: 2026-08-01
last_verified: 2026-08-01
related_code:
  - README.md
  - task.md
  - configs/experiment.yaml
  - configs/y.yaml
  - configs/n.yaml
  - configs/m.yaml
  - src/data/preprocess.py
  - src/data/split.py
  - src/data/build_preference.py
  - src/data/build_next_item.py
  - src/data/negative_sampling.py
  - src/data/build_step2.py
  - src/eval/candidate_sets.py
  - src/eval/ranking_metrics.py
  - src/eval/binary_metrics.py
  - src/inference/prompts.py
  - src/inference/base_zero_shot.py
  - src/train/preference_dataset.py
  - src/train/train_y.py
  - tests/test_split.py
  - tests/test_candidate_sets.py
  - tests/test_ranking_metrics.py
  - tests/test_y_training_data.py
---

# 面向学习的当前工程讲解

## 这份文档解决什么问题

当前工程已经从一个数据处理练习，推进成了一个包含数据层、评测层、推理层、训练层和 wiki 生命周期的 MVP 工作区。对学习者来说，最容易迷路的地方不是某一行代码，而是同时存在两条轴线：

```text
推进步骤轴：
STEP 1 -> STEP 2 -> STEP 3 -> STEP 4 -> STEP 5 -> STEP 6 -> STEP 7 -> STEP 8

任务功能轴：
Base / Y-K0 / N-K0 / M-K0
```

理解这个项目时，不要先盯着 Llama、QLoRA 或云端命令。先把数据如何变成任务样本、任务样本如何变成评测和训练输入看懂。

## 当前项目现状

截至 2026-08-01，项目目标是在 MovieLens 上构建一个可靠、可复现、可扩展的 LLM 推荐微调 MVP。当前只做 K0 版本：

```text
Base：不微调，直接 zero-shot 推理。
Y-K0：Yes/No preference tuning。
N-K0：full-sequence next-item tuning。
M-K0：Y + N multi-task tuning。
```

当前已经建立：

- STEP 1：实验配置和 MVP 边界已经固定。
- STEP 2：MovieLens 数据层已经实现，MovieLens-100K 已生成完整开发产物。
- STEP 3：固定候选集和 ranking/binary 指标已经实现。
- STEP 4：Base zero-shot 本地 mock dry-run、真实 scorer、batch 推理和增量输出已经实现。MovieLens-32M Base validation/test 全量评测已在云端完成，但尚未汇总进最终 `outputs/results.csv`。
- STEP 5：Y-K0 训练代码链路已经实现，MovieLens-100K smoke training 已在云端完成，loss 和 validation loss 均下降。adapter reload check 暴露过 tokenizer 输出兼容问题，当前代码已修复并提供 `--reload-only` 补验入口。

当前尚未完成：

- MovieLens-32M Base 全量结果尚未汇总进最终 `outputs/results.csv`。
- Y-K0 尚未完成正式训练、统一评测和 reload 修复后的云端补验。
- N-K0 训练尚未实现。
- M-K0 多任务训练尚未实现。
- STEP 8 统一结果表和 error analysis 尚未实现。

当前 100K 数据产物摘要：

```text
Y users: 943
N users: 902
Y samples: train 95867 / validation 1985 / test 2148
N samples: train 21995 / validation 902 / test 902
```

## 先建立一个总图

这个项目的核心数据流是：

```text
MovieLens 原始评分
-> full_sequence 用户完整交互序列
-> timestamp bucket split
-> Y 样本和 N 样本
-> 固定 candidate set
-> Base zero-shot / Y-K0 / N-K0 / M-K0
-> binary metrics / ranking metrics
```

更具体地说：

```text
data/raw/ml-100k/u.data
data/raw/ml-100k/u.item
  -> src/data/preprocess.py
  -> full_sequences.jsonl / positive_sequences.jsonl
  -> src/data/split.py
  -> split.json
  -> src/data/build_preference.py
  -> preference_train/valid/test.jsonl
  -> src/data/build_next_item.py
  -> next_item_train/valid/test.jsonl
  -> src/eval/candidate_sets.py
  -> data/candidates/{dataset}/valid.jsonl
  -> data/candidates/{dataset}/test.jsonl
```

## 目录怎么读

先按这个顺序看目录：

```text
configs/
  实验契约。决定数据路径、任务名、候选数、history 长度、模型名和输出路径。

src/data/
  STEP 2 数据层。负责把 MovieLens 原始文件变成 Y/N 样本。

src/eval/
  STEP 3 评测层。负责固定候选集、HR/NDCG/MRR、AUC/F1/Accuracy。

src/inference/
  STEP 4 推理层。负责 Base zero-shot prompt、mock scorer、real scorer 和 prediction 输出。

src/train/
  STEP 5 训练层。当前只实现 Y-K0。

tests/
  用小样本保护关键语义，尤其是无泄漏、候选集、指标和 loss mask。

wiki/
  项目知识库。current_state 看当前状态，modules 看模块语义，guides 看流程。
```

## STEP 1：固定实验配置

STEP 1 的目的不是训练模型，而是先把实验边界固定住。主要文件是：

```text
configs/experiment.yaml
configs/y.yaml
configs/n.yaml
configs/m.yaml
```

`configs/experiment.yaml` 是统一契约。它规定：

- 开发数据集是 `movielens-100k`。
- 正式 MVP 数据集是 `movielens-32m`。
- MovieLens-100K 原始评分路径是 `data/raw/ml-100k/u.data`。
- MovieLens-100K 电影元数据路径是 `data/raw/ml-100k/u.item`。
- 正反馈阈值是 `rating >= 4`。
- history 最大长度是 `10`。
- N 候选数是 `5`，也就是 1 个真实 next item 加 4 个随机负候选。
- 当前 MVP 不加入 KAR、SASRec、hard negative、多 seed、7B 模型等扩展。

这一层的学习重点是：配置文件不是摆设。后续每一步都应该读同一份配置，避免数据路径、候选数、seed 或任务语义各写各的。

## STEP 2：构建 MovieLens 数据层

STEP 2 是当前项目最核心、也最值得先学懂的部分。入口是：

```bash
python -m src.data.build_step2 --config configs/experiment.yaml --dataset movielens-100k
```

它做五件事：

```text
1. 读取 MovieLens 原始评分和电影标题。
2. 为每个用户构造完整时间序列。
3. 按 timestamp bucket 做无泄漏切分。
4. 构造 Y 样本和 N 样本。
5. 写出统计和人工检查样本。
```

### 2.1 原始数据读取

`src/data/preprocess.py` 负责读取两种 MovieLens 格式：

```text
MovieLens-100K:
  ratings: u.data，tab 分隔，无表头
  movies: u.item，pipe 分隔，latin-1 编码

MovieLens-32M:
  ratings: ratings.csv
  movies: movies.csv
```

读取后每条评分会变成统一字段：

```text
user_id
movie_id
rating
timestamp
title
```

### 2.2 full_sequence 和 positive_sequence

项目会构造两个序列：

```text
full_sequence:
  保留用户所有真实评分交互，评分 1 到 5 都保留。

positive_sequence:
  只保留 rating >= 4 的交互。
```

当前 MVP 的主序列永远是 `full_sequence`。`positive_sequence` 只用于辅助统计和 future work，不参与 MVP split，不决定 N target，也不决定 N history。

这是很重要的语义边界：N 任务预测的是下一次真实交互，不是下一部喜欢的电影。

### 2.3 timestamp bucket 和严格 history

项目不直接按行号切时间，而是按 timestamp bucket 理解用户时间：

```text
bucket(t) = 该用户 timestamp == t 的所有 interaction
```

严格历史规则是：

```text
history = 所有 timestamp < target_timestamp 的 interaction
```

所以：

- `timestamp == target_timestamp` 的其他电影不能放进 history。
- 同一 timestamp 内没有可观测先后顺序。
- 不能用 `movie_id`、文件顺序或排序后位置假装同一 timestamp 有先后。
- timestamp tie 不再导致整个用户被删掉。

代码里为了输出稳定会按 `(timestamp, movie_id)` 排序，但 `movie_id` 只用于稳定输出，不代表真实时间。

### 2.4 Y 样本怎么构造

Y 是偏好判断：

```text
History + Target movie -> Yes / No
```

标签规则是：

```text
rating >= 4 -> Yes
rating < 4  -> No
```

Y 按 timestamp bucket 切分：

```text
最后一个 timestamp bucket       -> test
倒数第二个 timestamp bucket     -> validation
更早 timestamp buckets          -> train
```

如果同一个 timestamp bucket 中有多个 target，它们都可以成为 Y 样本，并共享同一份严格 history。

当前 Y 产物：

```text
data/processed/movielens-100k/preference_samples.jsonl
data/processed/movielens-100k/preference_train.jsonl
data/processed/movielens-100k/preference_valid.jsonl
data/processed/movielens-100k/preference_test.jsonl
```

### 2.5 N 样本怎么构造

N 是行为序列预测：

```text
History + Candidate Set -> 实际发生的下一个 Item
```

N 的 ground truth 是 full sequence 中真实发生的下一次 interaction，不按评分过滤。低评分电影也可以是正确答案，因为这里评测的是“下一次行为”，不是“最喜欢”。

N 只构造严格可确定的 next-item 样本：

```text
如果下一个 timestamp bucket 只有 1 个 interaction：
  可以构造 N 样本。

如果下一个 timestamp bucket 有多个 interaction：
  无法知道其中哪一个先发生。
  跳过这个 N sample。
  不跳过整个用户。
```

每个用户先枚举所有合法 N 样本，再切分：

```text
最后一个合法 N sample       -> test
倒数第二个合法 N sample     -> validation
更早合法 N samples          -> train
```

当前 N 产物：

```text
data/processed/movielens-100k/next_item_train.jsonl
data/processed/movielens-100k/next_item_valid.jsonl
data/processed/movielens-100k/next_item_test.jsonl
```

一条 N 样本包含：

```text
history
target
candidate_movie_ids
ground_truth_movie_id
ground_truth_index
label
label_set
```

如果 `candidate_movie_ids = ["1082", "1027", "94", "1415", "1337"]`，真实 next item 是 `"94"`，那么：

```text
ground_truth_index = 2
label = "C"
```

### 2.6 负采样语义

`src/data/negative_sampling.py` 定义当前负采样：

```text
负候选池 = 全部电影 - 当前样本的 ground truth item
```

当前允许采到用户历史中看过的电影，也允许采到用户喜欢过的电影。原因是这些“负候选”只表示：

```text
不是本样本真实下一次交互的候选
```

它们不表示：

```text
用户不喜欢这些电影
```

这一点非常关键。不要把 N 的负候选解释成显式负反馈。

## STEP 3：固定候选集和指标

STEP 3 的入口是：

```bash
python -m src.eval.candidate_sets --config configs/experiment.yaml --dataset movielens-100k
```

它读取：

```text
data/processed/{dataset}/next_item_valid.jsonl
data/processed/{dataset}/next_item_test.jsonl
```

然后写出正式评测共用的固定候选集：

```text
data/candidates/{dataset}/valid.jsonl
data/candidates/{dataset}/test.jsonl
```

为什么需要固定候选集？因为后续 Base-N、N-K0、M-N，以及 Y-K0 的 ranking mode，都必须面对同一批候选、同一候选顺序、同一正确答案位置。否则模型之间的 ranking 指标不可比。

当前 ranking 指标：

```text
HR@1
HR@5
NDCG@5
MRR
```

对于 5 个候选，HR@5 通常会是 1，因为真实答案一定在候选集中。真正有区分度的是 HR@1、NDCG@5 和 MRR。

当前 binary 指标：

```text
AUC
F1
Accuracy
```

Binary 指标服务 Y，ranking 指标服务 N 或候选排序模式。

## STEP 4：Base LLM zero-shot

Base 不训练。它只把 STEP 2/3 的样本渲染成 prompt，然后让模型输出概率。

入口是：

```bash
python -m src.inference.base_zero_shot --config configs/experiment.yaml --dataset movielens-100k --mode mock --limit 20
```

本地主要用 `--mode mock` 检查：

- 输入文件能否读到。
- prompt 是否符合任务语义。
- target rating 或 candidate rating 是否被泄漏。
- prediction jsonl 是否能写出。
- metrics 是否能算。

云端用 `--mode real` 加载 `meta-llama/Llama-3.2-3B-Instruct`。真实 scorer 对 Y 输出：

```text
P(Yes), P(No)
```

对 N 输出：

```text
P(A), P(B), P(C), P(D), P(E)
```

当前代码支持 `--batch-size` / `--batch_size`，real 模式下单 token 答案会走 batch logits 路径，prediction 文件按 batch 增量写出。

## STEP 5：Y-K0 训练

当前训练层只实现了 Y-K0。入口是：

```bash
python -m src.train.train_y --config configs/y.yaml --dataset movielens-100k
```

Y-K0 读取：

```text
data/processed/{dataset}/preference_train.jsonl
data/processed/{dataset}/preference_valid.jsonl
```

训练目标是让模型在 prompt 之后输出 `Yes` 或 `No`。关键实现位于 `src/train/preference_dataset.py`：

```text
prompt tokens: label = -100
answer tokens: label = token id of Yes/No
padding tokens: label = -100
```

也就是只在答案 token 上计算 loss，不让模型为复述 prompt 付出训练损失。

`PreferenceDataCollator` 做右侧 padding：

```text
input_ids       -> 用 pad_token_id 补齐
attention_mask  -> 真实 token 为 1，padding 为 0
labels          -> padding 位置为 -100
```

这一块对学习最重要，因为它解释了语言模型监督微调里 `input_ids`、`attention_mask` 和 `labels` 的关系。

当前 Y-K0 MovieLens-100K smoke training 已在云端跑通，loss 与 validation loss 均下降。训练后 reload check 暴露过 tokenizer 输出兼容问题，代码已修复，并提供：

```bash
python -m src.train.train_y \
  --config configs/y.yaml \
  --dataset movielens-100k \
  --reload-only \
  --adapter-dir outputs/y/movielens-100k/smoke_100k/adapter
```

## STEP 6：N-K0 尚未实现

`configs/n.yaml` 当前只是任务配置外壳，标记为 `not_implemented`。后续 N-K0 应该读取：

```text
data/processed/{dataset}/next_item_train.jsonl
```

训练目标会是：

```text
History + Candidate Set -> A/B/C/D/E
```

如果继续用 LLM，就和 Y-K0 类似，只在答案 token `A/B/C/D/E` 上计算 loss。

如果先做学习复刻，建议不要一开始用 LLM。可以先用一个小的 ID 模型：

```text
history item ids -> sequence encoder -> user state
candidate item ids -> candidate embeddings
scores = dot(user_state, candidate_embedding)
loss = CrossEntropy(scores, ground_truth_index)
```

这就是新建复刻项目要走的简化路线。

## STEP 7：M-K0 尚未实现

M-K0 是同一个模型联合学习 Y 和 N：

```text
Y batch
N batch
Y batch
N batch
...
```

但多任务训练必须先切时间，再构造任务，再混合训练：

```text
Raw interactions
-> chronological split
-> Y_train / N_train
-> multi-task training
```

禁止先从完整数据生成所有 Y/N 样本再混合，因为那样可能把用户 validation/test 时间范围的信息泄漏进训练。

## STEP 8：统一评测和错误分析尚未实现

最终结果应汇总到：

```text
outputs/results.csv
```

并至少比较：

```text
Base-Y vs Y-K0 vs M-Y
Base-N vs N-K0 vs M-N
```

当前还没有完成统一结果表和 error analysis。

## 学习时先抓住这 6 个概念

### 1. full_sequence

完整用户评分序列。N 的 target 和 history 都来自它，不按评分过滤。

### 2. strict history

任何 target 的 history 都只能包含更早 timestamp 的交互：

```text
history_timestamp < target_timestamp
```

这是防止时间泄漏的核心。

### 3. timestamp tie

同一 timestamp 内不能制造顺序。Y 可以保留同 timestamp 多个 target，N 遇到下一个 bucket 多交互时跳过该 sample。

### 4. negative sampling

N 的随机负候选只排除当前 ground truth。负候选不等于用户不喜欢。

### 5. padding 和 mask

训练 batch 要补齐长度。真实 token 的 `attention_mask` 是 1，padding 是 0。语言模型训练里不该算 loss 的 token，`labels` 应该设为 `-100`。

### 6. HR/NDCG

Ranking 指标看真实 next item 在候选集里的排名：

```text
rank = 1 -> HR@1=1, NDCG@5=1, MRR=1
rank = 3 -> HR@1=0, HR@5=1, NDCG@5=1/log2(4), MRR=1/3
```

## 最适合你现在复刻的路线

为了学习，不建议直接复刻整个 LLM MVP。建议先只复刻 N 任务的简化 ID 模型版本：

```text
1. 读取 MovieLens-100K 原始 u.data / u.item。
2. 按用户构造 timestamp 升序 full_sequence。
3. 按 timestamp bucket 枚举合法 next-item 样本。
4. 每个用户最后一个合法样本作 test，倒数第二个作 validation，其余作 train。
5. 把 movie_id 映射成连续 item_id，0 作为 padding。
6. 对 history 截断到 max_len，并 padding 成固定长度。
7. 为每条样本采 4 个随机负候选，加 1 个真实 target。
8. 用 embedding + pooling 或 GRU 编码 history。
9. 用 dot product 给 5 个候选打分。
10. 用 CrossEntropy(scores, ground_truth_index) 训练。
11. 用 HR@1、HR@5、NDCG@5、MRR 评估。
```

这条线会覆盖你提到的关键点：

```text
数据集构造
历史序列
padding
mask
negative sampling
训练 loss
HR/NDCG 评估
```

同时它不会引入 LLM prompt、QLoRA、chat template、云端显存、adapter reload 等额外复杂度。

## 推荐阅读顺序

如果你想逐步看懂当前工程，建议按这个顺序：

```text
1. wiki/current_state.md
2. 本文档
3. configs/experiment.yaml
4. src/data/preprocess.py
5. src/data/split.py
6. src/data/build_next_item.py
7. src/data/negative_sampling.py
8. src/eval/candidate_sets.py
9. src/eval/ranking_metrics.py
10. src/train/preference_dataset.py
```

先不要读 `src/inference/scoring.py` 和完整 `src/train/train_y.py` 的云端细节。那些是后续工程化复杂度，不是理解推荐任务的第一入口。
