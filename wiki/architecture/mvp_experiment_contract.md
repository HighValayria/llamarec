---
title: MVP 实验契约
type: architecture
status: current
authority: normative
source: mixed
created: 2026-07-28
updated: 2026-08-03
last_verified: 2026-08-03
related_code:
  - task.md
  - README.md
  - configs/experiment.yaml
  - configs/y.yaml
  - configs/n.yaml
  - configs/m.yaml
  - wiki/current_state.md
  - wiki/modules/movielens_data_layer.md
---

# MVP 实验契约

## 范围

MVP 限定为 MovieLens K0 实验：

- Base
- Y-K0：Yes/No Preference Tuning
- N-K0：Full-sequence Next-item Tuning
- M-K0：Y + N Multi-task Tuning

MovieLens-100K 是开发与流程验证数据集。基于 100K 全链路预算实验和 32M 运行成本评估，当前正式 MVP 主实验数据集调整为 MovieLens-1M。MovieLens-32M 暂停作为 Phase 2 或压力测试数据，不作为当前主线。

KAR、SASRec、Hard Negative、Bootstrap、额外数据集、大规模超参数搜索、7B 模型和多 seed 实验均属于 Phase 2 或更晚阶段。

截至 2026-08-02，MovieLens-1M Base/Y/N/M 主结果已经完成，MVP 主链路关闭。下一阶段的唯一近期实验方向是 M-K0 多任务干扰诊断，而不是扩展新模块。

## 任务契约

Y 是显式偏好监督：

```text
History + Target -> Yes / No
```

N 是完整交互序列上的行为序列监督：

```text
History + Candidate Set -> 实际发生的下一个 Item
```

N 的 target 来自 full interaction sequence 中真实发生的下一次 interaction，不根据评分筛选。

M 使用同一个模型联合学习 Y 与 N，并分别以 M-Y 和 M-N 模式评测。

## 严格历史契约

对任意 target：

```text
history = 所有 timestamp < target_timestamp 的 interaction
```

`timestamp == target_timestamp` 的其他 interaction 不得视为 target 之前的历史。

同一 timestamp 内没有可观测先后顺序，不得使用 movie_id、文件顺序或其他人为规则构造先后关系。

timestamp tie 不再导致整个用户退出数据集。

## Y/N 数据划分契约

Y 与 N 不要求拥有完全相同的用户集合。

Y 的 validation/test 可按 timestamp bucket 划分：

```text
最后一个 timestamp bucket       -> Y test targets
倒数第二个 timestamp bucket     -> Y validation targets
更早 timestamp buckets          -> Y train targets
```

同一 bucket 内多个 Y target 共享同一份严格历史。

N 先构造严格可确定的合法 next-item 样本。如果下一 timestamp bucket 中包含多个 interaction，则该位置不能构造单一 next-item ground truth：

```text
跳过歧义 N sample，而不是跳过整个 user。
```

然后按每个用户的合法 N samples 时间顺序划分：

```text
最后一个合法 N sample       -> N test
倒数第二个合法 N sample     -> N validation
更早合法 N samples          -> N train
```

只有当用户不足以构造所需合法 N 样本时，才从 N 任务中跳过该用户。

## 公平评测契约

公平性按任务接口分别保证：

```text
Base-Y / Y-K0 / M-Y
必须使用同一固定 Y validation/test set。

Base-N / N-K0 / M-N
必须使用同一固定 N validation/test set。
```

不要为了强制 Y/N 用户完全一致而大量删除用户。

当前 `344/943` 用户方案只允许用于开发阶段 smoke test，不作为正式主实验数据方案。

## Multi-task Temporal Leakage

M 的训练数据必须先经过统一时间切分，再生成任务样本：

```text
Raw interactions
-> chronological split
-> Y_train / N_train
-> multi-task training
```

禁止先从完整数据生成全部 Y samples 和全部 N samples 后再混合训练。

只要某 interaction 已经位于该用户的 validation/test 时间范围，就不得以任何形式进入 M 的训练数据，包括 Y target、Y history、N target、N history 或其他派生训练样本。

训练顺序本身不定义是否泄漏。先训练全部 Y_train 再训练全部 N_train，只要二者都严格来自训练时间区域，就不是未来信息泄漏；但默认 M 训练仍采用 Y/N 样本混合或交替训练。

核心原则：

```text
先切时间，再构造任务，再混合训练。
```

## 统计契约

STEP 2 必须输出：

- 总用户数
- timestamp bucket size 分布：`size=1 / size=2 / size=3 / size>=4`
- singleton timestamp bucket 占比
- 每个用户可构造的合法 N sample 数
- Y train/validation/test 用户数与样本数
- N train/validation/test 用户数与样本数
- 因合法 N sample 不足最终跳过的用户数
- 保留用户与跳过用户的 interaction 数、rating 分布等基本对比

## 边界

Ranking 只作为 N 的评测方式之一，不再作为独立训练任务名称。

当前 MVP 不使用以下语义描述 N：

```text
下一个正反馈物品
下一个喜欢物品
下一个正反馈交互
```

Phase 2 可以保留消融设想：

```text
N-all：完整交互序列预测 next interaction
N-pos：仅正反馈序列预测 next positive interaction
```

但该消融不进入当前 MVP 实现范围。

## MVP 后诊断契约

当前 M-K0 在同一模型中保留了 Y 与 N 两类能力，但没有超过对应单任务模型。因此不得将现有 M-K0 结果描述为“已产生正迁移”或“全面超过单任务”。

第一轮 M 诊断已经完成：

```text
M0: Y:N=1:1, max_steps=1500，MVP baseline
M1: Y:N=1:1, max_steps=3000，当前最佳 M 诊断版本
M2: Y:N=2:1, max_steps=1500，未缓解干扰且损害 N
M3: 不启动
```

M1 在 validation best-F1 threshold 校准后，test AUC=0.7669、F1=0.7818、Accuracy=0.7029，接近 Y-K0；M1 的 test HR@1=0.6950，明显优于 M0 但仍低于 N-K0。

后续若继续训练 M，仍必须分别记录 Y validation 和 N validation，不能只记录混合总 loss。当前训练入口会在 mixed validation 外追加 `eval_y_*` 与 `eval_n_*` 指标，并支持用 `--task-ratio-y` / `--task-ratio-n` 设置采样比例。

任何 M 诊断仍必须遵守先 temporal split、再生成 Y_train/N_train、最后混合训练的无泄漏契约。
