# Alignment Summary

Date: 2026-09-01

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

Fresh SASRec alignment runs are complete for s23/s47/s94/s188/s391. Validation-first matched comparisons show N-K0 wins at every matched point. The gap narrows by 200k but remains large.

## M1 Matched-Exposure Result

M1-48 validation-only PopMatch evaluation is complete. At matched 48k N-task exposure, N48 still beats M1-48, but only narrowly:

| pair | HR@1 gap | NDCG@5 gap | MRR gap |
|---|---:|---:|---:|
| N48 - M1-48 | +0.0088105727 | +0.0046919704 | +0.0062026432 |

This preserves the validation-first direction `N-K0 > M1` at 48k, but weakens any broad claim that N is decisively better than M1 at high matched exposure. M1-96 is now the useful conditional next point if the claim needs high-exposure alignment.

## Main Implication

Do not claim N-K0 has converged. It has not converged through 200k under the validation-first criterion.

Do not blindly continue single-seed N-K0 beyond 200k. Beyond 200k becomes repeated-pool or multi-epoch exposure and should be framed as a separate question.

## Next Minimum Work

1. Decide whether the paper/claim needs M1-96. If yes, resume M1 from checkpoint-12000 to checkpoint-24000 and evaluate validation first.
2. Do not run M1-200 unless M1-96 shows a possible crossover or the final argument specifically needs a 200k M1 endpoint.
