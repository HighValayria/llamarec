# ICECAI 2026 Venue Adaptation Execution Report

Date: 2026-09-11  
Status: `VENUE_ADAPTED_AWAITING_USER_METADATA`

## A. Scope

Executed only the frozen R-BALANCED reference refresh, minimal bilingual citation wording changes, five keywords, Tables III--VII textual-reference repairs, a dedicated ICECAI build layer, rebuilds, validation, contract migration, and audit. No author identity or GenAI disclosure was supplied; no experiment, metric, bootstrap, CI, table payload, figure data, Abstract, Word conversion, compression, or submission action was performed.

## B. R1--R5 Execution

| ID | Old source | Action | Final source | Result |
| --- | --- | --- | --- | --- |
| R1 | InstructRec 2023 preprint | Same-work metadata upgrade | ACM TOIS 2025, DOI `10.1145/3708882` | PASS |
| R2 | Sequential scaling 2023 preprint | Same-work metadata upgrade | RecSys 2024, DOI `10.1145/3640457.3688129` | PASS |
| R3 | Dallmann et al. 2021 | Replace | Pereira, Said, and Santos, RecSys 2025, DOI `10.1145/3705328.3748086` | PASS |
| R4 | Dacrema et al. 2019 | Replace | Milogradskii et al., RecSys 2024, DOI `10.1145/3640457.3688073` | PASS |
| R5 | Rendle et al. 2022 | Replace | Shehzad and Jannach, RecSys 2025, DOI `10.1145/3705328.3748156` | PASS |

R1/R2 retain their citation keys and scientific roles. R3 was narrowed to general sampling-strategy reliability; no Dallmann-specific full/uniform/popularity, model, dataset, or repeat-count details were transferred. R4 is limited to baseline replicability/tuning and does not imply SASRec evaluation. R5 is limited to standardized evaluation and competitive tuned conventional baselines and is not the repository's SASRec implementation source.

## C. Bibliography Diff

The active bibliography remains 25 references: two same-work publication upgrades, three scientific replacements, zero additions. All frozen classic, method/dataset, and novelty-boundary references remain active. The five deliberately uncited inventory records remain outside the active cited count and are not counted as active orphans.

## D. Recency Calculation

Final active cited references: 25. References published in 2024--2026: 13. Ratio: `13/25 = 52%`. ICECAI threshold `>=50%`: `PASS`. R1/R2 use the final formal-publication year, without treating that year as new scientific evidence.

## E. Country Check

`PASS`. Active-reference evidence explicitly covers at least China (`zhang2023instructrec`), the United States (`kang2018sasrec`), and Spain (`canamares2020target`). This is compliance evidence only and is not written into the manuscript.

## F. Citation-Slot Repairs

- `results.rq2.p01`: removed only the duplicate Table III marker; the legitimate Table III reference remains in `results.rq1.p01`.
- `results.rq3.p01`: Table V now routes to seed42 paired-bootstrap intervals; Table VI routes to the three-seed 96k summary.
- `results.rq3.p02`: Table IV now attaches to the seed42 trajectory; Table VI attaches to the three-seed 96k evidence.
- `results.rq3.p03`: Table VI now attaches to multiseed mean/SD; Table VII attaches to the seed42 paired interval.
- `results.rq4.p01--p02`: Table VI now denotes the three-seed protocol summary and Table VII the seed42 paired-bootstrap protocol intervals.

No number or scientific boundary changed. No Figure 1/2, Table II/III legitimate/IV/VIII, or FLOAT_ONLY Table I/IX placement was disturbed.

## G. Keyword Update

Configured exactly five English keywords: Large language model recommendation; Recommendation supervision; Sequential recommendation; Multitask learning; Task-sample exposure. The English PDF contains only the English list and no pending-keyword placeholder.

## H. ICECAI Adapter and Config

Created `paper/submission/icecai_2026/` while leaving `paper/submission/ieee_generic/` unchanged. The venue layer inherits the existing IEEE generator and adds English/bilingual pre-final builds, five keywords, conditional author validation, exactly-one-corresponding validation, corresponding-name `*`, corresponding email rendering, a disabled user-supplied disclosure slot, 13/25 recency validation, and three-country evidence validation. It emits 9 tables, 2 figures, and the active bibliography.

## I. Author Manual Gate

`AUTHOR_INFO_STATUS = USER_MANUAL_COMPLETION_REQUIRED`. The current PDF uses the detectable `AUTHOR INFORMATION REQUIRED` pre-final placeholder. Real author data must be entered in the dedicated config; final submission mode rejects missing fields and anything other than exactly one corresponding author. Instructions: `paper/submission/icecai_2026/AUTHOR_INPUT_REQUIRED.md`.

## J. GenAI Manual Gate

`GENAI_DISCLOSURE_STATUS = USER_MANUAL_COMPLETION_REQUIRED`. The disclosure slot is disabled and renders no manuscript text. Only user-supplied text can be enabled. Instructions: `paper/submission/icecai_2026/GENAI_DISCLOSURE_INPUT_REQUIRED.md`.

## K. Word Issue

`WORD_REQUIREMENT_STATUS = ORGANIZER_OR_PORTAL_CONFIRMATION_REQUIRED`. No DOCX was created and no LaTeX-to-Word conversion was attempted.

## L. EN/ZH Parity

`PASS`. English and bilingual builds contain the same 76 paragraph IDs, identical English paragraph fingerprint, identical 25 citation keys, and synchronized EN/ZH claims, scope, evidence roles, and table routing in every changed paragraph.

## M. Compile

English: `COMPILED`, 10 pages before and 10 pages after. Bilingual review: `COMPILED`, 16 pages after natural reflow. Both builds have zero overfull boxes, undefined citations, undefined references, missing characters, duplicate labels, and unprocessed floats. The English submission fee estimate therefore remains RMB 6,200 under the organizer-confirmed rule; no page optimization was performed.

## N. Visual Audit

`PASS_AUTOMATED_RENDER_AND_LAYOUT_AUDIT`. The final English PDF was rasterized across all 10 pages. All pages are nonblank; no raster content touches the page border; no extracted text origin lies outside the media box. Nine unique table labels, two figure labels, two embedded figures, the five keywords, and all five refreshed DOI strings are present. The English PDF contains no CJK text and no unexpected placeholder; the author placeholder is explicitly allowed. Formal figure bytes and all nine table CSV hashes match the parent contract. The local image-display helper failed with a pre-existing Windows sandbox setup error, so the audit is based on complete-page raster, PDF-object, text-coordinate, compile-log, and frozen-asset checks rather than an interactive image viewer.

## O. Tests

Final result: `70/70 PASS`.

- Manuscript, assembly, evidence, citation, bilingual, original-14-table archive, compact-table lineage, and current-contract tests: 53/53.
- Generic IEEE submission tests: 11/11.
- ICECAI adapter, author/disclosure guards, keyword, recency, country, and EN/ZH identity tests: 6/6.

The first post-edit run correctly reported two failures because the test helper still pointed to the old post-compression contract. After creating the new child contract and moving only the current-contract pointer, the full suite passed; neither old contract was modified.

## P. Remaining Submission Gates

- Gate A: user fills real author information.
- Gate B: user marks exactly one corresponding author.
- Gate C: user supplies the corresponding email.
- Gate D: user writes and enables the disclosure manually.
- Gate E: user confirms whether the portal truly requires Word.

After Gates A--D, perform one final author-bearing rebuild and final visual check. Current state is pre-final and must not be represented as ready to submit.
