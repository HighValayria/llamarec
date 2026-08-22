# Figure Plan

## Figure 1: Task Framework

Show one history feeding three interfaces:

- Y: History + Item -> Yes/No.
- N: History + Candidates -> Next item label.
- M: shared LLM with Y and N interfaces.

Purpose: conceptual anchor for supervision semantics.

## Figure 2: Sample-efficiency Curve

Use existing MovieLens sample-efficiency curve. Highlight closest-exposure
N-K0 advantage and high-exposure SASRec regime separately.

Purpose: visual support for budget-regime claim.

## Figure 3: Candidate Difficulty Diagnostic

Use either candidate-size robustness or Random-vs-PopMatch popularity gap and
ranking effect. Prefer one figure only if table space is tight.

Purpose: show that candidate construction changes interpretation.

## Deferred Figures

Cold/tail grouped diagnostics should be appendix material unless the narrative
needs a diagnostic figure. The coldest bucket has only 26 samples.
