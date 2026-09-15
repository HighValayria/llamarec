# MS96 证据整合摘要

日期：2026-09-08。状态：MS96 INTEGRATED；Y96_STATUS RESOLVED。本文是现有证据整理，不包含训练、推理、预测指标重算、重采样或新统计检验。

## 1. 来源与核验层级
seed42 使用本地冻结的 [exposure_main_table.csv](../../.agent/exposure_scaling/final_evidence/exposure_main_table.csv)、[specialist bootstrap](../../.agent/exposure_scaling/final_evidence/tables/table_specialist_multitask.csv) 与 [protocol bootstrap](../../.agent/exposure_scaling/final_evidence/tables/table_hard_candidate.csv)。
seed43/44 来源为 Git 提交 `a9c6cd959cf32afe046bb05be9eb5096bebfc5fb` 的 `artifacts/multiseed96/seed43` 和 `seed44`。八份文本导入 [本地只读副本](../../.agent/ms96_integration/imported/a9c6cd9/artifacts/multiseed96/)；通过 `git hash-object --path` 核对八份导入文件，规范化后的 blob 全部与提交一致。归档导出有 CRLF 转换，不声称本地字节与 Git blob 完全相同。
每 seed 只使用 validation_summary 与 test_summary；summary 与 validation_summary 相同，不作为第二次运行。artifact_index 只提供远端产物路径，未下载其中完整 metrics.json、checkpoint 或执行参数，不能据此关闭 RUN_METADATA。逐源 SHA256 见 [数据来源清单](ms96_data_provenance.json)。

本次程序只解析144条原生任务指标，计算72条差值及24组均值/样本标准差。Y96 汇总中的排序字段属于 Y-as-ranker 桥接，保留在导入原文件，不混入 N-native。M1 的12381/11544 samples 对应 Y binary，不是 M-N 排序样本数；43/44排序均为5675。seed42所用汇总不列样本数，正规化表留空而非补零。

## 2. Validation 与 Frozen Test
validation 指导模型选择和实验决策；决策冻结后，test 是仅报告的最终留出泛化证据，不用于选模型，也不降格为“次要证据”。下表分开报告，不能混合两个 split 或把同一评估集在三个训练 seed 下当作三份独立用户样本。

### Validation 原始点估计
| seed | Y96_AUC | Y96_F1 | Y96_Accuracy | M1-Y_AUC | M1-Y_F1 | M1-Y_Accuracy | N96_HR@1 | N96_NDCG@5 | N96_MRR | M1-N_HR@1 | M1-N_NDCG@5 | M1-N_MRR |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 42 | 0.78435 | 0.77832 | 0.72353 | 0.78684 | 0.78384 | 0.72813 | 0.62379 | 0.83029 | 0.77324 | 0.62344 | 0.82914 | 0.77175 |
| 43 | 0.77909 | 0.78324 | 0.72215 | 0.78812 | 0.78689 | 0.72845 | 0.62802 | 0.83216 | 0.77572 | 0.62537 | 0.83039 | 0.77340 |
| 44 | 0.78217 | 0.78002 | 0.72401 | 0.78512 | 0.78448 | 0.72312 | 0.63524 | 0.83451 | 0.77896 | 0.62062 | 0.82911 | 0.77162 |

### Frozen Test 原始点估计
| seed | Y96_AUC | Y96_F1 | Y96_Accuracy | M1-Y_AUC | M1-Y_F1 | M1-Y_Accuracy | N96_HR@1 | N96_NDCG@5 | N96_MRR | M1-N_HR@1 | M1-N_NDCG@5 | M1-N_MRR |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 42 | 0.78535 | 0.77802 | 0.72211 | 0.78648 | 0.78356 | 0.72713 | 0.61004 | 0.82190 | 0.76220 | 0.59736 | 0.81623 | 0.75465 |
| 43 | 0.78150 | 0.77858 | 0.71708 | 0.78497 | 0.78454 | 0.72523 | 0.61392 | 0.82371 | 0.76462 | 0.60617 | 0.81914 | 0.75861 |
| 44 | 0.78027 | 0.77698 | 0.71873 | 0.78571 | 0.78752 | 0.72696 | 0.61057 | 0.82207 | 0.76244 | 0.60053 | 0.81727 | 0.75606 |

CSV 保留来源可用精度：[验证主表](../tables/ms96_main_validation.csv)、[测试主表](../tables/ms96_main_test.csv)、[逐指标与来源](ms96_raw_metrics.csv)。此处五位小数只用于显示。M1-96总曝光192k、每任务预期96k；专家96k，非总计算量对齐。

