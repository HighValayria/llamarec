# Text Compression Judge Packet

## Current Structure

- English IEEE build: 14 pages, 80 compiled paragraphs, about 6,949 English words.
- Largest prose blocks: Results 1,546; Experimental Setup 1,005; Discussion 905; Related Work 852; Introduction 709.
- Four `contributions.*` working paragraphs add 310 source words but are not compiled and yield no page saving.
- Float warning: Results begins p5 and Discussion p8, while Results tables continue through p11; word and page savings are not linearly additive.

## Frozen Scientific Contract

- Thesis: conclusions are conditioned on supervision formulation, cumulative downstream task-sample exposure, and candidate evaluation protocol.
- RQ1-RQ5 all remain.
- Contribution order: C2 primary; C4 secondary; C3 supporting; C1 framing.
- Preserve: strict temporal/same-timestamp rules; Y/N/M1 definitions; exposure definition and M1 expectation; validation/frozen-test roles; 96k multiseed versus seed42 bootstrap distinction; non-nested protocols; Amazon directional-only boundary; exposure not equal to compute/pretraining fairness.

## Frozen T/D Inputs

- T-BALANCED: 9 main tables; estimated 1.8-2.8 pages.
- D-BALANCED: keep both figures; figure=trend, table=precision, prose=headline+contrast+interpretation; estimated 0.8-1.3 pages.
- Joint T+D planning estimate: 2.4-3.8 pages, not a mechanical sum.

## Proposed P-BALANCED Reductions

| Section | Current words | Safe target | Main action |
| --- | ---: | ---: | --- |
| Abstract | 232 | 220-230 | protected; micro-trim only |
| Introduction | 709 | 560-610 | tighten design/findings/contribution repetition |
| Related Work | 852 | 620-690 | synthesize by four themes; reduce paper-by-paper narration |
| Problem Formulation | 427 | 370-405 | keep definitions/RQs; remove downstream redefinition |
| Methodology | 495 | 420-455 | keep leakage/targets/loss/QLoRA/scoring; tighten overview |
| Experimental Setup | 1,005 | 760-850 | let Tables I/II carry counts; preserve operational boundaries |
| Results | 1,546 | 1,400-1,460 | nonnumeric only; remove premature Discussion and roadmap repetition |
| Discussion | 905 | 610-700 | merge six subsections into four interpretive themes |
| Limitations | 363 | 315-340 | compact by scope theme; delete no boundary |
| Conclusion | 415 | 225-275 | three paragraphs; no second Results |

P-BALANCED saves about 950-1,450 English words and 1.1-1.8 pages beyond, and non-overlapping with, D-BALANCED's numeric plan.

## Plan Choice

| Plan | Word saving | Page saving | Combined expected final range | Risk |
| --- | ---: | ---: | ---: | --- |
| P-LIGHT | 450-700 | 0.5-0.9 | 9.7-11.2 pages | low, but still long |
| P-BALANCED | 950-1,450 | 1.1-1.8 | 8.7-10.4 pages | recommended |
| P-AGGRESSIVE | 1,800-2,350 | 2.0-2.9 | 7.6-9.4 pages | high; context and readability loss |

Recommendation: `P-BALANCED`. It has a plausible favorable path to about 8 pages, but naturally centers near 9-10 pages. Seven pages is not a defensible default target without a hard short-paper limit.

## NON_COMPRESSIBLE_CORE

1. Three-condition thesis and final takeaway.
2. RQ1-RQ5 and C2>C4>C3>C1 hierarchy.
3. H/H10, strictly earlier history, same-timestamp handling, N next-interaction not next-liked-item.
4. Complete Y/N formulation distinction and M1 shared/two-interface design.
5. Exposure includes repeats; M1 total versus expected per-task; SASRec actual consumption.
6. Validation versus frozen-test role.
7. Full seed42 trajectory versus multiseed 96k operating point.
8. Paired bootstrap versus cross-training-seed variability; no equivalence claim.
9. Non-nested candidate protocols and no isolated candidate-size claim.
10. Amazon early seed42 ranking-direction support only.
11. Downstream exposure matching does not equal compute, pretraining, tokens, FLOPs, or deployment fairness.
12. EN/ZH must be revised together with equivalent claim strength.

## Execution Prerequisite

Recovery is `PARTIAL / NOT EXECUTION-READY`: the current contract verifies 35 Markdown source hashes (the 37-file tree also contains two `.gitkeep` placeholders) and generated bilingual builds aid reconstruction, but 10 Related Work/Discussion source parts are untracked, so Git alone cannot restore the exact current Markdown. Before any prose compression, create an immutable 35-source pre-compression snapshot or equivalent commit with SHA manifest. This audit creates no snapshot and authorizes no execution.

No manuscript, table, Figure, submission, build, or PDF was modified; no recompilation, experiment-output research, Wiki access, or GPT6 Astra call occurred.
