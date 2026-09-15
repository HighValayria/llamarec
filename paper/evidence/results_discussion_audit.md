# Results / Discussion / Limitations 一致性审查

日期：2026-09-08。状态：审查完成，修改建议未执行。

本轮以用户最新的“只记录修改计划，不直接修改”要求为准。没有修改双语正文、既有证据控制文件、图表、参考文献或旧构建产物。本文中的 REWRITE / REMOVE 均指后续建议，不表示已经修改。实施细节集中在[统一修改计划](F:/Projects/llamarec/paper/plan/task-packets/results-discussion-revision-plan.md)。

## 一、主要发现

三章已经保留了主要证据层次。没有发现将三种子96k运行点复现冒充完整多种子曝光曲线、将小差距写成等价，或将候选数量写成因果机制的正文错误。需要处理的是局部表述范围、比较身份和章节分工，不是重做论文故事。

| 编号 | 优先级 | 发现及影响 | 位置 | 建议 |
| --- | --- | --- | --- | --- |
| R01 | P1 | Y“收益逐渐减小”的概括没有限定指标/划分；验证AUC支持后段增量较小，测试AUC不是同样走势 | [RQ2](F:/Projects/llamarec/paper/modules_parts/results/rq2_exposure_response.md:14)的p01/p03；discussion.exposure.p01 | 限定为验证AUC增量变小、其他Y收益有限或不均匀 |
| R02 | P1 | RQ5及基线讨论混入较早高曝光SASRec对低曝光N的历史比较，容易被误读成正式四点中的反超或多种子轨迹 | [RQ5](F:/Projects/llamarec/paper/modules_parts/results/rq5_sasrec_exposure.md:25)；[基线讨论](F:/Projects/llamarec/paper/modules_parts/discussion/exposure_aware_baselines.md:25) | 从当前正式比较主线移除历史句，不否定历史数据 |
| R03 | P1 | RQ2报告桥接NDCG，却只引用不含该指标的binary_exposure表 | [RQ2](F:/Projects/llamarec/paper/modules_parts/results/rq2_exposure_response.md:14)的p01 EN/ZH | 补已有semantics_bridge表引用 |
| R04 | P1 | 独立novelty map仍写MS96待补，并笼统写hard条件差距更大；主冻结文件追加段已正确更新 | [新颖性映射](F:/Projects/llamarec/paper/evidence/final_novelty_claim_map.md:9)，第9、10、33行 | 后续只同步实证范围，不重新裁决文献新颖性 |
| R05 | P2 | Discussion有开头总述，但六节后没有整体收束，最后停在Amazon证据分工 | [Discussion](F:/Projects/llamarec/paper/modules/07_discussion.md:23) | 计划增加一个综合段，不进入Conclusion |
| R06 | P2 | Results少量一般报告启示与Discussion重复；Discussion局部重述结果，RQ3/RQ4数值较密 | rq1.p02、rq4.p03、amazon.p02及相应讨论 | 句级压缩，保留证据及过渡，不整章重写 |
| R07 | P2 | Limitations已有四类，但统计边界挤在评估段，尚未明确采样候选评估不是全目录评估 | [Limitations](F:/Projects/llamarec/paper/modules/08_limitations.md:23) | 统计说明归入训练/统计范围，补既有协议支持的范围句 |
| R08 | P2 | 基线标题裸用Sample Efficiency；两处中文“显著改善”容易被读成统计显著 | [基线讨论](F:/Projects/llamarec/paper/modules_parts/discussion/exposure_aware_baselines.md:4)、第18行；RQ5第29行 | 统一为下游任务曝光下表现；中文改“明显改善” |
| R09 | P2 | outline仍称Discussion的MS96更新在未来；协议表中文表头残留protocol | [提纲](F:/Projects/llamarec/paper/plan/outline.md:12)及manifest协议表 | 后续状态/表头整理，不改数据 |

P1表示下轮改稿应先处理的范围或追溯问题，不表示主要实验结论被推翻。P2为结构、紧凑度或表达问题。全部尚未实施。

## 二、范围与证据顺序

