# Task Packet

## Scope

Open Paper Writing / Submission Package stage and produce the first audit
package: evidence gaps, frozen RQs, main claims, table/figure inventory, and
submission-risk notes.

## Files To Read

- `.agent/current_task.md`
- Authorized relevant wiki reports.
- `.agent/paper_result_consolidation/`
- `.agent/cross_dataset_validation/`

## Files Allowed To Edit

- `.agent/current_task.md`
- `.agent/stage_state.yaml`
- `.agent/paper_writing_submission/`

## Required Skills

- `using-research-writing`
- `paper-orchestration`
- `experiment-results-planning`

## Evidence/Data Inputs

Use existing evidence only. No new experiment launch.

## Required Artifacts

- `evidence_gap_audit.md`
- `claims_final.yaml`
- `claim_evidence_matrix_final.csv`
- `tables/table-schema.md`
- `figures/figure_plan.md`
- `submission/paper_claim_checklist.md`
- `submission/missing_evidence.md`

## Rejection Checks

- No universal LLM-over-SASRec claim.
- No M1 dominance or positive-transfer claim.
- No Amazon multi-seed claim.
- Candidate protocol named for every ranking claim.
- SASRec budget regime named for every SASRec claim.

## Validation Commands

- `python tools/stage_guard.py`
