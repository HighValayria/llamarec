# ICECAI 2026 Final Scientific Review Packet

## Review Mandate

You are the FINAL SCIENTIFIC JUDGE. Review scientific correctness, claim-evidence fit, coherence, and submission readiness. Do not act as a copy editor, venue secretary, formatting reviewer, or compression editor. Author information and the disabled GenAI disclosure slot are `DEFERRED_USER_METADATA` and must not count as failures.

Current English PDF: `F:/Projects/llamarec/paper/builds/icecai_2026/en/main.pdf` (10 pages).

Required verdict: exactly one of `ACCEPT_SCIENTIFIC_FREEZE`, `MINOR_REPAIR_BEFORE_FREEZE`, or `MAJOR_REPAIR_REQUIRED`; then enumerate P0/P1/P2/P3 findings. P0 is a scientific correctness blocker. P1 is a claim/evidence/method issue that should be fixed before submission. P2 is worth improving but safe to submit unchanged. P3 is editorial preference only. If P0=0 and P1=0, accept the scientific freeze even if P2/P3 exist.

## 1. Paper Title

**Recommendation Supervision Semantics and Exposure-Aware Evaluation for Recommendation-Tuned LLMs**

## 2. Abstract

Empirical conclusions about large language models (LLMs) for recommendation can depend on what is supervised, how much downstream supervision a model consumes, and how candidates are evaluated. We study these dependencies using Llama-3.2-3B-Instruct with QLoRA, taking MovieLens-1M as the main dataset and Amazon Musical Instruments as a directional ranking-side check. We compare rating-derived preference prediction (Y), next-interaction prediction (N), and a shared Y+N multitask adapter (M1), trace task-sample exposure, evaluate alternative candidate protocols, and compare N-trained LlamaRec with SASRec at approximately matched downstream exposures. The complete Y and N formulations yield distinct measured capability profiles. In the MovieLens seed42 trajectory, Y's measured gains through 96k are limited or uneven, whereas N ranking improves across measured validation and test points through 200k. Under standard k5 evaluation, the N-specialist-M1 validation gap narrows substantially from 48k to 96k per task. The 96k small-gap regime is reproduced across three training seeds; held-out tests nevertheless retain a modest N advantage, while M1 preserves comparable Y-side preference capability. Alternative candidate protocols materially change the remaining specialist-multitask gap. N-trained LlamaRec leads the evaluated SASRec baseline at four approximately matched downstream task-sample exposure points, but SASRec improves strongly and the gap narrows at 200k. Key ranking directions also appear on Amazon at earlier seed42 operating points. These results show that recommendation capability and relative model performance are conditional on prediction formulation, cumulative downstream exposure, and candidate evaluation protocol.

## 3. Contribution Hierarchy

- **C2 PRIMARY:** exposure-conditioned specialist/shared relationship. MovieLens seed42 traces the trajectory; standard-k5 validation narrows from 48k to 96k per task. Seeds 43/44 replicate only the resulting 96k small-gap operating point. Frozen tests across all three seeds retain a modest N advantage. M1 preserves comparable measured Y-side preference capability at 96k.
- **C4 SECONDARY:** four-point approximately matched downstream task-sample exposure comparison between N-trained LlamaRec and SASRec (24k, 48k, 96k, 200k). N leads at each evaluated point; SASRec improves strongly and the later gap narrows.
- **C3 SUPPORTING:** candidate-protocol boundary. k20 exposes a much larger remaining N-specialist gap than k5; k50 favors N but is smaller than k20 and seed-sensitive. Protocols are separately constructed and non-nested.
- **C1 FRAMING:** supervision formulation defines prediction capability. Y and N are complete formulations with different targets, data construction, prompts, and scoring interfaces, not an isolated semantic-label intervention.

## 4. Research Questions

