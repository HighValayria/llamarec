# Abstract

Recommendation-tuned LLMs are often evaluated under a broad notion of
recommendation ability, but common supervision signals encode different tasks.
This paper presents a systematic empirical study of preference supervision,
next-item supervision, unified multi-task tuning, candidate-set difficulty, and
SASRec baseline positioning. On MovieLens-1M, preference tuning improves
explicit preference prediction, but P(Yes)-based candidate ranking does not
substitute for next-item candidate-label ranking. N-task tuning gives the
strongest LLM ranking results, while M1 serves as a unified adapter that
retains both interfaces without surpassing the task-specific specialists.
Harder candidate protocols change the interpretation of ranking evidence:
PopMatch-k5 and candidate-size stress expose model separations that Random-k5
can obscure. SASRec comparisons are exposure dependent. N-K0 is stronger under
closest N-task sample exposure, while a SASRec checkpoint trained with far more
sequential exposure surpasses the current low-exposure N-K0 on MovieLens. Amazon Musical
Instruments seed42 reproduces the main ranking-side directions, including
N-K0 over Y P(Yes)-based ranking, N-K0 over M1 with a narrow margin, and N-K0
over closest-exposure SASRec. The results support recommendation evaluation
that states supervision semantics, candidate protocol, and baseline exposure
regime explicitly.
