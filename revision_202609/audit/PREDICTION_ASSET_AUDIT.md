# Prediction Asset Audit

Scope: N96 and M1-N96; seeds 42, 43, 44; protocols k5, k20, k50; validation and test splits.

No model training, model inference, model download, candidate regeneration, or frozen paper evidence modification was performed.

## Completeness Summary

- Exact feasible N96 vs M1-N96 pairs: 12 of 18 expected seed/protocol/split combinations.
- Feasible pairs are seed43 and seed44 for k5, k20, and k50 on validation and test.
- Seed42 N96/M1-N96 prediction-level files were not recovered; frozen aggregate metrics exist but were not used for bootstrap.
- Existing machine_A files are lower-exposure paths and were not treated as N96/M1-N96 assets.

## Pairing Rule

Pairing was verified by explicit `(split, user_id, ground_truth_movie_id)` identity, equal candidate item order, equal ground-truth index, equal row count, and absence of duplicate query identities. Raw row position was not used until identity equality was proven.

## Files

- N96 seed42 k5 validation: NO - missing N96/M1-N96 prediction-level asset
- N96 seed42 k5 test: NO - missing N96/M1-N96 prediction-level asset
- N96 seed42 k20 validation: NO - missing N96/M1-N96 prediction-level asset
- N96 seed42 k20 test: NO - missing N96/M1-N96 prediction-level asset
- N96 seed42 k50 validation: NO - missing N96/M1-N96 prediction-level asset
- N96 seed42 k50 test: NO - missing N96/M1-N96 prediction-level asset
- N96 seed43 k5 validation: YES - exact N96 vs M1-N96 pair verified
  - path: `.agent/missing_prediction_bundles_imported/machine_B/payload/outputs/n/movielens-1m/exposure_n_s12000_seed43/popmatch_eval/n_valid_predictions.jsonl`
  - rows: 5675; sha256: `e3ab2e20e090a249cef1a752694dff80509c3eb86215ba87bb9b685c6d329c0c`
  - fields: user_id=YES, query_identity=YES, candidates=YES, target=YES, scores=YES, final_rank_persisted=NO, final_rank_computable=YES
- N96 seed43 k5 test: YES - exact N96 vs M1-N96 pair verified
  - path: `.agent/missing_prediction_bundles_imported/machine_B/payload/outputs/n/movielens-1m/exposure_n_s12000_seed43/popmatch_eval/n_test_predictions.jsonl`
  - rows: 5675; sha256: `ed3048e8f3bcbbd4344e9129bd46d1fe7bd4f0cd05d6b458e67cca88290985cb`
  - fields: user_id=YES, query_identity=YES, candidates=YES, target=YES, scores=YES, final_rank_persisted=NO, final_rank_computable=YES
- N96 seed43 k20 validation: YES - exact N96 vs M1-N96 pair verified
  - path: `.agent/missing_prediction_bundles_imported/machine_B/payload/outputs/phase2a/multiseed96_ranking_robustness/seed43/n_k0_k20_seed42/n_valid_predictions.jsonl`
  - rows: 5675; sha256: `3ba573d36ab786f5258803738ce89440b8fa343ceef804a829016ed53cd3042e`
  - fields: user_id=YES, query_identity=YES, candidates=YES, target=YES, scores=YES, final_rank_persisted=NO, final_rank_computable=YES
- N96 seed43 k20 test: YES - exact N96 vs M1-N96 pair verified
  - path: `.agent/missing_prediction_bundles_imported/machine_B/payload/outputs/phase2a/multiseed96_ranking_robustness/seed43/n_k0_k20_seed42/n_test_predictions.jsonl`
  - rows: 5675; sha256: `1942b3e42c9a2fe0ca03e8a4668e0ac9cfc10a1abb779305b9b9054d27bb13a4`
  - fields: user_id=YES, query_identity=YES, candidates=YES, target=YES, scores=YES, final_rank_persisted=NO, final_rank_computable=YES
