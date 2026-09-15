# Conclusion 科学审查与最小修改计划

日期：2026-09-09。模式：REVIEW ONLY / PLAN ONLY。审查对象为现有双语 Conclusion 初稿；本文记录建议，不应用任何正文修改。

## A. Overall verdict

**MINOR_REVISE**。

当前 Conclusion 准确代表冻结的科学故事，完成了从研究问题、具体发现到报告原则的收束。没有科学冲突，也没有需要降级的实质性过强论断。建议两处局部改进：把 N 已观察到的改善方向说清楚，压缩开头与结尾的重复解释，让曝光条件下专家与共享模型关系的变化更突出。

| 等级 | 数量 | 判断 |
| --- | --- | --- |
| P0：Scientific contradiction | 0 | 未发现与冻结证据相反的结论 |
| P1：Claim strength / scope problem | 0 | 未发现语义因果、三seed全轨迹、等价、正迁移或跨域/计算外推 |
| P2：Narrative / redundancy problem | 2 | R01：N的改善方向被弱化；R02：重复框定分散主发现的强调 |
| P3：Optional polish | 1 | R03：可局部补明非嵌套关系，提高协议段的独立可读性 |

P2并不意味着已有发现不成立。R01恢复已获支持的描述性方向；R02调整表达分工。无需新证据、实验或文献，不建议重写整章。

## B. Current story extracted from Conclusion

现稿实际讲的是：共享适配设置中的“推荐能力”随完整预测问题而异，模型间的距离也随任务监督积累与候选评估条件而变化。最关键的例子是，seed42标准k5验证比较在48k到96k之间明显接近，而三个训练seed在96k复现较小差距、测试仍偏向N；M1在这个运行点同时保持接近Y专家的偏好表现。因此，低预算时看到的专家优势不能直接概括共享模型进一步适配后的表现。

候选协议揭示这一接近关系的范围，SASRec四个近似曝光匹配点说明跨模型系列的优势也有具体监督条件；Amazon提供的是早期运行点的外部排序方向支持。末段据此要求把预测形式、累计任务样本曝光和候选协议与模型表现一起报告。它没有提出新模型、评估框架或基准。

## C. Evidence-to-claim audit

定位以现有 paragraph ID 和同一语言段内句序为准。下表的C1-C8为finding ID；贡献层级的C2/C4/C3/C1是另一套编号，不能混用。证据以[claim matrix](F:/Projects/llamarec/paper/evidence/claim_matrix.md)、[source of truth](F:/Projects/llamarec/paper/evidence/source_of_truth.md)及[故事冻结文件的MS96追加更新](F:/Projects/llamarec/paper/evidence/story_and_novelty_freeze.md)为准。冻结文件前部“MS96待处理”等历史文字已被末尾更新覆盖。

