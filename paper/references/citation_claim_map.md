# 当前双语正文与原文证据映射

日期：2026-09-09。状态：TARGETED_METHOD_CITATION_CLOSURE / APPLIED。用于00-02、related_work parts及指定Methods段落；本地实验结论与项目配置仍由C1-C9/M1-M8支撑。

| 段落 | 已应用的科学表述 | 引用与原文位置 | 不支持的升级 |
| --- | --- | --- | --- |
| intro.p01 / rw.llm.p01 | LLM推荐、零样本对话与排序、推荐调优背景 | S01/04/05题名；S02/03方法 | S05未核hard细节 |
| intro.p02 | 反馈/下一事件问题与共同语言接口 | S07 §2/4；S08 §III.E；S02 §3 | 完整Y/N等同或单一语义机制 |
| intro.p03 | 累计曝光定义及前人任务/数据分析 | M3；S02 §5.6与Appendix C；S15 §4.3 | 先前没有数据曲线、预算不匹配 |
| intro.p04 | 采样策略和候选构造改变比较；任务与数据已有部分联合；提出具体研究问题 | S10官方摘要/扩展稿；S11 §3；S12冻结用途边界；S02/15/21/25 | 领域空白、首次完整联合、全因子因果，或Dallmann专属实验细节转移 |
| intro.p05 / intro.p06 | 已冻结研究设置与有限发现，p06保持原样 | 既有C1-C8/M3，MS96仍保留 | 新seed或Amazon完整缩放 |
| intro.p07 / contributions.p01-p04 | C2主、C4次、C3支撑、C1界定 | 既有事实+story_and_novelty_freeze | 平均力度的新模型/首创叙事 |
| rw.llm.p02 | P5语言输入输出、TALLRec指令与YesNo、InstructRec多接口 | S02 §3；S03 §2；S16 §2 | 所有指令推荐统一loss或任务 |
| rw.tasks.p01 | 显式评分拟合、隐式偏好/置信度、下一物品 | S06 Basic MF Eq1-2；S07 §2/4；S08 §III.E | 未交互等于明确不喜欢 |
| rw.tasks.p02 | P5 >=4及next-item，ITDR不同任务；本文完整形式及桥接 | S02 §3；S15 §3；C1/M1/M4 | 预测问题区分首创 |
| rw.unified.p01 | P5专家及实例量，ITDR两类消融，Open权重/低数据单多域 | S02 §5.6/Appendix C；S15 §4.3；S21 §6.3.2/B.5 | 前人只孤立研究或已做完整曝光网格 |
| rw.unified.p02 | Penha辅助任务上限与域专家不同于Y/N目标累计曝光 | S25 §5/7 Fig4；S22 §6 | Penha非LLM或单点；域/任务专家混同 |
| rw.evaluation.p01 | 有限采样次序命题、采样策略可靠性、正确target set、已有LLM hard | S10/S11；S12 Pereira冻结用途边界；S16 §3.3 | 所有指标极限、非嵌套候选的纯大小因果、Dallmann专属实验细节 |
| rw.evaluation.p02 | 基线复现与调优、标准化评价下传统基线竞争力、TALLRec同K曲线、序列重复训练，本文四点累计轨迹 | S08；S13 Milogradskii冻结用途边界；S14 Shehzad/Jannach冻结用途边界；S03 §3；S23 §IV.B-C；C7/M3/M7 | 新文献评价SASRec、first budget-aware、不同量纲倍数、总成本公平 |

## ICECAI 2026 R-BALANCED Reference Closure (2026-09-11)

| ID | Old source | Action | New source | Scientific role | Claim locations | Historical-meaning guard |
| --- | --- | --- | --- | --- | --- | --- |
| R1 / S16 | 2023 InstructRec preprint | Same-work formal upgrade | TOIS 2025, DOI 10.1145/3708882 | Existing instruction interfaces and difficult-candidate precedent | rw.llm.p02; rw.evaluation.p01 | Publication year is not new scientific evidence |
| R2 / S23 | 2023 sequential-scaling preprint | Same-work formal upgrade | RecSys 2024, DOI 10.1145/3640457.3688129 | Data-pool size and repetition precedent | rw.evaluation.p02 | Scientific role unchanged |
| R3 / S12 | Dallmann et al. 2021 | Replace | Pereira et al. 2025, DOI 10.1145/3705328.3748086 | Sampling-strategy reliability and model-ranking sensitivity | intro.p04; rw.evaluation.p01 | No transfer of full/uniform/popularity or study-specific details |
| R4 / S13 | Dacrema et al. 2019 | Replace | Milogradskii et al. 2024, DOI 10.1145/3640457.3688073 | Baseline replicability and careful tuning | rw.evaluation.p02 | Do not imply SASRec evaluation |
| R5 / S14 | Rendle et al. 2022 | Replace | Shehzad and Jannach 2025, DOI 10.1145/3705328.3748156 | Standardized evaluation and competitive tuned conventional baselines | rw.evaluation.p02 | Not the source of this repository's SASRec implementation |
| rw.synthesis.p01 | 部分重合研究到具体模型关系问题 | 前文来源+既有C1-C7/M3/M5 | Agent过程、搜索未发现式缺口 |

