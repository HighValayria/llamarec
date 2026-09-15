# 论文证据层

`source_of_truth.md` 记录事实和原始来源优先级；`claim_matrix.md` 把段落与允许措辞对应；`pending_evidence.md` 记录未纳入证据，A/B/C 分支统一维护于 `ms96_integration_plan.md`。此层不是新实验结果仓库。

表格由冻结 CSV/JSON 提取，保留 split、seed、接口和曝光口径。验证集用于模型选择和训练决策，冻结 test 完整报告并参与最终解释；这一区别是选择纪律，不是证据等级。发现汇总与实现不一致时记录具体冲突，采用更直接的来源或保留未决，不能静默补全。

本次文字修订见 `narrative_revision_log.md`、`defensive_language_audit.md` 和 `paragraph_quality_audit.md`。审计层可以详细记录限制，但正文按发现、意义、必要边界组织，不直接复制审计语气。
