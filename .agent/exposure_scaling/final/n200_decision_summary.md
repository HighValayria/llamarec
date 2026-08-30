# N200 Decision Summary

Cloud N200 evaluation completed on MovieLens-1M PopMatch-k5 seed42.

Validation-first N-K0 curve:

| exposure | HR@1 | NDCG@5 | MRR |
| ---: | ---: | ---: | ---: |
| 24k | 0.5774449339 | 0.8067686847 | 0.7420058737 |
| 48k | 0.6029955947 | 0.8200163654 | 0.7595418502 |
| 96k | 0.6237885463 | 0.8302923694 | 0.7732422907 |
| 200k | 0.6516299559 | 0.8431902590 | 0.7904170338 |

Validation deltas:

| transition | HR@1 | NDCG@5 | MRR |
| --- | ---: | ---: | ---: |
| N24 -> N48 | +0.0255506608 | +0.0132476807 | +0.0175359765 |
| N48 -> N96 | +0.0207929515 | +0.0102760040 | +0.0137004405 |
| N96 -> N200 | +0.0278414097 | +0.0128978895 | +0.0171747430 |

Test metrics remain report-only after validation decisions are fixed:

| exposure | HR@1 | NDCG@5 | MRR |
| ---: | ---: | ---: | ---: |
| 24k | 0.5612334802 | 0.7968087155 | 0.7289720999 |
| 48k | 0.5869603524 | 0.8106805727 | 0.7472687225 |
| 96k | 0.6100440529 | 0.8218966233 | 0.7622026432 |
| 200k | 0.6281938326 | 0.8318910144 | 0.7753803231 |

Decision:

- Do not extend Y-K0: Y 24k -> 48k showed no meaningful validation improvement.
- Treat N-K0 200k as the single-seed near-full-pool anchor, not as evidence of plateau.
- Stop blind single-seed exposure escalation here and move to consolidation: figure/table generation, SASRec comparison audit, and multi-seed or selected-repeat validation if the paper needs variance support.
