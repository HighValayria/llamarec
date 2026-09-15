# Abstract 科学审查与最小修改计划

日期：2026-09-09。模式：REVIEW ONLY / PLAN ONLY。对象：[当前双语Abstract](F:/Projects/llamarec/paper/modules/10_abstract.md)。本文仅记录审查与修改建议，不生成完整替代稿，不应用正文修改。

## A. Overall verdict

**MINOR_REVISE**。

只读当前Abstract，读者能够辨认研究问题、以曝光为条件的专家/共享模型关系、候选协议边界、四点SASRec比较及最终科学含义。实证主线与已修订Conclusion一致；没有必要重新组织论文故事或重写摘要。

| 等级 | 数量 | 判定 |
| --- | --- | --- |
| P0 — Scientific contradiction | 0 | 未发现与冻结正文相反的结果 |
| P1 — Claim strength / scope problem | 0 | 未发现三seed全轨迹、等价、正迁移、候选数量因果、普遍基线优势或Amazon完整复现的实质性误写 |
| P2 — Narrative / information density / emphasis problem | 2 | R01：中文首句引入英文没有的研究惯例概括；R02：中文设计句与核心结果句合并过密 |
| P3 — Optional polish | 2 | R03：将N/M1收窄句的seed42承接写明；R04：补明SASRec在200k收窄的参照为96k |

R01不判为科学冲突或P1：中文没有说前人都忽略这些条件，“往往在固定设置下比较”本身也不能据此判假，且原起草任务允许从固定运行点切入。问题是双语开头承担了不同的陈述，中文又把这层概括接成“因此”的理由。R02是阅读负担，不是遗漏证据。两项P3在当前上下文中已有可恢复的指代，不作为阻碍使用摘要的科学问题。

## B. Current Abstract story

现稿讲的是一个具体适配设置中的实证研究：用Llama-3.2-3B-Instruct与QLoRA，在MovieLens-1M上比较Y、N及共享M1，并追踪任务样本曝光、候选协议及与SASRec的关系。Y/N呈现不同被测能力和曝光响应；N的排序改善持续到已测200k点。主发现是，增加每任务监督后，标准k5验证上的N/M1差距从48k到96k明显接近，三训练seed在96k复现小差距，同时测试仍偏向N，M1保留Y侧能力。

这一接近关系随候选协议改变。N在四个近似曝光匹配点领先被评估SASRec，但SASRec也随监督改善，较高曝光下差距收窄。Amazon较早seed42点只补充关键排序方向。全文由此支持结合预测形式、累计下游监督和候选协议解释能力与模型优劣，没有声称提出新模型、基准或评价标准。

| 只读Abstract应回答的问题 | 当前可读到的答案 | 判断 |
| --- | --- | --- |
| 研究什么问题 | E1提出监督内容、消耗量和候选评估条件如何影响推荐结论 | 清楚 |
| 最主要的实证贡献 | E5-E7把任务响应与专家/共享关系的变化连起来 | 清楚，尚可改善中文句子组织 |
| 哪些结论依赖曝光 | Y/N响应、N/M1接近、N/SASRec比较 | 清楚 |
| 哪些结论依赖候选协议 | E8承接标准k5小差距，说明专家/多任务差距随协议改变 | 清楚 |
| SASRec比较的条件 | 被评估基线、四个下游任务样本曝光近似匹配点 | 清楚 |
| 最终科学含义 | 能力和相对表现须连同三个条件理解 | 清楚 |

## C. Sentence-level audit

英文按句末标点划分为E1-E11；中文为Z1-Z9。全部同属abstract.p01，英文位于文件第12行，中文位于第16行。E2/E3合并为Z2，E6/E7合并为Z5。这里的句号是审查定位，不改变paragraph ID。

证据使用：[Conclusion](F:/Projects/llamarec/paper/modules/09_conclusion.md)、[Contributions](F:/Projects/llamarec/paper/modules/00_contributions.md)、[Introduction](F:/Projects/llamarec/paper/modules/01_introduction.md)及本轮任务给定的冻结事实。未因存在词语压缩而重新读取实验材料。