## Methods Citation Closure (2026-09-09)

本轮只核验既知方法引用缺口，没有扩展检索新颖性文献，也没有改变论文故事。所有写入正文的新增来源均为 HIGH；来源仅支撑其对应的方法或数据身份，不替代本地 artifact 对项目配置、处理后规模和实际统计执行的证明。

| ID | Statement | Primary source | Why it supports | Bib key | Confidence |
| --- | --- | --- | --- | --- | --- |
| C01 / S26 | 使用 Llama-3.2-3B-Instruct 底座 | Meta 官方 Llama 3.2 model card，Model Information / Model Architecture | 官方文档列出 instruction-tuned 3B 模型；只支撑模型身份，不支撑本项目训练配置 | meta2024llama32 | HIGH |
| C02 / S27 | LoRA 是冻结预训练权重并训练低秩增量的适配方法 | Hu et al., ICLR 2022，Abstract / §1 / §4.1 | 原始 LoRA 论文直接定义低秩适配；不支撑本项目 rank、alpha、dropout 或 target modules | hu2022lora | HIGH |
| C03 / S28 | QLoRA 在冻结的 4-bit 量化底座上训练 LoRA，并引入 NF4 | Dettmers et al., NeurIPS 2023，官方摘要 / §3 | 原始 QLoRA 论文直接覆盖 4-bit frozen base、LoRA 与 NF4；不支撑本项目具体运行参数 | dettmers2023qlora | HIGH |
| C04 / S29 | 数据源为 MovieLens-1M | Harper and Konstan, ACM TiiS 2015；GroupLens 官方引用页 | GroupLens 指定的 MovieLens 数据集来源；不支撑本项目处理后划分和样本数 | harper2015movielens | HIGH |
| C05 / S30 | Amazon 数据源为 Amazon Reviews 2023 的 5-core Musical Instruments | Hou et al., ACL 2026；官方数据集页和 5-core 页面 | 论文与官网确认 Reviews 2023、5-core 处理及 Musical Instruments 子集；不支撑本项目处理后计数 | hou2026amazonreviews | HIGH |
| C06 / S08 | SASRec 提供基于自注意力的序列推荐基线 | Kang and McAuley, ICDM 2018，§III.E / §IV.D | 原论文支撑模型和下一物品任务身份；不支撑本仓库 full-item CE、batch size 或运行制度 | kang2018sasrec | HIGH（既有核验） |
| C07 / S31 | bootstrap 重采样与 percentile confidence interval 有标准统计依据 | Efron and Tibshirani, 1993，出版社目录中的 bootstrap percentile interval 章节 | 标准专著支撑 bootstrap 与百分位区间；pairing、用户级采样、replicates、seed 和执行溯源仍由本地证据负责 | efron1993bootstrap | HIGH |

正文落点严格限定为 methods.training.p01、methods.datasets.p01、methods.datasets.p02、methods.statistics.p01 和 methods.baseline.p01；EN/ZH 使用相同 BibTeX 键并保留原 paragraph ID。BOOTSTRAP_PROVENANCE 与 RUN_METADATA 未因方法引用闭环而关闭。
## 登记纪律

31条库存中25条实际入稿。citation_registry.json记录实际段落，BibTeX提供唯一键；每对EN/ZH引用键一致。00-02中的文献证据继续由EVIDENCE注释关联S编号；本轮Methods新增来源由registry与claim matrix绑定，段落注释保留paper_manifest当前已登记的证据ID。literature_gap_registry.json保留原句和原未核理由，另记本轮行动、最终双语文本、证据状态与正文状态。

[原文定位](primary_source_notes.md)、[原文裁决](primary_source_adjudication.md)、[跨Agent对齐](cross_agent_reconciliation.md)是不同证据层；两份原始报告与[旧未采用备份](UNAPPLIED_MANUSCRIPT_EDIT_SNAPSHOT.md)不作为本轮作者源。零处六类引用marker不等于零处实验pending。
