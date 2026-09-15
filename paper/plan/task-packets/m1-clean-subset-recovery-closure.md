# M1 Clean-Subset Prediction Recovery Closure

日期：2026-09-11  
状态：`CLEAN_SUBSET_REANALYSIS_COMPLETE`  
科学裁决：`NO_RETRAIN_SALVAGE_FEASIBLE_WITH_RESTRICTED_CLAIMS`

## 1. 执行边界

本轮只拉取并过滤已有逐样本prediction，未训练、未重训、未运行模型推理、未重建候选、未重新bootstrap，也未修改论文正文。原`CLEAN_SUBSET_NOT_FEASIBLE`的唯一原因是逐样本prediction缺失；该原因现已解除。

## 2. Artifact闭环

GitHub数据分支及提交：

| Machine | Seed | Commit | Archive SHA256 | Source files |
| --- | ---: | --- | --- | ---: |
| A | 42 | `45fd370` | `c5ebd07db05767726df47fe317f6ba51a1cf69a63d83f1dbca13d3944bc87dd8` | 4 |
| B | 43 | `bc99dfd` | `1bb428e8ad190ae3f9dc09fb95502331f56848b1f644afd419cfebaa9bf82f7d` | 12 |
| C | 44 | `cb716b9` | `4d452b2d43017a20ffb189d733ad8cd3373682a1bfafa95bf8273afbb498b292` | 12 |

三个archive、28个解压源文件的SHA256、字节数与行数均和远端manifest一致；每个prediction文件为5,675行。N/M1的用户、ground truth、候选顺序和ground-truth index逐对一致。seed43/44在未过滤全集上重算的72个指标与冻结`ms96_raw_metrics.csv`逐项一致，容差`1e-12`。

## 3. Clean口径与保留量

沿用既有保守口径：对N评测样本，仅保留M1的Y分支已消费前缀中，同一用户不存在时间戳不早于该评测目标的训练target。保留集的exact target、later history及same-user future/equal target违反均为0。

| M1 point | Split | Original | Clean | Retention |
| --- | --- | ---: | ---: | ---: |
| M1-48 | validation | 5,675 | 5,494 | 96.8106% |
| M1-48 | test | 5,675 | 5,600 | 98.6784% |
| M1-96 | validation | 5,675 | 5,318 | 93.7093% |
| M1-96 | test | 5,675 | 5,535 | 97.5330% |

## 4. Seed42 48k结果

差值定义均为`N48 - M1-48`。

| Split | Metric | N48 | M1-48 | Delta |
| --- | --- | ---: | ---: | ---: |
| validation | HR@1 | 0.6036 | 0.5928 | +0.0107 |
| validation | NDCG@5 | 0.8202 | 0.8146 | +0.0056 |
| validation | MRR | 0.7598 | 0.7524 | +0.0075 |
| test | HR@1 | 0.5863 | 0.5764 | +0.0098 |
| test | NDCG@5 | 0.8103 | 0.8054 | +0.0049 |
| test | MRR | 0.7467 | 0.7403 | +0.0064 |

该运行点仅有seed42，不得升级为跨seed结论。本轮未为这些差值新增bootstrap区间。

## 5. 96k三seed结果

下表报告clean subset上的`N96 - M1-96`三seed均值和样本标准差；`3/3`表示seed42/43/44方向均为正。这是描述统计，不是置信区间。

| Protocol | Split | Metric | Mean delta | Sample SD | Positive seeds |
| --- | --- | --- | ---: | ---: | ---: |
| k5 | validation | HR@1 | +0.0071 | 0.0093 | 3/3 |
| k5 | validation | NDCG@5 | +0.0035 | 0.0029 | 3/3 |
| k5 | validation | MRR | +0.0046 | 0.0040 | 3/3 |
| k5 | test | HR@1 | +0.0107 | 0.0027 | 3/3 |
| k5 | test | NDCG@5 | +0.0053 | 0.0007 | 3/3 |
| k5 | test | MRR | +0.0070 | 0.0009 | 3/3 |
| k20 | validation | HR@1 | +0.0804 | 0.0297 | 3/3 |
| k20 | validation | NDCG@5 | +0.1183 | 0.0113 | 3/3 |
| k20 | validation | MRR | +0.0872 | 0.0190 | 3/3 |
| k20 | test | HR@1 | +0.0768 | 0.0349 | 3/3 |
| k20 | test | NDCG@5 | +0.1157 | 0.0136 | 3/3 |
| k20 | test | MRR | +0.0844 | 0.0214 | 3/3 |
| k50 | validation | HR@1 | +0.0099 | 0.0070 | 3/3 |
| k50 | validation | NDCG@5 | +0.0146 | 0.0131 | 3/3 |
| k50 | validation | MRR | +0.0183 | 0.0073 | 3/3 |
| k50 | test | HR@1 | +0.0105 | 0.0044 | 3/3 |
| k50 | test | NDCG@5 | +0.0142 | 0.0122 | 3/3 |
| k50 | test | MRR | +0.0181 | 0.0060 | 3/3 |

## 6. 可支持与不可支持的结论

可以支持：

- 在直接跨任务target泄漏被排除的高保留率子集上，N specialist在48k seed42及96k三个seed的所有已测N-side条件中均高于M1。
- 96k下k5差距较小；k20差距明显更大；k50仍偏向N，但与k5的相对大小依metric和split变化。
- 协议改变会改变观察到的specialist--multitask差距，但k20/k50候选并非k5的嵌套扩展，不能归因于候选数量单一因素。

不可支持：

- 原全量M1-N结果重新变为有效；这些结果仍包含已确认的跨任务target leakage。
- “更高曝光普遍缩小specialist差距”。seed42 validation从48k到96k收窄，但test并未一致收窄；48k也没有多seed复现。
- 多任务等价、正迁移或因果机制；三seed描述统计也不是显著性检验。
- 将MovieLens clean结论直接外推到尚未完成同口径审计的Amazon M1。

## 7. 状态裁决

- `PREDICTION_RETRIEVAL`: `RESOLVED`
- `CLEAN_SUBSET_NOT_FEASIBLE`: `SUPERSEDED`
- `CLEAN_SUBSET_REANALYSIS`: `COMPLETE`
- `NO_RETRAIN_SALVAGE`: `FEASIBLE_WITH_RESTRICTED_CLAIMS`
- `P1_01_ACTUAL_LEAKAGE_FOUND`: 事实保持，不得删除；clean-subset是替代分析，不是对原全量结果的追认。

## 8. 待授权稿件同步计划

当前不修改稿件。若用户授权，最小同步范围应为：

1. 以clean-subset数值替换MovieLens中依赖全量M1-N的RQ3/RQ4表格与句子。
2. 将曝光结论收紧为seed42 validation收窄、test不一致，不写普遍缩小。
3. 在Methods/Experimental Setup简述clean样本定义和保留量，并明确这是既有checkpoint的无泄漏评测子集。
4. 在Limitations保留原训练数据存在跨任务target overlap、clean subset改变评测人群、48k仅seed42、三seed统计为描述性等边界。
5. 同步Introduction/Contribution/Conclusion/Abstract只做依赖关系所需的最小措辞，不扩展新故事。

## 9. 机器可读产物

- `recovered_clean_summary.json`
- `recovered_clean_per_seed.csv`
- `recovered_clean_multiseed.csv`
- `clean_multiseed_96_summary.json`
- `clean_multiseed_96_summary.csv`
- `m1_clean_subset_recovered_analysis.py`
- `m1_clean_subset_three_seed_summary.py`
- `test_clean_subset_recovered_analysis.py`
