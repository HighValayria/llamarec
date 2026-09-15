# FINAL MANUSCRIPT AUDIT

Date: 2026-09-13  
Mode: READ-ONLY audit of existing artifacts; this report is the sole new output.

## 1. Executive Verdict

**NOT READY for submission as the current standalone manuscript.** No P0 issue was established. There are three P1 findings: absent table assets despite live callouts, malformed native probability equations, and overbroad SASRec-gap language in the Abstract and Introduction. Five P2 findings concern citation ordering, summary qualifiers, missing method identifiers, proofing remnants, and narrative emphasis.

This is not a rejection of the frozen experimental evidence. All nine existing generated source tables match their corresponding CSVs: **72 rows and 271 numeric cells**, checked at the declared five-decimal display precision, with all nine CSV hashes matching the existing build manifest. The Results' quoted performance numbers also match the relevant frozen evidence. The critical distinction is that **these tables are not present in the current DOCX**.

### Audited Target and Authority

- Requested path: `true_paper/paper.doc`. That file does not exist. Actual current draft audited: [paper.docx](F:/Projects/llamarec/true_paper/paper.docx), 32,769 bytes.
- SHA-256: `d73671c73de66bb23c299f463abcb0d8f25b742abfc61904d8756209f0fa8e2f`.
- Read all 131 top-level Word paragraphs in document order, including headings, equations, the bibliography, and the final empty paragraph. P001-P131 below mean one-based `word/document.xml / w:document/w:body/w:p` positions, not printed page or line numbers. Quotes and paragraph IDs identify the exact current text.
- Narrative authority: the synchronized [canonical story skeleton](F:/Projects/llamarec/true_paper/PAPER_STORY_SKELETON_CANONICAL.md). Experimental authority: frozen evidence and the later common-safe/clean-subset corrections, not older prose or full-holdout M1 summaries.
- [source_of_truth.md](F:/Projects/llamarec/paper/evidence/source_of_truth.md), [claim_matrix.md](F:/Projects/llamarec/paper/evidence/claim_matrix.md), and [run metadata ledger](F:/Projects/llamarec/paper/evidence/run_metadata_ledger.md) establish scope and provenance. The older [MS96 integration summary](F:/Projects/llamarec/paper/evidence/ms96_integration_summary.md) is not substituted for the corrected clean-subset ranking tables.
- Existing [main.aux](F:/Projects/llamarec/paper/builds/icecai_2026/en/main.aux) and [build manifest](F:/Projects/llamarec/paper/builds/icecai_2026/en/build_manifest.json) identify the previous nine-table/two-figure asset inventory. Their successful build status does **not** validate the newly edited DOCX.
- Applied the relevant peer-review and verification guidance. No writing/rebuilding workflow, training, inference, bootstrap, prediction regeneration, or new experimental run was executed. No formal wiki content was read.

### Verification Boundaries

The DOCX was inspected through its ZIP/XML contents without saving it. It contains zero `w:tbl` elements, drawings, pictures, text boxes, embedded media/objects, or alternative-content imports; no hidden table-bearing ancillary part was found. Consequently table/figure placement and current-page layout cannot be certified. No new PDF or page images were generated.

Citation identity and support were compared with the local bibliography, registry, and frozen primary-source notes. This is not a fresh external verification of every cited publication. One targeted Microsoft documentation lookup verified the native equation separator interpretation used in P1-02.

## 2. P0 / P1 / P2 Issues

### P0

**None established.** The audit did not find fabricated numbers, an affirmative convergence/equivalence/positive-transfer claim, a claimed symmetric Y/N task grid, or a claim of full Amazon replication.

### P1-01: The Current DOCX Refers to Tables It Does Not Contain

**Locations:** Experimental Setup P045, P050-P051, P058; Results P071-P073, P075, P078, P080.

Examples: P045 says "task-specific user and split counts are reported in Table I"; P051 says "exact exposures are reported in Table V"; P073 reports mean deltas "(Table VIII)"; P080 cites "(Table IX)".

**Evidence:** 12 table callouts reference seven distinct numbers: I, II, III, V, VII, VIII, IX. There are no actual tables or table captions in the current document. The earlier source inventory contains Tables I-IX, but source assets elsewhere in the repository do not make these references resolvable inside this draft.

**Impact:** Essential dataset counts, exact exposure accounting, confidence intervals, and seed/protocol detail are delegated to missing assets. A reader cannot independently check the paper's evidence from the manuscript. This is a submission-completeness blocker, not a numerical disagreement.

**Minimal fix:** Integrate the already frozen intended tables, without altering numbers. If the nine-table source inventory is retained, add the missing callouts for Table IV around Results A/B and Table VI at P070, then verify all numbering and placement against the assembled final document. Do not claim current floats pass merely because the previous source build did.

### P1-02: Probability Equations Have Malformed Native Delimiters

**Locations:** Problem Formulation P026, P027, P029; compare the adjacent explanations P025, P027-P030 and the canonical skeleton's Problem Formulation.

