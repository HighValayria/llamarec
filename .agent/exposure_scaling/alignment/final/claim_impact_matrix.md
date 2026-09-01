# Claim Impact Matrix

Date: 2026-09-01

| claim | current support | missing evidence | action |
|---|---|---|---|
| Y-K0 saturates early | Supported by validation: Y24 and Y48 are effectively flat/slightly worse on NDCG/MRR | none for current stage | keep claim conservative |
| N-K0 improves with exposure through 200k | Supported by validation N24/N48/N96/N200 monotonic gains | no multi-seed confidence yet | report as seed42 validation evidence |
| N-K0 has converged | Not supported | N continues improving through N200 | do not claim convergence |
| N-K0 > SASRec at matched exposure | Supported by fresh validation comparisons at 24k/48k/96k/200k; gap narrows at 200k but remains positive | multi-seed confidence if needed | report as seed42 matched-exposure evidence |
| N-K0 > M1 at 48k matched N-task exposure | Supported but narrow: N48 beats M1-48 by HR@1 +0.0088, NDCG@5 +0.0047, MRR +0.0062 | M1-96 if high-exposure trend matters | soften claim; run M1-96 only if needed |
| SASRec s3000 is a fair N200 comparator | Not supported | s3000 is 1.53M processed examples, repeated-pool exposure | treat as repeated-exposure anchor only |
