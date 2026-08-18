# Limitations And Boundary Wording

## Dataset Scope

All consolidated evidence is from MovieLens-1M. The results are strong enough
for a MovieLens-1M empirical story, but not yet enough for a broad cross-domain
claim. A second dataset or a larger MovieLens variant remains the largest
external-validity gap.

Paper wording:

> On MovieLens-1M, the completed diagnostics show consistent task-interface and
> budget-regime effects. We leave cross-dataset generalization to future work.

## Candidate Protocol Scope

Canonical Random-k5, PopMatch-k5, k20/k50 candidate-size stress tests, and
candidate order perturbation answer different questions. Tables must not mix
them without a protocol column.

Paper wording:

> We report each ranking result together with the candidate construction
> protocol because random negative pools and popularity-matched pools induce
> different shortcut opportunities.

## Binary Metric Scope

Binary AUC, fixed-threshold F1, and validation-calibrated F1 should remain
separate. Y-K0 and M1 binary results are meaningful for preference prediction,
but they do not imply candidate-label ranking strength.

## SASRec Budget Scope

SASRec has three interpretable regimes:

- optimizer-step-aligned diagnostic;
- closest N-task sample-exposure diagnostic;
- high-exposure sequential recommendation anchor.

Only the closest N-task exposure curve supports sample-efficiency language.
High-exposure SASRec supports a different conclusion: with far more N-task
exposure, SASRec is the strongest ranking model.

## Multi-task Budget Scope

M1 matches N-K0 on N-task exposure in the fair-budget diagnostic, but its total
Y+N exposure is larger. Use "unified tradeoff" rather than "strictly fair
compute match."

## Cold/Tail Scope

The coldest `<=10` popularity bucket has only 26 samples. Treat the cold/tail
slice as a diagnostic: useful for qualifying where SASRec high-exposure gains
appear, but not a primary claim by itself.

## Model Prior Scope

The Llama backbone may already encode movie-title and popularity priors. The
current controls reduce shortcut concerns but do not eliminate all pretraining
prior explanations.