完整阅读七份控制文件：
[source_of_truth](F:/Projects/llamarec/paper/evidence/source_of_truth.md)、
[story_and_novelty_freeze](F:/Projects/llamarec/paper/evidence/story_and_novelty_freeze.md)、
[ms96_integration_summary](F:/Projects/llamarec/paper/evidence/ms96_integration_summary.md)、
[claim_matrix](F:/Projects/llamarec/paper/evidence/claim_matrix.md)、
[pending_evidence](F:/Projects/llamarec/paper/evidence/pending_evidence.md)、
[final_novelty_claim_map](F:/Projects/llamarec/paper/evidence/final_novelty_claim_map.md)、
[discussion_literature_update_notes](F:/Projects/llamarec/paper/evidence/discussion_literature_update_notes.md)。

完整阅读06/07/08及Results、Discussion全部parts，共33对EN/ZH段落；Limitations没有parts。00/01只读参考，共11对。定向核对已有Methods曝光定义、评估协议、统计说明、图表清单、对应CSV及既有证据测试。实际查看两张现有PNG。

优先使用MS96摘要、更新后的claim matrix和冻结文件末尾的证据更新。历史段落不因被检索到就重新成为当前限制。贡献编号C1-C4与finding编号C1-C9是两个命名空间。

没有访问正式Wiki、重新读取整个历史证据库、搜索文献、训练、推理或新增统计分析。全局只读装配检查读取其他模块仅为校验依赖，不开展其内容重写或进入摘要/结论写作。

## 三、科学事实核对

### RQ1与RQ2

Y/N涉及完整监督形式：目标构造、任务数据、提示及评分接口共同不同。原生偏好预测与桥接下一交互排序不是同一能力，不能用AUC和HR的数值大小直接比较能力强弱。RQ1及监督接口讨论保持了这一边界。

seed42的Y原生验证AUC为0.7761274819、0.7816111073、0.7843504067，后段增量较小。验证F1为0.7791746032、0.7848403087、0.7783174665，不是单调改善。测试AUC为0.7784561583、0.7804671174、0.7853511126，后段增量反而较大。因此，不宜将验证AUC的形态概括为所有Y指标、所有划分都收益递减。这里是核对已有点估计，不是新增统计分析。

Y桥接验证NDCG@5为0.6002715889、0.5994649797、0.6030699894；RQ2给出的范围正确，但支持它的是semantics_bridge，不是binary_exposure。

N在24/48/96/200k的两划分排序指标持续改善，正文正确。N200是接近完整合法样本池的一遍曝光参照，不是收敛点；已有methods.exposure.p03及表说明支持这一解释，不必每章重复。不能推断Y已收敛或N会无限改善。

### RQ3：三层证据与Y侧

1. 轨迹：seed42标准k5验证HR差距从48k的0.0088105727减至96k的0.0003524230。
2. 复现：seed42/43/44在96k均处于小差距区间。这是运行点复现，不是三个种子的48至96k轨迹。
3. 最终留出测试：96k三种子、三项排序指标均N高于M1。平均HR差距0.0101615272，训练种子样本标准差约0.002469057。seed42测试48k差距0.0093392070、96k差距0.0126872247，该区间并未收窄。

Y侧三种子测试点估计均为M1略高，但seed44验证Accuracy较Y低约0.0008884581。seed42验证AUC/Accuracy的bootstrap区间跨零，F1区间为正。现稿解释为保留被测偏好能力，而不是普遍正迁移，正确。上述三层、测试例外与Y验证例外都必须保留。

### RQ4：协议关系

三种子、两划分、三项排序指标在k20/k50下均N高于M1。k20差距比k5大；k50差距小于k20，且不总大于k5。验证HR平均差距约为k5 0.00587372、k20 0.08164464、k50 0.01027900；测试约为0.01016153、0.07765051、0.01010279。均引用已有汇总，不重新估计。

k5为流行度匹配5候选；k20/k50为随机20/50候选，独立构造且非嵌套。候选生成seed均为42，不等于训练seed都为42。数量、组成、采样及难度共同变化，不能解释为纯数量效应。

“k50幅度随seed变化”可用；不能升级为“k50标准差一定大于k20”或“候选越多差距越大”。精确嵌套比例的原审计文件尚未补齐，本轮不声称重新独立验证该比例。

### RQ5与Amazon

