# Paper Result Consolidation Stage Summary

## Status

Stage-local consolidation is complete. No new training was launched, and formal
wiki read access remained revoked after the one-time stage-opening migration
read.

## Main Paper Claims

1. Y-style preference supervision and N-style next-item supervision learn
   different recommendation semantics.
2. N-K0 is the strongest completed LLM ranking setting, while M1 is the best
   unified Y/N tradeoff.
3. LLM-vs-SASRec conclusions are budget-regime dependent: N-K0 is stronger at
   closest N-task sample exposure, while high-exposure SASRec is stronger.
4. Canonical Random-k5 must be supplemented with PopMatch-k5 and candidate-size
   stress tests to reduce popularity shortcut concerns.

## Evidence Strength

- Multi-seed stability is available for seeds 42/43/44.
- PopMatch-k5, k20/k50, popularity, BPR-MF, and SASRec diagnostics support the
  core ranking narrative.
- Sample-efficiency evidence supports low-exposure LLM advantage over SASRec,
  but not strict compute matching.

## Main Limitations

- MovieLens-1M only.
- Candidate protocols remain offline diagnostics.
- SASRec comparisons are not strict FLOP, wall-clock, or capacity matches.
- M1 has larger total Y+N exposure than N-K0 in fair-budget framing.
- Coldest item bucket has only 26 samples.

## Recommended Next Stage

Run a compact cross-dataset validation stage before claiming broad
generalization. If that is blocked, move to manuscript table finalization and
state MovieLens-1M scope explicitly.

## Produced Artifacts

- `.agent/paper_result_consolidation/paper_ready_claims.json`
- `.agent/paper_result_consolidation/paper_results_draft.md`
- `.agent/paper_result_consolidation/limitations.md`
- `.agent/paper_result_consolidation/tables/`
- `.agent/paper_result_consolidation/final/validated_findings.yaml`
- `.agent/paper_result_consolidation/final/rejected_findings.yaml`
- `.agent/paper_result_consolidation/final/open_questions.yaml`
- `.agent/paper_result_consolidation/final/next_stage_recommendation.md`
- `.agent/paper_result_consolidation/final/wiki_update_proposal.yaml`
