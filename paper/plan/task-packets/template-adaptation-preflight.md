# Submission Template Adaptation Preflight

日期：2026-09-10

性质：只读审计与执行计划。本轮未修改作者源、科学表述、图表数据或参考文献内容，未生成submission稿，未联网下载模板。

## A. Template identity

### A1. 已找到的模板

| 文件 | 身份 | 作用 | 当前判断 |
| --- | --- | --- | --- |
| paper/templates/Conference-LaTeX-template_10-17-19/conference_101719.tex | 通用IEEE conference LaTeX示例 | LaTeX入口与格式示例 | 当前最适合作为自动化适配入口 |
| paper/templates/Conference-LaTeX-template_10-17-19/IEEEtran.cls | IEEEtran V1.8b，2015-08-26 | conference class | 必需 |
| paper/templates/Conference-LaTeX-template_10-17-19/IEEEtran_HOWTO.pdf | IEEEtran class使用说明 | 类选项、图表、附录和BibTeX说明 | 规范参考 |
| paper/templates/Conference-template-letter.docx | 通用IEEE conference Letter版Word模板 | Word投稿入口候选 | 与LaTeX模板属于同一通用模板家族 |
| paper/templates/Checking list.pdf | 本地投稿自检表 | 4至20页、关键词、图表和参考文献附加要求 | 可能是会议组织方要求，但未写venue |
| paper/templates/文件3：关于学术会议投稿须知.pdf | 通用会议投稿须知 | 出版、检索和注册说明 | 不提供venue或版式身份 |

### A2. 模板身份结论

| 字段 | 结论 | 依据 |
| --- | --- | --- |
| Venue | UNKNOWN | 所有文件均未给出会议名称、缩写或track |
| Template family | IEEE conference | LaTeX入口使用documentclass conference IEEEtran，Word模板和检查清单也明确引用IEEE |
| Version | LaTeX文件夹日期2019-10-17；IEEEtran V1.8b，2015-08-26 | 文件名与class头部 |
| Submission mode | 当前示例为非匿名、作者信息完整的camera-ready式布局；实际review mode UNKNOWN | 示例含完整author block；没有会议级匿名说明 |
| Columns | 双栏 | IEEEtran conference默认双栏；检查清单明确双栏 |
| Page size | US Letter，612乘792 pt | class默认、Word模板和检查清单一致；示例PDF实测为Letter |
| Bibliography | 数字顺序引用；IEEE格式 | 示例使用cite与手工thebibliography；HOWTO建议IEEEtran BibTeX style |
| Required class/style | IEEEtran.cls、cite、amsmath、amssymb、amsfonts、algorithmic、graphicx、textcomp、xcolor | conference_101719.tex |
| Missing template dependency | IEEEtran.bst未随模板提供 | HOWTO建议bibliographystyle IEEEtran，但目录中没有bst |

结论：可确认的是通用IEEE conference模板家族，不能确认具体venue。执行适配前必须由用户确认会议名称、年份或track，以及LaTeX还是Word为正式提交入口。

Word模板使用Strict OOXML关系命名空间，常见python-docx解析器不能直接打开。若正式入口选择Word，执行阶段需先在可审计的兼容层中转换为Transitional OOXML，或使用能够保留Strict OOXML的Word自动化流程；不能把当前解析失败误判为模板损坏。LaTeX路径没有这一兼容障碍，因此是当前技术推荐。

模板目录中的aux、log、synctex.gz、DS_Store和以波浪号开头的Word锁文件是现有编译或编辑缓存，不属于正式模板合同，也不应进入submission package。

## B. Submission constraints

### B1. REQUIRED

以下仅按本地Checking list与模板明文记录：

| 约束 | 要求 |
| --- | --- |
| 页面 | Letter纸，双栏；上边距1.9 cm、下边距2.54 cm、左右约1.57 cm；不手工改class控制的边距、字体、列宽或行距 |
| 篇幅 | 至少4页，最多20页 |
| 标题 | 不使用副标题；标题和摘要不放符号、特殊字符、脚注或数学公式 |
| 作者 | 检查清单要求完整姓名、单位、城市、邮编、国家，并用星号标通讯作者 |
| 关键词 | 3至10个 |
| 图片 | 高清、100%查看可读、不得含中文、嵌入正文并按首次引用后放置 |
| 表格 | 可编辑；正文引用并连续编号 |
| 公式 | 连续编号；模板控制排版，不以图片代替可编辑公式 |
| 参考文献 | 至少5条，正文全部引用，数字编号；检查清单要求每条有DOI或来源链接 |
| 模板文本 | 提交前必须删除示例和指导文字 |

### B2. RECOMMENDED