This is distinguishable from ordinary text-extraction loss. The outer `m:d` objects use `<m:sepChr m:val=","/>` between two base arguments. The second argument itself starts with a conditional bar or an equality-plus-bar:

| Paragraph | Native outer arguments, structurally reconstructed | Problem |
| --- | --- | --- |
| P026 | `P(Like, | H_10(u,t)i)` | Extra comma before the conditional bar; missing separator before item `i`. |
| P027 | `P(Yes, | H_10(u,t), i)` | Extra comma before the conditional bar. |
| P029 | `P(NextInteraction, =i | H_10(u,t)C)` | The comma splits the event from its equality; missing separator before candidate set `C`. |

These are XML-based reconstructions, not screenshots. Microsoft documents that `sepChr` is rendered between the delimiter's base arguments, confirming that the comma is part of the equation structure rather than an extraction artifact. [Microsoft Open XML separator definition](https://learn.microsoft.com/en-us/dotnet/api/documentformat.openxml.math.separatorchar?view=openxml-3.0.1).

**Impact:** The formal task definitions have invalid/ambiguous probability notation even though the surrounding prose correctly describes the intended tasks.

**Minimal fix:** Repair the three native equations to express `P(Like | H_10(u,t), i)`, `P(Yes | H_10(u,t), i)`, and `P(NextInteraction=i | H_10(u,t), C)`. Preserve the task definitions and results; verify the equations visually afterward.

### P1-03: Abstract and Introduction Overgeneralize SASRec-Gap Narrowing

**Locations:** Abstract P004: "with the difference narrowing as SASRec receives more training"; Introduction P010: "while the gap narrows as SASRec receives more training."

**Evidence:** [frozen N-versus-SASRec CSV](F:/Projects/llamarec/paper/tables/n_vs_sasrec_exposure.csv) gives these HR@1 differences, N minus SASRec:

| N exposure | Recorded SASRec exposure | Validation gap | Frozen-test gap |
| --- | --- | --- | --- |
| 24,000 | 24,064 | 0.30431718 | 0.27083700 |
| 48,000 | 48,128 | 0.30995595 | 0.28475771 |
| 96,000 | 96,256 | 0.29568282 | 0.27911894 |
| 200,000 | 200,000 | 0.17674009 | 0.17709251 |

Both gaps **increase from 24k to 48k**. The statements are defensible as an overall endpoint summary, but without that qualifier they imply a general training-linked narrowing that the full sequence does not show. Results P078 correctly limits its numerical narrowing claim to 96k-to-200k; Discussion P091 and Conclusion P104 correctly emphasize the largest endpoint.

**Minimal fix:** Bound the Abstract/Introduction language to the later interval or the smaller gap at the largest measured exposure. Preserve the supported claim that N is ahead at all four points. This requires a wording correction, not a new experiment.

### P2-01: Citation Labels Were Not Reordered After Prose Reorganization

**Locations:** Introduction P007; Related Work P013, P015, P018, P021; bibliography P106-P130.

P007 first introduces [6], [7], and [8] before [5]. P013 first introduces [14] before [5]. P018 introduces [12], [13], and [16] before [9]-[11] in P021.

**Observed first-use order:** `1, 2, 3, 4, 6, 7, 8, 14, 5, 15, 12, 13, 16, 9, 10, 11, 17, 18, 19, 20, 21, 22, 23, 24, 25`.

**Impact:** Fails the requested first-appearance ordering check. There are no undefined citations, duplicate bibliography labels, or uncited entries in the current 25-entry bibliography.

**Minimal fix:** Renumber body citations and bibliography together by first use after final text/float assembly. Do not delete references just to conceal the ordering problem.

### P2-02: Summary Qualifiers Are Less Precise Than the Results

**Locations:** Abstract P004; Introduction P010; Conclusion P103.

P004 says "N maintains a small advantage over M1-N across three training seeds" without specifying PopMatch-k5. P010 similarly says "N retains a small ranking advantage over M1-N" and "M1 remains close to the Y specialist" without anchoring the latter to 96k.

**Evidence:** Results P070 explicitly anchors Y-side preservation to 96k. Results P073 anchors the small ranking gap to PopMatch-k5. The clean 96k mean HR@1 gaps are approximately 0.00708/0.01072 for k5 but 0.08042/0.07678 for k20, on validation/test respectively. The summary's following protocol-dependence sentence helps, but does not identify where "small" applies.

**Minimal fix:** Attach 96k to the Y-preservation summary and PopMatch-k5 to the small-gap summary. Keep the broader all-tested-protocol conclusion about **direction**, not uniformly small magnitude.

### P2-03: Compression Removed Several Reproducibility Identifiers

**Locations:** Experimental Setup P044-P045, P053-P055, P061; Results P080.

