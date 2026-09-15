# Revision Analysis Ready

TRAINING_STARTED = NO

## 1. Usable Raw Prediction Pairs

- seed42 k5 validation: NO - raw N96/M1-N96 prediction pair unavailable.
- seed42 k5 test: NO - raw N96/M1-N96 prediction pair unavailable.
- seed42 k20 validation: NO - raw N96/M1-N96 prediction pair unavailable.
- seed42 k20 test: NO - raw N96/M1-N96 prediction pair unavailable.
- seed42 k50 validation: NO - raw N96/M1-N96 prediction pair unavailable.
- seed42 k50 test: NO - raw N96/M1-N96 prediction pair unavailable.
- seed43 k5 validation: YES - exact raw N96/M1-N96 pair verified.
- seed43 k5 test: YES - exact raw N96/M1-N96 pair verified.
- seed43 k20 validation: YES - exact raw N96/M1-N96 pair verified.
- seed43 k20 test: YES - exact raw N96/M1-N96 pair verified.
- seed43 k50 validation: YES - exact raw N96/M1-N96 pair verified.
- seed43 k50 test: YES - exact raw N96/M1-N96 pair verified.
- seed44 k5 validation: YES - exact raw N96/M1-N96 pair verified.
- seed44 k5 test: YES - exact raw N96/M1-N96 pair verified.
- seed44 k20 validation: YES - exact raw N96/M1-N96 pair verified.
- seed44 k20 test: YES - exact raw N96/M1-N96 pair verified.
- seed44 k50 validation: YES - exact raw N96/M1-N96 pair verified.
- seed44 k50 test: YES - exact raw N96/M1-N96 pair verified.

## 2. Can User-Level Paired Bootstrap Be Added Without Retraining?

Yes, partially: it can be added for seed43 and seed44 across k5/k20/k50 validation/test using existing raw predictions. Seed42 cannot be bootstrapped without raw prediction-level files.

## 3. Main Bootstrap Conclusions