- **RQ1:** How do observed capability profiles under rating-derived preference prediction (Y) and next-interaction prediction (N) differ across native and bridge evaluations?
- **RQ2:** How do Y and N respond to cumulative task-sample exposure within their own interfaces?
- **RQ3:** At matched per-task exposure, how closely does shared Y+N adapter M1 approach the corresponding Y and N specialists?
- **RQ4:** Does the standard PopMatch-k5 specialist-M1 relationship persist under alternative candidate protocols?
- **RQ5:** How does N-trained LlamaRec versus SASRec change across approximately matched downstream task-sample exposure points?

## 5. Task Definitions: Y, N, and M1

- **Y:** estimates `P(Like | H10, i)`. Ratings >=4 map to Yes and lower ratings to No. All rating levels remain in histories and targets. Native evaluation is rating-derived class discrimination (AUC/F1/accuracy). Y-as-ranker independently scores candidates with `P(Yes)` and is a bridge, not the native Y task.
- **N:** estimates `P(NextInteraction=i | H10, C)`. The set contains the observed next item and fixed distractors; the answer is the target candidate label. All rating levels are eligible. A distractor is not a confirmed dislike, and previously encountered items remain eligible.
- **M1:** one shared adapter, task-specific prompts and answer spaces, Y/N examples interleaved 1:1. M-Y and M-N reuse the Y/N scoring routes. Each specialist is compared with the corresponding M1 interface at matched task exposure; M1 total exposure sums both tasks.

## 6. Temporal and Leakage Rules

- `H(u,t)` contains only interactions strictly before target time `t`; prompts retain at most the 10 most recent eligible events (`H10`).
- Sequences are grouped into timestamp buckets. Same-bucket Y targets share only preceding history. Last bucket supplies Y test, previous bucket validation, and earlier buckets training; a held-out Y bucket may yield several targets.
- N requires prior history and one unique next item. Multi-interaction buckets are skipped as N targets but retained in later histories. The last two legal N examples become validation/test; earlier legal examples form training.

## 7. Training and Exposure Definition

- Llama-3.2-3B-Instruct with QLoRA over frozen 4-bit NF4; rank-16 LoRA, alpha 32, dropout 0.05, q/k/v/o and gate/up/down projections; gradient checkpointing; max length 2,048.
- Instruction-chat examples use response-only loss: prompt/padding tokens are masked. Effective batch is 8. Inference scores allowed-answer likelihood; multi-token answers use complete-sequence log-likelihood.
- Task-sample exposure is cumulative consumed examples for task q, including repetitions. It is neither unique interactions nor computation. Specialists consume 24k/48k/96k; N also has 200k. M1-48/M1-96 have expected per-task exposure 48k/96k and total 96k/192k, conditional on correct resume skipping.
- N200 consumes 200,000 of 212,725 legal N examples (about 94.0%) and is a near-one-pass anchor, not convergence. SASRec actual consumptions are 24,064/48,128/96,256/200,000; these approximately match task-sample exposure, not compute.

## 8. MovieLens Main Evidence

- Y: 6,040 users, 976,284 train, 12,381 validation, 11,544 test. N: 5,675 users, 212,725 train, 5,675 validation, 5,675 test.
- RQ1: Y96 native validation AUC=0.78435. Y96 bridge PopMatch-k5 validation HR@1=0.22115 versus N96 native HR@1=0.62379. This is a complete-formulation capability contrast, not universal N superiority.
- RQ2 Y validation AUC is 0.77613/0.78161/0.78435 at 24k/48k/96k; F1 and bridge ranking do not improve uniformly. Supported wording: limited or uneven, not saturated.
- RQ2 N PopMatch-k5 validation HR@1 is 0.57744/0.60300/0.62379/0.65163 at 24k/48k/96k/200k; test is 0.56123/0.58696/0.61004/0.62819. Improvement is limited to evaluated points through 200k.
- Seed42 M1-N test HR@1 is 0.57762 at 48k per task and 0.59736 at 96k; N is 0.58696 and 0.61004. Validation gaps narrow from 0.00881 to 0.00035; only validation supports the narrowing claim.

## 9. Multiseed 96k Evidence

