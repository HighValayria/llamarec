# Evidence Provenance & Method Citation Closure Plan

> **CURRENT STATUS UPDATE（2026-09-09）**：本计划中的BOOTSTRAP_PROVENANCE `PARTIAL` 判断已被后续原机器取证取代。该项现为 **RESOLVED**；exact shell invocation未留存，但effective parameters、summary/input与执行时期源码身份已交叉恢复。不得按本文旧P0清单重复搜索或重跑。当前依据见 `paper/evidence/bootstrap_provenance_closure.md`。RUN_METADATA仍独立未闭。

日期：2026-09-09。状态：审计计划已完成，所有证据闭项和稿件修改动作均未执行。

## 任务包

- 目标：逐处说明RUN_METADATA、BOOTSTRAP_PROVENANCE、METHOD_CITATIONS缺什么、能从哪些既有资产恢复，以及后续最小动作。
- 只读输入：八份指定控制/审查文件、Methods、非Wiki仓库的现有实验资产/代码/命令和reference assets；本机根目录为F:/Projects/llamarec，附件/root/llamarec视为远端运行根，不假定当前可访问。
- 唯一paper可写文件：本文。另维护.agent/current_task.md、.agent/stage_state.yaml。
- 禁止：修改既有paper文件、删marker、改测试/旧基线、训练/推理、生成候选、新统计/重采样、搜索文献、Wiki访问、模板适配、Conclusion/Abstract。
- 证据分类：A RECOVERABLE_FROM_EXISTING_ASSET；B RECOVERABLE_WITH_MANUAL_CONFIRMATION；C NOT_RECOVERABLE_BUT_NONBLOCKING_IF_DISCLOSED；D WOULD_REQUIRE_NEW_EXPERIMENT；E MARKER_IS_STALE_OR_MISSCOPED。
- 验收：逐标记/运行族/引用陈述矩阵、最小人工补充清单、三项及总体关闭判断、只读验证和191项既有paper保护核验。
- 流程：using-research-writing、paper-orchestration、peer-review、verification；仅审计统计报告与已有引用，不写章节或重新设计故事。能力使用及验收记录集中在本文，不改progress/notes。

## 1. 审计结论与计数口径

本轮审计已完成；以下所有“补充、映射、关闭、同步”均为未来获授权后的动作，未执行。结论强度沿用冻结版本：seed42完整曝光轨迹；seed43/44仅96k运行点复现；k5小差距、k20较大专家差距、k50较小且变动的差距；Y侧preservation/comparable；正式SASRec四点；Amazon仅外部排序方向检查。

| 对象 | 精确计数 | 本地可直接整理 | 仍需最小外部材料 | 当前结论 |
| --- | --- | --- | --- | --- |
| RUN_METADATA | 作者源2处；覆盖8个审计结果族，不等于8个独立训练run | 6类已有事实，见3.1；完整关闭的marker为0 | 8族均有历史实参或产物绑定待确认；A与H的Amazon Base、E与B/C/D、F与E共享资产，不重复索取 | PARTIALLY_CLOSE；状态PARTIAL |
| BOOTSTRAP_PROVENANCE | 作者源1处 | 脚本、默认参数、统计定义、冻结导出链 | 原summary、实际执行记录、输入预测绑定 | PARTIAL；B类，尚未证明资产不可恢复 |
| METHOD_CITATIONS | 作者源2处；7项实质引文映射 | SASRec 1项READY | 6项缺主引用资产 | PARTIAL |
| 总体 | 5处作者源marker | 可以执行局部整理的依据已清楚 | 跨机器小文件及既有主引用材料待补 | NEEDS_USER_INPUT |

没有证据表明现在必须重训、推理或重做bootstrap。远端未同步不是实验未发生；也不能把“有命令”写成“实际按命令执行”。本轮不关闭任何marker。

## 2. 全部标记位置与总审计表

### 2.1 搜索范围与去重

全仓库精确词搜索使用 `rg --hidden --no-ignore -n -w -e RUN_METADATA -e BOOTSTRAP_PROVENANCE -e METHOD_CITATIONS`。排除 `wiki/**`、`.git/**`及依赖/缓存目录，不访问Wiki。覆盖modules、modules_parts、evidence、tables、assembly、plan、README、实验文档、configs、scripts及非Wiki的.agent。首次搜索包含全部当前管理记录；末次登记排除本文及本轮重写的current_task，防止自引用。

以下是全部既有命中位置；同一行包含多个名称时只登记一行。作者源5处、旧构建记录15条镜像、其余为控制/历史记录，没有在tables、assembly源码、configs或脚本里找到额外的这三个精确名称。

| 文件或同构文件组 | 行号 | 角色及周边内容 | 处理 |
| --- | --- | --- | --- |
| [training_setup.md](F:/Projects/llamarec/paper/modules_parts/methods/training_setup.md:11) | 11、45 | METHOD_CITATIONS；RUN_METADATA | 作者源MC01、RM01 |
| [baseline_setup.md](F:/Projects/llamarec/paper/modules_parts/methods/baseline_setup.md:11) | 11 | RUN_METADATA | 作者源RM02 |
| [datasets.md](F:/Projects/llamarec/paper/modules_parts/methods/datasets.md:11) | 11 | METHOD_CITATIONS | 作者源MC02 |
| [bootstrap_and_statistics.md](F:/Projects/llamarec/paper/modules_parts/methods/bootstrap_and_statistics.md:11) | 11 | BOOTSTRAP_PROVENANCE | 作者源BP01 |
| [source_of_truth.md](F:/Projects/llamarec/paper/evidence/source_of_truth.md:48) | 48、52 | 临时CSV为MISSING；默认配置不能保证历史optimizer/scheduler/LR | 同一缺口的裁决记录 |
| [claim_matrix.md](F:/Projects/llamarec/paper/evidence/claim_matrix.md:9) | 9、12 | methods.training.*未审定运行参数；statistics.*缺原预测链 | 主张映射，非新marker |
| [pending_evidence.md](F:/Projects/llamarec/paper/evidence/pending_evidence.md:13) | 13、14、15 | 三项未闭项及写作边界 | 状态记录，不改 |
| [ms96_integration_summary.md](F:/Projects/llamarec/paper/evidence/ms96_integration_summary.md:8) | 8 | artifact_index只是远端路径，不足关闭RUN_METADATA | 状态记录，不改 |
| [results_discussion_audit.md](F:/Projects/llamarec/paper/evidence/results_discussion_audit.md:242) | 242、252 | final阻拦；记录恢复不等于必须重训 | 既有审计记录 |
| [results-discussion-revision-plan.md](F:/Projects/llamarec/paper/plan/task-packets/results-discussion-revision-plan.md:212) | 212、285 | 独立未闭项；既有final检查失败 | 历史授权/验收记录 |
| [ms96_integration_review.md](F:/Projects/llamarec/paper/plan/review/ms96_integration_review.md:28) | 28、38 | 方法引文及RUN/BOOT未闭；旧build为历史版本 | 历史审阅记录 |
| [ms96_integration_audit.json](F:/Projects/llamarec/paper/plan/review/ms96_integration_audit.json:265) | 265、266、267 | 三项名称数组 | 历史机器记录 |
| [progress.md](F:/Projects/llamarec/paper/plan/progress.md:21) | 21 | 残余三项及模板、范围边界 | 不更新 |
| [methods_zh.build.json](F:/Projects/llamarec/paper/builds/review/methods_zh.build.json:221) | 221、222、223、224、225 | 按training引文、training运行、datasets引文、baseline运行、statistics统计的顺序复制5处作者源 | 旧build镜像，不新增5个缺口 |
| [methods_en.build.json](F:/Projects/llamarec/paper/builds/review/methods_en.build.json:221) | 221、222、223、224、225 | 同上 | 旧build镜像 |
| [methods_bilingual.build.json](F:/Projects/llamarec/paper/builds/review/methods_bilingual.build.json:221) | 221、222、223、224、225 | 同上 | 旧build镜像 |
| [.agent/current_task.md](F:/Projects/llamarec/.agent/current_task.md) | 本轮修改前34行；现行按标题定位 | 上轮残余三项；本轮改为审计摘要 | 管理记录，行号随压缩变化 |
| [.agent/stage_state.yaml](F:/Projects/llamarec/.agent/stage_state.yaml) | 管理记录 | 本轮目标与禁项说明 | 不计为稿件marker |

### 2.2 作者源周边文本与门控对象

下列摘录取自当前双语作者源，省略处不改变其原意。每个HTML marker同时约束中英两版，不能按语言重复计数。

