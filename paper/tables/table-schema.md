# 图表数据契约

| 稳定 ID | 目的 | 数据源与生成规则 | 展示规则 |
| --- | --- | --- | --- |
| datasets | 任务级数据规模 | state_reconstruction/dataset_comparison.md 与 Amazon stats；人工转录四行 | Y/N分别，不能将目标数当用户数 |
| training_exposure | 单任务/多任务预算 | training_protocol_comparison 与冻结别名；列步数和曝光 | M1每任务计数为预期；正文保留resume假设 |
| binary_exposure | Y 与 M-Y 原生表现 | exposure_main_table.csv，JSON secondary_metrics 展开 | seed42；validation/test分别；原数值保留 |
| semantics_bridge | Y-as-ranker 与 N | 同上；Y24/48/96桥接与N96排序 | 相同候选协议内比较；不混合AUC与HR尺度 |
| exposure_scaling | seed42共同cross-task-safe子集上的M1-48/96 k5曝光关系 | `m1-common-clean-exposure-verification.csv`机械重排 | 两个曝光点使用同一validation/test样本；只报point estimates与gap change |
| specialist_multitask | Y96与M1-Y96配对差与CI | 既有`specialist_multitask.csv`仅筛取Y侧三行 | 只支撑seed42 validation二分类Y侧比较，不支撑M1-N ranking |
| ms96_delta_summary_compact | 96k三seed cross-task-safe N-M1排序差值 | `clean_multiseed_96_summary.csv`机械重排 | 18行含两split、三协议、三指标；mean/sample SD/signs，非CI |
| hard_candidate_compact | M1-48/96 cross-task-safe subset覆盖率 | common-safe机器证据中的四组计数 | evaluation-side restriction；N与M1-N同一保留样本 |
| n_vs_sasrec_exposure | SASRec样本曝光对齐 | 主表与sasrec_exposure_alignment.csv按run/split连接 | 不插值；实际曝光；正文表展示HR，CSV保留NDCG/MRR |
| cross_dataset | Amazon方向 | seed42_result_summary.json的PopMatch ranking字段 | 只有test/seed42；不引入binary输出 |

原始精度保留于 CSV，Markdown 表一般显示五位小数，正文主要指标四位、delta/CI五位。`asset_provenance.json` 记录自动导出源与目标 hash；datasets/training_exposure 是人工维护表，单独按上述来源核验。空缺不能写成零；模型没有该接口时不生成伪指标。没有完整三 seed 时不生成 mean/std 行。

## MS96新增表契约

| 稳定ID | 行数/用途 | 来源 | 展示与限制 |
| --- | --- | --- | --- |
| ms96_main_validation | 3行seed，12个原生指标 | seed42冻结CSV；43/44 validation_summary | Y96、M1-Y、N96、M1-N分列；不混Y-as-ranker；M总192k、每任务预期96k |
| ms96_main_test | 3行seed，12指标 | 对应test_summary及seed42冻结CSV | 决策冻结后仅报告，与validation分表 |
| ms96_protocol_validation | 9行seed×k5/k20/k50 | 原protocol CSV及43/44 validation_summary | N/M/差值，HR/NDCG/MRR全保留；候选seed42不是训练seed |
| ms96_protocol_test | 9行seed×协议 | 对应test数据 | 同上，held-out report-only |
| ms96_delta_summary | 24行split×接口协议×指标 | 72条相同seed内差值 | 等权mean、sample std、ddof=1、n=3；非CI，不替代raw |

数据由analysis/ms96_evidence.py定向解析，仅汇总现有指标；--check只读。ms96_raw_metrics.csv含来源，ms96_per_seed_deltas.csv保留全部差值。新MS96 provenance独立记录，不覆盖旧asset_provenance或原seed42 CI。源summary与validation_summary重复不双计；M1的samples属于Y，不当成排序目标数。未新增图，既有图仍只描绘seed42轨迹。
