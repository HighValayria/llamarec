# Missing Prediction Bundle: Machine C

- generated_utc: 2026-09-11T09:16:17Z
- hostname: ubuntu22
- machine: C
- seed: 44
- repository_head: a1fa349141b8ea6060de9f44f89e93d60c277f8d
- training_invoked: NO
- inference_invoked: NO
- evaluation_invoked: NO
- archive_bytes: 30890258
- archive_sha256: 4d452b2d43017a20ffb189d733ad8cd3373682a1bfafa95bf8273afbb498b292

## Source files

- outputs/n/movielens-1m/exposure_n_s12000_seed44/popmatch_eval/n_valid_predictions.jsonl | bytes=6322067 | rows=5675 | sha256=84fb2647cefb9e061ed0f0b15e9ed3e535dcd0d43a15a9ef968e080ae0ddf16d
- outputs/n/movielens-1m/exposure_n_s12000_seed44/popmatch_eval/n_test_predictions.jsonl | bytes=6287449 | rows=5675 | sha256=d9bc5f5850037c77e0ebb674085ea573a1d3557db55fddbbffd5972fe1121273
- outputs/m/movielens-1m/exposure_m1_s24000_seed44/popmatch_eval/m_n_valid_predictions.jsonl | bytes=6361770 | rows=5675 | sha256=317ad0aab3d3906bc6365f16cabddab5490cfb65bb5e89ec005a3cd3ef772074
- outputs/m/movielens-1m/exposure_m1_s24000_seed44/popmatch_eval/m_n_test_predictions.jsonl | bytes=6327614 | rows=5675 | sha256=5bedc31b9c19197c1a3baf4ee84889de01ce31eb3cb801c4195617ed468189c5
- outputs/phase2a/multiseed96_ranking_robustness/seed44/n_k0_k20_seed42/n_valid_predictions.jsonl | bytes=10936372 | rows=5675 | sha256=284a6683422f1adb3c6408cd87db4c8be8d1715ebb8c9fc25135271910e7fc81
- outputs/phase2a/multiseed96_ranking_robustness/seed44/n_k0_k20_seed42/n_test_predictions.jsonl | bytes=10901724 | rows=5675 | sha256=8c52e0342d0fb50d222be1feef0055b2059c5642f8b03d8a41699acd310202e5
- outputs/phase2a/multiseed96_ranking_robustness/seed44/m1_k20_seed42/m_n_valid_predictions.jsonl | bytes=10996287 | rows=5675 | sha256=00a2882489d37c2ca3aab433e32bf216e63a33aecc794ff47396135db5d2a97e
- outputs/phase2a/multiseed96_ranking_robustness/seed44/m1_k20_seed42/m_n_test_predictions.jsonl | bytes=10962381 | rows=5675 | sha256=555ed7c368746b46abbbc1eb27764e50e4a98896c0c865d061b146f831db4e5f
- outputs/phase2a/multiseed96_ranking_robustness/seed44/n_k0_k50_seed42/n_valid_predictions.jsonl | bytes=22189025 | rows=5675 | sha256=1eb440114dd6640eb2d6287e1dd60c67a958eceeb643fedd3e0e1751ca0aa07a
- outputs/phase2a/multiseed96_ranking_robustness/seed44/n_k0_k50_seed42/n_test_predictions.jsonl | bytes=22153635 | rows=5675 | sha256=77c540bf27bfc0dd3f00f259082321b354b105d05eef50e3b17664581568de26
- outputs/phase2a/multiseed96_ranking_robustness/seed44/m1_k50_seed42/m_n_valid_predictions.jsonl | bytes=22251140 | rows=5675 | sha256=186e1390d60ee9d49846bafc5ba834a19fe03ee2ad6f57f93cea69726a2c9a33
- outputs/phase2a/multiseed96_ranking_robustness/seed44/m1_k50_seed42/m_n_test_predictions.jsonl | bytes=22218036 | rows=5675 | sha256=74ecea2df70581170302b3e7421ed4ddec657006f701a5132994205fe6186ddf

## Archive parts

- predictions.tar.gz.part-00 | bytes=30890258 | sha256=4d452b2d43017a20ffb189d733ad8cd3373682a1bfafa95bf8273afbb498b292

## Restore

```bash
cat predictions.tar.gz.part-* > predictions.tar.gz
sha256sum predictions.tar.gz
tar -tzf predictions.tar.gz
```