- **RM01**：`methods.training.p04`，training_setup:45。EN：“The exposure analysis uses a single-device micro-batch of 1 and 8 gradient-accumulation steps, giving 8 task examples per optimizer update. Checkpoints are indexed by cumulative optimizer steps and task-sample exposure.” ZH：“曝光分析采用单设备 micro-batch 为 1、梯度累积步数为 8 的设置，每次优化器更新消耗 8 个任务样本。”后文限定多任务续训的“预期每任务分配”。门控M2/M3，关联training.p01配置、p02配比、exposure_definition，以及training_exposure、exposure_scaling、binary_exposure、MS96各表。
- **RM02**：`methods.baseline.p01`，baseline_setup:11。EN：“SASRec supplies a sequential baseline using item and position embeddings with causal sequence encoding. The evaluated repository implementation trains a next-target classifier with full-item cross-entropy...” ZH：“曝光对齐运行采用 batch size 512，并记录末尾 batch 的实际消耗量。”门控M7/C7及n_vs_sasrec_exposure；不授权替换冻结的四点。
- **BP01**：`methods.statistics.p01`，bootstrap_and_statistics:11。EN：“We use paired user-level bootstrap intervals to characterize evaluation-sample uncertainty for fixed trained models.” 后文写相同目标配对、用户有放回、全部用户样本共同进入两模型、2.5/97.5百分位和M-Y/N-M差值方向。ZH：“本文使用用户级配对 bootstrap 区间，衡量固定已训练模型的评估样本不确定性。”门控M6/C4/C5/C6、specialist_multitask与hard_candidate及对应结果解释，不门控跨seed显著性。
- **MC01**：`methods.training.p01`，training_setup:11。EN：“The adapted models use Llama-3.2-3B-Instruct with QLoRA and a frozen 4-bit NF4 base representation. Low-rank adapters have rank 16, scaling alpha 32, and dropout 0.05.” ZH：“适配模型使用 Llama-3.2-3B-Instruct，采用 QLoRA，并冻结 4-bit NF4 量化的底座表示。”门控M2/M4的底座、LoRA/QLoRA方法归属；rank/alpha等本实验配置由运行记录负责，不由引用证明。
- **MC02**：`methods.datasets.p01`，datasets:11。EN：“MovieLens-1M supplies 976,284 training, 12,381 validation, and 11,544 test examples for Y.” ZH：“合法 N 划分包含 212,725 个训练样本，两个评估划分各含 5,675 个样本”。门控M8的数据来源归属，关联datasets表；这些处理后计数属于本项目，不应声称来自数据集原论文。p02的Amazon没有独立METHOD marker，仍有数据来源引文缺口。

### 2.3 总审计表

分类缩写严格按任务包A-E；“B”表示待原有材料或人工确认，不表示本轮允许搜索、重跑或补写。E为范围判断，不是删marker许可。

| ID | Marker | Location | Missing information | Why needed | Candidate source | Recoverability | Risk | Proposed action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| RM01 | RUN_METADATA | training.p04:45，及其覆盖的训练/评估族 | 历史生效实参、底座revision、检查点完成/续训状态、评估文件绑定；部分软件记录 | 将配置说明与正式结果绑定 | 3.3运行映射、3.5代码字段审计、6节小文件 | B RECOVERABLE_WITH_MANUAL_CONFIRMATION | 默认值冒充执行事实；重复消费当独立样本 | 先整理已有事实，再补各run最小实参和评估记录；分字段关闭 |
| RM02 | RUN_METADATA | baseline.p01:11 | 四个alignment run实际summary/metric及候选绑定 | 核实批量、短尾batch和正式曝光 | 正式SAS索引/命令及四run小JSON | B RECOVERABLE_WITH_MANUAL_CONFIRMATION | 误换s23或391×512；论文方法与原SASRec混同 | 只接收指定四点原记录，保留200000短尾曝光 |
| BP01 | BOOTSTRAP_PROVENANCE | statistics.p01:11 | 冻结数值对应的原summary、输入、实际命令/版本、参数链 | 可审计区间的真正生成过程 | seed42_deep_analysis.py/.sh；原analysis_handoff | B RECOVERABLE_WITH_MANUAL_CONFIRMATION | 把硬编码导出当重采样原件、默认5000当运行证明 | 按4节恢复链；若确认已丢失再判断C或D |
| MC01 | METHOD_CITATIONS | training.p01:11 | Llama、LoRA、QLoRA三项主引用身份/条目 | 归属使用的已有模型/方法 | 既有reference资产；用户已有原文/正式条目 | B RECOVERABLE_WITH_MANUAL_CONFIRMATION | 凭常识补作者年份；二手笔记替代原文 | C01-C03逐项取得主资产后做双语映射 |
| MC02 | METHOD_CITATIONS | datasets.p01:11，并覆盖p02待补 | MovieLens与Amazon版本对应的两项正式引用 | 数据来源归属 | 现有处理协议只能证实版本；用户已有主引用 | B RECOVERABLE_WITH_MANUAL_CONFIRMATION | 把网页/处理脚本当学术引用 | C04-C05；不改变处理后统计 |
| MC03 | METHOD_CITATIONS范围内未单标 | baseline.p01首句 | SASRec引用落点和registry映射 | 方法身份归属 | S08/kang2018sasrec | A RECOVERABLE_FROM_EXISTING_ASSET | 把原文引用用于证明本仓库全物品CE | 仅在首句映射原始SASRec，不扩文学叙述 |
| MC04 | METHOD_CITATIONS范围内未单标 | statistics.p01首句 | bootstrap标准方法主引用 | 统计方法归属 | 目前无主bibliography资产 | B RECOVERABLE_WITH_MANUAL_CONFIRMATION | 脚本可追溯不等于已完成学术归属 | C07，与BP01独立验收 |
| SC01 | METHOD_CITATIONS | Amazon p02、SASRec p01、bootstrap p01 | 标记覆盖范围不足，不是已经满足 | 避免只补两个物理落点就宣布引文关闭 | 当前Methods和7项引用表 | E MARKER_IS_STALE_OR_MISSCOPED | 漏掉无同名marker的陈述 | 未来在控制清单拆分映射，不在本轮增删marker |
| SC02 | 三类名称的镜像 | 三份methods build.json各221-225 | 无独立科学缺口，属于旧导出重复位置 | 正确去重 | 作者源五处及旧build记录 | E MARKER_IS_STALE_OR_MISSCOPED | 按15条镜像计为15项新欠项 | 以作者源验收；将来获授权装配时自然同步 |
| SC03 | RUN_METADATA潜在范围误扩 | Base、k20/k50 | 未训练Base和纯评估hard协议不具有新增optimizer/LR | 避免制造不存在的训练metadata | Base评估/硬候选命令；3.4 | E MARKER_IS_STALE_OR_MISSCOPED | 追问Base优化器；为每个候选协议假设新训练 | Base下游训练N/A，hard继承N96/M96；只补评估绑定 |

没有发现五处作者源marker中任何一处已被完整证据满足、可纯状态删除。C/D目前只作为材料确认丢失后的条件分支，不把本地缺文件直接判为C/D。

## 3. RUN_METADATA closure matrix

### 3.1 六类可直接恢复的事实

下列6类为A：RECOVERABLE_FROM_EXISTING_ASSET。A只指注明的事实层级，不能扩展成所有历史run的完整执行证明。

| 事实组 | 可以直接记录的内容 | 证据及限制 |
| --- | --- | --- |
| A1 当前配置契约 | Llama-3.2-3B-Instruct；4-bit NF4；LoRA r16/alpha32/dropout0.05；q/k/v/o/gate/up/down投影；gradient checkpointing；max length 2048 | [experiment.yaml](F:/Projects/llamarec/configs/experiment.yaml)、[y_local_model.yaml](F:/Projects/llamarec/configs/y_local_model.yaml)、[n_local_model.yaml](F:/Projects/llamarec/configs/n_local_model.yaml)、[m_local_model.yaml](F:/Projects/llamarec/configs/m_local_model.yaml)。是当前配置，不是每个历史run的实参快照；确切base revision未知 |
| A2 冻结运行与曝光映射 | Y/N/M标签、命令目标步数、冻结曝光；SAS四点实际曝光24064/48128/96256/200000 | [existing_checkpoint_inventory.csv](F:/Projects/llamarec/.agent/exposure_scaling/existing_checkpoint_inventory.csv)、[exposure_accounting.json](F:/Projects/llamarec/.agent/exposure_scaling/exposure_accounting.json)、[sasrec_checkpoint_inventory.csv](F:/Projects/llamarec/.agent/exposure_scaling/alignment/sasrec_checkpoint_inventory.csv)、[training_exposure.csv](F:/Projects/llamarec/paper/tables/training_exposure.csv)。属于既有归档证据，不冒充本轮读到checkpoint |
| A3 M1交错与计数规则 | 1:1顺序交错，单设备batch1×accum8时每更新预期4Y+4N；M48/M96对应每任务48k/96k | [m1_exposure_audit.md](F:/Projects/llamarec/.agent/exposure_scaling/alignment/m1_exposure_audit.md)、[multitask_dataset.py](F:/Projects/llamarec/src/train/multitask_dataset.py:35)、[train_m.py](F:/Projects/llamarec/src/train/train_m.py:283)。算法可恢复；实际resume data skip、停止点及是否覆盖实参仍待核对 |
| A4 本机k5候选资产 | MovieLens PopMatch-k5的valid/test文件均实际存在，各5675行；本轮SHA256见3.2 | 本地文件可读，不能据当前哈希证明当年远端用了同一字节文件 |
| A5 当前评分实现 | Y为Yes/No归一化及独立候选P(Yes)；N/M-N为候选标签完整答案序列似然；SAS为序列表示上的候选物品分数 | 当前[training_setup.md](F:/Projects/llamarec/paper/modules_parts/methods/training_setup.md:32)、[evaluate_n_adapter.py](F:/Projects/llamarec/src/inference/evaluate_n_adapter.py:121)、[sasrec.py](F:/Projects/llamarec/src/baselines/sasrec.py:256)。当前实现可查，历史code/config版本仍需运行记录绑定 |
| A6 已导入结果的身份与覆盖 | seed43/44的Y/N/M96摘要、validation/test、hard k20/k50；Amazon user-reported cloud summary的seed42及ranking test 57439 | [ms96_data_provenance.json](F:/Projects/llamarec/paper/evidence/ms96_data_provenance.json)、[seed42_result_summary.json](F:/Projects/llamarec/.agent/cross_dataset_validation/seed42_result_summary.json)。导入摘要已在本机，不再索取一遍；MS96 M行samples是Y二分类数量，不能当M-N排序样本数 |

