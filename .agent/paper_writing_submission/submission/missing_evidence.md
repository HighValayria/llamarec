# Missing Evidence

## Non-blocking Gaps

### Amazon validation-calibrated binary metrics

Amazon seed42 outputs include binary AUC/F1/Accuracy for Base, Y-K0, and M1,
but the validation-calibrated threshold protocol is not documented for Amazon.

Impact: do not use Amazon as strong binary-calibration evidence. The main
cross-dataset ranking and sample-exposure conclusions remain usable.

Optional proposal if needed: run low-cost validation/test binary evaluation
with existing Amazon Y-K0 and M1 adapters. Requires user approval.

### Amazon seed43/44

Amazon N-K0 exceeds M1 on PopMatch-k5, but the margin is narrow and seed42-only.

Impact: use cautious wording. Not blocking unless the final paper elevates
cross-dataset N-K0 > M1 to a very strong claim.

Optional proposal if needed: only run Amazon N-K0 and M1 on PopMatch-k5 for
seed43/44. Do not default to Base/Y/SASRec/Random.

### Strict compute matching

Strict FLOPs/wall-clock/capacity matching is absent.

Impact: limitation/future work. Current paper can use budget-regime and
sample-exposure language.

### Related Work citations

Current stage has not yet performed citation retrieval or source verification.

Impact: Related Work cannot be drafted as final prose until evidence-driven
writing/literature review stage is run.

## Draft v0 Decision

No missing evidence currently blocks a complete empirical paper draft. The two
most useful optional patches are validation-calibrated Amazon binary evaluation
from existing adapters, if the paper needs a strong cross-dataset preference
claim, and Amazon PopMatch seed43/44 for N-K0 and M1, if the narrow seed42
margin is judged too fragile for the target venue.

Neither patch should run without explicit user approval.
