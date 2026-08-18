# Results Draft

## 4.1 Preference And Next-item Supervision Learn Different Semantics

We first separate the binary preference interface from the candidate-label
ranking interface. On MovieLens-1M, Y-K0 improves the binary preference task
over the zero-shot base model: under validation-calibrated reporting, Y-K0
reaches AUC 0.7691 and F1 0.7831, compared with base AUC 0.6205 and F1 0.7414.
M1 reaches a comparable binary operating point, with AUC 0.7669 and F1 0.7818.
These results show that the adapted models learn the binary preference signal.

The same supervision does not transfer cleanly to candidate-label ranking. Under
Canonical Random-k5, N-K0 reaches HR@1 0.7189, NDCG@5 0.8773, and MRR 0.8356,
whereas Y-K0's P(Yes)-based ranking reaches HR@1 0.3048, NDCG@5 0.6504, and MRR
0.5366. The gap widens under PopMatch-k5: N-K0 reaches HR@1 0.5447, while Y-K0
falls to HR@1 0.1854. We therefore treat preference prediction and next-item
ranking as distinct task interfaces rather than interchangeable evaluation
views.

## 4.2 Multi-task Training Gives A Unified Tradeoff, Not A Ranking Win

Among the tested multi-task variants, M1 is the strongest unified setting. It
retains near-Y-K0 binary quality while providing a strong M-N candidate-label
ranking interface. Under Canonical Random-k5, M1 reaches HR@1 0.6950, NDCG@5
0.8674, and MRR 0.8223. Under PopMatch-k5, M1 reaches HR@1 0.5244, NDCG@5
0.7785, and MRR 0.7047.

N-K0 remains the ranking specialist. Under PopMatch-k5, N-K0 exceeds M1 by HR@1
0.0203 in the seed-42 run, and the multi-seed study preserves the direction
across seeds 42, 43, and 44 with a minimum HR@1 margin of 0.0104. The appropriate
paper claim is therefore not that multi-task training dominates ranking, but
that M1 is the best current compromise when both preference prediction and
candidate-label ranking are needed.

## 4.3 Harder Candidate Controls Reduce Popularity Shortcut Concerns

Canonical Random-k5 is useful as a standard offline diagnostic, but it is too
easy to interpret alone. Popularity and BPR-MF baselines are strong under the
canonical random candidate protocol and then drop sharply under PopMatch-k5. For
example, the popularity N-train baseline decreases from HR@1 0.5663 under
canonical random-k5 to HR@1 0.3226 under PopMatch-k5. BPR-MF similarly decreases
from HR@1 0.5611 to HR@1 0.3352.

The LLM ranking models remain above these baselines under PopMatch-k5. N-K0
exceeds popularity N-train by HR@1 0.2220 and BPR-MF by HR@1 0.2095; M1 exceeds
the same baselines by HR@1 0.2018 and 0.1893, respectively. Candidate-size
stress tests are directionally consistent: N-K0 remains above M1 at k20 and k50,
with HR@1 margins of 0.0453 and 0.0775. These controls do not eliminate every
shortcut explanation, but they make the main ranking pattern less dependent on
easy random negatives.

## 4.4 SASRec Comparisons Depend On The Budget Regime

The SASRec comparison has to be read through the training budget. Under roughly
matched N-task sample exposure, SASRec s23 uses 11,776 N-task exposures against
the 12,000-exposure N-K0 anchor. In this regime, N-K0 is much stronger: seed-42
HR@1 is 0.5466 for N-K0 and 0.2700 for SASRec s23. The sample-efficiency curve
shows the same direction at lower and higher matched exposure points: N-K0
outperforms the closest-exposure SASRec point across the roughly 3k, 6k, 12k,
and 24k N-exposure comparisons.

At high exposure, the conclusion changes. SASRec s3000 uses 1,534,656 N-task
exposures, about 127.9 times the N-K0 exposure, and reaches HR@1 0.6243 in
seed 42. In the multi-seed study, high-exposure SASRec remains above N-K0 in
every seed, with a minimum HR@1 margin of 0.0777. The paper should therefore
state a budget-conditioned result: the LLM adapter is more sample efficient in
the low-exposure matched diagnostic, while heavily trained SASRec is the
stronger high-exposure sequential recommender.

## 4.5 Cold/Tail Slices Qualify Where The Gains Appear

The cold/tail diagnostic adds a popularity-conditioned view of the PopMatch-k5
ranking results. N-K0 exceeds M1 in every item-popularity bucket, with HR@1
margins from 0.0168 in the head bucket to 0.0905 in the 11-50 bucket. This
supports the interpretation that N-K0's ranking advantage is not confined to a
single head-only slice.

The high-exposure SASRec advantage over N-K0 is mainly middle/head driven. It is
negative in the smallest `<=10` bucket, but that bucket contains only 26 samples,
so it should not be elevated into a primary claim. The safer use is as a
limitation and diagnostic: high-exposure SASRec is strongest overall, but the
completed slice does not prove uniform dominance in the coldest item region.

## 4.6 Stability Across Seeds

The main directions are stable across seeds 42, 43, and 44. Y-K0 binary F1 has a
range of 0.0098. N-K0 remains above M1 on PopMatch-k5 ranking in every seed.
N-K0 also remains above the sample-exposure-matched SASRec point in every seed,
with HR@1 margins above 0.2766. Conversely, high-exposure SASRec remains above
N-K0 in every seed, with HR@1 margins above 0.0777.

This stability study strengthens the result narrative by separating robust
directions from single-run diagnostics. The stable directions are suitable for
main-text claims; coldest-bucket behavior, exact order-sensitivity numbers, and
unreplicated variant details should remain in diagnostic or appendix language.
