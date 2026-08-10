---
title: "Baseline BPR-MF Comparison"
type: report
status: current
authority: descriptive
source: mixed
created: 2026-08-10
updated: 2026-08-10
last_verified: 2026-08-10
related_code:
  - src/baselines/bpr_mf.py
  - src/baselines/popularity.py
  - src/analysis/baseline_result_summary.py
  - src/analysis/baseline_llm_comparison.py
  - tests/test_bpr_mf_baseline.py
  - tests/test_popularity_baseline.py
  - tests/test_baseline_result_summary.py
  - tests/test_baseline_llm_comparison.py
---

# Baseline BPR-MF Comparison

## Scope

This report records the MovieLens-1M BPR-MF baseline stage. It evaluates a
trainable matrix-factorization recommender under the same fixed N candidate-file
and ranking-metric contracts used by Base, N-K0, M1, Y-K0, and the Popularity
baselines.

The stage does not train SASRec or new LLM adapters.

## Baseline

`src/baselines/bpr_mf.py` implements an in-repository PyTorch BPR-MF baseline.
It trains from `next_item_train` targets, samples negatives from the configured
item universe, and scores only the fixed candidate items supplied by the N
candidate files.

The formal MovieLens-1M cloud runs used:

| setting | value |
|---|---:|
| embedding_dim | 64 |
| epochs | 10 |
| batch_size | 4096 |
| learning_rate | 0.01 |
| seed | 42 |

## Cloud Artifacts

BPR-MF canonical output:

```text
/root/llamarec/outputs/baselines/movielens-1m/bpr_mf_canonical_k5
```

BPR-MF popmatch output:

```text
/root/llamarec/outputs/baselines/movielens-1m/bpr_mf_k5_popmatch_seed42
```

Baseline plus LLM comparison:

```text
/root/llamarec/outputs/baselines/movielens-1m/llm_comparison/baseline_llm_comparison.md
```

## BPR-MF Metrics

| condition | HR@1 | NDCG@5 | MRR | HR@5 | samples |
|---|---:|---:|---:|---:|---:|
| canonical k5 | 0.5610572687 | 0.8066675971 | 0.7411424376 | 1.0000000000 | 5675 |
| popmatch k5 | 0.3351541850 | 0.6757962567 | 0.5690719530 | 1.0000000000 | 5675 |

The canonical-to-popmatch drop is large:

| comparison | delta_HR@1 | delta_NDCG@5 | delta_MRR |
|---|---:|---:|---:|
| BPR-MF popmatch minus BPR-MF canonical | -0.2259030837 | -0.1308713403 | -0.1720704846 |

## Popmatch LLM Comparison

Under the Phase 2C popularity-matched candidate set, N-K0 and M1 remain clearly
above BPR-MF.

| comparison | delta_HR@1 | delta_NDCG@5 | delta_MRR |
|---|---:|---:|---:|
| N-K0 minus BPR-MF popmatch | 0.2095154185 | 0.1120011246 | 0.1480117474 |
| M1 minus BPR-MF popmatch | 0.1892511013 | 0.1027046809 | 0.1355917768 |
| Base minus BPR-MF popmatch | -0.0202643172 | -0.0121941775 | -0.0159353891 |
| Y-K0 minus BPR-MF popmatch | -0.1497797357 | -0.0956224990 | -0.1247900147 |

## Interpretation

BPR-MF is the strongest non-LLM popmatch baseline evaluated so far. It slightly
exceeds N-train Popularity under popmatch k5, but remains far below N-K0 and
M1 on next-item ranking.

The canonical BPR-MF row is strong and close to canonical Popularity, which
reinforces the Phase 2C finding that random canonical candidates expose a
popularity-related shortcut. Popmatch k5 remains the fair comparison condition
for Phase 2C LLM ranking claims.

The current baseline evidence supports this boundary: popularity and basic
matrix factorization do not explain the N-K0/M1 popmatch ranking advantage.

## Claim Boundaries

- Do not compare canonical BPR-MF rows against popmatch LLM rows as a
  like-for-like ranking claim.
- Do not claim this stage evaluates sequence models; SASRec remains untested.
- Do not use Y-K0 ranking as next-interaction ranking evidence.
- Do not treat this single seed as a multi-seed stability result.

## Verification

Local targeted tests:

```text
C:/Users/33967/AppData/Local/Programs/Python/Python312/python.exe -m pytest tests/test_baseline_result_summary.py tests/test_baseline_llm_comparison.py tests/test_bpr_mf_baseline.py tests/test_popularity_baseline.py tests/test_ranking_metrics.py tests/test_candidate_sets.py --basetemp .pytest_tmp_bpr_mf
19 passed
```

Stage guard before wiki sync:

```text
C:/Users/33967/AppData/Local/Programs/Python/Python312/python.exe tools/stage_guard.py
0 error(s), 0 warning(s)
```
