# Next Stage Recommendation

## Recommended Next Stage

**Cross-dataset Validation** is the recommended next stage.

Reason: the current MovieLens-1M evidence is internally coherent and now
multi-seed stable. The largest remaining risk is external validity, not another
MovieLens-1M metric tweak. A second dataset would directly test whether the
paper's central task-interface and budget-regime claims generalize.

## Suggested Scope

- Reuse the accepted Y-K0, N-K0, and M1 setup.
- Reuse the PopMatch-style hard candidate protocol.
- Include one sequential baseline regime with explicit sample-exposure wording.
- Prioritize a compact validation over a full sweep.

## Non-recommended Immediate Stages

- **New method module first:** not necessary before external validation unless
  the target venue demands algorithmic novelty.
- **More MovieLens-1M ablations first:** lower marginal value than testing
  generalization.
- **Strict compute matching first:** useful only if reviewers or venue norms
  require it; current budget-conditioned story is already clear.

## Fallback

If compute or data access blocks cross-dataset validation, the next-best stage
is manuscript table finalization plus a short title-prior/anonymous-item
diagnostic proposal.