| 约束 | 建议 |
| --- | --- |
| Figure/Table placement | 放在栏顶或栏底；大图表可跨双栏；图题在图下，表题在表上 |
| Equations | 使用align或IEEEeqnarray，不使用eqnarray；尽量保持单栏宽度 |
| Cross-references | 使用LaTeX label/ref等软引用，不硬编码编号 |
| Acknowledgment | 使用不编号标题；资助信息按模板放首屏脚注，不需要时删除示例thanks |
| Bibliography generation | 使用BibTeX和IEEEtran style，或者按模板的IEEE格式生成等价参考文献 |
| Last page | 最终编译时检查双栏平衡 |

### B3. UNKNOWN

模板未明确以下事项，不使用常识补齐：

- 20页是否包含References。
- Appendix是否计入页数，以及是否允许主稿附录。
- Supplementary material的提交形式、页数和匿名规则。
- Abstract字数上限。当前英文摘要只读统计为233词。
- 具体venue要求的章节顺序。
- 双盲、单盲或实名投稿。
- Ethics、broader impact、reproducibility或专门checklist章节。
- arXiv政策。
- URL与DOI的精确显示格式。
- Camera-ready版权页、copyright notice或paper ID要求。

### B4. 本地文件冲突

| 冲突 | LaTeX/IEEE示例 | Checking list | 处理原则 |
| --- | --- | --- | --- |
| 图引用名称 | 常规conference示例使用Fig. | 要求Figure全称 | 执行前确认会议方哪个文件优先 |
| 表编号 | IEEEtran通常按罗马数字显示 | 检查清单示例为阿拉伯数字 | 不手工覆写class，先向会议方确认 |
| 正文引用 | cite生成普通方括号数字 | 检查清单要求上标形式的方括号数字 | 先确认是否为Word专用要求或会议覆盖规则 |

## C. Current to template section map

第一版适配应保持现有科学结构，只映射展示层：

| Current module | Template destination | Action | 理由 |
| --- | --- | --- | --- |
| Abstract | abstract environment，位于maketitle之后 | KEEP | 与模板原生结构一致 |
| Introduction | Section I Introduction | KEEP | 无需重排 |
| Related Work | Section II Related Work | KEEP | 通用示例允许独立主题section；没有venue文件禁止独立Related Work |
| Problem Formulation | Section III Problem Formulation | KEEP | 先保留任务定义与符号边界 |
| Methodology | Section IV Methodology | KEEP | 与问题定义分工明确 |
| Experimental Setup | Section V Experimental Setup | KEEP | 当前约1041词且承载数据、训练、评估和统计设置，不宜预检阶段机械合并 |
| Results | Section VI Results | KEEP | 主结果结构冻结 |
| Discussion | Section VII Discussion | KEEP | 与结果分开保留解释层 |
| Limitations | Section VIII Limitations | KEEP | 模板未要求合并，当前独立section可保留 |
| Conclusion | Section IX Conclusion | KEEP | 与模板惯例兼容 |
| References | 不编号References区 | TEMPLATE-SPECIFIC | 交给IEEE bibliography层生成 |

paper/modules/00_contributions.md是内部Contribution Working Version，不应自动成为独立投稿section。适配器应将其标记为TEMPLATE-SPECIFIC：先检查Introduction是否已承载相同贡献，再决定只作为校验输入还是经另行授权合并，不能重复装入正文。

### Methods结构判断

Problem Formulation、Methodology、Experimental Setup第一版全部保留。若真实编译超过上限，再按以下顺序提出方案：

1. 先缩短标题层级、去除重复空白并优化图表浮动，不改内容。
2. 仍超限时，优先评估Problem Formulation与Methodology合为一个展示section，但保留原paragraph ID和内部顺序。
3. Experimental Setup因信息密度高，暂不并入Methodology；只有实际页数证明必要时才另行计划。

## D. References integration

### D1. 当前状态

- paper/references/library.bib含31条记录。
- 只读字段检查显示31条均至少含DOI或URL，满足本地检查清单的最低链接要求。
- 当前作者源使用Pandoc风格引用标记，例如方括号中的at-key；当前Markdown assembler不会转换为LaTeX cite命令。
- 模板目录没有IEEEtran.bst。示例tex使用手工thebibliography；IEEEtran HOWTO建议bibliographystyle IEEEtran与bibliography。

### D2. 迁移方案

1. 保留library.bib为参考文献source of truth，不在作者源中手改引用。
2. LaTeX适配层将单条和成组引用转换为cite命令，并保持首次出现顺序。
3. 构建层接入IEEEtran bibliography style。若正式venue包未提供IEEEtran.bst，先确认TeX发行版是否内置；submission package是否必须携带bst由venue决定。
4. 构建测试必须拒绝未解析at-key、缺失BibTeX key、正文未引用条目和中文残留。
5. 检查清单中的上标方括号引用要求与通用LaTeX模板冲突，未确认前不增加自定义宏覆盖cite。
6. 标题大小写、作者列出规则和DOI/URL显示交给submission bibliography层处理，不改原始library.bib的科学身份。

