# Text Compression Audit

## A. Scope, Baseline, and Accounting Rule

本审计只制定压缩计划，不提供replacement prose，也不修改任何双语作者源、表格、Figure、submission或build。科学主线冻结为：在已评估推荐适配设置内，能力与相对模型表现的结论取决于supervision formulation、cumulative downstream task-sample exposure和candidate evaluation protocol。贡献层级保持C2 primary、C4 secondary、C3 supporting、C1 framing。

当前English IEEE PDF为14页。35个Markdown作者源包含84个正式段落：当前装配正文使用80段、约6,949个英文词；`paper/modules/00_contributions.md`另有4个工作段落、约310词，但不进入当前PDF，故不计页面收益。`modules`树另有2个空目录占位`.gitkeep`，合计37个文件。PDF标题位置显示Abstract从p1开始，Introduction p1，Related Work p2，Problem Formulation和Methodology p3，Experimental Setup p4，Results p5，Discussion p8，Limitations和Conclusion p12，References p13。Results浮动体持续到p11，因此章节跨页不等于纯文字占页。

P-LIGHT/P-BALANCED/P-AGGRESSIVE的word/page saving只计算本轮语义文字压缩，特别排除D-BALANCED已规划的Results逐点数字删减，避免重复计数。与T-BALANCED+D-BALANCED合并后的页数仅给reflow区间，不作机械相加保证。

## B. Section Function and Compression Map

PDF footprint同时给出当前视觉跨度和可归因的正文等效占页；后者为近似值，表图浮动会改变最终reflow。

| Section | Function / unique information | Main repetition | Class | Current words / paras | Approx. PDF footprint | P-BALANCED safe target | Est. prose saving | Risk |
| --- | --- | --- | --- | ---: | --- | ---: | ---: | --- |
| Abstract | 独立概括问题、设计、主要发现和三条件takeaway | 与Intro findings及Conclusion必然重复，但承担摘要自足性 | KEEP_NEAR_FULL | 232 / 1 | p1约0.5页 | 220-230 | 2-12词，近0页 | 高；不作为主要省页来源 |
| Introduction | context -> problem -> gap -> design -> findings -> contributions | p05-p07连续重复研究设计、结果和贡献；p01/p04与RW重合 | MODERATE_COMPRESSION | 709 / 7 | p1-p2，约1.1-1.3页 | 560-610 | 99-149词，0.12-0.20页 | 中；必须保留完整论证链和贡献层级 |
| Related Work | 证明问题有先例并定位本文多问了什么 | 每个主题第二段都再次介绍本文；P5/ITDR在多个主题承担近似角色 | HIGH_COMPRESSION_POTENTIAL | 852 / 9 | p2-p3，约1.2-1.4页 | 620-690 | 162-232词，0.20-0.30页 | 中；不能压成逐篇罗列或失去novelty boundary |
| Problem Formulation | 唯一定义H、H10、Y、N、M1和RQ1-RQ5 | Y/N/M1在Methods/Setup被局部重述 | KEEP_NEAR_FULL | 427 / 5 | p3约0.5-0.6页 | 370-405 | 22-57词，0.03-0.08页 | 高；定义删除会使后文失去语义锚点 |
| Methodology | 唯一给出时间合法性、目标构造、loss、QLoRA和scoring | overview重复Problem；training.p04预告Setup曝光统计 | MODERATE_COMPRESSION | 495 / 7 | p3-p4，约0.7-0.9页 | 420-455 | 40-75词，0.05-0.10页 | 高；复现和leakage规则不可牺牲 |
| Experimental Setup | 唯一操作化数据、曝光、协议、baseline和统计角色 | Table I/II已承载计数；开头重复设计；多处数字逐项复述表格 | HIGH_COMPRESSION_POTENTIAL | 1,005 / 13 | p4-p5，约1.3-1.6页含表 | 760-850 | 155-245词，0.18-0.30页 | 中高；不得丢actual/expected exposure和两类uncertainty |
| Results | 回答what happened，给minimum evidence和即时boundary | 开头重复全文路线；若干段尾提前承担Discussion；数值重复另属D-BALANCED | MODERATE_COMPRESSION | 1,546 / 16 | p5-p8正文，结果浮动体至p11；正文约1.8-2.2页 | 1,400-1,460，限非数字部分 | 86-146词，0.10-0.18页 | 高；需保留valid/test tension和protocol boundary |
| Discussion | 回答what findings mean，提出解释与报告实践 | 多小节首段重述Results；六主题可合成四组；首尾重复thesis | STRUCTURAL_MERGE_CANDIDATE | 905 / 14 | p8-p12受结果浮动体打断；正文约1.1-1.4页 | 610-700 | 205-295词，0.25-0.38页 | 中；必须保留解释，不能只剩结果摘要 |
| Limitations | 约束统计、评估、跨域和资源解释 | 单段内部边界可按主题高密度合并，外部重复是必要scope control | MODERATE_COMPRESSION | 363 / 4 | p12约0.45-0.60页 | 315-340 | 23-48词，0.03-0.07页 | 很高；只可收句，不能删边界 |
| Conclusion | 回答研究问了什么、三组核心发现和最终takeaway | p02-p03近似第二个Results，重复具体轨迹、种子、协议和Amazon | HIGH_COMPRESSION_POTENTIAL | 415 / 4 | p12-p13约0.55-0.75页 | 225-275 | 140-190词，0.17-0.25页 | 中；保持claim strength与三条件结论 |

