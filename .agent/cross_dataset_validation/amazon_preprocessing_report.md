# Amazon Musical Instruments Preprocessing Report

## Status

Formal CPU/data gate is **PASS** for `amazon-musical-instruments`.

This report supersedes the earlier `Amazon-books` catalog feasibility failure
inside the same Cross-dataset Validation stage.

## Raw Data

Interaction file:

```text
data/raw/amazon_reviews_2023/musical_instruments/interactions/Musical_Instruments.csv
```

Metadata shards:

```text
data/raw/amazon_reviews_2023/musical_instruments/metadata/full-00000-of-00002.parquet
data/raw/amazon_reviews_2023/musical_instruments/metadata/full-00001-of-00002.parquet
```

## User-provided Raw Audit

- interactions: 511,836
- users: 57,439
- items: 24,587
- `rating >= 4`: 85.4680%
- `rating < 4`: 14.5320%
- duplicate rows: 0
- duplicate user-item-timestamp rows: 0
- user-timestamp buckets: 511,824
- multi-item timestamp buckets: 12
- multi-item bucket ratio: about 0.00234%

## Metadata Audit

- metadata rows: 213,593
- unique `parent_asin`: 213,593
- effective title ratio: 0.999925
- interaction item title coverage: 24,584 / 24,587 = 0.999878
- missing-title interaction items: `B000P5V2UM`, `B0BWJ4X2ZY`, `B01M5CXA0N`

## Adapter Decision

Amazon rows are standardized as:

| Amazon field | Internal compatibility field |
|---|---|
| `user_id` | `user_id` |
| `parent_asin` | `movie_id` and `parent_asin` |
| `rating` | `rating` |
| `timestamp` | `timestamp`, converted from milliseconds to seconds if needed |
| metadata `title` | `title` |

The internal `movie_id` name is kept for compatibility with existing split,
candidate, training, inference, and SASRec code. Artifacts retain `parent_asin`
inside interaction records for traceability.

## Missing-title Policy

Default policy:

```text
drop interactions whose parent_asin cannot resolve to a valid metadata.title
```

Formal output retained 511,792 interactions and 24,584 items, dropping 44 raw
interaction rows versus the raw audit because three interaction items had no
valid metadata title.

## Formal Strict Split

| Quantity | Value |
|---|---:|
| retained users | 57,439 |
| retained items | 24,584 |
| retained interactions | 511,792 |
| Y train samples | 396,908 |
| Y validation samples | 57,442 |
| Y test samples | 57,442 |
| N train samples | 339,449 |
| N validation samples | 57,439 |
| N test samples | 57,439 |
| N users skipped for insufficient legal samples | 0 |

Formal Y labels:

| Label | Count |
|---|---:|
| Yes | 437,418 |
| No | 74,374 |

Formal timestamp buckets:

| Bucket size | Count |
|---|---:|
| 1 | 511,764 |
| 2 | 14 |
| 3 | 0 |
| >=4 | 0 |

Singleton timestamp bucket ratio is 0.999972644388778. The strict temporal
policy remains valid: Y samples with equal timestamps share the same strict
history, while N skips only ambiguous next-item samples rather than entire
users.

## Candidate Item Universe

For `amazon-musical-instruments`, candidate negatives are drawn from items
observed in the retained interaction sequences after title join, not from all
metadata-only ASINs. This prevents Random-k5 and PopMatch-k5 from sampling
products that never appear in the interaction log.

## Candidate Gate

Both fixed candidate protocols were built for validation and test, each with
57,439 records per split and exactly five candidates per record.

PopMatch-k5 substantially reduces mean absolute popularity gap relative to
Random-k5:

| Split | Random gap | PopMatch gap | Reduction |
|---|---:|---:|---:|
| validation | 141.1943844774 | 33.8107862254 | 76.05387223% |
| test | 130.7513710197 | 29.3606869897 | 77.54446708% |

## Next Gate

Seed42 GPU experiments are now unblocked. Do not start seed43/44 until seed42
cross-dataset synthesis has been reviewed.
