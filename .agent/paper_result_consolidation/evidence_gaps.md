# Evidence Gaps

## Current Largest Gap

The largest paper-level evidence gap is external validity: all final formal
results are on MovieLens-1M. A second dataset would reduce the risk that the
observed sample-efficiency and semantic-split findings depend on movie-title
semantics or Llama pretraining exposure to movie knowledge.

## Other Gaps

- Strict compute/FLOPs/capacity matching between LLM adapters and SASRec is not
  completed.
- Coldest bucket evidence is small (`<=10`, 26 examples).
- Sample-efficiency findings are scoped to the current PopMatch-k5 protocol.
- Hyperparameter sensitivity for SASRec and LLM adapters is not fully mapped.
- The final target venue and required paper structure are not specified.

## Initial Recommendation

If the target paper needs stronger empirical generalization, prioritize a
Cross-dataset Validation Stage over additional MovieLens tuning. If the target
venue requires a method contribution, evaluate whether hard-negative training
or stronger next-item supervision is necessary; do not default to KAR without a
claim-to-evidence reason.