### 3.2 路径、候选和曝光单位

以下远端路径以 `R=/root/llamarec` 为附件给定的候选根；机器实际根若不同，由用户确认。它不是本机存在的目录。表内 `R/outputs/...` 是可精确展开的原资产候选路径，不表示已读取。

候选路径约定：
- **ML-K5**：`R/data/candidates/movielens-1m/variants/k5_popmatch_seed42/{valid,test}.jsonl`。
- **ML-K20/K50**：`R/data/candidates/movielens-1m/variants/{k20_seed42,k50_seed42}/{valid,test}.jsonl`，本机对应4文件不在当前候选目录；不能用k5或重生成文件替代。
- **AM-RANDOM/POP**：`R/data/candidates/amazon-musical-instruments/variants/{random_k5_seed42,popmatch_k5_seed42}/{valid,test}.jsonl`，本机不在当前候选目录。
- 大括号表示分别列举，不是要求存在带大括号的文件名。ML的`k5_popmatch`与Amazon的`popmatch_k5`顺序不同，按实际命令保留。

本机已读候选：
| 本地文件 | 行数 | SHA256（本轮读取） |
| --- | --- | --- |
| [ML k5 valid](F:/Projects/llamarec/data/candidates/movielens-1m/variants/k5_popmatch_seed42/valid.jsonl) | 5675 | EC3006BA1D28E665165A165E9F5F19B7B97E12FAD7FDA27672D5B57148AE8324 |
| [ML k5 test](F:/Projects/llamarec/data/candidates/movielens-1m/variants/k5_popmatch_seed42/test.jsonl) | 5675 | 19205F08CE8A16FDC5E17BE9219062E75779A8C1DB7053BE9460BF2921E4272F |

首行记录中candidate_generation.seed分别为143和244，不能据此把训练seed42改写成143/244；候选代码独立维护split seed偏移。当前文件行数也不能取代每次评估实际成功计数或历史候选哈希。

单位必须分开：
- optimizer steps是累计优化器更新次数。LLM 24k/48k/96k/200k指累计downstream task-example consumption，不是这些数目的optimizer steps。
- effective batch在单设备、完整累积且不发生丢弃/短尾变化的契约下是1×8=8。M1每任务曝光还要按1:1分配。
- unique samples、数据池大小、累计重复消费、epochs互不相等；200000训练cap也不是原始合法N样本212725或Y样本976284。
- M1-48为总96000、每任务48000；M1-96为总192000、每任务96000，正文当前保留“预期”措辞。
- SAS S391为391个optimizer steps、实际200000条消费；不是391×512=200192。不能凭completed_epochs字段名断言跑完了整轮数据。
- 曝光匹配不是token、预训练、FLOPs或wall-clock匹配，本轮不新增计算公平性主张。

### 3.3 正式运行定位表

来源为既有inventory、冻结表及下列命令，不用命令推定实际执行完成：
[seed42初段命令](F:/Projects/llamarec/.agent/exposure_scaling/commands/gpu_batch1_train.sh)、
[Y链](F:/Projects/llamarec/.agent/exposure_scaling/alignment/commands/y_commands.sh)、
[N96](F:/Projects/llamarec/.agent/exposure_scaling/commands/gpu_n96_train.sh)、
[N200](F:/Projects/llamarec/.agent/exposure_scaling/commands/gpu_n200_train.sh)、
[M链](F:/Projects/llamarec/.agent/exposure_scaling/alignment/commands/m1_commands.sh)、
[SAS四点命令](F:/Projects/llamarec/.agent/exposure_scaling/alignment/commands/sasrec_commands.sh)、
[MS96队列](F:/Projects/llamarec/.agent/exposure_scaling/multiseed96/commands/multiseed96_queue.sh)、
[hard候选评估命令](F:/Projects/llamarec/.agent/exposure_scaling/alignment/commands/phase2a_hardnegative_commands.sh)、
[Amazon队列](F:/Projects/llamarec/.agent/cross_dataset_validation/seed42_gpu_queue.sh)。全部只读，未执行。

| 正式run | run目录（接R） | checkpoint及步数 | 冻结曝光/任务说明 |
| --- | --- | --- | --- |
| Y24/42 | /outputs/y/movielens-1m/exposure_y_s3000 | checkpoints/checkpoint-3000；3000 | Y24000 |
| Y48/42 | /outputs/y/movielens-1m/exposure_y_s6000 | checkpoints/checkpoint-6000；6000 | Y48000 |
| Y96/42 | /outputs/y/movielens-1m/exposure_y_s12000 | checkpoints/checkpoint-12000；12000 | Y96000 |
| N24/42 | /outputs/n/movielens-1m/sample_efficiency_n_s3000 | checkpoints/checkpoint-3000；3000 | N24000；不是exposure_n_s3000 |
| N48/42 | /outputs/n/movielens-1m/exposure_n_s6000 | checkpoints/checkpoint-6000；6000 | N48000 |
| N96/42 | /outputs/n/movielens-1m/exposure_n_s12000 | checkpoints/checkpoint-12000；12000 | N96000 |
| N200/42 | /outputs/n/movielens-1m/exposure_n_s25000 | checkpoints/checkpoint-25000；25000 | N200000 |
| M1-48/42 | /outputs/m/movielens-1m/exposure_m1_s12000 | checkpoints/checkpoint-12000；12000 | 总96000，预期Y48000+N48000 |
| M1-96/42 | /outputs/m/movielens-1m/exposure_m1_s24000 | checkpoints/checkpoint-24000；24000 | 总192000，预期Y96000+N96000 |
| Y96/43、44 | /outputs/y/movielens-1m/exposure_y_s12000_seed{43,44} | checkpoints/checkpoint-12000；12000 | 各seed仅Y96k |
| N96/43、44 | /outputs/n/movielens-1m/exposure_n_s12000_seed{43,44} | checkpoints/checkpoint-12000；12000 | 各seed仅N96k |
| M1-96/43、44 | /outputs/m/movielens-1m/exposure_m1_s24000_seed{43,44} | checkpoints/checkpoint-24000；24000 | 各seed预期每任务96k |
| S47/42 | /outputs/baselines/movielens-1m/alignment_sasrec_s47 | 47；不假造HF格式checkpoint目录 | N24064 |
| S94/42 | /outputs/baselines/movielens-1m/alignment_sasrec_s94 | 94 | N48128 |
| S188/42 | /outputs/baselines/movielens-1m/alignment_sasrec_s188 | 188 | N96256 |
| S391/42 | /outputs/baselines/movielens-1m/alignment_sasrec_s391 | 391 | N200000 |
| Amazon Base/42 | /outputs/base/amazon-musical-instruments/seed42_{random,popmatch}_k5_eval | 原底座，无下游adapter训练 | 下游训练N/A；预训练暴露未知且不估算 |
| Amazon Y/42 | /outputs/y/amazon-musical-instruments/amazon_y_1500_seed42 | 命令目标1500 | 实际batch/消费待生成config或实参确认 |
| Amazon N/42 | /outputs/n/amazon-musical-instruments/amazon_n_1500_seed42 | 命令目标1500 | 同上 |
| Amazon M/42 | /outputs/m/amazon-musical-instruments/amazon_m1_3000_seed42 | 命令目标3000 | 同上，不能凭名称把每任务消费升级为已验证 |
| Amazon SAS/42 | /outputs/baselines/amazon-musical-instruments/sasrec_exp_match_k5_seed42_s23_popmatch_eval | 命令目标23 | 此为Amazon早期运行，不进入MovieLens正式四点 |

已导入[seed43 artifact_index](F:/Projects/llamarec/.agent/ms96_integration/imported/a9c6cd9/artifacts/multiseed96/seed43/artifact_index.txt)及[seed44 artifact_index](F:/Projects/llamarec/.agent/ms96_integration/imported/a9c6cd9/artifacts/multiseed96/seed44/artifact_index.txt)能定位k5的`<run>/popmatch_eval/{evaluation_summary.json,valid_metrics.json,test_metrics.json}`，以及hard：
- seed42：`R/outputs/phase2a/current96_ranking_robustness/{n_k0,m1}_{k20,k50}_seed42/`。
- seed43/44：`R/outputs/phase2a/multiseed96_ranking_robustness/seed{43,44}/{n_k0,m1}_{k20,k50}_seed42/`。
- 两种hard目录均读取evaluation_summary和valid/test_metrics；模型seed与目录尾部候选seed42含义不同。

