---
title: "Exposure Scaling Seed42"
type: report
status: current
authority: descriptive
source: mixed
created: 2026-09-03
updated: 2026-09-03
last_verified: 2026-09-03
related_code:
  - .agent/exposure_scaling/final_evidence/README.md
  - .agent/exposure_scaling/final_evidence/exposure_main_table.csv
  - .agent/exposure_scaling/final_evidence/sasrec_exposure_alignment.csv
  - .agent/exposure_scaling/final_evidence/claim_evidence_matrix.md
  - .agent/exposure_scaling/final_evidence/rejected_or_revised_claims.md
  - .agent/exposure_scaling/final_evidence/stage_summary.md
  - .agent/exposure_scaling/final_evidence/tables/table_hard_candidate.csv
  - .agent/exposure_scaling/final_evidence/validated_findings.yaml
  - .agent/exposure_scaling/final_evidence/rejected_findings.yaml
  - .agent/exposure_scaling/final_evidence/open_questions.yaml
superseded_by: null
---

# Exposure Scaling Seed42

## Scope

本报告固化 MovieLens-1M seed42 的 LLM exposure scaling、M1 对齐、hard-candidate robustness 与 SASRec exposure-aware baseline 证据。它记录已经冻结的结果口径，不启动训练、不重新评测、不新增 checkpoint。

事实源是 `.agent/exposure_scaling/final_evidence/`。该目录由 no-training evidence consolidation 生成，包含主表、claim matrix、rejected claims、论文 Results draft、discussion outline、表格、图和阶段关闭建议。

## Evaluation Contract

Validation split 用于判断训练是否继续、是否扩展 exposure、是否冻结结论。Test split 只用于 report-only，在 validation 决策已经固定后补充报告，不能反向改变训练选择或 claim strength。

Y-K0 的原生任务是 binary preference prediction，主要指标是 AUC、F1 和 Accuracy。Y-as-ranker 只是在 PopMatch candidate set 上用 `P(Yes)` 排序的 bridge metric，不等同于 N-task next-item ranking。

N-K0 的原生任务是 next-item candidate ranking，主要指标是 HR@1、NDCG@5 和 MRR。M1 同时保留 M-Y binary interface 与 M-N ranking interface。SASRec 只作为 next-item ranking baseline。

LLM exposure 按 `per_device_train_batch_size * gradient_accumulation_steps * world_size * optimizer_steps` 计算。本阶段正式 LLM runs 使用 `1 * 8 * 1`，即每个 optimizer step 处理 8 个训练样本。Y/N 单任务中，3000/6000/12000/25000 steps 分别对应 24k/48k/96k/200k exposure。M1-96 是 24000 steps，按 1:1 Y/N mixing 解释为 96k Y exposure 加 96k N exposure。

## Main Findings

Y-native preference capability 到 96k 后收益减弱，但不能写成严格收敛。Validation AUC 从 Y24 的 `0.7761` 到 Y48 的 `0.7816`，再到 Y96 的 `0.7844`；F1 从 `0.7792` 升至 `0.7848` 后回落到 `0.7783`；Accuracy 从 `0.7191` 到 `0.7230`，再到 `0.7235`。

N-native ranking 到 200k 仍随 exposure 增长。PopMatch-k5 validation HR@1 从 N24 `0.5774`、N48 `0.6030`、N96 `0.6238` 提升到 N200 `0.6516`；NDCG@5 从 `0.8068` 提升到 `0.8432`；MRR 从 `0.7420` 提升到 `0.7904`。N200 是 near-full-pool one-pass anchor，不是 converged endpoint。

M1-96 没有显示 Y-side degradation。相对 Y96，M1-96 的 validation binary delta 为 AUC `+0.00248`、F1 `+0.00553`、Accuracy `+0.00460`。Bootstrap 显示 F1 有小的正向信号，AUC 与 Accuracy 仍兼容 parity，因此不能写成整体 positive transfer。

M1-96 在 PopMatch-k5 validation 上接近 N96。N96-M1-96 delta 为 HR@1 `+0.00035`、NDCG@5 `+0.00115`、MRR `+0.00149`，对应 CI 均跨 0。该结论只支持 k5 validation near-parity，不能写 M1 超过 N96，也不能写 N96 在 k5 validation 上显著强于 M1-96。

Hard-candidate protocols 暴露 N-side robustness advantage。k20 validation 下 N96-M1-96 gaps 为 HR@1 `+0.11242`、NDCG@5 `+0.12698`、MRR `+0.10626`；k50 validation 下为 HR@1 `+0.01709`、NDCG@5 `+0.02896`、MRR `+0.02583`。这些 candidate protocols 几乎 non-nested，因此写作时必须称为 hard-candidate protocol robustness，不能单独归因于 candidate size。

SASRec 对齐结果支持 exposure-aware baseline comparison。在近似 matched task-sample exposure 下，N-K0 在 24k、48k、96k、200k 全部强于 SASRec；validation HR@1 gaps 分别为 `+0.3043`、`+0.3100`、`+0.2957`、`+0.1767`。200k gap 缩小，但不支持 “LLM universally dominates SASRec”，也不支持严格 FLOPs、wall-clock、GPU cost 或 parameter-update matching。

## Claim Boundaries

可以写：preference supervision 与 next-interaction supervision 编码不同推荐语义，且对 exposure 的响应不同。

可以写：Y-native gains weaken by 96k，N-native ranking remains exposure-sensitive through 200k。

可以写：M1-96 preserves Y-side capability and approaches N96 under PopMatch-k5 validation。

可以写：harder candidate protocols reveal a remaining N-side robustness advantage for the dedicated model。

可以写：at approximately matched task-sample exposure, N-K0 outperforms SASRec across evaluated exposure points。

不能写：Y fully converged、N200 converged、M1 demonstrates overall positive transfer、M beats N、N beats M on k5 validation、candidate-size effect without composition caveat、LLM universally dominates SASRec。

## Open Questions

- Seed42 的 M1/Y 与 M1/N 关系是否跨 seed 稳定。
- k20/k50 gap 有多少来自 candidate composition，而非 candidate count。
- M1-200 是否会改变高 exposure 下 specialist/multitask 的关系。
- Amazon 是否需要 exposure scaling 复现，或只保留 directional validation。

## Paper Use

本报告应取代旧的固定 specialist/interference 叙事。论文 Results 应采用 exposure-aware 主线：Y/N semantics 不同，Y 与 N 对 exposure 的收益曲线不同，M1 是统一模型的能力保留与折中，而不是单任务全面替代；SASRec 比较必须区分 task-sample exposure 与高训练预算 regime。