## 3. Y 侧差值
定义：M1-Y - Y96。
| seed | split | metric | delta |
| --- | --- | --- | --- |
| 42 | validation | AUC | 0.00248 |
| 42 | validation | F1 | 0.00553 |
| 42 | validation | Accuracy | 0.00460 |
| 43 | validation | AUC | 0.00903 |
| 43 | validation | F1 | 0.00365 |
| 43 | validation | Accuracy | 0.00630 |
| 44 | validation | AUC | 0.00295 |
| 44 | validation | F1 | 0.00447 |
| 44 | validation | Accuracy | -0.00089 |
| 42 | test | AUC | 0.00113 |
| 42 | test | F1 | 0.00554 |
| 42 | test | Accuracy | 0.00502 |
| 43 | test | AUC | 0.00346 |
| 43 | test | F1 | 0.00596 |
| 43 | test | Accuracy | 0.00814 |
| 44 | test | AUC | 0.00544 |
| 44 | test | F1 | 0.01054 |
| 44 | test | Accuracy | 0.00823 |

总体相近或略高，三 seed 的 test AUC/F1/Accuracy 全部 M1 稍高。seed44 validation Accuracy 为0.7231241418对0.7240126000，差值-0.0008884581；因此不能说两个split的每项指标均提高。只支持保留被测偏好表现，不支持正迁移或跨seed显著提升。

## 4. Standard k5 差值
定义：N96 - M1-N。三个 seed、两个 split、三个指标均为正。
| seed | split | metric | delta |
| --- | --- | --- | --- |
| 42 | validation | HR@1 | 0.00035 |
| 42 | validation | NDCG@5 | 0.00115 |
| 42 | validation | MRR | 0.00149 |
| 43 | validation | HR@1 | 0.00264 |
| 43 | validation | NDCG@5 | 0.00177 |
| 43 | validation | MRR | 0.00231 |
| 44 | validation | HR@1 | 0.01463 |
| 44 | validation | NDCG@5 | 0.00540 |
| 44 | validation | MRR | 0.00734 |
| 42 | test | HR@1 | 0.01269 |
| 42 | test | NDCG@5 | 0.00567 |
| 42 | test | MRR | 0.00755 |
| 43 | test | HR@1 | 0.00775 |
| 43 | test | NDCG@5 | 0.00457 |
| 43 | test | MRR | 0.00601 |
| 44 | test | HR@1 | 0.01004 |
| 44 | test | NDCG@5 | 0.00481 |
| 44 | test | MRR | 0.00638 |

采用 small-gap regime 与 modest N-specialist advantage，不采用 parity/equivalence。完整曝光轨迹仅 seed42：验证 HR@1 gap 从48k的0.0088105727降至96k的0.0003524230；test gap 却由0.0093392070变为0.0126872247，不能把“48→96k收窄”推广到 test。43/44只有96k，不验证各自48→96k变化。

## 5. 候选协议原始结果及差值
### Validation
| seed | protocol | N_HR@1 | M_HR@1 | delta_HR@1 | N_NDCG@5 | M_NDCG@5 | delta_NDCG@5 | N_MRR | M_MRR | delta_MRR |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 42 | k5 | 0.62379 | 0.62344 | 0.00035 | 0.83029 | 0.82914 | 0.00115 | 0.77324 | 0.77175 | 0.00149 |
| 42 | k20_seed42 | 0.38907 | 0.27665 | 0.11242 | 0.52098 | 0.39400 | 0.12698 | 0.52489 | 0.41863 | 0.10626 |
| 42 | k50_seed42 | 0.09586 | 0.07877 | 0.01709 | 0.13444 | 0.10549 | 0.02896 | 0.18514 | 0.15932 | 0.02583 |
| 43 | k5 | 0.62802 | 0.62537 | 0.00264 | 0.83216 | 0.83039 | 0.00177 | 0.77572 | 0.77340 | 0.00231 |
| 43 | k20_seed42 | 0.27700 | 0.19559 | 0.08141 | 0.37972 | 0.25331 | 0.12640 | 0.41528 | 0.32401 | 0.09127 |
| 43 | k50_seed42 | 0.07859 | 0.07524 | 0.00335 | 0.09854 | 0.09387 | 0.00468 | 0.15669 | 0.14503 | 0.01166 |
| 44 | k5 | 0.63524 | 0.62062 | 0.01463 | 0.83451 | 0.82911 | 0.00540 | 0.77896 | 0.77162 | 0.00734 |
| 44 | k20_seed42 | 0.24529 | 0.19419 | 0.05110 | 0.35099 | 0.24505 | 0.10594 | 0.38996 | 0.32282 | 0.06714 |
| 44 | k50_seed42 | 0.07947 | 0.06907 | 0.01040 | 0.10061 | 0.09068 | 0.00993 | 0.15984 | 0.14183 | 0.01801 |

