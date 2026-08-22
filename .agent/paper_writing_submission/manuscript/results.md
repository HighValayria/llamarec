# Results

## 6.1 Preference and Next-item Supervision Learn Different Capabilities

RQ1 asks whether preference supervision and next-item supervision teach the
same recommendation capability. MovieLens-1M gives the clearest answer because
it contains both validation-calibrated binary evidence and ranking evidence.
On the binary preference task, Y-K0 improves over the zero-shot base model:
Y-K0 reaches AUC 0.7691 and validation-calibrated F1 0.7831, compared with
base AUC 0.6205 and F1 0.7414. M1 reaches a similar binary operating point,
with AUC 0.7669 and F1 0.7818 under the canonical paper-ready binary report.
These results show that the preference interface is learnable and useful.

The ranking results separate that finding from next-item selection. Under
MovieLens PopMatch-k5, Y-K0 ranked by P(Yes) reaches HR@1 0.1854, NDCG@5
0.5802, and MRR 0.4443. N-K0, which is trained for candidate-label next-item
selection, reaches HR@1 0.5447, NDCG@5 0.7878, and MRR 0.7171 on the same
candidate protocol. The gap is not evidence that Y-K0 is a poor preference
model. It shows that a candidate-wise preference score does not substitute for
a next-interaction scoring interface.

Amazon Musical Instruments reproduces the ranking-side separation in seed42.
Under PopMatch-k5, Y-K0 P(Yes)-based ranking reaches HR@1 0.2298, NDCG@5
0.6100, and MRR 0.4830. N-K0 reaches HR@1 0.4669, NDCG@5 0.7420, and MRR
0.6570. Amazon binary outputs exist, but they are diagnostic-only for the
current paper because the validation-calibrated Amazon binary protocol is not
documented as a paper-grade artifact. The cross-dataset claim is therefore
limited to ranking-side task-interface separation.

## 6.2 Multi-task Unification Retains Both Abilities but Does Not Remove Specialization

RQ2 asks whether one adapted LLM can retain both recommendation capabilities.
The strongest completed unified condition is M1. On MovieLens, M1 nearly
retains the Y-side binary operating point while exposing an M-N candidate-label
ranking path. Under PopMatch-k5, M1 reaches HR@1 0.5244, NDCG@5 0.7785, and
MRR 0.7047. This places it close to the N-task specialist, but not above it:
N-K0 reaches HR@1 0.5447, NDCG@5 0.7878, and MRR 0.7171 in the same protocol.

The ranking gap is stable across MovieLens seeds. N-K0 exceeds M1 on
PopMatch-k5 for seeds 42, 43, and 44, with HR@1 margins of 0.0227, 0.0208, and
0.0104. The margin narrows in seed44, but the direction does not reverse.
This supports a tradeoff interpretation. M1 is useful when a single model must
serve both interfaces, but the evidence does not show positive transfer beyond
the strongest task-specific specialists.

Amazon gives directional but narrower support. Under PopMatch-k5 seed42,
N-K0 reaches HR@1 0.4669, while M1 reaches HR@1 0.4582. The HR@1 margin is
0.0087, with NDCG@5 and MRR margins of 0.0036 and 0.0049. The specialist-over-
unified direction therefore reproduces, but the Amazon margin is small and
should be reported cautiously rather than presented as a strong dominance
claim.

## 6.3 Harder Candidate Sets Reveal Evaluation Weaknesses Hidden by Random Negatives

RQ3 asks whether the candidate protocol changes the conclusion. Random-k5 is a
useful reference condition, but it is not strong enough to carry the main
ranking claim alone. On MovieLens, N-K0 reaches HR@1 0.7189 under canonical
Random-k5 and 0.5447 under PopMatch-k5. M1 similarly moves from HR@1 0.6950 to
0.5244. The lower PopMatch numbers do not simply weaken the story; they make
the protocol more credible by reducing popularity-matched distractor shortcuts.

