# Executive Summary

Scientific consistency: PARTIAL

Skeleton alignment: PASS

Numeric consistency: PASS

Citation consistency: PARTIAL

Critical issues: 0

Major issues: 0

Minor issues: 6

The manuscript is scientifically well aligned with the frozen evidence and with the synchronized canonical story skeleton. All hard protocol boundaries are stated correctly: Y and N are defined as different prediction problems; prompt histories are limited to the 10 most recent strictly earlier interactions; M1 cross-task safety is described as an evaluation-side restriction; the 48k-to-96k gap-narrowing claim is restricted to seed42 validation; the 96k ranking conclusion is descriptive rather than inferential; candidate protocols are explicitly nonnested; SASRec matching is limited to downstream task-sample exposure; and Amazon is kept as a ranking-direction check.

No numeric mismatch was found. The remaining scientific-language issues are two recurring wording patterns: (1) several claims refer to capabilities or behaviors as "learned" rather than directly measured, and (2) Y-native preference discrimination is called "strong" without a frozen benchmark or threshold establishing that qualitative intensity. Four bibliography entries are uncited in the body. These are narrowing and citation-cleanup issues, not contradictions of the reported experiments.

Audit inputs:

- Current manuscript: `true_paper/paper.docx`, SHA256 `45005b2044553caab3bc6f0163de646a33b44c513125b9422f06e2084e438e9e`.
- Canonical skeleton: `true_paper/PAPER_STORY_SKELETON_CANONICAL.md`, SHA256 `4d6c61657ae2d40b392b4207190da0aa3ef71c7638a1001a3017095886beaaee`.
- Frozen evidence: `paper/evidence/source_of_truth.md`, `paper/evidence/claim_matrix.md`, `paper/evidence/ms96_integration_summary.md`, `paper/evidence/run_metadata_ledger.md`, and the frozen CSV tables under `paper/tables/`.
- Method: read-only DOCX XML extraction including Word math text, citation-range expansion, terminology scan, heading-chain comparison, and direct comparison with frozen tables. No manuscript text was changed and no new external evidence was introduced.

# 1. Abstract

Overall status: NEEDS_NARROWING.

Safe claims:

- The study scope correctly includes Y, N, M1, MovieLens, candidate-protocol checks, the four-point N-SASRec comparison, and Amazon as a ranking-side check.
- "N ranking continues to improve over the evaluated exposure range" is supported by the seed42 24k/48k/96k/200k trajectories on both validation and test.
- "M1 largely preserves Y-side preference capability" is appropriately weaker than equivalence or positive transfer.
- The N-M1 validation narrowing is explicitly limited to seed42 and is explicitly not reproduced on test.
- The 96k three-seed conclusion is limited to a small N ranking advantage.
- The SASRec and Amazon claims include the required scope limitations.

Issue A1:

- Exact quote: "we compare the capabilities learned by Y and N" and "different recommendation objectives can lead to different learned behaviors"
- Status: NEEDS_NARROWING
- Evidence source: `source_of_truth.md` C1; `claim_matrix.md` `results.rq1.*`; canonical skeleton Abstract and Results A.
- Why: The evidence establishes different measured capability profiles for complete supervision formulations. It does not identify an internal learned mechanism or a single causal semantic factor.
- Minimal correction direction: Tie the claim to observed or measured capability/behavior under the evaluated task interfaces.

Issue A2:

- Exact quote: "Y achieves strong native preference discrimination"
- Status: NEEDS_NARROWING
- Evidence source: `binary_exposure.csv` and `semantics_bridge.csv`.
- Why: Y96 validation AUC is 0.7843504067, but the frozen evidence contains no benchmark, calibrated threshold, or comparative test that establishes the qualitative label "strong."
- Minimal correction direction: State the measured Y-native result or use a neutral capability description without an unsupported intensity label.

# 2. Introduction

Overall status: NEEDS_NARROWING.

