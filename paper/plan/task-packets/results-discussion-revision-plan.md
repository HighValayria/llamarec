# Results / Discussion / Limitations 统一修改计划

原审查日期：2026-09-08；执行验收日期：2026-09-09。当前状态：**R01-R09已按明确授权执行，待用户审阅；一项旧保护测试与新授权范围冲突，未修改测试或旧基线。**

对应[完整审查报告](F:/Projects/llamarec/paper/evidence/results_discussion_audit.md)。本文保留原修改方案，并兼作执行与验收记录。最新明确授权为：严格执行R01-R09；Intro p06仅为R01做一句最小双语同步；允许R04/R09状态同步；不得额外扩写、重构或进入Conclusion/Abstract。这一授权覆盖上一轮“只记录计划”的限制。第一、三、六节保留原审查约定、方案与当时记录；其中“未执行”“后续授权”等历史措辞不代表当前状态，当前结果见第二、七节。

## 一、原审查任务约定（历史）

- 工作类型：跨章节证据与表达一致性审查，不是论文改写。
- 当前产出：审查报告、本文；另维护两份.agent任务管理记录。
- 本轮禁止改动：全部既有paper文件，包括EN/ZH作者源、控制文件、CSV、caption、参考文献、图、旧build及既有计划。
- 禁止动作：训练、推理、新实验、新bootstrap/等价检验、新统计分析、文献搜索、Wiki访问、prepare_assets.py、整稿生成、摘要/结论写作、模板适配。
- 研究定位：已有设计下的经验研究，不新增模型、方法、机制解释、RQ或新颖性判断。
- 保留层级：贡献C2为主、C4为次、C3为支撑、C1为界定；不与实验finding编号混淆。
- 依据：七份指定控制文件、完整33对Results/Discussion/Limitations段落、00/01的11对只读参考段落、已有Methods说明及图表数据。
- 失败条件：擅自改稿；混淆验证/测试或两类seed；把96k复现写成全轨迹复现；将小差距升级为等价/正迁移；更改原始数值；将协议差异解释为数量因果。

## 二、优先次序与实施门槛

| 顺序 | 编号 | 优先级 | 目的 | 是否需要新实验 | 当前状态 |
| --- | --- | --- | --- | --- | --- |
| 1 | R01 | P1 | Y收益结论限定到支持它的指标/划分 | 否 | 已执行 |
| 2 | R02 | P1 | 正式四点与历史非匹配比较分离 | 否 | 已执行 |
| 3 | R03 | P1 | RQ2桥接指标引用可直接追溯 | 否 | 已执行 |
| 4 | R04 | P1 | 旧novelty map实证状态与MS96一致 | 否 | 已执行，已获明确授权 |
| 5 | R06 | P2 | 减少结果/解释重叠及重复数字 | 否 | 已执行 |
| 6 | R07 | P2 | Limitations按四类边界组织 | 否 | 已执行 |
| 7 | R08 | P2 | 效率术语及中英文强度一致 | 否 | 已执行 |
| 8 | R05 | P2 | Discussion最后形成一次整体综合 | 否 | 已执行 |
| 9 | R09 | P2 | 提纲状态、中文表头整理 | 否 | 已执行，已获明确授权 |

P1/P2是编辑优先级，不是实验优先级。没有P0科学结果失效问题。应先完成范围修正，再压缩重复，最后写综合段，避免为尚未明确的表述再增加一段总结。

用户现已明确授权全部R01-R09及R04/R09状态同步。00继续冻结；01仅修改intro.p06中概括Y曝光响应的一句，EN/ZH各对应一句，不改其余引言。具体方案原文中的授权门槛已满足，不据此扩大范围。

## 三、逐项修改方案（保留原文）

### R01：Y收益结论按指标和划分限定

**定位**
- [RQ2](F:/Projects/llamarec/paper/modules_parts/results/rq2_exposure_response.md:14)：results.rq2.p01与p03，EN/ZH。
- [曝光讨论](F:/Projects/llamarec/paper/modules_parts/discussion/exposure_interpretation.md:14)：discussion.exposure.p01，EN/ZH。
- 只读联动核对：[引言](F:/Projects/llamarec/paper/modules/01_introduction.md:69)的intro.p06。

**当前问题**
“The additional gains on Y become smaller”与“Y shows diminishing measured gains through 96k”容易覆盖全部Y指标和测试划分，但现有数据仅明确支持验证AUC后一段增量较小。验证F1非单调，测试AUC后一段增量较大。