P-BALANCED总安全区间约减少934-1,449词；考虑段落合并的实际可执行性，方案层面采用较保守的950-1,450词。

## C. Section-Specific Instructions

### Abstract

- Current role: 自足地给出问题、数据、比较、主要结果和三条件takeaway。
- Keep: 研究对象、两个数据集角色、Y/N/M1、五组核心证据、SASRec改善、Amazon directional范围。
- Compression: 只去除一处可有可无的连接性重复；不改变结果密度，不大改结构。
- Protected claim: 三条件限定和Amazon仅早期方向支撑。

### Introduction

| ID | Role | Audit |
| --- | --- | --- |
| intro.p01 | BACKGROUND | 与RW LLM背景重叠，可缩为领域与评估问题的入口。 |
| intro.p02 | PROBLEM | 保留完整监督形式问题，但无需预讲全部target/interface细节。 |
| intro.p03 | GAP | 保留exposure gap和total/per-task区别。 |
| intro.p04 | GAP | 保留candidate evaluation gap，文献枚举交给RW。 |
| intro.p05 | STUDY_DESIGN | 保留五组比较的一句话路线，删与p03/p04重复解释。 |
| intro.p06 | FINDINGS_PREVIEW | 保留C2主发现、C4次发现、C3边界和C1 framing，不逐项复刻Results。 |
| intro.p07 | CONTRIBUTIONS | 可与p06形成紧凑的findings-to-contributions收束，但必须显式保持C2>C4>C3>C1。 |

推荐从709词压到560-610词。p05-p07是主要回收点；不是删去贡献段，而是消除“做了什么 -> 发现什么 -> 同样内容再命名为贡献”的三遍复述。

### Related Work

- LLMs for Recommendation: 将zero-shot、P5、TALLRec、InstructRec压为“不同接口与适配形式”的综合定位，避免逐篇展开。
- Supervision Formulation: 保留explicit/implicit/sequential target差异与P5/ITDR共同接口先例，这是C1 framing的必要文献根基。
- Multitask/Unified: 保留P5、ITDR、OpenOneRec、Penha和OneReason的设计差异，但将“本文做什么”集中到段尾一次。
- Evaluation/Baseline: 保留sampled-evaluation风险、SASRec reproducibility和TALLRec/sequence-scaling的资源口径差异；不需每项研究都单独收束到本文。
- Synthesis: 只承担一段gap synthesis，不再复述完整研究设计。

推荐从852词压到620-690词，仍保留全部当前引用与“precedent不等于本文已被做过”的定位。

### Problem, Methodology, and Setup

- Definition primary home: `Problem Formulation`完整定义H/H10/Y/N/M1；后文只引用接口名。
- Temporal primary home: `Methodology`完整保留strictly earlier timestamp bucket、same-timestamp处理、N legal single-interaction target和history retention。
- Exposure primary home: `Experimental Setup`完整定义task-sample exposure、M1 expected per-task accounting和SASRec actual consumption。
- Tables I/II responsibility: 数量和运行点精度归表，正文只解释为什么样本群体不同、total与per-task为何不同、actual与expected为何不能混同。
- Statistical primary home: Setup完整区分seed42 paired bootstrap与n=3 training-run mean/SD；Results只报告必要区间状态，Limitations只说明推断边界。