| Claim | Conclusion wording | Evidence support | Verdict | Priority |
| --- | --- | --- | --- | --- |
| 核心thesis | p01 “across complete supervision formulations…exposure…protocols”；p04要求与三个条件一起报告 | Core Thesis；intro.p04/p07；discussion.synthesis.p01 | 科学含义一致；p01/p04有叙事重复。原则性报告建议可接受，不等于证明普遍因果规律 | P2 / R02 |
| 监督问题与能力结构 | p02 s1 “distinct measured capability profiles”；s2明确“complete prediction formulations” | finding C1、M1/M4；贡献p01；discussion.semantics.p01/p02 | 通过。Y/N比较指完整问题；“produced”与下一句合读不构成语义单因素归因。没有潜在能力独立性或AUC/HR跨量纲判断 | 无 |
| Y曝光响应 | p02 s3 “measured gains through 96k were limited or uneven across metrics” | finding C2；intro.p06；discussion.exposure.p01 | 通过。没有把某个验证指标的后段小增量写成所有指标/test收益递减，也没有收敛或饱和判断 | 无 |
| N曝光响应 | p02 s3 “remained exposure-sensitive through the evaluated 200k point” | finding C3明确24/48/96/200k排序持续上升；intro.p06及discussion.exposure.p01明确持续改善；本轮任务明确两split范围 | 正确但弱于已有证据。“敏感/有响应”不说明变好还是变坏，削弱Y/N响应对照；原起草任务允许此措辞，故不判科学错误 | P2 / R01 |
| 专家/共享随曝光接近 | p02 s4明确seed42同一轨迹、standard-k5 validation、48k到96k每任务 | finding C5、M3；贡献p02；freeze的MS96更新 | 通过。收窄仅指seed42标准k5验证轨迹；不误归于test或额外seed的轨迹 | 无 |
| 96k复现与留出差距 | p02 s5 “Independent seeds 43 and 44…96k small-gap regime”；“frozen tests…modest N advantage” | finding C5；intro.p06；discussion.unification.p01/p02 | 通过。完整保留轨迹变化、运行点复现、留出集剩余优势三层关系；没有等价或追平结论 | 无 |
| Y侧多任务表现 | p02 s6 “preserved comparable measured Y-side preference capability” | finding C4；贡献p02；MS96追加更新 | 通过。只作描述性接近判断，不把三seed test略高或单项区间解释为正迁移 | 无 |
| k20相对k5 | p03 s1/s2由standard-k5承接到“much larger N-specialist advantage…all three…both data splits” | finding C6；贡献p03；discussion.protocol.p01 | 通过。比较对象由前一句明确为k5；三训练seed、validation/test、96k范围正确 | 无 |
| k50与候选条件 | p03 s3 “favored N, but by less than k20 and with seed-dependent magnitude”；联合变化归于协议整体 | finding C6、M5；freeze更新；discussion.protocol.p01/p02 | 通过。没有说k50一定比k5差距大，也没有说变异绝对大于k20；当前未重述“非嵌套”和“不总大于k5”，是可接受压缩 | P3 / R03（可选） |
| N与SASRec | p03 s4/s5 “all four approximately matched downstream task-sample exposures”；基线改善、200k gap小于96k | finding C7/M7；贡献p04；intro.p06；discussion.baseline.p01/p02 | 通过。对应N24/S47、N48/S94、N96/S188、N200/S391四个正式点；没有普遍优越性、预训练公平、计算效率或不会反超的断言 | 无 |
| Amazon | p03 s6 “only…earlier seed42 operating points”；“directional external support” | finding C8；intro.p05/p06；discussion.external.p01/p02 | 通过。N高于Y-as-ranker、M1、被评估SASRec的方向明确；未把ML详细轨迹、三seed96k或协议结果外推到Amazon | 无 |
| 最终综合判断 | p04 “reported together with…prediction formulation…exposure…protocol” | Core Thesis；intro.p07；discussion.synthesis.p01 | 通过。是现有经验观察支持的解释和报告原则，没有新benchmark/方法宣称 | 无；叙事压缩合并计入R02 |

额外边界检查：没有精确CI、p值、跨seed显著性、等价性检验或收敛推断；没有预训练、共享表示或困难候选的未经验证机制；没有内部provenance标记或citation/hash工作流文字。无需因尚未闭合的运行/统计溯源而降级已冻结的描述性结果。

## D. Missing takeaway audit

| 必查内容 | 当前覆盖 | 是否遗漏 |
| --- | --- | --- |
| supervision | p01设置、p02完整预测问题与不同被测能力 | 没有；无需再次展开公式或比较AUC/HR绝对数值 |
| exposure | p02分别写Y到96k与N到200k、seed42轨迹 | 没有整个finding缺失；N的正向改善被压弱，见R01 |
| multitask | p02是主实证段，含收窄、96k复现、test剩余差距及Y保留 | 没有；必须整体保留证据层级 |
| protocol | p03保留k20大差距、k50较小及seed变化、联合构造差异 | 没有；不强求Conclusion重新列所有协议定义 |
| SASRec | p03正面写四点领先、基线改善和200k相对96k收窄 | 没有；没有写成模糊的“some differences” |
| Amazon | p03限定较早seed42点的三个排序方向 | 没有；完整数据版本身份无需在Conclusion重复引用 |
| final synthesis | p04提供三个条件与解释原则 | 明确，建议保留核心句并减少与p01的重复 |

### 与Introduction的对称性

[引言](F:/Projects/llamarec/paper/modules/01_introduction.md)中，p02的预测问题区分由Conclusion p02回应；p03/p04的“额外监督后专家/共享及LLM/序列基线关系如何变化”由Conclusion p02/p03回应；不同候选条件下关系是否保持由p03回应；p05的外部排序检验由p03末句回应；p07的整体意义由p04收束。问题、观察和最终含义基本闭合，没有发现引言承诺了却在结论完全失踪的重要问题。

