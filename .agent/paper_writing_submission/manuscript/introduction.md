# Introduction

Large language models are increasingly used as recommendation components, with
recent work studying recommendation as language processing, instruction tuning,
prompting, conversational recommendation, and zero-shot ranking
[@zhao2024llmrec; @geng2022p5; @bao2023tallrec; @he2023zeroshotconv;
@hou2024zeroshotrankers]. This expansion makes the word recommendation cover a
wider set of model interfaces than before. A recommendation-tuned LLM may
produce a binary preference score, a candidate label, or a generated ranking,
yet these outputs need not represent the same capability. Treating them as
interchangeable can make an offline evaluation look cleaner than the underlying
supervision actually is.

The distinction is not only specific to LLMs. Preference-oriented collaborative
filtering and implicit-feedback models provide one foundation for learning from
user-item behavior [@koren2009mf; @hu2008implicit], while sequential
recommenders such as SASRec and BERT4Rec model ordered histories and next-item
behavior [@kang2018sasrec; @sun2019bert4rec]. These traditions suggest two
different questions for an adapted LLM. A preference-prediction interface asks
whether a user is likely to like a given item. A next-item interface asks which
candidate is the next observed interaction. The two formulations may share user
histories and item identities, but they define different labels, scoring
interfaces, and ranking semantics.

Evaluation protocol can further change the conclusion drawn from the same
model family. Sampled metrics, target item sampling, and sampling strategies
for sequential recommendation have all been studied as sources of offline
evaluation sensitivity [@krichene2020sampled; @canamares2020target;
@dallmann2021sampling]. Baseline positioning carries a similar risk:
reproducibility and benchmark critiques show that conclusions about neural
recommenders can change when baselines and evaluation conditions are revisited
[@dacrema2019progress; @rendle2022ials]. For recommendation-tuned LLMs, these
concerns meet in a concrete way. Candidate difficulty determines what ranking
evidence means, and the amount of sequential supervision determines how an LLM
comparison with SASRec should be read.

This paper studies these issues through a controlled empirical analysis of
recommendation supervision semantics. The experiments separate Y preference
supervision from N next-item supervision, evaluate the M1 multi-task adapter as
a unified interface, compare Random-k5 with PopMatch-k5 and larger candidate
sets, and position SASRec under closest-exposure and high-exposure regimes.
MovieLens-1M provides the full evidence package, including multi-seed stability
and diagnostics. Amazon Musical Instruments provides seed42 cross-domain
validation for the main ranking-side directions, but it is not treated as
multi-seed cross-dataset evidence.

The contribution is a claim-traceable account of what different supervision
interfaces teach recommendation-tuned LLMs. The study shows that preference and
next-item supervision induce distinct capabilities, that multi-task tuning can
retain both interfaces while leaving specialist advantages, that harder
candidate protocols change ranking interpretations, and that LLM-vs-SASRec
comparisons must be stated in exposure-regime-specific terms. The paper does
not propose a new recommender architecture or claim universal LLM superiority;
it makes the evaluation boundaries part of the empirical result.
