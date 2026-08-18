# Current Task

## Stage Goal
- Open the Cross-dataset Validation stage using `amazon-books` as the selected
  second dataset.
- First answer the Dataset Feasibility Gate before any GPU training.
- Validate, when data is feasible, whether MovieLens-1M findings transfer:
  Y/N task-interface separation, N-K0 ranking specialist behavior, M1 unified
  tradeoff, PopMatch candidate difficulty, and closest-exposure SASRec
  positioning.

## Scope
- Dataset: `amazon-books`.
- Raw local files currently found under `data/raw/Amazon-books/`.
- Stage-local artifacts under `.agent/cross_dataset_validation/`.
- Initial work is CPU-only data and code feasibility auditing.

## Non-Goals
- No GPU training until the Amazon Books feasibility gate passes.
- No KAR, review-text augmentation, description augmentation, hard-negative
  training, new M variant, LoRA sweep, 7B, third dataset, or strict FLOPs match.
- Do not force the catalog dataset into a different task definition.
- Do not write formal wiki during this stage until stage-end authorization.

## Long-Term Constraints
- Paper Result Consolidation was wiki-synced and committed before opening this
  stage.
- A one-time direct relevant wiki read was used at stage opening on
  2026-08-18 and then revoked.
- Subsequent stage work should rely on this current task, stage-local
  artifacts, current code/config, and raw Amazon Books files.
- The strict history rule remains `timestamp < target_timestamp`.
- Candidate protocols must keep train seed and candidate seed separate.
- SASRec exposure matching must be recomputed from actual N-K0 N-task exposure
  on the second dataset.

## Evidence Sources
- User directive on 2026-08-18 selecting `amazon-books`.
- One-time direct wiki read at stage opening:
  - `wiki/index.md`
  - `wiki/current_state.md`
  - `wiki/reports/paper-result-consolidation.md`
  - `wiki/reports/multiseed-stability.md`
  - `wiki/reports/sample-efficiency-training-efficiency.md`
  - `wiki/reports/fair-budget-baseline-positioning.md`
  - `wiki/reports/phase-2c-popmatch-hard-candidate-diagnosis.md`
- Raw files:
  - `data/raw/Amazon-books/Amazon_popular_books_dataset.csv`
  - `data/raw/Amazon-books/Amazon_popular_books_dataset.json`
  - `data/raw/Amazon-books/README.md`
- Stage artifacts:
  - `.agent/cross_dataset_validation/dataset_stats.json`
  - `.agent/cross_dataset_validation/dataset_feasibility.md`
  - `.agent/cross_dataset_validation/code_reuse_audit.md`
  - `.agent/cross_dataset_validation/protocol.yaml`
  - `.agent/cross_dataset_validation/resolved_cloud_commands.md`
  - `.agent/cross_dataset_validation/cloud_commands.sh`

## Related Code
- `configs/experiment.yaml`
- `src/data/build_step2.py`
- `src/data/preprocess.py`
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

## Current Progress
- Paper Result Consolidation wiki sync was applied and committed.
- Cross-dataset Validation stage opened with `amazon-books` selected by the
  user.
- Raw Amazon Books files were inspected locally.
- Dataset Feasibility Gate currently blocks training:
  - 2269 item rows and 2269 unique ASINs.
  - 100% title coverage.
  - no user/reviewer id column.
  - no per-user interaction rows.
  - `rating` is aggregate average rating, not per-interaction rating.
  - `timestamp` is catalog scrape timestamp, not interaction timestamp.
  - strict Y samples: 0.
  - strict N samples: 0.
  - PopMatch-k5: blocked because no legal N targets or training-split item
    popularity.
- Code reuse audit found current code is conceptually reusable but
  MovieLens-shaped around `movie_id`, `load_movies()`, and "movie" prompt text.

## Verification Results
- `tools/wiki_guard.py` passed after Paper Result Consolidation wiki sync.
- `tools/stage_guard.py` passed before closure commit.
- Local Amazon Books CSV feasibility statistics were computed from the raw CSV.
- Local Python lacks `yaml`, so some CLI `--help` checks that import project
  config fail locally; cloud/venv should be used for final resolved commands
  after data is unblocked.

## Unresolved Questions
- Can the user provide an Amazon Books review interaction file, not only the
  product catalog?
- Should the current catalog file be used as item metadata after interaction
  data is added?
- If Amazon Books review interactions are unavailable, should the stage switch
  to another Amazon review category with interaction rows?

## Pending Wiki Sync
- None yet. At stage end, propose a cross-dataset validation report and current
  state update based on the final gate/result status.

## Invalidating Conditions
- Treating aggregate product ratings as user preference labels.
- Treating catalog scrape timestamp as an interaction timestamp.
- Creating synthetic users or sequences to force the dataset through Y/N.
- Launching GPU training before strict Y/N samples and fixed candidate files
  exist.
