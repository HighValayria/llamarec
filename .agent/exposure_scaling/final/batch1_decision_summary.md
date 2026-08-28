# Batch 1 Decision Summary

Validation-first decision after cloud eval:

- Stop Y-K0 scaling at 48k: Y 24k -> 48k does not improve NDCG@5 or MRR, and test metrics decline.
- Continue N-K0 to 96k: N 24k -> 48k improves validation HR@1 by 0.0255506608, NDCG@5 by 0.0132476807, and MRR by 0.0175359765.
- Keep test metrics report-only until validation decisions are fixed.

Generated next scripts:

- `.agent/exposure_scaling/commands/gpu_n96_train.sh`
- `.agent/exposure_scaling/commands/gpu_n96_train_nohup.sh`
- `.agent/exposure_scaling/commands/gpu_n96_eval.sh`
- `.agent/exposure_scaling/commands/gpu_n96_eval_nohup.sh`