正式MovieLens链为N24/N48/N96/N200对应S47/S94/S188/S391。SASRec实际累计样本数为24,064/48,128/96,256/200,000。两划分上正式四点均N领先，SASRec继续改善，200k差距比96k小。近似对齐的是下游N任务曝光，不是计算成本。

正式表与图没有混入其他SASRec运行。问题在正文历史句：较早高曝光SASRec超过低曝光N属于另一个比较身份，不能被当成正式曲线的交叉点。历史finding C9可以真实存在，同时不适合继续夹在当前四点结果及对应讨论中。计划只删除当前主线中的两处历史句，不删除artifact或否定C9。

Amazon为较早seed42运行点、57,439个测试排序样本，支持N优于Y-as-ranker、N高于M1和被评估SASRec的排序侧方向。不能替代MovieLens完整曝光曲线、96k多种子行为、原生Y侧画像或替代候选协议复现。

## 四、Audit A-O

| 项目 | 当前判断 | 后续处理 |
| --- | --- | --- |
| A 主线 | RQ1形式/能力、RQ2响应、RQ3轨迹/复现/test、RQ4协议、RQ5四点、Amazon均存在，顺序合理 | 保留；R01/R02局部收紧 |
| B Results职责 | 以比较、数值、趋势及直接解释为主；RQ1p02/RQ4p03有少量一般报告启示 | R06句级压缩 |
| C Discussion职责 | 没有逐格报表或精确指标小数；exposure/unification/protocol/external部分重述发现 | 保留最低事实锚点，突出含义和跨RQ连接 |
| D seed42-only | 正文正确区分完整seed42轨迹与96k三seed；没有“所有结果单seed” | 正文OK；旧控制映射R04 |
| E 收窄与等价 | 验证48至96k收窄、96k运行点复现、测试优势已区分；跨零CI不证明等价 | 保留，不能压成“M追上N” |
| F Y侧 | 保留能力、seed44验证Accuracy例外、固定seed CI均准确 | OK，不升级正迁移 |
| G 协议 | 非嵌套、联合变化和k20/k50差异明确，没有单调数量因果 | 正文OK；旧映射R04 |
| H SASRec | 正式链准确，但历史比较句混入；标题裸样本效率 | R02/R08 |
| I validation/test | 选择与冻结后留出角色明确，test不是secondary；Results开头说明一次report-only合理 | OK，无需反复加限制 |
| J 不确定性 | 固定模型评估抽样、三seed训练变异、选择/留出角色分开 | 事实OK，R07只重排限制 |
| K 数字密度 | Results有必要数字，Discussion和Limitations无指标小数；RQ3/RQ4区间端点较密 | R06可压缩重复端点，原表保留 |
| L 段落完整性 | 33对均为自然论证段，未见连续一两句碎段或claim/caveat交替独立成段 | 不机械合并、扩写 |
| M 过渡 | RQ1至RQ2、RQ2至RQ3、RQ3至RQ4、RQ4至RQ5及Amazon均有连接 | 保留问题推进，不改成编号导航 |
| N 贡献层级 | RQ3最长，RQ4次之，RQ1不占最大篇幅；RQ5虽短但四点完整 | C2主/C4次/C3支撑/C1界定不变，不配平篇幅 |
| O 综合收束 | 三条件贯穿，但Discussion结尾只有跨域分工 | R05增加整体综合，避免每节重复三条件 |

按英文空白分词并去除图表标记，Results约1466词、Discussion约1034词、Limitations约351词。RQ1/2/3/4/5/Amazon约167/221/355/314/164/156词，Results开篇89词。这是编辑篇幅核对，不是实验统计。RQ4接近主贡献篇幅，应先精简重复数字，不给RQ5填充内容。

## 五、逐段职责记录

稳定段落ID用于定位。“压缩/补充”均是计划。EN/ZH同步核对范围、方向及例外。

