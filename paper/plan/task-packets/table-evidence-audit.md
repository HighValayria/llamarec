# Table Evidence Audit and Pre-Compression Archive

本审计依据当前14页English PDF、generated manifest/aux、14份active CSV和作者源引用。占页为120 dpi整页渲染的近似视觉估计，只用于比较方案。

## A. Current Table Inventory

| PDF / ID / source | Section / RQ | Primary and secondary claim | Split / seed / protocol / metrics | Page footprint | Redundancy |
| --- | --- | --- | --- | --- | --- |
| I / datasets / datasets.csv | Setup / all | Y/N与MovieLens/Amazon样本范围；外部证据边界 | train-valid-test counts / dataset-level | p4, ~0.16 page | Methods复述多数计数 |
| II / training_exposure / training_exposure.csv | Setup / RQ2,3,5 | 曝光定义、M1每任务对齐、SASRec比较基础 | no eval split / all runs / steps,batch,total,Y,N exposure | p5, ~0.22 | constant batch和零列冗长 |
| III / binary_exposure / binary_exposure.csv | Results / RQ1,2,3 | Y-native能力与有限/不均匀曝光响应 | valid+test / seed42 / 24k-96k+M1 / AUC,F1,Acc | p6, ~0.20 | 与VI/VII的96k值及正文重叠 |
| IV / semantics_bridge / semantics_bridge.csv | Results / RQ1,2 | Y-as-ranker与N-native能力差异；Y bridge弱响应 | valid+test / seed42 PopMatch-k5 / HR,NDCG,MRR | p6, ~0.17 | 可与III做双panel |
| V / exposure_scaling / exposure_scaling.csv | Results / RQ2,3 | N持续改善；validation gap收窄而test仍有gap | valid+test / seed42 k5 / 24k-200k / 3 metrics | p6, ~0.27 | Figure1仅重复validation N；VI/VII重叠96k |
| VI / ms96_main_validation / ms96_main_validation.csv | Results / RQ3 | 三seed 96k Y/M与N/M validation raw values | validation / train seeds42-44 / binary+k5 / 12 metric cols | p8, ~0.12 | IX摘要delta，VIII给seed42 CI |
| VII / ms96_main_test / ms96_main_test.csv | Results / RQ3 | 三seed frozen-test Y preservation与N modest gap raw values | test / train seeds42-44 / binary+k5 | p8, ~0.12 | IX摘要delta，X含seed42 k5 CI |
| VIII / specialist_multitask / specialist_multitask.csv | Results / RQ3 | seed42 Y-side preservation与k5 uncertainty | validation / paired bootstrap / 6 metrics delta+CI | p8, ~0.16 | IX是training-run variability，不能替代 |
| IX / ms96_delta_summary / ms96_delta_summary.csv | Results / RQ3,4 | 三seed mean+sample SD，binary/k5/k20/k50双split | valid+test / seeds42-44 / 3 metrics | p9, ~0.70 | 摘要VI/VII/XI/XII；正文复述headline |
| X / hard_candidate / hard_candidate.csv | Results / RQ3,4 | seed42 paired CI随k5/k20/k50变化 | valid+test / seed42 / non-nested protocols / 3 metrics | p10, ~0.48 | seed42 point values与XI/XII重叠，CI独有 |
| XI / ms96_protocol_validation / ms96_protocol_validation.csv | Results / RQ4 | 三seed各协议validation raw grid | validation / train seeds42-44,candidate seed42 / N,M,delta x3 | p10, ~0.18 | IX mean/SD，X seed42 CI |
| XII / ms96_protocol_test / ms96_protocol_test.csv | Results / RQ3,4 | 三seed各协议frozen-test raw grid | test / train seeds42-44,candidate seed42 / N,M,delta x3 | p11, ~0.18 | IX mean/SD，X seed42 CI |
| XIII / n_vs_sasrec_exposure / n_vs_sasrec_exposure.csv | Results / RQ5 | N四点领先，同时SASRec随曝光改善 | valid+test / seed42 k5 / exact exposure+HR | p11, ~0.23 | Figure2仅重复validation HR |
| XIV / cross_dataset / cross_dataset.csv | Cross-dataset / external RQ1,3,5 | Amazon早期seed42 test ranking方向复现 | test only / PopMatch-k5 / HR,NDCG,MRR | p11, ~0.09 | 正文复述较多，但表已很小 |

