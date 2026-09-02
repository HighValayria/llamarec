# Evaluation Coverage Decision

Date: 2026-09-02

## What The Coverage Check Shows

Y-K0 has two different evaluation meanings:

- Y-native binary: AUC/F1/Accuracy on Yes/No preference prediction.
- Y-as-ranker: PopMatch-k5 candidate ranking by sorting candidates with P(Yes).

The current Y scaling evidence is split. Y-as-ranker ranking is almost flat from Y24 to Y96, while Y-native binary shows only a small and mixed gain by Y96:

| metric | Y24 valid | Y48 valid | Y96 valid | Y48 - Y24 | Y96 - Y48 |
|---|---:|---:|---:|---:|---:|
| AUC | 0.7761274819 | 0.7816111073 | 0.7843504067 | +0.0054836254 | +0.0027392994 |
| F1 | 0.7791746032 | 0.7848403087 | 0.7783174665 | +0.0056657055 | -0.0065228422 |
| Accuracy | 0.7190856958 | 0.7230433729 | 0.7235279864 | +0.0039576771 | +0.0004846135 |

Y-as-ranker validation changes remain small:

| metric | Y24 valid | Y48 valid | Y96 valid | Y96 - Y48 |
|---|---:|---:|---:|---:|
| HR@1 | 0.2156828194 | 0.2165638767 | 0.2211453744 | +0.0045814977 |
| NDCG@5 | 0.6002715889 | 0.5994649797 | 0.6030699894 | +0.0036050097 |
| MRR | 0.4704082232 | 0.4694772394 | 0.4741791483 | +0.0047019089 |

M1-96 validation is strong on both interfaces:

| run | binary AUC | binary F1 | binary Acc | ranking HR@1 | ranking NDCG@5 | ranking MRR |
|---|---:|---:|---:|---:|---:|---:|
| Y96 valid | 0.7843504067 | 0.7783174665 | 0.7235279864 | 0.2211453744 | 0.6030699894 | 0.4741791483 |
| M1-96 valid | 0.7868352749 | 0.7838427948 | 0.7281318149 | 0.6234361233 | 0.8291402759 | 0.7717533040 |

## Decision

Do not describe Y-K0 as fully converged based only on PopMatch ranking. The accurate statement is that Y-as-ranker utility is nearly flat through 96k, while Y-native binary improves only weakly and unevenly: AUC rises, Accuracy barely rises, and F1 falls from Y48 to Y96.

Pure Y96 has now supplied the fair Y-native comparison against M1-96. On validation, M1-96 exceeds Y96 on AUC, F1, and Accuracy while also nearly tying N96 on PopMatch-k5 ranking. If the claim is only about next-item ranking, Y96 should remain auxiliary because Y-as-ranker ranking is not the native Y objective and remains far below N/M ranking.

## Remaining Coverage Gaps

- Y96 test is missing.
- M1-48 and M1-96 test metrics are missing.
- M1 test should remain report-only and should be run after validation-based training decisions are fixed.
