# N96 vs M1-N96 User-Level Paired Bootstrap

TRAINING_STARTED = NO

Bootstrap design: paired USER-level resampling with replacement; 10000 replicates; deterministic seed base 20260915. If a user has multiple queries, all of that user's queries are kept together.

Supported combinations: seed43 and seed44, protocols k5/k20/k50, validation/test. Seed42 is unavailable at raw prediction level.

## Consistency With Frozen Paper Results

All newly computed N96/M1-N96 aggregate metrics for feasible pairs are exact or numerically consistent with frozen protocol tables.

## Bootstrap Results

- seed43 k5 validation HR@1: delta N-M1=0.0026431718, CI [-0.0086343612, 0.0137444934], crosses zero=YES, users=5675, queries=5675.
- seed43 k5 validation NDCG@5: delta N-M1=0.0017669311, CI [-0.0030484972, 0.0064494530], crosses zero=YES, users=5675, queries=5675.
- seed43 k5 validation MRR: delta N-M1=0.0023142438, CI [-0.0041116006, 0.0085639501], crosses zero=YES, users=5675, queries=5675.
- seed43 k5 test HR@1: delta N-M1=0.0077533040, CI [-0.0033480176, 0.0188546256], crosses zero=YES, users=5675, queries=5675.
- seed43 k5 test NDCG@5: delta N-M1=0.0045732989, CI [-0.0001467761, 0.0094148873], crosses zero=YES, users=5675, queries=5675.
- seed43 k5 test MRR: delta N-M1=0.0060088106, CI [-0.0003114537, 0.0124524963], crosses zero=YES, users=5675, queries=5675.
- seed43 k20 validation HR@1: delta N-M1=0.0814096916, CI [0.0727753304, 0.0903964758], crosses zero=NO, users=5675, queries=5675.
- seed43 k20 validation NDCG@5: delta N-M1=0.1264047631, CI [0.1187309782, 0.1339456937], crosses zero=NO, users=5675, queries=5675.
- seed43 k20 validation MRR: delta N-M1=0.0912695462, CI [0.0847688255, 0.0977547876], crosses zero=NO, users=5675, queries=5675.
- seed43 k20 test HR@1: delta N-M1=0.0717180617, CI [0.0632599119, 0.0801762115], crosses zero=NO, users=5675, queries=5675.
- seed43 k20 test NDCG@5: delta N-M1=0.1221905560, CI [0.1147408516, 0.1297117339], crosses zero=NO, users=5675, queries=5675.
- seed43 k20 test MRR: delta N-M1=0.0863464972, CI [0.0800787953, 0.0926888771], crosses zero=NO, users=5675, queries=5675.
- seed43 k50 validation HR@1: delta N-M1=0.0033480176, CI [0.0000000000, 0.0066960352], crosses zero=YES, users=5675, queries=5675.
- seed43 k50 validation NDCG@5: delta N-M1=0.0046784669, CI [0.0027192412, 0.0067297154], crosses zero=NO, users=5675, queries=5675.
- seed43 k50 validation MRR: delta N-M1=0.0116551112, CI [0.0094859410, 0.0138413140], crosses zero=NO, users=5675, queries=5675.
- seed43 k50 test HR@1: delta N-M1=0.0051101322, CI [0.0012334802, 0.0089867841], crosses zero=NO, users=5675, queries=5675.
- seed43 k50 test NDCG@5: delta N-M1=0.0043670424, CI [0.0023160312, 0.0064640721], crosses zero=NO, users=5675, queries=5675.
- seed43 k50 test MRR: delta N-M1=0.0116260593, CI [0.0092528366, 0.0140022715], crosses zero=NO, users=5675, queries=5675.
- seed44 k5 validation HR@1: delta N-M1=0.0146255507, CI [0.0037004405, 0.0259030837], crosses zero=NO, users=5675, queries=5675.
- seed44 k5 validation NDCG@5: delta N-M1=0.0054001154, CI [0.0007098430, 0.0101392808], crosses zero=NO, users=5675, queries=5675.
- seed44 k5 validation MRR: delta N-M1=0.0073362702, CI [0.0010541850, 0.0136359031], crosses zero=NO, users=5675, queries=5675.
- seed44 k5 test HR@1: delta N-M1=0.0100440529, CI [-0.0008810573, 0.0211453744], crosses zero=YES, users=5675, queries=5675.
- seed44 k5 test NDCG@5: delta N-M1=0.0048050704, CI [0.0000459564, 0.0095918964], crosses zero=NO, users=5675, queries=5675.
- seed44 k5 test MRR: delta N-M1=0.0063788546, CI [0.0000524963, 0.0128048458], crosses zero=NO, users=5675, queries=5675.
- seed44 k20 validation HR@1: delta N-M1=0.0511013216, CI [0.0437004405, 0.0586784141], crosses zero=NO, users=5675, queries=5675.
- seed44 k20 validation NDCG@5: delta N-M1=0.1059372555, CI [0.0993637662, 0.1125925296], crosses zero=NO, users=5675, queries=5675.
- seed44 k20 validation MRR: delta N-M1=0.0671369880, CI [0.0617535437, 0.0727329650], crosses zero=NO, users=5675, queries=5675.
- seed44 k20 test HR@1: delta N-M1=0.0465198238, CI [0.0394669604, 0.0537444934], crosses zero=NO, users=5675, queries=5675.
- seed44 k20 test NDCG@5: delta N-M1=0.1011733518, CI [0.0946979195, 0.1076900563], crosses zero=NO, users=5675, queries=5675.
- seed44 k20 test MRR: delta N-M1=0.0633521788, CI [0.0581752426, 0.0686871280], crosses zero=NO, users=5675, queries=5675.
- seed44 k50 validation HR@1: delta N-M1=0.0103964758, CI [0.0065198238, 0.0144493392], crosses zero=NO, users=5675, queries=5675.
- seed44 k50 validation NDCG@5: delta N-M1=0.0099297278, CI [0.0077986943, 0.0121291774], crosses zero=NO, users=5675, queries=5675.
- seed44 k50 validation MRR: delta N-M1=0.0180115395, CI [0.0156096651, 0.0205259550], crosses zero=NO, users=5675, queries=5675.
- seed44 k50 test HR@1: delta N-M1=0.0112775330, CI [0.0075770925, 0.0151541850], crosses zero=NO, users=5675, queries=5675.
- seed44 k50 test NDCG@5: delta N-M1=0.0100950607, CI [0.0078921815, 0.0123767206], crosses zero=NO, users=5675, queries=5675.
- seed44 k50 test MRR: delta N-M1=0.0186628137, CI [0.0162200707, 0.0211603296], crosses zero=NO, users=5675, queries=5675.

Intervals crossing zero are not equivalence claims; different seeds and candidate protocols are not pooled as independent bootstrap samples.
