# Candidate Protocol Diagnosis

No candidate sets were regenerated. k5 uses preserved candidate files; k20/k50 use preserved prediction JSONL files as carriers of the candidate sets because standalone k20/k50 candidate files were not found.

## Protocol Statistics

- k5 validation: queries=5675, users=5675, sizes={"5": 5675}, positive_presence=1.000000, duplicate_rate=0.000000.
  Popularity baseline: HR@1=0.308899, NDCG@5=0.656677, MRR=0.544320; target-minus-negative popularity gap mean=23.446388; fraction negatives more popular than target=0.392247.
- k5 test: queries=5675, users=5675, sizes={"5": 5675}, positive_presence=1.000000, duplicate_rate=0.000000.
  Popularity baseline: HR@1=0.322643, NDCG@5=0.663582, MRR=0.553486; target-minus-negative popularity gap mean=24.946872; fraction negatives more popular than target=0.385242.
- k20 validation: queries=5675, users=5675, sizes={"20": 5675}, positive_presence=1.000000, duplicate_rate=0.000000.
  Popularity baseline: HR@1=0.269604, NDCG@5=0.496047, MRR=0.460894; target-minus-negative popularity gap mean=125.910345; fraction negatives more popular than target=0.177018.
- k20 test: queries=5675, users=5675, sizes={"20": 5675}, positive_presence=1.000000, duplicate_rate=0.000000.
  Popularity baseline: HR@1=0.270308, NDCG@5=0.488872, MRR=0.456475; target-minus-negative popularity gap mean=122.544577; fraction negatives more popular than target=0.185402.
- k50 validation: queries=5675, users=5675, sizes={"50": 5675}, positive_presence=1.000000, duplicate_rate=0.000000.
  Popularity baseline: HR@1=0.149075, NDCG@5=0.300432, MRR=0.298398; target-minus-negative popularity gap mean=126.116131; fraction negatives more popular than target=0.178337.
- k50 test: queries=5675, users=5675, sizes={"50": 5675}, positive_presence=1.000000, duplicate_rate=0.000000.
  Popularity baseline: HR@1=0.145374, NDCG@5=0.298343, MRR=0.295211; target-minus-negative popularity gap mean=122.672391; fraction negatives more popular than target=0.185051.

## Pairwise Overlap

- validation k5 vs k20: common_queries=5675, candidate_jaccard_mean=0.042473, negative_jaccard_mean=0.000809, nested=NO.
- validation k5 vs k50: common_queries=5675, candidate_jaccard_mean=0.019484, negative_jaccard_mean=0.000966, nested=NO.
- validation k20 vs k50: common_queries=5675, candidate_jaccard_mean=0.018268, negative_jaccard_mean=0.003777, nested=NO.
- test k5 vs k20: common_queries=5675, candidate_jaccard_mean=0.042505, negative_jaccard_mean=0.000841, nested=NO.
- test k5 vs k50: common_queries=5675, candidate_jaccard_mean=0.019444, negative_jaccard_mean=0.000926, nested=NO.
- test k20 vs k50: common_queries=5675, candidate_jaccard_mean=0.018106, negative_jaccard_mean=0.003615, nested=NO.

## Prediction-Level Diagnostics

- seed43 k5 validation: N rank mean=1.666, M1 rank mean=1.677, N margin mean=0.261849, M1 margin mean=0.257109, HR@1 disagreement=0.186960.
- seed43 k5 test: N rank mean=1.714, M1 rank mean=1.739, N margin mean=0.237682, M1 margin mean=0.230560, HR@1 disagreement=0.184670.
- seed43 k20 validation: N rank mean=5.520, M1 rank mean=7.033, N margin mean=-0.132604, M1 margin mean=-0.226938, HR@1 disagreement=0.114537.
- seed43 k20 test: N rank mean=5.696, M1 rank mean=7.228, N margin mean=-0.142124, M1 margin mean=-0.235495, HR@1 disagreement=0.108722.
- seed43 k50 validation: N rank mean=20.932, M1 rank mean=22.827, N margin mean=-0.277222, M1 margin mean=-0.378115, HR@1 disagreement=0.016740.
- seed43 k50 test: N rank mean=21.213, M1 rank mean=23.140, N margin mean=-0.287817, M1 margin mean=-0.390149, HR@1 disagreement=0.022379.
- seed44 k5 validation: N rank mean=1.664, M1 rank mean=1.677, N margin mean=0.262325, M1 margin mean=0.249736, HR@1 disagreement=0.182026.
- seed44 k5 test: N rank mean=1.721, M1 rank mean=1.743, N margin mean=0.242947, M1 margin mean=0.226035, HR@1 disagreement=0.179912.
- seed44 k20 validation: N rank mean=5.567, M1 rank mean=6.782, N margin mean=-0.161213, M1 margin mean=-0.221866, HR@1 disagreement=0.085639.
- seed44 k20 test: N rank mean=5.789, M1 rank mean=6.987, N margin mean=-0.171158, M1 margin mean=-0.226375, HR@1 disagreement=0.080352.
- seed44 k50 validation: N rank mean=20.017, M1 rank mean=22.994, N margin mean=-0.297968, M1 margin mean=-0.352430, HR@1 disagreement=0.023436.
- seed44 k50 test: N rank mean=20.248, M1 rank mean=23.281, N margin mean=-0.308588, M1 margin mean=-0.363573, HR@1 disagreement=0.021498.

The larger k20 N-M1 gap is observable in preserved predictions, while k20 differs from k5/k50 in candidate composition and ranking difficulty. This is descriptive only; these non-nested protocols do not support a causal candidate-size claim.
