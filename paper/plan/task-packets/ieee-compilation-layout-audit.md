# IEEE Compilation, Layout Audit, and Page-Cost Assessment

## Task Packet

- Stage: S5 review and submission engineering.
- Scope: 重新生成并真实编译English与bilingual IEEE builds；审计日志、页数、section占用、14表、2图、References、浮动体和视觉页面；计算用户给定的粗略额外页成本。
- Files to read: `paper/submission/ieee_generic/**`、两套generated build、编译日志/PDF、现有47项manuscript tests与8项submission tests。
- Files allowed to edit: `paper/submission/ieee_generic/**`、`paper/builds/ieee_generic/**`、submission tests、本任务包、独立审计报告、`paper/plan/progress.md`、`.agent/current_task.md`、`.agent/stage_state.yaml`。
- Frozen inputs: `paper/modules/**`、`paper/modules_parts/**`、`paper/references/library.bib`、`paper/tables/*.csv`、正式figure与科学证据控制文件。
- Required skills: using-research-writing、paper-orchestration、latex-output、peer-review、verification、pdf。
- Evidence inputs: TeX tool versions、`kpsewhich`结果、adapter fresh builds、main.log/aux/bbl/blg/PDF、PDF page metadata、全页PNG渲染、文本与坐标提取。
- Required artifacts: 两份可打开PDF及辅助编译文件；一份包含逐表/逐图/逐section/References和P0–P4建议的审计报告；更新后的自动测试和阶段记录。
- Rejection checks: 不手改generated sections；不修改科学作者源或数据；不删段落/列/实验/文献；不通过margin、极端小字或负vspace规避页数；不把generic audit声称为venue compliance。
- Validation commands: fresh adapter generation；English和bilingual完整LaTeX/BibTeX编译链；log模式扫描；PDF metadata与全页render；47+8 tests；assembly checks；current manuscript contract；stage_guard；限定diff-check。

## Review gates

1. Spec compliance: 两版真实编译，必需辅助文件保留，页数由PDF metadata读取，逐表逐图与视觉页面均有证据。
2. Quality and isolation: BLOCKER/LAYOUT_WARNING/HARMLESS分类可靠；只执行P0/P1生成层修复；作者源和数据哈希保持不变。

## Completion

- 状态：COMPLETED。
- M01至M03按用户明确授权执行并通过验证。
- 最终English为14页，Bilingual为22页；详细编译、版面、逐表逐图和成本审计见`paper/plan/task-packets/ieee-post-layout-fix-audit.md`。
- 当前建议：`CONTENT_COMPRESSION_WORTH_REVIEWING`，仅为下一阶段建议，本轮未执行任何内容压缩。
