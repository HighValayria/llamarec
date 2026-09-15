# Compression Scientific Judge

## 1. Overall Verdict / 总体裁决

**APPROVE_WITH_CHANGES。唯一推荐：OPTION B，即T-BALANCED + D-BALANCED + P-BALANCED，并执行第5节的明确修正。**

九张主文表、两张Figure及适度正文压缩可以完整承载五个RQ。需要修正的是精简证据的最低内容、结论附近的限定语和解释结构，而不是退回逐种子完整网格。本文继续定位为实证与评估方法研究，不增加新模型或方法创新声明。

冻结主命题：在已评估推荐适配设置内，对推荐能力和模型相对表现的结论取决于监督形式、累计下游任务样本曝光、候选评估协议。贡献层级保持C2主贡献、C4次贡献、C3支撑、C1问题界定。

这是科学可行性裁决，APPROVED表示方案获科学认可，不表示本轮授权修改稿件。本文档不包含替换稿。页数、旧表归档状态和词数沿用输入审计；本轮不独立复验实验结果或编译页面。

## 2. T-Plan Verdict / 表格裁决

**T-BALANCED：change，保留九表方案，补齐证据保留条件。** 下文均使用压缩前表号；未来编号可改变，表的逻辑身份及来源必须可追溯。

| 裁决问题 | 结论 | 必须满足的条件 |
| --- | --- | --- |
| III+IV双panel | 批准 | A为Y-native二分类，B为Y-as-ranker/N-native排序；各自标明task/interface、split、曝光和指标。不得跨panel比较AUC与HR@1数值，也不得把完整监督形式差异写成单一语义因素的因果效应。 |
| VI/VII移出主文 | 批准 | V承担seed42轨迹，VIII承担seed42 validation区间，IX承担三种子偏好与排序摘要。RQ3若保留test bootstrap表述，还必须引用X；V+VIII+IX不是这条区间声明的完整证据链。 |
| XI/XII移出主文 | 批准 | IX保留跨种子的量级和方向；X保留seed42固定模型区间。主文仍能辨认k20较大差距、k50较小且非单调的关系。 |
| IX精简 | 修改后批准 | 必须保留偏好侧三指标及ranking三个协议的双split摘要，不能仅剩HR@1 mean/SD。最低内容见下表。 |
| X精简 | 批准HR@1完整数值CI、NDCG@5/MRR方向与CI状态 | 状态必须按protocol、split和metric逐项列出，明确仅seed42；不能以一句“其余均显著”替代。主文不讨论省略指标的CI宽度或精确界限。 |
| XIII与Figure 2双留 | 批准 | 表给实际曝光计数与双split精确值，图给validation相对趋势；二者有独立作用。 |
| XIV继续CORE_MAIN | 批准 | 这是第二领域方向性证据的直接载体，保留test-only、早期seed42运行点、模型、样本数和现有三指标；不扩大跨域结论。 |

### IX的最低内容

| 信息 | 主文最低保留形式 |
| --- | --- |
| 比较身份 | task/interface或panel标识；Y侧为M1-Y减Y96，ranking侧为N96减M1-N，符号方向显式区分。 |
| 曝光与split | 96k对应任务曝光，M1为expected per-task；validation与frozen test分别报告，不合并求均值。常量可进caption。 |
| 偏好侧 | AUC、F1、Accuracy分别保留三种子delta mean和sample SD，两个split均保留。正/负/零方向计数或带符号范围须让读者看到各seed是否一致。 |
| 排序侧 | k5、k20、k50分别保留HR@1、NDCG@5、MRR的delta mean和sample SD，双split均保留；可用紧凑panel/列组减少重复标签。 |
| 逐种子方向 | 每个相关metric的正/零/负计数或可核验的带符号范围，支撑“每个seed均同向”。正的mean本身不能证明所有seed均为正。 |
| 统计身份 | 训练seed 42/43/44、n=3、等权均值、sample SD、ddof=1；注明描述训练运行变异，不是CI或跨seed显著性。 |
| candidate身份 | k5=PopMatch，k20/k50=random，分别构造且非嵌套；candidate-generation seed42与training seed区分。 |
| 非单调性 | 主文保留seed43 test中k50与k5 HR@1差值对照：+0.00511与+0.00775。可放正文或caption，不能用彼此不配对的range代替。 |

