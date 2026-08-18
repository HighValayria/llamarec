# Paper Table Plan

## Table 1: Core Y/N/M Results

Purpose: show that Y and N supervision learn different recommendation
semantics and that M1 is a tradeoff.

Rows: Base, Y-K0, N-K0, M1.

Metrics: binary AUC, validation-calibrated F1, ranking HR@1, NDCG@5, MRR.

Required labels: binary interface, ranking interface, candidate protocol.

Data source: `wiki/reports/phase-2b-result-synthesis.md` plus Phase 2C
PopMatch rows where used.

## Table 2: Hard-Candidate / Robustness

Purpose: show that harder candidate protocols reveal limitations and that
candidate-size expansion matters more than order perturbation.

Rows: Base, N-K0, M1 across Canonical Random-k5, PopMatch-k5, k20, k50, and
selected order perturbation deltas.

Data source: Phase 2A and Phase 2C reports.

Constraint: do not present different candidate protocols as a single unlabeled
leaderboard.

## Table 3: SASRec Budget / Sample-Efficiency Positioning

Purpose: express complementary SASRec facts without contradiction.

Rows: N-K0 closest exposure, SASRec closest exposure, SASRec high-exposure, and
M1 supplemental where appropriate.

Metrics: N-task exposure, total exposure, optimizer steps, effective batch,
HR@1, NDCG@5, MRR, budget regime.

Data source: fair-budget and sample-efficiency reports.

## Table 4: Multi-seed Stability

Purpose: report mean +/- std and paired deltas across seeds 42/43/44.

Rows: Y-K0 binary, N-K0 ranking, M1 ranking, SASRec exp-match, SASRec
high-exposure.

Data source: `.agent/multiseed_stability/final/multiseed_aggregates.csv` and
`.agent/multiseed_stability/final/multiseed_comparisons.csv`.

## Analysis Table/Figure: Popularity Slice

Purpose: support the diagnostic statement that high-exposure SASRec advantage
is mainly middle/head driven.

Rows: target-popularity buckets.

Models: N-K0, M1, SASRec exp-match, SASRec high-exposure.

Boundary: `<=10` bucket has only 26 examples; do not upgrade to a main claim.
