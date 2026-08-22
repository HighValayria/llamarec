# Method Framework

The framework uses a shared base LLM and varies the supervision interface. The
base condition provides a zero-shot reference point. Y-K0 adapts the model to
the preference interface only. N-K0 adapts the model to the next-item candidate
interface only. M1 adapts the model under a unified multi-task construction that
keeps both preference and next-item outputs available. The paper does not
present these variants as a new architecture; they are controlled interfaces
for studying what different recommendation supervision signals teach the same
base model family.

For preference prediction, the input consists of a user history and a target
item. The output is a yes/no decision or probability-like score associated with
liking the item. The ranking version of this interface is candidate-wise: each
candidate is scored through the same P(Yes) path, and the candidates are sorted
by that score. This route is useful because it tests whether explicit
preference supervision alone can act as a next-item ranking proxy.

For next-item ranking, the input consists of a user history and a fixed
candidate set. The output is a candidate-label decision, scored through the N
interface. Unlike P(Yes)-based sorting, this scoring path is trained to select
the next observed interaction among candidates. Candidate construction is
therefore part of the task definition. Random-k5, PopMatch-k5, k20, and k50 are
reported as distinct protocols rather than merged into one leaderboard.

The SASRec comparison is framed as a baseline-positioning study. SASRec is not
treated as one undifferentiated baseline row. The closest-exposure rows compare
models under roughly matched N-task sample exposure. The high-exposure rows
show what happens after SASRec receives substantially more sequential
supervision. This separation is necessary because the two regimes support
different claims.
