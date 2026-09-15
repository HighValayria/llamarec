# GenAI Disclosure Input Required

Supply the disclosure manually in `paper/submission/icecai_2026/submission_config.yaml`, under `genai_disclosure.text`, then set `genai_disclosure.enabled: true`.

The venue adapter renders the supplied text in an unnumbered disclosure section immediately before References. Rebuild with:

```powershell
python paper/submission/icecai_2026/build_submission.py --lang en --mode submission --compile
```
