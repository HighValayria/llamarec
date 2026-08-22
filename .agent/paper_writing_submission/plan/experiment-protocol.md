# Experiment Protocol

The paper uses existing completed experiments only. MovieLens-1M is the primary
dataset because it has the full Y/N/M, robustness, sample-efficiency, cold-tail,
and multi-seed evidence package. Amazon Musical Instruments is the second
dataset and is used as seed42 cross-domain validation.

The preference task estimates `P(Like | History, Item)`. The next-item task
selects the actual next interaction from a candidate set, not the next liked
item. Histories use events with timestamp strictly earlier than the target
timestamp. Ranking results distinguish Y P(Yes)-based scoring from N
candidate-label scoring.

Candidate protocols are separated throughout the manuscript. Random-k5 is an
easy-negative reference protocol. PopMatch-k5 is the primary controlled ranking
protocol. Random-k20 and Random-k50 provide candidate-size stress. Candidate
order perturbation remains an appendix diagnostic because its effect is smaller
than candidate-size expansion in the current evidence.

The LLM model family includes the zero-shot base interface, Y-K0, N-K0, and M1.
M0 and M2 remain diagnostic variants. SASRec is reported in two budget regimes:
closest N-task sample exposure and high sequential-supervision exposure. The
paper does not claim strict compute or FLOPs matching.

Primary metrics are AUC and validation-calibrated F1 for preference prediction
where the calibrated protocol is available, and HR@1, NDCG@5, and MRR for
ranking. MovieLens reports multi-seed stability for seeds 42, 43, and 44.
Amazon reports seed42 only.