seed42普通k5评估在既有分析脚本中使用`popmatch_eval`和`popmatch_eval_valid_only`的优先/备选搜索，详见4.2；尚未取得实际summary，不能提前确定命中了哪个分支。

### 3.4 八个运行族的字段级关闭矩阵

“正文”与“控制”栏都只写未来修改需求；本轮实际均不修改。本地正式run目录及原预测未取得，不能以toy/smoke产物替代。八族尚无一族满足“整个族历史执行链完全关闭”，但不意味着每个字段都缺。

| 族 | Current evidence / exact recoverable fields | Missing metadata / fields still unknown | Source path与候选/计数/评分 | 是否需正文变化 | 是否需证据控制变化 / 分类 |
| --- | --- | --- | --- | --- | --- |
| A LLM Base | A1当前模型标识、A5评分；当前semantics_bridge和exposure表没有ML Base正式点；cross_dataset确有Amazon Base | 真正报告的Base评估底座revision、配置与结果绑定；ML历史Base不扩进主表；optimizer/训练步数N/A | 3.3 Amazon Base根；AM-RANDOM/POP；已报告test ranking57439；原run_summary/scoring仍需核对 | 若补齐，只需底座身份说明；不新增ML Base结果或训练参数 | 与H共用Base资产，B；不重复索取 |
| B Y24/Y48/Y96 | seed42/ML/Y身份、3个run及目标checkpoint，24/48/96k冻结曝光；micro1×accum8和QLoRA来自当前配置 | 每run实际生效batch/精度/adapter配置、停止与resume路径；实际checkpoint和评估绑定；base revision | 3.3及Y链；Y-native处理后val12381/test11544；桥接ML-K5各5675是候选规模，需原metric核实有效计数；Y为P(Yes) | 仅确证后补最小实参/来源，当前未写的LR不强加 | 按run记录来源/未确认字段，B |
| C N24/N48/N96/N200 | seed42/ML/N身份、正确N24旧名、4曝光点；目标steps3000/6000/12000/25000 | 实际batch、停止、N48究竟从N24还是备用N12恢复；checkpoint/config与结果绑定 | 3.3及N命令；ML-K5；legal N val/test各5675，当前缺各run原metric有效计数；候选标签评分 | 保留已冻结单位；必要时补实参而不扩实验结果 | 同B，B |
| D M1-48/M1-96 | seed42/ML/M、目标steps12000/24000，1:1交错源码及每任务预期48k/96k | 实际resume data skip、各段计数/尾部、是否始终顺序采样；不能把构造池计数当实际消费 | 3.3、A3；ML-K5；Y/M-Y计数与M-N计数分开；共用adapter两接口 | 继续“预期”，只有足够运行记录才可取消限定；本轮不改 | 恢复配置/状态，保留计数假设，B |
| E MS96 42/43/44 | seed42复用B/C/D；43/44已有4份validation/test摘要及远端索引；Y/M-Y val12381/test11544，N/hard每split5675；不是完整曲线 | 43/44各Y/N/M实际summary、checkpoint实参与评估绑定；M-N k5不能用混合摘要的Y样本列作证明；确切训练版本 | 3.3与导入目录；ML-K5/K20/K50；Y、N、M-N接口沿用A5；43/44仅96k | 最小补充复现配置，保持运行点而非全轨迹 | 不重导重复summary.txt，不把索引当执行实参，B |
| F k20/k50 robustness | 对同一N96/M96的评估；seed42冻结表及43/44摘要有结果；目标k20/k50、NDCG仍@5、MRR全列表 | 原候选文件/已有哈希及顺序，eval summary到adapter路径与metric的绑定；当前本机无hard候选原件 | 上述hard目录；ML-K20/K50；43/44摘要5675/split；seed42冻结有效样本须原summary确认 | 若必要仅补评估来源；不得写成只操纵k或新增训练 | 候选和eval provenance补足；训练继承C/D/E，B |
| G 正式SAS四点 | 冻结S47/S94/S188/S391及实际曝光；batch512命令；当前源码为全物品CE | 四run的实际batch/seed/stop/train_examples/candidate_files；缺原run_summary和valid/test_metrics；现行代码默认LR不是原实参 | 3.3四根、[sasrec_artifact_index.md](F:/Projects/llamarec/.agent/exposure_scaling/final_evidence/sasrec_artifact_index.md)；ML-K5，预期5675/split，原有效计数待核 | 仅绑定正式实现/短尾消费；不换run、不加入历史高预算比较 | 保存四点真实来源与排除项，B |
| H Amazon Base/Y/N/M/SAS | cloud summary明确complete_user_reported_cloud_run、seed42、test57439；Random/Pop两协议；3个训练目标及SAS23可定位 | 生成后的amazon_local config、实际batch/消费/stop、QLoRA/底座、评估config/scoring/candidates；旧protocol与当前实现的流行度计数来源需原快照裁决 | 3.3；AM-RANDOM/POP；当前cross_dataset表为Pop test，旧summary中的Random仅按已有正文所需核对，不新增表行 | 保持external ranking-side directional check，不补成Amazon原生Y或曝光曲线 | 仅映射已报告结果；A共用Base，B |

本机未见正式的训练summary/config_snapshot/trainer_state。现有outputs中toy/smoke、其他数据集及popularity调试产物均不适用。针对已知正式路径的本地Git历史查询没有取回原记录；这是“当前本地refs未提供”，不是所有机器/远端都不存在。本轮未fetch/pull、未checkout/reset。

### 3.5 配置与历史实参不可混用

- [train_y.py:473](F:/Projects/llamarec/src/train/train_y.py:473)及[train_n.py:230](F:/Projects/llamarec/src/train/train_n.py:230)：config_snapshot写合并配置；run_summary含模型、dataset、seed、加载记录数等，但并不完整保存CLI覆盖后的LR/batch/max_steps等训练实参。只要这两份文件，仍可能无法关闭RUN。
- [train_m.py:432](F:/Projects/llamarec/src/train/train_m.py:432)增加task ratio、interleaved counts/cycles/task_schedule；这些是构造的数据安排，不等于已消费总量。SequentialTrainer与1:1交错源码支持预期分配，缺实际resume/data-skip证据时不升级。
- 最小补充是对应checkpoint的trainer_state.json，加已有可读TrainingArguments/执行日志实参片段；已有training_args.bin可在原可信环境导出必要字段，不索取或加载模型权重，不在本轮反序列化不可信二进制。
- 当前Y/N/M配置含smoke默认值，LR0.0002、max_steps100等不能抄入正式run。当前Methods没有报告optimizer类别/LR/scheduler数值，不为“完整”新增这些正文参数；若旧控制项要求记录，只恢复实际值或诚实留未知。软件版本/base revision先查已保存记录，无记录时披露，而不是重训来制造原记录。
- Y24命令从Y1500锚点恢复；Y48从Y24、Y96从Y48；N48命令在N24与旧N1500锚点间有fallback；N96/N200继续链；M48从旧M3000锚点、M96从M48。需实际command/log判定分支，不能仅按目标路径推断。
- MS96命令从各seed早期Y/N1500、M3000锚点续训到96k，而非证明43/44所有中间点都被评估。已导入索引的checkpoint保存间隔与当前queue参数不完全一致，进一步说明当前脚本不能自动代替历史执行版本。
- [sasrec.py:256](F:/Projects/llamarec/src/baselines/sasrec.py:256)的run_summary有optimizer_steps、training_stop、batch_size、learning_rate、seed、train_examples、candidate_files等关键字段；未直接保存独立的累计实际消费字段。应结合原run记录与冻结200000短尾审计，而非无条件乘法。
- eval summary记录adapter_dir/candidate_files/counts/scoring等，但同一路径先valid后test可能覆盖summary；需要的两个split以各自已保存metric与原日志绑定，不假定一份最后summary包含两次评估。
- Amazon [protocol.yaml](F:/Projects/llamarec/.agent/cross_dataset_validation/protocol.yaml)中旧train-only流行度说明与当前冻结Methods及[candidate_sets.py](F:/Projects/llamarec/src/eval/candidate_sets.py:351)的full_sequences实现不同。这是历史执行来源核对项，不以旧文档覆盖当前冻结协议，也不据此新增泄漏或机制结论。

### 3.6 RUN_METADATA裁决

**PARTIALLY_CLOSE**。2处物理marker均不能整体关闭；8族各含本地已知信息和待补绑定。6类已有事实可直接整理；历史原件的补充按B类办理，没有已证实必须重跑的metadata项。若最终发现某些版本/实参从未保存，先判断其是否可诚实披露为未知而不影响已冻结的有限结论（C），不是自动转D。重新训练也不能证明旧run当时用了什么。

后续获授权时，先更新来源/字段证据控制，再判断Methods是否确需一两句配置或出处同步；Results、Discussion、Limitations及各冻结数值无需随之重写。

## 4. BOOTSTRAP_PROVENANCE closure matrix

### 4.1 已定位到哪里，尚未闭合哪里

**当前分类B：RECOVERABLE_WITH_MANUAL_CONFIRMATION；关闭状态PARTIAL。**

