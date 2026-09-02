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

Y-K0 does not improve from 24k to 48k under the Y-as-ranker PopMatch ranking view. However, Y-native binary validation still rises slightly from Y24 to Y48: AUC +0.0054836254, F1 +0.0056657055, Accuracy +0.0039576771. Therefore, pure Y96 is optional for ranking claims but justified if the paper needs a fair Y-native comparison against M1-96.

## Y-Native Binary Coverage

| run | split | AUC | F1 | Accuracy |
|---|---|---:|---:|---:|
| Y24 | valid | 0.7761274819 | 0.7791746032 | 0.7190856958 |
| Y48 | valid | 0.7816111073 | 0.7848403087 | 0.7230433729 |
| M1-48 | valid | 0.7813698559 | 0.7496657048 | 0.7127049511 |
| M1-96 | valid | 0.7868352749 | 0.7838427948 | 0.7281318149 |

M1-96 already exceeds Y48 on AUC and Accuracy, while F1 is essentially tied but slightly below Y48. A pure Y96 run would tell whether that is because Y single-task still improves with exposure or because multitask training changes the binary tradeoff.
## SASRec Matched-Exposure Result

Fresh SASRec alignment runs are complete for s23/s47/s94/s188/s391. Validation-first matched comparisons show N-K0 wins at every matched point. The gap narrows by 200k but remains large.

## M1 Matched-Exposure Result

M1-48 and M1-96 validation-only PopMatch evaluations are complete. At matched 48k N-task exposure, N48 still beats M1-48, but narrowly. At matched 96k N-task exposure, N96 only numerically beats M1-96 by a negligible margin:

| pair | HR@1 gap | NDCG@5 gap | MRR gap |
|---|---:|---:|---:|
| N48 - M1-48 | +0.0088105727 | +0.0046919704 | +0.0062026432 |
| N96 - M1-96 | +0.0003524229 | +0.0011520935 | +0.0014889868 |

This preserves the raw validation direction `N-K0 > M1` at 48k and 96k, but the 96k result should be treated as practical parity, not a decisive N advantage.


## Evaluation Coverage Note

The current exposure-scaling evidence is strongest for PopMatch-k5 candidate ranking. That is native for N-K0, M-N, and SASRec, but it is only a bridge metric for Y-K0. For Y-native claims, report binary AUC/F1/Accuracy from Y and M-Y metrics. Use `python .agent/exposure_scaling/alignment/commands/eval_coverage_summary.py` on the cloud machine to expose available binary/ranking metrics and missing test coverage.
## Main Implication

Do not claim N-K0 has converged. It has not converged through 200k under the validation-first criterion.

Do not make a strong claim that N-K0 decisively beats M1 once matched exposure is increased. The defensible claim is that M1 closes the gap by 96k and is effectively tied with N-K0 under seed42 validation.

## Next Minimum Work

1. Stop M1 scaling here unless a 200k M1 endpoint is essential for the final paper claim.
2. If M1-200 is run, treat it as an expensive endpoint/crossover check rather than a default continuation.
