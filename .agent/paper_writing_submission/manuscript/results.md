# Results

## 6.1 Preference and Next-item Supervision Learn Different Capabilities

RQ1 asks whether preference supervision and next-item supervision teach the
same recommendation capability. MovieLens-1M is the main evidence source for
this question because it contains both validation-calibrated binary evaluation
and controlled candidate-ranking evaluation. On the binary preference task,
Y-K0 reaches AUC 0.7691 and validation-calibrated F1 0.7831, compared with the
zero-shot base model's AUC 0.6205 and F1 0.7414. M1 reaches a similar binary
operating point, with AUC 0.7669 and F1 0.7818 in the canonical paper-ready
binary report. These results establish that the preference interface can be
adapted successfully under the completed MovieLens protocol.

The ranking task separates that finding from next-item selection. Under
MovieLens PopMatch-k5, Y-K0 ranked by the candidate-wise P(Yes) score reaches
HR@1 0.1854, NDCG@5 0.5802, and MRR 0.4443. N-K0, trained for candidate-label
next-item selection, reaches HR@1 0.5447, NDCG@5 0.7878, and MRR 0.7171 on the
same candidate protocol. This gap should not be read as a failure of Y-K0 as a
preference model. It shows that a preference score and a next-interaction
score answer different ranking questions, even when both are evaluated over
the same user history and candidate set.

Amazon Musical Instruments gives a second-domain check of the ranking-side
separation. Under PopMatch-k5 seed42, Y-K0 P(Yes)-based ranking reaches HR@1
0.2298, NDCG@5 0.6100, and MRR 0.4830, while N-K0 reaches HR@1 0.4669,
NDCG@5 0.7420, and MRR 0.6570. Amazon binary outputs exist only as
diagnostics in the current package because the validation-calibrated Amazon
binary protocol is not documented as a paper-grade artifact. The cross-dataset
claim for RQ1 is therefore limited to ranking-side interface separation.

## 6.2 Multi-task Unification Retains Both Abilities but Does Not Remove Specialization

RQ2 asks whether one adapted LLM can retain both recommendation capabilities.
The strongest completed unified condition is M1. On MovieLens, M1 preserves a
Y-side binary operating point close to Y-K0 while also exposing an M-N
candidate-label ranking path. Under PopMatch-k5, M1 reaches HR@1 0.5244,
NDCG@5 0.7785, and MRR 0.7047. N-K0 remains higher in the same protocol, with
HR@1 0.5447, NDCG@5 0.7878, and MRR 0.7171.

The specialist-over-unified ranking direction is stable across MovieLens
seeds. N-K0 exceeds M1 on PopMatch-k5 for seeds 42, 43, and 44, with HR@1
margins of 0.0227, 0.0208, and 0.0104. The margin narrows in seed44, but the
direction does not reverse. This supports a tradeoff interpretation: M1 is
useful when a single adapter must serve both interfaces, while the completed
evidence does not show positive transfer beyond the strongest task-specific
models.

Amazon provides the same direction with a smaller margin. Under PopMatch-k5
seed42, N-K0 reaches HR@1 0.4669 and M1 reaches HR@1 0.4582. The HR@1 margin
is 0.0087, with NDCG@5 and MRR margins of 0.0036 and 0.0049. The result is
consistent with the MovieLens tradeoff pattern, but its size and single-seed
status make it directional support rather than a strong cross-dataset
dominance claim.

## 6.3 Harder Candidate Sets Reveal Evaluation Weaknesses Hidden by Random Negatives

RQ3 asks whether the candidate protocol changes the conclusion drawn from a
ranking experiment. Random-k5 is useful as an easy-negative reference, but it
is too permissive to carry the main robustness claim alone. On MovieLens, N-K0
reaches HR@1 0.7189 under canonical Random-k5 and 0.5447 under PopMatch-k5.
M1 moves from HR@1 0.6950 to 0.5244 across the same protocol change. The lower
PopMatch values do not merely make the task harder; they reduce the chance
that a model is rewarded for distinguishing targets from popularity-mismatched
distractors.

Candidate-size stress adds a second source of difficulty. In MovieLens
Random-k20, N-K0 reaches HR@1 0.4164 while M1 reaches 0.3711. In Random-k50,
N-K0 reaches 0.1995 while M1 reaches 0.1219. The N-K0 over M1 HR@1 margin
increases from 0.0203 under PopMatch-k5 to 0.0453 under k20 and 0.0775 under
k50. The result is therefore not only that larger candidate sets lower all
scores. Larger sets also change model separation, which changes the
interpretation of robustness.