| 段落ID | 当前职责与审查结果 | 动作 |
| --- | --- | --- |
| results.p01 | 路线、种子覆盖与test用途 | 保留 |
| results.rq1.p01 | 原生/桥接数值对照 | 保留 |
| results.rq1.p02 | 完整形式解释与曝光过渡，少量广泛启示 | R06 |
| results.rq2.p01 | Y验证与桥接；总括范围过宽、缺直接表引用 | R01/R03 |
| results.rq2.p02 | N两划分至200k走势 | 保留 |
| results.rq2.p03 | 响应差异和每任务对齐过渡，Y概括较宽 | R01 |
| results.rq3.p01 | Y保留能力、验证例外与CI | 保留事实，R06可缩CI复述 |
| results.rq3.p02 | 验证轨迹与96k复现分开 | 必须保留两层 |
| results.rq3.p03 | 最终test优势和48至96k不收窄例外 | 必须保留第三层 |
| results.rq4.p01 | k20跨seed方向与大小 | 保留，R06可缩逐指标CI |
| results.rq4.p02 | k50方向及非单调反例 | 保留反例 |
| results.rq4.p03 | 协议联合变化与跨家族过渡 | R06压缩报告建议 |
| results.rq5.p01 | 正式四点正结果 | 保留 |
| results.rq5.p02 | SASRec改善/差距收窄，夹带历史句 | R02/R08 |
| results.amazon.p01 | 第二域点估计与排序方向 | 保留 |
| results.amazon.p02 | 直接含义及跨域范围 | R06缩重复边界 |
| discussion.p01 | 三条件开场 | 保留，R05在章末收束 |
| discussion.semantics.p01 | 能力需绑定预测问题 | 保留 |
| discussion.semantics.p02 | benchmark解释及原生/桥接互补 | 保留 |
| discussion.exposure.p01 | 运行点含义，重复检查点且Y范围较宽 | R01/R06 |
| discussion.exposure.p02 | 每任务计量与预算解释 | 保留 |
| discussion.unification.p01 | 轨迹/运行点证据如何改变专家优势解释 | R06保留简短锚点 |
| discussion.unification.p02 | 共享能力的解释，协议内容稍重复 | R06把详细协议解释交下一节 |
| discussion.protocol.p01 | 单一k5不能代表其他条件 | 保留含义，减少重述 |
| discussion.protocol.p02 | 协议内配对与协议间敏感性 | R06缩重复构造；R05移交最终总括 |
| discussion.baseline.p01 | 领先与基线响应同时有意义 | 保留；R08中文强度 |
| discussion.baseline.p02 | 部分比较轴及资源范围，含历史句 | R02/R08 |
| discussion.external.p01 | 第二域方向的意义 | R06减少逐项排序复述 |
| discussion.external.p02 | 两数据集分工，不是全篇综合 | R06保留分工，R05另加综合 |
| limitations.training.p01 | 覆盖、末端未知、计数/优化范围 | R07接纳统计边界 |
| limitations.evaluation.p01 | 协议、回顾性流行度、完整形式，另挤入统计 | R07归位统计、补采样范围 |
| limitations.cross_dataset.p01 | Amazon仅排序方向 | 保留，可明确未覆盖96k多seed |
| limitations.compute.p01 | 曝光不等于资源或系统效率 | R08统一措辞 |

## 六、Redundancy Audit

| Claim | Results location | Discussion location | Keep in Results | Keep in Discussion | Action |
| --- | --- | --- | --- | --- | --- |
| Y/N capability distinction | results.rq1.p01/p02 | discussion.semantics.p01/p02 | 原生/桥接对照及完整形式限制 | 能力名称绑定预测问题 | 压缩Results一般benchmark启示 |
| Y/N exposure response | results.rq2.p01-p03 | discussion.exposure.p01/p02 | 点估计、划分范围、非均匀收益 | 运行点和每任务计量为何重要 | 限定Y范围；讨论不枚举全部检查点 |
| 48至96 gap narrowing | results.rq3.p02 | discussion.unification.p01 | seed42验证轨迹与差值 | 低预算优势不能代表以后 | 讨论留一句锚点，不重报数字 |
| 96k multiseed small-gap regime | results.rq3.p02/p03 | discussion.unification.p01/p02 | 三seed运行点、两划分角色 | 运行点复现增强哪层解释 | 保留，不能压成等价 |
| Y-side preservation | results.rq3.p01 | discussion.unification.p01 | seed44例外及CI解读 | 共享模型保留被测任务能力 | CI细节留表，不变成正迁移 |
| k20 specialist advantage | results.rq4.p01 | discussion.protocol.p01、unification.p02 | 方向与较大差距 | k5小差距不足以定义全面统一 | 协议节负责解释，上一节不再展开 |
| k50 direction | results.rq4.p02/p03 | discussion.protocol.p01/p02 | 小于k20、可小于k5的反例 | 非单调的协议敏感关系 | 保留反例，缩重复构造 |
| SASRec four-point trajectory | results.rq5.p01/p02 | discussion.baseline.p01/p02 | 四点领先、SASRec改善、200k收窄 | 优势绑定运行点 | 两处历史非匹配比较移出主线 |
| Amazon external check | results.amazon.p01/p02 | discussion.external.p01/p02 | 测试方向与范围 | 两数据集角色互补 | 缩排序列表与重复缺口清单 |

