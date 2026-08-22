# Related Work Outline

This section is intentionally an outline with citation slots. It must not be
treated as citation-complete manuscript prose.

## LLMs for Recommendation

Use this subsection to situate instruction-tuned or language-model-based
recommenders, including work that frames recommendation as prompting,
classification, generation, or item selection. TODO:CITATION for representative
LLM recommender papers and surveys.

## Preference Prediction and Sequential Recommendation

Use this subsection to separate explicit preference prediction from sequential
next-item recommendation. The bridge to this paper is that the two objectives
are often both called recommendation, but they imply different labels, scoring
interfaces, and evaluation metrics. TODO:CITATION for matrix factorization,
implicit feedback, and sequential recommendation foundations.

## Candidate-set Evaluation and Negative Sampling

Use this subsection to discuss sampled candidate evaluation, random negatives,
popularity bias, and harder negative construction. The manuscript's PopMatch
and k20/k50 results belong here. TODO:CITATION for candidate sampling and
negative-sampling evaluation critiques.

## Sequential Baselines and Budget-aware Comparison

Use this subsection to cover SASRec and specialized sequential recommenders,
then motivate why exposure and training-budget language matters. TODO:CITATION
for SASRec and recent sequential recommender baselines.
