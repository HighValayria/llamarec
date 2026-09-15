# ICECAI 2026 Scientific Repair Evidence

日期：2026-09-11  
状态：`P1_01_ACTUAL_LEAKAGE_FOUND`  
限制：A--N为只读代码与materialized artifact初始审计；后续O节只过滤已有预测并重算干净子集指标/bootstrap。全程未训练、未推理、未修改论文或历史artifact。

## A. P1-01 Question

审计正式M1训练所直接读取的Y/N训练目标，确认一个任务的验证/测试目标事件是否被另一任务作为M1训练目标，并将target isolation与history role overlap分开报告。

## B. Exact Split Implementation Map

| Role | Source | Function / lines | Implemented behavior |
| --- | --- | --- | --- |
| Y split | `src/data/split.py` | `build_full_sequence_leave_two_out_split`; `_build_y_user_split` | 最后timestamp bucket为test、倒数第二bucket为validation，更早bucket为train。 |
| N legal targets | `src/data/split.py` | `_legal_next_item_targets` | 首桶跳过；后续仅singleton bucket可作N target；多事件桶只跳过target角色。 |
| N split | `src/data/split.py` | `_build_n_user_split` | 最后两个legal targets依次为validation/test，其余legal targets为train。 |
| Y materialization | `src/data/build_preference.py:30` | `build_preference_samples`; train branch lines 49--63 | 所有timestamp早于Y validation bucket的事件均物化为Y train target。 |
| N materialization | `src/data/build_next_item.py:29` | `build_next_item_samples`; lines 57--108 | legal target序列末二项为validation/test；此前项为train。 |
| M1 sources | `src/train/train_m.py:56` | `run_m_training`; lines 56--78 | 直接读取`preference_train.jsonl`和`next_item_train.jsonl`，无跨任务二次过滤。 |
| M1 interleave | `src/train/multitask_dataset.py:11` | `MultitaskTrainingDataset`; lines 38--60 | 按Y:N=1:1顺序交错两份输入记录。 |
| Resume/sampler | `src/train/train_m.py:151` and `:283` | `trainer.train(resume_from_checkpoint=...)`; `SequentialTrainer` | 续训恢复checkpoint；训练sampler为SequentialSampler。它改变消费进度，不改变样本成员资格。 |

配置路径为`configs/m.yaml`：Y来源`data/processed/{dataset}/preference_train.jsonl`，N来源`data/processed/{dataset}/next_item_train.jsonl`。

## C. Canonical Event Identity

事件键为`(user_id, movie_id, timestamp, sequence_index, rating)`。`user_id + movie_id + timestamp`是业务身份基础；加入排序后materialized记录保留的`sequence_index`与`rating`，用于区分潜在同用户/物品/时间重复并与split实现中的`_same_target`语义一致。六个文件内target均为唯一事件。

| Set | Rows / unique targets | SHA256 |
| --- | ---: | --- |
| Y train | 976,284 | `2160f92d7755cb5bd0c9f46592c611ea69559a5283230d9a297541e89ac03ae3` |
| Y validation | 12,381 | `3c50e4a5ade73228d36e02c81cad0e873ac7b0fd9d17137d1e7a1fe5180b23dd` |
| Y test | 11,544 | `d5f1252e2efef1add1976e3edf8b74e6a573983f72a672c4a89c446bef74bf8e` |
| N train | 212,725 | `b0382a1a5d02e69edb7ddc466fec542a4f44595d03466a445e98a2e42aefab42` |
| N validation | 5,675 | `78bb80789e0f8a4a5ed1bd6e03c47c772278b8cbb9401118ae0284e496162955` |
| N test | 5,675 | `9eb1e1f424b04f5184f2f1df2f899a4866774cca1bc9d8cb88977d9321581e23` |

审计脚本：`paper/plan/task-packets/p1_01_cross_task_holdout_audit.py`。脚本只读六个JSONL并向stdout输出汇总。

