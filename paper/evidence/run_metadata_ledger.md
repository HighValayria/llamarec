# RUN_METADATA 运行台账与闭环裁决

日期：2026-09-09。状态：**RESOLVED WITH DISCLOSED LIMITS**。

## 1. 裁决范围

本台账只闭合当前 Methods 已写出的运行事实：模型/配置身份、训练 seed、micro-batch、gradient accumulation、最终 optimizer step/checkpoint、M1 的 1:1 调度、固定候选与 split 指标绑定，以及 SASRec 四个曝光对齐点。它不追补正文未声称的 optimizer、scheduler、learning rate、CUDA/驱动版本，也不把未留存的 exact shell invocation 或底座 revision/hash 补猜出来。

五份回收 JSON 均可解析，共 39 个训练或评测记录。原始文件保持不改，其 SHA256 为：

| 文件 | SHA256 |
| --- | --- |
| `run_metadata_recovery.machine_a.json` | `5286f62975e8558136d2be433804e18fe6f5ca9ea3214dbe1d2c22afe36a9505` |
| `run_metadata_recovery.machine_b_seed43.json` | `b9eaf6cd2174fcb733669c685e4203fbbee8ad24caf31b235bfe32acea0fc2b7` |
| `run_metadata_recovery.machine_c_seed44.json` | `9dde92a1d66650e44758e7460bc0a57b3abe695d5739d2875becbd2695f8468d` |
| `run_metadata_recovery.machine_d_sasrec.json` | `e36d70262f85ae6e5687d36df6f3c3ef8a4e3e83388a32b9b679d8db73a0cbfb` |
| `run_metadata_recovery.machine_e_amazon.json` | `617b20288efa01bc3ed4b236aac3933a3f8bc0c46cddc7f32579f571a190531c` |

以下远端路径均以 `/root/llamarec/` 为根。

## 2. 采集状态的人工复核

采集器报告 13 个 `CONFLICT`，全部来自同一误判：它同时收集了同一 run 目录中的阶段性 checkpoint 与最终 checkpoint，并把不同 `global_step` 当成运行冲突。每个 run 均存在目标最终 checkpoint，且其中 `max_steps` 与目标步数一致。阶段性 checkpoint 是正常留存，不是相互矛盾的正式结果。

N24 的 `training_seed=UNKNOWN` 也是字段提取遗漏。其历史 `config_snapshot.yaml` 在嵌套 `seed.random_seed` 中明确记录 42；训练目录、checkpoint-3000 和 `global_step=3000` 均已找到。因此 N24 训练身份改判为已确认。

## 3. LLM 训练与评测绑定

历史运行快照共同记录 Llama-3.2-3B-Instruct 配置身份、最大长度 2048、micro-batch 1 和 gradient accumulation 8；最终 `trainer_state.json` 独立确认 micro-batch 1 与停止步数。gradient accumulation 8 位于该历史运行保存的配置快照中，并与冻结曝光账本的每更新 8 个任务样本一致；exact CLI 未留存，因此只按交叉恢复的生效设置登记，不声称恢复了原命令行。

| Run | Seed | 最终步数/checkpoint | 训练目录 | PopMatch-k5 指标绑定 |
| --- | ---: | --- | --- | --- |
| Y24 | 42 | 3000 / checkpoint-3000 | `outputs/y/movielens-1m/exposure_y_s3000` | 同目录 `popmatch_eval/{valid,test}_metrics.json` |
| Y48 | 42 | 6000 / checkpoint-6000 | `outputs/y/movielens-1m/exposure_y_s6000` | 同目录 `popmatch_eval/{valid,test}_metrics.json` |
| Y96 | 42 | 12000 / checkpoint-12000 | `outputs/y/movielens-1m/exposure_y_s12000` | `popmatch_eval_valid_only/valid_metrics.json`；`popmatch_eval/test_metrics.json` |
| N24 | 42 | 3000 / checkpoint-3000 | `outputs/n/movielens-1m/sample_efficiency_n_s3000` | `outputs/n/movielens-1m/sample_efficiency_n_s3000_popmatch_eval/{valid,test}_metrics.json`；路径与 test 值由既有 `final_curve` 明确绑定，validation 值由冻结 seed42 曲线绑定 |
| N48 | 42 | 6000 / checkpoint-6000 | `outputs/n/movielens-1m/exposure_n_s6000` | 同目录 `popmatch_eval/{valid,test}_metrics.json` |
| N96 | 42 | 12000 / checkpoint-12000 | `outputs/n/movielens-1m/exposure_n_s12000` | 同目录 `popmatch_eval/{valid,test}_metrics.json` |
| N200 | 42 | 25000 / checkpoint-25000 | `outputs/n/movielens-1m/exposure_n_s25000` | 同目录 `popmatch_eval/{valid,test}_metrics.json` |
| M1-48 | 42 | 12000 / checkpoint-12000 | `outputs/m/movielens-1m/exposure_m1_s12000` | `popmatch_eval_valid_only/valid_metrics.json`；`popmatch_eval/test_metrics.json` |
| M1-96 | 42 | 24000 / checkpoint-24000 | `outputs/m/movielens-1m/exposure_m1_s24000` | `popmatch_eval_valid_only/valid_metrics.json`；`popmatch_eval/test_metrics.json` |
| Y96 / N96 / M1-96 | 43 | 12000 / 12000 / 24000 | 对应 `exposure_{y,n,m1}_s{12000,12000,24000}_seed43` | 各 run 的 `popmatch_eval/{valid,test}_metrics.json` |
| Y96 / N96 / M1-96 | 44 | 12000 / 12000 / 24000 | 对应 `exposure_{y,n,m1}_s{12000,12000,24000}_seed44` | 各 run 的 `popmatch_eval/{valid,test}_metrics.json` |

