# Manuscript Outline

## 1 Introduction

Motivate the mismatch between preference prediction and next-interaction
ranking for recommendation-tuned LLMs. Present the paper as an empirical study
of supervision semantics, multi-task unification, candidate difficulty, and
budget-aware baseline positioning.

## 2 Related Work

- LLMs for recommendation.
- Recommendation tuning and instruction tuning.
- Sequential recommendation and SASRec-style baselines.
- Multi-task recommendation.
- Candidate sampling and offline evaluation protocols.

## 3 Problem Formulation

- Preference prediction: `P(Like | History, Item)`.
- Next-item prediction: `P(Next Item | History, Candidate Set)`.
- Multi-task Y/N formulation with separate inference interfaces.

## 4 Experimental Framework

- Base LLM.
- Y-K0.
- N-K0.
- M1.
- Candidate scoring interfaces.
- Training setup and seed handling.

## 5 Experimental Setup

- Datasets: MovieLens-1M and Amazon Musical Instruments.
- Strict temporal split.
- Candidate construction: Random-k5, PopMatch-k5, k20/k50, order perturbation.
- Baselines: Base, Popularity, BPR-MF, SASRec.
- Metrics.
- Budget and exposure protocol.
- Multi-seed protocol.

## 6 Results

- RQ1 Preference vs next-item supervision.
- RQ2 Specialized vs multi-task learning.
- RQ3 Candidate difficulty and robustness.
- RQ4 LLM vs SASRec across exposure regimes.
- RQ5 Cross-dataset validation.
- Stability and diagnostic analysis.

## 7 Discussion

- What recommendation-tuned LLMs learn.
- Sample efficiency versus high-budget sequential performance.
- Implications for unified recommenders.
- Limitations and future work.

## 8 Conclusion

Concise restatement of scoped empirical findings and boundaries.

## Abstract

Write last after Results/Discussion are stable.