| Sentence / Claim | Function | Evidence alignment | Verdict | Priority |
| --- | --- | --- | --- | --- |
| E1 / Z1：问题与三个条件 | Problem | intro.p03-p07；conclusion.p01/p04 | 英文以条件依赖切入，具体且没有“前人都忽略”的主张。中文额外概括“实验往往在固定设置下比较”，并由“因此”引出运行点限制；两语问题方向相同，但陈述内容不完全对应 | P2 / R01 |
| E2 / Z2前半：Llama、QLoRA、主数据集与Amazon | Design identity | 模型/数据集精确身份由本轮任务明确给定；intro.p05和conclusion.p03支持主次数据集角色 | 身份正确，Amazon明确是directional ranking-side check。不能声称本轮额外核验了Methods；此处无新增模型贡献 | 无；Z2密度见R02 |
| E3 / Z2后半：Y/N/M1、曝光、协议、SASRec | Design | intro.p05；conclusion.p01；contributions.p02/p04 | 实验身份完整。英文35词虽有多个动作，但结构可辨；中文与E2合成一条204字符长句，模型/数据/任务/比较共用一个句架 | P2 / R02 |
| E4 / Z3：完整Y/N形式产生不同被测能力结构 | Framing finding | contributions.p01；intro.p02/p06；conclusion.p02前两句 | 准确。“complete”和“measured”限制比较对象，没有语义单因素归因、独立潜在能力或跨指标大小判断；无需补机制或指标 | 无 |
| E5 / Z4：Y到96k有限/不均匀，N改善至200k | Exposure response | conclusion.p02第3句；intro.p06；本轮任务对两split明确约束 | MovieLens seed42、validation/test、已测点和200k均保留。N正向改善明确；没有Y饱和、N未收敛或未来趋势推断 | 无 |
| E6 / Z5前半：标准k5验证48k到96k收窄 | Primary trajectory | contributions.p02；conclusion.p02第3/4句 | 方向、任务曝光和validation限定正确。seed42从紧邻的E5/Z4承接，尚未独立绑定到本句；顺读时可恢复，建议可选补明 | P3 / R03 |
| E7 / Z5后半：三seed96k复现、测试N略强、M1保留Y能力 | Primary replication and residual gap | contributions.p02；conclusion.p02第5/6句；intro.p06 | 四层证据和比较身份都在；英文明确复现对象是“96k small-gap regime”，没有把三seed扩展到全轨迹。英文25词用分号和从句可辨，中文却与E6合成同一句，阅读负担较大 | P2 / R02（同一问题，不重复计数） |
| E8 / Z6：不同候选协议改变剩余专家/多任务差距 | Supporting boundary | contributions.p03；conclusion.p03前三句；intro.p06 | 紧接标准k5结果，足以说明小差距不跨协议恒定。“materially change”不是泛泛说结果波动；未归因为候选数量/难度。无需强塞k20/k50及构造细节 | 无 |
| E9 / Z7：四个匹配点N领先SASRec，SASRec改善，200k收窄 | Secondary finding | contributions.p04；conclusion.p03第5句；intro.p06 | 四点领先与基线改善都明确，比较限定于evaluated baseline和近似下游任务样本曝光。没有计算、预训练公平或普遍优越性声明。200k的参照点被省略，可选恢复96k | P3 / R04 |
| E10 / Z8：Amazon较早seed42点也出现关键排序方向 | External support | conclusion.p03末句；intro.p05/p06；本轮任务 | “directions also appear”与“也呈现相同的关键排序方向”相符，没有说全套研究在Amazon复现。早期运行点和seed范围明确 | 无 |
| E11 / Z9：能力与相对表现依赖三个条件 | Synthesis | intro.p07；conclusion.p04 | “These results”承接已命名研究设置；结论有实证意义，不是再次列实验清单。“conditional on”和“应结合”分别表述结果依赖与解释含义，科学力度协调 | 无 |

未发现first、novel framework、new benchmark、新评价方法、未经核验机制、统计显著性、等价性、非劣性或收敛主张。没有为了“更严谨”而增加免责声明的必要。

## D. Contribution hierarchy audit

贡献编号与finding编号不同。此处只按用户冻结的Primary / Secondary / Supporting / Framing角色判断，不重新排序论文贡献。

| 角色 | 对应句子与篇幅 | 当前强调 | 判断 |
| --- | --- | --- | --- |
| Primary：曝光条件下专家/共享关系 | E5-E7共67词；其中直接N/M1证据E6/E7共41词 | Y/N响应为过渡，随后连续给出轨迹接近、96k复现、测试剩余优势和Y保留 | 主干正确 |
| Secondary：曝光感知的N/SASRec比较 | E9共25词 | 明确四点领先与基线自身改善 | 充分，未压过主线 |
| Supporting：协议条件 | E8共9词 | 为前面的k5接近关系限定适用范围 | 简短但承担了清楚功能 |
| Framing：监督形式 | E4共11词，E3另作任务身份定义 | 不同完整预测问题界定被测能力 | 没有占去半篇或包装成最大创新 |
| External：Amazon方向支持 | E2交代角色，E10共12词报告方向 | 支撑范围明确 | 篇幅可接受，未挤掉主发现 |

