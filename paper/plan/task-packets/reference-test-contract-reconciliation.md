# Reference / Test Contract Reconciliation

## Task Packet
- Scope: 补齐S26-S31既有来源核验记录；让citation-position scanner按manifest扫描全部正式模块；保留两份历史hash baseline并新增版本化current manuscript contract。
- Files to read: references四项；`paper/assembly/tests/`；manifest；两个旧baseline；final readiness audit。
- Files allowed to edit: `paper/references/primary_source_notes.md`、必要的assembly tests/helper、新current contract、本任务包、`.agent/current_task.md`、`.agent/stage_state.yaml`及最小测试说明。
- Required skills: using-research-writing、paper-orchestration、peer-review、verification。
- Evidence inputs: 当前citation registry、BibTeX、claim map与已核官方来源记录；manifest正式模块顺序；写前作者源和历史baseline哈希。
- Rejection checks: 不联网；不改modules/modules_parts；不删registry/citation/assert；不覆盖旧hash；不把旧snapshot重定义为current；不处理draft/模板。
- Validation: 完整47项unittest、双语check、stage_guard、限定diff-check；S26-S31/Methods citation/module范围/旧baseline字节/新contract身份/作者源零修改专项检查。

## Stage
S5 Review。只修复reference/test repository contract，不修改论文科学内容。
