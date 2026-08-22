# Abstract

Recommendation-tuned LLMs are often evaluated as if recommendation were a
single capability, yet common supervision signals encode different tasks. This
paper presents a systematic empirical study of preference supervision,
next-item supervision, unified multi-task tuning, candidate-set difficulty, and
SASRec baseline positioning. On MovieLens-1M, preference tuning improves
explicit preference prediction, but P(Yes)-based candidate ranking does not
substitute for next-item candidate-label ranking. N-task tuning gives the
strongest LLM ranking results, while M1 acts as a unified compromise that
retains both interfaces without surpassing the task-specific specialists.
Harder candidate protocols change the conclusions drawn from ranking
evaluation: PopMatch-k5 and candidate-size stress expose model separations that
Random-k5 can obscure. SASRec comparisons are strongly budget dependent.
N-K0 outperforms SASRec under closest N-task sample exposure, whereas high-
exposure SASRec surpasses N-K0 on MovieLens after substantially more
sequential supervision. Amazon Musical Instruments seed42 reproduces the main
ranking-side directions, including N-K0 over Y P(Yes)-based ranking, N-K0 over
M1 with a narrow margin, and N-K0 over closest-exposure SASRec. The study
argues for recommendation evaluation that states supervision semantics,
candidate protocol, and baseline exposure regime explicitly.
