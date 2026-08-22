# Conclusion

The completed evidence supports a supervision-conditioned view of LLM
recommendation. Preference supervision improves explicit preference prediction,
but a P(Yes)-based ranking score does not replace a next-item candidate-label
ranking interface. N-task supervision produces much stronger next-interaction
ranking under the tested candidate protocols.

Multi-task tuning provides a useful unified model, but the strongest current
evidence favors a tradeoff interpretation. M1 retains both interfaces and ranks
close to N-K0, while N-K0 remains above M1 on MovieLens across seeds and
directionally above M1 on Amazon PopMatch-k5. Candidate difficulty is central
to this conclusion: Random-k5 is useful as a reference, but PopMatch-k5 and
candidate-size stress reveal separations hidden by easier candidates.

The SASRec comparison is budget-regime dependent. N-K0 is much stronger than
SASRec under closest N-task sample exposure on MovieLens and Amazon. High-
exposure SASRec, however, surpasses N-K0 on MovieLens after substantially more
sequential supervision. The resulting conclusion is not that either model
family is universally better, but that the comparison changes with the amount
and type of supervision available.

Future work can strengthen the current manuscript by adding validation-
calibrated Amazon binary reporting, Amazon seed43/44 robustness for the narrow
N-K0 over M1 margin, and stricter compute-aware comparison. These additions are
not required for the present empirical story, but they would sharpen the
cross-dataset and baseline-positioning boundaries.
