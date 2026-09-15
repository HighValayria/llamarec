# ICECAI 2026 Cross-Task-Safe Scientific Repair Execution

Date: 2026-09-11

## Goal

Replace every active M1-N ranking claim and table value with the completed cross-task-safe evidence, add the missing SASRec reproducibility disclosure, preserve English-Chinese semantic parity, rebuild both ICECAI PDFs, and leave the manuscript ready for a short independent P1 closure verification.

## Allowed Scope

- Methods and Experimental Setup: cross-task holdout-integrity protocol, common-subset exposure comparison, SASRec implementation and operating-point disclosure.
- Results: RQ3, RQ4, and the Amazon paragraph where M1 is not certified.
- Necessary dependent synchronization in Contributions, Introduction, Discussion, Limitations, Conclusion, and Abstract.
- Tables IV-VII, evidence controls, manuscript contract, execution report, builds, tests, and PDF visual QA.

## Fixed Evidence

- `m1-common-clean-exposure-verification.csv`: common-subset seed42 48k/96k k5 point metrics.
- `m1-clean-subset-audit/clean_multiseed_96_summary.csv`: 96k three-seed clean ranking deltas.
- `m1-clean-subset-recovery-closure.md`: prediction identity and 28/28 artifact closure.
- Existing verified Y-side paired bootstrap and SASRec run metadata.

## Table Decision

- Table IV: seed42 common cross-task-safe k5 exposure comparison.
- Table V: seed42 Y-side binary paired bootstrap only.
- Table VI: 96k cross-task-safe three-seed N-M1 ranking deltas.
- Table VII: cross-task-safe subset coverage.
- Figures 1 and 2 remain unchanged.

## Prohibitions

No training, retraining, inference, candidate generation, bootstrap, new statistical analysis, literature search, recompression, author metadata, GenAI disclosure, submission, or Wiki access/modification.

## Verification Gates

1. Active M1-N ranking numbers trace only to clean machine-readable evidence.
2. No old full-set M1-N values or old ranking bootstrap intervals remain active.
3. Final-protocol framing appears without experiment-debugging history.
4. No training-time joint cutoff is claimed.
5. SASRec architecture, optimizer, scoring, and operating-point selection are complete.
6. English and bilingual builds compile; citations, references, tables, figures, parity, contract, and visual layout pass.

## Completion State

Target state: `GPT6_REPAIR_VERIFICATION_READY`. This task does not perform the later GPT6 verification and does not freeze the science.
