# Protocol Terminology

## Binary Metrics

- `AUC`: threshold-free binary ranking metric.
- `F1 @ fixed 0.5`: diagnostic threshold setting only.
- `validation-calibrated F1`: threshold selected on validation and then fixed
  for test; preferred main-text F1.

Do not mix fixed-threshold F1 and validation-calibrated F1 in the same row
without a threshold column.

## Ranking Protocols

- `Canonical Random-k5`: original random 5-candidate N evaluation.
- `PopMatch-k5`: fixed `k5_popmatch_seed42` candidate files; preferred main
  hard-candidate ranking comparison.
- `Candidate-size Robustness k20`: explicit `k20_seed42` candidate variant.
- `Candidate-size Robustness k50`: explicit `k50_seed42` candidate variant.
- `Order Perturbation`: `k5_perm_seed43` or `k20_perm_seed43`; diagnostic
  because observed effects are small relative to candidate-size expansion.

Every ranking table must include candidate protocol, candidate size, negative
sampling type, and candidate seed or file.

## SASRec Budget Regimes

- `Optimizer-step-aligned diagnostic`: useful historical diagnostic, not fair
  sample-exposure evidence.
- `Closest N-task sample exposure`: preferred sample-efficiency comparison;
  use "approximately matched" or "closest available exposure" when mismatch is
  nonzero.
- `High-exposure SASRec`: shows that a specialized sequential model can exceed
  N-K0 with substantially more N-task exposure.

Do not use bare names such as `SASRec s1500` or `SASRec s3000` as paper-level
interpretive labels without the budget regime.
