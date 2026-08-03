# 基于 LoRA 的 Y/N/M 多任务 LLM 推荐系统 MVP 任务书

## 一、当前 MVP 范围与完成状态

当前 MVP 只包含：

```text
Base

Y-K0：
Yes/No Preference Tuning

N-K0：
Full-sequence Next-item Tuning

M-K0：
Y + N Multi-task Tuning
```

在得到可信主结果前，不纳入 KAR、SASRec、Hard Negative、Bootstrap、第二数据集、7B 模型、大规模超参数搜索或多 seed 实验。

MovieLens-100K 用于开发与 smoke test。基于 100K 全链路结果和 32M 运行成本评估，当前后续 MVP 主实验数据集调整为 MovieLens-1M；MovieLens-32M 暂停作为 Phase 2 或压力测试数据，不作为当前主线。

截至 2026-08-02，MovieLens-1M 上的 Base / Y-K0 / N-K0 / M-K0 主链路已经完成，STEP 1-8 均已跑通并生成结构化结果、主结果报告和基础 error analysis。原“实现 Y/N/M 主流程”的 MVP 任务关闭，后续工作重心从验证 Y/N/M 是否有效，调整为诊断并缓解 Y/N 多任务干扰。

当前不再自动扩展到 KAR、SASRec、Hard Negative、Bootstrap、MovieLens-32M full training、7B 模型、大规模 LoRA 搜索或完整多 seed。M-K0 多任务干扰诊断第一轮已经完成，当前进入 Phase 1.5：实验口径统一、分组诊断与 Ranking 稳健性验证。

Phase 1.5 先复用已有结果，提高结论可信度和解释力，不重新训练新模型。执行顺序为：

```text
STEP A：仓库检查
STEP B：统一 binary 阈值报告
STEP C：分组 Error Analysis
STEP D：candidate_num=20
STEP E：candidate_num=50 可行性
STEP F：候选顺序稳健性
STEP G：总结
```

当前 STEP A 已完成，检查结论记录在 `wiki/reports/phase_1_5_step_a_repository_check.md`。

## 二、统一数据来源

MVP 的核心数据来源是：

```text
full_sequence
```

`full_sequence` 是用户完整评分交互序列，按用户内 `timestamp` 升序排列，保留每一次真实评分交互，不按评分高低过滤。

辅助序列：

```text
positive_sequence
```

`positive_sequence` 只作为辅助统计或 Phase 2 概念保留，必须满足：

```text
positive_sequence 不参与 MVP split；
positive_sequence 不决定 N target；
positive_sequence 不决定 N history。
```

## 三、严格历史与 timestamp tie 规则

对任意 target：

```text
history = 所有 timestamp < target_timestamp 的 interaction
```

禁止将 `timestamp == target_timestamp` 的其他 interaction 视为 target 之前的历史。

同一 timestamp 内没有可观测的先后顺序，因此不得使用 `movie_id`、文件顺序、排序后的行号或其他人为规则构造先后关系。

timestamp tie 不再导致整个用户退出数据集。只有具体样本无法定义合法监督信号时，才跳过该样本或该任务下的该用户。

当前曾生成的 `344/943` 用户方案只允许用于开发阶段 smoke test，不作为正式主实验数据方案。

## 四、Y 任务：Yes/No Preference Prediction

Y 表示偏好判断：

```text
History + Target -> Yes / No
```

标签由 target 的评分决定：

```text
rating >= positive_rating_threshold -> Yes
rating < positive_rating_threshold  -> No
```

Y 的合法样本规则：

```text
history = timestamp < target_timestamp 的所有 interaction
target  = full_sequence 中的任意 interaction
```

同一 timestamp 可以存在多个 Y target。这些 target 共享同一份严格历史：

```text
history = timestamp < target_timestamp
```

因此 timestamp tie 本身不影响 Y 样本合法性，不因 tie 删除用户。

Y 的 validation/test 建议按 timestamp bucket 划分：

```text
最后一个 timestamp bucket       -> Y test targets
倒数第二个 timestamp bucket     -> Y validation targets
更早 timestamp buckets          -> Y train targets
```

同一 bucket 中的多个 interaction 都进入对应 split，并共享同一份严格历史。

## 五、N 任务：Full-sequence Next-item Prediction

N 表示行为序列预测：

```text
History + Candidate Set -> 实际发生的下一个 Item
```

N 的 ground truth 来自 `full_sequence` 中真实发生的下一次 interaction，不根据评分筛选。因此低评分 item 仍然可以是 N 的 ground truth。

N 要求 ground truth 是“严格可确定的下一个 interaction”。

构造 N 样本时，先按用户 timestamp bucket 处理：

```text
history = 所有 timestamp < target_timestamp 的 interaction
target_bucket = 某个后续 timestamp bucket
```

如果 `target_bucket` 中只有一个 interaction，则该 interaction 是严格可确定的 next item，可以构造合法 N sample。

