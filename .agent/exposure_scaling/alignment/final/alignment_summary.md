# Alignment Summary

Date: 2026-09-02

## Current Status

N-K0 has completed validation-first scaling through 200k exposure and keeps improving:

| run | exposure | valid HR@1 | valid NDCG@5 | valid MRR |
|---|---:|---:|---:|---:|
| N24 | 24000 | 0.5774449339 | 0.8067686847 | 0.7420058737 |
| N48 | 48000 | 0.6029955947 | 0.8200163654 | 0.7595418502 |
| N96 | 96000 | 0.6237885463 | 0.8302923694 | 0.7732422907 |
| N200 | 200000 | 0.6516299559 | 0.8431902590 | 0.7904170338 |

Y-K0 remains weak under the Y-as-ranker PopMatch ranking view through 96k. Y-native binary improves only weakly and unevenly by Y96: AUC continues upward, Accuracy barely rises, and F1 falls from Y48 to Y96. Pure Y96 now gives the fair Y-native comparison against M1-96.

## Y-Native Binary Coverage

| run | split | AUC | F1 | Accuracy |
|---|---|---:|---:|---:|
| Y24 | valid | 0.7761274819 | 0.7791746032 | 0.7190856958 |
| Y48 | valid | 0.7816111073 | 0.7848403087 | 0.7230433729 |
| Y96 | valid | 0.7843504067 | 0.7783174665 | 0.7235279864 |
| M1-48 | valid | 0.7813698559 | 0.7496657048 | 0.7127049511 |
| M1-96 | valid | 0.7868352749 | 0.7838427948 | 0.7281318149 |

M1-96 exceeds Y96 on all three Y-native binary validation metrics: AUC +0.0024848682, F1 +0.0055253283, Accuracy +0.0046038285. This supports the claim that multitask M1 preserves or improves the Y-native binary interface at matched 96k Y exposure while also matching N96 on PopMatch-k5 ranking.

## SASRec Matched-Exposure Result

Fresh SASRec alignment runs are complete for s23/s47/s94/s188/s391. Validation-first matched comparisons show N-K0 wins at every matched point. The gap narrows by 200k but remains large.

## M1 Matched-Exposure Result

M1-48 and M1-96 validation-only PopMatch evaluations are complete. At matched 48k N-task exposure, N48 still beats M1-48, but narrowly. At matched 96k N-task exposure, N96 only numerically beats M1-96 by a negligible margin:

| pair | HR@1 gap | NDCG@5 gap | MRR gap |
|---|---:|---:|---:|
| N48 - M1-48 | +0.0088105727 | +0.0046919704 | +0.0062026432 |
| N96 - M1-96 | +0.0003524229 | +0.0011520935 | +0.0014889868 |

This preserves the raw validation direction `N-K0 > M1` at 48k and 96k, but the 96k result should be treated as practical parity, not a decisive N advantage.


## Current96 k20/k50 Robustness

Phase2A candidate-size validation checks show that PopMatch-k5 near parity does not fully generalize to larger candidate sets. N96 remains stronger than M1-96, especially under k20:

| variant | HR@1 gap N96 - M1-96 | NDCG@5 gap N96 - M1-96 | MRR gap N96 - M1-96 |
|---|---:|---:|---:|
| k20_seed42 | +0.1124229075 | +0.1269794216 | +0.1062560801 |
| k50_seed42 | +0.0170925110 | +0.0289555766 | +0.0258293602 |

These are validation metrics. Test should remain report-only after validation decisions are frozen.
## Evaluation Coverage Note

The current exposure-scaling evidence is strongest for PopMatch-k5 candidate ranking. That is native for N-K0, M-N, and SASRec, but it is only a bridge metric for Y-K0. For Y-native claims, report binary AUC/F1/Accuracy from Y and M-Y metrics. Use `python .agent/exposure_scaling/alignment/commands/eval_coverage_summary.py` on the cloud machine to expose available binary/ranking metrics and missing test coverage.
## Main Implication

Do not claim N-K0 has converged. It has not converged through 200k under the validation-first criterion.

Do not make a strong claim that N-K0 decisively beats M1 once matched exposure is increased under PopMatch-k5. The defensible claim is that M1 closes the gap by 96k and is effectively tied with N-K0 under seed42 validation, while M1-96 also beats pure Y96 on Y-native binary validation.

## Next Minimum Work

1. Stop M1 scaling here unless a 200k M1 endpoint is essential for the final paper claim.
2. If M1-200 is run, treat it as an expensive endpoint/crossover check rather than a default continuation.
