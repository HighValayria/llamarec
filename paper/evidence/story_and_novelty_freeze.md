# 论文中心与新颖性边界冻结

冻结：2026-09-07；00-02应用完成：2026-09-08。决定：**MINOR_REVISE**。依据[跨Agent裁决](../references/cross_agent_reconciliation.md)、[原文裁决](../references/primary_source_adjudication.md)及原有[冻结事实链](source_of_truth.md)。本文件是写作控制，不是新的实验结论。

## Core Thesis

Within the evaluated recommendation-tuning setting, conclusions about recommendation capability and relative model performance are conditional on supervision formulation, cumulative task-sample exposure, and candidate evaluation protocol.

在本研究已评估的推荐调优设置中，关于推荐能力及模型相对表现的结论，取决于监督形式、累计任务样本曝光和候选评估协议。

保留用户建议中心，只收窄适用范围并明确曝光计量。不是三个变量全组合实验，也不是对全领域的因果定律。

## Primary Contribution：C2

**目标任务累计监督对齐下，专家与共享模型的关系随适配曝光改变。**

最强证据是现有MovieLens seed42比较：较高的每任务曝光显著缩小标准k5验证差距，冻结测试仍有N的小幅优势；同一共享adapter的Y侧也有既有配对证据。低曝光关系不能直接当成固定的专家优势。

新颖性候选是“每任务累计曝光对齐 × 专家/共享模型关系 × 已测轨迹”，不是这些组件分别首创。P5已有专家对照与衍生样本量分析；Penha已有新增任务数据上限曲线；ITDR与OpenOneRec已有任务/数据分配部分联合。本文应直接讲对应目标任务累计监督下的关系变化，不靠贬低这些近邻制造差异。

边界：M曝光是混合调度下的预期每任务计数，依赖正确resume data skipping；累计包含重复样本。单seed曲线，现有用户bootstrap只反映评估抽样，不代表训练随机性。MS96保持待处理，不能写跨seed稳定。

## Secondary Contribution：C4

**用四个近似匹配的下游任务曝光点刻画N与SASRec的比较轨迹。**

现有24k、48k、96k、200k运行点显示N排序更强，同时SASRec随监督增加明显改善。贡献在于把相对表现与明确的累计监督运行点联系起来，而非单一少样本胜负。

TALLRec已有K-shot选样预算对齐、SASRec对照和K=1-256曲线。本文累计消费与它的选出样本数不是同一量纲，不能把200k/256当作跨论文曝光倍数，也不能由此声称总成本或预训练公平。这里的“范围扩展”仅指从few-shot选样问题转向本研究明确24k-200k累计下游轨迹，不宣称跨论文优越性。

未观测SASRec反超、外推交叉点或N收敛；不攻击TALLRec的loss，不把本仓库SASRec实现等同原论文配置。

## Supporting Analytical Contribution：C3

**C2得到的关系本身受候选协议限定。**

标准k5验证差距很小，可以与较难候选条件下更大的N优势并存。一般采样敏感性已有Krichene、Cañamares、Dallmann等支持，InstructRec已有LLM困难检索候选评价。本文价值是将这一问题具体作用于较高曝光下的N/M关系解释。

边界：不同hard-k5/k20/k50非嵌套，大小、组成、难度不能分离；不写纯candidate-size因果、随k单调增大的差距规律或新的gap增长框架。PopMatch只是减少目标与干扰项流行度差异的回顾性离线控制，其全序列流行度范围仍按既有方法限制处理。

## Framing Contribution：C1

**监督形式定义预测问题与可观测能力画像。**

评分偏好判断、下一交互选择与桥接排序回答不同问题。P5已含>=4二值化及下一物品接口，ITDR已列不同推荐任务。这是问题界定与本文观察的经验组织，不是首次区分偏好和下一事件。

本研究比较的是完整目标、任务数据、prompt和scoring形式；不能隔离为语义本身造成差异的机制。Y增益减弱与N继续改善分别依各自指标和被测区间描述，不直接比较AUC与HR数值大小。

## Final Research Gap

Existing studies address partially overlapping questions about task formulation, training-data allocation, and candidate evaluation. Building on these connections, we examine how specialist-multitask and LLM-sequential-baseline relationships change with cumulative per-task supervision, and which relationships persist under alternative candidate conditions.

已有研究围绕任务形式、训练数据分配和候选评估考察了部分重合的问题。在这些关联的基础上，本文研究专家与多任务模型、LLM与序列基线的关系如何随累计每任务监督变化，以及哪些关系能在不同候选条件下保持。