已经定位负责配对预测和重采样的候选原生成脚本：
[seed42_deep_analysis.py](F:/Projects/llamarec/.agent/exposure_scaling/alignment/commands/seed42_deep_analysis.py)及[包装命令](F:/Projects/llamarec/.agent/exposure_scaling/alignment/commands/seed42_deep_analysis.sh)。本轮仅阅读。脚本虽自称“不训练”，其main仍会计算新的bootstrap；`--reuse-existing`仅复用配对CSV，仍调用重采样，故也未执行。

当前数值路径可追溯到：
`paper/tables/{specialist_multitask,hard_candidate}.csv`
← 冻结`final_evidence/tables`
← [build_final_evidence.py](F:/Projects/llamarec/.agent/exposure_scaling/final_evidence/build_final_evidence.py:63)的BINARY_BOOT/RANK_BOOT常量。

BINARY_BOOT保存6条二分类val/test指标记录；RANK_BOOT保存18条k5/k20/k50、val/test、三指标记录。它们是已冻结数值的导出，不是调用原summary实时读取重采样；现有常量没有绑定原预测哈希、实际命令和脚本版本。因此“冻结表数值有来源”与“原始统计生成链唯一闭合”是两回事。

本地同名CSV位于[临时目录](F:/Projects/llamarec/.agent/pytest_tmp_seed42_deep_analysis_fix/binary_bootstrap_summary.csv)及另一旧临时目录，内容均仅`status / MISSING`；临时README记录requested replicates为3，manifest中预测与trainer_state等为MISSING。它们是本地缺资产检查的产物，不能充当原5000次结果。默认输出根`R/.agent/exposure_scaling/analysis_handoff`当前本机没有对应原资产。

### 4.2 十个问题的逐项回答

| 问题 | 当前可追溯事实 | 未闭部分 / 最小动作 |
| --- | --- | --- |
| 1. 两个summary由哪个脚本生成？ | seed42_deep_analysis.py负责写binary_bootstrap_summary.csv和ranking_bootstrap_summary.csv；最终论文导出另由build_final_evidence.py硬编码常量形成 | 需原summary与生成时脚本版本/日志，才能确认冻结常量来自哪次该脚本运行，而非只认同名文件 |
| 2. 输入是什么？ | Y96/M96二分类；N96/M96 k5、k20、k50排序的valid/test预测，先按目标配对再成CSV；路径见4.3 | 实际选中的优先/备用输入分支、文件版本和是否有CLI OUT覆盖需原manifest/log |
| 3. prediction-level assets能否定位？ | 可以定位精确候选路径和7份当前论文CI所需的配对CSV文件名 | 本地未取得正式输入内容；toy/popularity预测和MISSING占位不能替代。优先从原分析机器取配对CSV，不重推理 |
| 4. 为何unit是user？ | group_indices按user_id分组；bootstrap_rows有放回抽取相同数量用户，将每个被抽用户的全部配对行带入两模型；可保留同用户多个Y目标的组内关联 | 这是代码定义，不是其已在原数值那次运行使用的独立证明；也不证明不同用户完全独立 |
| 5. bootstrap seed有留存吗？ | 脚本常量20260902；binary valid用基数，test加10000；ranking另加k5=0/k20=1000/k50=2000偏移；使用random.Random | 当前脚本级A；实际历史执行版本绑定B。不能把训练seed42或候选seed42写成bootstrap seed |
| 6. CI方法是什么？ | percentile：排序后线性插值百分位，位置(n-1)×p/100，取2.5和97.5；不是BCa | 方法级可恢复；仍缺数值到原执行的绑定 |
| 7. 5000来自哪里？ | 用户附件将5000列为已有事实；Python DEFAULT_BOOTSTRAPS=5000；sh环境BOOTSTRAP_REPLICATES默认5000，CLI允许覆盖 | 保留“用户报告/脚本默认5000”与“本地独立证实实际5000”的区别。原summary的replicates字段及README/实际命令才能闭合；本地3次MISSING测试不算 |
| 8. F1/Accuracy threshold=0.5可追溯吗？ | 分数>=0.5为正类，脚本显式计算并导出threshold；[binary_metrics.py](F:/Projects/llamarec/src/eval/binary_metrics.py)定义正类F1和Accuracy | 代码级可以；需原summary/版本将该阈值绑定到冻结输出，不改当前阈值或重新择阈值 |
| 9. ranking按user/request一组采样吗？ | 仍按user_id分组。当前合法N每split每用户一个目标时与request级一对一，但代码没有独立request bootstrap；每次共享重采样两模型相同用户 | 不按候选item独立抽样；输入未取回，实际重复目标/缺失配对尚不能核验 |
| 10. 输出能唯一关联现有provenance吗？ | 论文表到冻结常量的链存在，测试确认复制关系；源码统计逻辑存在 | 不能。缺原summary、有效输入、实际命令/版本的唯一关联，保留marker |

### 4.3 输入定位与最小配对文件

令`Y=R/outputs/y/movielens-1m/exposure_y_s12000`，
`N=R/outputs/n/movielens-1m/exposure_n_s12000`，
`M=R/outputs/m/movielens-1m/exposure_m1_s24000`。
`{valid,test}`代表两个既有split。

| 对象 | 脚本实际写明的输入选择顺序 |
| --- | --- |
| binary Y96 | 优先`Y/popmatch_eval_valid_only/y_{valid,test}_predictions.jsonl`，备用`Y/popmatch_eval/y_{valid,test}_predictions.jsonl` |
| binary M96 | 优先`M/popmatch_eval_valid_only/m_y_{valid,test}_predictions.jsonl`，备用`M/popmatch_eval/m_y_{valid,test}_predictions.jsonl` |
| k5 N96 | 优先`N/popmatch_eval/n_{valid,test}_predictions.jsonl`，备用`N/popmatch_eval_valid_only/n_{valid,test}_predictions.jsonl` |
| k5 M96 | 优先`M/popmatch_eval_valid_only/m_n_{valid,test}_predictions.jsonl`，备用`M/popmatch_eval/m_n_{valid,test}_predictions.jsonl` |
| hard N96 | `R/outputs/phase2a/current96_ranking_robustness/n_k0_{k20,k50}_seed42/n_{valid,test}_predictions.jsonl` |
| hard M96 | `R/outputs/phase2a/current96_ranking_robustness/m1_{k20,k50}_seed42/m_n_{valid,test}_predictions.jsonl` |

另读取processed preference/next_item valid/test元信息用于补充配对属性，原始ratings/metadata用于切片。关闭当前正文CI不要求收集切片分析全部文件。

若原配对CSV已保存，当前论文CI所需最小集合为：
- `<实际OUT>/binary_predictions_y96_m96_valid.csv`，1份。
- `<实际OUT>/ranking_predictions_{k5,k20,k50}_{valid,test}.csv`，6份。
- 合计7份，替代相应两模型共14份原JSONL，两个集合不必都索取。若配对CSV缺失，可先提供原JSONL供后续获授权的来源/配对核验；这不等于获准重采样。
- 原二分类test配对CSV为第8份，仅在需要完整历史链审计时再取；不因存在test常量就在当前论文补写Y test CI。
- `<实际OUT>`默认是`R/.agent/exposure_scaling/analysis_handoff`，但可由CLI覆盖，不能把默认目录说成原执行已确认目录。

### 4.4 源码方法与完整性边界

源码定位：[分组与重采样](F:/Projects/llamarec/.agent/exposure_scaling/alignment/commands/seed42_deep_analysis.py:487)、[binary分析](F:/Projects/llamarec/.agent/exposure_scaling/alignment/commands/seed42_deep_analysis.py:505)、[ranking分析](F:/Projects/llamarec/.agent/exposure_scaling/alignment/commands/seed42_deep_analysis.py:775)、[百分位](F:/Projects/llamarec/.agent/exposure_scaling/alignment/commands/seed42_deep_analysis.py:1207)。

- 二分类差值为M1-96 minus Y96；排序为N96 minus M1-96。沿用冻结差值与CI，不反向重算。
- AUC用rank-sum并对同分平均秩；只有单一类别的重采样可产生None，脚本过滤无效metric差值。因此“requested 5000”不自动证明每项指标有5000个有效draw；先读取原输出/报告是否记录有效次数，未记录则如实说明，不补算。
- 脚本可import当前binary_metrics，也有本地fallback；当前源码两者定义可见，原执行版本和import路径仍需留证。不是凭当前依赖版本复原过去环境。
- ranking使用HR@1、NDCG@5以及1/rank的MRR；相同得分时稳定排序可能依赖候选顺序，故候选顺序/预测输入是provenance的一部分。
- 二分类配对键为(user_id,target_movie_id或movie_id,label)，排序为(user_id,ground_truth_movie_id或target_movie_id)。使用字典和共同键交集，不自动断言全覆盖或键唯一；若原数据有重复键会存在覆盖风险，但本轮没有原输入，不能宣称实际发生丢样本。
- 排序CSV记录same_candidate_order，却不等于代码已强制所有行一致。后续仅核验既有输入的键/覆盖/顺序，不在本轮重算任何区间。
- p_delta_gt_0是重采样差值大于0的比例；不升级为新p-value、等价性检验或跨seed显著性。
- Git历史定位到2026-09-02的初稿、CSV复用和指标修正提交，以及09-03冻结导出提交；仅证明代码演化存在，不能证明采用了哪个commit运行。优先实际工作树快照/原运行记录，不checkout覆盖。

