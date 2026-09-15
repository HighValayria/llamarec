# ICECAI 2026 Reference Refresh Plan

## 1. Scope and Frozen Rules

- Stage type: `PLAN / RESEARCH ONLY`.
- Audit date: 2026-09-11.
- No manuscript, table, figure, bibliography, submission adapter, metadata, or PDF is modified in this stage.
- Organizer-confirmed rules are treated as closed facts: effective submission deadline 2026-09-14; 4-page base fee RMB 3,800; pages 5 onward RMB 400/page; current 10-page estimate RMB 6,200; initial PDF must contain author information; exactly one corresponding author must carry a superscript `*` and corresponding email.
- Strict recency window: publication years 2024--2026. Current active bibliography: 8/25 recent references (32%). Required final ratio: at least 50%.
- Compression remains closed: `COMPRESSION_STOP_RECOMMENDED`; no further compression is planned.
- The five uncited records already present in `library.bib` are inventory only and are not counted among the current 25 references.

## 2. Current 25-reference Classification

The classification below assigns one primary role to every active reference. `METHOD_DATASET_KEEP` is kept separate because these sources identify the actual model, adaptation method, or dataset and cannot be replaced by a topically newer paper.

| # | Current key | Year | Primary class | Protected scientific role |
|---:|---|---:|---|---|
| 1 | `he2023zeroshotconv` | 2023 | `NOVELTY_BOUNDARY_KEEP` | Early zero-shot conversational-recommendation precedent |
| 2 | `hou2024zeroshotrankers` | 2024 | `RECENT_KEEP` | Zero-shot LLM ranking precedent |
| 3 | `bao2023tallrec` | 2023 | `NOVELTY_BOUNDARY_KEEP` | Recommendation-specific Yes/No tuning and selected-example comparison precedent |
| 4 | `geng2022p5` | 2022 | `NOVELTY_BOUNDARY_KEEP` | Unified language-interface, single/multitask, and data-amount precedent |
| 5 | `zhao2024llmrec` | 2024 | `RECENT_KEEP` | Current LLM-recommender field context |
| 6 | `hu2008implicit` | 2008 | `CLASSIC_KEEP` | Foundational implicit-feedback preference/confidence distinction |
| 7 | `kang2018sasrec` | 2018 | `CLASSIC_KEEP` | Original SASRec and next-item prediction source |
| 8 | `liu2025itdr` | 2025 | `RECENT_KEEP` | Recent recommendation instruction-tuning and task/data ablation evidence |
| 9 | `krichene2020sampled` | 2020 | `CLASSIC_KEEP` | Foundational sampled-metric ordering result |
| 10 | `canamares2020target` | 2020 | `CLASSIC_KEEP` | Foundational target-item/candidate-set construction result |
| 11 | `dallmann2021sampling` | 2021 | `REPLACEABLE_SUPPORT` | Supporting example of sampling-strategy sensitivity; newer direct evidence exists |
| 12 | `zhou2025openonerec` | 2025 | `RECENT_KEEP` | Recent unified recommendation, task weighting, and low-data context |
| 13 | `penha2024bridging` | 2024 | `RECENT_KEEP` | Recent specialist/shared search-recommendation and data-allocation precedent |
| 14 | `zhang2023instructrec` | 2023 record | `NOVELTY_BOUNDARY_KEEP` | Instruction-format and hard-candidate precedent; same work has a 2025 TOIS version |
| 15 | `koren2009mf` | 2009 | `CLASSIC_KEEP` | Foundational rating-oriented matrix-factorization source |
| 16 | `onerecteam2026onereason` | 2026 | `RECENT_KEEP` | Recent expert/unified-student precedent |
| 17 | `dacrema2019progress` | 2019 | `REPLACEABLE_SUPPORT` | General baseline-tuning/reproducibility support; not the historical origin of a manuscript claim |
| 18 | `rendle2022ials` | 2022 | `REPLACEABLE_SUPPORT` | Additional baseline-tuning support; not used to identify the paper's implemented baseline |
| 19 | `zhang2023seqscaling` | 2023 record | `NOVELTY_BOUNDARY_KEEP` | Sequential data/model scaling precedent; same work was published at RecSys 2024 |
| 20 | `meta2024llama32` | 2024 | `RECENT_KEEP` | Exact base-model identity |
| 21 | `dettmers2023qlora` | 2023 | `METHOD_DATASET_KEEP` | Original QLoRA/NF4 method source |
| 22 | `hu2022lora` | 2022 | `METHOD_DATASET_KEEP` | Original LoRA method source |
| 23 | `harper2015movielens` | 2015 | `METHOD_DATASET_KEEP` | Canonical MovieLens dataset source |
| 24 | `hou2026amazonreviews` | 2026 | `RECENT_KEEP` | Amazon Reviews 2023 dataset/version source |
| 25 | `efron1993bootstrap` | 1993 | `CLASSIC_KEEP` | Original bootstrap-method source |