`results.rq3.p01`明确存在seed44 validation Accuracy轻微负差（-0.00089）；把IX压成“所有偏好指标改善”会损坏现有claim。主文可以依赖delta摘要及既有absolute anchor说明表现接近，不必重印VI/VII全部absolute values，但不能只用“差异不显著”证明能力保留，也不能称已证明等价或正迁移。

### X的最低内容

保留k5/k20/k50乘validation/test的六组比较；每组有N96-M1-N的HR@1点估计、95% CI上下界，以及NDCG@5和MRR各自的点估计方向、CI相对零的位置。CI状态至少区分全正、含零、全负和不可用；图例说明含零不等价于模型等价。标题/caption明确是seed42用户级配对bootstrap、固定模型评估样本不确定性，不能与IX三种子均值共用模糊的“±”标签。

本稿对secondary metrics主要保留方向与区间状态，故主文无需强制保留三指标全部numeric CI。若未来正文保留某个NDCG/MRR精确区间、宽度或效应幅度比较，该值必须仍在提交材料中可查；不能一边删数值一边继续讨论其精度。完整旧区间永久保留在归档，有supplement时可提交；没有supplement时主文也须自足。

### Valid/Test裁决

| 表 | 裁决 | 独立科学角色 |
| --- | --- | --- |
| I | BOTH，保留train/valid/test规模 | 数据与任务样本覆盖，不属于模型性能双split重复。 |
| II | NOT_APPLICABLE | 训练曝光计数，不是评估split。 |
| III/IV | SUMMARY_BOTH | validation保留Y-native/bridge轨迹，test保留关键端点与能力对照。 |
| V | BOTH | seed42 validation的48k到96k收窄与test仍有差距必须同时可见。 |
| VIII | VALID_ONLY | 原本只有seed42 validation区间，不能改名为全split统计证据。 |
| IX | SUMMARY_BOTH | 三seed在96k的Y保留和N-M差距，两类split的结论分别可读。 |
| X | BOTH | seed42 k5/k20/k50的validation与test区间，包括RQ3 test gap。 |
| XIII | BOTH | 四点validation比较及冻结test对照，实际曝光数一并可查。 |
| XIV | TEST_ONLY | Amazon只有既有早期test方向性证据，不补造validation。 |

RQ3必须在结果正文邻近位置明说：收窄成立于seed42标准k5 validation轨迹；96k小差距运行点得到复现，frozen test仍保留N优势。`results.rq3.p03`给出的seed42 test HR@1差距在48k为+0.00934、96k为+0.01269，故不能将“validation收窄”概括成两种split都收窄。精确值可留V/X，限定语不能全部后移到Limitations。

## 3. D-Plan Verdict / 图文展示裁决

**D-BALANCED：approve。** Figure 1继续`KEEP_WITH_PROSE_REDUCTION`，Figure 2继续`CORE_MAIN`。

- Figure 1的独立价值是让读者直接看见N在已测曝光点持续改善。Table V还承载test、多指标和M1；Figure 2需容纳更低的SASRec值，不能同样突出N内部增益。因此Figure 1有保留价值，但不是RQ3专家/共享轨迹图，不能引用它证明M1追近。
- Figure 2直接表达“N四点领先”与“SASRec在更多监督下改善、96k到200k差距缩小”同时成立。Table XIII保留精确匹配和test证据，双留合理。
- 两图只展示MovieLens seed42 validation，不能替代test或multiseed证据，也不增加已测点以外的收敛外推。这里只判断其科学角色，视觉质量沿用上轮审计。
- 批准删除Results完整数列、逐seed和逐secondary-metric的反复列举，保留少量量级、关键对照和即时边界。不能在图、表和正文三处同时删除同一个信息。
- 还可少量收紧：VIII已有Y侧完整区间时，正文无需专门反复列出唯一正的F1区间上下界；仍须共同报告AUC/Accuracy区间含零与描述性能力保留，避免选取单一指标暗示正迁移。不得借此更新现有科学结论。

## 4. P-Plan Verdict / 正文裁决