- Seeds 42/43/44 independently train Y96, N96, M1-96 only at 96k; they do not form a multiseed exposure trajectory.
- Y-side validation mean deltas `M1-Y - Y96`: AUC +0.00482 (SD 0.00365, +/+/+), F1 +0.00455 (SD 0.00094, +/+/+), accuracy +0.00334 (SD 0.00376, +/+/-). This supports comparable measured capability, not equivalence or general positive transfer.
- k5 validation mean deltas `N96 - M1-N`: HR@1 +0.00587 (SD 0.00767), NDCG@5 +0.00277, MRR +0.00371; all +/+/+.
- Frozen-test k5 mean deltas: HR@1 +0.01016 (SD 0.00247), NDCG@5 +0.00501, MRR +0.00665; all +/+/+. Every seed retains a modest N advantage on test.

## 10. Candidate-Protocol Evidence

- k20 three-seed HR@1 mean deltas `N96-M1-N`: validation +0.08164 (SD 0.03066), test +0.07765 (SD 0.03448); every seed/all ranking metrics favor N.
- k50 HR@1 mean deltas: validation +0.01028 (SD 0.00687), test +0.01010 (SD 0.00452). Every seed favors N, but magnitude is smaller than k20 and seed-dependent.
- Non-monotonic anchor: seed43 test HR@1 is +0.00775 at k5 and +0.00511 at k50.
- k5 is popularity-matched; k20/k50 random. Protocols are separately constructed and non-nested. Count, composition, sampling, and difficulty vary jointly; no candidate-count causal claim.
- Seed42 paired-bootstrap HR@1 intervals: k5 validation [-0.01040, 0.01128], test [0.00159, 0.02379]; k20 validation [0.10185, 0.12317], test [0.10396, 0.12511]; k50 validation [0.01251, 0.02185], test [0.00916, 0.01885].

## 11. SASRec Exposure Comparison

- Same PopMatch-k5 candidates within each split; validation guides decisions and frozen test is held-out evidence. SASRec is a full-item next-target classifier scored on fixed candidate lists.
- Validation HR@1 `(N, SASRec, delta)`: 24k `(0.57744, 0.27313, +0.30432)`; 48k `(0.60300, 0.29304, +0.30996)`; 96k `(0.62379, 0.32811, +0.29568)`; 200k `(0.65163, 0.47489, +0.17674)`.
- Test deltas are +0.27084/+0.28476/+0.27912/+0.17709. N leads at all evaluated points; SASRec improves strongly and the largest-exposure gap narrows.
- No universal sample-efficiency, compute/resource-efficiency, pretraining-fairness, or general-superiority claim.

## 12. Amazon Directional Evidence

- Amazon Musical Instruments uses seed42 full-test PopMatch-k5 at available earlier points only (57,439 examples).
- HR@1: base 0.35730, Y 0.22979, N 0.46688, M1 0.45817, SASRec 0.17566. N exceeds M1 by +0.00870.
- Directional ranking support only: no exposure trajectory, three-seed 96k, hard-candidate, N/SASRec four-point, or native-preference replication.

## 13. Statistical Treatment

- Seed42 paired user bootstrap resamples users and aligned examples for both fixed models. Percentile 95% intervals describe fixed-model evaluation-sample uncertainty. Replicates=5,000; seed=20260902; provenance is resolved from artifact/code identity though exact shell invocation was not retained.
- Seeds 42/43/44 equal-weight means and sample SD (`n=3`, `ddof=1`) describe training-run variability, not confidence intervals, significance tests, or multiplicity-adjusted inference.
- Zero-crossing intervals do not establish equivalence. No equivalence margin or all-comparison multiplicity adjustment was used.

## 14. Main Limitations

- **Statistics/training:** only 96k has three seeds; trajectories are seed42-only; no cross-seed significance/equivalence/multiplicity claim; behavior beyond Y96/N200 unknown; exposure changes coverage and optimization history; M1 counts are expected schedule counts without retained per-example trace.
- **Evaluation:** PopMatch-k5 and random k20/k50 are non-nested and vary jointly; PopMatch retrospectively uses full-corpus popularity and removes only one mismatch; sampled ranking is not exhaustive full-catalog evaluation; Y/N differ as complete formulations.
- **External validity:** Amazon supports earlier seed42 ranking directions only; detailed exposure/protocol conclusions remain MovieLens-specific.
- **Resources:** matching task samples does not align pretraining, tokens, updates, FLOPs, wall-clock, latency, or deployment cost.

