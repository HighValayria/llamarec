# Code Reuse Audit

## Summary

The existing pipeline can be reused with a small compatibility adapter. The
active dataset source is now Amazon Reviews 2023 5-core Musical_Instruments.
Its raw interaction contract is valid, and the implementation maps
`parent_asin` to the existing internal `movie_id` field while retaining
`parent_asin` for traceability.

## Directly Reusable Concepts

- Strict temporal split contract: `history = timestamp < target_timestamp`.
- Y task definition: `History + Target -> Yes/No`.
- N task definition: full-sequence next-item prediction.
- Fixed candidate files shared across Base/Y/N/M/SASRec.
- PopMatch idea: negatives matched to target item popularity using
  training-split popularity.
- Training entry points: `src/train/train_y.py`, `src/train/train_n.py`,
  `src/train/train_m.py`.
- Inference entry points: `src/inference/base_zero_shot.py`,
  `src/inference/evaluate_y_adapter.py`, `src/inference/evaluate_n_adapter.py`,
  `src/inference/evaluate_m_adapter.py`.

## MovieLens-specific Hardcoding Found

- `src/data/preprocess.py` is explicitly a MovieLens loader and uses
  `movie_id`, `movies`, and MovieLens file formats. A minimal Amazon Reviews
  2023 CSV/parquet adapter has now been added.
- `src/eval/candidate_sets.py` loads all candidate ids through
  `load_movies()` and writes `candidate_movie_ids` /
  `ground_truth_movie_id`. This remains acceptable for the current compatibility
  path because Amazon ASINs are stored internally as `movie_id`. A dataset
  option now lets Amazon use observed retained interaction items as the
  candidate universe instead of all metadata-only ASINs.
- `src/inference/prompts.py` renders "Target movie" and "Would the user like
  the target movie?". This is semantically imperfect for books/instruments but
  does not block CPU preprocessing. It should be revised before GPU inference.
- Candidate validation checks `target["movie_id"]`; the Amazon adapter supplies
  this field from `parent_asin`.
- Configuration uses `raw_movielens_*` and `movie_id` field names; a new
  `amazon-musical-instruments` raw file entry has been added with
  `candidate_item_universe: observed_interactions`.

## Minimal Code Direction After Data Is Unblocked

Longer term, add a dataset adapter layer rather than relying on the
compatibility `movie_id` mapping:

- `load_interactions(dataset_key, config)`
- `load_item_metadata(dataset_key, config)`
- `format_item_text(item)`

Then map:

- MovieLens: `movie_id`, `title`
- Amazon Books: `asin`, `title`

Keep current prompt semantics but replace hardcoded "movie" wording with a
generic "item" / "book" wording controlled by dataset metadata.

## Current Blocking Decision

Do not launch GPU training until formal strict preprocessing and candidate
construction pass in the project runtime. The immediate next step is CPU-only:
run `src.data.build_step2`, build Random-k5 and PopMatch-k5 candidate files,
and inspect candidate diagnostics.
