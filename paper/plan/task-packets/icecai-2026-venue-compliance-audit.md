# ICECAI 2026 Venue Compliance Audit

## 1. Audit Scope

- Audit date: 2026-09-11 (Asia/Shanghai).
- Target venue: 2026 IEEE 8th International Conference on Electrical, Computer and Artificial Intelligence (ICECAI 2026).
- Audited artifact: `paper/builds/ieee_generic/en/main.pdf` (English submission build, 10 pages).
- Current inventory: 9 tables, 2 figures, and 25 bibliography entries.
- This is an audit-only record. No manuscript source, figure, table, bibliography, author block, keyword block, or compiled PDF was modified; no compilation or statistical computation was performed.
- The formal repository wiki was not accessed.

## 2. Executive Verdict

**Overall status: `WAIT_FOR_ORGANIZER_CONFIRMATION`.**

The current manuscript is structurally compatible with the official ICECAI LaTeX package and is within the official 4--20 page range. It is English-only, anonymous at both visible-text and PDF-metadata levels, contains readable figures and editable tables, and has a complete, continuously numbered bibliography. There is no manuscript-level P0 blocker.

Submission should nevertheless wait for organizer confirmation because current official surfaces disagree on the submission deadline, page-fee basis, author-information timing, and several formatting details. Six known P1 manuscript actions also remain: replace the keyword placeholder, add an accurate generative-AI disclosure, remove one stray Table III reference, and turn the first references to Tables V--VII into proper prose.

## 3. Authoritative Sources

