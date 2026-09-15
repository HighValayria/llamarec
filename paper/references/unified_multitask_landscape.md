# 统一与多任务推荐：原文对照

> 2026-09-08：根据用户新授权与跨Agent原文裁决，证据已整合到00-02。以下映射为当前定位；两份原始报告及旧未采用备份保持不变。

日期：2026-09-07。准确书目见 citation_inventory.md。以下“未确认”不表示作者没有做，更不表示其设计不公平。

## 任务、参数、配比与对照

| 工作 | 任务及共享范围 | 训练流程与任务分配 | 评价/专家证据 | 本文使用边界 |
| --- | --- | --- | --- | --- |
| P5 / S02 | rating、sequence、explanation、review、direct；同一T5 encoder-decoder | 混合输入输出任务对；抽取prompt模板；§5.1的正负1:1不是任务配比 | §5.6 Fig5单/多任务；arXiv v7 Appendix C/Table16另有r10-200衍生训练实例量 | 已有真实专家比较，不得只称“统一范式题名”；不是shared LoRA证据 |
| ITDR / S15 | 七任务；GLM/Qwen/LLaMA派生模型各用LoRA | §4.2分层取训练集、2epochs；§4.3删根任务/子任务及数据子集 | 任务删除与25/50/75%规模消融分别报告，未全交叉 | 支持共享LoRA、任务组成和数据规模，但不能推出匹配每任务曝光的专家曲线 |
| InstructRec / S16 | pointwise/pairwise/matching/reranking，偏好与意图组合 | §2.3共享Flan-T5-XL序列到序列SFT，39模板生成252K指令；§3.3.3按场景增加指令 | hard候选及指令泛化 | 指令种类、训练量、任务分配不是独立控制变量 |
| OpenOneRec / S21 | 8任务，包括行为Yes/No、next-item、交互/条件推荐、解释；统一Qwen3派生模型 | §4.2 token warm-up后全参数co-pretraining；§5联合SFT、通用蒸馏、推荐RL；附录B.5列采样权重 | §6.3.2/Fig8为10%/全量单域/全量多域；B.5/Table15明确采样权重 | 最接近的统一接口与显式分配先例；不是Y/N专家下游曝光消融 |
| OneRec-Think / S20 | persona、next-item、item-caption、通用语言；开放数据全参数，工业部分LoRA | §4、附录A.3：warm-up、multi-task integration、reasoning SFT、RL；Table5给四任务比例 | 组件消融、生成推荐、线上指标 | 原文明示配比；不能说统一推荐未讨论任务分配 |
| OneReason / S22 | 多域推荐推理，统一学生与域专家 | §6：四域分别RL，再拒绝采样SFT或多教师on-policy蒸馏 | 比较混域RL、域专家、RFT、MOPD | “specialize-then-unify”是已有方法路线，不等于本文曝光驱动的共享adapter分析 |

| Penha / S25 | Flan-T5-base搜索、推荐、共享 | §5固定5epochs；§7改变新增任务每物品训练实例上限5/10/50/500 | 两任务结果及专门/共享关系 | 有数据分配曲线；辅助量上限与流行度共同变，不等于目标累计曝光对齐 |

主要来源：[P5含扩展附录](https://arxiv.org/pdf/2203.13366v7)、[Penha](https://arxiv.org/html/2410.16823v1)、[ITDR](https://arxiv.org/html/2508.05667v1)、[InstructRec](https://arxiv.org/pdf/2305.07001)、[OpenOneRec](https://arxiv.org/html/2512.24762v2)、[OneRec-Think](https://arxiv.org/html/2510.11639)、[OneReason](https://arxiv.org/html/2606.06260)。

## OneRec名称核对

| 名称 | 作者/年份/身份 | 确认的定义 | 不应混用的概念 |
| --- | --- | --- | --- |
| OneRec: Unifying Retrieve and Rank with Generative Recommender and Iterative Preference Alignment | Jiaxin Deng, Shiyao Wang, Kuo Cai, Lejian Ren, Qigen Hu, Weifeng Ding, Qiang Luo, Guorui Zhou；2025；arXiv:2502.18965 | 共享encoder-decoder/MoE生成session列表；NTP训练后偏好对齐，奖励模型选DPO对；报告DPO抽样比例和模型规模消融 | “统一”主要是召回/排序流程，不是评分Y与next-item N；DPO偏好对不是评分二分类 |
| OneRec Technical Report | Guorui Zhou等；2025；arXiv:2506.13695 | 工业端到端生成推荐及RL/系统；§4.2报告训练样本、模型与推理规模关系 | 样本规模曲线已存在，但不是本文共同底座Y/N任务专家曲线 |
| OneRec-Think: In-Text Reasoning for Generative Recommendation | Zhanyu Liu等；2025；arXiv:2510.11639 | 语义对齐与显式推理训练，见上表 | 不能简称早期OneRec后把推理/多任务配置倒灌给早期论文 |
| OpenOneRec Technical Report | Guorui Zhou等，正文署OneRec Team；首发2025，核读v2于2026-02-04；arXiv:2512.24762 | 开放数据、RecIF-Bench、co-pretraining与post-training、OneRec-Foundation | OneRec/OneRec-Pro为该报告中的不同数据预算变体，不是不同Y/N专家 |
| OneReason Technical Report | OneRec Team及署名作者；2026；arXiv:2606.06260 | 推荐推理及域专家整合 | 域专家/混域RL不自动等于任务专家/监督多任务 |

以上以已核arXiv版本引用，正式venue没有取得可信出版证据时不填写会议名。早期OneRec的arXiv摘要题名含Iterative，HTML题名省略该词；保留摘要书目题名并记录差异。其HTML有未替换的会议模板日期，不能当出版年份。ITDR也有会议模板残留，不据此宣布2026录用。

[早期OneRec身份](https://arxiv.org/abs/2502.18965)、[技术报告](https://arxiv.org/abs/2506.13695)、[Think身份](https://arxiv.org/abs/2510.11639)、[OpenOneRec身份](https://arxiv.org/abs/2512.24762)、[OneReason身份](https://arxiv.org/abs/2606.06260)。

## 配额与本文问题

明确配比不等于完成每任务累计曝光对照；固定epoch也不自动等于固定总曝光。相反，任务删除后保留数据按相同epoch训练，可能保持部分任务的重复次数，不能直接判作“曝光未匹配”。本次只确认这些原文未报告本文式跨曝光、专家配对及hard协议联动结果。

UNIFIED_TASK_ALLOCATION已通过P5、ITDR、OpenOneRec的具体事实改写关闭；Penha与OneReason进入后一段，分别区分辅助任务量与域专家。本文不提出新的任务分配、adapter或统一算法。