## D. Cross-Task Target Overlap

M1没有独立materialized训练文件；其两分支target集合分别等于Y train与N train输入集合。

| Check | Left count | Right count | Overlap events | Unique users | Rate of right | Verdict |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| A. M1 Y-train x N-validation | 976,284 | 5,675 | **3,342** | 3,342 | 58.8899% | heldout-as-train-target |
| B. M1 Y-train x N-test | 976,284 | 5,675 | **1,306** | 1,306 | 23.0132% | heldout-as-train-target |
| C. M1 N-train x Y-validation | 212,725 | 12,381 | **0** | 0 | 0% | no target overlap |
| D. M1 N-train x Y-test | 212,725 | 11,544 | **0** | 0 | 0% | no target overlap |

正式M1按顺序消费的Y前缀也已确认非零：每任务12k前缀含N-validation/test目标54/20项；48k前缀181/75项；96k前缀357/140项。因此泄漏不是只存在于未被正式checkpoint消费的Y train尾部。

匿名化不必要的ID-only示例已由脚本限制为每项最多5条。首个A类示例为`user=1, item=527, timestamp=978824195, sequence_index=41`；该事件是N-validation target，同时是Y-train target。

## E. History Role Overlap

| Check | Train examples with overlap | Unique heldout events | Unique users | Interpretation |
| --- | ---: | ---: | ---: | --- |
| Y-train histories x N-validation targets | 18,327 | 2,397 | 2,397 | 另一任务留出事件作为严格更早history出现；与target leakage分开记录。 |
| Y-train histories x N-test targets | 7,692 | 919 | 919 | 同上，属于角色重叠；本身不等同于heldout-as-train-target。 |
| N-train histories x Y-validation targets | 0 | 0 | 0 | 无角色重叠。 |
| N-train histories x Y-test targets | 0 | 0 | 0 | 无角色重叠。 |

history角色重叠可能满足单样本的`history timestamp < current target`，但不能消除D节已确认的同一事件同时作为Y训练target和N留出target。P1-01由target overlap直接触发，不依赖对history角色的进一步价值判断。

## F. P1-01 Verdict

`P1_01_ACTUAL_LEAKAGE_FOUND`

现有per-task split各自内部满足严格历史规则，但没有提供cross-task event isolation。M1的Y分支确实把大量N validation/test事件作为训练target，且正式12k/48k/96k消费前缀均受影响。共同时间截断不是唯一可能修法，但重新构造的M1数据必须显式阻止heldout-as-train-target。

**确认受影响的正式论文运行**：MovieLens M1-48 seed42；MovieLens M1-96 seeds42/43/44。任何从这些checkpoint续训或派生的M1评测同样受影响。Amazon M运行尚未做同类materialized审计，不能据MovieLens结果直接判定其计数。

**受影响科学范围**：RQ3及primary C2的N-specialist/M1比较；RQ4及supporting C3的k5/k20/k50 M1比较；M1-96的Y-side preservation结果也需由干净重训checkpoint重新评测。RQ1的Y/N specialist formulation对照、RQ2的Y/N specialist轨迹和RQ5的N/SASRec比较不由该M1泄漏直接推翻。Amazon的N/M方向需单独审计。

**最小重跑/重评集合（仅方案，未执行）**：

1. 定义并物化cross-task-isolated M1训练数据，至少排除Y-train中所有N validation/test target事件；对称保留零交集约束并固化审计测试。
2. 不得从受污染M1 checkpoint续训。重新训练M1-48 seed42及M1-96 seeds42/43/44；保持其余已验证recipe不变。
3. 重新评测上述M1 checkpoint的Y-native与N-side validation/frozen-test k5；重新评测M1-96三seed的k20/k50。
4. 重新生成所有依赖M1的paired deltas、三seed描述统计、bootstrap区间、Tables IV--VII与相应claim控制记录。N/Y specialists无需因本项重训。
5. 单独对Amazon materialized Y/N/M输入执行同一审计；只有发现同类泄漏时才把Amazon M纳入重训。