**P-BALANCED：change。** 词数目标作为软范围，优先保留科学职责；不得将达到每节下限设成验收条件。范围沿用输入审计的计数口径，本轮不重新全稿统计。

| 部分 | 原目标 | 裁决 | 执行边界 |
| --- | --- | --- | --- |
| Abstract | 232到220-230 | TOO_AGGRESSIVE，若视为必改要求 | 保持现有摘要；其独立概括属于必要重复，不设缩字指标。 |
| Introduction | 709到560-610 | SAFE | 保留context/problem/gap/design/findings/contributions链。收紧p05-p07；p07与p06可协调，但不机械合并到贡献层级无法辨认。 |
| Related Work | 852到620-690 | SAFE | 保留针对不同前作的实质区别与引用落点；同主题不等于同一已有发现。 |
| Problem | 427到370-405 | SAFE | H/H10、Y/N/M1、RQ1-RQ5都有清晰完整定义。 |
| Methodology | 495到420-455 | SAFE | temporal合法性、response-only loss、QLoRA、1:1和scoring不得变成只有名称。 |
| Experimental Setup | 1005到760-850 | SAFE，有条件 | 先移交真正重复的计数，建议优先靠近范围上端；Table I/II不含的唯一信息不能按“表中已有”删除。 |
| Results | 1546到1400-1460，仅P估计 | SAFE，有条件 | 1546是整节词数，不是单独非数字基线。P的86-146词预算与D只能按实际被删文字去重，1400-1460不是D+P联合后的最终目标。 |
| Discussion | 905到610-700，六到四 | SAFE，修改主题分组 | 保留曝光与统一的主解释、基线次贡献的独立解释；见下文四组结构。 |
| Limitations | 363到315-340 | SAFE，有条件 | 四类scope均保留；若保全边界需要更多词，允许超出340，不再硬削。 |
| Conclusion | 415到225-275，四到三 | SAFE | 采用三段职责和下面的近邻限定规则；无需重述所有细节。 |

### Discussion与Results的分工

批准Results回答finding + minimum evidence + immediate boundary，Discussion回答meaning + implication + reporting consequence。下列Discussion内容仍有独立价值，即使Results已经报告相关现象也不能删除：native/bridge能力应按预测问题解释；同一共享adapter的能力保留取决于对应任务曝光；协议内配对比较与跨协议敏感性是不同推断；下游曝光匹配具有局部比较价值但不代表资源效率；详细域内轨迹和外部方向性检验的证据角色不同。

批准六到四，修正为以下主题，而不是把C4基线解释附在C3候选协议之后、再给Amazon独立同等篇幅：

1. 监督形式与能力解释，承担C1问题界定。
2. 曝光与专家/共享模型关系，合并原Exposure及Specialist/Multitask，承担C2主解释并保留最大论证权重。
3. 候选协议与比较范围，承担C3支撑边界。
4. 曝光对齐下的跨模型基线比较，承担C4次解释；不得混同候选协议敏感性与下游监督比较。

原External Validity两段压为Discussion末尾一个短收束段，与全节综合协调，仍在四个主题之外明确说明两数据集角色，不另设第五标题；完整未验证范围留Limitations。这里的标题顺序不改变贡献重要性，Intro和Conclusion仍显式以C2为主、C4为次。

### Related Work的新颖性边界

| 层级 | 必须保留的定位 | 可以合并的叙述 |
| --- | --- | --- |
| C1 framing | preference/next-item及共同语言接口已有先例；不是首次提出任务区分。 | P5/ITDR在task主题合并介绍，保留与native/bridge解释相关的区别。 |
| C2 primary | 本文具体考察对应目标任务累计监督对齐的专家/共享关系随曝光变化，完整轨迹仍seed42-only。 | P5实例数、ITDR任务删除/子集、OpenOneRec采样/数据域、Penha辅助任务分配和OneReason专家/学生可综合，但不能概括成“前作都没考虑预算或专门化”。 |
| C3 supporting | 候选采样改变评估关系已有先例；本文将其用于限定较高曝光的专家/多任务关系。 | candidate sampling各篇可合并成一个定位段；保留原引用及非孤立candidate-size边界。 |
| C4 secondary | TALLRec已有选定样本预算比较；sequence scaling已有数据量/重复训练研究；本文是四点累计下游消费比较，不是首次预算感知比较。 | SASRec、reproducibility和TALLRec/scaling可缩写为紧凑证据链，保留selected-example与cumulative consumption的口径区别。 |

