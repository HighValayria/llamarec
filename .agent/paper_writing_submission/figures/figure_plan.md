# Figure Plan

## Figure 1: Task Framework

Show one history feeding three interfaces:

- Y: History + Item -> Yes/No.
- N: History + Candidates -> Next item label.
- M: shared LLM with Y and N interfaces.

Purpose: conceptual anchor for supervision semantics.

Draft v0 role: main figure. It should visually separate the Y path
`History + Item -> P(Yes)`, the N path `History + Candidate Set -> candidate
label`, and the M1 shared-adapter setting that exposes both paths.

## Figure 2: Sample-efficiency Curve

Use existing MovieLens sample-efficiency curve. Highlight closest-exposure
N-K0 advantage and high-exposure SASRec regime separately.

Purpose: visual support for budget-regime claim.

Draft v0 role: main figure. It should show N-K0 and SASRec along N-task sample
exposure, with the closest-exposure region visually separated from the
high-exposure SASRec anchors.

## Figure 3: Candidate Difficulty Diagnostic

Use either candidate-size robustness or Random-vs-PopMatch popularity gap and
ranking effect. Prefer one figure only if table space is tight.

Purpose: show that candidate construction changes interpretation.

Draft v0 choice: candidate-size robustness is preferred for the main paper.
Popularity/cold-tail diagnostics can move to appendix because the coldest
bucket is too small for a headline claim.

## Deferred Figures

Cold/tail grouped diagnostics should be appendix material unless the narrative
needs a diagnostic figure. The coldest bucket has only 26 samples.