### 与贡献层级的对齐

[贡献](F:/Projects/llamarec/paper/modules/00_contributions.md)和冻结定位要求C2主、C4次、C3支撑、C1界定。现稿大体遵守：p02的曝光条件下N/M1关系是实证主干；p03的SASRec提供第二主贡献；协议限定紧接N/M1结果，在论证顺序上先于SASRec是合理承接，不等于贡献排序被颠倒。开头和结尾的框定篇幅较多，但没有把监督区分包装成最大创新。R02只改善主发现的突出程度，不重排贡献或增加SASRec数字。

## E. Redundancy audit

英文按现有同一计词规则为479词，四段分别102、150、149、78词，篇幅在原起草目标内。中文四段与其对应。没有精确小数、图表、CI或整套指标复述，也没有逐段罗列局限。功能上属于已经完成科学综合、仍有局部冗余的Conclusion。

| 位置 | 重合或功能 | 建议 |
| --- | --- | --- |
| p01 s1/s2 | 概括研究问题和设计，能独立把读者带回全文对象 | 保留，必要时紧缩；不判为重复Methods的错误 |
| p01 s3/s4 与 p04 s1-s3 | 都在解释能力不宜脱离条件、三项条件须随比较报告、单一运行点不能泛化；也与discussion.p01及synthesis主题重合 | 主要可压缩区。开头负责设置范围，末段负责最后认识，无需在两处各展开一轮 |
| p02 s4-s6 | 与intro.p06和discussion.unification内容重合，但承担主发现及其证据层级的总结 | 保留。重复核心发现是Conclusion所需，不应为了“去重复”删掉96k复现或test优势 |
| p02 s7 | 再次说接近专家且冻结test留有gap，重复s5；末尾seed42全轨迹范围仍必要 | R02中可合并重复的test gap短语，把该句用于解释低预算判断的局限；seed范围必须仍明确 |
| p03 s2/s3 | 重述Discussion协议结论，给出标准k5接近关系的重要边界 | 保留方向和比较基准；不展开更多协议数字 |
| p03 s4/s5 | 用SASRec说明跨家族比较的监督条件，是第二主贡献 | 保留四点领先与基线继续改善的并置，不以免责声明替代 |
| p03 s6 | 一句话完整控制Amazon角色 | 保留；无需再加“未做binary/hard/multiseed”的清单 |
| p04中间句 | “Claims…reported together with…”准确完成最终takeaway | 保留核心内容；它本身不是新评估方法 |

与Discussion的主题重叠是必要的，未发现大段逐字复制。问题集中在Conclusion内部两次展开同一个报告原则，以及p02重复一次test差距，不能据此判为整章重写。不得再添加一段“Although/However/We cannot”清单。

## F. Revision plan

所有条目状态均为 **PROPOSED / NOT APPLIED**。本轮未修改Conclusion。R01与R02建议执行；R03可选。执行时仍保持四对段落及现有ID，英文维持原有350-550词范围，语义、条件和证据方向须中英同步。

### R01 / P2：写清N已经观察到的改善方向

- Location：[conclusion.p02英文第3句](F:/Projects/llamarec/paper/modules/09_conclusion.md:23)及[中文对应句](F:/Projects/llamarec/paper/modules/09_conclusion.md:27)。
- Problem：“remained exposure-sensitive / 仍对曝光保持响应”只表明有变化，没有明确持续改善；使已经得到正面回答的曝光问题变弱。该措辞符合原起草允许范围，故不升级为P1。
- Intended change：在同一句中把N分句改为排序在两个划分的已测点上持续改善至200k。顺带在本段首次提到轨迹处点明MovieLens seed42，帮助读者区别ML详细分析与Amazon外部方向支持；不另开局限段。无需填入精确增量。
- Must preserve：Y到96k的limited/uneven；N的截止点200k；完整轨迹仅seed42；M1收窄仍限定标准k5验证。
- Must not introduce：Y饱和、N收敛或“已证明未收敛”、200k之后预测、三seed全曝光曲线、Amazon同样持续改善。
- Acceptance：N明确使用改善方向；EN/ZH均有相同数据集、seed、split和区间范围，无新数值或检验。

### R02 / P2：减少重复框定，突出主发现的含义

