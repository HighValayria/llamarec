# Current Task

## Stage Goal
- Continue the active Cross-dataset Validation stage, rerouted on 2026-08-19
  from the rejected Amazon-books catalog to user-provided local Amazon Reviews
  2023 5-core Musical_Instruments.
- Integrate Amazon Musical Instruments through a dataset adapter, reuse the
  strict temporal Y/N pipeline, build fixed Random-k5 and PopMatch-k5
  candidates, then proceed to seed42 GPU experiments only after user approval.

## Scope
- Active dataset: `amazon-musical-instruments`.
- Rejected prior source: `Amazon-books` catalog as interaction source.
- Local raw files:
  - `data/raw/amazon_reviews_2023/musical_instruments/interactions/Musical_Instruments.csv`
  - `data/raw/amazon_reviews_2023/musical_instruments/metadata/full-00000-of-00002.parquet`
  - `data/raw/amazon_reviews_2023/musical_instruments/metadata/full-00001-of-00002.parquet`
- Stage-local artifacts under `.agent/cross_dataset_validation/`.
- Formal CPU/data/candidate gate is complete.

## Non-Goals
- No seed43/44 until seed42 synthesis is reviewed.
- No web search, dataset download, Hugging Face dataset loading, wget/curl, git
  clone, or replacement with non-local data.
- No KAR, review-text augmentation, description augmentation, hard-negative
  training, new M variant, LoRA sweep, 7B, third dataset, or strict FLOPs match.
- Do not write formal wiki during this stage until stage-end authorization.

## Long-Term Constraints
- Continue the current Cross-dataset Validation stage; do not create a new
  stage.
- Do not read formal wiki again. Stage opening wiki read was already completed
  and revoked on 2026-08-18.
- Use only local user-provided data.
- Amazon input information is limited to interaction `user_id`, `parent_asin`,
  `rating`, `timestamp`, and metadata `parent_asin`, `title`.
- Strict history remains `timestamp < target_timestamp`.
- Y label rule remains `rating >= 4 -> Yes`, `rating < 4 -> No`.
- N ground truth remains the actual next full-sequence interaction, not the
  next positive interaction.
- Same-timestamp N ambiguity skips only that N sample, not the entire user.
- Candidate seed and model training seed must remain separate.

## Evidence Sources
- User migration directive on 2026-08-19.
- User-provided raw audit for Amazon Reviews 2023 5-core Musical_Instruments.
- User-reported formal cloud CPU/data/candidate outputs on 2026-08-19.
- Current code/config inspection:
  - `configs/experiment.yaml`
  - `src/data/preprocess.py`
  - `src/data/build_step2.py`
  - `src/data/build_preference.py`
  - `src/data/build_next_item.py`
  - `src/data/split.py`
  - `src/eval/candidate_sets.py`
  - `src/inference/prompts.py`
- Stage artifacts:
  - `.agent/cross_dataset_validation/dataset_source_decision.md`
  - `.agent/cross_dataset_validation/amazon_dataset_stats.json`
  - `.agent/cross_dataset_validation/amazon_preprocessing_report.md`
  - `.agent/cross_dataset_validation/code_reuse_audit.md`
  - `.agent/cross_dataset_validation/protocol.yaml`
  - `.agent/cross_dataset_validation/resolved_cloud_commands.md`
  - `.agent/cross_dataset_validation/seed42_plan.md`

## Related Code
- `configs/experiment.yaml`
- `src/data/preprocess.py`
- `src/data/build_step2.py`
- `src/data/build_preference.py`
- `src/data/build_next_item.py`
- `src/data/split.py`
- `src/data/stats.py`
- `src/eval/candidate_sets.py`
- `src/inference/prompts.py`
- `src/inference/base_zero_shot.py`
- `src/inference/evaluate_y_adapter.py`
- `src/inference/evaluate_n_adapter.py`
- `src/inference/evaluate_m_adapter.py`
- `src/train/train_y.py`
- `src/train/train_n.py`
- `src/train/train_m.py`
- `src/baselines/sasrec.py`
- `tests/test_amazon_reviews_preprocess.py`

## Current Progress
- Rejected `Amazon-books` catalog as interaction source remains recorded.
- Active source corrected to Amazon Reviews 2023 5-core Musical_Instruments.
- Added `amazon-musical-instruments` raw file config.
- Added Amazon Reviews 2023 CSV interaction adapter in `src/data/preprocess.py`.
- Added Amazon parquet metadata reader in `src/data/preprocess.py`.
- Adapter maps `parent_asin` to internal `movie_id` and retains `parent_asin`.
- Missing-title policy drops interactions whose `parent_asin` lacks valid
  metadata title.
- Candidate negative universe is retained observed interaction items, not all
  metadata-only ASINs.
- Y prompt is dataset-aware and uses `item` for Amazon while preserving
  `movie` for MovieLens.
- Formal CPU/data gate passed on cloud:
  - retained users: 57,439
  - retained items: 24,584
  - retained interactions: 511,792
  - Y samples: 396,908 train / 57,442 validation / 57,442 test
  - N samples: 339,449 train / 57,439 validation / 57,439 test
  - Y labels: 437,418 Yes / 74,374 No
  - timestamp buckets: 511,764 singleton, 14 size-2, none size>=3
  - N users skipped for insufficient legal samples: 0
- Formal candidate gate passed:
  - Random-k5 validation/test: 57,439 records each
  - PopMatch-k5 validation/test: 57,439 records each
  - all candidate files use exactly five candidates per record
  - PopMatch reduces mean absolute popularity gap by about 76.1% on validation
    and 77.5% on test relative to Random-k5.

## Verification Results
- `py_compile` passed for `src/data/preprocess.py` and
  `tests/test_amazon_reviews_preprocess.py`.
- Local bundled Python lacks `pytest`, `PyYAML`, and a parquet engine, so full
  local `build_step2` and tests cannot run here.
- Project/cloud runtime completed strict Step2 build, Random-k5 build,
  PopMatch-k5 build, and candidate diagnostics.
- Seed42 GPU experiments remain pending explicit user approval.

## Unresolved Questions
- What are the seed42 Base, Y-K0, N-K0, M1, and SASRec-exp-match metrics on
  Amazon Musical Instruments?
- Does the MovieLens direction replicate on Amazon under fixed PopMatch-k5?
- Is Random-k5 materially easier than PopMatch-k5 for this dataset?

## Pending Wiki Sync
- None yet. Do not write formal wiki until this stage reaches a real stop point
  and the user grants stage-end write authorization.

## Invalidating Conditions
- Treating aggregate catalog ratings as user labels.
- Treating catalog scrape timestamps as interaction timestamps.
- Using review text, product description, brand, category, price, images, or
  LLM-generated knowledge.
- Creating synthetic users or synthetic sequences.
- Mixing candidate seed with training seed.
- Launching seed43/44 before seed42 synthesis review.