### Conclusion三段裁决

批准P1说明研究对象与问题；P2概括三组发现，依次以C2专家/共享关系、C4基线响应和C3协议边界为重点，C1能力界定可在P1简述；P3给出三条件takeaway。五RQ需在整篇保留，不要求Conclusion再逐项复述五RQ。

| 限定 | Conclusion中是否必须出现 |
| --- | --- |
| full trajectory seed42-only | 必须保留短限定，邻接曝光收窄声明；无需列全部运行点或重复一整段限制。 |
| multiseed只在96k | 必须保留，因为其增强C2证据；可只写三种子96k运行点，不列43/44每个编号。 |
| validation收窄与test仍有N差距 | 必须同时出现，防止压成无条件专家/共享等价。 |
| Y侧表现保留 | 必须在C2概括中出现，否则统一建模退化成只有ranking比较。 |
| protocol-conditioned关系 | 必须出现；不要求再列k20/k50所有大小对照及构造细节，但不暗示candidate count的因果效应。 |
| SASRec继续改善 | 必须与N领先共同出现，且保留approximately matched downstream exposure口径。 |
| Amazon directional-only | 若Conclusion提Amazon或“两数据集支持”，则必须就地加早期ranking方向限定；也可完全省略Conclusion中的Amazon，外部证据及完整边界仍在Results/Discussion/Limitations。 |
| bootstrap算法、SD定义、resume前提及未验证清单 | 可仅在Methods/Setup和Limitations完整保留；Conclusion不得写依赖更强推断的句子。 |

可进一步安全精简的是Conclusion的详细seed编号、各候选协议逐项方向、重复数据集介绍，以及Discussion首尾两次完整三条件枚举。摘要和关键限定的必要重复不计入这一空间，不另行提高省页承诺。

## 5. Required Corrections / 必须修正

1. **RC01：锁定IX/X最低证据并补齐RQ3对X的依赖。** IX保留Y侧三指标、ranking三指标、双split、mean/SD与逐种子方向；X保留seed42逐protocol/split的HR数值CI及其他指标区间状态。不能从正均值推断所有seed同向。
2. **RC02：限定语允许必要重复。** 唯一信息原则只约束完整定义与详细推导；RQ3 validation/test张力、非等价、完整formulation、protocol整体和Amazon范围须在相关强结论附近可见。旧repetition矩阵的U及MERGE标记不构成逐项删除命令。
3. **RC03：修正解释分组并保住新颖性层级。** Discussion采用能力、曝光/统一、协议、基线四主题，Amazon作为短收束；Intro贡献表达不能被findings preview吞没，Related Work保留四类前作边界。
4. **RC04：取消硬词数配额和未经验证的收益相加。** Abstract不安排缩字；Results的D/P按实际源段落删减去重，同一句含数字和解释时只计一次。删除Setup计数前逐项指定接收处：例如SASRec实际四点计数由XIII承载，不能笼统声称都在II；dataset物品/交互规模、rating与metadata universe区别、94%覆盖解释等若无接收处就保留。允许为完整边界超过目标词数。
5. **RC05：先保证可恢复、再移交证据。** 后续执行前建立含35份双语Markdown的不可变内容快照及manifest，旧hash contract保留、新版另建，不覆盖历史合同；旧表及完整区间沿用永久归档。先完成主文精简摘要的证据覆盖，才移除VI/VII/XI/XII主文引用，并保存段落合并和表号映射。本轮不创建这些执行产物。

## 6. Approved Compression Actions / 允许执行项

以下为`APPROVED_COMPRESSION_ACTIONS`，均须满足RC01-RC05，并在用户另行启动执行后实施。

