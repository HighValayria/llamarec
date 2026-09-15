# IEEE Compilation and Layout Modification Plan

## Status

`EXECUTED_AND_VERIFIED`

用户于2026-09-10通过“IEEE Pure Layout Fix Execution + Recompile”明确批准M01、M02、M03。本文件保留修复前事实，并在文末追加执行结果；作者源、表格CSV、正式图片和generated section正文均未手工修改。

## Evidence collected before modification

- `pdflatex`、`xelatex`、`bibtex`可用；`latexmk.exe`存在但因缺少Perl无法运行。
- `kpsewhich IEEEtran.bst`与`kpsewhich xeCJK.sty`均成功。
- English显式`pdflatex -> bibtex -> pdflatex -> pdflatex`已生成13页PDF，25条引用闭合；无undefined citation/reference。
- Bilingual在`xeCJK`加载后因AUTO回退到不存在的`FandolSong-Regular`而停止；本机`fc-list`确认`Noto Serif SC`可用。
- English第9页是纯float页并出现两次10.30617pt overfull vbox；14表中Table VI、VII、IX、X、XI、XII存在明显密度或可读性风险，最大风险是Table XI/XII及VI/VII。
- 宽表主要横向成本来自CSV保留的长小数串；当前生成器对数值原样输出，没有采用现有Markdown assembler的5位小数显示规则。

## Proposed changes

### M01 - P0 - Robust compiler fallback

- Files: `paper/submission/ieee_generic/build_submission.py`、submission tests。
- Change: 不仅检查`latexmk`路径是否存在，还执行轻量可用性探针；若其因缺少Perl返回非零，则自动回退到显式engine/BibTeX三遍链路。
- MiKTeX: 显式engine调用增加`--disable-installer`，避免审计过程隐式安装包；其他TeX发行版不添加该参数。
- Scientific effect: none。
- Acceptance: `--compile`在当前环境自动选择pdflatex或xelatex链路，不被坏掉的latexmk阻塞；测试覆盖fallback。

### M02 - P0 - Portable bilingual AUTO font fallback

- Files: `paper/submission/ieee_generic/build_submission.py`、submission config/tests。
- Change: AUTO按通用字体族名依次探测`Noto Serif CJK SC`、`Noto Serif SC`、`Source Han Serif SC`、`SimSun`；首个可用项用于`setCJKmainfont`，全部不可用时给出明确CJK错误。
- Current host: 将命中`Noto Serif SC`；不写个人字体绝对路径，不提交字体文件。
- Scientific effect: none。
- Acceptance: bilingual完整XeLaTeX/BibTeX链路成功，中文可提取且页面渲染无乱码/tofu。

### M03 - P1 - Wide-table display precision

- Files: `paper/submission/ieee_generic/submission_config.yaml`、`build_submission.py`、submission tests。
- Change: 新增显式`table_numeric_display_precision: 5`；只在生成LaTeX单元格时将普通浮点数字格式化为5位小数，整数、文本、样本数和原CSV保持不变。`build_manifest.json`继续以原始CSV payload计算一致性哈希，并额外记录显示策略。
- Motivation: Table VI/VII/X/XI/XII的10至18位小数迫使整表缩放到难以阅读；5位显示与现有Markdown assembler一致，可显著缩短列宽。
- Scientific effect: 不改变源数据、符号方向、统计含义或claim，但会改变PDF中的显示舍入，因此必须得到用户明确授权。
- Acceptance: 两版原始payload哈希继续一致；数值误差仅来自声明的显示舍入；宽表可读性改善；不删列、不改CSV。

## Deferred, report only

- P2: 文本重复压缩候选，不执行。
- P3: 表格拆分/合并候选，不执行。
- P4: Supplement/Appendix迁移候选，不执行。
- Last-page reference column balancing: 可改善第13页观感但预计不减少总页数，且更适合venue/camera-ready阶段，当前不执行。
- Float-only page 9: 先在M03后重新编译评估；若仍存在，只作为layout finding报告，不自动加入`
clearpage`、负vspace或激进float参数。

## Authorization boundary

- 请求一次性授权执行M01与M02。
- M03涉及PDF显示舍入，请用户单独明确是否一并授权。
- 未获授权前不修改上述adapter/config/tests；无论授权范围如何，都不修改manuscript作者源、library.bib、CSV或正式figure。

## Execution result

- M01 PASS：`latexmk.exe`探针识别其因缺Perl不可用，自动回退到`pdflatex/bibtex/pdflatex/pdflatex`或`xelatex/bibtex/xelatex/xelatex`；MiKTeX显式engine使用`--disable-installer`。
- M02 PASS：AUTO按批准顺序探测并命中`Noto Serif SC`；双语PDF成功生成，字体嵌入，中文可提取，视觉检查无tofu/乱码。
- M03 PASS：生成层统一显示5位小数。14份CSV SHA256、raw payload hash、行列数和符号方向与修复前一致；EN/Bilingual raw payload一致。
- English：修复前13页，修复后14页。表VI/VII/IX/X/XI/XII可读性明显改善；原float-only page 9和两次10.30617pt overfull vbox消失。
- Bilingual：首次完整编译成功，22页；仅作内部review，不用于投稿成本判断。
- 两版均为25条citation，undefined citation/reference均为0；无overfull hbox/vbox、missing character、duplicate label或unprocessed float。
- 详细结果见`paper/plan/task-packets/ieee-post-layout-fix-audit.md`。