Candidate-size stress creates a different pressure. In MovieLens Random-k20,
N-K0 reaches HR@1 0.4164 while M1 reaches 0.3711. In Random-k50, N-K0 reaches
0.1995 while M1 reaches 0.1219. The N-K0 over M1 margin grows from 0.0203
under PopMatch-k5 to 0.0453 under k20 and 0.0775 under k50. The important
result is not merely that all models score lower when there are more
candidates. The larger candidate sets change model separation and therefore
change the interpretation of robustness.

Amazon supports the same protocol caution. Under Random-k5, N-K0 and M1 are
nearly tied, with an HR@1 margin of only 0.0012. Under PopMatch-k5, the N-K0
margin grows to 0.0087. The absolute gap remains narrow, but the pattern shows
why Random-k5 should be treated as supplemental: it can hide differences that
become visible under a more controlled candidate construction.

## 6.4 Model Comparison Changes with Supervision Exposure

RQ4 asks how recommendation-tuned LLMs compare with SASRec. The answer depends
on the supervision exposure regime. Under roughly matched N-task sample
exposure on MovieLens, N-K0 uses 12,000 N-task exposures and SASRec closest-
exposure uses 11,776 exposures. N-K0 reaches HR@1 0.5466, NDCG@5 0.7885, and
MRR 0.7180, while SASRec reaches HR@1 0.2700, NDCG@5 0.6349, and MRR 0.5157.
The MovieLens multi-seed study preserves this direction across seeds 42, 43,
and 44, with minimum HR@1 margin 0.2767.

The high-exposure SASRec regime gives the complementary fact. MovieLens SASRec
with 1,534,656 N-task exposures reaches HR@1 0.6243, NDCG@5 0.8284, and MRR
0.7709 in seed42. Across MovieLens seeds 42, 43, and 44, high-exposure SASRec
remains above N-K0 with minimum HR@1 margin 0.0777. The paper therefore should
not ask which model is universally better. The supported claim is that N-K0 is
much stronger under limited or approximately matched N-task exposure, whereas
SASRec can surpass it after substantially more sequential supervision.

Amazon seed42 supports the closest-exposure direction. Under PopMatch-k5,
N-K0 reaches HR@1 0.4669, NDCG@5 0.7420, and MRR 0.6570. SASRec closest-
exposure reaches HR@1 0.1757, NDCG@5 0.5685, and MRR 0.4295. The HR@1 margin
is 0.2912. Amazon high-exposure SASRec was not evaluated, so the high-exposure
part of Claim 4 remains MovieLens-only.

## 6.5 Cross-dataset Validation

RQ5 asks which MovieLens findings reproduce on Amazon Musical Instruments.
The Amazon seed42 PopMatch-k5 results reproduce three ranking-side directions.
Y-K0 P(Yes)-based ranking is below N-K0, with HR@1 0.2298 versus 0.4669. N-K0
is above M1, with HR@1 0.4669 versus 0.4582, although the margin is narrow.
N-K0 is far above closest-exposure SASRec, with HR@1 0.4669 versus 0.1757.

Amazon also shows that the candidate protocol matters. Random-k5 leaves N-K0
and M1 nearly tied, while PopMatch-k5 creates a clearer although still modest
separation. This does not make Amazon a full replication of the MovieLens
package. It is a seed42 cross-domain validation run, not a multi-seed
cross-dataset stability study, and it lacks paper-grade validation-calibrated
binary reporting. Its role is to test whether the main ranking-side directions
survive a second domain.

## 6.6 Stability and Diagnostic Findings

The MovieLens stability study distinguishes main claims from diagnostics.
Y-K0 binary F1 is available across three seeds with a range of 0.0098. N-K0
remains above M1 on PopMatch-k5 ranking in every seed. N-K0 remains above
closest-exposure SASRec in every seed. High-exposure SASRec remains above
N-K0 in every seed. These are the stable directions that belong in the main
paper narrative.

Cold/tail and order diagnostics qualify the narrative without replacing it.
N-K0 exceeds M1 in every target-popularity bucket, but the coldest bucket has
only 26 samples and should not become a headline claim. High-exposure SASRec's
advantage over N-K0 is mainly middle/head driven in the completed slice.
Candidate order perturbations are smaller than candidate-size effects, so they
are best reported as appendix support for protocol robustness.