### 4.5 关闭条件及禁止替代

完整A类关闭需“原summary + 生成脚本版本 + 对应输入 + 实际command/config”共同存在，并能与冻结表逐记录关联；核对可用原输出字段和已有哈希，不执行bootstrap。原有哈希若存在优先复用；本轮新算文件哈希只能标识现在拿到的文件，不能伪造过去已有的绑定。

当前先按B向原分析机器索取。只有人工确认原始链确实不能恢复，才按C考虑谨慎披露或降级无法追溯的inferential claim，并另请用户授权；本轮不降级正文。若用户要求通过重新bootstrap或补算未保存指标建立新的分析链，则为D：WOULD_REQUIRE_NEW_EXPERIMENT，且是新的统计证据，不是旧provenance已恢复，本轮禁止。

bootstrap描述固定已训练模型的evaluation-sample uncertainty；seed42/43/44 mean/std描述training-run variability。两者不能互代，也不能借来源关闭获得跨seed显著性。

## 5. METHOD_CITATIONS closure matrix

### 5.1 七项实质引文映射

本轮完整核对当前[Methods](F:/Projects/llamarec/paper/modules_parts/methods/training_setup.md)、[library.bib](F:/Projects/llamarec/paper/references/library.bib)、[citation_inventory.md](F:/Projects/llamarec/paper/references/citation_inventory.md)、[citation_registry.json](F:/Projects/llamarec/paper/references/citation_registry.json)、[citation_claim_map.md](F:/Projects/llamarec/paper/references/citation_claim_map.md)，并定向核对[primary_source_notes.md](F:/Projects/llamarec/paper/references/primary_source_notes.md)和[旧bib_candidates.bib](F:/Projects/llamarec/.agent/paper_writing_submission/refs/bib_candidates.bib)。只使用既有资产，不联网查文献。

计数单位是“已有Methods陈述需要补的引文映射”，不是论文数量。7项中，1项READY、6项NEEDS_MANUAL_CONFIRMATION；后6项当前均缺对应主引用资产。若用户已有正式材料可覆盖多个陈述，后续按真实来源复用，不强凑7篇。没有“已核准主来源、仅缺录入bib”的独立项，因此本轮NEEDS_EXISTING_BIB_ENTRY为0。

| Location | Statement | Citation needed? | Existing source | Bib key | Status | Planned action |
| --- | --- | --- | --- | --- | --- | --- |
| C01 training.p01首句，中英两版 | 使用Llama-3.2-3B-Instruct | 是，model citation | 配置证实模型名；现有refs无对应Meta Llama 3.2官方/技术主资产 | 无已核实key | NEEDS_MANUAL_CONFIRMATION | 请求用户已有对应版本官方来源/正式技术记录；先核身份与覆盖，不从常识补Llama 3.x书目 |
| C02 training.p01第二句 | Low-rank adapters / 低秩adapter | 是，standard method citation | TALLRec等笔记提到使用LoRA，不是LoRA原始来源 | 无已核实key | NEEDS_MANUAL_CONFIRMATION | 取得用户已有LoRA原始材料；rank16/alpha32等数值仍由本项目配置证明 |
| C03 training.p01首句 | QLoRA、4-bit NF4冻结底座 | 是，standard method citation | 现有库未见QLoRA主bibliography条目 | 无已核实key | NEEDS_MANUAL_CONFIRMATION | 取得对应主来源后映射QLoRA/NF4方法身份；实际量化设置另需run绑定 |
| C04 datasets.p01首句 | MovieLens-1M数据来源 | 是，dataset citation | 数据处理规模与路径有证据，主学术条目缺失 | 无已核实key | NEEDS_MANUAL_CONFIRMATION | 核对能正式说明MovieLens来源且适用于1M的既有主资产，不把处理后计数归给原论文 |
| C05 datasets.p02首句 | Amazon Musical Instruments来源；已有协议表明2023 5-core版本 | 是，dataset citation | [dataset_source_decision.md](F:/Projects/llamarec/.agent/cross_dataset_validation/dataset_source_decision.md)证实选用版本/文件，不是学术引用 | 无已核实key | NEEDS_MANUAL_CONFIRMATION | 取得与Amazon Reviews 2023/该版本相符的既有正式来源，不误用另一年份数据集文献 |
| C06 baseline.p01首句 | SASRec的物品/位置嵌入与因果序列编码 | 是，standard method citation | S08；原始SASRec来源已在引用库并有定向原文核验 | kang2018sasrec | READY | 后续只在首句两种语言补映射并同步registry实际位置；不把原始论文用于证明仓库全物品CE |
| C07 statistics.p01首句及percentile定义 | 用户级配对bootstrap与百分位区间 | 是，standard method citation | 现有脚本支持实现；reference资产无已核实bootstrap标准主条目 | 无已核实key | NEEDS_MANUAL_CONFIRMATION | 请求既有标准主参考；用户分组及实现细节仍由代码/原运行证明，不能只补引文就关闭BP01 |

### 5.2 不机械堆引用的范围裁决

| Location | Statement | Citation needed? | Existing source | Bib key | Status | Planned action |
| --- | --- | --- | --- | --- | --- | --- |
| training.p01的r/alpha/dropout、max length、投影列表 | 本实验超参数 | 否；需要配置及run metadata | A1、3.5 | 不适用 | NO_CITATION_NEEDED | 不让LoRA/QLoRA引用承担实际参数证据 |
| training.p02-p04及exposure_definition | response-only loss、1:1交错、累计steps/每任务曝光 | 不为本文设置伪造引用 | 当前源码、命令与计数审计 | 不适用 | NO_CITATION_NEEDED | 恢复实参；保持预期/实际区分 |
| temporal_split及task_definition | strict earlier、同时间桶歧义跳过、H10、本文Y/N目标 | 本文定义，不因相似协议就借引文 | 既有定义/处理实现 | 不适用 | NO_CITATION_NEEDED | 保留清晰定义和provenance |
| evaluation.p01 | AUC/F1/Accuracy、HR@1/NDCG@5/MRR名称及常规定义、固定阈值 | 当前写法不要求每个名称单独补创始文献 | 指标代码与当前定义 | 不适用 | NO_CITATION_NEEDED | 不把指标命名当成创新；若将来新增理论/估计性质主张，需另审 |
| evaluation.p02 | 本文Random/PopMatch候选构造 | 不是借用名称的外部方法，不需名字相似的引用 | candidate_sets.py；冻结Methods | 不适用 | NO_CITATION_NEEDED | 记录构造、数据范围、候选路径和限制；不包装PopMatch新方法 |
| evaluation.p03 | 本文独立构造k20/k50候选、非嵌套及共享顺序 | 本文实验定义 | 冻结协议、原候选待回收 | 不适用 | NO_CITATION_NEEDED | provenance核实；不把已有采样文献当自己候选文件的证明 |
| Intro/RW已有sampled-evaluation讨论 | 采样评估可能改变模型比较 | 该类外部判断需要已有对应引文；当前Methods未扩写此叙述 | S10/S11/S12已在Intro/RW使用 | krichene2020sampled；canamares2020target；dallmann2021sampling | OUT_OF_SCOPE | 可复用但无需迁入Methods；本轮不改Intro/RW |
| training.p01的transformer blocks | 对所用底座组件的泛称，非独立Transformer方法介绍 | 当前由底座身份覆盖，不新增一套方法综述 | C01所需模型主来源 | 不适用 | NO_CITATION_NEEDED | 不因出现Transformer一词就增补无陈述负担的引用 |
| Methods没有的BPR方法陈述 | BPR | 否，当前无此方法陈述 | 无 | 不适用 | OUT_OF_SCOPE | 不造新缺口、不追加BPR介绍 |
| statistics.p02 | MS96 equal-weight mean、sample std、n=3/ddof=1及其边界 | 本研究汇总定义，不新增外部理论主张 | 当前MS96证据与测试 | 不适用 | NO_CITATION_NEEDED | 不改成跨seed检验；不以bootstrap引文替代 |

### 5.3 拟用或可复用来源的身份

以下书目信息来自现有库及已保存核验记录；本轮没有重新联网核验，也不声称通读原文。

