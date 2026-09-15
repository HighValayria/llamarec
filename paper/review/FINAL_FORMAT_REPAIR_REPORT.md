# FINAL FORMAT REPAIR REPORT

## Verdict

FORMAT REPAIR COMPLETE

The current assembled manuscript was repaired against the ICECAI/IEEE Word-template structure without changing substantive scientific prose. The final Word export is editable and the final PDF was rendered and inspected page by page.

## Deliverables

- DOCX: `true_paper/ICECAI_2026_FINAL_FORMAT_REPAIRED.docx`
- PDF: `true_paper/ICECAI_2026_FINAL_FORMAT_REPAIRED.pdf`
- Textual diff: `paper/review/FINAL_FORMAT_REPAIR_DIFF.md`

## Before / After

| Check | Before | After |
| --- | ---: | ---: |
| Pages | 9 | 8 |
| Tables | 7 | 7 |
| Figures | 2 | 2 |
| References | 25 | 25 |
| Page-1 abstract layout | Full width | Two-column |
| Scientific prose changes | 0 | 0 |

## Section And Column Repair

- Title and `Anonymous Authors` remain in a genuine one-column opening section.
- A continuous section break after the author block starts the genuine two-column body.
- Abstract, Keywords, and Introduction now flow through the first-page two-column section.
- Tables I, II, III, and VII are single-column objects inside the two-column body.
- Tables IV, V, and VI use genuine one-column continuous sections and span both columns.
- Figures 1 and 2 are single-column objects, each 3.45 inches wide.
- A final continuous section boundary balances the two reference columns.

## Abstract And Keywords

- `Abstract—` uses an em dash.
- `Keywords—` uses an em dash.
- The keyword list present in the assembled input was preserved; no keywords were generated or rewritten.

## Tables

- All seven tables use the template paragraph styles `table head`, `table col head`, and `table copy`.
- Spreadsheet-like gray header shading was removed; the final shading count is zero.
- Borders are lightweight and the tables use compact cell padding.
- Table values, row order, and retained columns match the assembled manuscript exactly.
- Permitted header abbreviations were applied to Tables I-III for single-column fit.
- Table VII display names were normalized to `Base`, `Y-as-ranker`, `N`, and `SASRec`.
- Visual inspection confirmed that Tables III, V, and VI are no longer split across columns/pages.

## Figures

- Both figures were deterministically re-rendered from the frozen CSV files at single-column dimensions.
- Times New Roman and approximately 8 pt axes, ticks, and legends are used.
- Internal chart titles were removed.
- The x-axis labels are `24k`, `48k`, `96k`, and `200k`.
- Figure 2 uses `N` and `SASRec`; `N-K0` does not appear in the document, captions, or regenerated plots.
- Captions use the template `figure caption` style and `seed 42` spacing.

## Equations

- The three probability expressions use the native OMML conditional operator `∣`; the logical-OR operator `∨` count is zero.
- Verified forms are Like, Yes, and NextInteraction conditional probabilities with native `H` subscript 10 structure.
- The Yes expression remains inline, matching the frozen source structure.
- The three actual display equations are numbered consecutively `(1)`, `(2)`, and `(3)` at the right margin.

## Template Styles

Style lint passed for:

- `paper title`: 1
- `Abstract`: 2
- `Keywords`: 1
- `Heading 1`: 9
- `Heading 2`: 21
- `figure caption`: 2
- `table head`: 7
- `table col head`: 43
- `table copy`: 387
- `references`: 25

Template automatic numbering is used for headings, table captions, figure captions, and references; duplicate manual numbering was removed from the underlying text.

## Privacy And Metadata

- `dc:creator`: empty
- `lastModifiedBy`: empty
- Company and manager: empty
- Custom properties: absent
- Comment parts: absent
- Tracked revisions: absent
- Nonempty author attributes: absent
- Visible author block: `Anonymous Authors`

Anonymous metadata scrub: PASS.

## Render Verification

Three render-and-review rounds were completed. The final PDF is 8 Letter pages. Every final page was visually inspected. No clipping, overlap, gray table shading, blank page, broken figure label, duplicate numbering, or reference-column overflow remains. Programmatic PDF boundary checks also found zero characters outside the page box.

## Final Checklist

- Pages = 8
- Tables = 7
- Figures = 2
- References = 25
- Page-1 abstract layout = TWO-COLUMN
- Single-column tables = I, II, III, VII
- Double-column tables = IV, V, VI
- Single-column figures = 1, 2
- Probability operators verified = `|` (OMML conditional bar `∣`)
- `N-K0` occurrences = 0
- Anonymous metadata scrub = PASS
- Template styles = PASS
- SUBSTANTIVE SCIENTIFIC PROSE CHANGES = 0
- Unresolved layout issues = none