| ID | Source | Accessed | Authority and use |
|---|---|---:|---|
| S1 | [ICECAI official home](https://www.icecai.org/) | 2026-09-11 | Independent conference site; dates, venue, page minimum, publication language |
| S2 | [ICECAI submission page](https://www.icecai.org/Submission) | 2026-09-11 | Submission files, originality, simultaneous-submission and plagiarism rules |
| S3 | [ICECAI registration page](https://icecai.org/Registration) | 2026-09-11 | Registration and extra-page fees |
| S4 | [ICECAI editorial policy](https://www.icecai.org/EditorialPolicy) | 2026-09-11 | Double-blind review, Turnitin screening, review process |
| S5 | [ICECAI AI-tools policy](https://www.icecai.org/GuidelinesforAITools) | 2026-09-11 | Permitted AI assistance, disclosure and author responsibility |
| S6 | [ICECAI download page](https://www.icecai.org/download) and downloaded `Templates.zip` | 2026-09-11 | Official Word/LaTeX templates and checking list |
| S7 | [AIS invitation/submission page](https://www.ais.cn/attendees/index/VZJN7V?invite=Z8427) | 2026-09-11 | User-specific submission gate and platform fee display; lower authority than S1--S6 for general rules |

The downloaded official template archive had SHA-256 `DEC187121FE981397B7F2B3A06629DF655FAC5D19AE68E6B3E301F00F194ECF7`. Its Word template, `IEEEtran.cls`, sample `.tex`, and sample PDF matched the corresponding repository template copies byte-for-byte.

## 4. Deadline and Fee Findings

### Deadline

- S1 publicly states full-paper submission closes **2026-09-11**.
- The AIS invitation page visibly labels 2026-09-11 23:59 as the second-round deadline.
- The same invitation page exposes a submission-gate timestamp corresponding to **2026-09-14 23:58 China Standard Time**.
- The later timestamp is credible evidence of a user-specific extension, but it does not supersede the public deadline without organizer confirmation.

**Classification:** `CONFLICTING_OFFICIAL_SOURCES + USER_EXTENSION_POSSIBLE + NEEDS_ORGANIZER_CONFIRMATION`.

### Ten-page fee

- S3 prices a regular paper at CNY 3,800 for 4--6 pages and CNY 400 for each page beginning with page 7: **CNY 5,400 for 10 pages**.
- S7 describes CNY 3,800 as covering 4 pages and charges CNY 400 beginning with page 5: **CNY 6,200 for 10 pages**.

**Classification:** `ORGANIZER_CONFIRMATION_REQUIRED`. Neither amount should be represented as final.

The official checking list allows 4--20 pages, so the current 10-page paper is eligible if the resulting fee is accepted. The sources do not clearly state whether references, appendices, supplementary material, biographies, or copyright pages are excluded from the page count; the conservative reading is that the entire submitted PDF counts.

## 5. Review, Identity, and Submission Files

- S4 explicitly states double-blind review. The current PDF displays `Anonymous Authors`, contains no author email, affiliation, acknowledgement, self-identifying repository link, or CJK identity clue, and has blank PDF Author metadata. No identity leakage was found.
- The official checking list simultaneously instructs authors to fill complete author information and mark the corresponding author with `*`. It does not clearly distinguish initial submission from camera-ready preparation.
- The user requirement of exactly one corresponding author with superscript `*` and email is compatible with the checklist, but its application stage is not officially resolved.
- S2 asks for a full paper in “word+pdf”, while S6 distributes an official LaTeX package. Whether a LaTeX-authored PDF must also be accompanied by a Word file needs platform or organizer confirmation.

**Initial-submission recommendation:** keep the paper anonymous until ICECAI confirms otherwise. Prepare, but do not insert, the full author block for camera-ready use.

## 6. Template and Layout

**Template match status: `COMPATIBLE_WITH_MINOR_ADAPTATION`.**

- The build uses the exact official `IEEEtran.cls` and the conference class option.
- PDF page size is US Letter (612 x 792 points), with the expected two-column IEEE layout.
- The paper has 10 pages, within the official 4--20 page range.
- The title, abstract, index terms, section hierarchy, two-column body, captions, and references visually follow the supplied IEEE sample.
- The last audited build had no unresolved citation/reference, duplicate-label, missing-character, float-placement, or overfull-box warning.
- Conference-specific copyright, DOI, footer, funding, and camera-ready metadata are absent from the official sample and must await final-paper instructions.

There are conflicts inside the official package: the sample LaTeX output uses ordinary bracketed citations, “Fig.” labels, and Roman-numbered tables, while the checking list requests superscript citations, the full word “Figure”, and Arabic table numbering. The current paper follows the actual official LaTeX template; do not override it until the organizer resolves the discrepancy.

## 7. Abstract, Keywords, and Language

- Abstract length: 232 lexical words. No explicit abstract word limit was found on S1--S6; current status is `PASS`, subject to any later submission-system limit.
- Keywords: the PDF contains `Keywords pending user decision.` The checking list requires 3--10 keywords. This is a submission-visible placeholder and a `MUST_FIX` item.
- The extracted PDF text contains no CJK characters. Figure labels, table contents, and references are English-only. The SVG companions for both figures also contain no CJK characters.
- No subtitle was found, consistent with the checking list.

## 8. Figures and Tables

### Figures

| Figure | Raster source | Effective PDF resolution | Audit result |
|---|---|---:|---|
| Figure 1 | 1644 x 1292 px, tagged 450 dpi | approximately 472 dpi | `PASS`: English labels, readable at 150%, embedded and cited |
| Figure 2 | 2012 x 1398 px, tagged 450 dpi | approximately 577 dpi | `PASS`: English labels, readable at 150%, embedded and cited |

No prohibited Lena image or Chinese figure text was found.

### Tables

All nine tables are native LaTeX tabular content rather than raster images. They remain editable, are sequentially numbered, fit the columns/page, and were readable in the rendered PDF. No Chinese table content was found.

## 9. First-reference Audit

| Object | First textual reference versus float | Status | Action |
|---|---|---|---|
| Table I | Float appears earlier on the same physical page | `SHOULD_FIX` | Optional: move or add a preceding sentence if the organizer interprets “first reference” literally |
| Table II | Text precedes float | `PASS` | None |
| Table III | Text precedes float | `PASS` | Remove a separate stray `Table III` fragment later in the RQ2 prose |
| Table IV | Text precedes float | `PASS` | None |
| Table V | First occurrence is a bare adjacent label | `MUST_FIX` | Integrate the reference into a grammatical evidence sentence |
| Table VI | First occurrence is a bare adjacent label | `MUST_FIX` | Integrate the reference into a grammatical evidence sentence |
| Table VII | First occurrence is a bare adjacent label | `MUST_FIX` | Integrate the reference into a grammatical evidence sentence |
| Table VIII | Text precedes float | `PASS` | None |
| Table IX | Float appears earlier on the same physical page | `SHOULD_FIX` | Optional: move or add a preceding sentence if required |
| Figure 1 | Text precedes float | `PASS` | None |
| Figure 2 | Text precedes float | `PASS` | None |

The two float-before-reference cases are ordinary top-float behavior, not demonstrated IEEE errors. They should not trigger layout churn without a direct venue instruction.

## 10. Citations and Bibliography

- Bibliography entries: 25; numbering is continuous from 1 to 25.
- Every bibliography entry is cited, and every manuscript citation resolves.
- Every entry contains a publication year and a DOI or URL.
- No duplicate keys or orphan entries were found.
- Citation groups are placed next to the claims they support; no detached citation-placement issue was found.
- The bibliography follows the IEEEtran output style. The checklist request for superscript bracket citations conflicts with the supplied LaTeX sample and therefore remains an organizer question, not an immediate formatting change.

### Recency

Publication-year distribution: 2026 (2), 2025 (2), 2024 (4), 2023 (5), 2022 (3), 2021 (1), 2020 (2), 2019 (1), 2018 (1), 2015 (1), 2009 (1), 2008 (1), 1993 (1).

- Strict interpretation, 2024--2026: 8/25 = **32%**.
- Broad interpretation, 2023--2026: 13/25 = **52%**.

The official material asks for recent references but does not define “recent” or state a 50% threshold. A three-calendar-year definition therefore requires confirmation. Do not add low-relevance citations solely to change this percentage.

Foundational older works that should normally be retained include bootstrap inference, implicit-feedback recommendation, matrix factorization, MovieLens, SASRec, sampled-metric bias, and target-item sampling (`efron1993bootstrap`, `hu2008implicit`, `koren2009mf`, `harper2015movielens`, `kang2018sasrec`, `krichene2020sampled`, `canamares2020target`).

### Country diversity

The bibliography clearly includes authors affiliated with at least the United States (UC San Diego/SASRec), Germany (University of Würzburg), and Spain (Universidad Autónoma de Madrid), with additional Chinese affiliations represented. This satisfies the checklist’s at-least-three-countries requirement under an affiliation-based reading.

## 11. Publication and Indexing Claims

- S1 states that accepted **and presented** papers are published in IEEE conference proceedings.
- Xplore inclusion is subject to IEEE scope and quality requirements.
- EI Compendex and Scopus are described as databases to which proceedings will be submitted; indexing is not guaranteed.
- No authoritative ICECAI 2026 statement confirming CNKI indexing was found.

Any submission-facing statement should preserve these qualifications and avoid presenting indexing as automatic or guaranteed.

## 12. Generative AI, Plagiarism, and Ethics

- S5 allows generative AI as an auxiliary language/formatting aid but keeps authors fully responsible for accuracy, originality, citations, charts, and data.
- When AI is used for manuscript writing, graphics, data collection, or analysis, S5 requires disclosure in Methodology or Acknowledgement, including tool name, version, function, and specific use.
- The current manuscript has no such disclosure. Because AI assistance was materially used in manuscript preparation, an accurate disclosure is `MUST_FIX`. It must not understate use or claim that AI generated no content if that is false.
- S4 states that new submissions are screened with Turnitin and that failure can cause desk rejection. No numeric similarity threshold is published.
- S2 prohibits plagiarism, simultaneous submission, and non-original work. No separate numeric self-plagiarism limit was found.
- The present study uses public recommendation datasets; the audited venue materials do not state that this alone requires human-subject ethics approval. Authors remain responsible for dataset licenses, privacy constraints, and truthful reporting.

## 13. Venue Requirement Matrix

| Requirement | Evidence | Status | Required response |
|---|---|---|---|
| Submission deadline | S1 public 9/11; S7 gate timestamp 9/14 | `ORGANIZER_CONFIRMATION_REQUIRED` | Obtain written confirmation that the invitation link remains valid through 9/14 |
| Paper length | Checking list: 4--20 pages; PDF: 10 | `PASS` | None |
| Ten-page fee | S3 implies CNY 5,400; S7 implies CNY 6,200 | `ORGANIZER_CONFIRMATION_REQUIRED` | Confirm base-page allowance and final invoice |
| Double-blind initial review | S4; current PDF anonymous | `PASS` | Retain anonymity unless organizer says otherwise |
| Author block timing | Double-blind policy conflicts with checklist | `ORGANIZER_CONFIRMATION_REQUIRED` | Confirm initial versus camera-ready identity rules |
| Exactly one corresponding author | Checklist uses singular and `*`, stage unclear | `ORGANIZER_CONFIRMATION_REQUIRED` | Confirm and prepare final author metadata |
| Official template | Exact official class/sample assets | `PASS` | None |
| Page size and columns | Letter, two-column IEEE build | `PASS` | None |
| Abstract | 232 words; no explicit limit found | `PASS` | Recheck submission-form field limit |
| Keywords | Placeholder; official requirement 3--10 | `MUST_FIX` | Supply 3--10 final keywords |
| English-only paper | PDF, figures, tables and references audited | `PASS` | None |
| Figure readability/resolution | Two figures readable, effective >450 dpi | `PASS` | None |
| Editable tables | Nine native LaTeX tables | `PASS` | None |
| Figures/tables cited | All objects cited | `PASS` | Improve three weak table references |
| First reference for Tables V--VII | Bare adjacent labels | `MUST_FIX` | Write grammatical first-reference sentences |
| Float before first text reference | Tables I and IX | `SHOULD_FIX` | Change only if venue requires strict physical ordering |
| Citation placement | Claim-adjacent citations | `PASS` | None |
| Citation style | Template and checklist conflict | `ORGANIZER_CONFIRMATION_REQUIRED` | Keep template style pending response |
| Figure/table label style | Template and checklist conflict | `ORGANIZER_CONFIRMATION_REQUIRED` | Keep template style pending response |
| At least five references | 25 entries | `PASS` | None |
| Every reference cited/resolved | 25/25 cited; zero unresolved | `PASS` | None |
| DOI or URL | 25/25 | `PASS` | None |
| Recent references | 32% strict; 52% broad; rule undefined | `ORGANIZER_CONFIRMATION_REQUIRED` | Ask how “past three years” is counted before refreshing |
| Three-country authorship diversity | Clear USA/Germany/Spain coverage | `PASS` | None |
| GenAI disclosure | Required by S5; absent | `MUST_FIX` | Add accurate disclosure before submission |
| Similarity screening | Turnitin required; threshold unstated | `SHOULD_FIX` | Run a pre-submission similarity check |
| Identity leakage | None found | `PASS` | Recheck after any metadata change |
| Visible placeholders | Author placeholder intentional; keyword placeholder invalid | `MUST_FIX` | Replace keywords; retain anonymous author text pending ruling |
| Bibliography integrity | Continuous, complete IEEE output | `PASS` | None |
| Word+PDF versus LaTeX submission | S2 wording conflicts with S6 package | `ORGANIZER_CONFIRMATION_REQUIRED` | Confirm required editable/source upload format |
| Copyright/DOI/footer | No definitive initial-submission instruction | `ORGANIZER_CONFIRMATION_REQUIRED` | Apply only at camera-ready stage |
| Appendix/supplement/biography allowance | Not stated | `UNKNOWN` | Treat all PDF pages as chargeable unless confirmed |
| CNKI indexing | No authoritative statement found | `UNKNOWN` | Do not claim CNKI indexing |

## 14. Prioritized Findings

### P0 — Submission blocker (0)

No demonstrated manuscript-level P0 issue.

### P1 — Must fix before submission (6)

1. Replace the keyword placeholder with 3--10 final English keywords.
2. Add an accurate GenAI-use disclosure conforming to S5.
3. Remove the isolated stray `Table III` fragment in the later RQ2 prose.
4. Rewrite the first reference to Table V as a grammatical evidence sentence.
5. Rewrite the first reference to Table VI as a grammatical evidence sentence.
6. Rewrite the first reference to Table VII as a grammatical evidence sentence.

### P2 — Should fix or verify internally (4)

1. Consider a preceding textual reference for Table I only if strict physical ordering is required.
2. Consider a preceding textual reference for Table IX only if strict physical ordering is required.
3. Run a pre-submission similarity report; do not infer a passing threshold that ICECAI has not published.
4. Prepare a targeted recent-reference refresh only if the organizer confirms the strict 2024--2026/50% interpretation.

### P3 — Camera-ready actions (2)

1. Insert the verified author affiliations, exactly one corresponding-author marker, and email after the anonymity stage ends.
2. Add copyright, DOI, conference footer, and funding information only from final-paper instructions.

### P4 — Organizer-confirmation questions (9)

1. Does the invitation link authorize submission through 2026-09-14 23:58 CST despite the public 2026-09-11 deadline?
2. Does a 10-page paper cost CNY 5,400 or CNY 6,200?
3. Should the initial double-blind file contain no author information despite the checklist?
4. Is exactly one corresponding author required, and at which stage must `*` and email appear?
5. Should LaTeX submissions use ordinary bracket citations or superscript bracket citations?
6. Should figure/table labels follow the LaTeX output or the conflicting checking-list wording?
7. How are “past three years” and any 50% recent-reference rule calculated?
8. Do references, appendices, supplements, biographies, and copyright pages count toward length and fees?
9. Must a LaTeX-authored submission include a Word file in addition to PDF/source files?

## 15. Final Assessment

The paper is **venue-adaptable with minor, evidence-preserving edits**, and no further compression is presently justified. The manuscript itself is not submission-blocked. Operational submission should wait for written organizer clarification on the deadline, fee, anonymity stage, and template/checklist conflicts, while the six P1 items can be prepared under a separately authorized manuscript-editing task.