不建议为了消除表面重复合并validation/test表，也不删原始每seed值或用均值替代它们。

## 七、Stale-Claim Audit

检索覆盖33对主审段落和00/01的11对参考段落，并定向检查Methods、manifest和控制文件。未命中只指本轮正文范围；否定句、合法匹配术语和历史段落不能机械删除。

| 词项/词组 | 位置与语境 | 状态 | 判断 |
| --- | --- | --- | --- |
| parity | 正文无；freeze更新为否定边界 | OK | 无等价主张 |
| equivalence | results.rq3.p02、limitations.evaluation.p01 | OK | 分别说明CI不证明等价、未设等价界限 |
| equivalent | 正文无 | OK | 不新增 |
| match / matched / matching | RQ2/3每任务、RQ5/基线近似曝光、Amazon参照、popularity-matched及资源否定句 | OK | 不等于性能相等；RQ5有approximately范围 |
| single seed / single training seed | 正文无笼统命中 | OK | 轨迹与96k覆盖分别说明 |
| one seed / only one training run | 正文无笼统命中 | OK | 无所有结果单次运行泛称 |
| seed42 only / seed42-only | contributions.p02、limitations.training.p01 | OK | 仅限定完整轨迹 |
| positive transfer / transfer | results.rq3.p01 | OK | 明确未建立跨seed正迁移 |
| significant / significance / 显著 | 限制中否定跨seed显著性；RQ5p02及baseline.p01中文“显著改善” | REWRITE | 否定句保留，两处中文改“明显”，不伪造检验 |
| candidate size / candidate-size | contributions.p03、results.rq4.p03 | OK | 明确未隔离数量效应 |
| larger candidate | 正文无 | OK | 无大k单调规律 |
| monotonic / monotonically | results.rq4.p02、discussion.protocol.p01 | OK | 均否定单调差距增加 |
| sample efficiency / sample-efficiency | baseline标题/p02、limitations.compute.p01 | REWRITE | 标题裸用；正文有限定但宜统一为下游曝光下表现 |
| secondary test / secondary | 正文无 | OK | test是正式留出结果 |
| harder candidates / harder candidate conditions | intro.p05合法协议总称；novelty map第10行笼统larger gaps | REWRITE | Intro不必动；旧映射需区分k20与k50 |
| converged | 正文无；限制称convergence unresolved | OK | 不写已收敛 |
| plateau | 正文无 | OK | 不新增plateau证明 |
| universally | 正文无 | OK | 无家族普遍优越性 |
| always | 正文无 | OK | 无协议必然放大优势 |
| all metrics improve | 正文无该泛称 | OK | N轨迹与Y三seed测试各有明确范围，不推广到所有Y |
| narrow / narrows / narrowing / close / approach | RQ3/unification为seed42验证；RQ5/baseline为200k相对96k；Intro/贡献同范围 | OK | 未把验证收窄扩为测试或三seed轨迹；一般文献approaches不是等价 |
| improve / better / preserve / maintain | RQ2/3/4及对应讨论 | REWRITE | 保留能力与方向正确，只处理R01笼统Y递减 |
| hard candidate / difficulty / k20 / k50 | RQ4、protocol、限制、贡献和caption | OK | 联合变化明确，不推断纯数量因果或更大seed标准差 |
| validation / test / held-out / model selection | results.p01、RQ3、统计Methods和限制 | OK | 选择与最终留出分开，不必反复report-only |
| earlier high-exposure SASRec surpasses low-exposure N | results.rq5.p02、discussion.baseline.p02 | REMOVE | 历史真实但非正式四点，移出当前主线 |
| MS96 pending / 未来MS96 | novelty map第33行、outline第12行 | REWRITE | 同步状态；freeze旧段已有追加覆盖，保留历史 |