如果 `target_bucket` 中包含多个 interaction，则无法知道这些 interaction 的内部真实顺序，该位置不能构造单一 next-item ground truth：

```text
跳过这个存在歧义的 N sample，
而不是跳过整个 user。
```

先从每个用户完整时间序列中构造所有严格可确定的合法 N samples，再按时间选择：

```text
最后一个合法 N sample       -> N test
倒数第二个合法 N sample     -> N validation
更早合法 N samples          -> N train
```

只有当某用户不足以构造所需合法 N 样本时，才从 N 任务中跳过该用户。

## 六、Y/N 固定评测集与公平比较口径

Y 和 N 不要求拥有完全相同的用户集合。

公平性要求改为：

```text
Base-Y / Y-K0 / M-Y
必须使用同一固定 Y validation/test set。

Base-N / N-K0 / M-N
必须使用同一固定 N validation/test set。
```

不要为了强制 Y/N 用户完全一致而大量删除用户。

N 任务仍使用固定候选集评测：

```text
1 ground-truth next item
+
若干随机候选 item
```

候选间不构造完整偏序。模型读取：

```text
P(A), P(B), P(C), ...
```

作为候选分数，因此继续保留 HR、NDCG、MRR 等 Ranking Evaluation。

这些 ranking metrics 衡量模型是否把真实 next interaction 排在候选集前面，不直接表示候选 item 的喜欢程度。

## 七、M 任务：Y + N Multi-task

M 使用同一个模型联合学习：

```text
Y：
P(Like | History, Item)

N：
P(Next Item | History, Candidate Set)
```

训练完成后必须分别评测：

```text
M-Y：
Yes/No preference prediction

M-N：
Full-sequence next-item prediction
```

不要只选择其中表现更好的模式作为 M 的唯一结果。

## 八、Multi-task Temporal Leakage 规范

多任务 M 的训练数据必须先经过统一时间切分，再生成任务样本：

```text
Raw interactions
-> chronological split
-> Y_train / N_train
-> multi-task training
```

禁止：

```text
先从完整数据生成全部 Y samples
先从完整数据生成全部 N samples
-> 再混合训练
```

因为这样可能导致一个任务的训练样本包含另一个任务 validation/test target 之后的用户行为。

对于任意用户，只要某 interaction 已经位于该用户的 validation/test 时间范围，就不得以任何形式进入 M 的训练数据，包括：

```text
Y target
Y history 中的未来 interaction
N target
N history 中的未来 interaction
其他由该 interaction 派生出的训练样本
```

M 的训练必须满足：

```text
Y_train 和 N_train
均只来自各用户训练时间区域。
```

训练顺序本身不定义是否泄漏。例如：

```text
先训练全部 Y_train
再训练全部 N_train
```

只要两者都严格来自训练时间区域，不属于未来信息泄漏；但这种 sequential training 可能产生灾难性遗忘和任务顺序偏差，因此不作为 M 的默认训练方式。

M 默认仍采用 Y/N 样本混合或交替训练，例如：

```text
Y batch
N batch
Y batch
N batch
...
```

核心原则是：

```text
先切时间，再构造任务，再混合训练。
```

而不是：

```text
先构造各任务全部样本，再考虑时间切分。
```

## 九、必须输出的数据统计

STEP 2 必须保存以下统计：

```text
总用户数

timestamp bucket size 分布：
size=1 / size=2 / size=3 / size>=4

singleton timestamp bucket 占比

每个用户可构造的合法 N sample 数

Y train/validation/test 用户数与样本数

N train/validation/test 用户数与样本数

因“合法 N sample 不足”最终跳过的用户数

保留用户与跳过用户的 interaction 数、rating 分布等基本对比
```

## 十、当前 MVP 主结论

MovieLens-1M 主结果表明，Y 与 N 两类 recommendation tuning 均已验证有效：

```text
Y-K0:
Base test AUC 0.6205 -> Y-K0 test AUC 0.7691

N-K0:
Base test HR@1 0.3167 -> N-K0 test HR@1 0.7189
```

Y 与 N 学习的是不同监督语义：

```text
Y: P(Like | History, Item)
N: P(Next Item | History, Candidate Set)
```

Y-K0 虽然显著提升 binary preference prediction，但没有提升 next-item ranking：

```text
Base HR@1 = 0.3167
Y-K0 HR@1 = 0.3048
```

因此不能使用 Y 的 `P(Yes)` 替代专门的 N candidate score。

当前 M-K0 是能力折中，而不是超过单任务的正迁移：

```text
M-K0 test AUC  = 0.7234 < Y-K0 test AUC  0.7691
M-K0 test HR@1 = 0.6717 < N-K0 test HR@1 0.7189
```

允许的表述是：

```text
M-K0 在同一个模型中同时获得了偏好判断能力和序列预测能力，
但当前联合训练存在多任务干扰，没有超过各单任务模型。
```

禁止写成：

```text
M 已经产生正迁移
M 超过了单任务模型
Y 与 N 联合后全面提升
```

