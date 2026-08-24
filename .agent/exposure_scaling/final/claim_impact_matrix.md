# Claim Impact Matrix

This matrix is preliminary because no new GPU scaling jobs have been run.

| claim | current evidence | scaling decision rule | current status |
|---|---|---|---|
| Claim A: Preference supervision and next-item supervision learn different capabilities. | Y-K0 binary is strong; Y P(Yes)-ranking is far below N-K0 at 12k. | Strengthened if Y binary improves/plateaus while Y ranking remains far below exposure-matched N. Weakened if Y ranking approaches N with exposure. | unchanged pending Y 24k/48k |
| Claim B: N specialist > M1 unified under matched per-task exposure. | N-K0 > M1 at 12k N exposure vs M1 12k N + 12k Y across seeds. | Strengthened if N remains above M1 at matched per-task high exposure. Weakened/changed if M1 catches or surpasses N. | unchanged pending M1 selected point |
| Claim C: N-K0 stronger than SASRec at limited/matched sample exposure. | N-K0 > closest-exposure SASRec at 3k/6k/12k/24k and across selected seeds. | Strengthened if N remains above SASRec at 48k/96k/near-full matched exposure. Weakened if SASRec catches at matched exposure. | currently strengthened for low exposure only |
| Claim D: High-exposure SASRec > LLM. | Existing high-exposure SASRec beats low-exposure N-K0, but no high-exposure LLM head-to-head exists. | Only claim true high-exposure head-to-head after high-exposure LLM point exists. Otherwise keep limitation. | must remain limited |