## B. Claim-to-Table Map

| RQ | Minimum claim and evidence | Necessary split / seed / metrics / protocol | Optional detail |
| --- | --- | --- | --- |
| RQ1 | compact III+IV：Y-native与Y-as-ranker/N-native回答不同预测问题 | Y validation trajectory + Y96/N96 held-out endpoints；seed42；binary 3 metrics，ranking HR primary+NDCG consistency；native Y+k5 | full bridge test trajectory |
| RQ2 | compact III/IV + V；II定义曝光 | validation用于trajectory，test确认方向；seed42 full trajectory；Y native metrics、N HR headline+NDCG/MRR trend；k5 | repeated Y test rows；Figure1 complementary |
| RQ3 | V + VIII + compact IX：Y preservation、validation narrowing、test modest N gap | both splits但角色不同；3 seeds at96k，seed42 trajectory/bootstrap；binary+k5 all metrics | raw VI/VII |
| RQ4 | compact IX + compact X：protocol-conditioned gap | both splits；3-seed mean/SD与seed42 paired CI分开；HR headline，NDCG/MRR方向/CI状态；non-nested k5/k20/k50 | raw XI/XII |
| RQ5 | XIII：四个matched exposure下N>SASRec且gap收窄 | both splits；seed42；HR required；PopMatch-k5 | source-only NDCG/MRR；Figure2 |

I与II是共享方法证据；XIV是有边界的外部方向支撑，不是完整trajectory replication。

## C. Valid/Test Role Audit

| PDF | Decision | Reason |
| --- | --- | --- |
| I | BOTH | 三个split计数共同界定数据与held-out规模。 |
| II | NOT_APPLICABLE | 训练曝光表没有评估split。 |
| III | SUMMARY_BOTH | validation给Y trajectory；test保留endpoint/consistency，不必保留每个test row。 |
| IV | SUMMARY_BOTH | validation给bridge trajectory；test给Y96/N96 held-out contrast。 |
| V | BOTH | validation narrowing与retained test gap是不同科学结论。 |
| VI | RAW_TO_SUPPLEMENT | validation raw可审计，main minimum由VIII/IX承担。 |
| VII | RAW_TO_SUPPLEMENT | test结论留main summary，raw absolute values后移。 |
| VIII | VALID_ONLY | 回答明确的seed42 validation bootstrap问题，不冒充test。 |
| IX | SUMMARY_BOTH | 核心价值正是并列validation与test的不同结论。 |
| X | BOTH | RQ4使用两个split的seed42 CI。 |
| XI | RAW_TO_SUPPLEMENT | IX/X的validation底层detail。 |
| XII | RAW_TO_SUPPLEMENT | IX/X的test底层detail。 |
| XIII | BOTH | validation指导运行点，frozen test评估已选点。 |
| XIV | TEST_ONLY | Amazon证据仅为full-test directional support。 |

不存在全局“只留test”规则。V、IX、X、XIII必须双split；III/IV摘要式双split；raw split表VI/VII/XI/XII适合后移。

## D. Per-Table Verdict