- P055 only says "k20 and k50 candidate protocols." It does not specify their random sampling construction, while P098 later says sampling strategy changes. The distinction from popularity-matched k5 is part of interpreting this supporting experiment.
- P061 identifies training seeds but omits the separately fixed candidate-generation seed. Fixed candidate lists in P054 establish within-comparison matching, not explicitly the cross-training-seed candidate control.
- P053 names F1 and accuracy but does not state the fixed 0.5 decision threshold used for the paired 96k Y-side comparison.
- P045 introduces "Base" as an Amazon comparator; P080 reuses it without explaining which model state and scoring route Base denotes.
- P044 names "Amazon Musical Instruments" without the dataset version and 5-core identity retained in the source.

**Evidence:** [source-of-truth contracts M5/M6/M8](F:/Projects/llamarec/paper/evidence/source_of_truth.md); [evaluation protocol source](F:/Projects/llamarec/paper/modules_parts/methods/evaluation_protocol.md); [statistical source](F:/Projects/llamarec/paper/modules_parts/methods/bootstrap_and_statistics.md); [dataset source](F:/Projects/llamarec/paper/modules_parts/methods/datasets.md); [historical run ledger](F:/Projects/llamarec/paper/evidence/run_metadata_ledger.md). Current candidate/scoring code was inspected as a contract cross-check, not used to infer unrecorded historical run parameters.

**Minimal fix:** Restore these brief definitions from existing evidence. State the threshold only for the paired result to which it applies; do not imply every historical diagnostic used that threshold. No new method or experiment is needed.

### P2-04: Title Placeholder and Formula/Text Boundary Spaces Remain

**Locations:** P001 is literally "Title". At P027, P047, and P049, the word immediately after the inline equation has no leading space.

Specific XML boundaries are `</m:oMath>...<w:t>and rank...` at P027, `...<w:t>as the cumulative...` after `q` at P047, and `...<w:t xml:space="preserve">is the batch...` after `B_s` at P049. There is no intervening whitespace run.

**Impact:** The title is an unequivocal finalization placeholder. The three missing source spaces are confirmed; their exact visual tightness is unverified because this audit did not render new pages. They should not be described as broken English sentences solely from flattened math text.

**Minimal fix:** Supply the intended title and repair/check the three formula-to-prose spaces. Also perform visual formula proofing for P1-02.

### P2-05: Summary Compression Underweights the Core Shared-Model Trajectory

**Locations:** Abstract P003-P004, Introduction P010, Conclusion P103-P104; contrast Results P071-P073 and Discussion P087.

The Abstract and Conclusion retain the SASRec exposure trend but omit the central distinction between the seed42 validation 48k-to-96k N-M1 narrowing and its failure to repeat on test. The synchronized skeleton explicitly retains that distinction in its Abstract and Conclusion. P010 compresses the shared-model result to endpoint closeness and a small gap.

P003 also groups the secondary baseline into "For the N-M1 ranking comparison ... include SASRec," whereas the actual baseline experiment is N-versus-SASRec, not an additional M1-versus-SASRec comparison.

**Impact:** The body still follows the intended hierarchy, so this is not a global story failure or an unsupported new finding. It is a local loss of emphasis/role separation after shortening.

**Minimal fix:** Preserve a brief bounded shared-model trajectory statement in the main summaries and separate the N-M1 protocol check from the N-versus-SASRec reference. Do not expand candidate sensitivity or SASRec into new central contributions.

## 3. Section-by-Section Coherence Audit

