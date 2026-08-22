# Cross-dataset Validation Stage Synthesis

## Status

The Cross-dataset Validation stage has reached a synthesis-ready stop point.
Amazon Musical Instruments seed42 full-test results are complete for Base,
Y-K0, N-K0, M1, and SASRec-exp-match on both Random-k5 and PopMatch-k5.

Formal wiki sync is still pending user authorization.

## Dataset And Protocol

Active second dataset: `amazon-musical-instruments`.

Source: user-provided local Amazon Reviews 2023 5-core Musical_Instruments.

Allowed inputs:

- interaction `user_id`
- interaction `parent_asin`
- interaction `rating`
- interaction `timestamp`
- metadata `parent_asin`
- metadata `title`

Forbidden inputs remained excluded: review text, product description, brand,
category, price, image data, and external item knowledge.

Strict temporal policy:

- Y history uses interactions with `timestamp < target_timestamp`.
- Y label is `rating >= 4 -> Yes`, otherwise `No`.
- N target is the actual next full-sequence interaction, not the next positive
  interaction.
- Same-timestamp ambiguity skips only ambiguous N samples.

## Data Gate

Formal retained data:

| quantity | value |
|---|---:|
| users | 57,439 |
| items | 24,584 |
| interactions | 511,792 |
| Y train | 396,908 |
| Y validation | 57,442 |
| Y test | 57,442 |
| N train | 339,449 |
| N validation | 57,439 |
| N test | 57,439 |

Candidate gate:

| candidate set | validation rows | test rows | mean abs popularity gap on test |
|---|---:|---:|---:|
| Random-k5 seed42 | 57,439 | 57,439 | 130.7513710197 |
| PopMatch-k5 seed42 | 57,439 | 57,439 | 29.3606869897 |

PopMatch-k5 reduced test mean absolute popularity gap by about 77.5% relative
to Random-k5.

## Seed42 Result

Primary PopMatch-k5 ranking metrics:

| model | HR@1 | NDCG@5 | MRR |
|---|---:|---:|---:|
| Base | 0.3573007887 | 0.6829490861 | 0.5789568064 |
| Y-K0 | 0.2297916050 | 0.6099650726 | 0.4830304033 |
| N-K0 | 0.4668779053 | 0.7420073620 | 0.6569789980 |
| M1 | 0.4581730183 | 0.7383638504 | 0.6520839499 |
| SASRec-exp-match | 0.1756646181 | 0.5685149085 | 0.4295165306 |

Primary PopMatch-k5 comparisons:

| comparison | delta HR@1 | delta NDCG@5 | delta MRR |
|---|---:|---:|---:|
| N-K0 minus M1 | 0.0087048869 | 0.0036435116 | 0.0048950481 |
| N-K0 minus SASRec-exp-match | 0.2912132871 | 0.1734924534 | 0.2274624674 |
| N-K0 minus Base | 0.1095771166 | 0.0590582759 | 0.0780221917 |
| N-K0 minus Y-K0 | 0.2370863002 | 0.1320422893 | 0.1739485947 |

Random-k5 supplemental comparisons:

| comparison | delta HR@1 | delta NDCG@5 | delta MRR |
|---|---:|---:|---:|
| N-K0 minus M1 | 0.0011838646 | 0.0010205825 | 0.0013037019 |
| N-K0 minus SASRec-exp-match | 0.0675673323 | 0.0410733831 | 0.0537628325 |

## Allowed Claims

- Cross-dataset direction replicates on Amazon Musical Instruments under
  PopMatch-k5: N-K0 remains above M1 and far above sample-exposure-matched
  SASRec.
- N-K0's advantage over M1 on Amazon is directionally consistent but small.
- N-K0's advantage over SASRec-exp-match on Amazon is large under PopMatch-k5.
- PopMatch-k5 is the better primary candidate protocol for Amazon because it
  reduces popularity-gap diagnostics and exposes a much larger SASRec drop.
- Random-k5 should be reported as supplemental/easier; N-K0 and M1 are nearly
  tied on Random-k5.

## Disallowed Or Risky Claims

- Do not claim Amazon multi-seed stability. Only seed42 has been run.
- Do not claim a large N-K0 over M1 advantage on Amazon; the PopMatch HR@1
  margin is only 0.0087048869.
- Do not claim strict compute matching. SASRec-exp-match is a sample-exposure
  diagnostic.
- Do not generalize to all Amazon categories; this is Musical Instruments only.
- Do not attribute gains to review text, product semantics beyond title, or
  external product knowledge.

## Seed43/44 Decision

Recommendation: do not launch seed43/44 immediately.

Reasoning:

- MovieLens already has multi-seed stability evidence.
- Amazon seed42 full-test is enough for a cross-dataset direction check if the
  paper frames Amazon as a validation dataset rather than a second full
  stability study.
- The only reason to run Amazon seed43/44 is to harden the small N-K0 over M1
  margin. That is a cost/claim-strength tradeoff, not a blocker for the current
  synthesis.

If seed43/44 are later approved, run only the minimum necessary matrix first:
N-K0 and M1 on PopMatch-k5. SASRec-exp-match can remain seed42 unless the
paper requires all baselines to be multi-seed on the second dataset.

## Next Step

Close this stage through authorized wiki sync, unless the user chooses to run a
minimal Amazon seed43/44 robustness check for N-K0 versus M1.
