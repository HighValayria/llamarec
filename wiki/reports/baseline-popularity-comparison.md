---
title: "Baseline Popularity Comparison"
type: report
status: current
authority: descriptive
source: mixed
created: 2026-08-09
updated: 2026-08-09
last_verified: 2026-08-09
related_code:
  - src/baselines/popularity.py
  - src/analysis/baseline_result_summary.py
  - src/analysis/baseline_llm_comparison.py
  - tests/test_popularity_baseline.py
  - tests/test_baseline_result_summary.py
  - tests/test_baseline_llm_comparison.py
---

# Baseline Popularity Comparison

## Scope

This report records the first traditional recommender baseline stage for
MovieLens-1M. It evaluates deterministic Popularity baselines under the same
fixed N candidate-file and ranking-metric contracts used by Base, N-K0, M1, and
Y-K0.

The stage does not train BPR/MF, SASRec, or new LLM adapters.

## Baselines

Two training-only popularity sources were evaluated:

- `n_train_targets`: counts targets from `next_item_train`.
- `preference_train_targets`: counts targets from `preference_train`, used as
  train-region interaction popularity.

Both baselines score each N candidate item by its training-only count. Ties use
the repository ranking metric behavior: stable candidate-order tie-breaking.

## Cloud Artifacts

Baseline plus LLM comparison:

```text
/root/llamarec/outputs/baselines/movielens-1m/llm_comparison/baseline_llm_comparison.md
```

Baseline summary:

```text
/root/llamarec/outputs/baselines/movielens-1m/summary/baseline_ranking_summary.md
```

## Baseline Metrics

| baseline | condition | HR@1 | NDCG@5 | MRR |
|---|---|---:|---:|---:|
| Popularity N-train | canonical k5 | 0.5663436123 | 0.8070103668 | 0.7417738620 |
| Popularity N-train | popmatch k5 | 0.3226431718 | 0.6635819590 | 0.5534860499 |
| Popularity preference-train | canonical k5 | 0.5295154185 | 0.7904400926 | 0.7196152717 |
| Popularity preference-train | popmatch k5 | 0.0918061674 | 0.5332976944 | 0.3819001468 |

The canonical-to-popmatch drop is large:

| comparison | delta_HR@1 | delta_NDCG@5 | delta_MRR |
|---|---:|---:|---:|
| N-train popmatch minus canonical | -0.2437004405 | -0.1434284078 | -0.1882878120 |
| preference-train popmatch minus canonical | -0.4377092511 | -0.2571423983 | -0.3377151248 |

## Popmatch LLM Comparison

Under the Phase 2C popularity-matched candidate set, LLM next-item models beat
Popularity baselines clearly.

| comparison | delta_HR@1 | delta_NDCG@5 | delta_MRR |
|---|---:|---:|---:|
| N-K0 minus Popularity N-train popmatch | 0.2220264317 | 0.1242154223 | 0.1635976505 |
| M1 minus Popularity N-train popmatch | 0.2017621145 | 0.1149189786 | 0.1511776799 |
| Base minus Popularity N-train popmatch | -0.0077533040 | 0.0000201202 | -0.0003494860 |
| N-K0 minus Popularity preference-train popmatch | 0.4528634361 | 0.2544996869 | 0.3351835536 |
| M1 minus Popularity preference-train popmatch | 0.4325991189 | 0.2452032433 | 0.3227635830 |
| Base minus Popularity preference-train popmatch | 0.2230837004 | 0.1303043849 | 0.1712364170 |

## Interpretation

Canonical random k5 candidates expose a strong popularity shortcut. Popularity
scores are high on canonical random candidates, but drop sharply when negatives
are popularity-matched to the target.

Popmatch k5 is therefore the fair comparison point for Phase 2C LLM results.
Under this condition, N-K0 and M1 are well above both Popularity definitions.
Base is roughly tied with N-train Popularity and above preference-train
Popularity.

This supports the Phase 2C interpretation: N-K0 remains the strongest next-item
ranking model, M1 remains close but below N-K0, and popularity alone does not
explain the popmatch N-K0/M1 ranking performance.

## Claim Boundaries

- Do not compare canonical Popularity rows against popmatch LLM rows as a
  like-for-like ranking claim.
- Do not claim that Popularity is a trained sequential recommender baseline.
- Do not treat this stage as evidence about BPR/MF or SASRec until those
  baselines are implemented under the same split/candidate/metric contract.
- Do not use Y-K0 ranking as next-interaction ranking evidence.

## Verification

Local targeted tests:

```text
C:/Users/33967/AppData/Local/Programs/Python/Python312/python.exe -m pytest tests/test_baseline_llm_comparison.py tests/test_baseline_result_summary.py tests/test_popularity_baseline.py tests/test_ranking_metrics.py tests/test_candidate_sets.py tests/test_analysis_outputs.py --basetemp .pytest_tmp_baseline
31 passed
```

Stage guard before wiki sync:

```text
C:/Users/33967/AppData/Local/Programs/Python/Python312/python.exe tools/stage_guard.py
0 error(s), 0 warning(s)
```