**修改意图**
- p01先限定“验证AUC的后段增量较小”，再交代F1变化不一致、桥接排序变化很小。
- p03概括“已测Y收益有限或不均匀，N排序在所测两划分至200k仍改善”，保留不同指标尺度不可直接比较及到RQ3的过渡。
- Discussion不列全部检查点，解释响应形态为何使低预算点不足以代表后续表现。
- 可用局部英文术语：smaller later increment in validation AUC；limited or uneven measured gains。中文必须保留相同的“验证”“指标”“已测范围”，不能只做词面替换。

**证据与不得丢失的事实**
binary_exposure中Y验证AUC为0.7761274819/0.7816111073/0.7843504067，测试AUC为0.7784561583/0.7804671174/0.7853511126；验证F1末点低于48k。semantics_bridge中Y验证NDCG约0.5995至0.6031。N已有两划分改善；不得新增收敛、饱和、无限增长或因果解释。

**验收**
读者不能把它读成所有Y指标、两个划分都单调收益递减。原数字不改，EN/ZH范围一致。intro.p06只列联动风险，不默认修改；若后续定稿与其概括产生实质不一致，再申请单句最小同步，不润色其他引言或贡献段。

### R02：正式SASRec四点与历史比较分离

**定位**
- [RQ5](F:/Projects/llamarec/paper/modules_parts/results/rq5_sasrec_exposure.md:25)：results.rq5.p02。
- [基线讨论](F:/Projects/llamarec/paper/modules_parts/discussion/exposure_aware_baselines.md:25)：discussion.baseline.p02。

**修改意图**
从这两个段落的EN/ZH中移除“较早高曝光SASRec超过早期低曝光N”的历史比较句。其来源属于另一预算比较，不作为当前正式四点的证据。不要移成新的Results段落扩大本轮范围，也不删除历史artifact或否定finding C9。

保留正向主线顺序：
1. 四个近似匹配下游任务曝光点均N领先。
2. SASRec随曝光明显改善。
3. 200k差距比96k小。
4. 因而比较须带上实际任务监督量及运行点，资源边界在必要处说明。

**证据与引用**
正式链N24/N48/N96/N200对S47/S94/S188/S391，实际SASRec曝光24,064/48,128/96,256/200,000。保留两划分正式结果及现有表图。移除历史句后，检查这两个段落的EVIDENCE标签：若C9已没有实际承载内容，移除段落中的C9引用，保留仍支撑内容的C7及相关M证据；不要删除source_of_truth里的C9。

**验收**
正文不再让历史跨预算反超与正式匹配四点混在同一证据链中。不能写SASRec在正式链已反超或一定会反超。任何必要claim_matrix位置同步只更新映射，不提升主张强度。

### R03：RQ2桥接NDCG补直接表引用

**定位**
[RQ2](F:/Projects/llamarec/paper/modules_parts/results/rq2_exposure_response.md:14)的results.rq2.p01，EN/ZH。

**修改意图**
保留已有binary_exposure引用，并在报告Y-as-ranker NDCG的同段补已有的semantics_bridge表引用。该指标存在于后者，不在前者。

**验收**
中英文表引用集合一致；桥接数值可以直接追溯。不新增数据表，不改CSV、caption或模型身份。自动检查本来就可能通过，因为旧引用“存在但不足以支撑该数字”，因此还需人工语义追溯。

### R04：只同步旧控制映射的实证状态

**定位**
[final_novelty_claim_map](F:/Projects/llamarec/paper/evidence/final_novelty_claim_map.md:9)，第9、10、33行。

**修改意图**
优先考虑追加明确的MS96实证范围更新及旧句覆盖说明，沿用现有story freeze保留历史的方式；若用户授权直接改表，也只动实证强度、允许表述及状态：
- 完整轨迹仍仅seed42；96k已有42/43/44独立复现。
- 48至96k收窄限定seed42标准k5验证，test保留N优势。
- k20较k5明显更大；k50同方向、较k20小，且不总大于k5。
- MS96已整合；运行元信息、bootstrap来源等独立缺口不因而关闭。

**禁止改变**
文献近邻、创新等级、首创性裁决、贡献层级、Core Thesis。不能删掉“跨seed等价不能证明”这种仍正确的边界，只纠正笼统的“不能写任何跨seed证据”。

**验收**
从这个独立文件进入的读者不会被MS96待补或所有hard条件差距更大误导。story_and_novelty_freeze已有末尾更新，无需回改历史；discussion_literature_update_notes是历史记录，不为消灭关键词而重写。此项超出默认正文编辑，需额外授权。