Safe claims:

- The motivation correctly distinguishes a common language interface from a common prediction objective.
- Task-sample exposure is correctly defined as cumulative consumed examples, including repeats.
- M1 comparisons are correctly framed at matched per-task exposure.
- Candidate protocols, SASRec, and Amazon remain subordinate checks rather than independent primary contributions.
- The Introduction correctly separates seed42 validation narrowing from the held-out test result and the 96k three-seed endpoint.

Issue I1:

- Exact quote: "different recommendation objectives can lead to different learned behaviors"
- Status: NEEDS_NARROWING
- Evidence source: `source_of_truth.md` C1 and canonical skeleton Introduction.
- Why: This repeats the Abstract's internal/causal wording. The controlled evidence supports different observed outcomes under complete task formulations, which also differ in target construction, task data, prompts, and scoring interfaces.
- Minimal correction direction: Restrict the statement to observed or measured capability profiles under the evaluated formulations.

Issue I2:

- Exact quote: "Y achieves strong rating-derived preference discrimination"
- Status: NEEDS_NARROWING
- Evidence source: `binary_exposure.csv`.
- Why: The numerical result is correct, but the adjective "strong" is not operationalized by frozen evidence.
- Minimal correction direction: Anchor the statement to the reported AUC or use a neutral measured-performance description.

# 3. Related Work

Overall status: SAFE.

- The four expected roles are present: LLM recommendation, supervision/task formulation, multitask/unified modeling, and offline evaluation/sequential baselines.
- The section does not claim novelty for the Y/N distinction itself, multitask recommendation generally, hard-candidate evaluation generally, or LLM-SASRec comparison generally.
- The cited works are assigned plausible, distinct argumentative roles based on the manuscript's own reference descriptions. No new literature search was performed, as required.
- The phrase "capabilities learned under one supervision objective" inherits the recurring terminology caution, but in context it refers to cross-interface measured behavior and does not create an additional independent issue.
- No claim-citation mismatch is evident from the supplied frozen materials.

# 4. Problem Formulation

Overall status: SAFE.

- Y is correctly defined as `P(Like | H_10, i)` with rating at least 4 mapped to Yes and lower ratings to No.
- N is correctly defined as `P(NextInteraction=i | H_10, C)` and targets the next observed interaction regardless of rating.
- N is not described as next-liked-item prediction or preference ranking.
- The prompt uses at most the 10 most recent interactions strictly earlier than the target.
- Y-as-ranker is correctly identified as a bridge that independently scores candidates with `P(Yes)`.
- M1 uses a shared adapter, 1:1 task interleaving, task-specific prompts/answer spaces, and corresponding-task exposure matching.
- RQ1-RQ5 follow the canonical narrative order.

# 5. Methodology

Overall status: SAFE.

- The temporal construction correctly distinguishes Y timestamp buckets from legal N target buckets.
- Multi-interaction N buckets are skipped as targets but remain available to later histories.
- No sentence implies that the model prompt receives the full user sequence.
- QLoRA and response-only scoring descriptions agree with the frozen configuration and source-of-truth boundaries.
- M1 is not described as trained under a joint temporal cutoff.
- Validation is used for decisions and test is reported only after decisions are fixed.

Citation note: the manuscript describes LoRA rank and target projections but does not cite bibliography entry [22]. This is counted under Citation Audit as minor issue C1.

# 6. Experimental Setup

Overall status: SAFE.