| 编号 | 具体动作 |
| --- | --- |
| A01 | II压缩重复标签或常量；保留run、total exposure、Y/N expected per-task exposure，effective batch与步数关系在正文/caption可查。 |
| A02 | III/IV合为native binary与bridge ranking双panel，validation轨迹加test关键端点分别保留。 |
| A03 | 完成IX的双任务摘要后，将VI/VII完整逐seed absolute grid移出主文；原表保留。 |
| A04 | 完成IX/X的跨协议摘要与seed43非单调对照后，将XI/XII逐seed逐协议网格移出主文；原表保留。 |
| A05 | IX用panel/列组精简重复行标签；X以HR完整CI及NDCG/MRR方向与区间状态呈现，不重算CI。 |
| A06 | I、V、VIII、XIII、XIV继续主文；两图继续主文，Results删重复完整数列，只留必要量级和对照。 |
| A07 | Intro p05-p07去重，保留设计、发现、贡献三个角色；RW聚合逐篇介绍且保留引用对应的实质区别。 |
| A08 | Problem完整定义一次；Method保留构造与计算；Setup只删已有明确表格/段落接收的重复说明。 |
| A09 | Results删除冗长导航和提前展开的普遍意义解释；保留RQ3/RQ4/RQ5及Amazon的finding、最低证据与即时边界。 |
| A10 | Discussion按修正后的四主题整合；External Validity两段合为短收束，不能删尽跨域解释。 |
| A11 | Limitations保留统计、评估、外部效度、资源四类，压缩同类边界的重复句式。 |
| A12 | Conclusion四段压为三段；EN/ZH同时修改，原段落ID的合并关系明确记录；摘要本轮执行范围仍保持原稿。 |

主文九表目标维持：I、compact II、merged III/IV、V、VIII、compact IX、compact X、XIII、XIV。无supplement时，删去的是raw展开而非主文所需证据；私人归档不能替代读者需要的主文摘要。

## 7. DO_NOT_COMPRESS / 禁止压掉的内容

1. 三条件主命题、五RQ定义、C2>C4>C3>C1层级及经验研究定位；不得添加first/new-model等更强创新表述。
2. H/H10、严格早于target的history、同timestamp bucket处理、Y/N各自合法目标与留出规则；N不是next liked item。
3. Y评分标签阈值、低评分事件参与样本构造、N distractor不等于dislike、M1共享adapter保留双接口及完整formulation比较边界。
4. response-only loss、M1 1:1、QLoRA关键设置、Y/N响应似然及多token评分规则；不能只留下实现名称。
5. 曝光包含重复消费且不等于unique interactions；M1 total/expected per-task及正确resume skipping前提，缺少per-example trace的边界。
6. I的数据任务/split规模；II必要曝光身份；III/IV两个任务panel及指标口径，不能跨量纲比较。
7. V中的seed42 48k/96k专家和共享模型双split对照，以及N到200k的已测响应。Y有限/不均匀增益不能缩成已证实饱和。
8. IX的binary三指标与ranking三个协议双split mean/sample SD、逐seed方向；X的HR numeric CI和另外两指标各自CI状态。
9. RQ3的validation收窄、96k小差距复现、frozen-test retained N gap及Y-side preservation；不写unqualified parity或已证明equivalence。
10. full trajectory seed42-only与three-seed 96k operating point的区别；training seed与candidate-generation seed的区别。
11. paired user bootstrap的配对与用户分组、95%区间含义和差值方向；固定模型评估样本不确定性不等于跨训练seed变异。
12. n=3、ddof=1、SD不是CI；零跨区间不证明等价，未设equivalence margin、未做全比较multiplicity-adjusted inference，不新增跨seed显著性判断。
13. validation用于决策、frozen test用于决策后held-out报告；VIII VALID_ONLY、X/IX必要双split不能互相冒充。
14. k5/k20/k50分别构造、非嵌套，数量/组成/采样/难度共同变化；k50 gap不总大于k5及主文可核查反例；不写candidate-size因果或单调性结论。
15. PopMatch使用全语料流行度的retrospective性质、残余流行度影响，以及sampled evaluation不等于full-catalog评价。
16. XIII四个近似匹配的实际下游消费量、N四点领先与SASRec继续改善的并存；不能删后半句扩大LLM优势。
17. XIV的test-only、earlier seed42、ranking-side支持；Amazon不支持完整曝光曲线、96k多种子、hard-candidate或native preference跨域复现。
18. 下游task-sample matching不匹配pretraining、tokens、updates、FLOPs、wall-clock、serving或部署成本；现有实现与训练范围限定不能删。
19. Y至96k、N至200k之外的行为/收敛未知，exposure同时改变覆盖与优化历程，不能增加未验证机制。
20. 原表、旧正文内容快照、历史hash contract与来源映射；EN/ZH必须同步且claim范围/强度一致。

