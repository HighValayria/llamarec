# Exposure Scaling Summary

First audit round completed without GPU jobs.

## Key Answers So Far

1. Current Y-K0 exposure is 12,000 Y-task samples.
2. Current N-K0 exposure is 12,000 N-task samples.
3. Current M1 exposure is 12,000 Y + 12,000 N, 24,000 total.
4. MovieLens-1M train pools are 976,284 Y and 212,725 N; audited formal caps are 200,000 per task.
5. Current Y-K0/N-K0 cover 6% of their loaded 200k cap; M1 covers 6% per task.
6. Current 12k LLM anchors should have no sample repetition under the audited single-process first-pass assumptions.
7. Cloud inventory and `training_args.bin` readback now confirm resume state exists and the effective exposure step size is 8 task samples.
8. Existing N-K0 24k and SASRec 24k-aligned points should be reused.

## First GPU Batch Recommendation

After explicit GPU approval:

- Do not repeat N 24k.
- Resume Y-K0 to 24k and 48k.
- Resume N-K0 to 48k, preferably from existing N 24k if the cloud checkpoint is present.
- Generate validation PopMatch metrics for existing and new points.

This is more efficient than blindly launching N 24k again.
