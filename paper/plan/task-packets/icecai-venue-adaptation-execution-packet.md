# ICECAI Venue Adaptation Execution Packet

## Confirmed Organizer Rules

- Effective deadline: 2026-09-14.
- Fee: RMB 3,800 for 4 pages; RMB 400 per page from page 5; 10-page estimate RMB 6,200.
- Initial submitted PDF contains real author information.
- Exactly one corresponding author, marked with superscript `*`, with corresponding email.
- References from 2024--2026 must be at least 50%.
- Keep the 10-page paper; no further compression.

## Reference Actions: R-BALANCED

| Current | Action | Final source |
|---|---|---|
| `zhang2023instructrec` | Upgrade same work's metadata | Zhang et al., ACM TOIS 2025, DOI `10.1145/3708882` |
| `zhang2023seqscaling` | Upgrade same work's metadata | Zhang et al., RecSys 2024, DOI `10.1145/3640457.3688129` |
| `dallmann2021sampling` | Replace | Pereira et al., RecSys 2025, DOI `10.1145/3705328.3748086` |
| `dacrema2019progress` | Replace | Milogradskii et al., RecSys 2024, DOI `10.1145/3640457.3688073` |
| `rendle2022ials` | Replace | Shehzad and Jannach, RecSys 2025, DOI `10.1145/3705328.3748156` |

Result: 3 scientific replacements, 2 same-work publication upgrades, 0 additions; final total 25; 13 references from 2024--2026; **52% PASS**. Do not replace any classic, method/dataset, or novelty-boundary work. R3 needs a minor wording adjustment so Pereira et al. supports general sampling reliability rather than inheriting Dallmann's exact design.

## Keywords

Recommended five:

`Large language model recommendation`; `Recommendation supervision`; `Sequential recommendation`; `Multitask learning`; `Task-sample exposure`.

Alternates: `Candidate-set evaluation`; `Instruction tuning`.

## GenAI Disclosure Draft

Preferred minimal draft after exact model/version confirmation:

> OpenAI Codex was used to assist with manuscript language editing, code development, organization of existing experimental evidence, and scripted preparation of figures from frozen data. The reported numerical results originate from recorded experiments and deterministic repository artifacts; the generative-AI tools did not create new experimental observations.

User must first confirm exact Codex/Claude model versions, any additional GenAI use, figure-code attribution, and whether an author-review/responsibility sentence is factually supportable.

## Required Author Input

For each author: verified name, department/institution, city, country, and required email. Mark exactly one `corresponding: true`; render `*` on that name and display the corresponding email. Current repo state is `authors: []`; do not infer any value.

## Table/Figure Citation Fixes

- `results.rq2.p01`: remove only the duplicate isolated Table III tag.
- `results.rq3.p01`: integrate first references to Table V (seed42 paired intervals) and Table VI (three-seed summary) into one grammatical evidence-routing clause.
- `results.rq3.p02`: attach later Table IV/VI references to the claims they support.
- `results.rq3.p03`: attach Table VI to multiseed evidence and Table VII to seed42 paired/protocol evidence.
- `results.rq4.p01` and `results.rq4.p02`: integrate repeated Table VI/VII references into existing sentences.
- Figures 1--2 and Tables II--IV, VIII pass. Tables I and IX are `FLOAT_ONLY`; do not disturb layout.

## Remaining Portal Issue

`WORD_REQUIREMENT_STATUS = ORGANIZER_OR_PORTAL_CONFIRMATION_REQUIRED`.

The public page says “word+pdf” but distributes a LaTeX template; the upload control is not publicly inspectable. Do not convert to Word without confirmation.

## Execution Verification

After explicit edit authorization: update `library.bib`, citation registry/claim map and bilingual citation slots; populate author/keyword/disclosure configuration; apply only listed prose/reference fixes; rebuild English and bilingual outputs; verify 13/25 recency, zero unresolved/orphan citations, exactly one corresponding author, EN/ZH parity, no placeholders, 10-page target unless natural reflow changes it, and full visual/layout checks.