这是有具体文献依据的正向问题定义，不再依赖“全领域缺少联合研究”的存在性否定。JOINT_CONDITIONING_COVERAGE的正文状态为REWRITTEN_AND_RESOLVED；领域穷尽性仍未证明。

## Nearest Neighbors

| 工作 | 已有重合 | 本文不同问题 | 核验范围 |
| --- | --- | --- | --- |
| P5 | 统一语言推荐、多任务、>=4/next-item接口、single/multitask及衍生训练实例量 | 目标任务累计曝光对齐下的关系轨迹及候选条件 | Tier1 §3/5.6、arXiv v7 Appendix C/Table16 |
| TALLRec | 推荐适配、few-shot选样曲线、同K SASRec对照 | 四个24k-200k累计下游监督点的next-interaction排序轨迹 | Tier1 §3 Table3/Fig3 |
| ITDR | LoRA、多任务构成消融、数据子集敏感性 | 配对的目标任务累计曝光与专门/共享轨迹；并非否认它多轴部分联合 | Tier1 §4.3 |
| OpenOneRec | 多任务Yes/No与生成、显式SFT权重、低数据单/多域对照 | 不同曝光运行点的对应任务专家关系及协议条件 | Tier1 §3.2.2/6.3.2/B.5 |
| InstructRec | 共享指令适配、多接口、困难检索候选评价 | 较高曝光N/M差距在具体不同候选条件下的表现 | Tier2 §2/3.3 |
| Penha et al. | Flan-T5搜索/推荐专门与共享、多个新增任务每物品上限 | 目标任务累计消费对齐，而非辅助任务上限与流行度联合变化 | Tier1 §5/7 Fig4 |
| OneReason | 域RL专家与统一学生 | Y/N任务监督adapter而非域RL蒸馏 | Tier2 §6 |

## Explicit Non-Claims

- not first unified recommendation model
- not first multitask LLM recommender
- not first specialist/shared comparison
- not first hard-candidate evaluation
- not first data scaling study
- not first budget-aware LLM-vs-SASRec comparison
- not a new architecture
- 不是PopMatch新方法或首次流行度匹配评价；没有专门prior-art依据。
- 不是语义机制隔离、普遍正迁移、跨seed等价性或LLM全面优于SASRec。
- 不是预训练、tokens、FLOPs、优化步数、wall-clock或总信息预算公平。
- 不是“前人从未联合三个轴”或“有限检索证明首创”。

## Evidence Limits And Freeze Scope

MovieLens支撑详细单seed轨迹；Amazon仅提供旧运行点排序方向，不能替代完整Y/N、共享曝光、hard或N/SASRec曲线。新的MS96、运行元信息和统计溯源缺口继续保留，不在本轮处理。

本轮仅整合贡献/引言/相关工作及文献资产。方法、结果、讨论、限制、表图和旧稿冻结。没有发现足以要求MAJOR_REVISE的HIGH完整设计冲突；这不是新颖性证书。检索到此停止。

## MS96 Evidence Update / 证据范围更新

追加：2026-09-08，MS96 INTEGRATED。此段仅更新实验证据状态，覆盖前文历史性的“MS96待处理/不能跨seed”范围说明，不改原文献定位、Core Thesis或贡献层级：C2 primary、C4 secondary、C3 supporting、C1 framing。

- 完整曝光轨迹仍为seed42；48→96k的标准k5差距收窄限定validation，不能扩展为三seed轨迹或test同样收窄。
- 96k的Y96/N96/M1-96已覆盖seed42/43/44，两额外seed独立复现small-gap regime；冻结test三seed三排序指标一致保留modest N-specialist advantage，不是parity或等价。
- Y侧保持相近的被测偏好表现，test点估计三seed均M1稍高；seed44验证Accuracy略低，不写正迁移。
- k20三seed两split三指标均保留明显大于k5的N优势；k50方向相同但小于k20、幅度随seed变，且不总大于k5。不把“所有alternative协议都扩大gap”当作更新后结论。
- k5流行度匹配、k20/k50随机，非嵌套；大小、组成、采样和难度共同变化。精确嵌套比例本轮仅有用户提供，未独立取得audit。
- bootstrap仍仅seed42，三训练seed的mean/sample std是n=3、ddof=1描述统计；test为冻结决策后的留出证据。SASRec正式四点和Amazon旧排序方向边界不变。

数值与允许措辞以 [MS96整合摘要](ms96_integration_summary.md) 和更新后的 [claim matrix](claim_matrix.md) 为准；本段不提供新的文献新颖性判断。