## 15. Discussion

The Discussion follows the hierarchy: supervision formulation determines which capability a score reflects; cumulative task exposure locates the specialist/shared relation; protocol-conditioned differences delimit standard k5 and prohibit candidate-count causality; and the N/SASRec trajectory requires reporting both N's measured lead and SASRec's continuing improvement while exposure remains only a partial cross-model axis. Amazon closes as directional external support, not replication. Results mainly state what happened; Discussion mainly interprets why claims must remain conditional.

## 16. Conclusion

Paragraph 1 defines the study over complete supervision formulations, cumulative downstream task-sample exposure, and candidate protocols, with Y/N/M1 as different capabilities rather than a causally isolated semantic contrast. Paragraph 2 reports seed42 validation narrowing, 96k-only independent-seed replication, retained frozen-test N advantage, comparable M1 Y-side capability, the four-point N/SASRec trajectory with SASRec improvement, and protocol conditioning without candidate-count causality. Paragraph 3 says claims should jointly report formulation, exposure, and protocol because these conditions define supported capability and relative performance.

## 17. Novelty and Reference-Refresh Positioning

- C1 is not the first preference-versus-next distinction; P5 and ITDR include related interfaces.
- C2 is not the first data-aware multitask/specialist-shared comparison; P5, ITDR, OpenOneRec, Penha et al., and OneReason overlap. The narrower contribution is the measured corresponding-task cumulative-exposure relationship.
- C3 is not the first candidate-sensitivity study; its role is delimiting the higher-exposure N/M1 relation.
- C4 is not the first budget-aware LLM/baseline comparison; its scope is four approximately matched cumulative downstream-consumption points, distinct from selected-example budgets and compute.
- InstructRec TOIS 2025 and RecSys 2024 sequential scaling are publication upgrades of already used works, not new precedents.
- Pereira 2025 supports sampling/evaluation reliability only. Milogradskii 2024 supports replicability and implementation/tuning sensitivity only. Shehzad & Jannach 2025 supports standardized evaluation and strong conventional baselines only; neither is the source of this repository's SASRec implementation.

## 18. Nine-Table / Two-Figure Evidence Map

| Display | Scientific role |
| --- | --- |
| Table I `datasets` | Task-specific splits and legal-example counts. |
| Table II `training_exposure_compact` | Steps, total exposure, and per-task exposure. |
| Table III `supervision_semantics_compact` | Y-native trajectory, bridge ranking, and Y96/N96 endpoints for RQ1/RQ2. |
| Table IV `exposure_scaling` | Seed42 N/M-N validation/test exposure trajectory for RQ2/RQ3. |
| Table V `specialist_multitask` | Seed42 paired-bootstrap validation deltas. |
| Table VI `ms96_delta_summary_compact` | Three-training-seed 96k mean/SD/signs; training-run variability for RQ3/RQ4. |
| Table VII `hard_candidate_compact` | Seed42 paired-bootstrap protocol deltas; fixed-model evaluation-sample uncertainty for RQ3/RQ4. |
| Table VIII `n_vs_sasrec_exposure` | Four-point N/SASRec validation and frozen-test evidence for RQ5. |
| Table IX `cross_dataset` | Amazon earlier-point seed42 directional evidence. |
| Figure 1 `n_native_exposure` | Seed42 N validation exposure trend only; not test evidence. |
| Figure 2 `n_vs_sasrec_exposure` | Seed42 validation N/SASRec trajectory only; not test evidence. |

## Required Review Dimensions

Judge story coherence across title/abstract/introduction/RQs/results/discussion/conclusion; contribution hierarchy; RQ1-RQ5; statistical distinction; novelty positioning; reference-refresh fit; method completeness; evaluation boundaries; table/figure sufficiency; Results-versus-Discussion roles; four-part limitations; and the three-paragraph conclusion. Minor repetition or editorial preference alone must not trigger P1.