Amazon supports the same protocol caution. Under Random-k5, N-K0 and M1 are
nearly tied, with an HR@1 margin of 0.0012. Under PopMatch-k5, the N-K0 margin
increases to 0.0087. The absolute gap remains narrow, but the pattern explains
why Random-k5 is treated as supplemental: it can hide differences that become
visible under a more controlled candidate construction. Figure 3 visualizes the
same point from the paper-facing robustness table: Random-k5 is shown as a
reference setting, while PopMatch-k5 and larger candidate sets expose harder
ranking conditions and larger model separation.

## 6.4 Model Comparison Changes with Supervision Exposure

RQ4 asks how recommendation-tuned LLMs compare with SASRec. The comparison
depends on the supervision exposure regime. Under roughly matched N-task sample
exposure on MovieLens, N-K0 uses 12,000 N-task exposures and the closest-
exposure SASRec row uses 11,776 exposures. N-K0 reaches HR@1 0.5466, NDCG@5
0.7885, and MRR 0.7180, while SASRec reaches HR@1 0.2700, NDCG@5 0.6349, and
MRR 0.5157. The MovieLens multi-seed study preserves this direction across
seeds 42, 43, and 44, with minimum HR@1 margin 0.2767.

The high-exposure SASRec anchor gives a complementary but narrower result.
MovieLens SASRec with 1,534,656 N-task exposures reaches HR@1 0.6243,
NDCG@5 0.8284, and MRR 0.7709 in seed42. Across MovieLens seeds 42, 43,
and 44, these high-exposure SASRec checkpoints remain above the current
N-K0 checkpoint, whose N-task exposure is about 12,000, with minimum HR@1
margin 0.0777. We did not train or evaluate N-K0 at the same 1.53M exposure.
The supported conclusion is therefore not a completed high-budget head-to-head
frontier: N-K0 is much stronger under approximately matched N-task exposure,
while SASRec can surpass the current low-exposure N-K0 checkpoint after
substantially more sequential supervision.

Amazon seed42 supports only the closest-exposure part of this comparison.
Under PopMatch-k5, N-K0 reaches HR@1 0.4669, NDCG@5 0.7420, and MRR 0.6570.
The closest-exposure SASRec row reaches HR@1 0.1757, NDCG@5 0.5685, and MRR
0.4295, giving an HR@1 margin of 0.2912. Amazon high-exposure SASRec was not
evaluated, so no cross-dataset claim is made about that regime. Figure 2
keeps this boundary visible by plotting the MovieLens sample-exposure curve
and showing Amazon only as a closest-exposure seed42 comparison, with the
Amazon high-exposure SASRec point explicitly absent.

## 6.5 Cross-dataset Validation

RQ5 asks which MovieLens findings directionally reproduce on Amazon Musical
Instruments. The Amazon seed42 PopMatch-k5 results preserve three ranking-side
directions. Y-K0 P(Yes)-based ranking is below N-K0, with HR@1 0.2298 versus
0.4669. N-K0 is above M1, with HR@1 0.4669 versus 0.4582, although the margin
is narrow. N-K0 is also far above closest-exposure SASRec, with HR@1 0.4669
versus 0.1757.

Amazon also reinforces the candidate-protocol result. Random-k5 leaves N-K0
and M1 nearly tied, while PopMatch-k5 creates a clearer but still modest
separation. This does not make Amazon a full replication of the MovieLens
evidence package. It is a seed42 cross-domain validation run, not a multi-seed
cross-dataset stability study, and it lacks paper-grade validation-calibrated
binary reporting. Its role is to test whether the main ranking-side directions
survive a second domain.

## 6.6 Stability and Diagnostic Findings

The MovieLens stability study separates main claims from diagnostics. Y-K0
binary F1 is available across three seeds with a range of 0.0098. N-K0 remains
above M1 on PopMatch-k5 ranking in every seed. N-K0 remains above
closest-exposure SASRec in every seed. High-exposure SASRec remains above
N-K0 in every seed. These repeated directions are the stability evidence that
belongs in the main paper narrative.

Cold/tail and order diagnostics qualify the narrative without replacing it.
N-K0 exceeds M1 in every target-popularity bucket, but the coldest bucket has
only 26 samples and should not become a headline claim. High-exposure SASRec's
advantage over N-K0 is mainly middle/head driven in the completed slice.
Candidate-order perturbations are smaller than candidate-size effects, so they
are best reported as appendix support for protocol robustness rather than as a
separate main claim.
