# Seed42 Plan

## Status

Prepared only. Do not execute GPU jobs until strict preprocessing and candidate
construction pass.

## Dataset

```text
amazon-musical-instruments
```

## Model Matrix

| Model | Binary | Random-k5 | PopMatch-k5 |
|---|---|---|---|
| Base | yes | yes | yes |
| Y-K0 | yes | P(Yes) ranking | P(Yes) ranking |
| N-K0 | no | candidate-label ranking | candidate-label ranking |
| M1 | M-Y | M-N | M-N |
| SASRec-exp-match | no | candidate ranking | candidate ranking |

## Candidate Seeds

- random candidate seed: 42
- popmatch candidate seed: 42
- model train seed: 42

Candidate files must remain fixed across any later seed43/44 runs.
Candidate negatives should be drawn from retained observed interaction items,
not from metadata-only ASINs.

## SASRec Exposure

Do not reuse the MovieLens `s23` value. Compute SASRec optimizer steps after
N-K0 actual N-task exposure is known:

```text
target_n_exposure = N-K0 optimizer_steps * N-K0 effective_batch
sasrec_steps = round(target_n_exposure / 512)
actual_sasrec_exposure = sasrec_steps * 512
relative_mismatch = (actual_sasrec_exposure - target_n_exposure) / target_n_exposure
```

If mismatch is not zero, report it as approximately exposure matched.

## GPU Runs After CPU Gate

1. Base inference on Y and N cohorts.
2. Y-K0 training and evaluation.
3. N-K0 training and evaluation.
4. M1 training and evaluation.
5. SASRec closest-exposure training and evaluation.

No seed43/44 runs should start until seed42 synthesis is reviewed.