## E. Figure and table risks

### E1. Figures

| Asset | Current role | Likely template placement | Risk |
| --- | --- | --- | --- |
| n_native_exposure，1644乘1292 | N任务随曝光变化 | 先试单栏figure；若轴标签缩小后不可读则figure* | MEDIUM，图较接近方形，单栏宽度可能使标签偏小 |
| n_vs_sasrec_exposure，2012乘1398 | N与SASRec曝光对齐比较 | 优先figure*或单栏实编译对照 | MEDIUM，图例和多序列在单栏有可读性风险 |

两图当前均为英文标签且像素充足。需要在真实PDF 100%查看时验证轴、图例和线型，不能只凭像素尺寸判定。

### E2. Tables

| Asset | Current role | Likely template placement | Risk |
| --- | --- | --- | --- |
| datasets，6列乘4行 | 数据集与任务划分 | 单栏table | MEDIUM |
| training_exposure，6列乘9行 | 训练步数与曝光 | 单栏优先，必要时table* | MEDIUM |
| binary_exposure，6列乘10行 | Y侧曝光结果 | table*或拆分展示 | MEDIUM |
| semantics_bridge，6列乘8行 | Y-as-ranker与N | table* | MEDIUM |
| exposure_scaling，6列乘12行 | N与M-N曝光轨迹 | table* | MEDIUM |
| specialist_multitask，5列乘6行 | specialist与multitask差值和区间 | 单栏优先 | LOW |
| hard_candidate，8列乘18行 | k5/k20/k50稳健性 | table*；详细行可列为appendix candidate | HIGH |
| n_vs_sasrec_exposure，7列乘8行 | N与SASRec曝光对齐 | table* | HIGH |
| cross_dataset，5列乘5行 | Amazon外部验证 | 单栏table | LOW |
| ms96_main_validation，13列乘3行 | 96k三seed验证主结果 | table*，需多级表头或受控横向压缩 | HIGH |
| ms96_main_test，13列乘3行 | 96k三seed测试主结果 | table*，需多级表头或受控横向压缩 | HIGH |
| ms96_protocol_validation，11列乘9行 | 多候选协议验证结果 | table*；appendix candidate | HIGH |
| ms96_protocol_test，11列乘9行 | 多候选协议测试结果 | table*；appendix candidate | HIGH |
| ms96_delta_summary，7列乘24行 | 三seed差值均值与样本标准差 | table*；appendix candidate | HIGH，长表和长caption均占页 |

风险处理只改变展示，不改变CSV、数值、方向或caption含义。优先措施为多级表头、合理缩写、单栏与双栏浮动选择、重复caption压缩和长表分页策略。将资产移入appendix或supplement必须等待venue政策和用户授权。

## F. Page-budget risk

### F1. 只读统计

| 项目 | 当前规模 |
| --- | ---: |
| 英文作者内容 | 约7,481词 |
| 其中Contribution Working Version | 约313词，不能默认作为独立投稿section |
| 英文摘要 | 233词 |
| 正式表格 | 14 |
| 正式图片 | 2 |
| BibTeX记录 | 31 |
| 本地清单页数上限 | 20页 |

### F2. 风险判断

总体为MEDIUM。7千余词本身不能推出超页，但14张表中有5张11至13列宽表，另有多张长表和较长caption，浮动布局是主要风险。References是否计入20页未知，因此现在不能给出预计页数，也不能证明需要正文压缩。

当前机器未检测到latexmk、pdflatex或bibtex。后续页数估计应在LaTeX适配器完成后，用正式编译环境生成第一版不压缩PDF，并记录：

1. 主文、References和Appendix各自起止页。
2. 每张图表实际占页、跨栏状态与首次引用距离。
3. overfull box、浮动积压、孤行和最后一页平衡。
4. 分别按“References计入”和“不计入”两种规则计算预算，直到venue规则确认。

在真实编译前不建议删减科学正文。若超页，严格按格式与空白、表格布局、重复caption、重复叙述、附录候选、科学内容压缩的顺序处理；后三项需另行授权。

## G. Proposed submission build architecture

推荐采用方案A：继续以现有Markdown双语作者源为source of truth，扩展submission-specific LaTeX assembly layer。

建议未来新增但本轮不创建：

paper/submission/<venue>/

