# Novelty + Positioning + Citation Evidence Package

**研究定位报告:Supervision Formulation × Task-sample Exposure × Candidate Protocol 的 recommendation-tuned LLM 实证研究**

生成日期:2026-09-07。
方法说明:5 条并行检索线(arXiv API / arXiv abs 页 / ar5iv 全文 / DBLP / Semantic Scholar + 本地 PDF 全文精读)。ACM DL 多次返回 403,凡未能打开一手页面的条目均标注 UNVERIFIED。本报告只依据一手来源;搜索范围限于 arXiv 索引的英文文献与本地候选区,不排除存在未覆盖的付费全文工作。

---

## 1. Executive Summary

当前"Supervision Semantics Under Exposure"的故事**站得住,但需要精确限定**。三轴联合研究(监督形式化 × per-task 曝光 × 候选协议)在已检索范围内**没有找到先例**——最近的三篇近邻各自只覆盖严格子集:**P5**(RecSys 2022)在同一 multitask LLM 中同时包含本文 Y、N 两种任务形式(甚至同用的 rating≥4 二值化),并在固定数据量下做过 specialist ablation,但从未变化数据量或候选协议;**ITDR**(arXiv:2508.05667)在同一 instruction 语料中同时含 rating prediction 与 next-item 并做了数据规模(25/50/75%)分析,但只用"移除任务"式消融、无 matched-budget specialists、无候选协议变化、无 SASRec 对比;**Penha et al.**(RecSys 2024)研究 generative retrieval 中 search+rec 统一模型 vs 任务专属模型,但曝光轴只有一个单点实验。最大风险有三:(a) C3(候选协议敏感性)的**一般性结论已有强先例**(Krichene & Rendle KDD 2020;Dallmann et al. RecSys 2021;Zhao et al. CIKM 2020;Cañamares & Castells RecSys 2020),绝不能写成新发现;(b) PerRecBench 已方向性地报告"rating 强的 LLM 无法识别偏好排序",削弱 C1 的定性新颖度;(c) TALLRec 已做 matched-budget LLM-vs-SASRec——但仅 K≤256、AUC 协议。最稳的贡献是 **C2(曝光条件下的 specialist-vs-multitask)与 C4(曝光对齐的 LLM vs SASRec 扫描)**。若干题名/年份错误已在核验中纠正(见 §8)。

---

## 2. Research-gap Verdict

**Q3 判定:SAFE(带轻微收紧)。**

已检索范围内未发现任何工作在同一 recommendation-tuned LLM 框架内联合变化监督形式化、per-task 训练样本量与候选评估协议。三个轴各自都有文献,交叉处为空:任务形式化比较(P5、ITDR、PerRecBench、RecRanker)、数据规模(scaling laws 一系)、候选协议(Krichene & Rendle、Dallmann、Zhao、Cañamares)。搜索覆盖:16+ 条独立 arXiv API 查询(任务形式化、监督目标、instruction scaling、评估协议、负采样鲁棒性、multitask vs specialist、preference vs next-item、scaling laws、负迁移、公平 LLM-vs-traditional 对比、"PopMatch")+ 4 条专题网络核验线 + 本地 24 篇 PDF 精读。未检索到 "PopMatch" 在任何推荐论文中出现(仅有一个无关的因果推断 Python 包)。

**推荐 wording(英文):**

> Existing work has studied supervision formulations for LLM recommenders, multitask unification, training-data scaling, and the sensitivity of recommender evaluation to candidate sampling—largely in isolation (e.g., P5, ITDR, Krichene & Rendle, Dallmann et al.). How empirical conclusions about recommendation-tuned LLMs shift when supervision formulation, task-sample exposure, and candidate protocol are varied jointly within a single framework remains insufficiently characterized.

**中文:** 已有工作分别研究了 LLM 推荐的监督形式化、多任务统一、训练数据规模与评估对候选采样的敏感性,但多各自孤立;在同一框架内联合变化监督形式化、任务样本曝光与候选协议时,关于 recommendation-tuned LLM 的经验结论如何变化,仍缺乏系统刻画。

注意:不要写 "no prior work has / we are the first"。若审稿人举出 P5 或 ITDR,上述表述仍成立,因为它们只覆盖子集。