| 来源 | Canonical title | Authors | Year / key | Already used | Primary / 可支持范围 |
| --- | --- | --- | --- | --- | --- |
| S08，唯一直接Methods映射候选 | Self-Attentive Sequential Recommendation | Wang-Cheng Kang; Julian McAuley | 2018；kang2018sasrec；DOI 10.1109/ICDM.2018.00035 | intro.p02；rw.tasks.p01；rw.evaluation.p02 | 原始论文；已有作者PDF的III.E/IV.D等定向核验。支持SASRec方法身份，不支持将本仓库full-item CE说成原论文相同损失；原文训练/评估设置与本实现需区分 |
| S10，仅说明已有可复用eval来源 | On Sampled Metrics for Item Recommendation | Walid Krichene; Steffen Rendle | 2020；krichene2020sampled；DOI 10.1145/3394486.3403226 | intro.p04；rw.evaluation.p01 | 原始研究；本地核验范围为官方摘要及同作者2021扩展文本，不冒充已获KDD全文。支持采样度量比较的风险，不是PopMatch来源 |
| S11，仅说明已有可复用eval来源 | On Target Item Sampling in Offline Recommender System Evaluation | Rocio Canamares; Pablo Castells | 2020；canamares2020target；DOI 10.1145/3383313.3412259 | intro.p04；rw.evaluation.p01 | 原始研究；target set含被评分的候选全集，不只正目标；按已保存核验范围复用 |
| S12，仅说明已有可复用eval来源 | A Case Study on Sampling Strategies for Evaluating Neural Sequential Item Recommendation Models | Alexander Dallmann; Daniel Zoller; Andreas Hotho | 2021；dallmann2021sampling；DOI 10.1145/3460231.3475943 | intro.p04；rw.evaluation.p01 | 原始案例研究；支持该研究范围的采样敏感性，不证明本项目全部协议结论 |
| C01模型主来源 | 未从已有资产核实，不填推测题名 | 未核实 | 未核实；无key | Methods仅写模型名，无来源映射 | MISSING_PRIMARY_CITATION_ASSET |
| C02 LoRA主来源 | 未从已有资产核实 | 未核实 | 未核实；无key | 其他论文使用LoRA的二手笔记不算 | MISSING_PRIMARY_CITATION_ASSET |
| C03 QLoRA主来源 | 未从已有资产核实 | 未核实 | 未核实；无key | 无主映射 | MISSING_PRIMARY_CITATION_ASSET |
| C04 MovieLens主来源 | 未从已有资产核实 | 未核实 | 未核实；无key | 仅数据集名称/处理说明 | MISSING_PRIMARY_CITATION_ASSET |
| C05 Amazon版本主来源 | 未从已有资产核实 | 未核实 | 未核实；无key | 2023版本选择文件不等于书目核验 | MISSING_PRIMARY_CITATION_ASSET |
| C07 bootstrap主来源 | 未从已有资产核实 | 未核实 | 未核实；无key | 仅统计实现说明 | MISSING_PRIMARY_CITATION_ASSET |

TALLRec/ITDR等论文中的LoRA使用描述不能代替LoRA/QLoRA原始引用；数据集homepage、download脚本与processing记录也不能自动当作学术引文。缺失项以B类待用户提供其已有主资产；若用户没有现成材料，未来检索须另获授权，本轮不搜。

### 5.4 引用关闭的未来最小动作

先核六项主资产的准确身份、版本和句子支持范围，再在Methods对应中英同一句添加必要映射；SASRec可直接用现有key。只录入确实缺失且已核实的bib条目，同步citation_registry/citation_claim_map的真实使用位置和核验范围。不重写引言、相关工作或方法叙事，不把本项目配置和样本数量“引用化”。本轮上述动作均未执行。

## 6. Minimal user-supplied evidence needed

### 6.1 请求原则与精确文件模板

机器名无法从现有库确定的，明确写“原运行机器待确认”，不猜主机。seed44有另一台机器这一事实沿用用户说明。下表的R和run/OUT均使用3.2-3.3、4.3中明确的路径；第一步确认真实根/实际OUT即可，不要求同步整个outputs、全部日志、训练数据或权重。

请求按“先小清单、后只补缺字段”执行。当前只提出请求清单，不远程连接、不导出或复制任何资产。

定义最小包，均为既有文件或其必要字段的只读摘录：
- **T(run,step)**：`<run>/run_summary.json`、`<run>/config_snapshot.yaml`、`<run>/checkpoints/checkpoint-<step>/trainer_state.json`。若CLI覆盖后的batch/accum、实际max_steps、resume/数据跳过信息仍缺，再给该checkpoint既有`training_args.bin`的可信可读字段导出或当时训练命令/log片段。不要权重、optimizer.pt、scheduler.pt或整个checkpoint。
- **E(eval)**：`<eval>/evaluation_summary.json`及论文实际使用split的`valid_metrics.json`/`test_metrics.json`；Base改为`<eval>/run_summary.json`。只有模型配置、revision、候选绑定不在上述文件时，再给既有`evaluation_config_snapshot.yaml`或实际命令片段。文件名须按原目录已有文件确认，不为凑清单新造summary。
- **S(run)**：SAS `<run>/run_summary.json`与`{valid_metrics.json,test_metrics.json}`；若其中已经包含实际字段，不额外索取不存在的config_snapshot。若历史版本确有快照且关键字段仍缺，才补该既有文件。
- **Q(protocol)**：3.2指定候选文件的已有生成manifest/哈希/记录数；本地ML k5已有原件，优先仅确认远端身份是否一致。hard和Amazon若没有既有哈希或顺序记录，再提供论文实际使用的候选JSONL，不重新生成。

| 优先级 / Machine | Run | Exact file/path（按模板精确展开） | Why needed / 不必重复的部分 |
| --- | --- | --- | --- |
| P0 原seed42分析机器，主机及实际OUT待确认 | 原paired bootstrap那次分析 | `<实际OUT>/binary_bootstrap_summary.csv`、`ranking_bootstrap_summary.csv`、`README.md`、`artifact_manifest.csv`中有关输入/输出/命令的部分；当时script版本或源码快照、实际CLI/环境覆盖片段 | 先确认冻结常量的原summary、5000实际次数、seed和输入分支。无需全部切片报告；如果文件名不存在，说明原命令/目录即可 |
| P0 同一分析机器 | 论文已用的seed42 CI | `<实际OUT>/binary_predictions_y96_m96_valid.csv`及`ranking_predictions_{k5,k20,k50}_{valid,test}.csv`，7份 | 输入级来源闭合；优先原配对CSV，可用4.3相应原JSONL替代，不要求两套或重推理 |
| P0 用户已有文献存储位置，待确认 | C01/C02/C03/C04/C05/C07 | 对应Llama-3.2、LoRA、QLoRA、MovieLens、Amazon Reviews 2023、bootstrap的已有主文档或正式来源记录及BibTeX；本地路径未提供，不能编造 | 六项缺主资产；只需足以核实身份和支持句子的材料。不要求新检索；SASRec无需再供 |
| P1 原seed42训练机器 | Y24/Y48/Y96、N24/N48/N96/N200、M1-48/M1-96 | 3.3九个明确run各T(run,3000/6000/12000/25000/24000对应值)；各自实际k5 E目录按原日志确认 | batch/QLoRA实参、真实checkpoint与停止/续训；run若共享同一配置版本，可给共同快照加明确覆盖表，不重复相同文件 |
| P1 seed43原机器 | Y96/N96/M1-96 | `R/outputs/{y,n,m}/movielens-1m/{exposure_y_s12000_seed43,exposure_n_s12000_seed43,exposure_m1_s24000_seed43}`按任务一一对应的T包；各`popmatch_eval`的E包 | 原实参与结果绑定；已有validation/test_summary及artifact_index无需重供 |
| P1 seed44另一台原机器 | Y96/N96/M1-96 | 与上一行相同一一对应规则，seed43改seed44，T步数12000/12000/24000；各`popmatch_eval`的E包 | 不因本机路径不可见写实验不存在；只收元数据，不收adapter权重 |
| P1 各对应seed评估机器 | N96/M1-96 hard-k20/k50 | 3.3两个hard目录规则下的E包及Q(ML-K20/K50)；相同候选只提供一次 | adapter→候选→各split metric绑定；不再索取独立训练记录，继承N96/M96 |
| P1 原seed42 SAS机器 | 仅S47/S94/S188/S391 | `R/outputs/baselines/movielens-1m/alignment_sasrec_s{47,94,188,391}/`各S包 | actual optimizer_steps/batch/训练池/stop及200000短尾；排除ML s23、canonical、debug及历史高曝光 |
| P1 原Amazon云运行机器 | Base/Y/N/M/SAS | Base为3.3两个eval根的已有Base E；Y/N/M训练根各T（checkpoint名按原文件确认）；Y/N/M的`<run>_{random,popmatch}_k5_eval`各E；SAS Pop根S及`R/outputs/baselines/amazon-musical-instruments/sasrec_exp_match_k5_seed42_s23_random_eval`已有test记录 | 先补已报告test链；不为正文未用的validation新增评估。Base与A共用，不重复 |
| P1 原Amazon配置/候选机器 | 对应上述运行 | `R/configs/experiment.amazon_local.generated.yaml`和`R/configs/{y,n,m}.amazon_local.generated.yaml`中实际用到的文件；Q(AM-RANDOM/POP) | 恢复真实配置继承、消费与流行度来源；当前本机没有这些生成快照 |
| P2 对应模型/环境原机器 | 全部共享底座的正式run | 已有base加载日志/缓存revision记录及环境版本清单中的相关部分，实际文件名待用户指认 | 不要求重新构造完整环境；确未保存时明确unknown，先判断是否可披露而非阻断受限结论 |

这里P0/P1/P2是材料回收优先级，不是新实验矩阵。引用主资产路径未提供时诚实记未知，不用模型记忆填一个“精确”文件名。若用户只想先推进有限结论，优先处理P0原bootstrap来源判断；训练实参的完整归档可分批完成。

## 7. 最终关闭裁决与后续结论边界

