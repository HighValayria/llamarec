# Current Task

## Stage Goal
- Start the Paper Writing / Submission Package stage.
- Convert the completed experimental system into a venue-neutral manuscript
  package with traceable claims, consistent experiment language, frozen table
  plans, explicit limitations, and a submission checklist.
- First milestone: perform a final evidence-gap audit, freeze research
  questions and main claims, inventory tables/figures, then report back before
  drafting full manuscript sections.

## Scope
- Stage-local paper artifacts under `.agent/paper_writing_submission/`.
- Durable wiki context after one-time stage-opening read authorization.
- Existing results, CSV/JSON/Markdown reports, and stage artifacts only.
- Necessary code/config checks for experiment definitions and supported CLI
  behavior.

## Non-Goals
- No new LLM training.
- No Amazon seed43/44 unless later explicitly approved as a minimal robustness
  extension.
- No new SASRec checkpoint.
- No M3/M4, KAR, hard-negative training, 7B, MovieLens-32M, third dataset,
  LoRA sweep, or strict compute/FLOPs matching.
- No formal wiki writes until stage-end synchronization authorization.
- No venue-specific LaTeX template until a target venue is chosen.

## Long-Term Constraints
- This is an empirical/systematic analysis paper, not a new model-architecture
  paper.
- Positioning should be a systematic empirical study of recommendation
  supervision semantics, multi-task tradeoffs, hard-candidate robustness, and
  sample-efficiency-aware baseline positioning for recommendation-tuned LLMs.
- Claims must distinguish Random-k5, PopMatch-k5, k20/k50 robustness,
  closest-exposure SASRec, and high-exposure SASRec regimes.
- Cross-dataset wording must treat Amazon Musical Instruments seed42 as
  directional validation, not multi-seed stability.
- Evidence gaps must be recorded first; no supplementary experiment can start
  without explicit user approval.
- Formal wiki reads are currently pending stage-opening authorization.

## Evidence Sources
- User migration directive for Paper Writing / Submission Package on
  2026-08-22.
- Closed Cross-dataset Validation wiki sync at commit
  `6b47df0 Sync cross-dataset validation wiki`.
- Pending one-time wiki read authorization for:
  - `wiki/index.md`
  - `wiki/current_state.md`
  - directly relevant result reports
  - relevant Paper Result Consolidation stage artifacts.
- Existing stage artifacts, to be inspected after stage initialization:
  - `.agent/paper_result_consolidation/`
  - `.agent/cross_dataset_validation/`
  - `.agent/multiseed_stability/`
  - `.agent/sample_efficiency_training_efficiency/`
  - `.agent/cold_tail_item_slice_diagnostic/`

## Related Code
- `configs/experiment.yaml`
- `configs/y.yaml`
- `configs/n.yaml`
- `configs/m.yaml`
- `src/data/preprocess.py`
- `src/data/build_step2.py`
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
- New stage requested by the user.
- Cross-dataset Validation is closed and wiki-synced.
- Stage initialization is in progress.
- One-time wiki read authorization has not yet been granted in this stage, so
  formal wiki has not been read for Paper Writing.

## Verification Results
- Pending.

## Unresolved Questions
- Does the user authorize a one-time stage-opening read of the directly
  relevant wiki files listed in the migration directive?
- Are Amazon binary metrics already sufficient for Claim 1, or is there a
  paper-facing binary evidence gap to record?
- Does the narrow Amazon N-K0 over M1 margin require optional seed43/44 later,
  or only cautious wording?
- Is the current empirical contribution enough for the target paper, or should
  a future method-extension stage be considered after the manuscript audit?

## Pending Wiki Sync
No pending wiki sync.

## Invalidating Conditions
- Starting new experiments during paper writing without explicit user approval.
- Claiming universal LLM superiority over SASRec.
- Claiming M1 positive transfer or universal dominance.
- Treating Amazon seed42 as multi-seed evidence.
- Treating Random-k5 as the primary hard-candidate claim setting.
- Writing formal wiki during the stage without stage-end authorization.