推荐Problem减少22-57词，Methodology减少40-75词，Setup减少155-245词。三节合计217-377词，主要来自overview、表格数字复述和跨节再定义，而非删除复现信息。

### Results Non-Numeric Prose

不重开上一轮Numeric Audit。D-BALANCED继续负责逐点数列、重复CI和secondary metrics；本轮新增空间仅来自非数字叙述：

- `results.p01`: 将全文路线压成短导航，Amazon/valid-test角色已在Setup说明。
- `results.rq2.p03`: 保留Y/N response-profile结论，删除对“不同运行点代表不同适配程度”的长解释，移交Discussion。
- `results.rq3`: 保留Y preservation、validation narrowing、frozen-test modest N gap及不等价边界；删段尾重复综合。
- `results.rq4.p03`: 保留non-nested和jointly varied即时边界，不展开报告实践意义。
- `results.rq5.p02`: 保留“N领先且SASRec继续改善”的即时对照，资源公平解释交给Discussion/Limitations。
- `results.amazon.p02`: 完整保留directional-only范围，它不是冗余过渡。

非数字文字建议另减86-146词；与D-BALANCED的数字回收分开核算。

### Discussion

推荐从六个subsections压成四个主题组，不是只为少标题，而是让每组只回答一种“meaning”问题：

1. Supervision and capability interpretation: 合并semantics两段，保留native/bridge评估为何防止错误能力归因。
2. Exposure and specialization/unification: 合并exposure与unification，保留operating point、per-task allocation和conditional unification。
3. Evaluation protocol and baseline comparison: 合并protocol与baseline，先说明protocol-conditioned gap，再说明exposure-aware cross-family comparison及其局部公平性。
4. External validity: 合并Amazon两段，保留第二域只验证早期ranking directions。

`discussion.p01`缩为入口，`discussion.synthesis.p01`缩为一条三条件收束。所有具体数值与逐seed方向留Results/Table。推荐减少205-295词。

### Limitations

四主题结构本身正确，不合并成一个大段。每段采用“scope boundary + consequence”的高密度表达，保留全部边界。推荐只减少23-48词，不以Limitations换页面。

### Conclusion

未来可压为三段：p01说明研究问题；p02+p03合并为三组central findings；p04保留最终三条件takeaway。细节不再逐项复述所有曝光点、seed、协议和Amazon数值，但必须保留seed42-only trajectory、96k multiseed operating point、protocol-conditioned relationship、SASRec improving和Amazon directional-only的强度限定。推荐减少140-190词。

## D. Cross-Section Repetition Matrix

标记：`P`=PRIMARY_HOME，`S`=完成该节职责所需的SHORT_REFERENCE，`U`=当前可去除的不必要完整重复，`-`=无需出现。PRIMARY_HOME指完整定义或证据论证，不表示其他节不能报告其不同功能。

| Concept | Intro | Problem | Methods | Setup | Results | Discussion | Limitations | Conclusion |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Y vs N semantic distinction | S | P | S | U | P finding | S meaning | S whole-form boundary | S takeaway |
| H(u,t), H10 | - | P | S construction | U | - | - | - | - |
| strict temporal / same-timestamp rule | - | S | P | U | - | - | - | - |
| task-sample exposure definition | S gap | S RQ | S accounting basis | P | S use | S meaning | S measured-range boundary | S takeaway |
| M1 per-task exposure | S | S | S 1:1 | P | S comparison | S implication | P expectation caveat | S |
| validation vs frozen test | U | - | S | P policy | P evidence roles | U | P inference scope | S only tension |
| multiseed 96k | S preview | - | - | P design | P result | S interpretation | P scope | S |
| paired bootstrap | - | - | - | P method | S interval status | U | P distinction | U |
| candidate protocols non-nested | S gap | S RQ | - | P construction | P immediate boundary | S meaning | P scope consequence | S |
| N vs SASRec | S design/preview | S RQ | - | P baseline/alignment | P finding | S meaning | P resource boundary | S |
| Amazon directional boundary | S design/preview | - | - | P dataset role | P observation | S meaning | P generalization limit | S |

最严重的跨节重复不是单一一句，而是三条链：`intro.p05-p07 -> results -> discussion -> conclusion.p02-p03`对同一组findings反复完整概括；`Problem -> methodology.p01 -> setup.p01`反复定义研究维度；`Results段尾 -> Discussion段首`先后解释相同意义。

## E. Unique Information Principle

