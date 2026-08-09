---
title: "Phase 2A Ranking Robustness"
type: report
status: current
authority: descriptive
source: mixed
created: 2026-08-09
updated: 2026-08-09
last_verified: 2026-08-09
related_code:
  - src/eval/candidate_sets.py
  - src/eval/ranking_metrics.py
  - src/inference/base_zero_shot.py
  - src/inference/evaluate_n_adapter.py
  - src/inference/evaluate_m_adapter.py
  - src/inference/tokenization_check.py
  - src/analysis/grouped_error_analysis.py
  - src/analysis/phase2a_robustness_report.py
  - tests/test_candidate_sets.py
  - tests/test_ranking_metrics.py
  - tests/test_base_zero_shot_local.py
  - tests/test_n_m_adapter_evaluation.py
  - tests/test_analysis_outputs.py
---

# Phase 2A Ranking Robustness

## Scope

This report records Phase 2A ranking robustness on MovieLens-1M. It tests
whether the canonical 5-candidate ranking conclusions survive candidate-size
expansion and candidate-order perturbation.

Models in the main robustness matrix:

- Base
- N-K0
- M1 (`diag_m1_1m_m_200k_3000`)

Candidate variants:

- `k5_perm_seed43`
- `k20_seed42`
- `k20_perm_seed43`
- `k50_seed42`

Y-K0 was not part of the main explicit-variant matrix. Earlier diagnostics show
that Y-K0 ranking behaves like preference scoring rather than next-interaction
prediction.

## Protocol

Candidate variants were generated under explicit variant paths instead of
overwriting the canonical candidate files:

```text
data/candidates/movielens-1m/variants/{variant_name}/valid.jsonl
data/candidates/movielens-1m/variants/{variant_name}/test.jsonl
```

Each model evaluation used the same variant file through `--valid-candidates`
and `--test-candidates`. Outputs were written to:

```text
outputs/phase2a/ranking_robustness/{model}_{variant}
```

The final report was generated from explicit variant metric directories:

```text
outputs/phase2a/ranking_robustness/phase2a_ranking_robustness_report.md
```

Tokenizer smoke verified that k50 labels `A` through `AX` are single-token for
the configured Llama tokenizer. `use_sequence_likelihood_for` was empty, so k50
uses the same next-token logits scoring path as k5/k20.

## Test Metrics

| model | variant | HR@1 | HR@5 | HR@10 | HR@20 | HR@50 | NDCG@5 | MRR |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| Base | k5_perm_seed43 | 0.3217621145 | 1.0000000000 |  |  |  | 0.6654236813 | 0.5556710720 |
| Base | k20_seed42 | 0.0690748899 | 0.2928634361 | 0.5605286344 | 1.0000000000 |  | 0.1811710274 | 0.2088236555 |
| Base | k20_perm_seed43 | 0.0680176211 | 0.2925110132 | 0.5700440529 | 1.0000000000 |  | 0.1791652421 | 0.2072718710 |
| Base | k50_seed42 | 0.0292511013 | 0.1210572687 | 0.2445814978 | 0.4500440529 | 1.0000000000 | 0.0744893997 | 0.1057905143 |
| N-K0 | k5_perm_seed43 | 0.7150660793 | 1.0000000000 |  |  |  | 0.8756450438 | 0.8334302496 |
| N-K0 | k20_seed42 | 0.4163876652 | 0.7859030837 | 0.9101321586 | 1.0000000000 |  | 0.6157234085 | 0.5818276991 |
| N-K0 | k20_perm_seed43 | 0.4229074890 | 0.7948898678 | 0.9073127753 | 1.0000000000 |  | 0.6233681330 | 0.5879084187 |
| N-K0 | k50_seed42 | 0.1994713656 | 0.4387665198 | 0.5691629956 | 0.7365638767 | 1.0000000000 | 0.3250292649 | 0.3241909857 |
| M1 | k5_perm_seed43 | 0.6932158590 | 1.0000000000 |  |  |  | 0.8665986756 | 0.8212657856 |
| M1 | k20_seed42 | 0.3711013216 | 0.7022026432 | 0.8747136564 | 1.0000000000 |  | 0.5482297492 | 0.5285907582 |
| M1 | k20_perm_seed43 | 0.3758590308 | 0.7138325991 | 0.8761233480 | 1.0000000000 |  | 0.5574065896 | 0.5352182816 |
| M1 | k50_seed42 | 0.1219383260 | 0.3064317181 | 0.4969162996 | 0.7196475771 | 1.0000000000 | 0.2149517589 | 0.2346155309 |

## Main Findings

Order sensitivity is small. At k20, HR@1 changes are:

- Base: `-0.0010572687`
- N-K0: `+0.0065198238`
- M1: `+0.0047577093`

Candidate-size expansion is the dominant stressor:

- N-K0 HR@1 changes by `-0.2986784141` from k5 permutation to k20, then by
  `-0.2169162996` from k20 to k50.
- M1 HR@1 changes by `-0.3221145374` from k5 permutation to k20, then by
  `-0.2491629956` from k20 to k50.
- Base HR@1 also drops sharply, from `0.3217621145` on k5 permutation to
  `0.0690748899` on k20 and `0.0292511013` on k50.

N-K0 remains more robust than M1. N-K0 minus M1 HR@1 is:

- `+0.0218502203` on k5 permutation;
- `+0.0452863436` on k20;
- `+0.0470484581` on k20 permutation;
- `+0.0775330396` on k50.

Popularity remains a major robustness axis. On k20 test:

| popularity bucket | N-K0 HR@1 | M1 HR@1 |
|---|---:|---:|
| <=10 | 0.0769230769 | 0.0769230769 |
| 11-50 | 0.1105527638 | 0.0904522613 |
| 51-200 | 0.2412177986 | 0.2131147541 |
| 201-500 | 0.3219772879 | 0.3012692051 |
| >500 | 0.5327525008 | 0.4688609229 |

The cold-item weakness remains severe for both N-K0 and M1; N-K0's advantage is
clearest on mid-popularity and popular items.

## Interpretation

Phase 2A strengthens the current project interpretation: M1 is a useful
multi-task tradeoff, but it is not a replacement for the dedicated N-K0
next-item model. As candidate sets become larger, the N-K0 advantage over M1
becomes larger rather than smaller.

The canonical 5-candidate result is not merely an artifact of candidate order:
order permutations are stable. The larger issue is candidate-set size and the
model's ability to distinguish the true next interaction from a larger negative
pool, especially for cold or less popular target items.

## Follow-Up Options

Reasonable next work:

- optional Y-K0 explicit-variant run as a preference-ranking control;
- cold-item robustness analysis or targeted negative sampling work;
- paper/report writing around the multi-task tradeoff and candidate-size
  sensitivity.

Do not start M3, KAR, hard negatives, SASRec, 7B models, multi-seed experiments,
or MovieLens-32M full training without a separate scoped stage.