- Non-zero intervals: 28 metric/protocol/split/seed rows.
- Intervals crossing zero: 8 metric/protocol/split/seed rows.
- seed43 k5 validation HR@1: delta=0.002643, CI [-0.008634, 0.013744], crosses_zero=YES.
- seed43 k5 validation NDCG@5: delta=0.001767, CI [-0.003048, 0.006449], crosses_zero=YES.
- seed43 k5 validation MRR: delta=0.002314, CI [-0.004112, 0.008564], crosses_zero=YES.
- seed43 k5 test HR@1: delta=0.007753, CI [-0.003348, 0.018855], crosses_zero=YES.
- seed43 k5 test NDCG@5: delta=0.004573, CI [-0.000147, 0.009415], crosses_zero=YES.
- seed43 k5 test MRR: delta=0.006009, CI [-0.000311, 0.012452], crosses_zero=YES.
- seed43 k20 validation HR@1: delta=0.081410, CI [0.072775, 0.090396], crosses_zero=NO.
- seed43 k20 validation NDCG@5: delta=0.126405, CI [0.118731, 0.133946], crosses_zero=NO.
- seed43 k20 validation MRR: delta=0.091270, CI [0.084769, 0.097755], crosses_zero=NO.
- seed43 k20 test HR@1: delta=0.071718, CI [0.063260, 0.080176], crosses_zero=NO.
- seed43 k20 test NDCG@5: delta=0.122191, CI [0.114741, 0.129712], crosses_zero=NO.
- seed43 k20 test MRR: delta=0.086346, CI [0.080079, 0.092689], crosses_zero=NO.
- seed43 k50 validation HR@1: delta=0.003348, CI [0.000000, 0.006696], crosses_zero=YES.
- seed43 k50 validation NDCG@5: delta=0.004678, CI [0.002719, 0.006730], crosses_zero=NO.
- seed43 k50 validation MRR: delta=0.011655, CI [0.009486, 0.013841], crosses_zero=NO.
- seed43 k50 test HR@1: delta=0.005110, CI [0.001233, 0.008987], crosses_zero=NO.
- seed43 k50 test NDCG@5: delta=0.004367, CI [0.002316, 0.006464], crosses_zero=NO.
- seed43 k50 test MRR: delta=0.011626, CI [0.009253, 0.014002], crosses_zero=NO.
- seed44 k5 validation HR@1: delta=0.014626, CI [0.003700, 0.025903], crosses_zero=NO.
- seed44 k5 validation NDCG@5: delta=0.005400, CI [0.000710, 0.010139], crosses_zero=NO.
- seed44 k5 validation MRR: delta=0.007336, CI [0.001054, 0.013636], crosses_zero=NO.
- seed44 k5 test HR@1: delta=0.010044, CI [-0.000881, 0.021145], crosses_zero=YES.
- seed44 k5 test NDCG@5: delta=0.004805, CI [0.000046, 0.009592], crosses_zero=NO.
- seed44 k5 test MRR: delta=0.006379, CI [0.000052, 0.012805], crosses_zero=NO.
- seed44 k20 validation HR@1: delta=0.051101, CI [0.043700, 0.058678], crosses_zero=NO.
- seed44 k20 validation NDCG@5: delta=0.105937, CI [0.099364, 0.112593], crosses_zero=NO.
- seed44 k20 validation MRR: delta=0.067137, CI [0.061754, 0.072733], crosses_zero=NO.
- seed44 k20 test HR@1: delta=0.046520, CI [0.039467, 0.053744], crosses_zero=NO.
- seed44 k20 test NDCG@5: delta=0.101173, CI [0.094698, 0.107690], crosses_zero=NO.
- seed44 k20 test MRR: delta=0.063352, CI [0.058175, 0.068687], crosses_zero=NO.
- seed44 k50 validation HR@1: delta=0.010396, CI [0.006520, 0.014449], crosses_zero=NO.
- seed44 k50 validation NDCG@5: delta=0.009930, CI [0.007799, 0.012129], crosses_zero=NO.
- seed44 k50 validation MRR: delta=0.018012, CI [0.015610, 0.020526], crosses_zero=NO.
- seed44 k50 test HR@1: delta=0.011278, CI [0.007577, 0.015154], crosses_zero=NO.
- seed44 k50 test NDCG@5: delta=0.010095, CI [0.007892, 0.012377], crosses_zero=NO.
- seed44 k50 test MRR: delta=0.018663, CI [0.016220, 0.021160], crosses_zero=NO.

## 4. Does The CI Support A Stable N Specialist Advantage?

Supported only descriptively and unevenly: k20 shows consistently positive N-M1 deltas with intervals not crossing zero in available seed43/44 evidence; k5 deltas are small and their uncertainty often includes zero; k50 is smaller than k20 and varies by metric/split/seed. Do not pool seeds or protocols as independent user samples.

## 5. Where Does Uncertainty Remain Large?

Uncertainty remains largest for small k5 deltas and for seed42, where raw prediction-level assets are missing. Any seed42 uncertainty statement would require unavailable raw predictions and must not be reconstructed from aggregate metrics.

## 6. What Distinguishes k5, k20, and k50 Candidate Protocols?

k5 is popularity-matched and has five candidates. k20/k50 are random candidate protocols carried in preserved prediction files with 20 and 50 candidates. Pairwise overlap diagnostics show the protocols are not nested and have low negative-candidate overlap, so they represent different evaluation compositions rather than a simple candidate-size ladder.

## 7. Observable Reason Why k20 Produces A Larger Gap?

The preserved evidence shows k20 has a much larger N-M1 gap than k5/k50 for seed43/44. Candidate diagnostics show k20 differs in candidate composition, popularity difficulty, and score/rank disagreement. This is an observable association, not a causal explanation.

## 8. Descriptive-Only Findings

Candidate-protocol differences, popularity gaps, overlap patterns, and k20 score/rank disagreement are descriptive only. They should not be framed as causal effects of candidate-set size because the protocols are non-nested and differ in sampling composition.

## 9. Is New Training Necessary?

No new training is necessary for the supported seed43/44 paired bootstrap and candidate-protocol diagnosis. New training would not recover seed42 raw predictions; it would create replay outputs rather than original submitted-paper prediction evidence.

REVISION_ANALYSIS_STATUS = PARTIALLY_SUFFICIENT
