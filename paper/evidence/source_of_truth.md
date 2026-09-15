# 事实来源与等级

版本：2026-09-10 RUN_METADATA闭环。seed42完整轨迹与seed43/44的96k独立复现分开登记；原始来源保持只读。运行到结果映射见 [run_metadata_ledger.md](run_metadata_ledger.md)，数值摘要见 [ms96_integration_summary.md](ms96_integration_summary.md)。

## 优先级

1. `.agent/exposure_scaling/final_evidence/`：seed42数值与原配对区间；`.agent/ms96_integration/imported/a9c6cd9/artifacts/multiseed96/`：固定Git提交的seed43/44 validation/test汇总，已核对八份文本的规范化blob。两者共同构成当前数值来源，不由旧叙事推翻。
2. `.agent/state_reconstruction/`：任务语义、别名、旧多 seed 与 Amazon 的证据范围。
3. `.agent/paper_reasoning/`：研究问题关系和故事边界；它不是新的观测数据。
4. 定向的已完成 artifact 与当前代码：补充具体统计/协议说明；代码默认值不能冒充历史运行实参。
5. 旧 manuscript 与旧 writing artifacts：文字组织参考，不能推翻以上来源。

`CORE` 指论文中的核心作用，不自动意味着跨 seed 或因果证据。下表的等级分别标注任务契约、单 seed 观察、评估抽样区间、跨训练 seed 和外部方向支持。

## Finding → 证据

| ID | 核心 finding | Supporting artifact（仓库根目录相对路径） | 当前等级 | 依赖 seed42 | multi-seed 已验证 | Amazon 支持 |
| --- | --- | --- | --- | --- | --- | --- |
| C1 | Y 偏好与 N 下一交互是不同目标；桥接排序表现不同 | `configs/experiment.yaml`; `src/data/split.py`; `.agent/exposure_scaling/final_evidence/exposure_main_table.csv` | 任务契约 + seed42 观察 | 定义否、数值是 | 旧点局部，不覆盖新曲线 | 仅 Y-as-ranker 与 N 的排序方向 |
| C2 | Y 在 24/48/96k 的收益有限且指标并非一致单调 | `.agent/exposure_scaling/final_evidence/exposure_main_table.csv` | seed42 描述 | 是 | 否 | 无曝光曲线 |
| C3 | N 的排序在 24/48/96/200k 点持续上升 | 同上；`.agent/state_reconstruction/CURRENT_FINDINGS_DATA_ANALYSIS_CONCLUSION.md` | seed42 描述 | 是 | 否 | 无曝光曲线 |
| C4 | 96k的M1-Y保持与Y96接近的被测偏好表现；三seed test点估计稍高，seed44验证Accuracy例外 | `paper/evidence/ms96_raw_metrics.csv`; `paper/evidence/ms96_integration_summary.md`; 原 `table_specialist_multitask.csv` | 三训练seed点估计 + seed42 validation用户级bootstrap | 轨迹/CI是，96k点否 | 是，仅96k；Y96_STATUS已关闭 | 无对应binary证据 |
| C5 | common cross-task-safe seed42标准k5验证gap在48→96k三指标收窄；test不收窄；三seed96k两split均保留小幅N优势 | `paper/plan/task-packets/m1-common-clean-exposure-verification.csv`; `paper/plan/task-packets/m1-clean-subset-audit/clean_multiseed_96_summary.csv` | seed42共同样本轨迹 + 三训练seed 96k描述统计；无ranking CI | 轨迹是 | 是，仅96k；不是三seed曝光曲线 | 未复现96k |
| C6 | cross-task-safe三seed两split的k5/k20/k50三指标均N>M；k20 gap最大，k5/k50较小且相对次序依metric/split变化 | `paper/plan/task-packets/m1-clean-subset-audit/recovered_clean_per_seed.csv`; `paper/plan/task-packets/m1-clean-subset-audit/clean_multiseed_96_summary.csv` | 三训练seed 96k点估计、均值、sample SD与方向；无ranking CI | 否 | 是，仅96k和这三个协议 | 未测试 |
| C10 | 排除直接跨任务target泄漏的MovieLens高保留率子集上，N在48k seed42及96k三seed所有已测N-side条件均高于M1；k20差距最大，k5/k50较小且相对次序依metric/split变化 | `paper/plan/task-packets/m1-clean-subset-recovery-closure.md`; `paper/plan/task-packets/m1-clean-subset-audit/recovered_clean_per_seed.csv`; `paper/plan/task-packets/m1-clean-subset-audit/clean_multiseed_96_summary.csv` | 既有checkpoint的clean-subset替代分析；三seed描述统计；新增部分无bootstrap | 48k是；96k否 | 96k方向是；48k否 | 无；Amazon M1未做同口径审计 |
| C7 | 约同 N 样本曝光下 N 在四个验证点高于 SASRec | `.agent/exposure_scaling/final_evidence/sasrec_exposure_alignment.csv`; `tables/table_n_sasrec.csv`（同一目录） | seed42 对齐观察，非 compute 公平 | 是 | 旧低曝光方向有；新四点无 | 旧低曝光排序方向 |
| C8 | Amazon 提供外部排序方向，非完整复现 | `.agent/cross_dataset_validation/seed42_result_summary.json`; `.agent/state_reconstruction/dataset_comparison.md` | seed42 外部描述 | 是 | 否 | 本行即 Amazon，只有 Random/PopMatch-k5 |
| C9 | 旧低曝光及高曝光基线方向具有旧三 seed 支持 | `.agent/state_reconstruction/CURRENT_FINDINGS_DATA_ANALYSIS_CONCLUSION.md`; `.agent/multiseed_stability/final/`（已重建索引，本轮不扩读） | 已重建的旧三 seed 证据 | 非仅 seed42 | 是，仅旧 operating points | 否 |

