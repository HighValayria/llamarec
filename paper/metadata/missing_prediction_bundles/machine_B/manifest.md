# Missing Prediction Bundle: Machine B

- generated_utc: 2026-09-11T09:16:30Z
- hostname: ubuntu22
- machine: B
- seed: 43
- repository_head: a9c6cd959cf32afe046bb05be9eb5096bebfc5fb
- training_invoked: NO
- inference_invoked: NO
- evaluation_invoked: NO
- archive_bytes: 30711830
- archive_sha256: 1bb428e8ad190ae3f9dc09fb95502331f56848b1f644afd419cfebaa9bf82f7d

## Source files

- outputs/n/movielens-1m/exposure_n_s12000_seed43/popmatch_eval/n_valid_predictions.jsonl | bytes=6320863 | rows=5675 | sha256=e3ab2e20e090a249cef1a752694dff80509c3eb86215ba87bb9b685c6d329c0c
- outputs/n/movielens-1m/exposure_n_s12000_seed43/popmatch_eval/n_test_predictions.jsonl | bytes=6286827 | rows=5675 | sha256=ed3048e8f3bcbbd4344e9129bd46d1fe7bd4f0cd05d6b458e67cca88290985cb
- outputs/m/movielens-1m/exposure_m1_s24000_seed43/popmatch_eval/m_n_valid_predictions.jsonl | bytes=6362850 | rows=5675 | sha256=5c4993c79cae1ada54f025d284212b006a8323bb4e0d27bd1609c7ce6d91f4f1
- outputs/m/movielens-1m/exposure_m1_s24000_seed43/popmatch_eval/m_n_test_predictions.jsonl | bytes=6328178 | rows=5675 | sha256=63b04b7d92b40ae10aa6834f2762b9189475e91a5220e356a8ebef61ce8948bb
- outputs/phase2a/multiseed96_ranking_robustness/seed43/n_k0_k20_seed42/n_valid_predictions.jsonl | bytes=10925118 | rows=5675 | sha256=3ba573d36ab786f5258803738ce89440b8fa343ceef804a829016ed53cd3042e
- outputs/phase2a/multiseed96_ranking_robustness/seed43/n_k0_k20_seed42/n_test_predictions.jsonl | bytes=10891490 | rows=5675 | sha256=1942b3e42c9a2fe0ca03e8a4668e0ac9cfc10a1abb779305b9b9054d27bb13a4
- outputs/phase2a/multiseed96_ranking_robustness/seed43/m1_k20_seed42/m_n_valid_predictions.jsonl | bytes=10996727 | rows=5675 | sha256=cd848bc1e81b30a37642c8f272bc18d303a195048ac807ae52ad6330eae7aca1
- outputs/phase2a/multiseed96_ranking_robustness/seed43/m1_k20_seed42/m_n_test_predictions.jsonl | bytes=10962857 | rows=5675 | sha256=1bb31f854db9d5d11f6101e5f3b5a4d6c71e3c8dbc83374ed1a4622452f7cae1
- outputs/phase2a/multiseed96_ranking_robustness/seed43/n_k0_k50_seed42/n_valid_predictions.jsonl | bytes=22173869 | rows=5675 | sha256=b74adbda18bdd7e2c25b8d34a1c2a463dd5e8b4ceb76e550ce88b4a151016463
- outputs/phase2a/multiseed96_ranking_robustness/seed43/n_k0_k50_seed42/n_test_predictions.jsonl | bytes=22142807 | rows=5675 | sha256=c09a276d6f0c348020e06588da4dd33b7b0cf0c9536ddfa70da8026988ef1df9
- outputs/phase2a/multiseed96_ranking_robustness/seed43/m1_k50_seed42/m_n_valid_predictions.jsonl | bytes=22258110 | rows=5675 | sha256=4b614a5240c25154b36879cd7aa9dfb31e76db4439197ce135ed5c53599ec547
- outputs/phase2a/multiseed96_ranking_robustness/seed43/m1_k50_seed42/m_n_test_predictions.jsonl | bytes=22223552 | rows=5675 | sha256=0c082288a842c78caab580fa0fb4ec71490df95f5765225e73971f2bf72909c3

## Archive parts

- predictions.tar.gz.part-00 | bytes=30711830 | sha256=1bb428e8ad190ae3f9dc09fb95502331f56848b1f644afd419cfebaa9bf82f7d

## Restore

```bash
cat predictions.tar.gz.part-* > predictions.tar.gz
sha256sum predictions.tar.gz
tar -tzf predictions.tar.gz
```
