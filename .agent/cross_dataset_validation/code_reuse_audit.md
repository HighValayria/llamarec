# Code Reuse Audit

## Summary

The existing pipeline can be reused conceptually, but it is currently
MovieLens-shaped in field names and loader assumptions. The larger blocker is
not code abstraction; it is that the supplied Amazon Books files are not
interaction data.

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
  `movie_id`, `movies`, and MovieLens file formats.
- `src/eval/candidate_sets.py` loads all candidate ids through
  `load_movies()` and writes `candidate_movie_ids` /
  `ground_truth_movie_id`.
- `src/inference/prompts.py` renders "Target movie" and "Would the user like
  the target movie?".
- Candidate validation checks `target["movie_id"]`.
- Configuration uses `raw_movielens_*` and `movie_id` field names.

## Minimal Code Direction After Data Is Unblocked

Add a dataset adapter layer rather than copying all Y/N logic:

- `load_interactions(dataset_key, config)`
- `load_item_metadata(dataset_key, config)`
- `format_item_text(item)`

Then map:

- MovieLens: `movie_id`, `title`
- Amazon Books: `asin`, `title`

Keep current prompt semantics but replace hardcoded "movie" wording with a
generic "item" / "book" wording controlled by dataset metadata.

## Current Blocking Decision

Do not implement these code changes until an Amazon Books interaction file is
available. Without interaction rows, data-layer abstraction cannot produce
valid Y/N samples.
