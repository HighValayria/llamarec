# Claim Evidence Matrix

| ID | Strength | Paper wording | Limitations |
|---|---|---|---|
| C1 | CORE | Preference and next-interaction supervision induce different recommendation capabilities. | Y-as-ranker is a bridge metric, not Y native objective |
| C2 | SUPPORTED | Y-side gains weaken by 96k, while N-native ranking continues to improve through 200k. | Do not write strict convergence; tested range only |
| C3 | CORE | N-native ranking remains exposure-sensitive through the 200k near-full-pool point. | N200 is near-full-pool anchor, not converged endpoint |
| C4 | SUPPORTED | M1-96 preserves Y-native preference capability without detectable degradation. | Do not claim overall positive transfer |
| C5 | SUPPORTED | Under k5 validation, the N96-M1-96 gap is statistically compatible with parity. | Limited to k5 validation |
| C6 | SUPPORTED | Harder candidate protocols reveal a remaining N-side robustness advantage for the dedicated model. | Candidate size and composition are confounded; protocols are not nested |
| C7 | CORE | At approximately matched task-sample exposure, N-K0 outperforms SASRec across the evaluated exposure points. | Exposure matching is sample-based, not FLOPs/wall-clock matched |