E2/E3共59词属于理解结果所需的设计，不应全部算成监督形式贡献。协议先于SASRec是自然的论证承接，不代表支持性贡献被升级为主贡献。无需为满足字数目标删除主结果，也无需另加一句宣称“我们的首要贡献是”。

## E. Missing / overcompressed finding audit

| 检查项 | 是否保留 | 压缩是否造成实质损失 |
| --- | --- | --- |
| Supervision | E3定义、E4完整形式与被测能力 | 没有；不必再次解释like与next-item的全部接口 |
| Y/N exposure | E5有不同响应、96k/200k、MovieLens seed42、两split已测点 | 没有；N正向方向足够明确 |
| N/M1 trajectory | E6有validation、k5、48k到96k每任务 | 没有；seed42局部承接可通过R03更直接 |
| Three-seed replication | E7明确96k运行点，留出集仍偏N | 没有；复现对象不是轨迹 |
| Y-side preservation | E7明示comparable Y-side preference capability | 没有；不是正迁移 |
| Protocol | E8明确改变剩余N/M1差距 | 没有；上一句小差距与下一句协议变化已有具体逻辑，不强求展开k20/k50 |
| SASRec | E9四点领先、基线改善、200k收窄 | 没有；参照96k可选补明，不改为“某些点有差异” |
| Amazon | E2和E10限定方向、早期点和seed42 | 没有；无需在摘要列出三个排序对手 |
| Takeaway | E11将结果归结为三个条件下的解释 | 没有；并非新规范或单纯实验清单 |

“信息在一句里挤得太多”与“证据被删掉”应区分。当前英文E7虽然含三项相关观察，但共享同一个96k运行点，25词且有分号分层，不要求再拆。中文Z5将E6与E7合并，单句同时承担轨迹、运行点复现、测试剩余优势、Y保留四项关系，属于值得调整的结构问题。

Protocol没有精写k20更大，属于本任务明确允许的摘要压缩。现句含“remaining specialist-multitask gap”，可由前文识别对象，不能等同于弱化为没有方向的“results varied”。若后续需要额外压缩，也不应删掉N到200k改善或SASRec四点领先。

## F. Redundancy audit

英文按上一轮相同正则计词规则为232词，按空白分词为230词，两者仅是计词方式不同，均处于本任务长度区间。当前为英文11句、中文9句，各一个自然段。无需强压到200词。

| 位置 | 重复或密度性质 | 裁决 |
| --- | --- | --- |
| E1与E11 | 都出现监督、曝光、候选三个条件；E1提出问题，E11由具体结果给出判断 | 有轻度主题镜像，但功能不同且中间有充分结果，不构成单独P2。无需为去重复删掉三个条件 |
| E2与E10的Amazon | 前者交代设计角色，后者限定并报告方向支持 | 合理分工，可保留 |
| E3与E9的SASRec匹配 | 前者说明比较设计，后者报告四点优势和差距变化 | 有身份重复但有助单独理解结果，不建议牺牲曝光口径 |
| E3各实验动作 | 35词介绍三任务、曝光、候选与基线 | 信息密集但英文可读；不要求全句重写 |
| Z2 | 合并英文两个设计句，含204个字符（含模型名、英文及标点） | R02优先拆成两个句子，维持一个中文自然段 |
| Z5 | 合并英文两个核心结果句，含102个字符及四层结果 | R02在轨迹与运行点复现之间拆句；保留四层证据 |
| E7内部 | 96k复现、测试剩余优势、Y保留 | 相关信息并列且不重复，不能按普通冗余删除 |

建议的小修以双语对齐和中文句子分工为目标，英文现有232词可以保持。210-225词不是验收硬指标。

## G. Revision plan

所有条目状态为 **PROPOSED / NOT APPLIED**。本轮未修改Abstract或其他正文。R01、R02建议执行；R03、R04可选，不能据此扩大到整篇润色。

### R01 / P2：让中文开头与英文提出同一个问题