- N96 seed43 k50 validation: YES - exact N96 vs M1-N96 pair verified
  - path: `.agent/missing_prediction_bundles_imported/machine_B/payload/outputs/phase2a/multiseed96_ranking_robustness/seed43/n_k0_k50_seed42/n_valid_predictions.jsonl`
  - rows: 5675; sha256: `b74adbda18bdd7e2c25b8d34a1c2a463dd5e8b4ceb76e550ce88b4a151016463`
  - fields: user_id=YES, query_identity=YES, candidates=YES, target=YES, scores=YES, final_rank_persisted=NO, final_rank_computable=YES
- N96 seed43 k50 test: YES - exact N96 vs M1-N96 pair verified
  - path: `.agent/missing_prediction_bundles_imported/machine_B/payload/outputs/phase2a/multiseed96_ranking_robustness/seed43/n_k0_k50_seed42/n_test_predictions.jsonl`
  - rows: 5675; sha256: `c09a276d6f0c348020e06588da4dd33b7b0cf0c9536ddfa70da8026988ef1df9`
  - fields: user_id=YES, query_identity=YES, candidates=YES, target=YES, scores=YES, final_rank_persisted=NO, final_rank_computable=YES
- N96 seed44 k5 validation: YES - exact N96 vs M1-N96 pair verified
  - path: `.agent/missing_prediction_bundles_imported/machine_C/payload/outputs/n/movielens-1m/exposure_n_s12000_seed44/popmatch_eval/n_valid_predictions.jsonl`
  - rows: 5675; sha256: `84fb2647cefb9e061ed0f0b15e9ed3e535dcd0d43a15a9ef968e080ae0ddf16d`
  - fields: user_id=YES, query_identity=YES, candidates=YES, target=YES, scores=YES, final_rank_persisted=NO, final_rank_computable=YES
- N96 seed44 k5 test: YES - exact N96 vs M1-N96 pair verified
  - path: `.agent/missing_prediction_bundles_imported/machine_C/payload/outputs/n/movielens-1m/exposure_n_s12000_seed44/popmatch_eval/n_test_predictions.jsonl`
  - rows: 5675; sha256: `d9bc5f5850037c77e0ebb674085ea573a1d3557db55fddbbffd5972fe1121273`
  - fields: user_id=YES, query_identity=YES, candidates=YES, target=YES, scores=YES, final_rank_persisted=NO, final_rank_computable=YES
- N96 seed44 k20 validation: YES - exact N96 vs M1-N96 pair verified
  - path: `.agent/missing_prediction_bundles_imported/machine_C/payload/outputs/phase2a/multiseed96_ranking_robustness/seed44/n_k0_k20_seed42/n_valid_predictions.jsonl`
  - rows: 5675; sha256: `284a6683422f1adb3c6408cd87db4c8be8d1715ebb8c9fc25135271910e7fc81`
  - fields: user_id=YES, query_identity=YES, candidates=YES, target=YES, scores=YES, final_rank_persisted=NO, final_rank_computable=YES
- N96 seed44 k20 test: YES - exact N96 vs M1-N96 pair verified
  - path: `.agent/missing_prediction_bundles_imported/machine_C/payload/outputs/phase2a/multiseed96_ranking_robustness/seed44/n_k0_k20_seed42/n_test_predictions.jsonl`
  - rows: 5675; sha256: `8c52e0342d0fb50d222be1feef0055b2059c5642f8b03d8a41699acd310202e5`
  - fields: user_id=YES, query_identity=YES, candidates=YES, target=YES, scores=YES, final_rank_persisted=NO, final_rank_computable=YES
- N96 seed44 k50 validation: YES - exact N96 vs M1-N96 pair verified
  - path: `.agent/missing_prediction_bundles_imported/machine_C/payload/outputs/phase2a/multiseed96_ranking_robustness/seed44/n_k0_k50_seed42/n_valid_predictions.jsonl`
  - rows: 5675; sha256: `1eb440114dd6640eb2d6287e1dd60c67a958eceeb643fedd3e0e1751ca0aa07a`
  - fields: user_id=YES, query_identity=YES, candidates=YES, target=YES, scores=YES, final_rank_persisted=NO, final_rank_computable=YES
