# Figure and Results Display Audit Task Packet

## Task Packet

- Stage: S5 display-responsibility review.
- Scope: 当前两张正式Figure、Results逐段数字、T-BALANCED九表目标、必要Discussion/Conclusion重复、当前English PDF展示位置与占页。
- Files to read: 当前English PDF；Results作者源；两张figure源、caption与data manifest；`table-evidence-audit.md`、`table-evidence-judge-packet.md`；必要Discussion/Conclusion。
- Files allowed to edit: 本任务包、`figure-results-display-audit.md`、`figure-results-display-judge-packet.md`、`paper/plan/progress.md`和阶段控制文件。
- Frozen files: `paper/modules/**`、`paper/modules_parts/**`、`paper/tables/*.csv`、`paper/figures/**`、`paper/submission/ieee_generic/**`、当前build/PDF。
- Required skills: using-research-writing、paper-orchestration、peer-review、verification、pdf只读视觉检查。
- Evidence inputs: 14页English PDF及页面渲染、Results RQ1-RQ5/Amazon段落、两图数据/caption、T-BALANCED表格责任图。
- Required artifacts: 完整display audit、紧凑judge packet、RQ display responsibility map、逐段数字分类、D-LIGHT/BALANCED/AGGRESSIVE与页数区间。
- Rejection checks: 不改Results/Discussion/Conclusion；不改/重画/删除Figure；不改table或submission；不重新编译；不开始Text Compression Audit；不调用GPT6 Astra。
- Validation commands: 写前/写后author source、figure、table、submission与PDF SHA比较；报告结构/段落覆盖检查；两阶段review；stage_guard；限定diff-check。

## Review Gates

1. Spec compliance: 两图各有唯一verdict；RQ1-RQ5显示责任明确；Results每段数字都有保留/删减计划；三档方案与页面区间齐全。
2. Quality and isolation: scientific comprehension优先；Figure/Table同源不自动判冗余；删除候选只针对第三层逐点数字复述；冻结文件零修改。