- Location：[conclusion.p01英文第3/4句及中文对应句](F:/Projects/llamarec/paper/modules/09_conclusion.md:12)、[p02最后一句](F:/Projects/llamarec/paper/modules/09_conclusion.md:23)、[p04收束段](F:/Projects/llamarec/paper/modules/09_conclusion.md:45)。
- Problem：p01已展开一轮“模型能力须结合三个条件解释”，p04再次展开；p02末句又重复s5的test剩余gap。读者能理解报告原则，但主贡献“低曝光关系不能固定代表共享模型后续表现”的含义被一般性提醒分散。
- Intended change：保留p01研究范围与设计，只用紧凑判断承接后文；p02保留s4-s6的具体证据链，将末句的重复部分收成低预算专家优势不足以概括进一步适配后共享表现的含义，仍明确seed42全轨迹边界。p04保留与预测形式、任务曝光和候选协议一起报告的核心句，收紧其余同义句。只压缩或合并重复句，不大段重写、不要求改变四段结构。
- Must preserve：C2主/C4次的关系；seed42验证收窄与三seed96k复现的区别；冻结test仍有N小幅优势；同一M1的Y侧能力保留；最后三个条件的清楚收束。p03的SASRec和Amazon证据不因此删除。
- Must not introduce：把主要发现降成“存在某些差异”、改为普遍多任务成功/失败、三因素全因子设计、框架/基准创新、语义独立能力；也不增加未来实验或provenance免责声明。
- Acceptance：开头与结尾分工清楚；主发现得到一句解释；必要条件在Conclusion内仍完整出现；结尾读者仍能说出监督什么、累计多少任务监督、如何评估候选。

### R03 / P3，可选：让协议边界更易独立理解

- Location：[conclusion.p03英文第3句](F:/Projects/llamarec/paper/modules/09_conclusion.md:34)及[中文对应句](F:/Projects/llamarec/paper/modules/09_conclusion.md:38)。
- Problem：当前“independently constructed”没有逐字明示non-nested；读过Methods/Discussion可理解，单独阅读Conclusion则少一个直接线索。现稿已明确联合变化，故不存在候选数量因果误写。
- Intended change：在现有候选集合构造短语中补一个“非嵌套”的限定，明确修饰跨协议集合关系即可；不新增独立方法说明。k50不总大于k5可以继续留在前文，当前省略不构成虚假概括。
- Must preserve：k20相对k5更大；k50小于k20且幅度随seed变化；协议整体解释。
- Must not introduce：将独立构造理解为统计独立；“k50波动一定比k20大”；所有较大候选都放大差距；纯数量因果。
- Acceptance：EN/ZH对同一关系补同一限定，长度不因补定义而膨胀。若用户优先原文简洁，可不执行。

## G. 双语与统计措辞核对

| 段落 | claim strength / scope | seed / split / protocol / comparison identity | 裁决 |
| --- | --- | --- | --- |
| p01 | EN更绝对的“does not support a context-free notion”与ZH“不能充分解释”略有语气差别；二者仍同指解释原则 | 共同适配设置，Y/N/M1与N/SASRec身份一致 | 无科学强度错配；R02压缩时顺便统一正向口吻，不额外计P1 |
| p02 | measured、limited/uneven、comparable、modest均对齐；中文“形成”不比英文produced多引入机制 | seed42全轨迹；43/44的96k复现；k5 validation收窄；冻结test N略强；Y到96k、N到200k一致 | 通过；N两语都同样写弱，按R01一并调整 |
| p03 | larger/smaller、seed-dependent、led、improved substantially均语义对应；中文“明显”没有替换成统计“显著” | 三训练seed/两split只绑定96k协议比较；四点SASRec不冒充三seed轨迹；Amazon earlier seed42与方向一致 | 通过；“both data splits”的指代可由validation/test语境确定 |
| p04 | “most informative”与“应同时说明”都承担报告建议，不是新实证检验 | 三个条件一致；不额外延展到所有模型/所有数据 | 通过；R02属于收束和重复处理 |

Conclusion没有equivalence/positive transfer/significant等正面论断，也没有“证明”“显著”“收敛”“持平”“等价”所对应的更强中文统计结论。没有新claim、未新增方法引用、未用未闭合provenance构造强判断。没有把“无法推广到所有条件”写成“模型在其他条件一定失败”。