## G--L. P1-02 Recovery Status at Mandatory Stop

发现actual leakage后，按任务规则停止普通repair流程。以下仅记录停止前已恢复事实，不继续闭合P1-02。

| Area | Status | Evidence recovered before stop |
| --- | --- | --- |
| G. LLM optimizer/config | PARTIAL | effective batch 8、LR 2e-4、bf16命令、max steps/exposure、seed入口和QLoRA字段已见代码/命令；实际optimizer、scheduler、warmup、weight decay尚未由正式run metadata闭合。 |
| H. N training candidates | VERIFIED | 5 candidates=1 target+4 unique random negatives；pool为全部item减当前target；允许历史交互item；materialization时shuffle；A--E按最终位置映射；训练random与正式eval PopMatch-k5不同。 |
| I. SASRec architecture | NOT_RETAINED_IN_THIS_AUDIT | 因强制停止未继续恢复。 |
| J. SASRec optimization | NOT_RETAINED_IN_THIS_AUDIT | 因强制停止未继续恢复。 |
| K. SASRec checkpoint selection | NOT_RETAINED_IN_THIS_AUDIT | 四点数值身份已存在既有控制记录，但selection procedure未在本轮闭合。 |
| L. Amazon operating points | NOT_RETAINED_IN_THIS_AUDIT | 因强制停止未继续恢复。 |

## M. Missing Evidence

- 正式LLM run实际采用的optimizer、scheduler、warmup和weight decay身份。
- SASRec架构、优化和S47/S94/S188/S391选择程序的完整Level 1--3证据。
- Amazon各模型准确checkpoint/exposure映射及其cross-task isolation审计。

P1-02 verdict：`P1_02_PARTIAL_EVIDENCE`。本轮不需要用户运行remote命令；当前阻断原因是已确认的本地数据泄漏，而非本地材料缺失。

## O. No-Retrain Clean-Subset Follow-up

后续无重训审计已在`m1-clean-subset-salvage-audit.md`闭合。M1-48保留validation/test 5,494/5,600个用户，M1-96保留5,318/5,535个用户，保留集A/B/C违反均为0；N训练分支对N留出target/history违反也均为0。

缺失的seed42 N48/M1-48及seed43/44 N96/M1-96逐用户prediction已从GitHub取回。三个archive与28个源文件均通过SHA256、字节数和行数校验；seed43/44未过滤指标与冻结汇总逐项一致。clean-subset重算现覆盖48k seed42及96k三个seed的k5/k20/k50：所有seed级N-M1差值均为正，96k的18个三seed汇总格均为3/3正向。裁决更新为`NO_RETRAIN_SALVAGE_FEASIBLE_WITH_RESTRICTED_CLAIMS`，完整结果见`m1-clean-subset-recovery-closure.md`。原全量M1-N结果仍无效，新恢复部分未重新bootstrap。

SASRec子项现已恢复完整：64维、2 heads、2层因果Transformer、dropout 0.2、最大历史10、全物品交叉熵；AdamW、LR 0.001、weight decay 0、无scheduler、batch 512、seed42。S47/S94/S188/S391是脚本预先指定且分别独立从头训练的optimizer-step点，不是validation选择；实际曝光为24,064/48,128/96,256/200,000，S391含短尾batch。四点均绑定PopMatch-k5 seed42候选。故**P1-02的SASRec disclosure子项为RESOLVED**；P1-02整体仍因LLM/Amazon其他披露项保持PARTIAL。

## N. Proposed Minimal Manuscript Repairs

当前不执行正文修改。无需重训的clean-subset替代证据已经闭合，但它不追认原全量M1-N结果。后续只有在用户明确授权后，才可按`m1-clean-subset-recovery-closure.md`第8节执行最小稿件同步；必须同时替换相关数值、收紧曝光结论并披露clean人群边界，不能只加入一句Methods或Limitations。
