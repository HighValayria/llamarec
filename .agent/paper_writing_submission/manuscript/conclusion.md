# Conclusion

The completed evidence supports a supervision-conditioned view of LLM
recommendation. Preference supervision improves explicit preference prediction,
but a P(Yes)-based ranking score does not replace a next-item candidate-label
ranking interface. N-task supervision produces much stronger next-interaction
ranking under the tested candidate protocols, which means that task interface
semantics must be stated before interpreting recommendation-tuned LLM results.

The multi-task results support a tradeoff interpretation rather than a
dominance claim. M1 retains both interfaces and ranks close to N-K0, while
N-K0 remains above M1 on MovieLens across seeds and directionally above M1 on
Amazon PopMatch-k5. Candidate difficulty is central to this conclusion.
Random-k5 is useful as a reference condition, but PopMatch-k5 and
candidate-size stress reveal separations that easier candidates can obscure.

The SASRec comparison is also exposure-aware but not a complete frontier.
N-K0 is much stronger than SASRec under closest N-task sample exposure on
MovieLens and Amazon. A MovieLens SASRec checkpoint trained with substantially
more sequential supervision surpasses the current low-exposure N-K0 checkpoint,
but N-K0 was not trained to the same 1.53M exposure. The resulting conclusion is
not that either model family is universally better; it is that the observed
evidence supports N-K0 sample efficiency while leaving high-budget head-to-head
comparison open.

The remaining gaps define clear follow-up work rather than blocking the current
empirical story. Validation-calibrated Amazon binary reporting would strengthen
cross-dataset preference evidence. Amazon seed43/44 would test the narrow
N-K0-over-M1 margin more directly. Stricter compute-aware comparison would
separate exposure effects from FLOPs, wall-clock time, and model capacity.
Until those additions are made, the paper's claims remain deliberately scoped
to supervision semantics, candidate difficulty, and exposure-aware baseline
positioning.
