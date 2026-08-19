# Current Task

## Stage Goal
- Continue the active Cross-dataset Validation stage, rerouted on 2026-08-19
  from the rejected Amazon-books catalog to user-provided local Amazon Reviews
  2023 5-core Musical_Instruments.
- Integrate Amazon Musical Instruments through a dataset adapter, reuse the
  strict temporal Y/N pipeline, build fixed Random-k5 and PopMatch-k5
  candidates, then stop and report before GPU training.

## Scope
- Active dataset: `amazon-musical-instruments`.
- Rejected prior source: `Amazon-books` catalog as interaction source.
- Local raw files:
  - `data/raw/amazon_reviews_2023/musical_instruments/interactions/Musical_Instruments.csv`
  - `data/raw/amazon_reviews_2023/musical_instruments/metadata/full-00000-of-00002.parquet`
  - `data/raw/amazon_reviews_2023/musical_instruments/metadata/full-00001-of-00002.parquet`
- Stage-local artifacts under `.agent/cross_dataset_validation/`.
- This turn is CPU/data preparation only.

## Non-Goals
- No GPU training, Base inference, Y-K0/N-K0/M1 fine-tuning, SASRec training, or
  seed43/44.
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
- Local raw file presence checks.
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
- Raw feasibility from user audit:
  - interactions: 511,836
  - users: 57,439
  - items: 24,587
  - positive ratio at `rating >= 4`: 85.4680%
  - title coverage for interaction items: 24,584 / 24,587 = 0.999878
  - multi-item user-timestamp buckets: 12 / 511,824
  - approximate legal strict-Y targets: 454,396
  - legal strict-N targets: 454,374
- Added `amazon-musical-instruments` raw file config.
- Added Amazon Reviews 2023 CSV interaction adapter in `src/data/preprocess.py`.
- Added Amazon parquet metadata reader in `src/data/preprocess.py`.
- Adapter maps `parent_asin` to internal `movie_id` and retains `parent_asin`.
- Missing-title policy: drop interactions whose `parent_asin` lacks valid
  metadata title.
- Seed42 plan and CPU-only cloud commands are prepared, but formal strict
  preprocessing and candidate construction have not been run yet.

## Verification Results
- `py_compile` passed for `src/data/preprocess.py` and
  `tests/test_amazon_reviews_preprocess.py`.
- Local bundled Python lacks `pytest`, `PyYAML`, and a parquet engine, so full
  local `build_step2` and tests cannot run here.
- Formal verification remains pending in the project `.venv` or cloud runtime:
  strict Step2 build, Random-k5 build, PopMatch-k5 build, and candidate
  diagnostics.

## Unresolved Questions
- Does the cloud/project `.venv` have `pandas` and `pyarrow` or `fastparquet`?
- After missing-title drops, what are the formal retained users/items/interactions?
- What are the formal Y train/validation/test counts and label distributions?
- What are the formal N train/validation/test counts and skipped ambiguous N
  target counts?
- Does PopMatch-k5 reach acceptable matching quality and build success?

## Pending Wiki Sync
- None. Do not write formal wiki until this stage reaches a real stop point and
  the user grants stage-end write authorization.

## Invalidating Conditions
- Treating aggregate catalog ratings as user labels.
- Treating catalog scrape timestamps as interaction timestamps.
- Using review text, product description, brand, category, price, images, or
  LLM-generated knowledge.
- Creating synthetic users or synthetic sequences.
- Launching GPU training before strict Y/N samples and fixed candidates exist.
