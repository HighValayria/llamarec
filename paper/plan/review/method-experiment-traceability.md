# 方法与证据对应

| 实证论点 | 方法段落 | 现有对照 | 图表 | 允许结论 |
| --- | --- | --- | --- | --- |
| 监督语义 | problem.*; methods.task.* | Y binary / Y-as-ranker / N | semantics_bridge; binary_exposure | 目标与观察到的能力不同 |
| 曝光响应 | methods.exposure.* | Y24/48/96; N24/48/96/200 | binary_exposure; Figure 1; n_vs_sasrec_exposure | seed42被测范围内的task-native趋势 |
| 条件性统一 | methods.training.*; methods.evaluation.* | Y96/M1-Y；common cross-task-safe N48/96与M1-N | specialist_multitask; exposure_scaling; ms96_delta_summary_compact; hard_candidate_compact | seed42 validation 48→96k三指标收窄；test不收窄；三seed96k小幅N优势；Y侧能力保留 |
| 协议鲁棒性 | methods.evaluation.* | cross-task-safe N96/M1-N的k5/k20/k50 | ms96_delta_summary_compact | 96k三seed的k20差距最大、k5/k50较小；非候选大小因果 |
| SASRec 定位 | methods.baseline.* | N 与 S47/94/188/391 | n_vs_sasrec_exposure | 样本曝光条件化比较 |
| 外部方向 | methods.datasets.* | Amazon 旧 seed42 ranking | cross_dataset | 部分外部方向，无完整复现 |
