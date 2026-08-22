# Limitations

The paper is an empirical study of supervision interfaces and evaluation
protocols, not a new recommendation architecture. Its claims should not be read
as evidence for a universal LLM recommender or as evidence that M1 achieves
positive transfer beyond single-task specialists.

Amazon Musical Instruments is seed42 only. It provides cross-domain validation
for the ranking-side directions, but it does not provide multi-seed
cross-dataset stability. The Amazon N-K0 over M1 margin is positive but narrow,
so the manuscript should describe it as directional reproduction rather than
strong dominance.

Amazon binary outputs exist, but the validation-calibrated paper-grade binary
protocol is incomplete. MovieLens supports the main binary preference claim.
Amazon should not be used to claim fully validated cross-dataset preference
specialization unless a later approved evaluation fills that gap.

The SASRec comparison is sample-exposure aware, not strictly compute matched.
The current evidence distinguishes closest N-task exposure from high sequential
exposure, but it does not equalize FLOPs, wall-clock time, model capacity, or
all optimization conditions. This limitation is part of the paper's baseline
positioning rather than a reason to collapse the two regimes.

The study uses two datasets, and both contain textual item identities. MovieLens
may benefit from pretrained movie knowledge, while Amazon Musical Instruments
may have different text and popularity structure. The completed cold/tail
analysis is diagnostic and does not support a universal cold-start claim.
