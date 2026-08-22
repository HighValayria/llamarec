# Experimental Setup

The experiments use MovieLens-1M as the primary dataset and Amazon Musical
Instruments as the cross-dataset validation set. MovieLens-1M carries the full
evidence package: single-task Y and N adapters, multi-task variants, candidate
robustness, baseline positioning, sample-efficiency curves, cold/tail
diagnostics, and seeds 42, 43, and 44 for the main stability comparisons.
Amazon Musical Instruments is used as a second-domain seed42 full-test
validation run.

All sequence construction respects temporal order. A target example uses only
history events whose timestamp is strictly earlier than the target timestamp.
For the N task, the target is the actual next interaction under this temporal
sequence, not a filtered next liked item. This choice keeps preference
prediction and next-interaction prediction semantically separate.

Amazon Musical Instruments contains 57,439 users, 24,584 items, and 511,792
interactions after preprocessing. The Y task contains 396,908 training samples,
57,442 validation samples, and 57,442 test samples. The N task contains 339,449
training samples, 57,439 validation samples, and 57,439 test samples. These
statistics are used to define the second-dataset role of Amazon in the paper:
it validates whether the main ranking-side directions survive a larger and
different item domain, but it does not provide multi-seed evidence.

Candidate sets are reported by protocol. Random-k5 is an easy-negative
reference condition. PopMatch-k5 is the primary controlled ranking protocol
because it reduces popularity-gap shortcuts between targets and distractors.
MovieLens additionally includes k20 and k50 candidate-size stress tests and
candidate-order perturbation diagnostics. Amazon includes Random-k5 and
PopMatch-k5 full-test seed42 comparisons.

The evaluated model families are the zero-shot base interface, Y-K0, N-K0,
M1, and SASRec. M0 and M2 remain development diagnostics and are assigned to
the appendix. Preference prediction is evaluated with AUC and
validation-calibrated F1 where the calibrated protocol is documented. Ranking
is evaluated with HR@1, NDCG@5, and MRR. SASRec is reported under closest
N-task sample exposure and, for MovieLens, high sequential-supervision
exposure. The study does not claim strict compute or FLOPs matching.
