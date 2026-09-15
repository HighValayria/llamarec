# 关键原文裁决

日期：2026-09-07。仅复核会改变本轮新颖性、引言缺口或相关工作定位的争议。没有通用检索，没有扩大独立文献池；Penha 来自用户提供的 Claude 包。下列 Tier 1 指实际核读的指定原文部分，不表示通读全文或复现实验。

## P5：两个版本导致的证据遗漏

- 原作者站版本为18页；[arXiv v7](https://arxiv.org/pdf/2203.13366v7)为19页，身份页标明2023-01-02修订、RecSys 2022录用。正文继续著录2022年，不把版本更新当成新论文。
- §3明确评分至少4对应like/dislike，并列出下一物品生成、候选选择、下一物品Yes/No接口。阈值和任务类型重合，不等于与本研究完整数据划分、prompt、目标和scoring相同。
- §5.6 Fig.5确有P5-S与各single-task模型对照，增益依任务不同。§5.1的10 epochs、batch和正负1:1，不是统一每任务累计曝光的直接账本。不能仅从联合训练总数据更多断言每任务预算不匹配。
- **Appendix C / Table 16（PDF第14页）确实改变训练数据量**：对原始用户物品交互，在含99个负例与正例的候选池中产生训练实例，随机选择prompt，生成实例数r从10变化到200。这既不是仅改变不同prompt模板数量，也不是把测试候选数从10改为200。
- 裁决：Claude概括“从不改变数据量”错误；其附录细节有依据。Codex上轮所读作者站版本未覆盖该附录，须修正遗漏。P5应作为任务、专家对照和衍生训练数据量的实质近邻。已核部分未呈现本文所考察的每任务累计曝光对齐下专家/共享关系轨迹及候选协议关联，但这不是领域不存在的证明。

## Penha：不是单点，也不是非预训练语言模型

原文：[Bridging Search and Recommendation in Generative Retrieval: Does One Task Help the Other?](https://arxiv.org/html/2410.16823v1)；[PDF](https://arxiv.org/pdf/2410.16823)首页确认RecSys 2024，DOI 10.1145/3640457.3688123，作者为Gustavo Penha、Ali Vardasbi、Enrico Palumbo、Marco de Nadai、Hugues Bouchard。

- §5的生成模型使用google/flan-t5-base，训练5 epochs，batch128；不能归为非预训练语言模型适配。
- GenR、GenS与GenR+S对应推荐、搜索与共享模型。§7 / Fig.4（PDF第7页）改变**新增任务每物品训练实例上限5、10、50、500**，分别观察推荐与搜索表现，不是单点或单向对照。
- 上限会共同改变辅助任务数据量、流行度分布和共现结构；原文围绕流行度正则化解释结果，不是隔离目标任务累计曝光的设计。
- 裁决：升为C2的重要近邻S25，纠正Claude的单点/非LLM表述。本文不同问题是对应目标任务累计监督对齐下的专门/共享关系轨迹，再考察候选协议条件。不能写“首次数据感知的专家/共享比较”。

## TALLRec：选样曲线确实存在

原文：[TALLRec](https://arxiv.org/pdf/2305.00447)，§2.1-2.2、§3 Table3/Fig.3。

- K-shot定义为选出的训练样本数；Table3比较含SASRec的传统基线与TALLRec在K=16/64/256时的AUC；Fig.3b覆盖K=1到256。
- 因此有few-shot选样预算对齐和数据量曲线。不能说“只有单点”“没有data-size scan”或“本文首次budget-aware比较”。
- 已核证据不足以把相同K直接等同于相同累计样本消费。本文N/SASRec的24k、48k、96k、200k是累计下游任务样本轴；与TALLRec的K是不同计量对象。
- 裁决：C4强调本文四个累计监督运行点的轨迹及条件性解释。**不以200k/256计算跨论文监督量倍数，也不攻击其loss或基线实现。**

## ITDR：部分联合存在，未确认全交叉网格

原文：[ITDR v1](https://arxiv.org/html/2508.05667v1)，§3、§4.2-4.3、附录C。

- 使用多任务指令LoRA适配；§4.3 RQ2/Fig.3做根任务删除，RQ3/Table1做子任务删除。
- RQ5/Fig.4b在GLM4-9B上使用分层25%、50%、75%数据子集；不同任务显示不同数据响应。
- 文中报告的是分别开展的任务构成与规模消融，未呈现“任务子集×各规模”的完整交叉网格。
- 裁决：Codex“多轴部分重合”与Claude“未完整交叉”可以同时成立；前者不能推成全交叉，后者不能推成彼此孤立。C1不靠预测问题首创；C2不靠从未研究任务与数据关系。

## OpenOneRec：配比与低数据对照均明确

原文：[OpenOneRec v2](https://arxiv.org/html/2512.24762v2)，§3.2.2、§6.3.2/Fig.8、Appendix B.5/Table15。

- 包含行为Yes/No预测及下一物品生成；不等同于本研究rating-derived Y。
- Table15明确SFT采样权重，例如label7.800%、video3.971%、recommendation合计35.022%。
- Fig.8比较10% few-shot、全量single-domain、全量multi-domain三个设置，确有数据量与训练策略部分关联。
- 未核到在若干相同每任务累计曝光点配对的完整专门/共享轨迹。模型家族预训练token对照不能直接当成这一轨迹。
- 裁决：拒绝把整个OneRec家族概括为“几乎没有任务分配/数据对照”；正文正面承认部分覆盖，再说具体问题的不同。

## 推荐缩放：重复训练并非空白

原文：[Scaling Law of Large Sequential Recommendation Models](https://arxiv.org/pdf/2311.11351)，§IV.B、§IV.C/Fig.3。

- §IV.B考察数据规模；§IV.C题为Scaling with Data Repetition，考察多epoch重复训练。
- 因此Claude“相关缩放只研究unique raw data”的家族概括错误。
- Ardalani等S24的单epoch数据子集设计仍成立，但不能外推至整个缩放文献。
- 裁决：数据池、重复训练、衍生任务累计消费、优化步数、token、FLOPs、预训练及时间必须分列；已有重复训练不意味着本文N200已收敛。

## Dacrema：两个编号是两篇相关论文

- [1907.06902](https://arxiv.org/abs/1907.06902)：Are We Really Making Much Progress? A Worrying Analysis of Recent Neural Recommendation Approaches；Dacrema、Cremonesi、Jannach；RecSys2019；DOI10.1145/3298689.3347058。
- [1911.07698](https://arxiv.org/abs/1911.07698)：A Troubling Analysis of Reproducibility and Progress in Recommender Systems Research；另含Simone Boglio；TOIS39(2),2021；DOI10.1145/3434185。
- 裁决：Claude建议把已有2019条目的编号“纠正”为1911不成立；保留S13与现有正式书目。不为排版整齐合并两篇，也不把baseline调优文献当成累计曝光匹配依据。

## 无需扩检的解释边界

- InstructRec的§2、§3.3已有Tier2原文定位，足够支撑任务接口和困难检索候选先例。
- OneReason的§6已有Tier2域RL专家与统一学生对照；域专家不等于Y/N任务adapter专家。
- PerRecBench包内没有足够精确的节/表定位，保留候选，不将其结论升格为已核原文。本轮C1已经由P5/ITDR充分收窄，补搜它不会改变定位。
- LLMRank对应既有S05。只使用已核身份及零样本排序主题，不采用本轮未核的候选/流行度细节。
- Krichene、Cañamares、Dallmann使用既有Tier2限定结论；Cañamares的target set是待评分候选集合，不是仅抽正目标。
- PopMatch方法首创、gap增长框架首创、未找到就证明交叉处为空，均是Tier5推断过度，不需要为否决这些措辞追加搜索。

## 停止判断

没有在上述核读范围内确认完全覆盖本研究具体设计、足以推翻当前中心的HIGH冲突。这个判断不是首创认证。当前争议已足够支撑有限、正面的研究定位；继续泛搜没有授权，也不是本轮稿件整合的前置条件。