- Location：[abstract.p01中文Z1](F:/Projects/llamarec/paper/modules/10_abstract.md:16)，对应英文E1。
- Problem：英文说推荐结论可能依赖三个条件；中文先说实验“往往”采用固定设置，再由“因此”推出运行点限制。中文多出对研究惯例的概括，二者不是同一层陈述。
- Intended change：保留英文问题句；中文改为直接描述推荐结论随监督内容、累计下游监督和候选评估条件而变化的可能性。无需增加文献缺口或方法新颖性，也无需把首末句全部改写。
- Must preserve：问题的三个具体条件、条件性语气、推荐能力与模型比较语境。
- Must not introduce：前人普遍忽略、首次系统研究、已识别独立因果、所有设置必然变化。
- Acceptance：两语开头陈述同一个经验问题；中文不再承担英文没有的领域频率概括。保持一对自然段。

### R02 / P2：拆开中文设计句与核心结果句的多重任务

- Location：[abstract.p01中文Z2与Z5](F:/Projects/llamarec/paper/modules/10_abstract.md:16)，分别对应英文E2/E3与E6/E7。
- Problem：Z2把模型、适配技术、数据集、三任务、曝光、候选和基线比较压在同一句；Z5把seed42轨迹与三seed运行点复现、test优势、Y保留也压在一句。困难来自句子组织，而非需要删除事实。
- Intended change：Z2按现有英文分工划为“模型/数据集身份”和“任务/比较设计”两句；Z5在标准k5验证轨迹描述之后断句，再以96k运行点承接复现、测试优势和Y侧保留。仍保留一个中文自然段。英文现有句界可保留。
- Must preserve：Llama-3.2-3B-Instruct、QLoRA、MovieLens-1M、Amazon角色、Y/N/M1身份、每任务曝光、候选协议和近似匹配基线；N/M1四层证据与全部seed/split条件。
- Must not introduce：第五种实验设计、三seed全轨迹、M1等价/正迁移、把Y/N framing提升为主贡献、以少字数为由删除主发现。
- Acceptance：一句不再同时跨越轨迹与复现等四层结果；主贡献更容易按顺序读出；一对paragraph及证据ID不变。

### R03 / P3，可选：让N/M1收窄句直接承接seed42

- Location：[英文E6](F:/Projects/llamarec/paper/modules/10_abstract.md:12)与中文Z5的轨迹分句。
- Problem：当前seed42限定在E5/Z4；E6/Z5依靠相邻语境承接。E7又明确只复现96k，顺读并未声称三seed轨迹，但快速扫读时局部指代还可以更直接。
- Intended change：仅在收窄句以“同一seed42轨迹”这一类短限定连接前句；无需新增完整轨迹免责声明或另列43/44。
- Must preserve：MovieLens、standard-k5 validation、48k到96k每任务、接下来的三seed仅指96k复现。
- Must not introduce：三seed均有48k到96k收窄、test差距也随曝光收窄、额外训练轨迹。
- Acceptance：即使单读收窄句，也能辨认seed42范围；两语同等明确。未执行此可选项本身不等于存在实质性越界。

### R04 / P3，可选：补明SASRec差距收窄的参照

- Location：[英文E9](F:/Projects/llamarec/paper/modules/10_abstract.md:12)与中文Z7。
- Problem：“gap narrows at 200k / 200k时差距缩小”没有逐字给出参照。正文已明确是相对96k；现句并未说四点差距单调收窄，当前概括可成立，但参照可以更具体。
- Intended change：在该短语末补明相对96k，不列完整曲线，不引入新数值。SASRec“improves strongly”的额外监督语境已可由曝光点恢复，无需再扩成方法句。
- Must preserve：N-trained LlamaRec、evaluated SASRec、四个近似匹配的downstream task-sample exposure点、基线自身改善。
- Must not introduce：整个区间单调收窄、最终追平/反超、全部曝光点的普遍LLM优势、算力或样本效率优越性。
- Acceptance：两语有同一参照点；现有四点优势不被弱化。

## H. Bilingual scope and strength audit