Primary-class counts before refresh:

- `CLASSIC_KEEP`: 6.
- `NOVELTY_BOUNDARY_KEEP`: 5.
- `METHOD_DATASET_KEEP`: 3.
- `REPLACEABLE_SUPPORT`: 3.
- `RECENT_KEEP`: 8.
- Total: 25.

No classic, method/dataset, or novelty-boundary reference is selected for scientific replacement.

## 3. Verified Recent Candidate Fit

Only primary publication pages, DOI records, author pages, proceedings pages, or the paper's own arXiv record were used to establish candidate identity and fit.

| Candidate | Identity and primary source | Existing claim supported | Action fit | Strength |
|---|---|---|---|---|
| Zhang et al., *Recommendation as Instruction Following: A Large Language Model Empowered Recommendation Approach* | ACM TOIS 43(5), Article 114, 2025; DOI [10.1145/3708882](https://doi.org/10.1145/3708882) | `rw.llm.p02`: pointwise/pairwise/matching/reranking instruction interfaces; `rw.evaluation.p01`: retrieved hard candidates | Bibliographic upgrade of the same work; replaces the 2023 preprint record, not the scientific source | `STRONG` |
| Zhang et al., *Scaling Law of Large Sequential Recommendation Models* | RecSys 2024, pp. 444--453; DOI [10.1145/3640457.3688129](https://doi.org/10.1145/3640457.3688129) | `rw.evaluation.p02`: data-pool size and repetition in sequential recommendation | Bibliographic upgrade of the same work; replaces the 2023 arXiv-only record | `STRONG` |
| Pereira, Said, and Santos, *On the Reliability of Sampling Strategies in Offline Recommender Evaluation* | RecSys 2025, pp. 360--369; DOI [10.1145/3705328.3748086](https://doi.org/10.1145/3705328.3748086); [arXiv:2508.05398](https://arxiv.org/abs/2508.05398) | `intro.p04` and `rw.evaluation.p01`: candidate sampling can distort metric values and model rankings; outcomes depend on sampling strategy, size, and exposure conditions | Replace `dallmann2021sampling` | `STRONG` |
| Milogradskii et al., *Revisiting BPR: A Replicability Study of a Common Recommender System Baseline* | RecSys 2024, pp. 267--277; DOI [10.1145/3640457.3688073](https://doi.org/10.1145/3640457.3688073); [arXiv:2409.14217](https://arxiv.org/abs/2409.14217) | `rw.evaluation.p02`: implementation details and hyperparameter tuning can materially change the apparent competitiveness of a standard baseline | Replace `dacrema2019progress` | `STRONG` |
| Shehzad and Jannach, *Revisiting the Performance of Graph Neural Networks for Session-based Recommendation* | RecSys 2025, pp. 842--846; DOI [10.1145/3705328.3748156](https://doi.org/10.1145/3705328.3748156) | `rw.evaluation.p02`: established baselines can remain competitive under standardized evaluation and adequate tuning | Replace `rendle2022ials` | `STRONG` |

### Candidates deliberately not selected

| Candidate | Potential relationship | Fit | Decision |
|---|---|---|---|
| Lyu et al., *LLM-Rec: Personalized Recommendation via Prompting Large Language Models* (Findings of NAACL 2024), DOI [10.18653/v1/2024.findings-naacl.39](https://doi.org/10.18653/v1/2024.findings-naacl.39) | Recent LLM-based personalized recommendation context | `MODERATE` | `NONE`: does not directly replace the paper's instruction-tuning, exposure, or candidate-protocol evidence |
| Yuan et al., *SOLAR: Serendipity Optimized Language Model Aligned for Recommendation* (Findings of EMNLP 2025), DOI [10.18653/v1/2025.findings-emnlp.538](https://doi.org/10.18653/v1/2025.findings-emnlp.538) | Recent recommendation-oriented instruction tuning | `MODERATE` | `NONE`: serendipity-specific and unnecessary for an existing claim slot |
| Gusak et al., *Time to Split: Exploring Data Splitting Strategies for Offline Evaluation of Sequential Recommenders* (RecSys 2025), DOI [10.1145/3705328.3748164](https://doi.org/10.1145/3705328.3748164) | Recent evidence that evaluation design affects model rankings | `MODERATE` | `NONE`: split-focused, whereas the manuscript's cited sentence is about candidate construction |
| *Scaling Sequential Recommendation Models with Transformers* (arXiv:2412.07585) | Recent sequential-scaling study | `MODERATE` | `NONE`: the formally published 2024 version of the already-cited scaling paper is a cleaner, smaller change |
| Existing uncited OneRec/OneRec-Think records | Recent generative recommendation | `WEAK` for current open slots | `NONE`: adding them would duplicate the already-cited OpenOneRec/OneReason context and constitute citation padding |

## 4. Recommended Reference Plan: R-BALANCED

The plan changes five bibliography records but introduces only three different scientific works. Two actions are metadata upgrades to formally published versions of already-cited works.

| ID | Current ref | Action | New ref | Claim location | Why safe | Prose impact |
|---|---|---|---|---|---|---|
| R1 | `zhang2023instructrec` (2023 arXiv) | `BIBLIOGRAPHIC_UPGRADE` | Zhang et al., TOIS 2025, DOI 10.1145/3708882 | `rw.llm.p02`, `rw.evaluation.p01` | Same title, authors, and scientific work; the historical attribution is preserved while the formal 2025 publication is cited | None expected |
| R2 | `zhang2023seqscaling` (2023 arXiv) | `BIBLIOGRAPHIC_UPGRADE` | Zhang et al., RecSys 2024, DOI 10.1145/3640457.3688129 | `rw.evaluation.p02` | Same scientific work; corrects arXiv-only metadata to the peer-reviewed proceedings version | None expected |
| R3 | `dallmann2021sampling` | `REPLACE` | Pereira et al., RecSys 2025, DOI 10.1145/3705328.3748086 | `intro.p04`, `rw.evaluation.p01` | Directly examines sampled offline evaluation, multiple samplers, sample size, exposure bias, fidelity, and model-ranking reliability; Krichene and Cañamares remain to preserve the foundational history | `MINOR_PROSE_ADAPTATION`: avoid attributing the exact old full/uniform/popularity design to the new paper; state the shared higher-level sampling-sensitivity result |
| R4 | `dacrema2019progress` | `REPLACE` | Milogradskii et al., RecSys 2024, DOI 10.1145/3640457.3688073 | `rw.evaluation.p02` | Direct replicability evidence that implementation and hyperparameter tuning alter a standard baseline's performance | None or a noun-level change from generic reproducibility to baseline replicability |
| R5 | `rendle2022ials` | `REPLACE` | Shehzad and Jannach, RecSys 2025, DOI 10.1145/3705328.3748156 | `rw.evaluation.p02` | Standardized comparison shows carefully tuned established baselines remain competitive; it supports the existing baseline-tuning statement without identifying the paper's SASRec implementation | None expected |

### Recency arithmetic

- Start: 8 recent / 25 total = 32%.
- R1 and R2 convert two existing arXiv-only 2023 records to their formal 2025 and 2024 publications: 10/25.
- R3--R5 replace three old supporting works with three 2024--2025 primary works: 13/25.
- Final: **13 recent / 25 total = 52%**.
- `REPLACE` (different scientific work): 3.
- `BIBLIOGRAPHIC_UPGRADE` (same scientific work): 2.
- `ADD`: 0.
- Classic references incorrectly replaced: 0.

This is the smallest natural plan found. It meets the strict rule without increasing the bibliography length or removing origin, method, dataset, or novelty-boundary sources.

## 5. Historical Meaning Guard

- Keep P5, TALLRec, the 2023 zero-shot conversational paper, and the substantive InstructRec work because they establish historical task and adaptation precedents.
- R1 and R2 must be recorded as formal-publication upgrades, never as newly invented 2024/2025 findings.
- Keep the original SASRec, MovieLens, bootstrap, implicit-feedback, matrix-factorization, LoRA, QLoRA, sampled-metric, and target-item-sampling sources.
- The replacement candidates may support current context, baseline sensitivity, or evaluation sensitivity. They must not be used to claim that LlamaRec is first, that prior studies lacked data analysis, or that candidate count alone causes the observed gaps.
- Do not cite the selected papers for numerical or experimental facts specific to this repository.

## 6. Country-source Check

The current bibliography visibly exceeds the three-country rule. Under R-BALANCED, removing Dallmann et al. removes the clearest German example, but the final set still clearly covers at least:

- United States: UC San Diego and other US-affiliated sources.
- Spain: Cañamares and Castells, Universidad Autónoma de Madrid.
- China: P5/TALLRec/InstructRec and other recommendation sources.
- Austria: Shehzad and Jannach.
- Brazil/Sweden: Pereira, Said, and Santos.
- Russia: Milogradskii et al.

Therefore the refresh does not endanger the at-least-three-countries requirement.

## 7. Figure/Table First-reference Plan

| Object | First textual reference paragraph | Status | Planned action |
|---|---|---|---|
| Figure 1 (`n_native_exposure`) | `results.rq2.p02` | `PASS` | None |
| Figure 2 (`n_vs_sasrec_exposure`) | `results.rq5.p01` | `PASS` | None |
| Table I (`datasets`) | `methods.datasets.p01` | `FLOAT_ONLY` | No source change; legal float placement only |
| Table II (`training_exposure_compact`) | `methods.exposure.p02` | `PASS` | None |
| Table III (`supervision_semantics_compact`) | `results.rq1.p01` | `PASS` | Keep the proper RQ1 citation; remove only the duplicate isolated tag in `results.rq2.p01` |
| Table IV (`exposure_scaling`) | `results.rq2.p02` | `PASS` | None |
| Table V (`specialist_multitask`) | `results.rq3.p01` | `NEEDS_SENTENCE_FIX` | Identify Table V as the seed42 paired-bootstrap interval source within a grammatical sentence |
| Table VI (`ms96_delta_summary_compact`) | `results.rq3.p01` | `NEEDS_SENTENCE_FIX` | Identify Table VI as the three-seed 96k delta summary within a grammatical sentence |
| Table VII (`hard_candidate_compact`) | `results.rq3.p03` | `NEEDS_SENTENCE_FIX` | Identify Table VII as the seed42 protocol/interval evidence within a grammatical sentence |
| Table VIII (`n_vs_sasrec_exposure`) | `results.rq5.p01` | `PASS` | None |
| Table IX (`cross_dataset`) | `results.amazon.p01` | `FLOAT_ONLY` | No source change; legal float placement only |

Exact paragraph-level repair intentions:

| Paragraph | Current issue | Required change intent |
|---|---|---|
| `results.rq2.p01` | Duplicate isolated Table III tag after a complete sentence | Remove the duplicate tag; retain Table III's proper first citation in `results.rq1.p01` |
| `results.rq3.p01` | First references to Tables V and VI are adjacent bare labels | Add one compact evidence-routing clause that distinguishes seed42 paired intervals (V) from three-seed summaries (VI) |
| `results.rq3.p02` | Later Tables IV and VI labels are bare | Attach both references to their respective trajectory and replication claims without adding new interpretation |
| `results.rq3.p03` | Table VII's first reference is a bare label beside Table VI | Attach VI to multiseed direction/dispersion and VII to seed42 paired intervals |
| `results.rq4.p01` and `results.rq4.p02` | Repeated Tables VI/VII labels remain syntactically detached | Integrate the references into existing evidence sentences; do not repeat numerical content |

No replacement prose is authorized in this stage. Tables I and IX must not be moved solely to make their rendered float precede/follow the source mention.

## 8. Keywords

### Recommended 5

1. Large language model recommendation
2. Recommendation supervision
3. Sequential recommendation
4. Multitask learning
5. Task-sample exposure

### Alternates

- Candidate-set evaluation
- Instruction tuning

The recommended set names the model family, central supervision question, sequential comparison, shared/specialist axis, and paper-specific exposure construct. `Candidate-set evaluation` can replace `Instruction tuning` only if the authors want the evaluation boundary represented more strongly.

## 9. Verifiable AI-use Inventory

| Use category | Repository evidence | Status and boundary |
|---|---|---|
| Manuscript language/writing assistance | Bilingual authoring, section drafting/revision, compression, abstract/conclusion review, and venue-adaptation task packets are recorded throughout `paper/plan/` and `paper/references/` | `CONFIRMED`: AI assistance was material, not merely spell-checking |
| Coding assistance | Repository records contain agent-authored or agent-revised analysis, paper-assembly, validation, provenance, and plotting workflows | `CONFIRMED`: disclose code-development assistance; exact model/version history is absent |
| Data-analysis assistance | Agent records organize frozen metrics, bootstrap outputs, exposure alignment, evidence matrices, and claim interpretation | `CONFIRMED_WITH_SCOPE`: assistance covered scripts, organization, checks, and interpretation of existing outputs; it must not be described as generating new experimental observations |
| Figure assistance | Formal figures were produced by `.agent/exposure_scaling/final_evidence/build_final_evidence.py` from frozen CSV evidence and later copied byte-for-byte | `CONFIRMED_WITH_ATTRIBUTION_GAP`: scripted figure preparation is clear; whether the plotting code was wholly AI-authored or AI-reviewed requires user confirmation |
| Scientific decision assistance | Cross-agent literature reconciliation, novelty/story freezing, scientific judge packets, and evidence-to-claim decisions are recorded | `CONFIRMED`: AI assisted evidence organization and framing; the raw experimental results remain repository artifacts |

Known tool identities in the records include OpenAI Codex and a Claude-produced novelty/positioning evidence package. Exact model/version identifiers, any additional ChatGPT/GPT use, and the division between AI drafting and author review are not reliably recoverable from repository files.

### User-confirmation fields before disclosure is finalized

- Exact OpenAI Codex model name(s) and version/date range used.
- Exact Claude model name/version used for the cross-agent evidence package.
- Whether ChatGPT or any other GenAI tool contributed outside the recorded repository workflow.
- Whether figure code was generated, modified, or only reviewed by GenAI.
- Whether the authors can affirm review and responsibility for all AI-assisted text, code, citations, analyses, and figures.

### Disclosure candidate A: minimal venue-compliant

After the model/version fields are confirmed, use the following two-sentence content:

> OpenAI Codex was used to assist with manuscript language editing, code development, organization of existing experimental evidence, and scripted preparation of figures from frozen data. The reported numerical results originate from recorded experiments and deterministic repository artifacts; the generative-AI tools did not create new experimental observations.

### Disclosure candidate B: slightly more explicit

After all tool identities and versions are confirmed, use the following three-sentence content:

> Generative-AI tools, including OpenAI Codex and the confirmed model used for a separate literature-positioning pass, assisted with bilingual manuscript drafting and editing, literature and evidence organization, development and review of analysis and paper-assembly code, and preparation of plots from frozen numerical artifacts. They also assisted in comparing candidate scientific framings and checking internal consistency. All reported metrics derive from recorded experiments and deterministic repository scripts; no new training run or experimental observation was generated by these tools during manuscript preparation.

Neither candidate claims human verification. A responsibility/review sentence may be added only after the authors explicitly confirm it.

## 10. Author-block Preparation

No real author metadata exists in `paper/metadata/`. The current `submission_config.yaml` contains `authors: []`, and the current adapter's camera-ready branch requires only `name` and `affiliation`; it does not yet encode corresponding-author status or email. The next authorized execution must collect and validate this minimum schema before rendering:

```yaml
authors:
  - name: ""
    affiliation:
      institution: ""
      department: ""
      city: ""
      country: ""
    email: ""
    corresponding: false
```

Hard constraints:

- At least one author.
- Every author has a verified name and affiliation.
- `sum(corresponding == true) == 1`.
- The one corresponding author's displayed name receives superscript `*`.
- The corresponding email is displayed in the required author block.
- Author order, spelling, affiliations, email visibility for non-corresponding authors, and funding/acknowledgement text are user-supplied facts and must not be inferred.

## 11. Word + PDF Status

The [official submission page](https://www.icecai.org/Submission) says “full paper (word+pdf)”, while the official download page distributes both Word and LaTeX templates. The Chinese AIS portal and English `paper-sub.com` upload fields are not publicly inspectable without entering the submission flow/login, so a technical Word-upload requirement cannot be established from the accessible pages.

`WORD_REQUIREMENT_STATUS = ORGANIZER_OR_PORTAL_CONFIRMATION_REQUIRED`.

This is an upload-format issue, not a scientific manuscript blocker. Do not convert the paper to Word in the next execution unless the portal or organizer explicitly requires it.

## 12. Execution Gate

The next stage may execute R1--R5, keywords, author metadata, disclosure, and table-reference repairs only after explicit manuscript-edit authorization and receipt of the missing author/tool fields. It must then update the citation registry/claim map, generate both language builds, compile, and verify recency, citation closure, paragraph parity, identity metadata, page count, and visual layout.

