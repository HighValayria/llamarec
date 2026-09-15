# ICECAI 2026 Submission Layer

This dedicated layer inherits the tested generic IEEE adapter and adds ICECAI pre-final metadata, reference-recency validation, country-source evidence, author validation, and an optional user-supplied disclosure insertion point.

The default `prefinal_placeholder` mode is for layout review only. It produces `VENUE_ADAPTED_PRE_FINAL`, not a submission-ready PDF.

```powershell
python paper/submission/icecai_2026/build_submission.py --lang en --compile
python paper/submission/icecai_2026/build_submission.py --lang bilingual --compile
```
