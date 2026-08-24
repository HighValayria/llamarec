# LLM Exposure Scaling & Convergence Validation - Stage Context

## Stage Goal

Answer whether current MovieLens-1M LLM checkpoints are undertrained, whether Y/N/M supervision-semantics claims survive larger task-sample exposure, and how N-K0 compares with SASRec over a clearer performance-vs-exposure frontier.

Paper Writing / Submission Package remains paused, not completed, while this evidence gap is resolved.

## Frozen Terminology

- Primary x-axis: task-sample exposure.
- Definition: task training examples actually consumed by optimization.
- Not equivalent to unique examples, raw interactions, tokens, FLOPs, or wall-clock compute.
- Paper wording should use "supervision-exposure scaling" or "task-sample-exposure scaling", not "compute scaling".

## One-Time Wiki Context Read

Read once on 2026-08-24, then revoked: `wiki/index.md`, `wiki/current_state.md`, `wiki/reports/fair-budget-baseline-positioning.md`, `wiki/reports/sample-efficiency-training-efficiency.md`, `wiki/reports/multiseed-stability.md`, and `wiki/reports/paper-result-consolidation.md`.

No further direct wiki access is allowed inside the stage without renewed user authorization.

## Durable Prior Findings Compressed

- Y-K0 is the dedicated binary preference model; its P(Yes)-based candidate ranking is weaker and should not be treated as next-item ranking.
- N-K0 is the strongest completed LLM ranking specialist on MovieLens-1M PopMatch-k5.
- M1 is the best current unified Y/N tradeoff but remains below N-K0 for ranking across seeds 42/43/44.
- N-K0 beats roughly exposure-matched SASRec in existing closest-exposure rows, while much higher exposure SASRec beats current low-exposure N-K0.
- High-exposure SASRec evidence is not a high-exposure LLM-vs-SASRec head-to-head because high-exposure LLM points do not yet exist.
- Existing sample-efficiency curve already contains N-K0 at 3k, 6k, 12k, and 24k N-task exposure, plus SASRec closest and high-exposure anchors.

## Code/Config Facts

- Formal dataset key: `movielens-1m`.
- Fixed hard-candidate protocol: `data/candidates/movielens-1m/variants/k5_popmatch_seed42/{valid,test}.jsonl`.
- LLM scripts use Hugging Face Trainer with `per_device_train_batch_size=1`, `gradient_accumulation_steps=8` in formal audited rows.
- Y/N single-task effective exposure per optimizer step is 8 samples under single-process training.
- M1 constructs a 1:1 interleaved dataset and uses `SequentialSampler`; each optimizer step consumes 4 Y and 4 N samples at batch 1, grad accumulation 8.
- SASRec uses batch 512, no gradient accumulation, shuffled no-replacement passes over the loaded pool, and accounts for the short final batch.
- TrainingArguments do not explicitly set `lr_scheduler_type`; the default scheduler should be treated as total-step-dependent unless the cloud environment proves otherwise.

## Data Pools

- MovieLens-1M Y train available: 976,284 samples.
- MovieLens-1M N train available: 212,725 samples.
- Formal capped pools for audited runs: 200,000 per task.
- PopMatch-k5 fixed test cohort: 5,675 N test candidates.