| Section | Sequential-reading verdict |
| --- | --- |
| Title / Abstract, P001-P004 | Title unresolved. Study design and main findings form a coherent two-paragraph abstract. P1-03, P2-02, and P2-05 affect scope and hierarchy, not sentence completeness. |
| I. Introduction, P006-P010 | Logical progression: shared interface -> distinct objectives -> exposure -> shared adaptation -> findings. No dangling paragraph was found. Citation ordering and compressed qualifiers need attention. Y/N are used at P007 before their local parenthetical redefinition at P009, but were already defined in the Abstract and immediately explained at P007; not an independent undefined-acronym defect. |
| II. Related Work, P013-P022 | Four subsections connect to the later design. The current text recognizes existing task unification, sampling, auxiliary-data, and baseline work; it does not claim these topics are unprecedented. No contradictory old RQ wording or unsupported blanket novelty claim found. Renumber citations. |
| III. Problem Formulation, P024-P031 | The prose consistently distinguishes preference, next observed interaction, and the one-way Y-as-ranker bridge. M1-Y/M1-N are explicitly defined. The native equations and one following space need repair; a flat text extraction alone would miss the delimiter error. |
| IV. Methodology, P033-P041 | Temporal construction flows into adaptation/scoring. Same-timestamp handling, singleton N targets, response-only loss, seven projection families, effective batch 8, and frozen-test decision discipline are mutually consistent. No fragment or false joint-training-cutoff statement found. |
| V. Experimental Setup, P044-P061 | Dataset -> exposure -> candidate protocols -> safe subset -> baseline/statistics is coherent. The last subsection combines SASRec and statistics abruptly but uses two complete paragraphs; splitting it is optional, not a required fix. Main problems are absent tables and compressed identifiers. |
| VI.A, P064-P065 | Native Y and Y-as-ranker are properly distinguished; the paragraph immediately rejects a single-semantic-factor interpretation. Quoted values pass. Table IV callout is absent relative to the source inventory. |
| VI.B, P067-P068 | Y's modest/non-monotone response contrasts naturally with N's upward trajectory. Validation and test are named separately. No saturation/convergence claim found. |
| VI.C, P070-P073 | Strongest scope discipline in the paper: Y-side uncertainty, common-safe validation narrowing, contrary test behavior, then three-seed endpoint direction. No reversal of inference order. Table VI callout absent; VII/VIII callouts present but tables absent. |
| VI.D, P075-P076 | "We next examine" supplies a clear transition. Direction versus magnitude is distinguished and non-causal interpretation is retained. `K20` at the start of P075 versus `k20` elsewhere is a minor casing variation, not a different protocol. |
| VI.E, P078 | Properly bounded N-versus-SASRec comparison, including later-interval gap numbers and a resource-comparison disclaimer. More precise than its Abstract/Introduction summaries. |
| VI.F, P080 | Explicitly a directional check, with one compact paragraph. Base needs a definition. No Amazon M1 or full-replication claim. |
| VII. Discussion, P083-P092 | Follows supervision -> exposure/shared model -> protocol -> conventional reference. The test counterexample remains adjacent to the narrowing observation. P083's "strong native preference performance" is more emphatic than the Results' numerical wording; a light tone alignment would improve consistency but is not a new scientific blocker. |
| VIII. Limitations, P094-P100 | Boundaries are organized by seeds, exposure denominators, uncertainty, retained population, protocols, Amazon, and compute. They qualify rather than contradict the detailed Results. |
| IX. Conclusion, P102-P104 | One conclusion, no duplicate second ending or incompatible draft splice. Endpoint findings are supported, but the core validation/test trajectory distinction has been compressed away while the SASRec trend remains. |
| References, P106-P130 | Twenty-five entries, each used and mapped. Numbering is continuous; ordering against first body use is not. |

**Story weighting:** Results A-C contain approximately 386 lexical words, versus 94 for candidate sensitivity, 85 for SASRec, and 63 for Amazon (the same simple word-token rule, headings excluded). Thus the body does not let secondary evidence dominate by volume. P2-05 concerns summary emphasis, not an invented universal word-count requirement.

## 4. Evidence Consistency Audit

### Frozen Source Checks

| Check | Result and evidence |
| --- | --- |
| Nine existing generated tables versus their designated CSVs | PASS: 72 rows, 271 numeric cells, all displayed nonnumeric fields/empty cells consistent; all nine source SHA-256 values match the existing manifest. This does not validate absent DOCX tables. |
| Compact task-formulation table versus seed42 frozen main evidence | PASS: 30 metric values agree with [exposure_main_table.csv](F:/Projects/llamarec/.agent/exposure_scaling/final_evidence/exposure_main_table.csv). Older full-holdout M1 ranking rows in this file were not treated as current clean results. |
| Clean 96k display summary versus frozen per-seed summary | PASS: 18 rows, 36 mean/SD values agree with [clean_multiseed_96_summary.csv](F:/Projects/llamarec/paper/plan/task-packets/m1-clean-subset-audit/clean_multiseed_96_summary.csv); all 54 stored per-seed deltas are positive. Only arithmetic/counting existing results was performed. |
| Common-safe trajectory population | PASS: [common-clean verification CSV](F:/Projects/llamarec/paper/plan/task-packets/m1-common-clean-exposure-verification.csv) records identical examples/candidate order at both exposure points, with 5,318 validation and 5,535 test examples. |
| Existing native-N figure data | PASS for the four HR@1 trajectory rows against frozen N results. The corresponding image is absent from this DOCX. |
| Existing N-versus-SASRec figure data | PASS for the four HR@1/exposure alignment rows against the table. The corresponding image is absent from this DOCX. |

### Numerical Claims in the Current Prose

