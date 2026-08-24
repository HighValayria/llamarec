# Y-K0 Scaling Plan

Evaluate both Y binary quality and P(Yes)-based next-item ranking as exposure increases.

| target Y exposure | optimizer steps | status |
|---:|---:|---|
| 12000 | 1500 | current anchor |
| 24000 | 3000 | planned |
| 48000 | 6000 | planned |
| 96000 | 12000 | conditional |
| 200000 | 25000 | near-full loaded pool, conditional |

Required metrics: AUC, F1@0.5, validation-calibrated threshold, calibrated F1, and fixed PopMatch-k5 HR@1/NDCG@5/MRR using P(Yes) over candidates.

If binary improves but P(Yes)-ranking remains far below N-K0, the supervision semantic separation claim is strengthened. If Y ranking approaches N-K0, the paper claim must be revised.