还逐处核对了seed42、seed43/44、three-seed：Results开篇、RQ2/3/4/5、Amazon；Discussion的exposure/unification/protocol/baseline；Limitations训练/评估/跨域段及00/01。未混淆训练seed与候选生成seed。旧literature notes中的“本轮未修改Discussion”是历史工作记录，不是本次状态声明。

## 八、Limitations与Discussion边界

目前已经是四个完整段落，而非按RQ的防御清单；没有重复HR或其他结果小数。后续建议：
1. 训练覆盖/统计范围：完整曲线仅seed42、96k三seed、固定模型bootstrap评估抽样、训练变异、无等价检验。将现有统计句从评估段移入此处，避免重复。
2. 评估协议：非嵌套、数量/组成/采样共同变、PopMatch回顾性流行度、完整Y/N形式。补“所报告候选排序比较是采样评估，并非穷尽全目录评估”。只限定所报评估，不宣称SASRec不能对全物品打分。
3. 跨数据集：Amazon旧seed42排序方向，不覆盖完整曝光、96k多seed和协议复现，不再报数值。
4. 资源/比较：曝光不等于预训练、token、更新次数、FLOPs、实际时间或服务成本。未测服务表现不推断。

Discussion并非每段都以“不能证明”收尾，无需整章重写。协议和外部效度中的系统性缺口可集中至Limitations；Discussion保留必要边界，先讲意义。

## 九、表格与图

清单有14张表，其中12张承担Results证据，另两张为数据集与训练计数。检查覆盖数值来源、表身份、caption、正文引用及既有冻结契约测试。

| 表 | 角色 | 结论 |
| --- | --- | --- |
| binary_exposure | seed42原生Y/M-Y两划分曝光点 | 保留，不能单独支持桥接NDCG |
| semantics_bridge | Y桥接与N96原生排序 | 数值正确，R03补引用 |
| exposure_scaling | seed42 N/M-N两划分轨迹 | 保留，N200不是收敛点 |
| specialist_multitask | seed42验证配对差值和原bootstrap CI | 保留固定模型评估抽样角色 |
| hard_candidate | seed42两划分三协议CI | 与新表部分重叠，但统计角色不同，不强制合并 |
| ms96_main_validation | 三seed96k原生任务 | 保留原始点估计与Y例外 |
| ms96_main_test | 冻结后正式留出复现 | 不与validation混表，不叫secondary |
| ms96_protocol_validation | 三seed三协议验证 | 保留协议、候选seed和三指标 |
| ms96_protocol_test | 三seed三协议最终留出 | 与验证分开，中文protocol表头可整理 |
| ms96_delta_summary | 24组差值mean/sample SD | n=3、等权、ddof=1，不是CI或检验，不替代原始值 |
| n_vs_sasrec_exposure | 正式四点两划分HR比较 | 表内只有正式链，不需改数据 |
| cross_dataset | Amazon早期seed42完整测试样本排序 | full-test不是full-catalog，范围正确 |

主表与协议表的k5重复属于不同入口。原CI表与三seed表的重叠服务不同不确定性层次。不建议盲目合并。正文可缩CI端点复述，但须保留关键大小、方向、区间解读与原始表引用。MRR“full candidate ranking”指完整采样候选列表，不是全目录。

已实际查看两张现有PNG并核对caption：
- [N曝光曲线](F:/Projects/llamarec/paper/figures/fig_n_native_exposure.png)：Validation HR@1，24/48/96/200k四点，与RQ2一致；seed42说明正确。
- [N/SASRec曝光图](F:/Projects/llamarec/paper/figures/fig_n_vs_sasrec_exposure.png)：四点N均较高，SASRec至200k改善明显；纵轴为validation HR@1。N-K0旧图例已由caption解释为N24/N48/N96/N200系列。

图内/caption无parity、数量因果或普遍效率主张。两图没有承担96k多seed协议复现的展示职责，新表已经承担，所以没有必须重画的证据缺口，不新增绘图流程或figure_revision_notes。未生成排版PDF；宽表最终版式不在本轮范围。