| EN / ZH对应 | 数据集、seed、split、曝光及对象 | 强度判断 |
| --- | --- | --- |
| E1 / Z1 | 问题范围同属LLM推荐比较，但中文多研究惯例陈述 | R01处理陈述对齐；不判为实验结果错误 |
| E2-E3 / Z2 | 模型、QLoRA、MovieLens主数据集、Amazon方向支持、Y/N/M1及SASRec身份一致 | 准确；R02改善句子组织 |
| E4 / Z3 | “complete / measured”与“完整 / 被测”一致 | 无潜在能力或语义因果升级 |
| E5 / Z4 | MovieLens seed42、Y96k、N200k、validation/test已测点一致 | 中文“持续改善”与英文“improves across measured…points”一致，没有未来外推 |
| E6-E7 / Z5 | k5验证收窄与96k三seed复现不同层级；留出测试N优势、M1的Y表现都在 | “明显”对应substantially，“小幅”对应modest；comparable不译成等价 |
| E8 / Z6 | 同为候选协议对剩余专家/多任务差距的影响 | materially与明显协调，没有数量或难度单因素归因 |
| E9 / Z7 | 四个近似匹配下游任务样本曝光点、同一基线、200k差距变化 | “领先”对应leads；中文“随监督增加”由英文曝光比较语境支持；参照点两语同样省略 |
| E10 / Z8 | Amazon、较早seed42运行点、关键排序方向一致 | “相同方向”不等于相同指标值或完整实验复现 |
| E11 / Z9 | 三个条件和能力/相对表现对象一致 | 英文给经验依赖结论，中文给解释含义；不是两个不同强度的统计结论 |

总体没有统计显著性、等价、收敛或正迁移措辞。末句未逐字重述“in the evaluated setting”，但“These results”及前文模型、数据集身份足以限定本研究结论，不据此推定为普遍定律。无需将正常Abstract压缩升级为P1。

## I. Reading scope and verification

本轮完整读取且仅以四份正文作为论文内容输入：10_abstract、09_conclusion、00_contributions、01_introduction。精确模型与数据集身份亦由本轮任务明确给定。没有发现必须追加读取冻结证据文件或原始材料才能核实的具体事实，因此未读取可选的story freeze、claim matrix或source_of_truth，也未读取用户排除的其他材料。

审查前四份正文已记录SHA256；Abstract基线为：

`4E235847B16C965032C51CEC74E5F16BA205D44C8AAC865CB07C506107ADEB5A`

- Abstract双语只读装配已通过：1个模块、1对段落、0个待补标记。
- 文本核对：英文232词，11句；中文9句；一对自然段。词数及句界仅用于信息密度审查，不是新实验统计。
- 本轮仅运行用户要求的单章装配、任务状态和格式检查，不运行整稿检查或完整测试。
- 最终验证记录：Abstract双语装配exit 0（1模块、1对段落、0待补标记）；stage_guard为0错误、0警告；指定三文件diff-check exit 0，仅有LF/CRLF转换提示。四份正文SHA256全部与审查开始时一致，Abstract及其对照正文未改动。新增计划A-J十节、R01-R04四项齐备，无行尾空白且以换行结束。

## J. Capability-use audit

- 使用peer-review完成逐句审查与轻重分级，沿用已读verification及写作流程原则验证实际产物；用户规定的窄范围优先，不扩大审查到其他章节。
- 产物：本审查计划与两份必要任务状态。所有R项为建议；未修改Abstract或其他正文，未输出整篇新版摘要。
- 已完成范围内的规范与质量核对：A-G齐备，双语对应、贡献层级、过强/过弱、长句密度、首尾分工、实验边界均有明确裁决。
- 后续仅需用户决定是否执行R01/R02及两项可选润色；当前审查不要求新增实验或文献。

## K. Execution record

日期：2026-09-09。状态：R01、R02已执行；R03、R04未执行。

- R01：中文首句已删除英文没有的研究惯例概括，改为直接说明经验结论可能取决于监督内容、下游监督量和候选评估方式，与英文提出同一科学问题。
- R02：中文设计部分拆为模型/数据集角色与任务/比较设计两句；N/M1部分拆为标准k5验证轨迹、96k三seed运行点及测试优势、M1的Y侧能力保留三步。仍为一个中文自然段，所有finding均保留。
- 未执行项：未补“同一seed42轨迹”等R03措辞，未补“相对96k”等R04参照；英文逐字未改，仍为232词。
- 质量检查：中文由9句调整为12句，最长句由原先204个字符降至108个字符。未发现禁用强结论、引用或正文过程文字；贡献层级和全部seed/split/曝光/协议边界保持不变。
- 验证：Abstract双语装配通过（1模块、1对段落、0待补标记）；整稿双语装配通过（11模块、84对段落、3个既有待补标记）；stage_guard为0错误、0警告；diff-check exit 0，仅有LF/CRLF提示。
- 测试：47项中10项仍失败，均为已知旧契约：2项旧hash、7项citation-location、1项primary_source_notes。未修改范围外文件追绿。
