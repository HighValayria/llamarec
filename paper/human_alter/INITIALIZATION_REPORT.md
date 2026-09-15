# DOCX Synchronization Initialization Report

- Location: `paper/human_alter/`
- Policy: one English master, one derived bilingual review copy
- Original inputs overwritten: NO
- Existing paragraph IDs reused: 78
- Managed English blocks: 101
- Paired EN/ZH blocks: 99
- English-only blocks: 2
- Tables mapped: 9
- Figures mapped: 2
- References mapped: 25
- Lowest English-master mapping score: 0.9970
- Lowest bilingual-English mapping score: 0.9970
- Lowest bilingual-Chinese mapping score: 0.9463
- Invisible-anchor visible-content difference (English): NO
- Invisible-anchor visible-content difference (Bilingual): NO
- Initial derived English blocks aligned to the master: 15
- Initial tables aligned: 0
- Initial figures aligned: 0
- EN_SYNC: PASS
- TABLE_SYNC: PASS
- REFERENCE_SYNC: PASS
- NUMERIC_PARITY: PASS
- CITATION_PARITY: PASS
- STRUCTURAL_DRIFT: 0
- ZH_UPDATE_REQUIRED: 0
- Render backend: Microsoft Word PDF export + bundled Poppler (LibreOffice was unavailable)
- English render pages: 10 before / 10 after
- Bilingual render pages: 14 before / 14 after
- English before/after mean pixel difference: 0.0
- Page-edge intrusions: 0
- Visual inspection: PASS
- Fixture tests: 7/7 PASS

The 15 initial derived-English alignments reconcile pre-existing wording or
line-break drift in `Bilingual.docx` to `English.docx`. They do not change the
English master or any Chinese block. No translation, scientific rewriting,
training, inference, evaluation, or manuscript-source edit was performed.
