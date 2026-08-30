# Claim Impact Matrix

Date: 2026-08-30

| claim | current support | missing evidence | action |
|---|---|---|---|
| Y-K0 saturates early | Supported by validation: Y24 and Y48 are effectively flat/slightly worse on NDCG/MRR | none for current stage | keep claim conservative |
| N-K0 improves with exposure through 200k | Supported by validation N24/N48/N96/N200 monotonic gains | no multi-seed confidence yet | report as seed42 validation evidence |
| N-K0 has converged | Not supported | N continues improving through N200 | do not claim convergence |
| N-K0 > M1 | Old comparison was not matched at higher M1 N-task exposure | M1-48 validation/test | run M1-48 first |
| N-K0 > SASRec at matched exposure | Not resolved for 24k/48k/96k/200k | Fresh SASRec s47/s94/s188/s391 valid/test | run SASRec alignment grid |
| SASRec s3000 is a fair N200 comparator | Not supported | s3000 is 1.53M processed examples, repeated-pool exposure | treat as repeated-exposure anchor only |