### R05：Discussion最后增加一次综合

**定位**
[07_discussion](F:/Projects/llamarec/paper/modules/07_discussion.md:23)最后一个INCLUDE之后。现有段落ID全部保留；未来新增ID可考虑discussion.synthesis.p01，实施前验证唯一性。

**段落职责，不是本轮代写稿**
- 用一个自然段归纳：被监督的预测问题决定被训练/测量的能力含义；累计每任务曝光决定比较所处的已观察训练状态；候选协议限定部分模型关系如何呈现。
- 结合正式SASRec四点说明跨家族表现同样应绑定已测运行点。
- 不再逐项报RQ或指标，不重讲Amazon数值，不堆不能证明的清单。
- 只概括现有经验事实，不说表征共享、预训练或潜在能力“导致”结果。

**联动**
保留简洁开篇。discussion.protocol.p02末句的全局三条件总括可交由综合段承担；协议节保留自身“协议内配对与协议间敏感性”的含义，避免三条件在每节重复。

**验收**
新增一对EN/ZH自然段，证据标记只指现有finding。没有新实验、新机制、首次方法或普遍模型排序。该段属于Discussion，不写09 Conclusion或10 Abstract。

### R06：句级分工与数字精简

| 位置 | 建议保留 | 建议压缩或移交 |
| --- | --- | --- |
| results.rq1.p02 | 完整形式边界与到曝光问题的过渡 | 一般benchmark报告启示交discussion.semantics |
| results.rq2.p03 | 响应对照与每任务对齐过渡 | R01改准后不再加一段意义复述 |
| results.rq3.p01/p02/p03 | Y例外、轨迹/复现/test三层、关键差值、CI解读 | 可减少逐指标重复区间端点，全部原CI仍在表中 |
| results.rq4.p01/p02 | k20较大、k50较小且可低于k5、跨seed方向 | 重复CI端点可留表；不能删除非单调反例 |
| results.rq4.p03 | 非嵌套构造、联合变化与跨家族过渡 | 一般“报告时应注明协议”建议交Discussion |
| results.amazon.p02 | 外部方向与直接范围 | 不重复完整未验证项目清单 |
| discussion.exposure.p01 | 为什么早期点不足以描述后续 | 删除24/48/96/200逐点枚举，不增加指标小数 |
| discussion.unification.p01/p02 | 低预算关系不是固定结论；共享模型保留哪些能力 | k20/k50展开交protocol节 |
| discussion.protocol.p01/p02 | k5不能代表所有条件；协议内/协议间解释不同 | 不再详述全部表格和多遍构造，系统边界交Limitations |
| discussion.external.p01/p02 | 详细域内研究与外部方向检验互补 | 压缩逐项模型排序、重复补实验缺口清单 |

**实施边界**
这不是删除所有重复词。Discussion仍需要少量结果锚点，Results仍需要直接解释及自然过渡。优先在同一个完整段落中压缩，不生成“一句claim、一段caveat”的碎片。

**验收**
冗余表中的九项分别有清楚职责；Discussion不变成Results 2.0或Limitations清单。RQ3保持三层证据，RQ4保持k50反例；原始表及每seed值不动。RQ5无需人为扩到与RQ3等长。

### R07：Limitations四类归位

**定位**
[08_limitations](F:/Projects/llamarec/paper/modules/08_limitations.md)，四个现有稳定段落ID。

**修改意图**
- limitations.training.p01：接纳evaluation段现有的bootstrap、训练变异、validation/test角色及无等价检验范围说明；与已有三seed描述统计句合并，避免重复。必要时将M6证据标记随实际内容移入。
- limitations.evaluation.p01：留下协议非嵌套、数量/组成/采样联合变化、PopMatch回顾性流行度、Y/N完整形式；补采样候选评估非穷尽全目录的简短说明。
- limitations.cross_dataset.p01：保留Amazon旧seed42方向检验；可明确未覆盖96k多seed复现，不复述结果数值。
- limitations.compute.p01：保留曝光不等于计算/预训练/服务资源的范围；措辞与R08一致。

**既有依据**
methods.evaluation的采样候选定义及k5/k20/k50清单支持采样评估说明；不需要新实验。它只限定本文报告的候选排序比较，不延伸到SASRec训练目标或全物品打分实现。bootstrap来源记录不完整仍保留。

