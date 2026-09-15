# M1 Clean-Subset Salvage Audit

> 2026-09-11更新：本文件的`CLEAN_SUBSET_NOT_FEASIBLE`裁决已被后续prediction恢复结果取代。28个缺失逐样本文件现已取回并验证；当前裁决见`m1-clean-subset-recovery-closure.md`：`NO_RETRAIN_SALVAGE_FEASIBLE_WITH_RESTRICTED_CLAIMS`。下文保留为恢复前审计记录。

日期：2026-09-11  
裁决：`CLEAN_SUBSET_NOT_FEASIBLE`  
限制：无训练、无推理、无候选重建、无新checkpoint、论文正文修改数为0。

## 1. 审计口径

对N验证/测试样本`e=(u,t_e)`，仅当M1的Y分支已消费训练目标中不存在同一用户且时间戳`t >= t_e`的目标时保留。M1训练数据按Y:N=1:1交错，`SequentialSampler`顺序读取，单卡batch为1、梯度累积为8，因此每个优化步对应4条Y和4条N样本；M1-48和M1-96分别按Y/N前48,000和96,000条构造保守掩码。

输入、掩码和结果的机器可读记录位于`m1-clean-subset-audit/`，生成脚本为`m1_clean_subset_salvage_audit.py`。

## 2. 覆盖率与闭合检查

| M1点 | Split | 原样本/用户 | 干净样本/用户 | 删除 | 干净比例 | 保留集A/B/C违反 |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| M1-48 | validation | 5,675 | 5,494 | 181 | 96.8106% | 0 / 0 / 0 |
| M1-48 | test | 5,675 | 5,600 | 75 | 98.6784% | 0 / 0 / 0 |
| M1-96 | validation | 5,675 | 5,318 | 357 | 93.7093% | 0 / 0 / 0 |
| M1-96 | test | 5,675 | 5,535 | 140 | 97.5330% | 0 / 0 / 0 |

A表示目标未作为M1 Y训练target，B表示目标未进入任何后续M1 Y训练history，C表示同用户不存在时间戳不早于评测目标的M1 Y训练target。N训练分支对N validation/test的target overlap和history overlap均为0。

## 3. 预测可用性

本地仅有seed42 N96/M1-96在k5/k20/k50、validation/test上的配对逐用户预测。以下必需artifact缺失：seed42 N48/M1-48，以及seed43/44 N96/M1-96的逐用户预测。多seed汇总指标不能按用户掩码过滤，不能替代逐样本预测。

因此无需训练，但若要闭合完整补救链，仍需要取得已有逐样本预测；若原机器也未保存，则必须新推理，而本轮明确禁止新推理。

## 4. Seed42 M1-96干净子集结果

| Protocol | Split | n | Metric | N96 | M1-96 | N-M1 |
| --- | --- | ---: | --- | ---: | ---: | ---: |
| k5 | validation | 5,318 | HR@1 | 0.6222 | 0.6209 | +0.0013 |
| k5 | validation | 5,318 | NDCG@5 | 0.8296 | 0.8278 | +0.0018 |
| k5 | validation | 5,318 | MRR | 0.7723 | 0.7700 | +0.0023 |
| k5 | test | 5,535 | HR@1 | 0.6074 | 0.5937 | +0.0137 |
| k5 | test | 5,535 | NDCG@5 | 0.8204 | 0.8144 | +0.0060 |
| k5 | test | 5,535 | MRR | 0.7603 | 0.7522 | +0.0081 |
| k20 | validation | 5,318 | HR@1 / NDCG@5 / MRR delta | | | +0.1104 / +0.1260 / +0.1048 |
| k20 | test | 5,535 | HR@1 / NDCG@5 / MRR delta | | | +0.1144 / +0.1253 / +0.1052 |
| k50 | validation | 5,318 | HR@1 / NDCG@5 / MRR delta | | | +0.0169 / +0.0294 / +0.0260 |
| k50 | test | 5,535 | HR@1 / NDCG@5 / MRR delta | | | +0.0143 / +0.0279 / +0.0237 |

seed42用户级配对bootstrap为5,000次。k5 validation三项95%区间均跨0；k5 test三项区间均高于0。k20/k50两个split的三项区间均高于0。完整区间见`m1-clean-subset-audit/seed42_clean_bootstrap.csv`。

## 5. 科学裁决

干净子集覆盖充分，且seed42方向仍可解释：k5验证近似持平，测试偏向N；更难候选协议稳定偏向N。然而RQ3依赖N48/M1-48曝光趋势和N96多seed稳定性，RQ4依赖M1-96多seed协议稳健性。缺少相应逐样本预测时，两者都不能从单seed局部结果升级为论文证据。

因此裁决为`CLEAN_SUBSET_NOT_FEASIBLE`，原因是**必需预测artifact不可用**，不是样本覆盖不足或残余泄漏。若随后只取回已有预测，可在不训练、不推理的前提下重新评估裁决。

## 6. SASRec披露恢复

SASRec实现为item/position embedding加2层因果Transformer encoder，维度64、2 heads、FFN宽度256、GELU、dropout 0.2、最终LayerNorm，以序列表示和item embedding点积加item bias评分。训练使用全物品cross-entropy、AdamW、LR 0.001、weight decay 0，无scheduler，batch 512，seed42，最大历史长度10。

S47/S94/S188/S391由正式脚本预先指定为47/94/188/391个optimizer steps，各点从头独立训练，不是按validation择优或early stopping。实际曝光分别为24,064/48,128/96,256/200,000；S391最后一个batch为短尾。所有点绑定同一PopMatch-k5 seed42 validation/test候选，validation用于主比较，test为report-only。
