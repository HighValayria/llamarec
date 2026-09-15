# FINAL FORMAT REPAIR TEXTUAL DIFF

## Scope

Input: `true_paper/ICECAI_2026_FINAL_ASSEMBLED.docx`

Output: `true_paper/ICECAI_2026_FINAL_FORMAT_REPAIRED.docx`

Substantive scientific prose was compared as an ordered sequence after excluding structural numbering, captions, display-equation numbering, and the explicitly permitted display-label changes. The 70 source and 70 final scientific paragraphs match exactly.

## Permitted Text-Level Changes

| Area | Before | After | Classification |
| --- | --- | --- | --- |
| Abstract label | `Abstract-` | `Abstract—` | Template punctuation |
| Keyword label | `Keywords-` / existing label form | `Keywords—` | Template punctuation |
| Heading prefixes | Manual `I.`, `A.`, etc. in paragraph text | Template automatic numbering | Structural formatting; visible wording preserved |
| Table caption prefixes | Manual `TABLE I` ... `TABLE VII` | Template automatic numbering | Structural formatting; visible numbering preserved |
| Figure caption prefixes | Manual `Fig. 1.` / `Fig. 2.` | Template automatic numbering | Structural formatting; visible numbering preserved |
| Reference prefixes | Manual `[1]` ... `[25]` | Template automatic numbering | Structural formatting; mapping and visible numbering preserved |
| Figure captions | `seed42` | `seed 42` | Required terminology spacing |
| Figure 2 terminology | Historical `N-K0` explanation | `N` | Required display terminology normalization |
| Table I header | `Validation` | `Val.` | Permitted single-column abbreviation |
| Table II headers | `Y exposure`, `N exposure` | `Y exp.`, `N exp.` | Permitted single-column abbreviation |
| Table III headers | `Full holdout`, `Coverage (%)` | `Full`, `Cov. (%)` | Permitted single-column abbreviation |
| Table VII row labels | `base`, `y`, `n`, `sasrec` | `Base`, `Y-as-ranker`, `N`, `SASRec` | Required display-name normalization |
| Probability separator | Ambiguous rendered operator | Native OMML conditional bar `∣` | Mathematical typography repair; semantics unchanged |
| Display equations | Unnumbered | `(1)`, `(2)`, `(3)` | Template equation numbering |

## Non-Textual Changes

- First-page section changed from full-width Abstract/Keywords to a one-column title block followed by a genuine two-column body.
- Tables I, II, III, and VII were fitted to one column.
- Tables IV, V, and VI retained full-width placement through genuine continuous sections.
- Table shading, grid-heavy borders, padding, and paragraph styles were replaced with template table formatting.
- Figures 1 and 2 were re-rendered from frozen CSV data for 3.45-inch single-column placement.
- Reference columns were balanced.
- Personal document metadata, comments, revision authors, and custom properties were removed.

## Verification Result

`SUBSTANTIVE SCIENTIFIC PROSE CHANGES = 0`

Table value differences outside the permitted header/display-label mapping: 0.

Reference-content differences: 0.
