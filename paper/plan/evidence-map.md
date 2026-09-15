# 文献到正文的证据映射

日期：2026-09-08。写前依据2026-09-07原文裁决更新。VERIFIED只对应下表可用事实；详细URL、版本、章节见references/primary_source_notes.md和primary_source_adjudication.md。

| Source | 原文定位/证据级别 | 可用事实 | 预定段落 | 风险边界 |
| --- | --- | --- | --- | --- |
| S01/S04/S05 | 旧书目/题名主题，Tier4 | LLM推荐、零样本对话与排序已有研究 | intro.p01、rw.llm.p01 | 不加入未核S05技术细节 |
| S02 P5 | Tier1 §3/5.6 Fig5、arXiv v7 Appendix C Table16 | >=4/next-item接口；专家对照；r10-200衍生训练实例量 | intro.p01-p04、rw.llm.p02、rw.tasks.p02、rw.unified.p01 | 不称无数据曲线或预算不匹配；非完整Y/N等同 |
| S03 TALLRec | Tier1 §2/3、Table3/Fig3 | Yes/No推荐适配，同K含SASRec对照，K=1-256曲线 | intro.p01、rw.llm.p02、rw.evaluation.p02 | K选样不同累计曝光；不比较倍数或攻击loss |
| S06 Koren | Tier2 Basic MF Eq1-2 | 拟合已观测评分 | rw.tasks.p01 | 不套成所有MF目标 |
| S07 Hu | Tier2 §2/4 | 隐式偏好与置信度；未观测不是明确不喜欢 | intro.p02、rw.tasks.p01 | 反馈目标不同，不证明Y/N单因素机制 |
| S08 SASRec | Tier2 §III.E/IV.D | 根据历史预测下一物品；序列参照 | intro.p02、rw.tasks.p01、rw.evaluation.p02 | 原论文loss不等于仓库实现 |
| S09 BERT4Rec | PARTIAL | 不作技术引用 | 不采用 | 未核内容不补造 |
| S10 Krichene | Tier2 KDD官方摘要+同作者IJCAI扩展正文 | 采样不保证保持精确指标的模型相对次序 | intro.p04、rw.evaluation.p01 | 未获取KDD完整PDF；不用全指标极限定律 |
| S11 Cañamares | Tier2 §3 | target set是待评分候选集合，候选范围影响比较 | intro.p04、rw.evaluation.p01 | 不是仅选择正目标，不自动无偏 |
| S12 Dallmann | Tier2 §4-5 | full/uniform/pop模型次序可能不同 | intro.p04、rw.evaluation.p01 | 采样重评非训练seed；无本研究纯大小因果 |
| S13 Dacrema | Tier2方法；Tier1两abs身份 | 基线调优影响进展判断；2019对应1907.06902 | rw.evaluation.p02 | 非累计曝光对齐证据；不改为另一TOIS论文 |
| S14 iALS | Tier2 §3-4/Table2 | 基线配置与竞争力相关 | rw.evaluation.p02 | 非预训练/计算公平证据 |
| S15 ITDR | Tier1 §3/4.3 RQ2/3/5 | 任务删除与25/50/75%数据消融分别报告，有部分多轴覆盖 | intro.p03-p04、rw.tasks.p02、rw.unified.p01 | 未报告完整交叉，不等于完全孤立 |
| S16 InstructRec | Tier2 §2/3.3 | 多指令接口，检索困难候选 | rw.llm.p02、rw.evaluation.p01 | 不将所有设置并为同一100候选协议 |
| S17 LLMRec | Tier2 SFT分析 | 多任务与训练量差异的背景证据 | 库存，不入稿 | 非预算隔离实验 |
| S18/19/20 OneRec系列 | Tier2分别记录 | 统一流程、训练样本规模、多任务混合 | 库存，不集中堆入正文 | 五篇家族不是一个实验设置 |
| S21 OpenOneRec | Tier1 §3.2.2/6.3.2 Fig8/B.5 Table15 | 行为二值/生成，显式权重，10%与单/多域 | intro.p04、rw.unified.p01 | 不等于本研究rating-derived Y或完整每任务轨迹 |
| S22 OneReason | Tier2 §6 | 域RL专家及统一学生 | rw.unified.p02 | 域专家不等于Y/N任务adapter |
| S23 序列缩放 | Tier1 §IV.C Fig3，Tier2其余相关节 | 数据池与重复训练均已有研究 | rw.evaluation.p02 | 不称仅unique scaling或N200已收敛 |
| S24 DLRM缩放 | Tier2 §2/附录A | 单epoch数据/参数/计算分析 | 库存，不入稿 | 不能概括整个缩放领域 |
| S25 Penha | Tier1 §5/7 Fig4 | Flan-T5专门/共享，辅助任务每物品上限5/10/50/500 | intro.p04、rw.unified.p02 | 非单点/非LLM；辅助量上限不同目标任务累计消费 |

## 原创实证与文献边界

贡献C1-C4的实验依据来自既有finding C1-C9和M1-M8，不由引用替代。C2主、C4次、C3支撑、C1界定。intro.p06仅按现有MS96数据局部更新；外部文献不能替代实验去升级跨seed、Amazon或因果力度。文献行保持冻结。

P0改为“部分重合研究基础上的具体关系问题”，不主张领域空白。两项引用补足与四项支持范围改写后关闭正文marker；领域穷尽性依旧未证。
