---
title: "Paper Post Exposure Revision"
type: report
status: current
authority: descriptive
source: mixed
created: 2026-09-03
updated: 2026-09-03
last_verified: 2026-09-03
related_code:
  - .agent/exposure_scaling/final_evidence/README.md
  - .agent/exposure_scaling/final_evidence/paper_results_draft.md
  - .agent/exposure_scaling/final_evidence/discussion_outline.md
  - .agent/exposure_scaling/final_evidence/claim_evidence_matrix.md
  - .agent/exposure_scaling/final_evidence/rejected_or_revised_claims.md
  - .agent/exposure_scaling/final_evidence/research_questions.md
  - .agent/exposure_scaling/final_evidence/next_stage_recommendation.md
superseded_by: null
---

# Paper Post Exposure Revision

## Purpose

本报告记录 exposure evidence freeze 之后的论文写作迁移要求。它不是完整论文交付物，也不声称 `.agent/paper_writing/post_exposure/` 已完成；它用于提醒后续写作必须从冻结证据重新组织 Results、Discussion、Abstract、Introduction、Related Work 和 claim hierarchy。

## Source Of Truth

后续论文写作必须以 `.agent/exposure_scaling/final_evidence/` 为事实源。旧 Results 中关于 specialist、interference、positive transfer、candidate size、sample efficiency、SASRec 和 convergence 的表述都需要重新审计。

推荐的工作目录是 `.agent/paper_writing/post_exposure/`。该目录尚未在本次 wiki sync 中生成，因此后续写作任务应先创建 claim audit、Results revised draft、Discussion draft、table/figure mapping、Introduction/Related Work revision plans、paper claim matrix 与 open issues。

## Required Narrative Shift

旧主线倾向把 M1 描述为持续低于专门模型，或把差距解释为固定 multi-task interference。冻结证据要求更细的表述：M1-96 在 Y-native binary 上没有可检测退化，并在 PopMatch-k5 validation 上接近 N96；但 k20/k50 hard-candidate protocols 仍显示 N-specialist robustness advantage。

旧 SASRec 叙事容易混合 optimizer-step alignment 与 sample-exposure alignment。新写作必须明确：SASRec 在高训练预算 regime 中可以很强，但在近似 matched task-sample exposure 下，N-K0 在当前评估点全部更强。

旧 candidate-size 叙事需要降级。k5/k20/k50 candidate files 几乎 non-nested，k20/k50 结果应写作 hard-candidate protocol robustness，而不是纯 candidate-size effect。

## Recommended Paper Structure

RQ1 应解释 Y/N supervision semantics 与原生指标差异。

RQ2 应写 exposure scaling：Y-native gains weaken by 96k，N-native ranking continues through 200k。

RQ3 应写 M1 unification：M1-96 preserves Y-side capability and approaches N96 on k5 validation，同时保留 hard-candidate robustness cost。

RQ4 应写 SASRec exposure-aware comparison：sample-exposure matched points favor N-K0，高预算 SASRec 作为 separate regime。

RQ5 应写 claim boundaries：validation-first selection、test report-only、candidate protocol composition confound、single-seed descriptive status、M1-200 deferred。

## Immediate Next Step

恢复 Paper Writing / Submission Package。不要再开训练。先在 `.agent/paper_writing/post_exposure/` 生成独立工作副本和审计文件，不直接覆盖正式 manuscript。写作时使用 validation 做选择依据，test 只作为冻结决策后的报告补充。
