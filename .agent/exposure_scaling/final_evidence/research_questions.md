# Research Questions

## RQ1: Supervision Semantics

Do preference prediction and next-interaction prediction induce different recommendation capabilities?

Core evidence: Y-native binary metrics, Y-as-ranker bridge metrics, and N-native ranking metrics.

## RQ2: Exposure Response

How do task-specific capabilities scale with supervision exposure?

Core evidence: Y24/Y48/Y96 native binary trajectory and N24/N48/N96/N200 native ranking trajectory.

## RQ3: Multi-task Unification

How does multi-task tuning affect specialized capabilities under matched per-task exposure?

Core evidence: Y96 vs M1-96-Y binary bootstrap and N96 vs M1-96-N k5 bootstrap.

## RQ4: Ranking Robustness

Does the apparent N/M relationship persist under harder candidate protocols?

Core evidence: k5, k20, and k50 comparisons with the explicit caveat that candidate protocols are not nested.

## RQ5: Exposure-aware Baseline Comparison

How does N-K0 compare with a specialized sequential recommender under approximately matched training-sample exposure?

Core evidence: N-K0 vs SASRec matched points at approximately 24k, 48k, 96k, and 200k.
