# Discussion

The results suggest that recommendation supervision should be treated as a
semantic choice rather than a generic adaptation signal. Preference supervision
asks whether a user is likely to like an item given the history. Next-item
supervision asks which item is the next observed interaction among candidates.
These objectives can be related in real recommender systems, but the
experiments show that they do not collapse into the same scoring behavior. A
candidate-wise P(Yes) score is not trained to resolve the same decision as a
candidate-label next-item score.

The multi-task findings are best understood as a unification tradeoff. M1 keeps
both interfaces available and is therefore operationally attractive. At the
same time, it does not eliminate specialization: Y-K0 remains the cleaner
preference specialist and N-K0 remains the cleaner ranking specialist in the
completed evidence. This is not a negative result for multi-task learning. It
is a boundary on what the current unified construction establishes. The
evidence supports retention of both abilities, not positive transfer beyond
both specialists.

The SASRec comparison shows why budget language has to be precise. Under
closest N-task exposure, N-K0 is much stronger than SASRec on both MovieLens
and Amazon. Under high sequential exposure, SASRec becomes stronger than N-K0
on MovieLens. One possible explanation is that LLM pretraining and language-
conditioned parameterization provide useful priors when sequential supervision
is limited, whereas a specialized sequential model can exploit large amounts
of repeated sequential training more effectively. This explanation is a
hypothesis, not a causal mechanism proved by the current experiments.

Candidate construction is another source of apparent contradiction. Random-k5
can make recommendation ranking look easier than it is, while PopMatch-k5 and
candidate-size stress tests expose different separations between models. The
paper therefore frames evaluation protocol as part of the empirical object. A
leaderboard without candidate-set semantics would hide a central result of the
study.
