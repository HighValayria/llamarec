# 4 Results

## 4.1 Distinct supervision semantics

本节检验偏好判断监督与下一交互预测监督是否学习到相同的推荐能力。实验将 Y-K0 作为 binary preference predictor 评估，同时把同一模型放入 PopMatch-k5 候选排序协议中作为 bridge metric；N-K0 则直接按照 next-item ranking 的原生目标评估。结果显示，Y-native binary 指标在 24k 到 96k exposure 范围内保持可用表现，Y-as-ranker 的 PopMatch-k5 NDCG@5 却始终停留在约 0.60 附近。N-K0 在相同数据集上的 PopMatch-k5 排序指标明显更高，96k validation HR@1 达到 0.6238，NDCG@5 达到 0.8303。这说明 Y 与 N 的监督语义不能被视为同一任务的不同表述，二者诱导出的能力具有明确差异。

## 4.2 Task-specific exposure scaling

曝光量变化进一步放大了这种任务差异。Y-native binary 的 AUC 从 Y24 的 0.7761 上升到 Y48 的 0.7816，再到 Y96 的 0.7844，但 F1 从 Y48 的 0.7848 回落到 Y96 的 0.7783，Accuracy 在 0.723 附近变化很小。相同区间内，Y-as-ranker 的 NDCG@5 基本没有随 exposure 增长而提高。N-native ranking 呈现另一种曲线：N24、N48、N96、N200 的 validation HR@1 分别为 0.5774、0.6030、0.6238 和 0.6516，NDCG@5 也从 0.8068 提升到 0.8432。N200 覆盖了 200k 训练池且没有重复样本，target item 覆盖 ratings universe 的 94.47%，history 与 target 的并集覆盖 97.57%。因此，N200 更适合作为 near-full-pool one-pass anchor，而不是收敛终点。

## 4.3 Multi-task specialization under matched exposure

本节考察 M1 在 matched per-task exposure 下是否牺牲专门任务能力。Y-side 上，M1-96 相比 Y96 的 binary bootstrap 显示 F1 有小幅正差异，validation delta 为 +0.00553，95% CI 为 [+0.00096, +0.01025]；test delta 为 +0.00554，95% CI 为 [+0.00046, +0.01041]。AUC 与 Accuracy 的置信区间跨过 0，说明点估计虽为正，但仍与 parity 兼容。由此更稳妥的判断是 M1-96 没有观察到 Y-side degradation，而不是已经证明整体 positive transfer。N-side 上，k5 validation 的 N96-M1-96 差异极小，HR@1 delta 仅 +0.00035，95% CI 为 [-0.01040, +0.01128]，NDCG@5 与 MRR 也跨过 0。这支持 k5 validation 上的 near-parity，但 test report-only 指标仍显示 N96 占优。

## 4.4 Robustness under harder candidate protocols

k5 上的 near-parity 没有推广到更复杂候选协议。在 k20 validation 中，N96-M1-96 的 HR@1、NDCG@5 和 MRR delta 分别为 +0.11242、+0.12698 和 +0.10626，bootstrap CI 均为正；test 上也保持同向差异。k50 协议下差距缩小，但 HR@1、NDCG@5 和 MRR 的 validation CI 仍全部为正。候选协议审计显示，k5、k20 与 k50 候选集几乎不构成嵌套关系，k5_in_k20 的 nested_fraction 为 0，k20_in_k50 也接近 0，Jaccard 相似度很低。因此，本文将这些结果表述为 hard-candidate robustness，而不是单纯 candidate-size effect。现有证据表明，M1-96 在较难候选协议下仍存在 N-side robustness cost。

## 4.5 Exposure-aware comparison with SASRec

SASRec 作为 specialized sequential recommender，需要按训练样本 exposure 对齐，而不是按 wall-clock、FLOPs 或 epoch 名义值直接比较。当前 alignment artifact 验证了 S47、S94、S188 与 S391 分别对应约 24k、48k、96k 与 200k exposure。在这些 matched points 上，N-K0 的 validation HR@1 均高于 SASRec：24k 对比为 0.5774 vs 0.2731，48k 为 0.6030 vs 0.2930，96k 为 0.6238 vs 0.3281，200k 为 0.6516 vs 0.4749。差距在 200k 处缩小，但方向没有反转。这个比较支持 exposure-aware baseline claim，同时边界也很清楚：它是 task-sample exposure matching，不是计算量匹配。

## 4.6 Cross-dataset validation

Amazon 结果暂不扩展为新的训练主线，只作为外部有效性的辅助证据。它的作用是检查 Y/N 语义分离与 N-side ranking 优势是否在 MovieLens 之外保持方向一致，而不是替代本节的 exposure scaling 主结果。当前论文结果部分可以把 Amazon 放在 cross-dataset validation 位置，用于降低单数据集叙事风险；更强的跨数据集 scaling 结论仍需单独实验支持。
