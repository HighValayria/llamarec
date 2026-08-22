# Introduction

Large language models are increasingly adapted for recommendation tasks, but
offline evaluation often treats recommendation ability as if it were a single
capability. In practice, common recommendation objectives ask different
questions. A preference-prediction interface estimates whether a user will like
a given item. A next-item interface selects the next observed interaction from
a candidate set. These two formulations share user histories and item
identities, yet they define different supervision semantics and different
ranking scores.

This distinction creates a gap in how recommendation-tuned LLMs are evaluated.
If a model learns explicit preference prediction, it is not obvious that the
same score should solve next-interaction ranking. If a model is trained on both
tasks, it is unclear whether the unified model retains both abilities or loses
some task-specific advantage. Candidate construction adds another layer: random
negative candidates can make a ranking task easier than popularity-matched or
larger candidate sets. Baseline comparisons also depend on training exposure,
especially when comparing an adapted LLM with a specialized sequential
recommender such as SASRec.

This paper studies these questions through a controlled empirical analysis of
recommendation supervision semantics. The experiments separate Y preference
supervision from N next-item supervision, evaluate a unified M1 multi-task
adapter, compare Random-k5 with PopMatch-k5 and larger candidate sets, and
position SASRec under closest-exposure and high-exposure regimes. MovieLens-1M
provides the full evidence package, including multi-seed stability and
diagnostics. Amazon Musical Instruments provides seed42 cross-domain validation
for the main ranking-side directions.

The contribution is not a new recommender architecture. The contribution is a
claim-traceable empirical account of what different supervision interfaces
teach recommendation-tuned LLMs, how multi-task unification changes the
specialist tradeoff, why candidate difficulty changes ranking conclusions, and
why LLM-vs-SASRec comparisons must be stated as budget-regime-specific claims.
The manuscript keeps these boundaries explicit so that positive results do not
turn into universal claims unsupported by the experiments.
