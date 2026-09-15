# Discussion

The main empirical lesson is that recommendation supervision is not a neutral
adaptation signal. In this study, preference supervision and next-item
supervision ask related but non-identical questions. The Y task asks whether a
user is likely to like an item given the history. The N task asks which item is
the next observed interaction among a candidate set. A deployed recommender may
need both signals, but the experiments show that they do not collapse into the
same scoring behavior. A candidate-wise P(Yes) score can be a useful preference
interface without becoming a reliable substitute for candidate-label
next-interaction ranking.

The M1 results place multi-task tuning in a more specific light. A single model
can preserve both interfaces well enough to be operationally attractive, but
the current evidence does not show that unification removes specialization.
On MovieLens, M1 remains close to N-K0 under PopMatch-k5, yet N-K0 keeps the
ranking advantage across all three seeds. On Amazon, the same direction appears
under seed42, although the N-K0 margin over M1 is narrow. The supported
interpretation is therefore a tradeoff: M1 is a compact unified adapter, while
Y-K0 and N-K0 remain the cleaner task-specific references for their respective
interfaces.

The SASRec comparison also depends on how supervision exposure is defined.
Under closest N-task sample exposure, N-K0 is far stronger than SASRec on both
MovieLens and Amazon. Under high sequential-supervision exposure, SASRec
overtakes N-K0 on MovieLens. These two facts are not contradictory because they
belong to different budget regimes. The results are consistent with the view
that language-model pretraining and instruction-style conditioning can provide
useful priors when task-specific sequential supervision is limited, whereas a
specialized sequential model can benefit substantially from much larger
sequential exposure. The current experiments support this as an interpretation
of the observed regimes, not as a causal mechanism.

Candidate construction explains another source of instability in offline
conclusions. Random-k5 often makes ranking appear easier, while PopMatch-k5
and candidate-size stress tests expose separations that are muted or absent
under random negatives. This matters because the study is not only comparing
model rows; it is comparing what different evaluation protocols allow one to
conclude. Reporting candidate-set semantics alongside ranking metrics is
therefore part of the evidence, especially when a model's apparent advantage
changes with candidate difficulty.

The cross-dataset results make the paper more robust, but they should not be
overread. Amazon Musical Instruments reproduces the main ranking-side
directions in seed42: N-K0 is above Y-K0 P(Yes)-based ranking, above M1 by a
small margin under PopMatch-k5, and above closest-exposure SASRec by a large
margin. It does not provide validation-calibrated binary evidence or Amazon
multi-seed stability, and high-exposure SASRec was not run there. The second
dataset therefore supports the scope of the empirical story without converting
it into a universal claim about all domains or all budget regimes.
