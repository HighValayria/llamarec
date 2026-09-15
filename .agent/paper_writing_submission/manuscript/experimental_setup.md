# Experimental Setup

The empirical design separates the dataset used for the complete evidence
package from the dataset used for a second-domain check. MovieLens-1M is the
primary setting because all major comparisons are available there: single-task
Y and N adapters, the M1 multi-task adapter, candidate-protocol robustness,
baseline positioning, sample-efficiency curves, cold/tail diagnostics, and
three-seed stability results for seeds 42, 43, and 44. Amazon Musical
Instruments is used differently. It provides a full-test seed42 validation run
in a larger item domain, but it is not treated as a multi-seed replication of
the MovieLens package.

All examples are constructed under a temporal constraint. For a target event,
the input history contains only events whose timestamp is strictly earlier than
the target timestamp. The N-task label is the actual next interaction in this
sequence, rather than the next liked item after preference filtering. This
definition preserves the distinction between preference prediction and
next-interaction ranking: the Y task estimates whether the user is likely to
like a candidate item, while the N task asks which candidate is the next
observed interaction.

After preprocessing, Amazon Musical Instruments contains 57,439 users, 24,584
items, and 511,792 interactions. The Y-task split contains 396,908 training
examples, 57,442 validation examples, and 57,442 test examples. The N-task
split contains 339,449 training examples, 57,439 validation examples, and
57,439 test examples. These counts define Amazon's role in the paper: it tests
whether the main ranking-side directions survive a different domain and larger
catalog, while calibrated binary validation and multi-seed stability remain
MovieLens-side evidence.

Ranking evaluation is organized around candidate-set construction. Random-k5
is reported as an easy-negative reference protocol. PopMatch-k5 is the primary
controlled ranking protocol because it narrows the popularity gap between the
target item and distractors, making it harder for models to succeed through
popularity shortcuts alone. MovieLens also includes Random-k20 and Random-k50
candidate-size stress tests, plus candidate-order perturbation diagnostics.
Amazon includes full-test seed42 Random-k5 and PopMatch-k5 comparisons.

The evaluated systems include the zero-shot base interface, the Y-K0 preference
adapter, the N-K0 next-item adapter, the M1 multi-task adapter, and SASRec.
Development variants such as M0 and M2 are retained only as diagnostics. Binary
preference prediction is measured with AUC and validation-calibrated F1 where
that calibration protocol is part of the paper-grade evidence. Ranking is
measured with HR@1, NDCG@5, and MRR. SASRec is reported under two exposure
regimes: closest N-task sample exposure, and, on MovieLens only, high
sequential-supervision exposure. The comparison is therefore exposure-aware,
not a strict compute- or FLOPs-matched benchmark.