### Frozen Test
| seed | protocol | N_HR@1 | M_HR@1 | delta_HR@1 | N_NDCG@5 | M_NDCG@5 | delta_NDCG@5 | N_MRR | M_MRR | delta_MRR |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 42 | k5 | 0.61004 | 0.59736 | 0.01269 | 0.82190 | 0.81623 | 0.00567 | 0.76220 | 0.75465 | 0.00755 |
| 42 | k20_seed42 | 0.37586 | 0.26115 | 0.11471 | 0.50144 | 0.37551 | 0.12593 | 0.50991 | 0.40405 | 0.10587 |
| 42 | k50_seed42 | 0.08300 | 0.06907 | 0.01392 | 0.12531 | 0.09753 | 0.02778 | 0.17461 | 0.15119 | 0.02342 |
| 43 | k5 | 0.61392 | 0.60617 | 0.00775 | 0.82371 | 0.81914 | 0.00457 | 0.76462 | 0.75861 | 0.00601 |
| 43 | k20_seed42 | 0.26890 | 0.19718 | 0.07172 | 0.37104 | 0.24885 | 0.12219 | 0.40697 | 0.32063 | 0.08635 |
| 43 | k50_seed42 | 0.06767 | 0.06256 | 0.00511 | 0.09063 | 0.08626 | 0.00437 | 0.14795 | 0.13633 | 0.01163 |
| 44 | k5 | 0.61057 | 0.60053 | 0.01004 | 0.82207 | 0.81727 | 0.00481 | 0.76244 | 0.75606 | 0.00638 |
| 44 | k20_seed42 | 0.23736 | 0.19084 | 0.04652 | 0.33997 | 0.23879 | 0.10117 | 0.38051 | 0.31716 | 0.06335 |
| 44 | k50_seed42 | 0.07048 | 0.05921 | 0.01128 | 0.09360 | 0.08350 | 0.01010 | 0.15332 | 0.13465 | 0.01866 |

完整精度：[验证协议表](../tables/ms96_protocol_validation.csv)、[测试协议表](../tables/ms96_protocol_test.csv)。
k20 在所有seed、split、指标上均 N>M，而且差值均大于相同seed/split/指标的k5差值。k50方向相同、差值均小于k20，幅度随seed变化，但并不总大于k5：seed43 test HR差值0.00511小于k5的0.00775；seed44 validation HR差值0.01040小于k5的0.01463。test平均HR差值k50为0.01010，略小于k5的0.01016。
“more seed-sensitive”若被理解为绝对标准差更大并不成立：k50 HR差值绝对SD小于k20。因此正文采用“smaller gap with seed-dependent magnitude”，不作无定义的变异大小比较。

k5为popularity-matched、5候选；k20/k50为random、20/50候选；候选生成seed均42，与训练seed42/43/44分开。三个集合非嵌套，数量、组成、采样方法与难度共同变化。用户给出嵌套比例0、0、约0.000176；本次Git轻量包未见独立audit原件，精确比例仅标作用户提供，正文不引用为本轮独立核验值。

## 6. 三训练 Seed 描述统计
所有组n=3、等权；标准差为sample std、ddof=1，不是CI或显著性。delta先在相同seed内计算，再跨seed汇总；不池化用户预测，不替代原始逐seed值。
| split | protocol | metric | mean | sample_std | n | ddof |
| --- | --- | --- | --- | --- | --- | --- |
| validation | binary | AUC | 0.00482 | 0.00365 | 3 | 1 |
| validation | binary | F1 | 0.00455 | 0.00094 | 3 | 1 |
| validation | binary | Accuracy | 0.00334 | 0.00376 | 3 | 1 |
| validation | k5 | HR@1 | 0.00587 | 0.00767 | 3 | 1 |
| validation | k5 | NDCG@5 | 0.00277 | 0.00230 | 3 | 1 |
| validation | k5 | MRR | 0.00371 | 0.00316 | 3 | 1 |
| validation | k20_seed42 | HR@1 | 0.08164 | 0.03066 | 3 | 1 |
| validation | k20_seed42 | NDCG@5 | 0.11977 | 0.01199 | 3 | 1 |
| validation | k20_seed42 | MRR | 0.08822 | 0.01974 | 3 | 1 |
| validation | k50_seed42 | HR@1 | 0.01028 | 0.00687 | 3 | 1 |
| validation | k50_seed42 | NDCG@5 | 0.01452 | 0.01277 | 3 | 1 |
| validation | k50_seed42 | MRR | 0.01850 | 0.00710 | 3 | 1 |
| test | binary | AUC | 0.00334 | 0.00216 | 3 | 1 |
| test | binary | F1 | 0.00735 | 0.00277 | 3 | 1 |
| test | binary | Accuracy | 0.00713 | 0.00183 | 3 | 1 |
| test | k5 | HR@1 | 0.01016 | 0.00247 | 3 | 1 |
| test | k5 | NDCG@5 | 0.00501 | 0.00058 | 3 | 1 |
| test | k5 | MRR | 0.00665 | 0.00081 | 3 | 1 |
| test | k20_seed42 | HR@1 | 0.07765 | 0.03448 | 3 | 1 |
| test | k20_seed42 | NDCG@5 | 0.11643 | 0.01335 | 3 | 1 |
| test | k20_seed42 | MRR | 0.08519 | 0.02128 | 3 | 1 |
| test | k50_seed42 | HR@1 | 0.01010 | 0.00452 | 3 | 1 |
| test | k50_seed42 | NDCG@5 | 0.01408 | 0.01220 | 3 | 1 |
| test | k50_seed42 | MRR | 0.01790 | 0.00593 | 3 | 1 |

