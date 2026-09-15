# 联合比较设计的最近邻核验

> 2026-09-08：根据用户新授权与跨Agent原文裁决，证据已整合到00-02。以下映射为当前定位；两份原始报告及旧未采用备份保持不变。

核验日期：2026-09-07；定位更新：2026-09-08。中心微调为本研究设置中监督、累计曝光与候选条件下的模型结论。这里记录定向原文检查，不是系统综述，也不证明整个领域不存在相同工作。出处身份、版本和完整引用键见 citation_inventory.md；检索顺序见 targeted_search_log.md。

## 对照口径

- 语义：是否区分不同推荐预测目标；Yes/No输出不自动等于评分派生偏好Y。
- 曝光：区分独立训练样本池大小、累计消耗样本、任务混合份额、token、算力。
- 统一：共享模型或adapter与任务专家；跨域专家也不自动等于跨任务专家。
- 协议：固定模型下候选组成/难度检查；生成Recall@K中的K不自动是输入候选数。
- 表内“未报告”仅指已检查的相关章节，不能当作全领域缺失证据。方法细节未明确时记“未确认”，不反推不公平。

## 最近邻设计

| 工作及原文位置 | 已有重合 | 预算/专家比较 | 候选相关证据 | 与本文仍不同之处 |
| --- | --- | --- | --- | --- |
| [P5](https://arxiv.org/pdf/2203.13366v7)，§3、§5.6 Fig5、Appendix C/Table16 | >=4喜欢判断、下一物品等任务；共享T5 | 专家/多任务对照；附录r10-200衍生训练实例量分析；未确认本文式配对累计每任务轨迹，不据此指责预算不匹配 | 任务各有评价接口；不是本文固定N/M配对的hard协议组 | 统一任务和专家对照已有先例；本文差别在曝光条件下的关系变化及桥接/协议证据链 |
| [TALLRec](https://arxiv.org/pdf/2305.00447)，§2、§3 Table3/Fig.3 | 评分转Yes/No、LoRA、少样本 | 相同K个选取样本下与含SASRec的基线比较；不是累计样本消费对齐 | 二分类AUC，非N候选next-item排序 | 不能声称首次LLM/SASRec数据预算比较 |
| [ITDR](https://arxiv.org/html/2508.05667v1)，§4.2-4.3、附录C | 共享LoRA、评分/下一物品等七任务、任务删除消融、规模响应 | 任务删除与25/50/75%子集分别报告；未呈现完整交叉，不等于任务与数据彼此隔离 | NIR固定1正+4随机负例；未报告同一任务hard稳健性组 | 评分是数值预测；UII/UIU聚合响应非本文Y/N原生及桥接响应；高度相关，但不是完整重复 |
| [InstructRec](https://arxiv.org/pdf/2305.07001)，§2.1-2.3、§3.3 | 多接口指令、共享Flan-T5、指令类型消融 | 增加指令场景；未确认每任务累计曝光匹配的专家曲线 | 明确做过二塔检索hard候选；100候选分组推理另属个性化搜索 | “LLM困难候选评估”不是新贡献；本文研究的是N/M关系，而非提出更强重排器 |
| [OpenOneRec](https://arxiv.org/html/2512.24762v2)，§3.2、§4.3、§5.1、§6.3-6.4、附录B.5 | Yes/No行为标签与next-item同处统一模型；明确任务配比；token scaling | 还比较10%少样本、单域/多域迁移；同数据后训练对照是OneRec/Pro，不是Y/N专家曝光曲线 | Pass/Recall和AUC；未报告本文式k5/非嵌套hard的专家配对 | 是最重要的新近部分重合；行为标签非评分派生Y，预训练token预算非本文下游任务样本曝光 |
| [OneReason](https://arxiv.org/html/2606.06260)，§6.1-6.4 | 明确比较混域RL、域专家、统一蒸馏模型 | 先域专家RL再RFT/MOPD整合；未确认每任务曝光配对 | 跨域Recall@K；K是输出截断，非固定输入候选难度 | 专家优势及统一保留已有研究；本文是Y/N共享adapter的监督适配比较，不是RL整合方法 |
| [LLMRec benchmark](https://arxiv.org/pdf/2308.12241)，实验/SFT分析pp4-7 | 五类任务能力画像、适配前后对照 | 作者主动指出与P5在训练量及prompt多样性上的差异；不是匹配预算控制 | 各任务原生指标；未报告同一N/M的hard组 | 能力异质性与预算警惕均有先例；本文可强调共同设置中的联动比较 |
| [OneRec-Think](https://arxiv.org/html/2510.11639)，§4、§5.3、附录A.3 | 多任务语义对齐、next-item、共享参数、任务配比 | warm-up、联合训练、推理SFT与RL；未报告曝光匹配任务专家曲线 | 生成式推荐及组件消融；不是本文候选组 | 方法性推理/语义对齐贡献与本文empirical定位不同 |

| [Penha et al.](https://arxiv.org/html/2410.16823v1)，§5/7 Fig4 | Flan-T5搜索/推荐适配，专门/共享模型 | 新增任务每物品上限5/10/50/500，不是单点；同时影响辅助数据量/流行度 | 未确认本文N/M高曝光候选对照 | 本文对齐对应目标任务累计消费，而非辅助任务上限；重要C2近邻 |

## 新颖性判断与停止规则

本次已核原文中，没有确认一篇同时覆盖“类似Y/N + 共享多任务LLM + 专家每任务累计曝光匹配 + 候选稳健性”的直接重复工作，未触发HIGH冲突停止条件。这个判断基于上述设计和实验章节，不仅是关键词未命中。P5、Penha、ITDR、InstructRec、OpenOneRec、OneReason均有必须承认的实质重合；具体裁决见primary_source_adjudication.md。

不能再用以下宽泛主张作为贡献：首次统一推荐任务；首次比较专家/多任务；首次观察任务能力不同；首次考虑样本效率；首次评估hard候选；所有前人忽略预算。

## 最安全的研究问题

EN: How do capability differences and specialist-multitask relationships evolve with cumulative per-task exposure in a common recommendation-tuning setting, and which observed ranking relationships persist under alternative candidate protocols?

ZH: 在共同推荐调优设置中，能力差异及专家与多任务模型的关系如何随累计每任务曝光变化？哪些已观察到的排序关系能够在其他候选协议下保持？

当前intro.p04已应用正向问题定义并以REWRITTEN_AND_RESOLVED关闭JOINT_CONDITIONING_COVERAGE。它不依赖“没有前人”这一否定前提；领域穷尽性仍未证明。最终双语措辞见story_and_novelty_freeze.md及literature_gaps.md。

## 对贡献的影响

贡献层级为C2主、C4次、C3支撑、C1界定。C2具体描述seed42内对应任务曝光下的关系，C3限定协议；C4使用24k-200k四个近似匹配的累计下游点，不与TALLRec选样K按倍数比较。科学强度不升级：不新增跨seed、跨数据集全曲线、纯语义因果、纯候选数量因果或compute公平主张。
