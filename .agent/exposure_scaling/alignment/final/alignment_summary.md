# Alignment Summary

Date: 2026-08-30

## Current Status

N-K0 has completed validation-first scaling through 200k exposure and keeps improving:

| run | exposure | valid HR@1 | valid NDCG@5 | valid MRR |
|---|---:|---:|---:|---:|
| N24 | 24000 | 0.5774449339 | 0.8067686847 | 0.7420058737 |
| N48 | 48000 | 0.6029955947 | 0.8200163654 | 0.7595418502 |
| N96 | 96000 | 0.6237885463 | 0.8302923694 | 0.7732422907 |
| N200 | 200000 | 0.6516299559 | 0.8431902590 | 0.7904170338 |

Y-K0 does not improve from 24k to 48k, so Y scaling is stopped.

## SASRec Matched-Exposure Result

Fresh SASRec alignment runs are complete for s23/s47/s94/s188/s391. Validation-first matched comparisons show N-K0 wins at every matched point:

| pair | HR@1 gap | NDCG@5 gap | MRR gap |
|---|---:|---:|---:|
| N24 - SASRec s47 | +0.3043171806 | +0.1703542950 | +0.2244023495 |
| N48 - SASRec s94 | +0.3099559471 | +0.1719794261 | +0.2266431718 |
| N96 - SASRec s188 | +0.2956828194 | +0.1586617467 | +0.2096328928 |
| N200 - SASRec s391 | +0.1767400881 | +0.0870848151 | +0.1157268722 |

The gap narrows by 200k but remains large. SASRec s1500/s3000 remain repeated-exposure anchors, not fair N200 comparators.

## Main Implication

Do not claim N-K0 has converged. It has not converged through 200k under the validation-first criterion.

Do not blindly continue single-seed N-K0 beyond 200k. Beyond 200k becomes repeated-pool or multi-epoch exposure and should be framed as a separate question.

## Next Minimum Work

1. M1 alignment: run M1-48 from the existing checkpoint-3000, then compare M1 N-interface validation against N48.
2. Stop after M1-48 and decide whether M1-96 is worth the cost.