- template_manifest.yaml：模板身份、mode、section mapping、caption和citation策略。
- main.tex：稳定的IEEEtran入口，只包含模板设置和generated include。
- generated/sections/：由现有paragraph ID生成的英文LaTeX片段。
- generated/tables/：由manifest与CSV生成的可编辑LaTeX表格。
- figures/：构建时从当前正式图资产复制或引用。
- library.bib：从现有library.bib字节复制或经可审计的格式层生成。
- build.ps1或等价Python入口：验证、转换、BibTeX、编译和产物清理。
- build_manifest.json：记录作者源、模板、资产和参考文献hash，以及paragraph到tex位置映射。

最终生成物仍写入paper/builds/<venue>/，不回写paper/modules或paper/modules_parts。

### 构建流程

1. 运行现有bilingual和English check，验证paragraph、evidence、数字和资产对应关系。
2. 按manifest选择英文，不删除中文作者源。
3. 结构化转换标题、段落、引用、公式、图表与交叉引用。
4. 生成LaTeX submission layer，检查所有正式module均有目的地，Contribution Working Version单独裁决。
5. 编译并检查未解析引用、missing asset、overfull box、页数和PDF视觉效果。
6. 生成可追溯build manifest；任何正文压缩回到单独授权的adaptation记录，不直接改generated tex。

不建议方案B的手工全文LaTeX迁移。它会复制35个作者源、破坏双语同步和现有evidence/hash contract，也容易产生两个互相漂移的正文版本。

## H. Required user decisions

执行前需要用户确认：

1. 具体venue、年份和track；目前文件无法确定。
2. 正式入口是LaTeX还是Word。技术上推荐LaTeX，但不能替用户决定。
3. 当前阶段是anonymous review还是camera-ready；现有示例本身不是匿名模板。
4. 20页是否包含References、Appendix，以及supplementary material政策。
5. Checking list与通用IEEE模板冲突时，以哪个文件为准，特别是Figure或Fig.、表编号和上标引用。
6. 是否允许把协议全表、delta summary等详细资产放入Appendix或Supplement。
7. 后续何时提供作者、单位、通讯作者、资助和acknowledgment信息；匿名阶段不得提前写入。
8. 若选择Word，是否允许先做Strict OOXML兼容转换；若不允许，应使用Word原生自动化而不是python-docx。

## I. Execution plan

后续必须另开执行阶段，建议顺序如下：

| Step | 工作 | 允许修改层 | 验收 |
| --- | --- | --- | --- |
| P0 | 用户确认H节决定；冻结venue模板身份 | submission plan和template manifest | venue、mode、page rule均非UNKNOWN |
| P1 | 实现LaTeX adapter及转换测试 | paper/assembly与paper/submission/<venue> | module全覆盖、paragraph映射、无中文泄漏、引用全解析 |
| P2 | 生成第一版未压缩英文稿 | generated layer与paper/builds | 不改作者源；编译成功；无模板指导文字 |
| P3 | 处理图表跨栏、caption和可编辑表格 | submission展示层 | 数值hash不变；100% PDF可读 |
| P4 | 做真实page-budget审计 | build报告与adaptation计划 | 报告主文、参考文献和附录页数 |
| P5 | 如超页，先执行纯格式优化 | submission展示层 | 不删结果、不改claim、不改RQ |
| P6 | 用户另行授权后才处理重复叙述或appendix迁移 | 双语作者源或venue adaptation记录 | 双语同步、科学审查、合同版本化 |
| P7 | 按anonymous或camera-ready模式打包 | submission metadata层 | 作者信息、ack、PDF元数据和文件清单符合venue要求 |

## J. Model recommendation for execution

- 主适配：中档coding模型。任务需要解析现有assembler、实现可测试的Markdown到IEEE LaTeX映射并维护hash与paragraph provenance。
- 机械复验：低成本coding模型可运行编译、引用、资产、页数和打包检查。
- 文字压缩：仅在真实超页且用户授权后，使用中档writing/reasoning模型；不得与格式适配混在同一轮。
- 不需要GPT6 Astra，也不需要联网研究、训练、推理或新实验。

### Capability-use audit

- Required skills：using-research-writing、paper-orchestration、peer-review、latex-output、pdf、documents、verification。
- Skills actually used：全部已读取并按只读预检范围执行。
- Inputs consumed：现有LaTeX/Word模板、IEEEtran HOWTO、Checking list、投稿须知、manifest、assembler/adapter、正式图表登记、BibTeX、模块头部与只读规模统计。
- Inputs not used：Wiki、实验outputs、联网venue说明；均不在本轮范围，且venue尚未确定。
- Artifacts produced：本preflight计划。
- Verification：模板文件清单、PDF/DOCX只读解析、Letter页面尺寸核对、模块和资产统计、BibTeX DOI/URL检查、作者源hash复核与stage guard。
- Remaining risk：具体venue、匿名模式、页数计入规则和本地检查清单冲突尚待用户决定；当前环境没有LaTeX编译工具，未做页数实测。