## H. 读取范围与验证

完整阅读：Conclusion、Contributions、Introduction、Discussion wrapper及其直接INCLUDE的六个parts、故事冻结文件与claim matrix。为核对N改善方向和C5/C6/C7范围，定向阅读获准的source_of_truth。另读取必要的两份.agent状态。

未读取Results全文、训练/推理输出、日志、全部表格、provenance计划、文献笔记或Wiki；没有网络检索、实验数据统计、新图表或任何正文写入。本文表格均为审查映射，不是新实验表。

审查开始时Conclusion的SHA256：

`4A9890E9CCEF033F75BC855FDF36E81DA23A667B54294D29932517EB7FE99AC4`

- Conclusion双语只读装配已执行并通过：1模块、4对段落、0待补标记，exit 0。
- 正文内容与证据范围经逐段人工审查；四段英文479词，无新引用。词数检查不是实验统计。
- 写入本计划和必要状态后，执行stage_guard、指定diff-check与13份已读论文材料的哈希复核；结果见下方最终记录。
- 本轮不重跑完整单元测试，也不修改旧hash、旧citation scanner或旧primary_source_notes契约。

## I. 能力使用与验收记录

- 使用：peer-review、verification；沿用已读的using-research-writing、paper-orchestration及writing-core的合规/质量检查原则。用户限定读取与写入范围优先，不重建通用写作计划或其他章节。
- 合规审查：A-F齐备；P0/P1/P2/P3分级明确；R01-R03包含location、problem、intended change、must preserve、must not introduce；所有建议均未应用。
- 科学与质量审查：核对两语、证据等级、Introduction对应、贡献层级、Discussion重复、claim过强/过弱、最终takeaway。没有把正常Conclusion压缩或可选润色升级为P1。
- 产物：本文件及必要的两份.agent记录。未生成新Conclusion版本，未修改任何既有paper文件。
- 剩余事项：用户决定是否执行R01/R02；R03自选。当前结论的科学方向成立；本轮审查不能替代最终投稿的运行元信息、统计溯源或模板准备。
- 最终验证记录：Conclusion双语装配exit 0（1模块、4对段落、0待补标记）；stage_guard为0错误、0警告；指定三文件diff-check exit 0，仅有既有LF/CRLF转换提示。13份论文输入SHA256全部未变。新增计划A-I九节、R01-R03三项齐备，独立空白检查通过并以换行结束。本轮仅新增本计划及更新两份.agent状态，所有正文建议均未执行。

## J. Execution record

日期：2026-09-09。状态：R01、R02已执行；R03未执行。

- R01：conclusion.p02现明确限定于MovieLens seed42完整轨迹，并写明N的排序表现于validation和test已测曝光点持续改善至200k；Y仍只覆盖至96k且维持limited/uneven表述。
- R02：p01删除与最终takeaway重复的context-free解释；p02末句不再复述frozen-test差距，改为低曝光专家优势不能直接代表进一步适配后的共享模型相对表现；p04压缩为两句并保留prediction formulation、cumulative downstream task-sample exposure和candidate evaluation protocol。
- 保留项：四对段落和paragraph ID不变；p03逐字未改；三层M1证据、Y侧能力保留、SASRec与Amazon边界均保留。未新增claim，未把既有claim扩展到冻结范围之外。
- 验证：Conclusion双语装配通过（1模块、4对段落、0待补标记）；整稿双语装配通过（11模块、83对段落、5个既有待补标记）；英文由479词减至415词；stage_guard为0错误、0警告；diff-check exit 0，仅有LF/CRLF提示；风格检查未发现列表、禁用过渡、主观措辞或过程文字，EN/ZH加粗为装配契约。
- 测试：47项中10项仍失败，均属于既有旧契约：library.bib与citation_claim_map哈希、7条citation位置登记、primary_source_notes缺S26。未为追绿修改范围外文件。
- Capability-use audit：使用using-research-writing、paper-orchestration、writing-chapters、writing-core和verification；消费本执行任务、审查计划、Conclusion及必要.agent状态；因用户冻结方向与读取范围，未使用brainstorming、文献、Results、实验输出、provenance或Wiki。产物为修订后的双语Conclusion及执行/状态记录；剩余风险仅为用户尚未确认最终措辞。
