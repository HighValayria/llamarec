# Missing Prediction Bundle: Machine A

- generated_utc: 2026-09-11T09:15:59Z
- hostname: ubuntu22
- machine: A
- seed: 42
- repository_head: a9c6cd959cf32afe046bb05be9eb5096bebfc5fb
- training_invoked: NO
- inference_invoked: NO
- evaluation_invoked: NO
- archive_bytes: 2975453
- archive_sha256: c5ebd07db05767726df47fe317f6ba51a1cf69a63d83f1dbca13d3944bc87dd8

## Source files

- outputs/n/movielens-1m/exposure_n_s6000/popmatch_eval/n_valid_predictions.jsonl | bytes=6274577 | rows=5675 | sha256=17939eb035919c8304cf02bbd31b1de3194b0e70e0b0136ae96f04dfc2f81dd6
- outputs/n/movielens-1m/exposure_n_s6000/popmatch_eval/n_test_predictions.jsonl | bytes=6240327 | rows=5675 | sha256=2571eb44757a98410a6b32f4dde6ab4121a4e4653eca7aa50d9cc39879addf96
- outputs/m/movielens-1m/exposure_m1_s12000/popmatch_eval_valid_only/m_n_valid_predictions.jsonl | bytes=6318411 | rows=5675 | sha256=f4e93f3d6ac735b8853ccabe83fd177682b35323255232f46c2e5f69d190f39a
- outputs/m/movielens-1m/exposure_m1_s12000/popmatch_eval/m_n_test_predictions.jsonl | bytes=6284311 | rows=5675 | sha256=4d815a424f557edfe1accaf8fa8463074c14d641807eb64372ef4618c5e718bf

## Archive parts

- predictions.tar.gz.part-00 | bytes=2975453 | sha256=c5ebd07db05767726df47fe317f6ba51a1cf69a63d83f1dbca13d3944bc87dd8

## Restore

```bash
cat predictions.tar.gz.part-* > predictions.tar.gz
sha256sum predictions.tar.gz
tar -tzf predictions.tar.gz
```
