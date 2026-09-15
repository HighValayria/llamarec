# ICECAI 2026 Submission Action Packet

## Current Gate

**Status: `WAIT_FOR_ORGANIZER_CONFIRMATION`.**

Do not upload a final package until the P1 manuscript actions are authorized and completed and the deadline/anonymity/file-format questions receive a usable answer. No new experiments, bootstrap runs, confidence-interval calculations, or evidence reinterpretation are needed.

## A. Organizer Message

Use the following concise message with the ICECAI contact channel. Retain the reply as submission provenance.

> Subject: ICECAI 2026 submission deadline, anonymity, template, and page-fee confirmation
>
> Dear ICECAI 2026 Secretariat,
>
> We are preparing a 10-page English paper using the LaTeX package downloaded from the ICECAI website. Could you please confirm the following before submission?
>
> 1. Our AIS invitation link currently exposes a submission gate ending on 14 September 2026, while the public site lists 11 September. Is submission through our link valid until 14 September (China Standard Time)?
> 2. For a 10-page paper, does the regular fee cover 4 pages or 4--6 pages, and what is the total fee in CNY?
> 3. Since the editorial policy states double-blind review but the checking list requests complete author information, should the initial-review PDF remain anonymous? At what stage should the corresponding-author `*` and email be added?
> 4. For LaTeX submissions, should citations, figure labels, and table numbering follow the supplied IEEE LaTeX output, or the differing wording in the checking list?
> 5. Must a LaTeX-authored submission include a Word file as well as PDF and source files?
> 6. If at least 50% of references must be from the past three years, which publication years count for a 2026 submission?
> 7. Do references and any appendix, supplement, biography, copyright, or DOI page count toward the page limit and extra-page fee?
>
> Thank you for your clarification.

## B. Actions That Do Not Need Organizer Confirmation

These require explicit manuscript-edit authorization because the present task is audit-only.

| ID | Priority | Action | Acceptance check |
|---|---|---|---|
| A1 | P1 | Replace `Keywords pending user decision.` with 3--10 final English keywords | No keyword placeholder remains; count is 3--10 |
| A2 | P1 | Add a truthful GenAI disclosure in Methodology or Acknowledgement | Names tool/version when known, function, and specific use; does not disclaim actual assistance |
| A3 | P1 | Remove the isolated later `Table III` fragment | No stand-alone fragment remains; intended Table III citation is preserved |
| A4 | P1 | Integrate Table V's first reference into prose | Reference is grammatical and tied to the supported claim |
| A5 | P1 | Integrate Table VI's first reference into prose | Reference is grammatical and tied to the supported claim |
| A6 | P1 | Integrate Table VII's first reference into prose | Reference is grammatical and tied to the supported claim |
| A7 | P2 | Generate a similarity report before upload | Report retained; any overlaps reviewed manually; no invented venue threshold |

For A2, a conservative disclosure structure is:

> During manuscript preparation, the authors used [tool and version, if available] for [language editing/translation/formatting/structured drafting or other actual functions]. The authors reviewed and verified all generated or revised text, citations, analyses, figures, and claims and remain fully responsible for the content.

This is a structure, not final wording. It must be completed from the actual tool-use record.

## C. Conditional Actions After Organizer Reply

| Trigger | Action | Do not do |
|---|---|---|
| 9/14 extension confirmed | Save the written reply and submit before the confirmed timestamp | Do not rely only on the hidden page timestamp |
| Extension denied or unanswered after public cutoff | Treat submission as closed unless the platform and organizer explicitly accept it | Do not present the invitation gate as guaranteed authorization |
| Base fee is 4--6 pages | Budget CNY 5,400 for 10 pages | Do not quote this as final before confirmation |
| Base fee is 4 pages | Budget CNY 6,200 for 10 pages | Do not quote this as final before confirmation |
| Initial file must be anonymous | Keep anonymous author text and blank PDF Author metadata | Do not add affiliations, email, funding, or identifying acknowledgements |
| Initial file must identify authors | Insert verified author metadata, one confirmed corresponding-author `*`, and email | Do not guess spelling, order, affiliation, or corresponding author |
| Template output governs style | Keep bracket citations, `Fig.`, and Roman table numbering | Do not rewrite style to match the checklist |
| Checking list governs style | Make only the explicitly confirmed style changes | Do not mix two conventions within the paper |
| Strict 2024--2026 50% rule confirmed | Perform a relevance-first literature refresh and re-audit citations | Do not remove foundational works or pad the bibliography mechanically |
| Word file required | Ask whether a faithful conversion is accepted or an official Word source is mandatory | Do not submit a lossy, unreviewed conversion |

## D. Reference Refresh Contingency

Current reference recency is 8/25 (32%) for 2024--2026 and 13/25 (52%) for 2023--2026. A refresh is unnecessary if ICECAI counts 2023--2026, but required if it explicitly demands at least 50% from 2024--2026.

If strict refresh is confirmed:

1. Preserve foundational methodological and dataset references.
2. Search only for recent work that directly supports existing claims about LLM recommendation, recommendation-oriented instruction tuning, exposure/sample efficiency, multitask specialization, candidate sampling, and sequential recommendation.
3. Prefer replacing weak or generic background citations before adding new bibliography mass.
4. Verify every new paper from a primary publication page or paper, then update the citation registry and provenance record.
5. Re-run citation-resolution, orphan-reference, claim-placement, country-diversity, and page-count checks.

## E. Submission Package Checklist

### Before upload

- [ ] Written deadline confirmation retained.
- [ ] Final page-fee basis confirmed.
- [ ] Initial-review anonymity rule confirmed.
- [ ] Required upload formats confirmed.
- [ ] Six P1 manuscript items completed under explicit edit authorization.
- [ ] Exactly 3--10 final English keywords present.
- [ ] GenAI disclosure accurately reflects actual use.
- [ ] Similarity report reviewed; no unsupported pass-threshold claim.
- [ ] All citations resolve and all bibliography entries are cited.
- [ ] No visible placeholder except an organizer-required anonymous author label.
- [ ] PDF Author metadata remains blank for anonymous review.
- [ ] No affiliation, email, acknowledgement, repository URL, or funding text leaks identity during blind review.
- [ ] English-only text confirmed in body, figures, tables, and references.
- [ ] Both figures remain legible and embedded at effective publication resolution.
- [ ] All nine tables remain editable and within layout boundaries.
- [ ] Final PDF page count checked after authorized edits.
- [ ] Upload receipt and submitted-file hash retained.

### Camera-ready only

- [ ] Author spelling, order, affiliation, ORCID if requested, and email independently verified.
- [ ] Exactly one corresponding author marked if confirmed by ICECAI.
- [ ] Copyright, DOI, footer, funding, and acknowledgements follow final instructions.
- [ ] Registration and presentation obligations assigned.
- [ ] Final source package opens and compiles in the required environment.

## F. Decision Rule

- Use `VENUE_ADAPTATION_READY` only after all P1 items are closed and organizer replies remove the operational ambiguities.
- Keep `WAIT_FOR_ORGANIZER_CONFIRMATION` while deadline, fee, anonymity, or accepted source format remains unresolved.
- Use `SUBMISSION_BLOCKED` only if ICECAI denies the extension, the submission portal rejects the package, or a mandatory requirement cannot be met.

Current decision: **`WAIT_FOR_ORGANIZER_CONFIRMATION`**.
