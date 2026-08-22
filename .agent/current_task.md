# Current Task

## Stage Goal
- Active stage: Paper Writing / Submission Package.
- Convert completed MovieLens-1M and Amazon Musical Instruments evidence into
  a venue-neutral manuscript package with traceable claims, frozen table/figure
  plans, explicit limitations, and a submission checklist.
- First milestone: stage creation, one-time relevant wiki read, context
  compression, evidence-gap audit, claim freeze proposal, table/figure
  inventory, and report back before drafting full manuscript sections.

## Scope
- Stage-local paper artifacts under `.agent/paper_writing_submission/`.
- Existing experiment outputs, analysis summaries, and result-consolidation
  artifacts only.
- Claim/evidence audit, RQ/claim freeze, table schemas, figure plan,
  appendix/reproducibility plan, and submission checklist.

## Non-Goals
- No new LLM training or baseline training.
- No Amazon seed43/44 unless later explicitly approved.
- No new SASRec checkpoint, M3/M4, KAR, hard-negative training, 7B,
  MovieLens-32M, third dataset, LoRA sweep, or strict FLOPs matching.
- No formal wiki writes until stage-end synchronization authorization.
- No venue-specific LaTeX template until a target venue is chosen.

## Long-Term Constraints
- Position the paper as a systematic empirical study of recommendation
  supervision semantics, multi-task tradeoffs, hard-candidate robustness, and
  sample-efficiency-aware baseline positioning for recommendation-tuned LLMs.
- Claims must distinguish Random-k5, PopMatch-k5, k20/k50 candidate-size
  stress, closest-exposure SASRec, and high-exposure SASRec regimes.
- Cross-dataset wording must treat Amazon Musical Instruments seed42 as
  directional validation, not multi-seed stability.
- Random-k5 is not the primary hard-candidate evidence.
- High-exposure SASRec can outperform N-K0, but that is a separate budget
  regime from sample-exposure matched comparisons.

## Evidence Sources
- User migration directive for Paper Writing / Submission Package on
  2026-08-22.
- One-time stage-start wiki read authorized by user on 2026-08-22, limited to:
  `wiki/index.md`, `wiki/current_state.md`, and directly relevant reports:
  Phase 2B synthesis, Phase 2C PopMatch, fair-budget baseline positioning,
  sample-efficiency curve, cold/tail diagnostic, multiseed stability,
  paper-result consolidation, and cross-dataset validation.
- The wiki read was compressed into this file and revoked on 2026-08-22.
- Stage-local evidence inputs from `.agent/paper_result_consolidation/`,
  including claims, evidence matrix, paper-ready claims, Results draft,
  limitations, table plan, artifact map, validated findings, and open
  questions.
- Current stage artifacts under `.agent/paper_writing_submission/`.

## Related Code
- `configs/experiment.yaml`
- `configs/y.yaml`
- `configs/n.yaml`
- `configs/m.yaml`
- `src/eval/candidate_sets.py`
- `src/inference/base_zero_shot.py`
- `src/inference/evaluate_y_adapter.py`
- `src/inference/evaluate_n_adapter.py`
- `src/inference/evaluate_m_adapter.py`
- `src/train/train_y.py`
- `src/train/train_n.py`
- `src/train/train_m.py`
- `src/baselines/sasrec.py`
- `src/analysis/phase2b_result_synthesis.py`
- `src/analysis/phase2c_result_summary.py`
- `src/analysis/sample_efficiency_curve.py`
- `src/analysis/multiseed_stability_summary.py`

## Current Progress
- Stage opened and pushed in commit `8a8d8a9`.
- One-time relevant wiki read completed and revoked.
- First-milestone paper artifacts created:
  - `.agent/paper_writing_submission/evidence_gap_audit.md`
  - `.agent/paper_writing_submission/claims_final.yaml`
  - `.agent/paper_writing_submission/claim_evidence_matrix_final.csv`
  - `.agent/paper_writing_submission/plan/outline.md`
  - `.agent/paper_writing_submission/plan/project-overview.md`
  - `.agent/paper_writing_submission/tables/table-schema.md`
  - `.agent/paper_writing_submission/figures/figure_plan.md`
  - `.agent/paper_writing_submission/submission/paper_claim_checklist.md`
  - `.agent/paper_writing_submission/submission/missing_evidence.md`
- Proposed RQs are frozen around supervision semantics, multi-task tradeoffs,
  candidate difficulty, LLM-vs-SASRec budget regimes, and cross-dataset
  validity.
- Proposed main claims are frozen as:
  1. Preference and next-item supervision induce distinct capabilities.
  2. Multi-task tuning unifies both capabilities but specialists retain
     advantages.
  3. Candidate-difficulty protocol strongly changes ranking conclusions.
  4. LLM-vs-SASRec conclusions depend on supervision exposure and budget
     regime.
  5. Cross-dataset evidence supports directionally similar N-task ranking
     behavior but not multi-seed cross-dataset stability.
- Manuscript Draft v0 moved the stage from evidence audit into drafting:
  - final RQs recorded in `.agent/paper_writing_submission/rqs_final.md`
  - four main tables created under `.agent/paper_writing_submission/tables/`
  - Draft v0 manuscript files created under
    `.agent/paper_writing_submission/manuscript/`
  - experiment protocol and traceability gates added under
    `.agent/paper_writing_submission/plan/`
  - no new experiments were started.

## Verification Results
- `git diff --check` passed on 2026-08-22.
- `python tools/stage_guard.py` passed on 2026-08-22 with 0 errors and 0
  warnings using the bundled Codex Python runtime.
- Draft v0 `git diff --check` passed on 2026-08-22.
- Draft v0 `python tools/stage_guard.py` passed on 2026-08-22 with 0 errors
  and 0 warnings using the bundled Codex Python runtime.
- Draft v0 acceptance review is recorded in
  `.agent/paper_writing_submission/submission/draft_v0_acceptance_review.md`.

## Unresolved Questions
- Amazon binary metrics are present as diagnostic test outputs, but not yet a
  validation-calibrated paper-grade binary claim; treat as a non-blocking
  evidence gap.
- Amazon N-K0 over M1 is positive but narrow under seed42; multi-seed Amazon is
  optional robustness work, not required before drafting if wording remains
  cautious.
- Target venue and template remain unset.
- A future method-extension stage may be useful only after manuscript gaps are
  visible; it is not part of this stage.

## Pending Wiki Sync
No pending wiki sync during this active stage. Stage-end wiki updates should
summarize the paper package artifacts only after explicit write authorization.

## Invalidating Conditions
- Starting new experiments during paper writing without explicit user approval.
- Claiming universal LLM superiority over SASRec.
- Claiming M1 positive transfer or universal dominance.
- Treating Amazon seed42 as multi-seed evidence.
- Treating Random-k5 as the primary hard-candidate claim setting.
- Writing formal wiki during the stage without stage-end authorization.
