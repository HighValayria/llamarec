# Local Audit Commands

Commands already used locally:

```powershell
(Get-Content -LiteralPath 'data\processed\movielens-1m\preference_train.jsonl' | Measure-Object -Line).Lines
(Get-Content -LiteralPath 'data\processed\movielens-1m\next_item_train.jsonl' | Measure-Object -Line).Lines
(Get-Content -LiteralPath 'data\candidates\movielens-1m\variants\k5_popmatch_seed42\test.jsonl' | Measure-Object -Line).Lines
Get-Content -LiteralPath '.agent\sample_efficiency_training_efficiency\final_curve\sample_efficiency_curve.csv'
```

Stage guard before handoff:

```powershell
python tools\stage_guard.py
```