**验收**
仍是四类自然段，不按RQ逐条辩护；统计说明归位后不在两段重复。移动EVIDENCE标记按实际支撑核对，不能为了对齐标签丢失信息。保留末端行为未知及M每任务调度预期/续训数据跳过条件。

### R08：下游曝光术语与双语强度统一

**定位**
[基线讨论](F:/Projects/llamarec/paper/modules_parts/discussion/exposure_aware_baselines.md:4)标题、p01/p02；
[RQ5](F:/Projects/llamarec/paper/modules_parts/results/rq5_sasrec_exposure.md:29)中文p02；
[Limitations](F:/Projects/llamarec/paper/modules/08_limitations.md:45)的compute.p01。

**修改意图**
- 标题不用裸Sample Efficiency/样本效率；可改为Exposure-Aware Baseline Comparison/曝光感知的基线比较等同范围名称。
- 正文尽量统一为performance under approximately matched downstream task-sample exposure，对应“近似匹配的下游任务样本曝光下的表现”。
- 两处中文“显著改善”改成“明显改善”，与英文strongly/substantial对应，避免无检验的显著性暗示。
- 原有“未建立跨seed显著性”等否定性边界必须保留，不机械清空significance词。

**验收**
不声称更低计算、token、FLOPs、预训练或部署成本；不把点估计优势写成一般样本复杂度定理。中英文范围和强度相等。

### R09：状态和表头整理

**定位**
[outline](F:/Projects/llamarec/paper/plan/outline.md:12)；
[paper_manifest](F:/Projects/llamarec/paper/assembly/paper_manifest.yaml)中两张MS96协议表的中文表头。

**修改意图**
- outline将“未来MS96局部更新”同步为已完成整合、当前待审查计划批准；不改RQ或章节结构。
- 中文protocol表头可改为“协议”，英文列名及CSV键不动。
- test caption现有report-only仅说明冻结后用途，不构成secondary，无需为了减少词频而强改。

**验收**
仅文字状态和表头，不改原始数值、表格角色、列映射、图或参考文献。此项需额外范围授权，不能默认连带执行。

## 四、不改事项与无需新实验的判断

以下现稿事实必须留下：
- seed42完整曲线与43/44仅96k运行点分开。
- 48至96k验证收窄与test不收窄分开。
- 三seed96k为小差距而非等价；测试保留N优势。
- Y能力保留及seed44验证Accuracy例外；不写普遍正迁移。
- k20较大，k50较小、随seed变且不总大于k5；没有单调数量因果。
- 固定seed bootstrap、三训练seed描述变异、验证选择/最终留出测试分别解释。
- 正式SASRec四点均N领先，同时基线改善且200k差距小于96k。
- Amazon只提供旧seed42外部排序方向。
- 曝光不是独立样本数或计算成本，M每任务计数为有条件的调度预期。

两张现有曲线和12张Results相关表均有明确证据职责，不需要新增绘图、合并validation/test或重做统计。原始表和CSV保持不动，除R09可选的中文表头外没有caption修改需求。

在这些边界下，没有需要新实验才能修复的审查问题。若要更强的跨域完整曲线、多seed整条曲线、等价性、正迁移或机制结论，则超出现有证据；本轮不把它们列成可执行实验矩阵。

Conclusion的受限经验结论没有新发现的科学硬缺口，但应先批准并核对范围修正。RUN_METADATA、BOOTSTRAP_PROVENANCE、METHOD_CITATIONS、TEMPLATE_UNASSIGNED仍是独立未闭项；不因此宣布论文可投稿，也不清除任何标记。

## 五、实施验收清单

1. 再读当前作者源及控制文件，确认用户没有同期改动，不覆盖其他人的工作。
2. 先实施R01/R02/R03，其他项按明确获准范围执行。
3. 每次修改保持EN在前、ZH在后；已有段落ID不重命名，新增综合ID唯一。
4. 重新完整阅读三章及00/01的相关发现概括，检查finding、meaning、必要边界的顺序。
5. 对照审查报告九项冗余表和stale词表逐项核验，不以“词都删掉”作为正确标准。
6. 核对原始每seed值、两split、三指标、CI和SD的身份不变；变化只发生在解释和引用职责。
7. 运行既有只读命令，不生成整稿或图表资产。
8. 检查改动清单和保护文件哈希；控制映射只作获准的位置/状态同步，claim strength不变。
9. 用户审阅后停止，不自动继续摘要、结论或投稿排版。