M-Y 存在明显 Yes 偏置。MovieLens-1M test error analysis：

```text
Base: FP=3157 / FN=1383 / Mean P(Yes|Yes)=0.6878 / Mean P(Yes|No)=0.5893
Y-K0: FP=2413 / FN=918  / Mean P(Yes|Yes)=0.6891 / Mean P(Yes|No)=0.4723
M-K0: FP=3986 / FN=156  / Mean P(Yes|Yes)=0.6927 / Mean P(Yes|No)=0.6054
```

当前 M-Y 的核心问题是 FN 很低、FP 很高、No 样本的 `P(Yes)` 过高。

当前 `candidate_num = 5`，因此 HR@5 没有区分度。主结论应依据 HR@1、NDCG@5、MRR、mean margin 和 rank distribution。后续可以在不重新训练模型的前提下，优先评估重新生成 `candidate_num = 20` 或 `50` 的固定 validation/test candidate set 并重新推理。

## 十一、MVP 开发顺序（已完成）

当前 MVP 已按以下顺序完成：

```text
STEP 1
固定实验配置
    ↓
STEP 2
MovieLens full_sequence 数据底座
    ↓
STEP 3
固定测试 Candidate Set + Ranking Metrics
    ↓
STEP 4
Base LLM Zero-shot
    ↓
STEP 5
Y-K0
    ↓
STEP 6
N-K0
    ↓
STEP 7
M-K0
    ↓
STEP 8
统一评测 + Error Analysis
```

后续若重新生成数据或候选集，仍禁止跳过 STEP 1-3 直接开始正式微调。

## 十二、M 多任务干扰诊断

M0/M1/M2 诊断已经完成。当前不再启动 M3，也不进入 KAR、SASRec、Hard Negative、Bootstrap、32M full training、7B、多 seed 或大规模超参数搜索。

诊断矩阵：

| 实验 | 定义 | 目的 | 状态 |
|---|---|---|---|
| M0 | Y:N train pool = 200k:200k，max_steps = 1500 | MovieLens-1M MVP baseline | 已完成 |
| M1 | Y:N train pool = 200k:200k，max_steps = 3000 | 判断 M-K0 是否只是尚未充分收敛 | 已完成，当前最佳 M 诊断版本 |
| M2 | Y:N sampling ratio = 2:1，200k Y + 100k N，max_steps = 1500 | 检验 M-Y Yes 偏置和 AUC 损失是否来自任务采样或梯度失衡 | 已完成，未缓解干扰且损害 N |
| M3 | Y:N sampling ratio = 1:2 | 原计划可选 N-heavy 对照 | 不启动 |

M1 的核心结果：

```text
默认 0.5 threshold:
M1 test AUC  = 0.7669
M1 test HR@1 = 0.6950

validation best-F1 threshold = 0.3208213008
calibrated test F1 = 0.7818
calibrated test Accuracy = 0.7029
```

M1 在校准后基本恢复 Y-K0 的 preference prediction，同时 M-N 明显优于 M0 但仍低于 N-K0。M2 表明简单提高 Y 采样比例不是有效缓解方案。

统一比较表至少包括：

```text
Experiment
Y:N ratio
max_steps
Y AUC / F1 / Acc
Y FP / FN
Mean P(Yes) for Yes
Mean P(Yes) for No
N HR@1 / NDCG@5 / MRR
N mean margin
```

后续若继续做 M 训练，仍必须分别记录 Y validation 和 N validation，不能只记录混合总 loss。诊断时需要区分：

```text
未收敛：增加 steps 后 Y/N 同时改善
任务失衡：调整采样或 loss 权重后，一个任务明显恢复
梯度或能力冲突：无论怎样平衡，一个任务改善都会稳定损害另一个任务
灾难性遗忘：按任务顺序训练时，后一个任务覆盖前一个任务
未来信息泄漏：训练样本越过 validation/test 时间边界
```

M 默认仍采用混合或交替训练，不采用“先完整训练 Y，再完整训练 N”作为主多任务方法。如果后续实现 sequential fine-tuning，必须明确标注为 sequential fine-tuning，而不是 multi-task joint training。

时间无泄漏要求保持不变：

```text
Raw interactions
-> chronological split
-> Y_train / N_train
-> multi-task training
```

任何 Y_train 或 N_train 样本都不能包含对应用户 validation/test 时间边界后的 interaction。

## 十三、Phase 2 / Future Work

后续论文扩展可以保留一个消融设想：

```text
N-all：
完整交互序列预测 next interaction

N-pos：
仅正反馈序列预测 next positive interaction
```

该内容只属于 Future Work / Phase 2，不进入当前 MVP 实现范围。

KAR knowledge augmentation、SASRec、Hard Negative、Bootstrap、第二数据集、多 seed、7B 模型和大规模超参数搜索，仍必须等待当前 M 诊断结果整理、分组 error analysis 和结论边界确认后再决定是否进入下一阶段。
