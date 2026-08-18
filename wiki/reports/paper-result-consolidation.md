---
title: "Paper Result Consolidation"
type: report
status: current
authority: descriptive
source: mixed
created: 2026-08-18
updated: 2026-08-18
last_verified: 2026-08-18
related_code:
  - .agent/paper_result_consolidation/claims.yaml
  - .agent/paper_result_consolidation/claim_evidence_matrix.csv
  - .agent/paper_result_consolidation/paper_ready_claims.json
  - .agent/paper_result_consolidation/paper_results_draft.md
  - .agent/paper_result_consolidation/limitations.md
  - .agent/paper_result_consolidation/tables/core_results.csv
  - .agent/paper_result_consolidation/tables/robustness_results.csv
  - .agent/paper_result_consolidation/tables/sample_efficiency_results.csv
  - .agent/paper_result_consolidation/tables/multiseed_results.csv
  - .agent/paper_result_consolidation/tables/popularity_analysis.csv
  - .agent/paper_result_consolidation/final/stage_summary.md
  - .agent/paper_result_consolidation/final/validated_findings.yaml
  - .agent/paper_result_consolidation/final/rejected_findings.yaml
  - .agent/paper_result_consolidation/final/open_questions.yaml
  - .agent/paper_result_consolidation/final/next_stage_recommendation.md
superseded_by: null
---

# Paper Result Consolidation

## Purpose

This report consolidates the completed MovieLens-1M evidence into a
paper-ready claim hierarchy, table plan, limitations, and next-stage
recommendation. It does not add new training or new evaluation results.

## Main Paper Claims

1. **Y-style preference supervision and N-style next-item supervision learn
   different recommendation semantics.** Y-K0 is strong on binary preference
   prediction, while N-K0 is much stronger on candidate-label next-item
   ranking. Y-K0's `P(Yes)` ranking should not be treated as equivalent to
   N-task ranking.
2. **N-K0 is the strongest completed LLM ranking setting, while M1 is the best
   unified Y/N tradeoff.** M1 retains near-Y-K0 binary ability and strong
   ranking, but it does not dominate N-K0.
3. **LLM-vs-SASRec conclusions are budget-regime dependent.** N-K0 is above
   SASRec at closest N-task sample-exposure points, while high-exposure SASRec
   is stronger under its much larger N-task exposure regime.
4. **Canonical Random-k5 must be supplemented with harder candidate controls.**
   PopMatch-k5, k20/k50 candidate-size stress tests, popularity baselines, and
   BPR-MF controls are required before making ranking claims.

## Evidence Strength

- Multi-seed stability is available for seeds 42/43/44.
- Y-K0 binary F1 is stable across three seeds, with range `0.0097766064`.
- N-K0 remains above M1 on PopMatch-k5 ranking across all three seeds; the
  minimum HR@1 margin is `0.0103964758`.
- N-K0 remains above roughly exposure-matched SASRec across all three seeds;
  the minimum HR@1 margin is `0.2766519824`.
- High-exposure SASRec s3000 remains above N-K0 across all three seeds; the
  minimum HR@1 margin is `0.0777092511`, but this remains a separate
  high-exposure budget regime.

## Claim Boundaries

- Do not write that M1 dominates N-K0. The supported claim is that M1 is a
  unified tradeoff and N-K0 is the ranking specialist.
- Do not write that LLM adapters beat SASRec overall. The supported claim is
  budget-conditioned: N-K0 is more sample efficient at closest N-task exposure,
  while high-exposure SASRec is stronger.
- Do not use Canonical Random-k5 alone to support recommender-quality claims.
- Do not promote the coldest target-popularity bucket into a main cold-start
  conclusion because the `<=10` bucket has only 26 samples.
- Do not describe the completed SASRec comparison as strict FLOP, wall-clock,
  capacity, or parameter matching.

## Paper Artifacts

The stage-local paper package is under `.agent/paper_result_consolidation/` and
contains:

- paper-ready claim JSON;
- claim-to-evidence matrix;
- protocol terminology;
- table schemas and CSVs;
- limitations;
- Results-section draft;
- validated and rejected finding registries;
- open questions;
- next-stage recommendation.

## Recommended Next Stage

Run a compact cross-dataset validation stage before claiming broad
generalization. The chosen second dataset is now Amazon Books, using the same
Y/N/M task-interface principles where feasible. The stage should first perform
a dataset feasibility audit before any GPU training.

If cross-dataset validation supports the main directions, the next major branch
is full paper writing and submission preparation. If only the Y/N separation is
stable, but sample-efficiency or SASRec positioning changes, the paper should
keep the task-interface contribution and downgrade model-positioning claims to
dataset-dependent findings.
