# 曝光与预算文献边界

> 2026-09-08：根据用户新授权与跨Agent原文裁决，证据已整合到00-02。以下映射为当前定位；两份原始报告及旧未采用备份保持不变。

日期：2026-09-07。预算意识不是本文首创。本文沿用任务样本累计消耗的操作定义，重复读取计入曝光；unique数据、token、step、FLOPs、时间、预训练投入分别登记。

| 工作/原文位置 | 实际预算轴 | 已有比较 | 与本文N/SASRec曲线的关系 |
| --- | --- | --- | --- |
| TALLRec §3 Table3/Fig.3 | K个选取训练样本，少样本池大小 | 含SASRec基线在相同K下的二分类AUC，K增长分析 | 直接预算先例；不是N排序，也未确认累计消费匹配 |
| LLMRec benchmark，SFT分析pp5-6 | prompt种类、训练数据构造及epoch | 明确讨论与P5训练量不同是比较解释因素 | 支持报告训练量差异；作者解释不是隔离预算效应的因果实验 |
| ITDR §4.3 RQ5 | 分层训练子集25/50/75% | 共享LoRA模型的任务类数据响应 | 不是固定样本池重复曝光，也不是LLM/SASRec配对 |
| Scaling Law of Large Sequential Recommendation Models §IV.B-C | 独立交互池大小；另做重复训练epoch | ID-only序列模型容量/数据规模及数据重复 | 重复曝光的推荐文献先例，不能声称此前只有unique样本数；非预训练LLM Y/N比较 |
| Understanding Scaling Laws for Recommendation Models §2、附录A | 数据样本数、参数、FLOPs分开；各模型一epoch | 工业DLRM式CTR模型的资源效率 | 一epoch下池大小与消费量联系紧密；不能转写为LLM下游公平原则；更长重复训练留作其未来工作 |
| OneRec Technical Report §4.2.1 | 累计训练样本与模型规模，另有推理Pass@K | 工业生成推荐的loss曲线 | 已有sample-axis scaling，但没有本文的Y/N任务专家对照；推理K非输入候选数 |
| OpenOneRec §4.3、§6.3.2 | co-pretraining token/FLOPs；另做Amazon10%少样本迁移 | 参数/token预算分配、域专门/混域与TIGER | 是更近的基础模型预算先例；预训练token和下游任务样本不可互换 |
| Dacrema §2.2 / iALS §3-4 | baseline调优和评价规范 | 相同评价程序、合理超参下重审方法竞争力 | 不直接支持task-sample matching；不再用它们替代预算研究 |

| P5 arXiv v7 Appendix C/Table16 | 每原始交互产生r10-200条训练实例 | 改变衍生数据量，非仅模板数或测试候选数 | 数据量分析已有；不等于固定任务池的累计消费配对曲线 |
| Penha §7 Fig4 | 新增任务每物品训练实例上限5/10/50/500 | Flan-T5搜索/推荐共享关系，辅助数据与流行度同时变化 | 不能写单点或非LLM；目标累计消费是另一具体比较轴 |

原文：[P5扩展版](https://arxiv.org/pdf/2203.13366v7)、[Penha](https://arxiv.org/html/2410.16823v1)、[TALLRec](https://arxiv.org/pdf/2305.00447)、[LLMRec benchmark](https://arxiv.org/pdf/2308.12241)、[ITDR](https://arxiv.org/html/2508.05667v1)、[序列scaling](https://arxiv.org/pdf/2311.11351)、[DLRM scaling](https://arxiv.org/pdf/2208.08489)、[OneRec报告](https://arxiv.org/html/2506.13695)、[OpenOneRec](https://arxiv.org/html/2512.24762v2)、[Dacrema](https://arxiv.org/pdf/1907.06902)、[iALS](https://arxiv.org/pdf/2110.14037)。

## 本文可以怎样写

当前C4明确为24k、48k、96k、200k四个近似匹配的累计下游任务曝光点。TALLRec的K=1-256是选出样本数，不能以200k/256宣称曝光量级倍数。相近N任务累计监督下的表现是描述性、条件化比较，不等于新的公平准则或总成本匹配。

相同样本数不等于相同token或有效监督信息，不抵消LLM预训练、文本信息、模型容量、调优搜索与计算差异。本文未匹配预训练FLOPs、壁钟时间或总成本。单个已评估SASRec实现也不能代表所有序列推荐器。

已有文献支持预算轴应当区分、数据量和重复训练会影响比较；本文曲线的具体优势与改善方向只能由冻结C7/M7及结果资产支持。EXPOSURE_BUDGET_COMPARISONS正文状态REWRITTEN_AND_RESOLVED，有限预算背景RESOLVED；“完全等价公平比较”无此证据，也不保留为本文主张。

## 搜索停止

上轮候选及本轮用户包中的Penha已覆盖决定当前定位的直接争议；本轮只定向核相关原文，未继续扩大搜索池。P5/TALLRec及采样基础文献已经补到具体章节，继续泛搜不会使“首次”变得可证明。停止扩展文献，不提出新训练任务。