- N96 seed44 k50 test: YES - exact N96 vs M1-N96 pair verified
  - path: `.agent/missing_prediction_bundles_imported/machine_C/payload/outputs/phase2a/multiseed96_ranking_robustness/seed44/n_k0_k50_seed42/n_test_predictions.jsonl`
  - rows: 5675; sha256: `77c540bf27bfc0dd3f00f259082321b354b105d05eef50e3b17664581568de26`
  - fields: user_id=YES, query_identity=YES, candidates=YES, target=YES, scores=YES, final_rank_persisted=NO, final_rank_computable=YES
- M1-N96 seed42 k5 validation: NO - missing N96/M1-N96 prediction-level asset
- M1-N96 seed42 k5 test: NO - missing N96/M1-N96 prediction-level asset
- M1-N96 seed42 k20 validation: NO - missing N96/M1-N96 prediction-level asset
- M1-N96 seed42 k20 test: NO - missing N96/M1-N96 prediction-level asset
- M1-N96 seed42 k50 validation: NO - missing N96/M1-N96 prediction-level asset
- M1-N96 seed42 k50 test: NO - missing N96/M1-N96 prediction-level asset
- M1-N96 seed43 k5 validation: YES - exact N96 vs M1-N96 pair verified
  - path: `.agent/missing_prediction_bundles_imported/machine_B/payload/outputs/m/movielens-1m/exposure_m1_s24000_seed43/popmatch_eval/m_n_valid_predictions.jsonl`
  - rows: 5675; sha256: `5c4993c79cae1ada54f025d284212b006a8323bb4e0d27bd1609c7ce6d91f4f1`
  - fields: user_id=YES, query_identity=YES, candidates=YES, target=YES, scores=YES, final_rank_persisted=NO, final_rank_computable=YES
- M1-N96 seed43 k5 test: YES - exact N96 vs M1-N96 pair verified
  - path: `.agent/missing_prediction_bundles_imported/machine_B/payload/outputs/m/movielens-1m/exposure_m1_s24000_seed43/popmatch_eval/m_n_test_predictions.jsonl`
  - rows: 5675; sha256: `63b04b7d92b40ae10aa6834f2762b9189475e91a5220e356a8ebef61ce8948bb`
  - fields: user_id=YES, query_identity=YES, candidates=YES, target=YES, scores=YES, final_rank_persisted=NO, final_rank_computable=YES
- M1-N96 seed43 k20 validation: YES - exact N96 vs M1-N96 pair verified
  - path: `.agent/missing_prediction_bundles_imported/machine_B/payload/outputs/phase2a/multiseed96_ranking_robustness/seed43/m1_k20_seed42/m_n_valid_predictions.jsonl`
  - rows: 5675; sha256: `cd848bc1e81b30a37642c8f272bc18d303a195048ac807ae52ad6330eae7aca1`
  - fields: user_id=YES, query_identity=YES, candidates=YES, target=YES, scores=YES, final_rank_persisted=NO, final_rank_computable=YES
- M1-N96 seed43 k20 test: YES - exact N96 vs M1-N96 pair verified
  - path: `.agent/missing_prediction_bundles_imported/machine_B/payload/outputs/phase2a/multiseed96_ranking_robustness/seed43/m1_k20_seed42/m_n_test_predictions.jsonl`
  - rows: 5675; sha256: `1bb31f854db9d5d11f6101e5f3b5a4d6c71e3c8dbc83374ed1a4622452f7cae1`
  - fields: user_id=YES, query_identity=YES, candidates=YES, target=YES, scores=YES, final_rank_persisted=NO, final_rank_computable=YES
- M1-N96 seed43 k50 validation: YES - exact N96 vs M1-N96 pair verified
  - path: `.agent/missing_prediction_bundles_imported/machine_B/payload/outputs/phase2a/multiseed96_ranking_robustness/seed43/m1_k50_seed42/m_n_valid_predictions.jsonl`
  - rows: 5675; sha256: `4b614a5240c25154b36879cd7aa9dfb31e76db4439197ce135ed5c53599ec547`
  - fields: user_id=YES, query_identity=YES, candidates=YES, target=YES, scores=YES, final_rank_persisted=NO, final_rank_computable=YES