| Current location / claim | Frozen value or check | Verdict |
| --- | --- | --- |
| P045: 3,706 rated MovieLens items; 3,883 metadata items; 24,584 Amazon items and 511,792 interactions | Matches the dataset/source contracts; rated-item and metadata universes are not conflated. | PASS |
| P050: N200 about 94% of the legal N pool | 200,000 / 212,725 = approximately 94.02%. | PASS |
| P058/P097: safe coverage above 93%; range 93.71%-98.68% | M1-48: 5,494/5,675 validation, 5,600/5,675 test; M1-96: 5,318/5,675 validation, 5,535/5,675 test. | PASS |
| P064: Y96 AUC 0.7844; Y-as-ranker HR@1 0.2211; N96 HR@1 0.6238 | 0.7843504067; 0.2211453744; 0.6237885463, all seed42 validation at 96k. | PASS |
| P067: Y AUC 0.7761 -> 0.7844; non-monotone F1 | AUC 0.7761274819 -> 0.7843504067. F1 0.7791746032 -> 0.7848403087 -> 0.7783174665. | PASS |
| P068: N HR@1 validation 0.5774 -> 0.6516; test 0.5612 -> 0.6282 | Validation 0.5774449339, 0.6029955947, 0.6237885463, 0.6516299559; test 0.5612334802, 0.5869603524, 0.6100440529, 0.6281938326. | PASS |
| P070: F1 interval positive; AUC/accuracy cross zero | M1-Y minus Y, seed42 validation: F1 CI [0.0009575692, 0.0102517897]; AUC [-0.0016706849, 0.0067379231]; accuracy [-0.0008861777, 0.0103524123]. | PASS |
| P071: common-safe validation HR gap +0.01072 -> +0.00132 | 0.010718315156 -> 0.001316284317. NDCG gap 0.005489198636 -> 0.001770255799; MRR 0.007277171869 -> 0.002297229535. | PASS |
| P072: no corresponding frozen-test narrowing in any of three metrics | HR gap 0.009394760614 -> 0.013730803975; NDCG 0.004533996672 -> 0.006048993561; MRR 0.006013249021 -> 0.008069858476. | PASS |
| P073: three-seed k5 mean HR gaps +0.00708 validation / +0.01072 test | 0.007082863232 / 0.010719662752. | PASS |
| P075-P076: k20 largest gap; 54 positive deltas; 18 summaries with 3/3 positive directions | Confirmed for the stored split/protocol/metric grid. No inference of monotonic candidate-size causality. | PASS |
| P078: all four N>SASRec; validation 96k/200k gaps +0.2957/+0.1767 | 0.2956828194 / 0.1767400881; all eight split-specific HR@1 differences positive. | PASS |
| P080: Amazon N HR@1 0.4669, above Base, Y-as-ranker, SASRec; same ordering for NDCG/MRR | HR@1: N 0.466877905256 > Base 0.357300788663 > Y 0.229791605007 > SASRec 0.175664618117; all active metrics retain that ordering. | PASS |

### Scope, Seeds, and Protocols

- **Seeds 42/43/44:** P061 and P094 correctly restrict full trajectories to training seed42 and additional seeds to the 96k endpoint. They do not turn the endpoint replication into a multiseed learning curve. Candidate-generation seed disclosure is a separate minor omission, not evidence of candidate changes.
- **Validation versus frozen test:** P041 states the decision discipline; P071-P073 keep the narrowing counterexample and endpoint replication separate. No test-selected checkpoint claim was found.
- **M1 cross-task safety:** P057 contains all three exclusion conditions; P058 explicitly says the restriction is evaluation-side and training uses original task-specific streams. P097 restricts the conclusion to the retained population. There is no claim that M1 was trained with a new joint cutoff.
- **M1 exposure:** P031 distinguishes per-task from total exposure; P050 calls M1-48/M1-96 per-task counts expected. The frozen training table gives total 96k/192k versus per-task 48k/96k. No exact per-task counter was fabricated.
- **SASRec exposure:** Source Table V uses recorded exposures 24,064/48,128/96,256/200,000, matching [checkpoint inventory](F:/Projects/llamarec/.agent/exposure_scaling/alignment/sasrec_checkpoint_inventory.csv). The 200k endpoint is not replaced by 391 x 512 = 200,192. P051 delegates the exact counts to missing Table V, so their current manuscript presentation is blocked by P1-01, not numerically wrong.
- **Protocol non-nestedness:** Explicit at P055/P098, with count/composition/sampling/difficulty confounding and full-corpus popularity recognized. No nested-set assumption was found.
- **Amazon:** P045/P080/P099 limit it to earlier seed42 ranking direction, not exposure, 96k multiseed, alternative protocols, or native preference replication. The active corrected table excludes uncertified Amazon M1.
- **Uncertainty:** P070/P096 do not infer equivalence from zero-crossing intervals or significance from three-seed SD. Existing ranking-bootstrap files elsewhere in the repository were not promoted into an unclaimed manuscript result.
- **Implementation consistency:** Relevant lines in [experiment.yaml](F:/Projects/llamarec/configs/experiment.yaml) (task/split/adaptation contract), [split.py](F:/Projects/llamarec/src/data/split.py) (timestamp buckets), [candidate_sets.py](F:/Projects/llamarec/src/eval/candidate_sets.py) (full-sequence popularity), [scoring.py](F:/Projects/llamarec/src/inference/scoring.py) (allowed-answer likelihood), and [sasrec.py](F:/Projects/llamarec/src/baselines/sasrec.py) (causal encoder/full-item CE) agree with the described design. Historical run metadata, not current function defaults, establishes actual SASRec batch 512 and other run parameters.

## 5. Table / Figure / Citation Audit

### Existing Frozen Table Inventory

The following numbering comes from the existing source build, not from floats in the current DOCX. PASS means generated table cells versus designated CSV, at five-decimal precision.

