# Table Evidence Audit Task Packet

## Task Packet

- Stage: S5 evidence-preserving table review.
- Scope: 当前English build中的Table I-XIV、其14份active CSV、Results及必要的Methods/Discussion/Limitations上下文、当前PDF页面占用，以及压缩前不可变归档。
- Files to read: `paper/tables/*.csv`、`paper/modules/06_results.md`、`paper/modules_parts/results/**`、必要的Methods/Discussion/Limitations、当前English build及PDF。
- Files allowed to edit: 本任务包、`table-evidence-audit.md`、`table-evidence-judge-packet.md`、`paper/archive/tables/pre_compression_2026-09-10/**`、`paper/plan/progress.md`、阶段控制文件。
- Frozen files: `paper/tables/*.csv`、`paper/modules/**`、`paper/modules_parts/**`、`paper/submission/ieee_generic/**`、正式figures及当前PDF。
- Required skills: using-research-writing、paper-orchestration、peer-review、verification；CSV结构按spreadsheets的科学数据规则核对；PDF只读检查按pdf流程执行。
- Evidence inputs: 当前14份CSV、generated TeX/manifest/aux、14页English PDF、Results及必要边界段落、既有审计记录。
- Required artifacts: 14/14 byte-for-byte archive、README、manifest.json、逐表审计、紧凑judge packet、阶段进度与能力使用审计。
- Rejection checks: 不改active CSV或作者源；不改submission布局；不重新编译；不执行合并、删除、正文压缩、Figure裁决、Supplement迁移或GPT6裁决。
- Validation commands: 写前/写后active SHA比较；archive-active SHA逐项比较；manifest schema/count/path检查；作者源与submission写前/写后SHA比较；两阶段审查；`stage_guard.py`与限定`git diff --check`。

## Review Gates

1. Spec compliance: 14张表均有精确来源、RQ/claim、split与唯一主分类；valid/test逐表裁决；RQ1-RQ5最小证据与三套方案齐全。
2. Quality and isolation: bootstrap与multiseed的不确定性角色不混同；压缩优先移动raw detail而非科学维度；归档不可变且active、作者源和submission零修改。
