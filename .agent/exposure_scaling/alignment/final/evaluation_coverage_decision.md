# Evaluation Coverage Decision

Date: 2026-09-02

## What The Coverage Check Shows

Y-K0 has two different evaluation meanings:

- Y-native binary: AUC/F1/Accuracy on Yes/No preference prediction.
- Y-as-ranker: PopMatch-k5 candidate ranking by sorting candidates with P(Yes).

The current Y scaling evidence is split. Y-as-ranker ranking is flat from Y24 to Y48, but Y-native binary still rises slightly:

| metric | Y24 valid | Y48 valid | delta |
|---|---:|---:|---:|
| AUC | 0.7761274819 | 0.7816111073 | +0.0054836254 |
| F1 | 0.7791746032 | 0.7848403087 | +0.0056657055 |
| Accuracy | 0.7190856958 | 0.7230433729 | +0.0039576771 |

M1-96 validation is strong on both interfaces:

| run | binary AUC | binary F1 | binary Acc | ranking HR@1 | ranking NDCG@5 | ranking MRR |
|---|---:|---:|---:|---:|---:|---:|
| M1-96 valid | 0.7868352749 | 0.7838427948 | 0.7281318149 | 0.6234361233 | 0.8291402759 | 0.7717533040 |

## Decision

Do not describe Y-K0 as fully converged based only on PopMatch ranking. The accurate statement is that Y-as-ranker utility stalls from 24k to 48k, while Y-native binary still has a small positive slope.

Pure Y96 is justified if the paper needs a fair Y-native comparison against M1-96, because M1-96 has 96k Y exposure and 96k N exposure. If the claim is only about next-item ranking, Y96 is lower priority because Y-as-ranker ranking was already flat by 48k.

## Remaining Coverage Gaps

- Y96 validation/test are missing.
- M1-48 and M1-96 test metrics are missing.
- M1 test should remain report-only and should be run after validation-based training decisions are fixed.