| PDF | Verdict | Minimum form / field necessity | Archive | Future identity |
| --- | --- | --- | --- | --- |
| I | CORE_MAIN | 4个dataset-task行与train/valid/test都界定范围，体量已小 | archived | unchanged |
| II | COMPACT_MAIN | run,total,Y,N exposure必要；batch=8可进caption；steps与total可按复现性取舍但不能丢M1总/每任务区别 | YES | training_exposure_compact.csv |
| III | COMPACT_MAIN | exposure,split,AUC/F1/Acc必要；seed常量进caption；test保留关键端点 | YES | binary_exposure_compact.csv |
| IV | MERGE_CANDIDATE | 保留Y bridge validation trajectory和Y96/N96双split endpoint，与III分panel不跨量纲 | YES | supervision_semantics_compact.csv |
| V | CORE_MAIN | trajectory、M1 matched points、双split、三指标共同支撑RQ2/3 | archived | unchanged |
| VI | SUPPLEMENT_CANDIDATE | raw三seedabsolute values有审计价值，main可用IX+VIII | YES | ms96_native_summary_compact.csv |
| VII | SUPPLEMENT_CANDIDATE | held-out summary必须留main，raw grid后移 | YES | ms96_native_summary_compact.csv |
| VIII | CORE_MAIN | 6行分别覆盖Y三指标和k5三指标CI，体量小且证据类型独立 | archived | unchanged |
| IX | COMPACT_MAIN | split,protocol,metric,mean,SD必要；n/ddof进caption；可HR headline并显式保留其他metrics方向 | YES | ms96_delta_summary_compact.csv |
| X | COMPACT_MAIN | protocol,split,HR delta+CI核心；NDCG/MRR必须保留CI方向状态或full supplement | YES | hard_candidate_compact.csv |
| XI | SUPPLEMENT_CANDIDATE | validation raw grid主要是IX/X底层detail | YES | ms96_protocol_summary_compact.csv |
| XII | SUPPLEMENT_CANDIDATE | test raw grid后移；seed43 k5/k50非单调检查点须在compact summary或正文可核查 | YES | ms96_protocol_summary_compact.csv |
| XIII | CORE_MAIN | exact exposure、双split、HR均必要；source的NDCG/MRR不必扩进当前表 | archived | unchanged |
| XIV | CORE_MAIN | 5 models、test、3 metrics和samples匹配directional claim，且已很小 | archived | unchanged |

计数：CORE_MAIN 5，COMPACT_MAIN 4，MERGE_CANDIDATE 1，SUPPLEMENT_CANDIDATE 4，REDUNDANT_MAIN 0。后四张仍有raw追溯价值，所以应后移而不是称为可删除。

## E. Redundancy Graph

| A | B | Type | Boundary |
| --- | --- | --- | --- |
| III | VI/VII | RAW_vs_SUMMARY | 96k seed42重叠；III有trajectory，VI/VII有multiseed absolute values。 |
| III | IV | SAME_METRIC_DIFFERENT_VIEW | 可同表分panel；native binary与bridge ranking不可跨量纲合并。 |
| V | Figure1 | TABLE_vs_FIGURE | Figure仅validation N；V还含test、M1、3 metrics。 |
| V | VI/VII | RAW_vs_SUMMARY | 96k seed42重叠；trajectory与multiseed角色不同。 |
| VI/VII | IX | RAW_vs_SUMMARY | per-seed absolute values vs delta mean/SD。 |
| VI/VII | VIII/X | BOOTSTRAP_vs_MULTISEED | 固定模型的评估样本不确定性不等于训练运行变异。 |
| XI/XII | IX | RAW_vs_SUMMARY | protocol raw vs mean/SD。 |
| XI/XII | X | BOOTSTRAP_vs_MULTISEED | seed42 CI与三seedraw不能互换。 |
| IX/X | Results prose | TABLE_vs_PROSE | prose仅重复headline，表维持完整维度。 |
| XIII | Figure2 | TABLE_vs_FIGURE | Figure仅validation；XIII含test和exact matching。 |
| XIV | prose | TABLE_vs_PROSE | prose重复较多，但小表是直接证据。 |

## F. Proposed Compact/Merge Designs

仅规划命名，不创建future scientific tables。

1. `training_exposure_compact.csv`: run,total,Y,N；batch常量进caption。
2. `supervision_semantics_compact.csv`: III/IV双panel；Y validation trajectory + Y96/N96 held-out endpoints，指标不跨panel比较。
3. `ms96_native_summary_compact.csv`: 按split/task给三seeddelta mean/SD、方向计数和必要absolute anchor；raw仍归档。
4. `ms96_delta_summary_compact.csv`: binary与k5/k20/k50分panel，valid/test并列；caption统一n=3,ddof=1。
5. `hard_candidate_compact.csv`: protocol/split保留HR delta+CI，增加NDCG/MRR CI方向字段；full 18 rows后移。
6. `ms96_protocol_summary_compact.csv`: 方向计数、range和非单调检查点；绝不覆盖XI/XII。