---

## 3. Near-neighbor Matrix

| Work | Rec LLM? | Multiple tasks? | Shared model? | Task formulation compared? | Training/data scale varied? | Per-task budget controlled? | Candidate protocol varied? | Specialist comparison? | LLM-vs-traditional budget comparison? | Overlap |
|---|---|---|---|---|---|---|---|---|---|---|
| **P5** (Geng et al., RecSys'22, arXiv:2203.13366) | Yes (T5) | Yes (5 task families) | Yes | 部分:两形式共存于多任务,从未作为监督选择 head-to-head | No(仅 prompt 数、任务族数消融) | No | No(seq 用全目录 beam;direct 用 1+99 随机) | **Yes(Sec 5.6, 固定数据量)** | No | **HIGH**(全轴有触点,无曝光/协议轴) |
| **TALLRec** (Bao et al., RecSys'23, arXiv:2305.00447) | Yes (LLaMA+LoRA) | No(单一偏好预测) | — | No | **Yes(K=16/64/256, Fig.3 扫到 256)** | Yes(K-shot 对齐,含 SASRec) | No(仅 AUC,无 ranking 协议) | N/A | **Yes,但仅 ≤256 样本退化区** | **HIGH**(C4 轴) |
| **ITDR** (Liu, Huang, Sang, arXiv:2508.05667) | Yes (GLM-4-9B) | Yes(7 子任务,含 rating+next-item) | Yes | 部分(移除式消融,非 matched specialists) | **Yes(25/50/75%)但与任务组成轴不交叉** | No | No(固定 5+5 / 1+4 随机负例) | No(仅移除消融) | No(无 SASRec) | **MEDIUM-HIGH**(最近的单篇) |
| **Penha et al.** (RecSys'24, arXiv:2410.16823) | Generative retrieval(非 LLM 微调) | Yes(search+rec) | Yes | Yes(search vs rec) | Partial(单一数据集上限制 added-task 实例数,Fig.4) | No | No(全目录 R@30) | **Yes** | No | **MEDIUM-HIGH**(C2 轴最近邻) |
| **UniMP** (Wei et al., ICLR'24, arXiv:2403.10667) | Yes (LVLM) | Yes(含 preference prediction + item rec) | Yes | No(不比较,只统一) | No | No | Not stated | Yes(vs 任务专属方法,非 matched) | No | MEDIUM |
| **LLaRA** (Liao et al., arXiv:2312.02445) | Yes | No(单一 next-item) | — | No | No(显式选 ML-100K 控规模) | No | No(固定 1+20 随机负例, HR@1) | N/A | Yes(非预算对齐) | MEDIUM(N 协议默认值的例证) |
| **BIGRec** (Bao et al., arXiv:2308.08434) | Yes | No | — | No | Partial(报告更多训练样本仅边际增益) | No | No(批评受限候选集,主张全目录) | N/A | Yes(非预算对齐) | MEDIUM |
| **Kang et al.** (arXiv:2305.06474) | Yes (250M–540B) | No(rating prediction) | — | No | Partial("小部分训练数据"即匹配 CF) | Partial | No | N/A | Yes(仅 rating 形式化) | MEDIUM(C4 的 Y 分支先例) |
| **Laser** (Lin et al., arXiv:2406.02368) | Yes | No | — | No | Yes(10%/50% 子采样) | **No(LLM 用子集,baseline 用全量——不对称)** | No | N/A | No(不对称) | MEDIUM(反面教材:样本效率≠预算对齐) |
| **RecBench** (Liu et al., NeurIPS'25 D&B, arXiv:2503.05493) | Yes | — | — | No(17 模型横评) | No | No | No | No | Yes(非预算对齐) | MEDIUM(限制 C4 的泛化表述) |
| **LLM Rec Scaling Laws** (Zhang et al., ICML'26, arXiv:2602.07298) | Yes | No(单任务持续预训练) | — | No | **Yes(幂律)** | No | No | No | Partial(SASRec 侧对比,非预算对齐) | MEDIUM(数据规模轴,单任务) |
| **Krichene & Rendle** (KDD'20, DOI 10.1145/3394486.3403226) | No | — | — | — | — | — | **Yes(采样 vs 全排序)** | — | — | MEDIUM(C3 一般性先例,非 LLM) |
| **Dallmann et al.** (RecSys'21, arXiv:2107.13045) | No | — | — | — | — | — | **Yes(uniform vs popularity 采样、k 变化)** | — | — | MEDIUM(C3 最近非 LLM 先例) |

(备选行,若需要:Cañamares & Castells RecSys'20、Zhao et al. CIKM'20、PLE RecSys'20、Gusak et al. RecSys'25、LLMRank ECIR'24。)

---

## 4. Unified / Multitask Recommendation Findings

**Q4(同一 LLM 承担多任务):** 已核实:P5(5 任务族)、VIP5(EMNLP 2023,P5 的多模态扩展——注意不是 "verified personalized prompt prefix",该描述有误)、UniMP(ICLR 2024,含 preference prediction 与 item recommendation,是与本文 Y/N 最接近的已发表任务对)、OpenP5(SIGIR 2024 资源轨)、M6-Rec(未发表,arXiv:2205.08084)、OneRec 全家族(Kuaishou;arXiv:2502.18965 及 2506.13695/2508.20900/2510.11639/2512.24762/2607.26500 等,**未发现非 Kuaishou 的 OneRec**)。

**Q5(是否报告 mixing ratio / per-task 预算 / matched specialist):** 几乎全部否。P5 只说 "for each raw datum, we only sample a portion of the personalized prompts"(Sec. 3),无 per-task 计数;唯一的数量消融是 Appendix C(生成式 direct-rec 的 prompt 重复数 10→200,Table 16)。PLE(RecSys 2020)是唯一显式做 "MTL gain = 相对同结构同训练样本单任务模型"(Eq. 11)的预算匹配 specialist 对比,并记录 seesaw 现象——但其任务是强相关的 CTR 互动标签,且**没有数据量轴**。

**Q6(specialist vs multitask 差距随 per-task 曝光变化):NO DIRECT PRECEDENT FOUND。** 最近的三个:
- **P5, Sec 5.6 / Fig. 5**:固定数据量下的 specialist ablation,multitask 在 rating/seq/direct rec 上持平或更好、生成类任务 specialist 胜出。但 specialists 只见各自任务族数据,总预算不匹配,且从不扫数据量。
- **Penha et al., RecSys 2024**:Podcasts 数据集上限制 added-task 实例数(Fig. 4)显示统一模型优势缩小——单点、单方向,非系统扫描;且其公开声明该领域 "hasn't established when a multi-task model beats task-specific ones"(可引作 gap 的直接文献支撑)。评估为全目录 beam search,无候选协议轴。
- **ITDR**:任务组成(移除消融)与数据规模(25/50/75%)作为**分离的两轴**,从不交叉,无 isolated specialists。

**对本研究的含义:** P5 的 Fig. 5 结论(multitask 持平或更好)建立在未匹配预算之上;本文的"低曝光下 specialist 胜、~96k 后差距缩小、hard 协议下再现"是对该结论的条件化限定而非矛盾——但 Related Work 必须显式处理这一张力(数据集、模型规模、任务定义都不同)。

---

## 5. Evaluation / Candidate Sampling Findings

**Q7:**
- **绝对指标失真(i):** Krichene & Rendle(KDD 2020;理论 + 实验)——采样指标与精确指标不一致,候选数缩小时所有指标向 AUC 塌缩;Li et al.(AAAI 2023, arXiv:2211.15743)给出修正估计量。
- **模型排序改变(ii):** Krichene & Rendle(Definition 1:期望意义上也不保序;实证 "the worst recommender would be found to be the best one");**Dallmann et al.(RecSys 2021)——这是证明"采样策略改变神经序列推荐器排序"的关键论文**,"uniform 与 popularity 采样互不一致";Zhao et al.(CIKM 2020)——采样比数据划分扰动排序更大,popularity 采样偏离全排序更远;Cañamares & Castells(RecSys 2020)——小 target 集导致 pairwise 系统对比失真,并提出 discriminative-power 准则。
- **特定模型对之间的 gap 随协议扩大/缩小(iii):** 无已验证先例以此研究对象。最近的是 Cañamares & Castells 的 discriminative power 分析与 Gusak et al.(RecSys 2025,划分策略改变含 LLM 在内的模型排序)。**"gap 增长"框架本身是新的。**

**Q8(popularity-aware / hard negative 评估构造):** 部分存在。Uniform vs popularity **负采样对比**:Dallmann et al.、Zhao et al.;popularity 混淆理论:Cañamares & Castells(SIGIR 2018 + RecSys 2020);hard negative **训练**理论:Shi et al.(WWW 2023,BPR+hard negative 优化 OPAUC,"K 越小负例应越硬")。**未发现任何 popularity-matched(候选流行度分布匹配正例)的评估构造**——PopMatch 可作为方法学贡献表述,但措辞用 "we could not identify prior popularity-matched evaluation constructions"。

**Q9:**
- **真正支持** "evaluation protocol can change the apparent relationship between models":Krichene & Rendle(KDD 2020)、Dallmann et al.(2021)、Zhao et al.(CIKM 2020)、Cañamares & Castells(RecSys 2020)、Gusak et al.(RecSys 2025,LLM 时代、划分轴)、Kostric & Balog(SIGIR 2026,对话推荐、实现细节敏感)。
- **不能用于解释 hard-k20/k50:** Ferrari Dacrema et al.(RecSys 2019)是复现性/基线论文,不操纵候选协议;Rendle/Zhang/Koren(arXiv:1905.01395)是基线调参论文;**且 Krichene & Rendle 的机制是均匀随机候选下指标向 AUC 塌缩(近似 vs 全排序),不预测"更难的候选拉大模型差距"**。本文的非嵌套 k5/k20/k50 设计对应的正是这一空白——文献只授权 "sensitivity, not causation" 的表述,这恰是本文已采取的立场。

**LLM 侧:** LLMRank(Hou et al., ECIR 2024)在 zero-shot 设置下变化候选池来源(BM25/Pop/BPRMF/SASRec 等作为 hard negatives),发现 LLM 在含热门项的池上崩溃;Is ChatGPT a Good Recommender?(RepGen@CIKM 2023)发现候选池顺序造成 ~10x 指标摆动。两者是"候选池构造主导 LLM 排序结论"的零样本先例;本文是该现象在**微调后**模型上的受控版本。

---

## 6. Exposure / Data-budget Findings

**Q10(matched downstream samples 的 LLM vs 传统模型):PARTIAL——本文量级无先例。** 两个最近邻:
- **TALLRec**:确实对齐(K-shot 同样本训练 LLM 与 SASRec/GRU4Rec/Caser;主表 AUC:SASRec ~0.52–0.54 vs TALLRec 0.72 @256-shot),但仅 K≤256 的退化区,无曝光扫描;且 baseline 用 MSE 损失训练二值标签(其实现细节),有 handicap 之嫌。本文 24k–200k 匹配曝光扫描 + 任务形式化对比 + SASRec 持续改善趋势 = 直接扩展其未运行的上界。
- **Laser**(arXiv:2406.02368):声称 10% 数据即匹配全量传统模型——但**预算不对称**(LLM 用子集、baseline 用全量),正是本文要区分的 "sample efficiency without budget matching" 模式。
- Kang et al.(arXiv:2305.06474):rating prediction 上 LLM 用小部分数据匹配 CF——仅 Y 形式化,无排序协议。

**Q11(性能 vs 训练规模曲线):** 存在,但量纲不同。Ardalani et al.(arXiv:2208.08489,CTR/DLRM,数据/参数/算力三轴幂律);Zhang et al.(arXiv:2311.11351,ID 序列推荐 0.8B 参数的 scaling law);LLM-rec scaling laws(arXiv:2602.07298,ICML 2026,单任务持续预训练)。差异:(i) 它们扫 **unique raw interactions / 数据集规模**,本文的 task-sample exposure 是**派生任务样本累计数**——同一交互在 Y/N 形式化下产生不同数量的训练样本;(ii) 单一模型家族,从不含预训练 LLM vs ID 模型的对比;(iii) 从不沿数据轴比较任务形式化。Muennighoff et al.(arXiv:2305.16264)是 "unique tokens vs repeated epochs 是不同量纲" 的一般 ML 锚点,可直接引作本文 exposure 概念的方法学先例。SASRec 原文(arXiv:1808.09781)**没有任何训练数据量消融**(已核全文),本文的 "SASRec keeps improving" 相对其自身消融也是新观测。

**Q12(术语卫生):** Kaplan et al.(arXiv:2001.08361)显式区分模型规模/数据规模/算力三轴幂律;Ardalani et al. 在推荐场景命名同一三分法。建议正文用 "downstream task-sample exposure (cumulative derived task examples), distinct from unique raw interactions, compute, and parameters" 并引这两篇 + Muennighoff。

**复现性背景:** Ferrari Dacrema et al.(RecSys 2019)与 Rendle et al.(arXiv:1905.01395)均关于基线调参公平而非样本预算;可用来预防 "你的低曝光 SASRec 是欠训练的" 质疑——本文 "SASRec 随曝光持续改善" 正是该质疑的内置回应;同一质疑也反身适用于 TALLRec 的 few-shot baselines。

---

## 7. Claim-by-Claim Literature Support

| Claim | Supporting work | Exact support | Strength | Recommended wording |
|---|---|---|---|---|
| 推荐存在不同 operational prediction targets(rating vs implicit vs next-item) | Koren et al. 2009 (DOI 10.1109/MC.2009.263);Hu et al. ICDM'08 (DOI 10.1109/ICDM.2008.22);Rendle arXiv:2101.08769 | 三篇分别确立 rating prediction、implicit feedback、item prediction 作为不同问题形式化 | **强** | 直接引用作背景,无需新颖性声明 |
| 偏好预测监督与 next-interaction 监督产生不同 observed capability | P5(两形式共存但未对照);PerRecBench arXiv:2501.13391(rating 强的 LLM 在 grouped ranking 上失败);Rendle 2101.08769(rating≠item prediction 的前 LLM 论证) | PerRecBench 是定性先例但非预算受控微调研究 | 中-强 | "在匹配曝光的单一微调框架内受控比较两种监督形式化" 是安全表述;定性方向需承认 PerRecBench 先例 |
| Specialist-vs-multitask 差距随 per-task 曝光变化 | P5 Sec 5.6(固定数据);Penha et al. Fig. 4(单点);PLE(预算匹配但无数据轴);ITDR(两轴不交叉) | 无直接先例 | **强** | 可作为核心贡献表述,引上述四篇作为 "examined in isolation" 的证据 |
| 候选协议改变 apparent model gap | Krichene & Rendle KDD'20;Dallmann et al. RecSys'21;Zhao et al. CIKM'20;Cañamares & Castells RecSys'20;Gusak et al. RecSys'25;LLMRank ECIR'24 | 排序翻转有强先例;"gap 动态 + 微调 LLM + 非嵌套协议" 无先例 | 中(**一般性结论必须引先例,不可声称新发现**) | "将协议敏感性分析扩展到微调后的 recommendation LLM 与 specialist/multitask 差距动态";非嵌套协议处只说 sensitivity 不说 causation |
| 匹配下游任务样本曝光下 LLM vs SASRec | TALLRec(≤256 对齐);Laser(不对称反面);Kang et al.(仅 rating);RecBench(不对齐) | 24k–200k 匹配扫描无先例 | 强(条件化表述下) | "在匹配 task-sample exposure 下检验(明确 exposure≠compute、LLM 有预训练优势)";绝不说 "LLM universally beats SASRec" |

---

## 8. Novelty Conflict Report

**搜索范围内未发现 HIGH 级 conflict**(定义:同时研究 Y/N 式不同监督 + shared multitask vs specialists + matched per-task 曝光 + 候选协议鲁棒性)。搜索范围:arXiv API 16+ 查询、ar5iv 全文核验、DBLP/Semantic Scholar、本地 24 篇 PDF 全文;ACM DL 403 限制使部分 RecSys/KDD 正式版未能打开一手页面。

| Paper | Overlap | Severity | Affected contribution | Recommended reframing |
|---|---|---|---|---|
| **P5**(RecSys'22) | 同一 multitask LLM 含 Y/N 两种形式 + 固定数据 specialist ablation | **MEDIUM-HIGH** | C1, C2 | 必须正面引用并区分:其 specialists 预算不匹配、无曝光轴、seq 评估为全目录;本文是对其 Fig. 5 结论的曝光/协议条件化,需解释数据集/规模差异 |
| **ITDR**(2508.05667) | rating+next-item 同语料 + 数据规模分析 | **MEDIUM** | C1, C2 | 引为最近先例:移除式消融而非 matched specialists,规模与任务组成两轴不交叉,无协议变化、无 SASRec |
| **Penha et al.**(RecSys'24) | unified vs task-specific + 单点 added-task 数据实验 | **MEDIUM** | C2 | 引其 "何时统一模型胜出尚未确立" 的公开声明作 gap 支撑;指出其非 LLM 微调、无系统曝光扫描 |
| **TALLRec**(RecSys'23) | matched-budget LLM vs SASRec | **MEDIUM** | C4 | 明确其结论限于 K≤256 + AUC 协议;本文是该对比在真实曝光量级的延伸;顺带指出其 baseline MSE-loss handicap(谨慎措辞) |
| **PerRecBench**(2501.13391) | rating-强 LLM 排序失败 | LOW-MEDIUM | C1 | 引作方向性佐证而非竞争:其为 prompted 评测基准,非预算受控微调研究 |
| **RecBench**(NeurIPS'25) | LLM vs 常规模型横评,LLM 胜 | LOW-MEDIUM | C4 | 不可声称 "LLM 输给传统模型";本文只做条件化声明(at matched exposure, with crossover trend),与 RecBench 不矛盾 |
| **LLMRank**(ECIR'24) | 候选池构成影响 LLM 排序结论 | LOW-MEDIUM | C3 | 引作零样本先例;本文是微调后、受控 k 网格版本 |
| **Scaling laws 一系**(2208.08489 / 2311.11351 / 2602.07298) | 数据规模曲线 | LOW | C4 术语 | 用于区分 unique-data scaling vs task-sample exposure |
| **OneRec 家族** | 工业端到端生成式架构 | LOW | — | 仅作 "本文不提架构" 的对照定位 |
| **Laser**(2406.02368) | 样本效率声明 | LOW | C4 | 作为 "样本效率≠预算对齐" 的反面引用 |

**题名/事实纠正(引用前必改):**
1. Krichene & Rendle 是 **KDD 2020**,不是 RecSys 2020;arXiv:1912.02263 是 Rendle 单独的不同预印本("Evaluation Metrics for Item Recommendation under Sampling"),不要混引。
2. 不存在 "Offline Recommender Evaluation: Challenges and Opportunities" 这篇论文;Cañamares & Castells 的对应论文是 **"On Target Item Sampling in Offline Recommender System Evaluation"(RecSys 2020)**。
3. Dallmann et al. 没有 "Robustness of Evaluation Metrics" 一文;模型排序结果全在 **RecSys 2021 case study**。
4. VIP5(EMNLP 2023)是 P5 的多模态扩展,不是 "verified personalized prompt prefix"。
5. Ferrari Dacrema et al. "Are We Really Making Much Progress?" 的 arXiv 为 1911.07698(一个检索线报告了 1907.06902,引用前请再核)。
6. Rendle/Zhang/Koren 基线论文是 arXiv:1905.01395;iALS 后续是 2110.14037 / 2110.14044。
7. 本地 paper/tiger.pdf 是**错误的论文**(Python 类型推断,NTU/Fudan),不是 Rajput et al. NeurIPS 2023 生成式检索 TIGER——若要引用后者需另行获取。
8. P5 原文标题即含拼写 "Paradam"(sic);引 RecSys 2022 正式版 DOI 10.1145/3523227.3546767。

---

## 9. Recommended Related Work Additions

**必须进入正文:**
1. **P5**(Geng et al., RecSys 2022, arXiv:2203.13366)— Related Work "multitask LLM rec" 小节。同时是最近先例与主要 gap 引用:Y/N 两形式共存于其任务族(含相同的 rating≥4 二值化),Sec 5.6 是 specialist ablation 的唯一直接 LLM-rec 先例,但无曝光轴、无协议轴。
2. **TALLRec**(RecSys 2023, arXiv:2305.00447)— C4 相关小节。matched-budget LLM-vs-SASRec 的唯一直接先例,限于 K≤256 + AUC;本文是其量级延伸。也是 Y 形式化的代表工作。
3. **Penha et al.**(RecSys 2024, arXiv:2410.16823)— C2 相关小节。"何时统一模型胜出尚未确立" 的直接文献支撑 + 单点 added-task 数据实验。
4. **Krichene & Rendle**(KDD 2020)+ **Dallmann et al.**(RecSys 2021, arXiv:2107.13045)— 评估协议小节。采样指标不一致与模型排序改变的权威先例;Dallmann 是 uniform-vs-popularity 对比最近邻。
5. **Cañamares & Castells**(RecSys 2020, DOI 10.1145/3383313.3412259)— 评估协议小节。target-set 对 pairwise 对比的失真 + discriminative power 概念。
6. **Rendle, "Item Recommendation from Implicit Feedback"**(arXiv:2101.08769)— 任务定义背景。rating vs item prediction 形式化之分的 pre-LLM 锚点。
7. **LLaRA**(arXiv:2312.02445)— N 形式化代表 + "1+20 随机负例 HR@1" 作为领域默认协议的证据(本文 k 网格的动机)。
8. **Muennighoff et al.**(arXiv:2305.16264)+ **Kaplan et al.**(arXiv:2001.08361)— 术语卫生:exposure vs unique data vs compute。

**值得一句到两句:**
9. **ITDR**(arXiv:2508.05667)— 最近的 instruction 数据集先例(需先核全文曲线;见 §10)。
10. **LLMRank**(ECIR 2024)— 零样本候选池敏感性 + 流行度偏差。
11. **PLE**(RecSys 2020)— 预算匹配 MTL-vs-specialist 比较的 pre-LLM 权威与 seesaw 现象。
12. **PerRecBench**(arXiv:2501.13391)— C1 方向性佐证。
13. **SASRec**(ICDM 2018)— 基线定义 + 其 100 随机负例协议是本文协议轴所偏离的软默认;其无数据量消融值得一句。
14. **Wu et al. survey**(arXiv:2305.19860)— 领域分类法;其 Sec 5.4 对基准规模的沉默本身是 gap 证据。
15. **UniMP**(ICLR 2024)— 含 preference prediction + item rec 的已发表统一模型,防 "首次统一" 误读。

**不建议引用:** 本地 egrerank / PIER / PRM / RankMixer / Seq2Slate / DLCM / CMR / DIN(与三轴无重叠);KAR 边缘(LLM-as-feature 范式,可作一句话对照);本地 tiger.pdf(错误论文)。

---

## 10. Open Questions

1. **ITDR(arXiv:2508.05667)的曲线细节仅 metadata + 部分全文核验**——其 25/50/75% 消融的具体图表结论需要打开全文确认后再作为 "两轴不交叉" 的表述依据。
2. **LLM-rec scaling laws(arXiv:2602.07298)仅 metadata 核验**(标题/作者/摘要);其 SASRec 对比细节未读全文,引用前需核。
3. **LLaRA 的正式 venue**(常引作 SIGIR 2024)未能在一手页面确认,引用前核对。
4. **MMoE(KDD 2018)与 Rendle RecSys 2022 正式版**(DOI 10.1145/3523227.3546784)因 ACM 403 未核验;若引用需查 PDF。
5. **Ferrari Dacrema arXiv 编号存在两个报告值**(1911.07698 vs 1907.06902),引用前用 arXiv API 终裁。
6. **Cañamares et al. TOIS 2021**(false-positive metrics)仅书目核验,摘要未取到。
7. **PopMatch 无先例的判断**基于未检索到同名构造;"未发现 popularity-matched 评估构造" 的措辞已按此保守化,若投稿前有条件可再做一轮定向检索(Dallmann、Cañamares 全文附录)。
8. 搜索工具限制:本轮 WebSearch 多数返回空,核验以 arXiv API/abs/ar5iv 为主;**ACM/IEEE 付费全文未系统覆盖**,不排除存在未 arXiv 索引的会议工作。

---

## 附:核心引用清单(一手链接)

- P5: https://arxiv.org/abs/2203.13366 (DOI 10.1145/3523227.3546767)
- TALLRec: https://arxiv.org/abs/2305.00447 (DOI 10.1145/3604915.3608857)
- ITDR: https://arxiv.org/abs/2508.05667
- Penha et al.: https://arxiv.org/abs/2410.16823
- UniMP: https://arxiv.org/abs/2403.10667
- VIP5: https://arxiv.org/abs/2305.14302
- OpenP5: https://arxiv.org/abs/2306.11134
- M6-Rec: https://arxiv.org/abs/2205.08084
- OneRec: https://arxiv.org/abs/2502.18965(家族:2506.13695, 2508.20900, 2510.11639, 2512.24762, 2607.26500)
- LLaRA: https://arxiv.org/abs/2312.02445
- E4SRec: https://arxiv.org/abs/2312.02443
- iLoRA: https://arxiv.org/abs/2408.10159
- BIGRec: https://arxiv.org/abs/2308.08434
- GPT4Rec: https://arxiv.org/abs/2304.03879(注意与 arXiv:2406.08229 同名碰撞)
- Kang et al. rating prediction: https://arxiv.org/abs/2305.06474
- Laser: https://arxiv.org/abs/2406.02368
- RecBench: https://arxiv.org/abs/2503.05493
- PerRecBench: https://arxiv.org/abs/2501.13391
- RecRanker: https://arxiv.org/abs/2312.16018
- LLMRank: https://arxiv.org/abs/2305.08845
- Is ChatGPT a Good Recommender?: https://arxiv.org/abs/2304.10149
- Wu et al. survey: https://arxiv.org/abs/2305.19860
- Krichene & Rendle: https://doi.org/10.1145/3394486.3403226 (KDD 2020; IJCAI 2021 扩展 10.24963/ijcai.2021/651)
- Rendle sampled metrics: https://arxiv.org/abs/1912.02263
- Cañamares & Castells SIGIR'18: https://doi.org/10.1145/3209978.3210014
- Cañamares & Castells RecSys'20: https://doi.org/10.1145/3383313.3412259
- Dallmann et al.: https://arxiv.org/abs/2107.13045 (DOI 10.1145/3460231.3475943)
- Zhao et al. CIKM'20: https://arxiv.org/abs/2010.04484
- Li et al. AAAI'23: https://arxiv.org/abs/2211.15743
- Shi et al. WWW'23: https://arxiv.org/abs/2302.03472
- Gusak et al. RecSys'25: https://arxiv.org/abs/2507.16289
- Kostric & Balog SIGIR'26: https://arxiv.org/abs/2605.13053
- Ihemelandu & Ekstrand: https://arxiv.org/abs/2309.11723
- Cornell et al. (KGC): https://arxiv.org/abs/2402.00053
- SASRec: https://arxiv.org/abs/1808.09781
- Koren et al. 2009: https://doi.org/10.1109/MC.2009.263
- Hu et al. ICDM'08: https://doi.org/10.1109/ICDM.2008.22
- Rendle item rec: https://arxiv.org/abs/2101.08769
- Ferrari Dacrema et al.: https://arxiv.org/abs/1911.07698 (RecSys 2019)
- Rendle/Zhang/Koren: https://arxiv.org/abs/1905.01395
- iALS reevaluation: https://arxiv.org/abs/2110.14037
- Ardalani et al.: https://arxiv.org/abs/2208.08489
- Zhang et al. seq scaling: https://arxiv.org/abs/2311.11351
- LLM rec scaling laws: https://arxiv.org/abs/2602.07298
- Kaplan et al.: https://arxiv.org/abs/2001.08361
- Muennighoff et al.: https://arxiv.org/abs/2305.16264
- Covington et al.: https://doi.org/10.1145/2959100.2959190
- PLE: RecSys 2020(本地 PDF 已核全文;ACM 页 403)
- BERT4Rec: RecSys 2019(本地 PDF 已核;popularity 采样负例的协议变体)