- MovieLens and Amazon sample counts match the frozen dataset table.
- Exposure accounting correctly distinguishes specialist exposure, M1 expected per-task exposure, and M1 total exposure.
- SASRec operating points are correctly described as independently trained from scratch, predefined, and not selected by validation or early stopping.
- SASRec configuration matches the frozen contract: hidden size 64, 2 heads, 2 layers, FFN 256, GELU, dropout 0.2, history length 10, full-item cross-entropy, AdamW learning rate 0.001, weight decay 0, batch 512, seed42.
- SASRec exposure alignment is explicitly limited to approximate downstream task-sample exposure.
- Random-k5, PopMatch-k5, k20, and k50 are correctly described as separately constructed; the nonnested warning prevents a candidate-size causal interpretation.
- Cross-task-safe evaluation is correctly described as an evaluation-side restriction. The retained-example coverage and common-safe intersection sizes match frozen evidence.
- Statistical scopes are correct: fixed-seed42 paired user bootstrap for Y-side evaluation-sample uncertainty; three-seed point estimates, mean, sample SD, and direction for N-M1; no ranking CI, significance, or equivalence claim.

Citation notes: bibliography entries [23] (MovieLens) and [25] (bootstrap) are not cited in the body. These are counted under Citation Audit as minor issues C2 and C4.

# 7. Results

Overall status: NEEDS_NARROWING.

Safe claims:

- RQ1 reports the correct Y96 native AUC, Y-as-ranker HR@1, and N96 HR@1, and explicitly states that the comparison concerns complete formulations rather than a single semantic factor.
- RQ2 correctly describes Y gains as modest and uneven and does not claim saturation.
- RQ2 correctly reports continuous N improvement at all four observed seed42 exposure points.
- RQ3 correctly limits common-safe 48k-to-96k narrowing to seed42 validation and states that test does not reproduce it.
- RQ3 correctly characterizes the 96k k5 result as a small, consistent N specialist advantage across seeds 42/43/44.
- RQ4 correctly reports 54/54 positive seed-level deltas and 18/18 summaries with 3/3 positive directions, without claiming significance.
- RQ4 correctly treats k5/k20/k50 as protocol sensitivity rather than a causal or monotonic candidate-size effect.
- RQ5 correctly states that N leads the evaluated SASRec baseline at all four approximately matched points, while SASRec improves substantially and the gap is smaller at 200k.
- Amazon contains only active Base, Y-as-ranker, N, and SASRec results and is explicitly limited to directional support.

Issue R1:

- Exact quote: "strong rating-derived preference discrimination does not directly translate into strong next-interaction ranking"
- Status: NEEDS_NARROWING
- Evidence source: `binary_exposure.csv`; `semantics_bridge.csv`; `source_of_truth.md` C1.
- Why: The cross-interface contrast is supported, but "strong" is not backed by a frozen threshold or baseline for either metric scale. AUC and HR@1 should not be treated as directly comparable magnitudes.
- Minimal correction direction: Retain the non-transfer conclusion while anchoring each side to its measured interface-specific result and avoiding an uncalibrated intensity label.

# 8. Discussion

Overall status: NEEDS_NARROWING.

Safe claims:

- The Discussion consistently ties capability claims to task definitions and interfaces.
- It treats per-task exposure as an accounting basis rather than compute equivalence.
- It explicitly rejects M1-N convergence, identifies validation/test disagreement, and preserves the 96k N advantage.
- It treats candidate analysis as protocol sensitivity and correctly rejects candidate-count causality.
- It limits the SASRec result to the observed exposure range and explicitly excludes compute/resource conclusions.
- It limits Amazon to directional cross-dataset support.

Issue D1:

- Exact quote: "Y learns to discriminate rating-derived preference, while N learns to identify the next observed interaction."
- Status: NEEDS_NARROWING
- Evidence source: task contracts M1/C1 and measured results C1-C3.
- Why: The task objectives directly train these outputs, and the metrics establish measured performance. The sentence can be read as an internal learning-mechanism claim rather than an objective-and-observation statement.
- Minimal correction direction: Tie each capability to what the task trains and what the native evaluation measures.

# 9. Limitations

Overall status: SAFE.