1. 定义只在PRIMARY_HOME完整出现；其他节用完成本节功能所需的最短引用。
2. Results负责finding + minimum evidence + immediate boundary；Discussion负责meaning、implication和reporting consequence。
3. Limitations中的重复是scope control，不能仅因别处提过就删；可压缩的是展开方式，不是边界本身。
4. Conclusion不重新证明结果，只保留三组central findings及三条件takeaway。
5. Abstract保持自足，因此其必要重复不参与主文去重。

## F. Paragraph Priority Map

`REMOVE_REDUNDANT_CONTENT`只授权未来删除段内重复成分，不等于删除整段。`MERGE_WITH_*`同样要求保留该段独有claim。Contribution Working Version不在当前PDF，分类仅用于未来源库一致性，不计省页。

| Paragraph ID | Priority | Keep / remove-repetition rationale |
| --- | --- | --- |
| abstract.p01 | KEEP | 独立科学审查后的自足摘要；只允许微调连接重复。 |
| contributions.p01 | KEEP | C1 framing工作记录，不在当前PDF。 |
| contributions.p02 | KEEP | C2 primary工作记录，不在当前PDF。 |
| contributions.p03 | KEEP | C3 supporting工作记录，不在当前PDF。 |
| contributions.p04 | KEEP | C4 secondary工作记录，不在当前PDF。 |
| intro.p01 | TIGHTEN | 背景与rw.llm重复；保留领域入口和评估问题。 |
| intro.p02 | KEEP | 主问题链的supervision formulation起点。 |
| intro.p03 | TIGHTEN | 保留exposure gap与total/per-task区别，删背景性铺陈。 |
| intro.p04 | TIGHTEN | 保留protocol gap，文献细节归Related Work。 |
| intro.p05 | TIGHTEN | 研究设计只需覆盖五组比较，不重释动机。 |
| intro.p06 | TIGHTEN | 保留分层findings preview，删逐项Results式展开。 |
| intro.p07 | MERGE_WITH_PREV | 与p06共同收束findings/contributions，保持C2>C4>C3>C1。 |
| rw.llm.p01 | TIGHTEN | 压缩zero-shot类型枚举，保留output interface定位。 |
| rw.llm.p02 | MERGE_WITH_PREV | adaptation先例可并入主题综合，保留P5/TALLRec/InstructRec差异。 |
| rw.tasks.p01 | KEEP | explicit/implicit/sequential target差异是C1必要定位。 |
| rw.tasks.p02 | MERGE_WITH_PREV | 与p01合成supervision主题，本文设计只在末句出现一次。 |
| rw.unified.p01 | TIGHTEN | 聚合P5/ITDR/OpenOneRec，不逐篇重复data-allocation意义。 |
| rw.unified.p02 | MERGE_WITH_PREV | Penha/OneReason保留为设计边界，合并本文gap收束。 |
| rw.evaluation.p01 | KEEP | sampled candidate结论风险是RQ4必要定位。 |
| rw.evaluation.p02 | MERGE_WITH_PREV | baseline/exposure先例并入同一比较主题，保留资源口径差异。 |
| rw.synthesis.p01 | TIGHTEN | 只做一次literature-to-gap synthesis，不复述完整study design。 |
| problem.p01 | KEEP | H、H10与两类prediction question的primary definition。 |
| methods.task.p01 | KEEP | Y target、rating threshold、bridge scoring不可删。 |
| methods.task.p02 | KEEP | N target、distractor非dislike及历史资格不可删。 |
| methods.task.p03 | KEEP | M1、M-Y/M-N和total/per-task关系不可删。 |
| problem.p02 | TIGHTEN | RQ1-RQ5全部保留，压缩连接性总结。 |
| methodology.p01 | REMOVE_REDUNDANT_CONTENT | pipeline overview重复Problem接口；保留方法路线一两句。 |
| methods.temporal.p01 | KEEP | Y timestamp bucket和strictly-earlier规则不可压丢。 |
| methods.temporal.p02 | KEEP | N legal target、same-timestamp bucket处理不可压丢。 |
| methods.training.p01 | KEEP | QLoRA/LoRA覆盖和关键超参数用于复现。 |
| methods.training.p02 | KEEP | response-only loss与M1 1:1是关键训练定义。 |
| methods.training.p03 | KEEP | Y/N likelihood scoring及multi-token规则不可删。 |
| methods.training.p04 | TIGHTEN | 保留effective batch与checkpoint逻辑，曝光细节交给Setup。 |
| setup.p01 | REMOVE_REDUNDANT_CONTENT | 三维设计和数据集角色重复Intro；保留valid/test政策入口。 |
| methods.datasets.p01 | TIGHTEN | Table I承担计数；正文保留Y/N样本差异原因。 |
| methods.datasets.p02 | TIGHTEN | Table I承担计数；保留Amazon数据域与早期test-only角色。 |
| methods.exposure.p01 | KEEP | task-sample exposure公式与非unique-interaction含义是primary home。 |
| methods.exposure.p02 | TIGHTEN | compact Table II承担逐run数字；保留M1 total/per-task及resume前提。 |
| methods.exposure.p03 | TIGHTEN | 表承担四点精确值；保留actual consumption和近似匹配边界。 |
| methods.evaluation.p01 | KEEP | native/bridge metrics与fixed threshold定义不可删。 |
| methods.evaluation.p02 | KEEP | Random/PopMatch构造、固定候选与retrospective边界不可删。 |
| methods.evaluation.p03 | KEEP | k20/k50 separate non-nested protocol定义不可删。 |
| methods.baseline.p01 | KEEP | 被评估SASRec实现及actual final batch范围用于复现。 |
| methods.baseline.p02 | TIGHTEN | 保留四点对齐、valid/test职责；高曝光参照一句即可。 |
| methods.statistics.p01 | KEEP | paired user bootstrap流程是唯一统计定义。 |
| methods.statistics.p02 | KEEP | multiseed/seed42 bootstrap、ddof与非等价边界不可删。 |
| results.p01 | REMOVE_REDUNDANT_CONTENT | 研究路线重复Intro/Setup；仅保留结果导航和证据范围。 |
| results.rq1.p01 | TIGHTEN | D-BALANCED承担数字去重；保留native/bridge核心contrast。 |
| results.rq1.p02 | TIGHTEN | 保留complete-formulation边界，删Discussion式延展。 |
| results.rq2.p01 | TIGHTEN | D-BALANCED压数值；保留Y limited/uneven finding。 |
| results.rq2.p02 | TIGHTEN | D-BALANCED压数列；保留N continued-improvement finding。 |
| results.rq2.p03 | REMOVE_REDUNDANT_CONTENT | 保留response-profile总结和过渡；operating-point意义归Discussion。 |
| results.rq3.p01 | TIGHTEN | 保留Y preservation与non-positive-transfer边界，数字归表。 |
| results.rq3.p02 | TIGHTEN | 保留valid narrowing、96k replication和non-equivalence。 |
| results.rq3.p03 | TIGHTEN | 保留frozen-test modest N gap及其与validation张力。 |
| results.rq4.p01 | TIGHTEN | 保留k20 substantially larger gap和跨seed/split一致性。 |
| results.rq4.p02 | TIGHTEN | 保留k50方向、较小幅度及non-monotonic boundary。 |
| results.rq4.p03 | KEEP | non-nested及count/composition/sampling joint variation是即时边界。 |
| results.rq5.p01 | TIGHTEN | 保留四点N领先；完整数列由Figure/Table承担。 |
| results.rq5.p02 | TIGHTEN | 保留SASRec改善与gap narrowing；compute解释归Limitations。 |
| results.amazon.p01 | TIGHTEN | 保留第二域排序顺序和最少anchor；完整metrics归Table XIV。 |
| results.amazon.p02 | KEEP | earlier-point directional-only范围不可删。 |
| discussion.p01 | REMOVE_REDUNDANT_CONTENT | 三条件总述已在Intro/Results出现；缩为讨论入口。 |
| discussion.semantics.p01 | KEEP | 提供capability应按prediction question解释的新含义。 |
| discussion.semantics.p02 | MERGE_WITH_PREV | benchmark-interface implication并入同一主题。 |
| discussion.exposure.p01 | KEEP | operating point如何改变比较含义是C2核心解释。 |
| discussion.exposure.p02 | TIGHTEN | 保留per-task accounting/reporting implication，删定义复述。 |
| discussion.unification.p01 | MERGE_WITH_PREV | 并入exposure主题，保留trajectory与replicated point区别。 |
| discussion.unification.p02 | MERGE_WITH_PREV | 并入conditional unification结论，保留seed42范围。 |
| discussion.protocol.p01 | REMOVE_REDUNDANT_CONTENT | 大部分是Results restatement；保留protocol-conditioned意义。 |
| discussion.protocol.p02 | TIGHTEN | 保留fixed-within/cross-protocol解释和非孤立factor边界。 |
| discussion.baseline.p01 | MERGE_WITH_PREV | 并入protocol/baseline主题，保留领先与追赶共存的解释。 |
| discussion.baseline.p02 | MERGE_WITH_PREV | 保留task exposure仅为partial comparison axis及资源限定。 |
| discussion.external.p01 | KEEP | Amazon跨域意义，但不重述数值。 |
| discussion.external.p02 | MERGE_WITH_PREV | 合并MovieLens detailed/Amazon directional角色。 |
| discussion.synthesis.p01 | TIGHTEN | 只留三条件综合和SASRec张力，不重复全文。 |
| limitations.training.p01 | TIGHTEN | 所有统计、范围、M1 expectation边界必须保留，可主题化收句。 |
| limitations.evaluation.p01 | TIGHTEN | 所有protocol、whole-formulation和sampled-set边界必须保留。 |
| limitations.cross_dataset.p01 | TIGHTEN | Amazon缺少trajectory/multiseed/protocol/native-Y的边界必须保留。 |
| limitations.compute.p01 | TIGHTEN | downstream exposure不等价compute/pretraining/token/FLOPs必须保留。 |
| conclusion.p01 | TIGHTEN | 研究问题和比较对象一段即可。 |
| conclusion.p02 | REMOVE_REDUNDANT_CONTENT | 保留C1/C2主发现及seed范围，删第二次Results式细节。 |
| conclusion.p03 | MERGE_WITH_PREV | 与p02合成三组central findings，保留C3/C4和Amazon边界。 |
| conclusion.p04 | KEEP | 最终三条件takeaway，措辞强度不得改变。 |

