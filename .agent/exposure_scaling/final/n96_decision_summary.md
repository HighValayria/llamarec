# N96 Decision Summary

Validation-first decision after N96 cloud eval:

- Stop Y-K0 scaling: Y 24k -> 48k does not improve NDCG@5 or MRR, and test metrics decline.
- Continue N-K0 from 96k to near-full-pool 200k: N 48k -> 96k improves validation HR@1 by 0.0207929515, NDCG@5 by 0.0102760040, and MRR by 0.0137004405.
- Keep test metrics report-only until validation decisions are fixed.

Generated next scripts:

- `.agent/exposure_scaling/commands/gpu_n200_train.sh`
- `.agent/exposure_scaling/commands/gpu_n200_eval.sh`
- `.agent/exposure_scaling/commands/gpu_n200_train_then_eval_nohup.sh`
- `.agent/exposure_scaling/commands/gpu_n200_progress.sh`