## 8. Expected Scientific Effect / 预期科学效果

| RQ | 修正后主文证据 | 可保留的结论及边界 |
| --- | --- | --- |
| RQ1 | merged III/IV与任务/评分定义 | Y-native与bridge/N-native能力有别；完整监督形式对照，不是单一语义因素识别。 |
| RQ2 | merged III/IV、V、Figure 1及曝光定义 | Y被测增益有限/不均匀，N在已测点持续改善；指标响应不跨量纲比较，完整轨迹seed42-only。 |
| RQ3 | V、VIII、compact IX；test区间由compact X承载 | validation随曝光收窄，96k三seed小差距但test偏N，Y能力保持；非等价、非跨seed正迁移结论。 |
| RQ4 | compact IX/X及正文非单调对照 | 三seed协议相关的剩余差距；bootstrap仅seed42，协议共同变化不识别candidate-size因果。 |
| RQ5 | XIII、Figure 2及SASRec设置 | 四个近似下游曝光匹配点N领先且SASRec改善，96k到200k差距缩小；不涉及总资源效率。 |

XIV提供独立但有限的跨域方向支撑，不是额外完整RQ曲线。修正后读者应更容易区分主贡献、次贡献和支撑边界；损失的是原始网格的主文展开与重复解释，结论强度不变。论文仍保留相反或限制性证据，不以摘要均值掩盖例外。

## 9. Stop Condition After Recompile / 后续停止条件

**接受8.7-10.4页作为既有方案的暂定规划范围；若后续真实英文编译为9-10页且以下条件满足，建议停止继续压缩。** 该范围不是实测预测、统计区间或本次保证，不据此追求更少页数，也不机械相加T/D/P估计。

- 五RQ的证据仍可在主文独立核查，特别是IX偏好侧、RQ3双split张力、X统计身份和RQ4非单调边界。
- 图表与caption在正常阅读尺寸清晰，浮动体顺序和引用正确；不以缩小字号抵消内容密度问题。
- EN/ZH的claim范围一致、引用仍支持对应表述；Abstract与压缩后的正文不存在结论冲突。
- RC01-RC05与DO_NOT_COMPRESS逐项通过，历史内容可恢复，所有数字与区间只是重排已有证据。
- 已知venue要求允许该篇幅；若之后获知新的硬页限，重新裁决范围，不自动进入P-AGGRESSIVE。

### 本轮任务与验证记录

- 任务类型：科学裁决。输入为用户附件、三份judge packet，必要时补读三份完整audit，以及定点16个段落。只因仓库流程维护`.agent`状态及`paper/plan/progress.md`，不拓展科学阅读范围。
- 定点来源：`results.rq3.p01-p03`、`results.rq4.p02`、`methods.datasets.p01-p02`、`methods.exposure.p03`、`rw.unified.p01-p02`、`rw.evaluation.p02`、四个`limitations.*.p01`和`conclusion.p02-p03`。均从对应作者源读取双语内容，不重复全稿审查。
- 复用本会话已载入的using-research-writing、paper-orchestration、peer-review、verification流程；不需要重新检索文献或调用PDF编译/视觉检查技能。
- 写入范围：本裁决文件与必要进度/状态记录。既有六份audit/packet及定点作者源均保留；不修改科学claims、表、图或构建。
- 规格审查：九节要求、A-F总体问题、七个表格问题、九部分目标、valid/test、两图、Discussion/Conclusion、文献定位、允许/禁止项与停止条件均已覆盖。
- 科学审查：修正RQ3对X的依赖，锁定IX/X统计与方向信息，保护近邻限定，拆开C3/C4解释，取消硬词数配额并防止D/P重复计数。
- 机械验证：九节齐全、必需字段零缺失、12项允许动作可定位；六份既有审计/裁决包及八份定点作者源文件共14个输入SHA256全部未变。stage_guard为0错误0警告，限定diff-check及新文件格式检查通过。上述核验不扩展为全仓库或完整实验数据复审。
