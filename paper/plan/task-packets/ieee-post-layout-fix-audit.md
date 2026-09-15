# IEEE Post-Layout-Fix Audit

## A. Environment

- `pdflatex`: MiKTeX-pdfTeX 4.27 / MiKTeX 26.5，可用。
- `xelatex`: MiKTeX-XeTeX 4.18 / MiKTeX 26.5，可用。
- `bibtex`: MiKTeX-BibTeX 4.2 / MiKTeX 26.5，可用。
- `latexmk.exe`: 路径存在，但缺Perl、probe失败；M01自动改走显式engine/BibTeX链路，未安装Perl。
- `IEEEtran.bst`: `kpsewhich`解析到MiKTeX系统路径，实际BibTeX使用IEEEtran.bst 1.14。
- `xeCJK.sty`: `kpsewhich`解析成功；M02 AUTO命中`Noto Serif SC`，PDF内嵌`NotoSerifSC-ExtraLight`。

## B. Compilation result

| Build | Engine | Driver | Status | PDF |
| --- | --- | --- | --- | --- |
| English | pdflatex | explicit engine + bibtex | COMPILED | `paper/builds/ieee_generic/en/main.pdf` |
| Bilingual | xelatex | explicit engine + bibtex | COMPILED | `paper/builds/ieee_generic/bilingual/main.pdf` |

两版均完成engine、BibTeX、engine、engine闭环。25条citation生成25个bibitem；undefined citation/reference、missing file/style/character、duplicate label、overfull hbox/vbox、unprocessed float均为0。

English有6处underfull hbox、3处underfull vbox；Bilingual有14处underfull hbox、4处underfull vbox，并有Latin/CJK粗体或斜体字形fallback。它们未造成截断、重叠、缺字或不可读页面，分类为HARMLESS/LAYOUT_WARNING，不是BLOCKER。

## C. Page counts

- English before M03: 13 pages。
- English after M03: 14 pages。
- Bilingual after M02/M03: 22 pages。
- English逻辑正文至第12页；References从第13页开始并延续至第14页。
- Bilingual正文至第20页；References位于第21至22页。

## D. Cost estimate

按用户给定而非venue官方的粗略模型：`max(0, 14 - 4) = 10`个额外页，估计额外成本约`10 * 400 = 4000 RMB`。4页只是理想目标；此估计不构成删减科学证据的自动授权。

## E. Compile warnings

- BLOCKER: 0。
- LAYOUT_WARNING: English有3个underfull vbox，来自宽表重新分布；Bilingual有4个underfull vbox及若干双语断行松散。
- HARMLESS: 英文复合词、caption和双语参考文献中的underfull hbox；双语缺少部分粗体/斜体CJK字形时回退到regular。
- 修复前English的float-only page 9与两次10.30617pt overfull vbox均已消失。

## F. Section space profile

| Section | Profile | Physical pages / observation |
| --- | --- | --- |
| Abstract | SMALL | page 1 |
| Introduction | MEDIUM | pages 1-2 |
| Related Work | MEDIUM | pages 2-3 |
| Problem Formulation | SMALL | page 3 |
| Methodology | MEDIUM | pages 3-4 |
| Experimental Setup | LARGE | pages 4-5 |
| Results | VERY_LARGE | text starts page 5; associated tables/figures extend through page 11 |
| Discussion | LARGE | starts page 8 and continues through page 12, interleaved with deferred result floats |
| Limitations | SMALL | page 12 |
| Conclusion | SMALL | pages 12-13 transition |
| References | MEDIUM | pages 13-14, approximately 1.5-2 columns of entries |

最大版面消费者是Results及其14张表，随后是Discussion；References约占不足一整页的双栏面积，不是13/14页规模的主要来源。

## G. Table audit