- M1-N96 seed43 k50 test: YES - exact N96 vs M1-N96 pair verified
  - path: `.agent/missing_prediction_bundles_imported/machine_B/payload/outputs/phase2a/multiseed96_ranking_robustness/seed43/m1_k50_seed42/m_n_test_predictions.jsonl`
  - rows: 5675; sha256: `0c082288a842c78caab580fa0fb4ec71490df95f5765225e73971f2bf72909c3`
  - fields: user_id=YES, query_identity=YES, candidates=YES, target=YES, scores=YES, final_rank_persisted=NO, final_rank_computable=YES
- M1-N96 seed44 k5 validation: YES - exact N96 vs M1-N96 pair verified
  - path: `.agent/missing_prediction_bundles_imported/machine_C/payload/outputs/m/movielens-1m/exposure_m1_s24000_seed44/popmatch_eval/m_n_valid_predictions.jsonl`
  - rows: 5675; sha256: `317ad0aab3d3906bc6365f16cabddab5490cfb65bb5e89ec005a3cd3ef772074`
  - fields: user_id=YES, query_identity=YES, candidates=YES, target=YES, scores=YES, final_rank_persisted=NO, final_rank_computable=YES
- M1-N96 seed44 k5 test: YES - exact N96 vs M1-N96 pair verified
  - path: `.agent/missing_prediction_bundles_imported/machine_C/payload/outputs/m/movielens-1m/exposure_m1_s24000_seed44/popmatch_eval/m_n_test_predictions.jsonl`
  - rows: 5675; sha256: `5bedc31b9c19197c1a3baf4ee84889de01ce31eb3cb801c4195617ed468189c5`
  - fields: user_id=YES, query_identity=YES, candidates=YES, target=YES, scores=YES, final_rank_persisted=NO, final_rank_computable=YES
- M1-N96 seed44 k20 validation: YES - exact N96 vs M1-N96 pair verified
  - path: `.agent/missing_prediction_bundles_imported/machine_C/payload/outputs/phase2a/multiseed96_ranking_robustness/seed44/m1_k20_seed42/m_n_valid_predictions.jsonl`
  - rows: 5675; sha256: `00a2882489d37c2ca3aab433e32bf216e63a33aecc794ff47396135db5d2a97e`
  - fields: user_id=YES, query_identity=YES, candidates=YES, target=YES, scores=YES, final_rank_persisted=NO, final_rank_computable=YES
- M1-N96 seed44 k20 test: YES - exact N96 vs M1-N96 pair verified
  - path: `.agent/missing_prediction_bundles_imported/machine_C/payload/outputs/phase2a/multiseed96_ranking_robustness/seed44/m1_k20_seed42/m_n_test_predictions.jsonl`
  - rows: 5675; sha256: `555ed7c368746b46abbbc1eb27764e50e4a98896c0c865d061b146f831db4e5f`
  - fields: user_id=YES, query_identity=YES, candidates=YES, target=YES, scores=YES, final_rank_persisted=NO, final_rank_computable=YES
- M1-N96 seed44 k50 validation: YES - exact N96 vs M1-N96 pair verified
  - path: `.agent/missing_prediction_bundles_imported/machine_C/payload/outputs/phase2a/multiseed96_ranking_robustness/seed44/m1_k50_seed42/m_n_valid_predictions.jsonl`
  - rows: 5675; sha256: `186e1390d60ee9d49846bafc5ba834a19fe03ee2ad6f57f93cea69726a2c9a33`
  - fields: user_id=YES, query_identity=YES, candidates=YES, target=YES, scores=YES, final_rank_persisted=NO, final_rank_computable=YES
- M1-N96 seed44 k50 test: YES - exact N96 vs M1-N96 pair verified
  - path: `.agent/missing_prediction_bundles_imported/machine_C/payload/outputs/phase2a/multiseed96_ranking_robustness/seed44/m1_k50_seed42/m_n_test_predictions.jsonl`
  - rows: 5675; sha256: `74ecea2df70581170302b3e7421ed4ddec657006f701a5132994205fe6186ddf`
  - fields: user_id=YES, query_identity=YES, candidates=YES, target=YES, scores=YES, final_rank_persisted=NO, final_rank_computable=YES

See `prediction_asset_matrix.csv` and `pairing_checks.csv`.