- Full exposure trajectories are correctly limited to seed42.
- Seeds 43/44 are correctly limited to the 96k endpoint.
- Bootstrap uncertainty and training-seed variation are correctly separated.
- The manuscript explicitly states that there is no cross-seed significance or equivalence test and no multiplicity correction/equivalence margin.
- Cross-task-safe M1-N analysis is correctly limited to retained populations and is not represented as joint-cutoff training.
- Candidate protocols are correctly described as nonnested with count, composition, sampling, and difficulty varying jointly.
- PopMatch full-corpus popularity is disclosed as a retrospective offline control.
- Amazon and N-SASRec scope limitations are complete and consistent with frozen evidence.

# 10. Conclusion

Overall status: SAFE.

- The conclusion follows the canonical order: Y/N capability difference, exposure trajectory, M1 versus specialists, candidate-protocol conditioning, and N versus SASRec.
- "N remains the stronger ranking specialist" is sufficiently bounded by the immediately following seed42 validation, held-out test, 96k three-seed, and protocol-specific statements. It is a comparative ranking claim, not a universal model-family claim.
- The conclusion does not claim M1 equivalence, positive transfer, general convergence, candidate-size causality, compute fairness, resource efficiency, universal LLM superiority, or full Amazon replication.

# Claim Matrix