## G. T-LIGHT

- Main tables: 12；compact: 2（IX/X）；merge: 0；supplement: XI/XII。
- Estimated saving: 0.8-1.4 pages。
- Retains: 五RQ、VI/VII raw native、两类uncertainty、双split均即时可见。
- Moves: protocol raw grid。Risk: 页数改善有限，VI/VII与IX仍raw-summary重复。

## H. T-BALANCED

- Main tables: 9，即I、II compact、III/IV merged、V、VIII、IX compact、X compact、XIII、XIV。
- Compact: 4；merge: III+IV；supplement candidates: VI/VII/XI/XII及full IX/X。
- Estimated saving: 1.8-2.8 pages。
- Retains: RQ1-RQ5所需task,split,seed,protocol,metric,uncertainty维度。
- Moves: 96k absolute per-seed grids和逐seed逐协议完整值。
- Risk: IX/X必须清楚区分multiseed SD与seed42 bootstrap，并保留其他metrics的一致性证据。

## I. T-AGGRESSIVE

- Main tables: 6：dataset、exposure accounting、III/IV/V capability-exposure、VIII/IX/X 96k evidence、XIII、XIV，均compact。
- Compact: 6；merge: two groups；supplement: most raw/full versions。
- Estimated saving: 2.8-4.0 pages。
- Retains: 理论上保留五RQ headline；moves: 多数raw、secondary metrics和部分split detail。
- Risk: 高，可能压平task量纲、valid/test张力或混淆两类uncertainty；仅在真实硬页限下考虑。

## J. Supplement-Allowed Branch

采用T-BALANCED。主文9表独立支撑五RQ；VI/VII/XI/XII和full IX/X进supplement，并绑定本archive SHA。Supplement增加raw审计深度，不承担主文claim成立所必需的信息。

## K. Supplement-Unavailable Branch

仍可用9表，但compact IX必须保留split,protocol,headline mean/SD、三seed方向或range；compact X必须保留HR CI与NDCG/MRR CI方向。VI/VII/XI/XII只永久archive、不提交。主文所有claim必须不依赖未提交材料。

## L. Archive Manifest

`paper/archive/tables/pre_compression_2026-09-10/`包含14/14 byte-for-byte CSV副本、`manifest.json`和写边界`metadata/baseline.json`。Archive是copy不是move，位于build输出之外；active path不重定向。未来compact/merge使用新identity，旧表即使不再引用也不删除。

## M. Recommendation

推荐`T-BALANCED`：优先后移raw detail，不减少科学维度。它需要选择性同时保留validation/test：V、IX、X、XIII为BOTH；III/IV为SUMMARY_BOTH；VIII保持VALID_ONLY；XIV保持TEST_ONLY。若supplement不可用，compact IX/X必须自足。本轮未创建future table，未执行merge/delete/move，未改正文、Figure、active CSV或submission layout。

## Review and Verification

- Spec review: PASS。14张表均有source、表号、RQ/claim、split裁决、唯一主分类、future identity和archive要求；RQ1-RQ5 minimum evidence、三档方案及supplement双分支齐全。
- Quality review: PASS。方案明确区分validation选择/trajectory与frozen-test held-out角色，也明确区分三seed sample SD与seed42 paired bootstrap；推荐依据是minimum defensible evidence而非表数最少。
- Archive verification: 14/14 CSV存在，active/archive/manifest SHA256逐项一致，行列数一致。
- Isolation verification: 37份manuscript author source整体SHA256仍为`2f208cb1f9d8a8db16e5f1aac81d2d8a10a25056105e67b975bd55d33aec5e9b`；10份submission adapter文件整体SHA256仍为`39028b9a54081568ce4e8298feeba91bd9c85e5406adc33fcc7d65b6e0c368a9`。