## 十、冻结章节与控制记录

00/01的贡献层级、RQ3三层范围、k20/k50区分、正式SASRec四点和Amazon身份与Results一致。00无需修改。intro.p06复用“Y增益减弱”概括，列为R01联动复核项；不默认改引言，只有后续采用更精确范围后存在实质不一致，才提出单句同步，不能借机润色其余内容。

Related Work与Methods保持原样。05相关曝光、统计、评估说明没有与已核Results相矛盾的事实。文献新颖性、近邻工作和贡献排序不重新裁决。

final_novelty_claim_map需要实证状态跟进，但只列入计划。story_and_novelty_freeze原历史段已被末尾更新明确覆盖，不回改历史。claim_matrix与pending_evidence已正确标明MS96整合，不因本次审查而清空独立缺口。

## 十一、验证记录

本轮实际运行：
- `python -B -X utf8 -m unittest discover -s paper/assembly/tests -v`：47项通过。
- `python -B -X utf8 paper/assembly/assemble.py --modules results discussion limitations --lang bilingual --check`：3模块、33对段落、0处待补，通过。
- `python -B -X utf8 paper/assembly/assemble.py --lang bilingual --check`：11模块、78对段落、8处既有待补，draft结构检查通过；没有生成整稿。
- `python -B -X utf8 paper/assembly/assemble.py --lang bilingual --mode final --check`：exit 1，受METHOD_CITATIONS、RUN_METADATA、BOOTSTRAP_PROVENANCE、draft/skeleton及未写摘要/结论阻拦。不能称final验证通过。
- `python -B -X utf8 tools/stage_guard.py`：管理记录更新前0错误、0警告；更新后复查记录在交付核验中。
- EN/ZH人工核对覆盖33对主审及11对参考段落；自动检查覆盖段落对、数值/引用对称、证据标记、表图引用。结构通过不意味着R01/R02等语义问题消失。

中断前189个既有paper文件逐一SHA-256一致；额度拦截没有创建报告或计划。恢复后再次建立189文件基线，用于核对本轮新增文档前后原文件不变，排除__pycache__。没有运行prepare_assets.py、新bootstrap、训练或推理；既有单测只验证已存在的数据契约。最终哈希和diff检查见末尾交付核验。

## 十二、下一步判断

现有证据足以支持带数据集、种子、运行点和协议边界的经验结论。R01-R09均不需要新增实验来修复，应先由用户审阅，再决定是否授权局部改稿。

这不等于投稿级复现记录完整。RUN_METADATA、BOOTSTRAP_PROVENANCE、METHOD_CITATIONS和TEMPLATE_UNASSIGNED仍保留；前两项首先是记录与来源恢复问题，不能假定必须重训，也不能假定必能无实验恢复。跨域完整曲线、完整多seed轨迹、等价性、正迁移或机制因果不在当前证据范围内，本轮不设计补实验。

结论写作没有新发现的科学证据硬阻塞，但应先确认范围修正和比较身份。此次完成的是审查与修改计划，不是“正文已经修好”的验收，不是Conclusion/Abstract完成。到此停止。

## 十三、交付核验

- 恢复后再次运行47项既有单测，全部通过；三章33对/0待补、全局78对/8既有待补的只读检查再次通过。
- final只读探针仍为exit 1，原因与第十一节一致；不将预期门禁阻拦说成最终稿通过。
- 189个预先存在的paper文件SHA-256逐项一致，当前共191个非缓存文件，新增项恰为本审查报告与统一修改计划。EN/ZH作者源、旧证据控制、表图、参考资产、旧build和既有计划均未改动。
- 两份新文档共34个本地文件链接全部存在，未发现UTF-8替换字符；33个主审段落ID全部进入逐段表，A-O无漏项，计划R01-R09齐全。
- 管理记录更新后stage_guard为0错误、0警告。git diff --check为exit 0，无空白错误，只有68条既有LF/CRLF提示。
- 本轮仅另行维护.agent/current_task.md和.agent/stage_state.yaml两份行政记录；未读取或修改正式Wiki。所有修改建议仍未执行，本轮交付完成后停止。