完整精度见 [描述统计表](../tables/ms96_delta_summary.csv)。程序 [ms96_evidence.py](../analysis/ms96_evidence.py) 的 `--check` 可只读核验生成值。seed42 k5原点保留到10位小数，因此重算差值与原bootstrap点差可能在约1e-10末位不同；不覆盖原delta/CI。

## 7. 已有 Seed42 Bootstrap
仅复用冻结区间，不生成新bootstrap。Y validation 的AUC/F1/Accuracy差值区间分别为[-0.00167,+0.00674]、[+0.00096,+0.01025]、[-0.00089,+0.01035]；只有F1区间为正。
k5 validation的HR/NDCG/MRR区间分别为[-0.01040,+0.01128]、[-0.00337,+0.00581]、[-0.00457,+0.00769]，均跨零；test三项均为正，其中HR为[+0.00159,+0.02379]。
k20/k50的seed42 validation/test三项区间全部为正，具体原值继续由原表展示。没有seed43/44 bootstrap，也没有新Y test bootstrap。

用户级配对bootstrap衡量一个已训练模型对的评估样本不确定性；三训练seed点估计与sample std描述训练运行间变异；validation/test是选择与留出角色。这三者不能互相替代。无等价界限、跨训练seed显著性检验或全比较多重性校正。原bootstrap预测与执行元数据缺口仍登记BOOTSTRAP_PROVENANCE。

## 8. 解释与未变边界
96k下，共享M1保留被测Y偏好表现，在标准k5进入小差距区间，N尤其在冻结test仍有小幅优势。两次额外独立训练复现的是这个运行点；“随曝光收窄”的证据仍来自seed42验证轨迹。k20显示小k5差距不能直接推广到其他候选协议；k50保持方向，但不支持随候选数单调增大的规律。
SASRec正式seed42系列保持S47/S94/S188/S391，对应实际24064/48128/96256/200000，与N24/N48/N96/N200近似匹配。本地冻结对齐CSV与inventory、远端artifact路径清单一致；未下载完整远端运行JSON，不将路径核对称为完整运行溯源复现。N在四点领先，SASRec改善且200k差距小于96k；不从旧seed43/44的s23或高曝光运行拼接正式轨迹。
Amazon仍为旧seed42的外部排序方向：Base约0.3573，Y-as-ranker约0.2298，N约0.4669，M约0.4582，matched SASRec约0.1757。未升级其原生偏好、完整曝光、hard协议或多seed证据。
冻结中心与层级保持C2主、C4次、C3支撑、C1界定；这里贡献编号与source_of_truth的finding编号各有原本含义，不混用。

## 9. 允许的正文措辞
- The seed42 trajectory shows substantial narrowing of the standard-k5 validation gap from 48k to 96k; two additional training seeds reproduce the 96k small-gap regime.
- At 96k, M1 maintains comparable Y-side preference performance across the evaluated seeds.
- Frozen held-out tests consistently retain a modest N-specialist advantage.
- Across all three evaluated training seeds, k20 reveals a substantially larger N-specialist advantage than standard k5.
- k50 also consistently favors N, but with a smaller gap than k20 and seed-dependent magnitude.
- These relationships are protocol-conditioned; the candidate protocols do not isolate candidate size.

## 10. 禁止的升级与审查处理
不写parity/equivalence/gap disappears/exactmatch；不写跨三seed提高曝光使差距收窄；不写positive transfer/significant improvement across seeds；不写所有alternative gap均大于k5、larger candidates cause larger gap或monotonic scaling；不写全轨迹或Amazon已获三seed验证；不写LLM普遍更省样本/计算/预训练公平或SASRec永不反超。
原冻结CSV的历史interpretation列包含parity，作为来源原文保持不动且不进入正文展示；当前证据解释以本文件与更新后的claim_matrix为准。原freeze正文保留，其末尾追加的MS96更新覆盖旧证据状态，不改变文献判断。