Coverage: 84/84 source paragraph IDs；其中80个进入当前submission，4个Contribution Working Version不进入当前PDF。

## G. NON_COMPRESSIBLE_CORE

未来任何执行模型必须把以下内容视为hard constraints：

1. Frozen thesis: capability和relative model performance由supervision formulation、cumulative downstream task-sample exposure及candidate evaluation protocol共同限定。
2. RQ1-RQ5均保留，且贡献层级保持C2 primary、C4 secondary、C3 supporting、C1 framing。
3. H(u,t)与H10定义；history严格早于target；same-timestamp bucket规则；N target是next interaction而非next liked item。
4. Y为rating-derived preference，N为next-interaction candidate selection，M1共享adapter但保留两个接口；比较针对完整formulation，不是被因果隔离的semantic factor。
5. Task-sample exposure统计累计消费且含重复样本；不同于unique interactions；M1需区分total与expected per-task exposure，后者依赖正确resume data skipping。
6. Validation指导决策，frozen test只在决策冻结后提供held-out report-only evidence。
7. 完整exposure trajectory仅seed42；seed43/44只复现96k operating point，不构成multiseed curve。
8. seed42 paired user bootstrap衡量固定模型的evaluation-sample uncertainty；n=3 mean/sample SD描述training-run variability；两者不可互换，zero-crossing CI不证明equivalence。
9. PopMatch-k5与random k20/k50为separately constructed、non-nested协议；count、composition、sampling method与difficulty共同变化，不能声称candidate-size causal effect。
10. Amazon只提供较早seed42 operating points的ranking-side directional support；不复现完整exposure、96k multiseed、hard protocol或native preference finding。
11. N与SASRec只按approximately matched downstream task-sample exposure比较；这不等价于pretraining、tokens、updates、FLOPs、wall-clock或deployment cost公平。
12. Y和N在已测范围外的convergence仍未知；不得把当前趋势外推为最终上限。
13. Final takeaway必须同时报告prediction formulation、cumulative downstream exposure和candidate evaluation protocol。
14. 未来EN/ZH必须同步修改，claim范围与强度逐段等价。