建议复用的现有命令：
```powershell
python -B -X utf8 -m unittest discover -s paper/assembly/tests -v
python -B -X utf8 paper/assembly/assemble.py --modules results discussion limitations --lang bilingual --check
python -B -X utf8 paper/assembly/assemble.py --lang bilingual --check
python -B -X utf8 paper/assembly/assemble.py --lang bilingual --mode final --check
python -B -X utf8 tools/stage_guard.py
git diff --check -- .agent/current_task.md .agent/stage_state.yaml paper
```

final检查若仍因独立缺口或draft/skeleton失败，应如实报告，不为通过而改ready或删除标记。当前未增综合段时三章为33对；未来增加一对后数量会变化，不能硬保33而删除其他段落。

## 六、原审查工作记录与能力使用审计（2026-09-08历史）

本轮已完成：控制文件与正文阅读、A-O审查、33对逐段职责核对、九项冗余表、stale措辞审查、Limitations四类判断、表图角色及现有PNG检查、既有只读验证、两份新文档。

使用的流程：using-research-writing、paper-orchestration、peer-review、verification、writing-core，以及statistical-analysis中的报告边界核对。没有执行统计检验。此次不是全稿写作，不触发章节起草、多agent全文生成或重做架构。

未使用：Wiki技能、文献搜索、图表生成、训练/推理、新实验分析、整稿质量门生成流程，原因均为用户明确限制或本轮不涉及。没有重新宣称外部引用已核验或新颖性获得新的证明。

验证：本轮47项既有测试通过，三章33对/0待补及全局78对/8既有待补通过只读结构检查；final只读门禁按既有缺口拒绝。哈希与最终交付验证见审查报告。结构通过不消除尚未实施的语义建议。

本文件兼作本轮持久任务包及能力使用审计。没有按通用技能模板去改既有progress.md，因为用户更具体的“不直接修改”要求优先；原计划、控制文件和作者源都保持原样，只更新.agent行政记录。

剩余风险：计划尚未获准执行；运行/统计溯源仍有缺口；本轮未做最终排版或外部文献再核。没有把审查完成说成稿件已经修订完成。

**原审查停止记录：当时两份文件完成并验证，R01-R09未执行。该记录保留用于追溯，现已由下列授权执行记录接续。**

## 七、授权执行与验收记录（2026-09-09）

### 实际执行

| 编号 | 已执行内容 | 验收边界 |
| --- | --- | --- |
| R01 | RQ2与曝光讨论改为Y被测收益有限或不均匀；后段增量较小具体限定为验证AUC。Intro p06仅同步对应一句，EN/ZH各一句。 | 不把结论扩大到全部Y指标或测试划分；原数值与N已测范围保留。 |
| R02 | 从RQ5和基线讨论各移除历史跨预算比较句及不再承载内容的C9标签；claim_matrix只将RQ5证据映射C7,C9改为C7。 | 正式四点均N领先、SASRec改善及200k差距小于96k保留；source_of_truth的C9及历史artifact未改。 |
| R03 | RQ2报告桥接NDCG的段落补semantics_bridge引用，两种语言一致。 | 原binary_exposure引用保留；没有新建或修改数据表。 |
| R04 | final_novelty_claim_map末尾追加“当前实证范围更新（R04）”，明确覆盖旧MS96状态和过宽表述。 | 原文件正文前缀保留；不改文献裁决、创新等级、贡献层级、Core Thesis或仍有效的独立缺口。 |
| R05 | 最后一个INCLUDE后仅新增discussion.synthesis.p01一对EN/ZH综合段；协议节原全局总括移交该段。 | 只综合现有监督形式、曝光、协议和SASRec已测关系；不加机制、数字、RQ或摘要/结论。 |
| R06 | 按原表压缩Results/Discussion的重复启示、逐点枚举和部分CI端点；保留关键结果锚点及过渡。 | RQ3的轨迹/96k复现/test三层、Y例外、RQ4的k50反例及所有原表端点保留；RQ3 p03整段未改。 |
| R07 | 统计范围移入training；evaluation保留构造边界并补“采样候选非全目录”；cross_dataset明确无96k多seed外部复现；compute收窄术语。 | 仍是四个原段落ID；未丢失未知末端行为、M预期每任务计数、续训数据跳过及统计溯源缺口。 |
| R08 | 基线讨论标题改为Exposure-Aware Baseline Comparison/曝光感知的基线比较；正文统一近似匹配下游任务曝光含义；两处中文“显著改善”改为“明显改善”。 | 保留无跨seed显著性、无等价性等边界；不声称计算、预训练或服务成本优势。 |
| R09 | outline仅同步Discussion完成状态；manifest两张MS96协议表的中文protocol表头改为“协议”。 | 仅两处zh显示字符串变化；英文、CSV键、列映射、caption、图、数值及章节结构不变。 |

