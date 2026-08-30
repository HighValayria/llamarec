# M1 Exposure Plan

Date: 2026-08-30

## Target Grid

| label | optimizer steps | Y exposure | N exposure | total exposure | relation to current M1-12 |
|---|---:|---:|---:|---:|---|
| M1-12 | 3000 | 12000 | 12000 | 24000 | existing |
| M1-48 | 12000 | 48000 | 48000 | 96000 | resume +9000 steps |
| M1-96 | 24000 | 96000 | 96000 | 192000 | conditional after M1-48 |
| M1-200 | 50000 | 200000 | 200000 | 400000 | expensive, conditional |

## Recommendation

Run M1-48 first, not M1-96/M1-200 immediately.

Reason:

- The current question is whether the old `N-K0 > M1` conclusion survives once M1 receives the same N-task exposure as N48.
- M1-48 is the smallest new M1 point that aligns with a completed N curve point with reliable validation metrics.
- M1-200 would require 47000 additional optimizer steps from the current M1 checkpoint and should only be justified after M1-48 shows that multitask training is catching up.

## Runtime Estimate

Based on recent LLM training logs on the cloud GPU, use a conservative 5-8 seconds per optimizer step for planning.

| job | additional steps | rough train time | eval time note | total planning estimate |
|---|---:|---:|---|---:|
| M1-48 from checkpoint-3000 | 9000 | 12.5-20 h | M1 evaluates both Y and N interfaces; budget several hours | 16-24 h |
| M1-96 from M1-48 | 12000 | 17-27 h | only if M1-48 warrants it | 22-34 h |
| M1-200 from M1-96 | 26000 | 36-58 h | expensive final check | 42-68 h |
| M1-200 direct from checkpoint-3000 | 47000 | 65-104 h | not recommended first | 75-115 h |

## Decision Rule

Use validation metrics first.

- Compare N48 validation against M1-48 validation on the N interface.
- M1 test metrics are report-only after the validation decision is fixed.
- If M1-48 remains clearly behind N48, do not run M1-96/M1-200 by default.
- If M1-48 narrows the gap enough to affect the claim, then run M1-96 next.