| Section | Claim | Status | Evidence | Issue | Correction Direction |
| --- | --- | --- | --- | --- | --- |
| Abstract | Study compares Y, N, and M1 across exposure, protocols, SASRec, and Amazon | SAFE | Canonical skeleton; C1-C8 | None | None |
| Abstract | Capabilities are "learned" and objectives lead to "learned behaviors" | NEEDS_NARROWING | C1; `results.rq1.*` | Evidence is behavioral and formulation-level, not an identified internal mechanism | Use measured/observed capability framing |
| Abstract | Y has "strong" native preference discrimination | NEEDS_NARROWING | `binary_exposure.csv` | No frozen threshold or benchmark defines "strong" | Anchor to AUC or neutral measured-performance wording |
| Abstract | N improves across evaluated exposure | SAFE | C3; `exposure_scaling.csv` | Seed42 scope is supplied by the study context | None |
| Abstract | M1 preserves Y-side capability; N has small 96k advantage | SAFE | C4, C10; Y bootstrap and clean multiseed tables | No equivalence or significance upgrade | None |
| Introduction | Common language interface does not imply common objective | SAFE | C1; task contracts | Conceptual framing agrees with task definitions | None |
| Introduction | Exposure enables matched per-task specialist/shared comparison | SAFE | M3; `training_exposure.csv` | M1 exposure is correctly treated as expected per-task allocation | None |
| Introduction | Objectives lead to learned behaviors | NEEDS_NARROWING | C1 | Internal/causal wording exceeds measured output evidence | Use observed/measured formulation-level outcome |
| Related Work | LLM recommendation, task formulation, multitask, and evaluation/baseline roles | SAFE | References [1]-[19]; canonical skeleton | No obvious role mismatch | None |
| Problem Formulation | Y is `P(Like | H_10,i)` with rating >= 4 as Yes | SAFE | M1; configuration/split contract | None | None |
| Problem Formulation | N predicts the next observed interaction regardless of rating | SAFE | M1; C1 | Not mislabeled as preference or next-liked-item prediction | None |
| Problem Formulation | History is at most 10 strictly earlier interactions | SAFE | M1; temporal split contract | No full-sequence prompt claim | None |
| Methodology | Y/N temporal sample construction is leakage-aware | SAFE | M1; task construction contract | Full chronology is used for construction, not prompt input | None |
| Methodology | QLoRA and answer-likelihood scoring | SAFE | M2, M4, M9 | Run metadata limits are respected | None |
| Experimental Setup | M1-N cross-task safety is evaluation-side only | SAFE | M10; coverage/common-safe tables | No joint training cutoff claim | None |
| Experimental Setup | Candidate protocols are separately constructed and nonnested | SAFE | M5, C10 | Count, composition, sampling, and difficulty vary jointly | None |
| Experimental Setup | SASRec configuration and independent operating points | SAFE | M7, M9; run metadata ledger | Not validation-selected or early-stopped | None |
| Experimental Setup | Statistics use fixed-seed bootstrap for Y and descriptive n=3 summaries for N-M1 | SAFE | M6, C4, C10 | No unsupported CI/significance/equivalence | None |
| Results | Y AUC rises modestly and unevenly from 24k to 96k | SAFE | C2; `binary_exposure.csv` | No saturation/all-metric monotonicity claim | None |
| Results | N HR@1 rises at all four observed exposure points | SAFE | C3; `exposure_scaling.csv` | Full trajectory correctly remains seed42 | None |
| Results | Seed42 common-safe validation gap narrows from 48k to 96k; test does not | SAFE | C10; `m1_common_safe_exposure.csv` | Split and seed boundaries are explicit | None |
| Results | 96k k5 supports a small, consistent N advantage | SAFE | C10; `m1_clean_multiseed_96.csv` | Descriptive only; no significance claim | None |
| Results | All 54 seed deltas and all 18 summaries favor N | SAFE | C10; clean multiseed table | Counts and direction match frozen evidence | None |
| Results | Candidate protocol changes gap magnitude | SAFE | C10 | No causal candidate-size claim | None |
| Results | N leads SASRec at four approximately matched exposure points | SAFE | C7; `n_vs_sasrec_exposure.csv` | Limited to evaluated implementation and sample exposure | None |
| Results | Amazon reproduces ranking direction only | SAFE | C8; `amazon_certified_models.csv` | No M1, exposure, multiseed, hard-candidate, or native-Y expansion | None |
| Results | Y-native discrimination is "strong" | NEEDS_NARROWING | C1; Y/bridge tables | Qualitative intensity is not calibrated | Report interface-specific measured contrast |
| Discussion | Y "learns" preference and N "learns" next interaction | NEEDS_NARROWING | C1-C3; M1 | Can imply internal mechanism beyond objective and measured behavior | Tie to training objective and native evaluation |
| Discussion | M1 partially preserves capabilities but does not converge to N | SAFE | C4, C10 | Correctly qualified by split and seed scope | None |
| Discussion | Protocol direction is stable but magnitude is sensitive | SAFE | C10 | 54/54 deltas and 18/18 summaries support direction; no significance claimed | None |
| Limitations | Trajectory, statistics, cross-task safety, protocol, Amazon, and compute limits | SAFE | C1-C10; M1-M10 | Required boundaries are all disclosed | None |
| Conclusion | N is the stronger ranking specialist in evaluated conditions | SAFE | C10 | Immediate context limits claim to measured seeds, splits, exposure, and protocols | None |
| Conclusion | N leads SASRec while SASRec closes much of the gap at 200k | SAFE | C7; N-SASRec table | No resource/universal superiority claim | None |

# Numeric Audit

NUMERIC_MISMATCHES: NONE

