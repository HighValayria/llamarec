# Evidence-gap Audit

## Status

The existing evidence is sufficient to continue manuscript writing with scoped
claims. No new experiment is required before drafting the first manuscript
package.

## Main Claims And Evidence Status

| Claim | Evidence status | Blocking gap |
|---|---|---|
| Preference and next-item supervision induce distinct abilities | strong on MovieLens; directional support on Amazon ranking | Amazon validation-calibrated binary metrics are incomplete |
| M1 unifies both abilities but does not dominate specialists | strong on MovieLens multi-seed; directional Amazon PopMatch support | Amazon N-K0 over M1 margin is small and seed42-only |
| Candidate difficulty changes conclusions | strong on MovieLens; supported by Amazon Random/PopMatch contrast | none blocking |
| LLM-vs-SASRec depends on supervision exposure | strong on MovieLens; Amazon seed42 supports closest-exposure direction | strict compute matching remains future work, not blocker |

## Amazon Binary Evidence Check

Amazon seed42 outputs include Base/Y-K0/M1 binary AUC, F1, and Accuracy on the
test split:

| model | AUC | F1 | Accuracy |
|---|---:|---:|---:|
| Base | 0.6084359088 | 0.3990274739 | 0.3545315275 |
| Y-K0 | 0.4902616517 | 0.9059705193 | 0.8283137774 |
| M1 | 0.5128936310 | 0.9032109784 | 0.8240486055 |

However, the paper-facing validation-calibrated Amazon binary protocol is not
yet documented. The current Amazon binary rows are sufficient as diagnostic
outputs but should not be used as a strong cross-dataset binary-calibration
claim.

Decision: record as a non-blocking evidence gap. If the paper later needs a
strong cross-dataset binary claim, propose a low-cost evaluation using existing
Amazon Y-K0/M1 adapters and validation/test splits; do not launch it without
user approval.

## Amazon N-K0 vs M1 Margin

Amazon PopMatch-k5 seed42:

| comparison | delta HR@1 | delta NDCG@5 | delta MRR |
|---|---:|---:|---:|
| N-K0 minus M1 | 0.0087048869 | 0.0036435116 | 0.0048950481 |

Decision: not blocking for a directional cross-dataset validation claim, but
the manuscript must say the Amazon margin is narrow. Amazon seed43/44 are an
optional strengthening experiment only if reviewers or target venue require
second-dataset multi-seed support.

## Strict Compute Matching

Strict FLOPs/wall-clock/capacity matching is not available. Existing evidence
supports sample-exposure-aware interpretation, not strict compute equivalence.

Decision: limitation/future work, not a blocker.

## Related Work Evidence

Current stage has not performed literature retrieval or citation verification.

Decision: not blocking the experiment audit, but Related Work drafting must be
a later evidence-driven task with citation checks.