### 范围核验

本轮修改前以当前磁盘191项paper文件建立SHA-256对照，不使用Git旧稿覆盖已有工作。最终仅19项paper文件变化：14份作者源、claim_matrix、final_novelty_claim_map、paper_manifest、outline及本文；其余172项未变，无新增paper文件。另维护两份.agent管理记录。原始CSV、PNG/SVG、参考文献、Methods、Contributions、Related Work、Results入口、旧build、历史审查报告、测试和旧测试基线均未改。

逐段对照为24对既有段落有计划内修改，新增1对discussion.synthesis.p01，没有删除或重命名既有段落ID。Intro全文件与修改前相比，仅两处对应句子替换，分别为EN和ZH；没有其他引言编辑。manifest全文件仅两处中文显示值变化。R04原文件前缀保留，追加内容只同步实证范围。

数据身份与语义核对保留：seed42完整轨迹和43/44仅96k；验证收窄与test不收窄；固定模型bootstrap与三训练seed描述变异；Y的seed44验证Accuracy例外；k20与k50的非单调反例；正式SASRec四点；Amazon早期seed42排序方向。未把跨seed小差距写成等价，未推断数量或模型机制因果。

### 实际验证结果

| 检查 | 结果 | 解释 |
| --- | --- | --- |
| 47项既有单元测试 | 46通过，1失败 | 唯一失败为旧保护哈希要求，详见下文；未修改测试、断言或旧基线。 |
| 三章双语只读装配 | 通过：3模块、34对段落、0待补 | 新增综合段使原33对变为34对；语言、数字与引用契约检查通过。 |
| 全局双语只读装配 | 通过：11模块、79对段落、8既有待补 | 仅运行check，没有生成整稿。 |
| final只读门禁 | exit1，按既有缺口拒绝 | METHOD_CITATIONS、RUN_METADATA、BOOTSTRAP_PROVENANCE及draft/skeleton、未写09/10仍阻止完成稿。未清除标记或改ready。 |
| 14份修改作者源风格扫描 | 已运行并人工复核提示 | 英文禁用表达、主观第一人称、流程文字泄漏检查无命中；双语标签及元数据的格式提示不作为删格式依据。 |
| 逐段与文件范围核验 | 通过 | 24对计划内修改、1对新增；Intro单句双语同步、R04追加、两处中文表头满足边界。 |
| stage_guard | 0错误、0警告 | 维护管理记录后复核。 |
| git diff --check | exit0 | 仅68条既有LF/CRLF提示，无空白错误。 |

旧保护测试为[单元测试](F:/Projects/llamarec/paper/assembly/tests/test_ms96_evidence.py:123)中的test_preserved_files_and_append_only_literature_freeze，读取[旧保护基线](F:/Projects/llamarec/paper/plan/review/ms96_scope_baseline.json)。其57个受保护文件有52个仍相同，只有本轮明确获准的5个文件发生变化：Results的RQ1、RQ2和Amazon段落文件，Discussion的external_validity，以及final_novelty_claim_map。测试在第一个变化的RQ1处失败。独立逐项哈希检查确认没有第六个冲突文件。保留失败如实交付，不以重写历史保护规则使结果变绿。

风格扫描保留一项旧中文词项提示：results.rq2.p03中“接下来的”。该句为原稿已有的每任务曝光对齐过渡，R06明确要求保留其职责，本轮没有为消灭关键词而追加润色。其余格式提示来自既有EN/ZH标签、YAML及证据标记；不据此宣称“全部风格检查零提示”。

### 流程与停止

沿用本地using-research-writing、paper-orchestration、writing-core、writing-chapters、peer-review、verification流程，并用experiment-results-planning和evidence-driven-writing核对结果与引言最小同步边界。已有明确论文定位、方案与本次逐项授权，不重新发起故事选择或章节重构。本文兼作实施任务包及能力使用记录；未为通用流程要求改写progress.md、notes.md或另增计划文件。

没有训练、推理、新实验、新bootstrap或新统计分析、文献搜索、Wiki访问、prepare_assets.py、图表生成、整稿生成、模板适配。既有测试的固定数据一致性检查不构成新的实验或统计结论。

**R01-R09执行完成，验收结果及旧测试冲突如实记录，待用户审阅。本轮到此停止；不自动处理独立证据缺口，不进入Conclusion或Abstract。**