| Source number | Source CSV | Rows | Numeric cells | Cell check |
| --- | --- | --- | --- | --- |
| I | [datasets.csv](F:/Projects/llamarec/paper/tables/datasets.csv) | 4 | 16 | PASS |
| II | [training_exposure_compact.csv](F:/Projects/llamarec/paper/tables/compression_2026-09-10/training_exposure_compact.csv) | 9 | 36 | PASS |
| III | [m1_cross_task_safe_coverage.csv](F:/Projects/llamarec/paper/tables/scientific_repair_2026-09-11/m1_cross_task_safe_coverage.csv) | 4 | 12 | PASS |
| IV | [supervision_semantics_compact.csv](F:/Projects/llamarec/paper/tables/compression_2026-09-10/supervision_semantics_compact.csv) | 10 | 40 | PASS |
| V | [n_vs_sasrec_exposure.csv](F:/Projects/llamarec/paper/tables/n_vs_sasrec_exposure.csv) | 8 | 40 | PASS |
| VI | [y_side_binary_bootstrap.csv](F:/Projects/llamarec/paper/tables/scientific_repair_2026-09-11/y_side_binary_bootstrap.csv) | 3 | 9 | PASS |
| VII | [m1_common_safe_exposure.csv](F:/Projects/llamarec/paper/tables/scientific_repair_2026-09-11/m1_common_safe_exposure.csv) | 12 | 66 | PASS |
| VIII | [m1_clean_multiseed_96.csv](F:/Projects/llamarec/paper/tables/scientific_repair_2026-09-11/m1_clean_multiseed_96.csv) | 18 | 36 | PASS |
| IX | [amazon_certified_models.csv](F:/Projects/llamarec/paper/tables/scientific_repair_2026-09-11/amazon_certified_models.csv) | 4 | 16 | PASS |

Historic internal asset IDs such as `hard_candidate_compact` and `exposure_scaling` were resolved through the manifest and labels. They were not assumed to retain their old scientific content.

### Current DOCX Cross-References

| Object | First current callout | Current asset status |
| --- | --- | --- |
| Table I | P045, dataset splits | Absent |
| Table II | P050, exposure schedule | Absent |
| Table III | P058, safe coverage | Absent |
| Table IV | None | Absent; source table is the native/bridge comparison |
| Table V | P051, exact SASRec exposures | Absent |
| Table VI | None | Absent; source table is the Y-side paired interval comparison |
| Table VII | P071, common-safe trajectory | Absent |
| Table VIII | P073, clean 96k seeds/protocols | Absent |
| Table IX | P080, Amazon ranking | Absent |
| Figures 1-2 in the prior source inventory | No figure callout anywhere | Neither present |

- Current first-distinct-callout order is **I, II, V, III, VII, VIII, IX**. Table V is mentioned before III. Recheck numbering and proximity after float integration; the existing ordering alone cannot establish the future float layout.
- Source labels are continuous for Tables I-IX and Figures 1-2. The current document has no captioned object sequence whose continuity can pass.
- Every current table callout is unresolved **in this DOCX**, although each maps to a real repository source asset. There is no invented nonexistent repository Table X.
- There are no existing DOCX figures/tables to classify as uncited floats. IV/VI are missing **source-inventory callouts**, not existing-but-unreferenced DOCX tables.
- Figure omission alone is not a mandatory scientific failure if an intentional text-and-table final version is chosen. If the two frozen figures are restored, add body callouts and verify their actual legends/placement. This audit did not certify their current page rendering.
- First-reference-before/near-float checks are **BLOCKED**, not PASS, because there are no current floats.

### Citations and References

| Programmatic check | Result |
| --- | --- |
| Bibliography labels | [1]-[25], continuous and unique |
| Body citation -> bibliography mapping | 25/25 referenced numbers resolve |
| Undefined body citations | 0 |
| Uncited current bibliography entries | 0 |
| Duplicate bibliography numbers | 0 |
| Unexplained missing reference numbers | 0 |
| First-use ordering | FAIL: exact sequence in P2-01 |
| Identity versus local registry | 25/25 current reference titles match their corresponding registered keys after normalization |
| Extra entries in repository library | Inactive library entries are not counted as uncited entries in this DOCX |
| Repeated body citation to the same work | Normal reuse, not a duplicate-number defect |

The role audit used [citation registry](F:/Projects/llamarec/paper/references/citation_registry.json), [library.bib](F:/Projects/llamarec/paper/references/library.bib), [primary-source notes](F:/Projects/llamarec/paper/references/primary_source_notes.md), and [primary-source adjudication](F:/Projects/llamarec/paper/references/primary_source_adjudication.md). No current passage was found to reintroduce the rejected claims that P5/TALLRec had no data-volume comparisons, that Penha was single-point/non-LLM, or that prior recommendation scaling excluded repeated training.