## H. Text Compression Plans

### P-LIGHT

- Actions: 删除明显重复定义；收紧Results非数字过渡和Discussion结果复述；Conclusion压成3段；其余仅句级精简。
- Word saving: 450-700 English words，排除D-BALANCED数值删减。
- Page saving: 约0.5-0.9页。
- Retains: 章节结构、六个Discussion小节、全部当前文献定位和复现细节。
- Risk: 低；Related Work和Setup仍偏长，主文大概率仍接近10-11页。

### P-BALANCED

- Actions: Intro收紧p05-p07；RW按四主题聚合；Problem/Methods/Setup执行primary-home去重；Results只留finding/evidence/boundary；Discussion合为四主题；Limitations高密度收句；Conclusion压成3段。
- Word saving: 950-1,450 English words，排除D-BALANCED数值删减。
- Page saving: 约1.1-1.8页。
- Retains: 五个RQ、全部NON_COMPRESSIBLE_CORE、当前引用覆盖、关键implementation/statistics与所有claim-strength boundary。
- Risk: 中低；执行时需逐段EN/ZH同步，并验证合并后引用位置与paragraph IDs策略。

### P-AGGRESSIVE

- Actions: short-paper叙事；Intro/RW大幅聚合；Setup主要依赖compact表；Method实现背景极简；Results只留最小证据；Discussion四主题各一段左右；Conclusion极短。
- Word saving: 1,800-2,350 English words，排除D-BALANCED数值删减。
- Page saving: 约2.0-2.9页。
- Retains: thesis、五RQ、必要定义、核心效应方向和hard boundaries。
- Loss/risk: 高；文献定位细腻度、复现上下文、valid/test与两类uncertainty的可读性会显著下降，审稿人更依赖表和supplement。只在明确short-paper硬页限下考虑。

