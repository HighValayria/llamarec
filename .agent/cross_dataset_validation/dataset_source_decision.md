# Dataset Source Decision

## Active Dataset Source

Active dataset:

```text
amazon-musical-instruments
```

Local files:

```text
data/raw/amazon_reviews_2023/musical_instruments/interactions/Musical_Instruments.csv
data/raw/amazon_reviews_2023/musical_instruments/metadata/full-00000-of-00002.parquet
data/raw/amazon_reviews_2023/musical_instruments/metadata/full-00001-of-00002.parquet
```

Decision:

```text
Amazon Musical Instruments raw feasibility: PASS
```

Rationale:

- Interaction file has user/item/rating/timestamp columns.
- Metadata shards contain `parent_asin` and `title`.
- User-provided raw audit reports 511,836 interactions, 57,439 users, 24,587
  items, and 99.9878% interaction-item title coverage.
- Timestamp ties are rare and compatible with the existing strict temporal
  protocol.

## Rejected Dataset Source

Rejected source:

```text
Amazon-books catalog
```

Reason:

- No user/reviewer id.
- No per-user interaction rows.
- Aggregate product rating only.
- Catalog scrape timestamp only.
- Strict Y/N samples cannot be constructed.
- PopMatch-k5 cannot be constructed.

The catalog source should not be deleted, but it must not be used as an
interaction source for this stage.

## Current Stage Route

Route:

```text
Local Amazon Reviews 2023 5-core Musical_Instruments
-> Amazon adapter
-> shared strict temporal split
-> shared Y/N builders
-> fixed Random-k5 and PopMatch-k5 candidate files
-> stop and report before GPU
```
