# Current Task

## Stage Goal
- Continue the active Cross-dataset Validation stage, rerouted on 2026-08-19
  from the rejected Amazon-books catalog to user-provided local Amazon Reviews
  2023 5-core Musical_Instruments.
- Integrate Amazon Musical Instruments through a dataset adapter, reuse the
  strict temporal Y/N pipeline, build fixed Random-k5 and PopMatch-k5
  candidates, and complete seed42 cross-dataset validation.

## Scope
- Active dataset: `amazon-musical-instruments`.
- Rejected prior source: `Amazon-books` catalog as interaction source.
- Local raw files:
  - `data/raw/amazon_reviews_2023/musical_instruments/interactions/Musical_Instruments.csv`
  - `data/raw/amazon_reviews_2023/musical_instruments/metadata/full-00000-of-00002.parquet`
  - `data/raw/amazon_reviews_2023/musical_instruments/metadata/full-00001-of-00002.parquet`
- Stage-local artifacts under `.agent/cross_dataset_validation/`.
- Formal CPU/data/candidate gate is complete.
- Seed42 full-test GPU queue is complete.

## Non-Goals
- No seed43/44 unless seed42 synthesis review explicitly decides the small
  N-K0 over M1 margin needs robustness evidence.
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
- User-reported seed42 full-test cloud metrics on 2026-08-22.
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
  - `.agent/cross_dataset_validation/seed42_result_summary.md`
  - `.agent/cross_dataset_validation/seed42_result_summary.json`

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
- Seed42 full-test run completed on 2026-08-22:
  - Base popmatch HR@1 / NDCG@5 / MRR: 0.3573007887 / 0.6829490861 / 0.5789568064
  - Y-K0 popmatch HR@1 / NDCG@5 / MRR: 0.2297916050 / 0.6099650726 / 0.4830304033
  - N-K0 popmatch HR@1 / NDCG@5 / MRR: 0.4668779053 / 0.7420073620 / 0.6569789980
  - M1 popmatch HR@1 / NDCG@5 / MRR: 0.4581730183 / 0.7383638504 / 0.6520839499
  - SASRec-exp-match popmatch HR@1 / NDCG@5 / MRR: 0.1756646181 / 0.5685149085 / 0.4295165306
  - N-K0 minus M1 on PopMatch: +0.0087048869 HR@1, +0.0036435116 NDCG@5, +0.0048950481 MRR
  - N-K0 minus SASRec-exp-match on PopMatch: +0.2912132871 HR@1, +0.1734924534 NDCG@5, +0.2274624674 MRR
  - On Random-k5, N-K0 and M1 are nearly tied: N-K0 minus M1 is +0.0011838646 HR@1.

## Verification Results
- `py_compile` passed for `src/data/preprocess.py` and
  `tests/test_amazon_reviews_preprocess.py`.
- Local bundled Python lacks `pytest`, `PyYAML`, and a parquet engine, so full
  local `build_step2` and tests cannot run here.
- Project/cloud runtime completed strict Step2 build, Random-k5 build,
  PopMatch-k5 build, and candidate diagnostics.
- Project/cloud runtime completed all planned seed42 full-test GPU jobs:
  Base, Y-K0, N-K0, M1, and SASRec-exp-match on Random-k5 and PopMatch-k5.
- Stage-local seed42 result summary recorded in
  `.agent/cross_dataset_validation/seed42_result_summary.md`.

## Unresolved Questions
- Should Amazon seed43/44 be run to test the small N-K0 over M1 margin, or is
  MovieLens multi-seed plus Amazon seed42 enough for the paper boundary?
- Should the stage now close through formal wiki sync, or first run a minimal
  Amazon seed43/44 N-K0-vs-M1 robustness check?

## Pending Wiki Sync
- `wiki/current_state.md`: update high-level project snapshot with completed
  Amazon Musical Instruments cross-dataset seed42 result.
- `wiki/reports/`: create or update a durable cross-dataset validation report
  with dataset adapter, data gate, candidate gate, seed42 metrics, and
  allowed/disallowed claims. If creating a new report, add it to wiki
  navigation during the authorized sync.
- `wiki/history/2026-08.md`: add a concise semantic history entry for the
  Amazon Musical Instruments dataset route and seed42 cross-dataset result.
- Optional `wiki/index.md`: update only if a new report file is created and
  needs navigation.
- Do not write formal wiki until the user grants one-time write authorization.

## Invalidating Conditions
- Treating aggregate catalog ratings as user labels.
- Treating catalog scrape timestamps as interaction timestamps.
- Using review text, product description, brand, category, price, images, or
  LLM-generated knowledge.
- Creating synthetic users or synthetic sequences.
- Mixing candidate seed with training seed.
- Launching seed43/44 before seed42 synthesis review.