Reference [24] is locally registered as the Amazon Reviews 2023 dataset-associated paper; its semantic-encoder title alone is not evidence of a wrong citation. Baseline reproducibility references [17]-[18] are used generically at P022, not falsely presented as the source of this repository's SASRec configuration. Fine-grained author/DOI/venue metadata were not freshly verified against every publisher, and local title agreement should not be mistaken for that broader certification.

## 6. Terminology Consistency Audit

| Term family | Finding |
| --- | --- |
| Y / N / complete task formulations | Defined in the Abstract and formally in Section III. P065/P084 explicitly include target construction, eligible data, prompts, and scoring; no isolated-supervision-semantics causal attribution. |
| Native tasks / Y-as-ranker | Consistently asymmetric: native Y, native N, and Y-to-ranking bridge. No N-to-preference evaluation is claimed. |
| M1 / M1-Y / M1-N | Consistent shared-adapter/interface terminology. Formal interface definitions at P031 precede detailed use. M1-N appears in the Abstract after M1's expansion; understandable summary notation, not an unresolved acronym. |
| Specialist / task-specific / shared / multitask | Refers to the same model roles, not competing model versions. "Small" needs protocol scope as in P2-02. |
| Task-sample exposure | Cumulative consumed examples including repeats, not unique items/interactions, total compute, or matched fraction of each task pool. |
| LlamaRec / legacy names | No current manuscript occurrence of LlamaRec, N-K0, Y-K0, standard-k5, or hard-candidate naming was found. Their presence in old source filenames/skeleton text is not a current-body defect. |
| RQ labels | No residual old RQ numbering found. Replacing RQ headings with descriptive headings is consistent throughout; there is no broken RQ reference. |
| Candidate sensitivity / robustness | Current prose uses sensitivity and bounded direction stability. No affirmative blanket robustness claim found. Random-k5/PopMatch-k5 are defined; k20/k50 need sampling identity (P2-03). |
| `K20` versus `k20` | One sentence-initial casing variation at P075. Optional normalization; no evidence of a second protocol. |
| Base | First named at P045, used in P080, not explicitly defined. Included in P2-03. |
| AUC / F1 / HR@1 / NDCG@5 / MRR / LoRA / QLoRA / SASRec | Standard specialist nomenclature; method names have citations and metrics are grouped at P053. Expanding familiar acronyms could improve accessibility, but no ambiguous new metric was invented by the edit. |

## 7. Cross-Section Claim-Strength Matrix

| Claim | Abstract / Introduction | Results | Discussion | Conclusion | Assessment |
| --- | --- | --- | --- | --- | --- |
| Y native preference versus Y-as-ranker | "performs well" / "transfers poorly", P004/P010 | Numeric contrast plus complete-formulation caveat, P064-P065 | "strong" at P083; task/data/interface limits at P084 | Observed task-specific capabilities, P102 | Scientifically bounded overall; Discussion adjective is stronger, optional tone alignment |
| N exposure response | Improves over evaluated range, P004/P010 | Both seed42 splits rise at all points, P068 | Task-dependent progress, P086 | Evaluated exposure range, P102 | Consistent |
| M1-Y preservation | 96k explicit in P004, absent in P010 | Seed42 96k, CI limitations, P070 | 96k explicit and no convergence, P087 | Closeness without explicit 96k in first sentence, P103 | Attach endpoint qualifier; do not imply all-budget parity |
| N-M1 48k -> 96k narrowing | Omitted | Seed42 common-safe validation only; test contrary, P071-P072 | Same bounded claim, P087 | Omitted | No false statement; central trajectory underweighted in summaries |
| N-M1 96k endpoint direction | "small" with no named k5 context, P004/P010 | Small k5 means and all-seed/all-protocol direction separated, P073-P076 | Direction/magnitude separated, P089 | All three evaluated seeds; protocol-conditioned magnitude, P103 | Summary small-gap scope needs narrowing |
| Candidate protocols | Supporting comparison, P003/P009-P010 | Independent sensitivity; no pure size effect, P075-P076 | Non-nested, P089 | Evaluation-conditioned magnitude, P103 | Consistent; brief protocol definitions missing |
| N-versus-SASRec | Unqualified training-linked gap narrowing, P004/P010 | N ahead throughout; gap shrinks on late interval, P078 | Smaller at 200k, not compute-equivalent, P091-P092 | Smaller at largest point, P104 | P1-03: summaries stronger than detailed evidence |
| Amazon | Additional/earlier ranking direction, P003-P004 | Directional check only, P080 | No broader Amazon replication asserted | Omitted | Consistent secondary role; omission from conclusion is not a defect |

### Explicitly Disallowed Claims

| Disallowed interpretation | Current audit result |
| --- | --- |
| Y/N difference caused solely by supervision semantics | Not asserted; expressly bounded at P065/P084 |
| Both Y and N symmetrically evaluated on both tasks | Not asserted; asymmetric bridge is explicit at P007/P016/P027 |
| M1-specialist convergence | Mentioned only to reject the inference at P072/P087 |
| Positive transfer | Mentioned only as not established at P070 |
| Equivalence | Mentioned only as not established at P070/P096 |
| Candidate-size causal effect | Explicitly rejected at P055/P076/P098 |
| SASRec compute/resource fairness | Explicitly rejected at P051/P078/P092/P100 |
| Universal LLM superiority | Not asserted; limited to evaluated SASRec setup and observed exposure range |
| Amazon replication of full MovieLens findings | Explicitly rejected at P080/P099 |

