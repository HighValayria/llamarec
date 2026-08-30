# Comparison Protocol

Date: 2026-08-30

## Candidate Protocol

All aligned comparisons use fixed PopMatch-k5 seed42 candidates:

- Validation: `data/candidates/movielens-1m/variants/k5_popmatch_seed42/valid.jsonl`
- Test: `data/candidates/movielens-1m/variants/k5_popmatch_seed42/test.jsonl`

Validation metrics decide whether a larger exposure point is needed. Test metrics are report-only after the validation decision is fixed.

## Comparisons

### N-K0 vs M1

Match by N-task exposure.

- N-K0 at `X` exposure consumes `X` N examples.
- M1 at matched `X` consumes `X` N examples and `X` Y examples, total `2X`, because M1 uses 1:1 Y/N sampling.
- The main metric is the M1 N interface ranking result against N-K0 ranking result on the same validation candidate file.

### N-K0 vs SASRec

Match by processed N examples.

- Use exact or nearest SASRec exposure points from the batch-size-512 accounting table.
- Report mismatch percentage for every non-exact point.
- Do not interpolate unless explicitly requested later.
- Treat SASRec s1500 and s3000 as repeated-exposure anchors, not as matched N200 comparators.

## Reporting Fields

For each compared point, report:

- model/run label
- optimizer steps
- effective batch or batch size
- actual exposure
- exposure mismatch when applicable
- validation HR@1, NDCG@5, MRR
- test HR@1, NDCG@5, MRR as report-only
- checkpoint/eval artifact path