## 方法与数值契约

| ID | 事实 | 直接来源 |
| --- | --- | --- |
| M1 | rating >= 4 为 Y 正例；历史长度 10；严格早于目标时间 | `configs/experiment.yaml`; `src/data/split.py` |
| M2 | 4-bit NF4、r16、alpha32、dropout0.05、attention/MLP 全线性投影 | `configs/experiment.yaml`; `src/train/train_y.py`; `src/train/preference_dataset.py` |
| M3 | 单卡有效 batch 8；M1 每任务曝光为调度预期值 | `.agent/pytest_tmp_seed42_deep_analysis_fix/training_protocol_comparison.md`; `src/train/multitask_dataset.py` |
| M4 | Yes/No 归一化与候选标签概率；多 token 使用序列似然 | `src/inference/scoring.py` |
| M5 | k5流行度匹配、k20/k50随机，候选seed42；独立非嵌套，数量/组成/采样/难度共同变；PopMatch读full_sequences | `src/eval/candidate_sets.py`; `.agent/exposure_scaling/multiseed96/commands/multiseed96_queue.sh`; 冻结非嵌套结论及用户MS96任务说明；本轮未执行队列 |
| M6 | 原seed42 bootstrap按用户分组、共享重采样、百分位95%CI；binary固定0.5；三seed汇总仅等权mean/sample std、ddof=1、n=3 | `.agent/exposure_scaling/alignment/commands/seed42_deep_analysis.py`; `paper/analysis/ms96_evidence.py`; 43/44无新增bootstrap |
| M7 | SASRec 本地实现为因果序列编码、全物品分类交叉熵；样本计数取实际清单 | `src/baselines/sasrec.py`; `.agent/exposure_scaling/alignment/sasrec_checkpoint_inventory.csv` |
| M8 | MovieLens 与 Amazon 任务级划分规模不同 | `.agent/state_reconstruction/dataset_comparison.md`; `.agent/cross_dataset_validation/amazon_dataset_stats.json` |
| M9 | 正式LLM/SASRec/Amazon运行的seed、最终停止点、配置、候选和metric绑定；M1与SASRec计数边界 | `paper/metadata/run_metadata_recovery.*.json`; `paper/evidence/run_metadata_ledger.md`; `.agent/exposure_scaling/alignment/sasrec_checkpoint_inventory.csv`; `.agent/sample_efficiency_training_efficiency/final_curve/sample_efficiency_curve.json` |
| M10 | MovieLens M1-N cross-task-safe subset排除被Y训练作为target消费、进入更晚Y训练history或存在同用户Y训练target时间戳不早于N评测target的样本；N训练分支对保留holdout的target/history重叠为0；M1-48与M1-96保留率分别为96.81%/98.68%和93.71%/97.53% | `paper/plan/task-packets/m1-clean-subset-audit/audit_summary.json`; `paper/plan/task-packets/m1-clean-subset-recovery-closure.md`; `paper/plan/task-packets/m1-common-clean-exposure-verification.csv` |

## 既有冲突与处理

| 项目 | 冲突或缺口 | 新稿处理 |
| --- | --- | --- |
| S391 曝光 | 重建别名表写 200192；冻结 CSV 与原对齐 inventory 都写 200000 | 采用实际 200000；不按 391×512 代替短尾 batch 计数 |
| binary 阈值 | 旧稿宽泛称 validation-calibrated F1；96k 配对脚本固定 0.5 | 新稿区分固定阈值结果与旧校准诊断，不混写 |
| bootstrap 源 | 原机器summary、当前CI所需7份paired prediction、README/manifest已回收；5000次、effective OUT、reuse行为、seed规则及执行时期源码Git/blob身份已交叉恢复；exact shell invocation未留存 | 采用冻结seed42用户级百分位CI；完整边界见 `bootstrap_provenance_closure.md`；BOOTSTRAP_PROVENANCE为RESOLVED，不重新bootstrap或重算CI |
| 候选嵌套审计 | 用户补充比例0、0、约0.000176，但本轮导入未含独立audit原件 | 正文采用已冻结非嵌套结论；精确比例仅在MS96摘要标作用户提供 |
| PopMatch 信息范围 | 实现从 full_sequences 统计流行度，非训练期专用统计 | 明示为离线候选控制；严格时间历史不等于全流程 train-only 信息 |
| all-linear | 配置使用七类投影名，而非字面 `target_modules='all-linear'` | 写全 attention/MLP 线性投影，并列明七类；不说嵌入和输出头也加 LoRA |
| 训练超参数 | 五份回收JSON已绑定正文所需历史run；exact CLI、精确base revision及正文未声称的完整optimizer/scheduler/LR/软件栈未留存 | 按运行台账只确认已交叉恢复字段；不补造未保存参数；RUN_METADATA已RESOLVED |
| k5验证与测试 | common-safe seed42 validation的48→96k三指标差距均缩小；test三指标均未缩小；三seed96k两split均N>M | 使用小幅N优势而非parity；轨迹收窄限定seed42 validation；clean ranking不使用旧CI |

本轮仅整合已有运行元数据，未评估模型、修改冻结CI或重算数值。MS96与Y96_STATUS已整合；BOOTSTRAP_PROVENANCE和RUN_METADATA均按各自闭环记录关闭。S47/S94/S188/S391正式seed42轨迹不与旧43/44的s23或高曝光运行混用；实际曝光为24064/48128/96256/200000。
