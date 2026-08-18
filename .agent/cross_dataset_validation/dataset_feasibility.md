# Dataset Feasibility Gate: Amazon Books

## Decision

**Gate status: blocked before training.**

The selected second dataset is `amazon-books`, stored under
`data/raw/Amazon-books`. The current files are a product catalog / aggregate
book metadata dataset, not a user-item interaction dataset. It has ASINs,
titles, aggregate ratings, review counts, bestseller ranks, categories, prices,
and catalog scrape timestamps, but it does not contain `user_id`,
per-interaction ratings, or per-user timestamps.

Therefore the current raw files cannot support the formal Cross-dataset
Validation protocol without additional review interaction data.

## Observed Raw Files

- `data/raw/Amazon-books/Amazon_popular_books_dataset.csv`
- `data/raw/Amazon-books/Amazon_popular_books_dataset.json`
- `data/raw/Amazon-books/README.md`

## Basic Statistics

- rows: 2269
- unique ASINs: 2269
- unique users: 0
- individual interactions: 0
- title coverage: 100%
- aggregate rating coverage: 100%
- timestamp coverage: 100%, but this is a catalog scrape timestamp, not a user
  interaction timestamp
- review count range: 10010 to 196572

## Gate Checks

| Check | Result | Notes |
|---|---|---|
| Has item id | pass | `asin` exists. |
| Has item title | pass | `title` coverage is 100%. |
| Has user id | fail | No user/reviewer id column exists. |
| Has per-interaction rating | fail | `rating` is aggregate average rating. |
| Has interaction timestamp | fail | `timestamp` is catalog scrape time. |
| Can construct strict Y train/valid/test | fail | No user-item preference events. |
| Can construct strict N train/valid/test | fail | No per-user temporal sequence. |
| Can compute train-split item popularity | fail | Review counts are aggregate item metadata, not split-specific interactions. |
| Can build PopMatch-k5 | fail | No legal N target samples. |

## Consequence

Do not launch Base, Y-K0, N-K0, M1, or SASRec training on this raw dataset.
Doing so would require changing the research question from interaction-level
recommendation to item-catalog prediction, which is outside the stage scope.

## Required Input To Unblock

To use Amazon Books as the second dataset under the current LlamaRec protocol,
add an interaction-level review file with at least:

- `user_id` or `reviewerID`;
- `asin` or equivalent item id;
- per-review `rating`;
- per-review timestamp, such as Unix time or review date;
- item title metadata keyed by ASIN.

The current catalog file can still be used as item metadata after an interaction
file is added.