Negated risk terms were not counted as prohibited affirmative claims.

## 8. Possible Artifacts of Sentence-Level Editing

### Confirmed

- **Native formula corruption:** P026/P027/P029 contain the separator/conditioning defects in P1-02. These would be easy to miss in a prose-only edit.
- **Deleted assets or unsynchronized assembly:** P045/P050/P051/P058/P071-P080 retain table-dependent sentences, but the DOCX has no table objects. The audit establishes the inconsistency, not which editing action caused it.
- **Unrenumbered citations:** P007/P013/P018/P021 preserve a former label order after prose reorganization.
- **Placeholder title:** P001 remains "Title".
- **Formula-to-prose boundary spaces:** P027/P047/P049 lack source whitespace after inline math. Visual severity remains unverified.

### Plausible Compression Effects, Not Proven Editing History

- P003 merges the candidate-protocol and conventional-baseline roles in a single clause.
- P004/P010 remove the late-interval qualifier from the SASRec trend.
- P004/P010/P103 retain endpoint conclusions while reducing explicit protocol/exposure qualifiers.
- P044-P061 omit short dataset/baseline/threshold/candidate identifiers preserved in source contracts.
- P103-P104 retain a secondary cross-model trend but omit the canonical shared-model validation/test trajectory distinction.

### Negative Findings

No duplicate complete paragraph or duplicated long sentence was detected; sequential reading found no clear two-version splice, repeated conclusion section, dangling old RQ reference, or incomplete ordinary prose sentence. The DOCX contains no tracked insertion/deletion blocks in the inspected body. These checks do not prove the document has never been edited.

Native mathematical structures contain symbols not recoverable by concatenating text nodes: summation signs, subscripts, and delimiter punctuation must be inspected structurally. The exposure equation P048 contains two native summations and an indicator condition; its flattened string alone is not grounds for alleging a missing summation or a new scientific error.

## 9. Minimal Final-Fix List

1. **Assemble the current manuscript's frozen tables.** Resolve all current callouts, add IV/VI callouts if the nine-table inventory remains, and verify caption numbering, first-callout order, and placement. Decide deliberately whether the two frozen figures are retained; do not regenerate results.
2. **Repair the three probability equations** at P026/P027/P029, then visually check their delimiters and variable separators.
3. **Bound the SASRec-gap summaries** in P004/P010 to the late interval or the largest-endpoint comparison.
4. **Renumber citations and bibliography together** in actual first-use order after the final text is settled.
5. **Restore brief scope/identity qualifiers:** 96k for M1-Y preservation; PopMatch-k5 for the small N-M1 gap; k20/k50 sampling identity; candidate seed versus training seed; the paired Y threshold; Base and Amazon dataset identity.
6. **Preserve the core shared-model trajectory distinction in summaries:** seed42 validation narrowing, no corresponding test narrowing, and separate three-seed 96k endpoint replication. Keep SASRec and Amazon secondary.
7. **Finish proofing:** replace "Title"; correct/check inline-math spaces at P027/P047/P049; optionally align "strong" at P083 with the Results' measured language.
8. **Re-audit the assembled final file** for unresolved table/figure references, citation order, equation rendering, and numeric integrity. This is an assembly/proofing verification, not a request for training, inference, or additional experiments.

No paper rewrite, new experiment, new statistical test, new claim, or replacement bibliography source is required by the confirmed findings.

## 10. Final Recommendation

**NOT READY** for the exact DOCX audited here.

The frozen numerical evidence and the detailed Results are substantially consistent. The current standalone file nevertheless lacks the tables to which it delegates evidence, contains malformed probability notation, and overstates the SASRec-gap trajectory in its main summaries. These must be fixed before a submission-ready verdict is justified. A limited final assembly and wording/proofing pass, followed by re-audit, is sufficient in scope; this audit does not establish a need for new experiments.

### Read-Only Verification Record

- Sole created file: this audit report. Existing manuscript, source, code, CSV, bibliography, generated tables/figures, and agent state were not edited.
- Hash-preservation check: all 56 audited local inputs were unchanged, including the exact DOCX snapshot, evidence/registry/contracts/code, CSVs, and generated source tables.
- The required `python -B tools/stage_guard.py` was run. It reported **1 error, 0 warnings**, `UNAUTHORIZED_WIKI_MODIFICATION`, for pre-existing wiki working-tree changes. No wiki content was read or modified, and no attempt was made to reset or repair unrelated changes. This is a repository-stage hygiene result, not an additional manuscript finding.
- No full page-layout/render certification, fresh publisher-wide metadata certification, or independent rerun of historical models is claimed.

