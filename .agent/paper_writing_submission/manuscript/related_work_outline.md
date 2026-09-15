# Related Work Outline

This section is intentionally an outline with citation slots. It must not be
treated as citation-complete manuscript prose.

## LLMs for Recommendation

Use this subsection to situate instruction-tuned or language-model-based
recommenders, including work that frames recommendation as prompting,
classification, generation, or item selection.

Citation slots:

- TODO:CITATION-LLMREC-SURVEY for recent surveys on LLM-based recommendation.
- TODO:CITATION-LLMREC-PROMPTING for prompt-based recommendation.
- TODO:CITATION-LLMREC-INSTRUCTION for instruction-tuned recommendation.
- TODO:CITATION-LLMREC-GENERATIVE for generation or item-selection interfaces.

## Preference Prediction and Sequential Recommendation

Use this subsection to separate explicit preference prediction from sequential
next-item recommendation. The bridge to this paper is that the two objectives
are often both called recommendation, but they imply different labels, scoring
interfaces, and evaluation metrics.

Citation slots:

- TODO:CITATION-PREF-MF for matrix-factorization preference prediction.
- TODO:CITATION-PREF-IMPLICIT for implicit-feedback recommendation.
- TODO:CITATION-SEQ-FOUNDATION for sequential next-item recommendation.
- TODO:CITATION-TASK-SEMANTICS for work distinguishing objective, label, or
  interface semantics in recommendation.

## Candidate-set Evaluation and Negative Sampling

Use this subsection to discuss sampled candidate evaluation, random negatives,
popularity bias, and harder negative construction. The manuscript's PopMatch
and k20/k50 results belong here.

Citation slots:

- TODO:CITATION-SAMPLED-EVAL for sampled-candidate ranking evaluation.
- TODO:CITATION-NEGATIVE-SAMPLING for negative-sampling protocol effects.
- TODO:CITATION-POPULARITY-BIAS for popularity bias in offline evaluation.
- TODO:CITATION-HARD-NEGATIVES for harder or popularity-matched candidate
  construction.

## Sequential Baselines and Budget-aware Comparison

Use this subsection to cover SASRec and specialized sequential recommenders,
then motivate why exposure and training-budget language matters.

Citation slots:

- TODO:CITATION-SASREC for the SASRec baseline.
- TODO:CITATION-SEQ-BASELINES for later sequential recommender baselines.
- TODO:CITATION-SAMPLE-EFFICIENCY for sample-efficiency or budget-aware model
  comparison.
- TODO:CITATION-COMPUTE-FAIRNESS for compute-aware or exposure-aware evaluation
  language.
