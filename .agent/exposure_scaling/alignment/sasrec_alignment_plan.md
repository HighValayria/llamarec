# SASRec Alignment Plan

Date: 2026-08-30

## Accounting

SASRec uses one optimizer update per batch, with no gradient accumulation in `src/baselines/sasrec.py`. The aligned historical baseline uses batch size 512 and `max_train_samples=200000`.

For `train_examples=200000`, `batch_size=512`:

- 390 full batches of 512 and one final batch of 320 per full pass.
- 391 optimizer steps process exactly 200000 examples.
- Before step 391, exposure is approximately `steps * 512`.

## Matched Grid

| target N exposure | SASRec point | actual SASRec exposure | mismatch | status |
|---:|---|---:|---:|---|
| 12000 | s23 | 11776 | -1.8667% | train/eval fresh alignment run |
| 24000 | s47 | 24064 | +0.2667% | train/eval fresh alignment run |
| 48000 | s94 | 48128 | +0.2667% | train/eval if not already present on cloud |
| 96000 | s188 | 96256 | +0.2667% | train/eval if not already present on cloud |
| 200000 | s391 | 200000 | 0.0000% | train/eval if not already present on cloud |

## High-Exposure Anchors

`sasrec_s1500` and `sasrec_s3000` are not matched to N200.

- s1500 processed 767424 examples: 200000 unique + 567424 repeated.
- s3000 processed 1534656 examples: 200000 unique + 1334656 repeated.

They answer a different question: what happens after many repeated passes over the SASRec pool. They are useful as high-exposure anchors but should not be used as the matched-exposure comparator for N200.

## Recommendation

First SASRec experiment:

1. Inventory cloud model directories and existing eval outputs.
2. Train/evaluate fresh s23, s47, s94, s188, and s391 alignment runs so current PopMatch candidates are included in the SASRec item mapping.
3. Keep existing s1500/s3000 PopMatch eval outputs only as repeated-exposure anchors.
4. Stop and compare validation-first against N24/N48/N96/N200.

SASRec should run before new M1 LLM training because it is comparatively cheap and immediately clarifies whether N-K0's scaling advantage is LLM-specific or just an exposure artifact.