## I. Combined Page Estimate

冻结的T-BALANCED+D-BALANCED联合预计先回收约2.4-3.8页。加入P档后，考虑float reflow和方案间局部重叠，当前14页的合理区间为：

| Combined plan | Expected final range | Interpretation |
| --- | --- | --- |
| T-BALANCED + D-BALANCED + P-LIGHT | 9.7-11.2 pages | 低风险，但未必达到高密度目标。 |
| T-BALANCED + D-BALANCED + P-BALANCED | 8.7-10.4 pages | 推荐；中心更接近9-10页，8页在有利reflow下可达。 |
| T-BALANCED + D-BALANCED + P-AGGRESSIVE | 7.6-9.4 pages | 7-8页才有较现实机会，但科学可读性和复现上下文损失明显。 |

结论：推荐组合不会自然稳定落到7-8页。8页存在有利情形，7页不应在无硬页限时作为目标；若实际重编译后为9页，也符合“科学完整、信息密度高”的当前目标。

## J. Old-Version Recovery Check

- Current manuscript contract: `paper/plan/review/manuscript_contract_2026-09-10.json`逐文件覆盖35份当前Markdown author source的SHA256；冻结树聚合记录另计2份`.gitkeep`，共37个文件，可检测漂移。
- Current generated EN/bilingual builds及manifest保留80个装配段落、源文件哈希和英文段落指纹，可辅助内容恢复与核验。
- Git status显示大部分作者源为staged additions，但10个Related Work/Discussion Markdown parts仍为untracked；因此Git历史本身不能保证逐字节恢复全部当前Markdown源。
- Existing contract是hash contract，不是内容snapshot；当前table archive只保护表，不保护manuscript。
- Recovery verdict: `PARTIAL / NOT EXECUTION-READY`。执行正文压缩前必须创建一次明确的pre-compression 35-source snapshot（可同时纳入2个`.gitkeep`）或等价提交，并记录manifest/SHA；本轮按用户要求不创建新正文snapshot。

## K. Recommendation and Execution Boundary

推荐`P-BALANCED`，标准顺序为scientific story clarity > defensibility > reproducibility > page cost。真正执行前先补齐manuscript旧版本snapshot，再一次性同步EN/ZH，并在执行后重建contract、编译两版、核对五RQ/NON_COMPRESSIBLE_CORE和页面。T-BALANCED、D-BALANCED与P-BALANCED仍需单独授权，本轮没有执行。

## L. Review

- Spec compliance review: PASS。10个正式section均有功能、词数、重复、target、page/risk；84/84源段落有唯一priority；11项repetition concept、三档P方案、NON_COMPRESSIBLE_CORE、联合页数和恢复检查齐全。
- Quality review: PASS。P方案未重复计入D-BALANCED numeric saving；定义、复现信息、valid/test tension、两类uncertainty、protocol non-nesting、Amazon和compute边界均受保护；推荐没有为命中7-8页夸大收益。
- Execution boundary: PLAN ONLY；未改manuscript/table/Figure/submission/build，未重编译，未访问Wiki，未调用GPT6 Astra，未研究experiment outputs。