所有上表 LLM run 均有 `run_summary.json` 和 `config_snapshot.yaml`；最终 checkpoint 内有 `trainer_state.json`。seed43/44 的目录中保留 11000/11500 或 23000/23500 等中间 checkpoint，不改变最终步数裁决。

M1 的正式 `run_summary.json` 记录 `task_ratio={y:1,n:1}`、每任务 200000 条构造池及顺序交错计数。它确认调度设计和最终停止点，但不构成逐样本消费 trace，也没有保存每次续训的 exact resume 来源或 data-skipping 实参。因此正文继续把每任务 48k/96k 写成在正确 resume data skipping 前提下的**预期分配**；本闭环不升级该主张。

## 4. Hard-candidate 纯评测绑定

k20/k50 记录是 N96 与 M1-96 checkpoint 的附加评测，不是新训练。seed42、43、44 各有 N96/M1-96 的 k20 与 k50 `evaluation_summary.json`、`valid_metrics.json`、`test_metrics.json`；其训练 seed 取被评测 checkpoint 的 seed，候选文件名中的 `seed42` 指固定候选集 seed，不表示 seed43/44 模型被改成训练 seed42。

seed42 评测根为 `outputs/phase2a/current96_ranking_robustness/`；seed43/44 根为 `outputs/phase2a/multiseed96_ranking_robustness/seed{43,44}/`。各目录名明确区分 `n_k0_k{20,50}_seed42` 与 `m1_k{20,50}_seed42`。

## 5. SASRec 四点

| Run | Seed | optimizer steps | Batch | 实际消费 | 运行与指标目录 |
| --- | ---: | ---: | ---: | ---: | --- |
| S47 | 42 | 47 | 512 | 24064 | `outputs/baselines/movielens-1m/alignment_sasrec_s47` |
| S94 | 42 | 94 | 512 | 48128 | `outputs/baselines/movielens-1m/alignment_sasrec_s94` |
| S188 | 42 | 188 | 512 | 96256 | `outputs/baselines/movielens-1m/alignment_sasrec_s188` |
| S391 | 42 | 391 | 512 | 200000 | `outputs/baselines/movielens-1m/alignment_sasrec_s391` |

每个目录均回收了 `run_summary.json`、`valid_metrics.json` 和 `test_metrics.json`。run summary 确认 seed、batch、optimizer steps、`training_stop=max_steps`、200000 条训练池，以及 validation/test 均使用 `k5_popmatch_seed42` 候选。实际消费量来自既有 `.agent/exposure_scaling/alignment/sasrec_checkpoint_inventory.csv`，并与冻结对齐表对应；它不是回收 JSON 中的独立字段。尤其 S391 的 200000 包含短尾 batch，不能用 `391 x 512 = 200192` 替代。

## 6. Amazon 外部验证绑定

Amazon-Y、Amazon-N、Amazon-M1 的训练 seed 均为 42，最终 checkpoint 分别为 1500、1500、3000；采集器列出的 1400/1450 与 2900/2950 是中间 checkpoint。三者的 test-only PopMatch-k5 评测分别绑定到 `amazon_{y,n,m1}_{1500,1500,3000}_seed42_popmatch_k5_eval/test_metrics.json`。Base 与 SASRec 的 test-only 记录也已绑定；各评测使用同一 `amazon-musical-instruments/variants/popmatch_k5_seed42/test.jsonl`，ranking 有效样本数为 57439。M1 run summary 另确认 1:1 交错以及 1000 Y + 1000 N 的构造计数。

Amazon 没有 validation、完整曝光曲线或 hard-candidate 复现；本台账只确认既有 test-only 外部方向验证，不扩大其科学作用。

## 7. 保留边界与关闭理由

- 未留存 exact shell invocation；历史生效参数由 config snapshot、trainer state、run summary、冻结曝光账本和指标路径交叉恢复。
- 精确 base-model revision/hash 未保存；只确认模型身份和路径。正文不声称某个 revision。
- optimizer、scheduler、learning rate 与完整软件栈未统一回收，当前正文也未列出这些运行值。
- M1 无逐样本 trace 和完整 resume/data-skip 记录，所以预期每任务曝光的限定永久保留；重新训练不能证明历史 run。
- N24 的评测文件没有包含在本轮回收 JSON 中，但其独立评测目录、test metric 与 evaluation-summary 路径已在原 `final_curve` 中登记，validation/test 数值也已进入冻结 seed42 证据。此处是跨既有档案绑定，不冒充本轮重新取得原文件。
- SASRec run summary 不直接写累计实际消费字段；正式实际消费量由原 alignment inventory 与冻结表提供，回收 run summary/metrics 负责确认四个正式运行及候选绑定。

在这些公开边界下，Methods 两个段落所需的最小运行来源已经可审计，`RUN_METADATA` 从 `PARTIAL` 更新为 **RESOLVED**。这表示不再需要继续搜机器或重跑实验，不表示仓库已达到 submission-ready；来源笔记、测试契约、venue/template 与作者最终审定仍是独立事项。