| 项目 | Closure status | 当前能做的最小后续动作 | 不能据此声称 |
| --- | --- | --- | --- |
| RUN_METADATA | PARTIAL；范围裁决PARTIALLY_CLOSE | 6类事实先整理；8族原实参/停止/候选绑定分批回收；字段不足保留明确unknown | 不能说所有历史运行完全复现；不能以当前默认值证明实际配置 |
| BOOTSTRAP_PROVENANCE | PARTIAL | 原summary、输入、实际命令及版本绑定；当前分类B | 脚本找到不等于原CI数值已独立重现；5000默认不等于本地执行证明 |
| METHOD_CITATIONS | PARTIAL | SASRec已有引用可映射；六项待既有主资产；不做新搜索 | 不能说Methods引用已齐，也不能只给两个marker段落补引用就收工 |
| Evidence provenance closure | NEEDS_USER_INPUT | 先取第6节最小材料，再逐项获授权执行关闭 | 不是READY_FOR_EXECUTION，更不是投稿ready |

### 7.1 是否阻塞未来Conclusion

没有发现必须增加新训练结果才能写出“冻结范围内的描述性经验结论”的科学硬缺口。这样的有限结论只能沿用当前事实层级：MovieLens单seed轨迹、96k三seed描述复现、协议依赖差距、正式四点SAS对照、Amazon排序方向核验，不额外加入机制、正迁移、等价性、跨seed显著性或跨域曝光规律。本轮不撰写这类结论。

RUN实参记录、base revision/软件版本、引用归属主要影响投稿级复现和方法文档完整性，不自动推翻现有点估计，也不必然阻断有限的描述性结论。但BOOT缺失不能一概说成“只差文档”：若以后确认原生成链永远无法恢复，任何依赖精确CI作强inferential判断的未来结论都应暂缓，或经用户批准收窄/降级。当前只是来源待回收，不能直接否定冻结CI，也不能无条件宣布统计依据已充分。

模板与未写模块独立保留：
- **TEMPLATE_UNASSIGNED remains intentionally open.** venue/template尚未确定，本轮不选venue、不下载模板、不调格式或bibliography style。
- Conclusion/Abstract（09/10）继续保持未写；不填placeholder、不改skeleton/draft状态。final检查失败不是本轮必须消除的目标。

### 7.2 什么情况下才属于新实验

| 条件 | 分类 | 诚实后续处理 |
| --- | --- | --- |
| 原JSON/log/config/checkpoint元数据、已有command/哈希仍在其他机器 | B RECOVERABLE_WITH_MANUAL_CONFIRMATION | 只读回收；不是新实验，不要求重跑 |
| 只缺未保存且不影响有限结论的版本/超参数记录，已确认无法恢复 | C NOT_RECOVERABLE_BUT_NONBLOCKING_IF_DISCLOSED | 披露unknown并保留复现限制；另获授权改控制/方法说明 |
| summary数值留存，但原统计链经确认无法恢复；保留受限描述或降级inferential解释 | C NOT_RECOVERABLE_BUT_NONBLOCKING_IF_DISCLOSED | 先由用户决定披露/降级范围，本轮不改稿；不假装CI已获完整复现 |
| 原预测真正丢失，为取得新的prediction assets而重新推理 | D WOULD_REQUIRE_NEW_EXPERIMENT | 需要新授权；产出是新的评估链，不是恢复旧执行记录 |
| 候选原件真正丢失，重新生成候选 | D WOULD_REQUIRE_NEW_EXPERIMENT | 即使seed相同也不能冒充旧字节资产；本轮禁止 |
| 原bootstrap来源无法恢复，要求重新bootstrap/重算CI/p-value或未保存指标 | D WOULD_REQUIRE_NEW_EXPERIMENT | 属于新增统计分析，本轮禁止；不能用“不是训练”绕开禁令 |
| 为统一已缺的历史实参而重训/续训 | D WOULD_REQUIRE_NEW_EXPERIMENT | 新run不能证明旧run实参；不是本轮恢复metadata的默认路径 |
| 方法主引用缺失 | B RECOVERABLE_WITH_MANUAL_CONFIRMATION | 先请求用户已有材料；若必须新检索另行授权。文献检索不是模型实验，但本轮同样禁止 |

当前没有确认成立、必须执行的D项。上述均为条件分支，不是补实验建议或执行队列。

### 7.3 未来执行顺序与验收边界

1. 用户确认原运行机器/实际OUT并提供最小材料；先核原文件身份、有效内容及当前冻结结果绑定，排除MISSING、toy和重复摘要。
2. 逐字段登记“实际记录/当前配置/冻结汇总/仍未知”；任何冲突停在对应字段，不改结果故事或擅自选替代run。
3. 引用仅在确证的Methods句子做双语映射及reference控制同步；统计仅整理已有执行参数，不执行重采样。
4. 获得新的明确修改授权后，才可修改Methods的必要出处/配置说明及相关证据控制文件；本轮不替用户预先授权。
5. 只有对应证明链齐全才删除对应marker；若仅局部齐全，保持未闭并缩小问题描述。旧build镜像在未来获准装配时同步，不把旧历史记录改造成新执行事实。

## 8. 能力使用与验证记录

### 8.1 Capability-use audit

| 能力 | 本轮用途 | 未执行的边界 |
| --- | --- | --- |
| using-research-writing | 识别为论文前置只读审计，不是改稿或选新故事 | 未进入章节写作、brainstorming或改RQ |
| paper-orchestration | 在本计划集中任务范围、矩阵、验收与交付 | 不改progress/notes，不创建额外paper计划或新任务 |
| peer-review | 核对claim门控、证据层级、引用负担和可恢复性 | 不把缺记录当新科学结论，不扩大冻结论断 |
| statistical-analysis（仅报告审查） | 阅读既有bootstrap定义、配对/分组/百分位、seed和CI来源 | 不执行bootstrap、指标、显著性或等价性计算 |
| verification | 运行指定既有测试及只读check、检查实际文件保护 | 不改测试、旧基线或final状态 |
| 终端/rg/结构化解析/Git只读 | 文件定位、JSON/CSV字段阅读、既有候选行数/SHA256、局部历史定位 | 不访问Wiki，不fetch/pull/reset/checkout，不调用模型或生成候选 |
| apply_patch | 仅编辑本计划与两份.agent管理记录 | 不修改正文、正式证据、引用、图表、manifest、旧build |
| 未使用 | web/Scholar/arXiv、外部文献连接器、训练/推理工具、Wiki工具、模板和整稿生成 | 全部超出本轮授权 |

### 8.2 验证结果

最终只读验证完成，未执行任何闭项或改稿动作。

| 检查 | 实际结果 | 判断 |
| --- | --- | --- |
| `python -B -X utf8 -m unittest discover -s paper/assembly/tests -v` | 47项，46通过、1失败；exit1 | 唯一失败仍为test_preserved_files_and_append_only_literature_freeze，test_ms96_evidence.py:123，首先报rq1_supervision_semantics.md旧哈希冲突；不是全测试通过 |
| `python -B -X utf8 paper/assembly/assemble.py --lang bilingual --check` | exit0；11模块、79对段落、8处待补标记 | 双语结构检查通过，未生成稿件 |
| `python -B -X utf8 paper/assembly/assemble.py --lang bilingual --mode final --check` | exit1；5处三类证据marker、09/10未写标记及draft/skeleton阻止final | 符合当前未闭状态，不能称完成稿通过；TEMPLATE另在控制层有意保持未分配 |
| `python -B -X utf8 tools/stage_guard.py` | exit0；0 errors、0 warnings | 管理记录检查通过，不等于Wiki审计或论文ready |
| `git diff --check -- .agent/current_task.md .agent/stage_state.yaml paper` | exit0；68条既有CRLF转换提示，无其他输出 | 无diff空白错误，不消除行尾提示 |
| 旧MS96保护基线复核 | 57项中52一致，5项不符 | 与R01-R09授权修订后已知情况一致；未改测试/基线 |
| 本次继续恢复点的paper SHA256保护 | 排除8个既有__pycache__文件与本文后191项；交付核对191项全部一致，非计划新增0 | 没有改动恢复点的正文/正式证据/引用/图表/manifest/build/test；本文是唯一新paper计划 |
| 本地证据链接 | 63个去重本地链接，核对存在；单个误写eval源码路径已在本文修正为src/inference | 不把远端候选路径当本地链接，也不因远端不可见说实验不存在 |

旧哈希不符的5项为：results/rq1_supervision_semantics、results/rq2_exposure_response、results/cross_dataset_validation、discussion/external_validity以及evidence/final_novelty_claim_map。既有R01-R09计划记录了授权改动，本轮不回滚、不更新旧测试基线。

哈希时间范围说明：中断前曾在内存记录191项基线；用户中断后该内存快照未延续，本次明确重新建立“继续恢复点”快照并完成对照，不冒充对中断前快照做了完整复核。恢复点多出的8项为既有Python缓存，并非新增论文文件。结合本轮编辑操作范围，实际只编辑本文及两份.agent记录；未执行模型、统计、文献搜索或正式Wiki读写。

## 9. 交付与停止

计划已完成，三类缺口的位置、已有证据、未知项、最小补充和关闭条件已登记。当前总体NEEDS_USER_INPUT仅指未来关闭所需材料，不表示本轮审计未完成。本轮到此停止，不执行计划中的恢复、引用映射、marker删除或稿件修改。
