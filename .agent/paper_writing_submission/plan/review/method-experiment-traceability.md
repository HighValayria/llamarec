# Method-Experiment Traceability

| Contribution | Method module | Experiment | Table/Figure | Allowed claim | Evidence status |
|---|---|---|---|---|---|
| Supervision semantics | Y and N task interfaces | MovieLens binary/ranking; Amazon ranking | Table 1, Figure 1 | Preference and next-item supervision induce distinct capabilities | Strong on MovieLens; directional Amazon ranking support |
| Specialist/unified tradeoff | Y-K0, N-K0, M1 | MovieLens PopMatch multi-seed; Amazon PopMatch seed42 | Table 1, Table 4 | M1 is a unified compromise; specialists retain advantages | Strong on MovieLens; narrow Amazon support |
| Candidate difficulty | Random-k5, PopMatch-k5, k20, k50 | Robustness and candidate construction comparisons | Table 2, Figure 3 | Random-k5 alone is insufficient for strong ranking claims | Strong on MovieLens; supported by Amazon candidate contrast |
| Exposure-aware baseline positioning | N-K0, SASRec closest exposure, SASRec high exposure | Sample-efficiency and multi-seed SASRec comparisons | Table 3, Figure 2, Table 4 | LLM-vs-SASRec conclusions depend on supervision exposure | Strong on MovieLens; Amazon supports closest-exposure direction |
| Cross-dataset validation | Amazon Musical Instruments seed42 | Full-test seed42 cross-domain run | Table 1, Table 3, Table 4 | Key ranking-side directions reproduce on Amazon | Directional only; not multi-seed |
