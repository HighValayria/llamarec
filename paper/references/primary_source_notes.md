# 原始文献定向核读记录

原文核验：2026-09-07；登记更新：2026-09-08。关键冲突裁决见primary_source_adjudication.md；00-02已授权应用。只记录为当前claim实际检查的部分；未逐页通读全篇，未复现实验。VERIFIED是claim相对原文的状态，不是研究结论被本项目复现。S01/S04/S05继承题名级事实；S09不使用。

## S01

键：`zhao2024llmrec`。[原文](https://doi.org/10.1109/TKDE.2024.3392335)：继承书目/题名级核验。

核到的事实：存在以LLM时代推荐系统为主题的研究。

使用边界：题名主题级；继承2026-08-22书目核验，2026-09-07仅本地比对

## S02

键：`geng2022p5`。[原文](https://yongfeng.me/attach/P5.pdf)：作者站18页版本，§3/5.1/5.6 Fig5；[原文](https://arxiv.org/pdf/2203.13366v7)：19页版本，Appendix C/Table16（PDF第14页）。

核到的事实：P5共享T5表达五类任务；§3含rating>=4喜欢判断及下一物品生成/选择。§5.6 Fig5有专家/多任务对照。arXiv v7 Appendix C/Table16将每交互衍生训练实例数r从10变到200，不只是prompt模板数。没有据此确认每任务累计消费匹配的专家轨迹，也不能断言预算不匹配。

使用边界：Tier1定向复核§3/5.6并补arXiv v7 Appendix C；修正上轮作者站18页版遗漏；不冒充通读。正式RecSys2022，v7修订于2023-01-02。

## S03

键：`bao2023tallrec`。[原文](https://arxiv.org/pdf/2305.00447)：§2.1-2.2 Table2; §3 Table3 Fig.3。

核到的事实：指令+like/dislike历史+目标物品，输出Yes/No；alpaca tuning再rec-tuning，LoRA条件语言建模。 K-shot是随机抽取训练样本数量；同一K下与含SASRec的传统模型比较，Table3为16/64/256，Fig3b为1-256。 评价为binary AUC；不能等同本文N候选next-interaction排序或累计样本消费匹配。

使用边界：已读相关方法及数据/预算实验。 2026-09-07 Tier1复核Table3/Fig3b；K曲线已存在，K选样不可与本研究累计消费按倍数比较，不采纳loss攻击。

## S04

键：`he2023zeroshotconv`。[原文](https://doi.org/10.1145/3583780.3614949)：继承书目/题名级核验。

核到的事实：已有工作将LLM用于零样本对话推荐。

使用边界：题名主题级；继承2026-08-22书目核验，2026-09-07仅本地比对

## S05

键：`hou2024zeroshotrankers`。[原文](https://doi.org/10.1007/978-3-031-56060-6_24)：继承书目/题名级核验。

核到的事实：已有工作研究LLM作为推荐系统中的零样本排序器。

使用边界：题名主题级；继承2026-08-22书目核验，2026-09-07仅本地比对

## S06

键：`koren2009mf`。[原文](https://datajobs.com/data-science-repo/Recommender-Systems-%5BNetflix%5D.pdf)：PDF p3（印刷p44），A Basic Matrix Factorization Model，Eq.1-2。

核到的事实：基本MF通过正则化平方误差拟合已观测评分；显式评分与隐式行为不是同一数据语义。

使用边界：已核论文原始排版副本相关正文；作者网页核书目，副本印刷42-49与既有正式著录30-37不同，不改写书目页码。

## S07

键：`hu2008implicit`。[原文](https://yifanhu.net/PUB/cf.pdf)：§2，§4 Eq.3，PDF pp2-4。

核到的事实：显式评价与隐式行为不同；原模型把行为转成偏好指示与置信度，未交互不等于明确不喜欢。

使用边界：已核作者原文的目标、反馈特性及置信度定义。

## S08

键：`kang2018sasrec`。[原文](https://cseweb.ucsd.edu/~jmcauley/pdfs/icdm18.pdf)：§III.E, §IV.D。

核到的事实：从历史预测下一物品；时间步正目标是下一序列事件。 原论文是采样负例BCE，每时间步每epoch一个负例；评价采100负例加真值。 仅作任务历史与模型身份依据，不能归因本仓库full-item CE实现为原论文配置。

使用边界：已读任务、训练及评价章节。

## S09

键：`sun2019bert4rec`。[原文](https://doi.org/10.1145/3357384.3357895)：继承书目/题名级核验。

核到的事实：本地仅保留短题名和旧序列主题备注，不足以描述其具体目标/结构。

使用边界：书目身份已记录，拟用技术claim缺直接内容

## S10

键：`krichene2020sampled`。[原文](https://research.google/pubs/on-sampled-metrics-for-item-recommendation/)：官方KDD摘要；同作者IJCAI2021扩展摘要§2-4（需定向阅读全文段落）；[原文](https://www.ijcai.org/proceedings/2021/0651.pdf)：同作者IJCAI2021扩展稿§2-4，已核定义与排序不一致例子；非新研究。

核到的事实：采样指标不必保留全库指标的模型相对次序，即使取期望也不保证。 研究采样指标相对精确指标的近似性质；不是本文hard协议的因果解释。

使用边界：KDD完整PDF未取得；官方摘要和同作者扩展稿正文支持限定采样结论，未假装通读KDD全文。

## S11

键：`canamares2020target`。[原文](https://castells.github.io/papers/recsys2020.pdf)：§1 pp1-2; §3 p3, T_u ∪ N_u。

核到的事实：target set是模型待评分候选集合；固定已评分test items T_u，变化额外unrated N_u，不能误写成只采正目标。 小/大候选范围可改变比较并与missing-not-at-random及模型popular/high-rating偏好相关；最大集合亦非自动无偏。

使用边界：已读定义及论证章节；纠正上轮题名推断。

## S12

键：`pereira2025sampling`。[正式出版页](https://doi.org/10.1145/3705328.3748086)：RecSys 2025, pp. 360--369。

核到的事实：按冻结R-BALANCED裁决，本条仅支持采样策略会影响离线推荐测量与模型排序，评价结论依赖采样设计。

使用边界：2026-09-11由`dallmann2021sampling`替换。Crossref正式书目已核，本轮未通读新论文全文；不得把旧文献的full/uniform/popularity、模型、数据集或重复次数细节转移给本条，也不能据此解释本文非嵌套协议的纯候选数量因果。

## S13

键：`milogradskii2024bpr`。[正式出版页](https://doi.org/10.1145/3640457.3688073)：RecSys 2024, pp. 267--277。

核到的事实：按冻结R-BALANCED裁决，本条支持基线复现、实现选择和超参数调优会影响基线竞争力判断。

使用边界：2026-09-11由`dacrema2019progress`替换。Crossref正式书目已核，本轮未通读新论文全文；仅用于BPR基线可复现性与谨慎调优，不暗示其评价SASRec，也不是下游样本预算匹配的直接证据。

## S14

键：`shehzad2025gnn`。[正式出版页](https://doi.org/10.1145/3705328.3748156)：RecSys 2025, pp. 842--846。

核到的事实：按冻结R-BALANCED裁决，本条支持标准化评价以及经调优传统基线仍可保持竞争力。

使用边界：2026-09-11由`rendle2022ials`替换。Crossref正式书目已核，本轮未通读新论文全文；不作为本仓库SASRec实现来源，也不支持下游曝光或总成本等价。

## S15

键：`liu2025itdr`。[原文](https://arxiv.org/html/2508.05667v1)：§3、§4.2-4.3、附录C。

核到的事实：多任务LoRA，评分/下一物品等任务；§4.3 RQ2/Fig3和RQ3/Table1删除任务，RQ5/Fig4b按25/50/75%分层数据子集实验。两类消融分别报告，不是全交叉，也不是任务与数据完全隔离。

使用边界：已核与当前claim直接相关的原文方法/实验章节，不宣称复现论文结果。v1；HTML会议模板未替换，不视为正式录用；2026-09-07 Tier1复核§4.3 RQ2/3/5

## S16

键：`zhang2023instructrec`。[正式出版页](https://doi.org/10.1145/3708882)：ACM TOIS 43(5), 2025, pp. 1--37；[同一工作原文](https://arxiv.org/pdf/2305.07001)：§2.1-2.3、§3.3.1-3.3.4。

核到的事实：共享Flan-T5指令适配；pointwise/pairwise/matching/reranking；有困难检索候选及较大候选检验。

使用边界：已核与当前claim直接相关的原文方法/实验章节，不宣称复现论文结果。2026-09-11仅执行同一工作的正式书目升级；2025出版年份不构成新的科学证据。

## S17

键：`liu2023llmrecbenchmark`。[原文](https://arxiv.org/pdf/2308.12241)：实验设置及SFT分析PDF pp4-7。

核到的事实：五类任务画像与SFT；明确讨论与P5训练量、prompt多样性的差异，不是预算隔离实验。

使用边界：已核与当前claim直接相关的原文方法/实验章节，不宣称复现论文结果。不是Wei等同名图增强LLMRec；本项目名LlamaRec亦非此文

## S18

键：`deng2025onerec`。[原文](https://arxiv.org/html/2502.18965)：§3.2-3.3、§4、§5.1-5.3。

核到的事实：用session生成和偏好对齐统一召回排序；DPO抽样比例不是Y/N任务配比。

使用边界：已核与当前claim直接相关的原文方法/实验章节，不宣称复现论文结果。摘要题名含Iterative，HTML省略；HTML会议模板日期无效；正式venue未确认

## S19

键：`zhou2025onerecreport`。[原文](https://arxiv.org/html/2506.13695)：§4.1-4.2。

核到的事实：工业生成推荐中报告训练样本轴的模型loss曲线，另研究参数、特征与推理规模。

使用边界：已核与当前claim直接相关的原文方法/实验章节，不宣称复现论文结果。独立技术报告，不与2502.18965合并

## S20

键：`liu2025onerecthink`。[原文](https://arxiv.org/html/2510.11639)：§4、§5.3-5.4、附录A.3/Table5。

核到的事实：多任务item-text对齐、next-item、推理SFT与RL；明确混合比例，开放与工业参数训练范围不同。

使用边界：已核与当前claim直接相关的原文方法/实验章节，不宣称复现论文结果。未核正式venue；不反向套给早期OneRec

## S21

键：`zhou2025openonerec`。[原文](https://arxiv.org/html/2512.24762v2)：v2 §3.2-3.3、§4.2-4.3、§5.1、§6.3-6.4、附录B.4-B.5。

核到的事实：统一行为Yes/No和生成推荐；B.5/Table15明确SFT采样权重（label7.800%、video3.971%、recommendation合计35.022%）；§6.3.2/Fig8比较10%few-shot、全量single-domain、全量multi-domain。未确认多个匹配每任务累计点的专家/共享轨迹。

使用边界：已核与当前claim直接相关的原文方法/实验章节，不宣称复现论文结果。首发2025；核读v2为2026-02-04，未将co-pretraining预算说成下游Y/N预算；2026-09-07 Tier1复核§3.2.2/6.3.2及B.5，不把家族概括成未报告配比

## S22

键：`onerecteam2026onereason`。[原文](https://arxiv.org/html/2606.06260)：§6.1-6.4。

核到的事实：混域RL、域专家和RFT/MOPD统一学生对照；不是Y/N共享监督adapter的曝光消融。

使用边界：已核与当前claim直接相关的原文方法/实验章节，不宣称复现论文结果。以报告团体作者引用；未核正式venue

## S23

键：`zhang2023seqscaling`。[正式出版页](https://doi.org/10.1145/3640457.3688129)：RecSys 2024, pp. 444--453；[同一工作原文](https://arxiv.org/pdf/2311.11351)：§III.C-E、§IV.A-C Fig.2-3。

核到的事实：ID-only序列模型研究数据池和模型规模；§IV.C/Fig3明确研究多epoch数据重复，不能概括为只有unique raw data scaling。不是本文预训练LLM与SASRec累计下游任务对齐。

使用边界：已核与当前claim直接相关的原文方法/实验章节，不宣称复现论文结果。2026-09-11仅执行同一工作的正式书目升级，不改变其数据池与重复训练的科学角色。

## S24

键：`ardalani2022scaling`。[原文](https://arxiv.org/pdf/2208.08489)：§2.1-2.2、附录A.1-A.4。

核到的事实：DLRM式CTR研究分别改变数据、参数和FLOPs；数据子集均一epoch，重复更久不在该实验内。

使用边界：已核与当前claim直接相关的原文方法/实验章节，不宣称复现论文结果。arXiv版本；不用于宣称LLM计算公平

## 获取与身份异常

Krichene的KDD完整PDF未成功获取，采用官方摘要及同作者IJCAI扩展稿限定支持。Koren作者站PDF及OSU副本取回失败，最终读取由大学课程列出的原论文排版副本；标题、三位作者、2009版权及基本模型可见，出版身份沿用作者列表与既有DOI。

发现一个未经核实的arXiv地址实际上指向无关物理论文，立即排除；没有引用其内容。搜索返回的评论、博客、综述性解读、课程讲义不作为技术结论依据。会议模板残留、发布日期与正式出版年不混同。

## S25

键：`penha2024bridging`。[原文](https://arxiv.org/html/2410.16823v1)：§3/5/7 Fig4；[原文](https://arxiv.org/pdf/2410.16823)：首页正式身份、PDF第7页Fig4。

核到的事实：Flan-T5-base适配GenR/GenS/GenR+S；§7 Fig4把新增任务每物品训练实例上限设为5/10/50/500，观察两任务表现。不是单点或非预训练LM；上限共同改变辅助量与流行度，不等于目标任务累计曝光配对。

使用边界：Tier1仅核§3/5/7与Fig4以及PDF首页身份；来自用户Claude既有候选而非扩搜，未通读全文或复现。

## S26

- source ID：`S26`；键：`meta2024llama32`。
- canonical source identity：Meta，*Llama 3.2 Model Card*，2024；官方模型文档。
- verified location / official source：[Meta llama-models model card](https://github.com/meta-llama/llama-models/blob/main/models/llama3_2/MODEL_CARD.md)，Model Information 与 Model Architecture。
- manuscript usage：`methods.training.p01`。
- what it supports：Llama 3.2 instruction-tuned collection 中 3B 模型的身份。
- what it does NOT support：不支撑本仓库的 QLoRA 配置、adapter 超参数、训练命令或正式 run metadata。
- verification status：`VERIFIED`；依据既有官方model card定向核验记录，未重新联网搜索，未宣称通读全部文档。

## S27

- source ID：`S27`；键：`hu2022lora`。
- canonical source identity：Edward J. Hu, Yelong Shen, Phillip Wallis, Zeyuan Allen-Zhu, Yuanzhi Li, Shean Wang, Lu Wang, Weizhu Chen，*LoRA: Low-Rank Adaptation of Large Language Models*，ICLR 2022；会议论文。
- verified location / official source：[OpenReview正式记录](https://openreview.net/forum?id=nZeVKeeFYf9)；[arXiv原文](https://arxiv.org/abs/2106.09685)，Abstract、§1、§4.1。
- manuscript usage：`methods.training.p01`。
- what it supports：冻结预训练权重并引入可训练低秩矩阵的 LoRA 方法身份。
- what it does NOT support：不证明本实验的 rank、alpha、dropout、target modules 或任何历史运行实参。
- verification status：`VERIFIED`；沿用既有原论文方法定义与ICLR出版记录核验，不重新检索。

## S28

- source ID：`S28`；键：`dettmers2023qlora`。
- canonical source identity：Tim Dettmers, Artidoro Pagnoni, Ari Holtzman, Luke Zettlemoyer，*QLoRA: Efficient Finetuning of Quantized LLMs*，NeurIPS 2023；会议论文。
- verified location / official source：[NeurIPS官方摘要](https://proceedings.neurips.cc/paper_files/paper/2023/hash/1feb87871436031bdc0f2beaa62a049b-Abstract.html)；[arXiv原文](https://arxiv.org/abs/2305.14314)，Abstract、§3。
- manuscript usage：`methods.training.p01`。
- what it supports：在冻结的 4-bit 量化预训练模型上向 LoRA adapter 反向传播，以及 NF4 的方法身份。
- what it does NOT support：不证明本仓库的具体 adapter 超参数、量化实参或正式 run 配置。
- verification status：`VERIFIED`；沿用既有官方摘要和原论文方法章节核验，不重新检索。

## S29

- source ID：`S29`；键：`harper2015movielens`。
- canonical source identity：F. Maxwell Harper, Joseph A. Konstan，*The MovieLens Datasets: History and Context*，ACM Transactions on Interactive Intelligent Systems，2015；期刊论文。
- verified location / official source：[GroupLens官方引用说明](https://grouplens.org/blog/movielens-datasets-context-and-history/)；[原论文](https://files.grouplens.org/papers/harper-tiis2015.pdf)，摘要与数据集历史。
- manuscript usage：`methods.datasets.p01`。
- what it supports：MovieLens 数据集的规范身份和来源。
- what it does NOT support：不承担本项目的任务过滤、时间切分、处理后样本数或用户数。
- verification status：`VERIFIED`；沿用既有GroupLens官方来源与论文身份核验，不重新检索。

## S30

- source ID：`S30`；键：`hou2026amazonreviews`。
- canonical source identity：Yupeng Hou, Jiacheng Li, Xiangjun Fu, Zhankui He, An Yan, Xiusi Chen, Julian McAuley，*Bridging Language and Items for Retrieval and Recommendation: Benchmarking LLMs as Semantic Encoders*，ACL 2026；会议论文与配套数据集文档。
- verified location / official source：[ACL Anthology正式记录](https://aclanthology.org/2026.acl-long.147/)；[Amazon Reviews 2023官网](https://amazon-reviews-2023.github.io/)；[5-core处理页](https://amazon-reviews-2023.github.io/data_processing/5core.html)的定义与 Musical_Instruments 行。
- manuscript usage：`methods.datasets.p02`。
- what it supports：Amazon Reviews 2023、5-core版本及 Musical Instruments 子集的身份。
- what it does NOT support：不承担本项目下载快照、清洗、任务构造或处理后计数。
- verification status：`VERIFIED`；沿用既有ACL记录与官方数据页核验，不重新检索。

## S31

- source ID：`S31`；键：`efron1993bootstrap`。
- canonical source identity：Bradley Efron, Robert J. Tibshirani，*An Introduction to the Bootstrap*，Chapman and Hall，1993；统计专著。
- verified location / official source：[出版社书目页](https://www.routledge.com/An-Introductionto-the-Bootstrap/Efron-Tibshirani/p/book/9780412042317)，目录中的 Confidence Intervals Based on Bootstrap Percentiles。
- manuscript usage：`methods.statistics.p01`。
- what it supports：bootstrap 重采样与基于 bootstrap 百分位数构造置信区间的标准方法身份。
- what it does NOT support：不证明本研究的配对方式、用户级重采样单位、5000次、seed、具体指标或执行 provenance。
- verification status：`VERIFIED`；依据既有出版社书目和目录核验，不重新联网搜索，不宣称核读全书。
