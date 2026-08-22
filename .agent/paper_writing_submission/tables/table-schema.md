# Table Schema

## Table 1: Core Supervision Results

Purpose: show Y/N semantic split and M1 tradeoff across MovieLens-1M and
Amazon Musical Instruments.

Rows: Base, Y-K0, N-K0, M1.

Metrics: binary AUC/F1/Accuracy where valid; ranking HR@1/NDCG@5/MRR.

Data source: Phase 2B, Phase 2C, Cross-dataset Validation.

Rule: label Y ranking as `P(Yes)-based candidate scoring`.

## Table 2: Candidate Difficulty / Robustness

Purpose: distinguish Random-k5, PopMatch-k5, candidate-size expansion, and
order perturbation.

Rows: key MovieLens Random/PopMatch/k20/k50 and Amazon Random/PopMatch rows.

Metrics: HR@1/NDCG@5/MRR and candidate popularity gap where relevant.

Data source: Phase 2A, Phase 2C, Cross-dataset Validation.

## Table 3: Sample-exposure-aware SASRec Comparison

Purpose: present LLM-vs-SASRec without conflating budget regimes.

Rows: N-K0, M1 supplemental, SASRec closest exposure, SASRec high exposure.

Metrics: N-task exposure, total exposure, optimizer steps, effective batch,
HR@1/NDCG@5/MRR.

Data source: Fair-Budget Baseline Positioning, Sample-Efficiency Curve,
Multi-seed Stability, Cross-dataset Validation.

## Table 4: Stability / Generalization

Purpose: compactly report MovieLens multi-seed stability and Amazon seed42
directional validation.

Rows: Y-K0 binary, N-K0 ranking, M1 ranking, SASRec exp-match, SASRec high
exposure, Amazon seed42 PopMatch rows.

Metrics: MovieLens mean/std/min margin; Amazon seed42 deltas.

Data source: Multi-seed Stability and Cross-dataset Validation.