| Numeric family | Manuscript values checked | Frozen evidence | Result |
| --- | --- | --- | --- |
| Y exposure validation AUC | 0.7761, 0.7816, 0.7844 at 24k/48k/96k | 0.7761274819, 0.7816111073, 0.7843504067 | MATCH |
| Y bridge at 96k | HR@1 0.2211 | 0.2211453744 | MATCH |
| N validation HR@1 | 0.5774, 0.6030, 0.6238, 0.6516 | 0.5774449339, 0.6029955947, 0.6237885463, 0.6516299559 | MATCH |
| N test HR@1 | 0.5612 to 0.6282, same increasing direction | 0.5612334802, 0.5869603524, 0.6100440529, 0.6281938326 | MATCH |
| Common-safe validation gaps | HR 0.01072 to 0.00132; NDCG 0.00549 to 0.00177; MRR 0.00728 to 0.00230 | `m1_common_safe_exposure.csv` | MATCH |
| Common-safe test gaps | HR 0.00939 to 0.01373; NDCG/MRR also non-narrowing | `m1_common_safe_exposure.csv` | MATCH |
| Common-safe retained counts | validation 5,318; test 5,535 | 5318, 5535 | MATCH |
| Cross-task-safe coverage | 96.81%, 98.68%, 93.71%, 97.53% | `m1_cross_task_safe_coverage.csv` | MATCH |
| 96k clean k5 HR delta | validation mean 0.00708, SD 0.00934; test mean 0.01072, SD 0.00271 | `m1_clean_multiseed_96.csv` | MATCH |
| Protocol counts | 54/54 seed-level positive; 18/18 summaries 3/3 positive | 3 protocols x 2 splits x 3 metrics x 3 seeds; all signs positive | MATCH |
| k20 HR delta | validation 0.08042; test 0.07678 | 0.0804187038; 0.0767841012 | MATCH |
| Y-side seed42 bootstrap | AUC +0.00248 [-0.00167, 0.00674]; F1 +0.00553 [0.00096, 0.01025]; Accuracy +0.00460 [-0.00089, 0.01035] | `y_side_binary_bootstrap.csv` | MATCH |
| Specialist/M1 exposure | Y/N 24k/48k/96k; N 200k; M1 total 96k/192k with expected 48k/96k per task | `training_exposure.csv` | MATCH |
| SASRec actual exposure | 24,064; 48,128; 96,256; 200,000 | run metadata ledger and N-SASRec table | MATCH |
| SASRec validation HR@1 | 0.2731, 0.2930, 0.3281, 0.4749 | 0.2731277533, 0.2930396476, 0.3281057269, 0.4748898678 | MATCH |
| SASRec test HR@1 | claim limited to same overall pattern and four-point lead | 0.2903964758, 0.3022026432, 0.3309251101, 0.4511013216 | MATCH |
| N-SASRec validation gaps | 0.3043, 0.3100, 0.2957, 0.1767 | 0.3043171806, 0.3099559471, 0.2956828194, 0.1767400881 | MATCH |
| Amazon HR@1 | N 0.4669; Base 0.3573; Y 0.2298; SASRec 0.1757 | 0.4668779053; 0.3573007887; 0.2297916050; 0.1756646181 | MATCH |
| MovieLens split counts | Y 976,284/12,381/11,544; N 212,725/5,675/5,675 | `datasets.csv` | MATCH |
| Amazon split counts | Y 396,908/57,442/57,442; N 339,449/57,439/57,439 | `datasets.csv` | MATCH |
| Dataset/cardinality counts | MovieLens Y users 6,040; legal N users 5,675; rated items 3,706; metadata items 3,883; Amazon users 57,439, items 24,584, interactions 511,792 | frozen dataset evidence | MATCH |

Numeric-scope checks:

- `seed42` is the only full-trajectory seed; `seed43` and `seed44` are used only at 96k.
- `n=3` summaries are means and sample SDs, not confidence intervals.
- The Word expression `10^-3` for SASRec learning rate corresponds to 0.001; superscript formatting is part of the DOCX representation.
- `200,000`, not 200,192, is correctly used for S391 actual exposure.

# Citation Audit

Citation consistency: PARTIAL

Body citations resolve to references [1]-[21]. No in-text citation number is missing from the References section. References [22]-[25] are not cited anywhere in the body.

