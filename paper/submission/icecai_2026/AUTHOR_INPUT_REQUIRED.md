# Author Input Required

Edit `paper/submission/icecai_2026/submission_config.yaml`, under `authors`.

For every author, fill `name`, `department`, `institution`, `city`, `country`, `email`, and `corresponding`. Author order is significant. Set `corresponding: true` for exactly one author; the adapter adds `*` to that name and requires the corresponding email.

Rebuild with:

```powershell
python paper/submission/icecai_2026/build_submission.py --lang en --mode submission --compile
```