| ID | Page | Float | Readability | Status | Observation |
| --- | ---: | --- | --- | --- | --- |
| datasets | 4 | single column | readable | OK | 宽度与正文一致，无溢出 |
| training_exposure | 5 | single column | readable | OK | caption较长但未造成异常空白 |
| binary_exposure | 6 | single column | readable | OK | 5位显示清晰 |
| semantics_bridge | 6 | single column | readable | OK | 与引用段落接近 |
| exposure_scaling | 6 | single column | readable | OK | 与Figure 1共同呈现，仍可读 |
| ms96_main_validation | 8 | table* | dense but readable | OK_AFTER_M03 | 12列，仍是高密度风险表 |
| ms96_main_test | 8 | table* | dense but readable | OK_AFTER_M03 | 12列，仍是高密度风险表 |
| specialist_multitask | 8 | single column | readable | OK | CI方向与符号清楚 |
| ms96_delta_summary | 9 | table* | clearly readable | OK_AFTER_M03 | 从修复前小字密集表变为完整可读；占用较高 |
| hard_candidate | 10 | table* | clearly readable | OK_AFTER_M03 | CI列清晰，无overfull |
| ms96_protocol_validation | 10 | table* | readable, small | OK_AFTER_M03 | 11列，仍是最高密度风险之一 |
| ms96_protocol_test | 11 | table* | readable, small | OK_AFTER_M03 | 11列，仍是最高密度风险之一 |
| n_vs_sasrec_exposure | 11 | table* | clearly readable | OK | exposure整数保持整数 |
| cross_dataset | 11 | single column | clearly readable | OK | 无异常缩放 |

M03后14表均无编译布局错误。残余最大风险是VI/VII/XI/XII的列密度，但在PDF实际尺寸下可读；不建议本轮再缩字。部分后置宽表与首次正文引用相隔2-4页，这是14表集中出现时的浮动体代价。

## H. Figure audit

- Figure 1: English page 7、Bilingual page 11；column width，原图1644x1292，曲线、坐标和caption可读，无裁切或异常空白。
- Figure 2: English page 8、Bilingual page 16；column width，原图2012x1398，图例、趋势和双语caption可读，无裁切。
- 两版复制图片字节与正式源SHA一致；未重绘或改变数据。

## I. References audit

- 实际引用25个key，生成25个bibitem；library.bib中未引用条目不会进入References。
- English References从page 13开始，在page 14左栏上部结束；Bilingual从page 21开始，在page 22左栏上部结束。
- 未发现duplicate entry、undefined citation、异常URL/DOI越界或不可读换行。
- 最后一页列未平衡，存在明显空白；列平衡只能改善观感，预计不能减少总页数，留到venue/camera-ready阶段。

## J. Pure layout fixes applied

- M01: 实际probe latexmk并在不可运行时回退显式编译链；MiKTeX禁止隐式安装。
- M02: 可移植CJK AUTO字体族回退，当前命中Noto Serif SC。
- M03: 生成PDF表格统一5位小数显示；整数、文本、CSV和raw payload不变。
- 未执行margin修改、negative vspace、极端字体缩小、删列、手改generated TeX或正文压缩。

## K. Optional compression candidates

- P0: 已完成，无剩余编译blocker。
- P1: 已完成已授权的显示精度与字体/driver修复；不建议继续以缩字换页。
- P2: 可在独立授权阶段审查Results与Discussion重复解释，保守估计可能节省约1-2页；本轮未标定具体删改句。
- P3: VI/VII、XI/XII存在成对结构，可评估合并展示或正文保留摘要表；可能节省约1-2页，但会改变结果呈现结构，本轮不执行。
- P4: 若未来venue允许supplement，可考虑将完整逐seed协议表移出正文，可能节省约2页；当前Appendix/Supplement政策UNKNOWN，不执行。

## L. Recommendation

`CONTENT_COMPRESSION_WORTH_REVIEWING`

理由：纯布局修复已达到编译正确和可读性目标，但English为14页，相对4页理想目标仍多10页，粗略成本约4000 RMB。额外页面主要来自完整Results表组和较长Discussion，而不是可通过免费格式技巧消除的空白。下一阶段若要降页，应先明确venue真实页限与supplement政策，再单独授权P2-P4；不得把本审计自动视为压缩授权。