| Reference | Related Work subsection(s) | Other body location/status |
| --- | --- | --- |
| [1] | A. LLMs for Recommendation | Introduction |
| [2] | A. LLMs for Recommendation | Introduction |
| [3] | A; D. Offline Evaluation and Sequential Baselines | Introduction |
| [4] | B. Recommendation Supervision and Task Formulation | Introduction |
| [5] | A. LLMs for Recommendation | None |
| [6] | B. Recommendation Supervision and Task Formulation | Introduction |
| [7] | B; D. Offline Evaluation and Sequential Baselines | Introduction |
| [8] | B. Recommendation Supervision and Task Formulation | Introduction |
| [9] | D. Offline Evaluation and Sequential Baselines | None |
| [10] | D. Offline Evaluation and Sequential Baselines | None |
| [11] | D. Offline Evaluation and Sequential Baselines | None |
| [12] | C. Multitask and Unified Recommendation Modeling | None |
| [13] | C. Multitask and Unified Recommendation Modeling | None |
| [14] | A. LLMs for Recommendation | None |
| [15] | B. Recommendation Supervision and Task Formulation | None |
| [16] | C. Multitask and Unified Recommendation Modeling | None |
| [17] | D. Offline Evaluation and Sequential Baselines | None |
| [18] | D. Offline Evaluation and Sequential Baselines | None |
| [19] | D. Offline Evaluation and Sequential Baselines | None |
| [20] | None | Methodology, Llama model card |
| [21] | None | Methodology, QLoRA |
| [22] | None | UNCITED: LoRA |
| [23] | None | UNCITED: MovieLens dataset |
| [24] | None | UNCITED: semantic encoders for retrieval/recommendation |
| [25] | None | UNCITED: bootstrap monograph |

REFERENCE_ROLE_REDUNDANCY: NONE

- [3] appears in Related Work A for LLM recommendation adaptation and D for an earlier SASRec comparison. These are distinct roles.
- [7] appears in B for sequential task formulation and D as the SASRec baseline. These are distinct roles.

Minor citation issues:

- C1: [22] is uncited although LoRA-specific configuration is described in Methodology.
- C2: [23] is uncited although MovieLens-1M is the main dataset.
- C3: [24] is uncited and has no visible claim role in the current manuscript.
- C4: [25] is uncited although paired bootstrap methodology is described.

No obvious claim-citation mismatch was found within the supplied evidence scope.

# Skeleton Audit

SKELETON_ALIGNMENT = PASS

The manuscript follows the canonical main chain in the required order:

1. Y/N supervision and measured capability difference.
2. Task-specific exposure trajectories.
3. Shared M1 versus specialists at matched per-task exposure.
4. Candidate-protocol robustness/sensitivity.
5. N versus SASRec as an exposure-aligned sequential baseline reference.
6. Amazon as a directional ranking check.

Section-level alignment:

| Manuscript location | Canonical role | Result |
| --- | --- | --- |
| Abstract and Introduction | State the full chain and evidence boundaries | PASS |
| Related Work A-D | LLMs, supervision, multitask, evaluation/baseline | PASS |
| Problem Formulation | Define Y, N, M1, interfaces, and RQ1-RQ5 | PASS |
| Methodology/Setup | Establish temporal, exposure, safety, protocol, baseline, and statistical contracts | PASS |
| Results A-F | Execute the canonical chain in exact order | PASS |
| Discussion A-D | Interpret supervision, exposure/shared modeling, protocol sensitivity, and SASRec scope | PASS |
| Limitations | Preserve seed, split, evaluation, protocol, cross-dataset, and compute boundaries | PASS |
| Conclusion | Return to the same chain without promoting secondary analyses | PASS |

Specific drift checks:

- The manuscript does not regrow a separate "supervision/exposure/evaluation three-pillar" story as the main contribution structure.
- Candidate protocol remains a robustness/sensitivity analysis and is not promoted to the same conceptual level as Y/N or M1.
- SASRec remains a reference trajectory rather than the paper's primary research problem.
- Amazon remains a secondary directional check rather than a second complete validation suite.
- Discussion and Conclusion remain consistent with the Introduction.
- The manuscript's Related Work subsection title "Offline Evaluation and Sequential Baselines" differs nominally from the canonical label "Evaluation and Baseline Comparison," but its role and content match exactly; this is not a skeleton deviation.

SKELETON_DEVIATIONS: NONE

# Final Gate

SAFE_AFTER_LISTED_CORRECTIONS
