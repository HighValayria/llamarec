# Current Task

## Stage Goal

Validate LlamaRec exposure scaling and convergence behavior for MovieLens-1M, then align follow-up comparisons against M1 and SASRec by actual per-task exposure.

## Scope

- Stage-local artifacts under `.agent/exposure_scaling/`.
- Training/evaluation launchers for cloud execution.
- Configs and code paths needed for Y-K0, N-K0, M1, and SASRec exposure accounting.
- Validation-first comparison protocol using fixed PopMatch-k5 seed42 candidates.

## Non-Goals

- Do not read or modify the formal `wiki/` during the active stage.
- Do not claim convergence from test metrics.
- Do not run blind single-seed N-K0 beyond 200k as part of the current minimum plan.

## Long-Term Constraints

- Validation metrics decide continuation; test metrics are report-only after decisions are fixed.
- For LLM runs, effective exposure is `per_device_train_batch_size * gradient_accumulation_steps * world_size * optimizer_steps`.
- Current formal LLM runs use `per_device_train_batch_size=1`, `gradient_accumulation_steps=8`, `world_size=1`, so effective batch is 8 examples per optimizer step.
- M1 uses 1:1 Y/N task sampling; with the current effective batch 8, each optimizer step consumes 4 Y and 4 N examples.
- SASRec aligned accounting uses batch size 512, no gradient accumulation, and processed-example exposure.

## Evidence Sources

- Cloud user-provided logs and metric tables for Y24/Y48, N24/N48/N96/N200, SASRec s23/s47/s94/s188/s391, and M1-48.
- `.agent/exposure_scaling/exposure_accounting.json`.
- `.agent/exposure_scaling/alignment/` artifacts.
- Current code in `src/train/train_m.py`, `src/train/multitask_dataset.py`, `src/inference/evaluate_m_adapter.py`, `src/baselines/sasrec.py`, and `src/analysis/training_budget_audit.py`.

## Related Code

- `src/train/train_y.py`
- `src/train/train_n.py`
- `src/train/train_m.py`
- `src/train/multitask_dataset.py`
- `src/inference/evaluate_n_adapter.py`
- `src/inference/evaluate_m_adapter.py`
- `src/baselines/sasrec.py`
- `src/analysis/training_budget_audit.py`
- `configs/y_local_model.yaml`
- `configs/n_local_model.yaml`
- `configs/m_local_model.yaml`

## Current Progress

- Completed Y scaling through Y48 and stopped Y because validation does not improve meaningfully.
- Completed N scaling through N200. Validation keeps improving: N24 HR@1 0.5774, N48 0.6030, N96 0.6238, N200 0.6516.
- Confirmed M1 existing point is M1-12: 3000 steps, 12000 Y exposure, 12000 N exposure, total 24000.
- Completed fresh SASRec alignment runs for s23/s47/s94/s188/s391.
- Completed M1-48 validation-only PopMatch evaluation.
- Preparing M1-96 continuation with Trainer internal eval disabled; only validation-only PopMatch should run after adapter save.
- Validation-first matched comparisons show N-K0 beats SASRec at 24k/48k/96k/200k.
- Validation-first matched comparison also shows N48 beats M1-48, but the gap is small.

## Verification Results

- N48 validation: HR@1 0.6029955947, NDCG@5 0.8200163654, MRR 0.7595418502.
- M1-48 validation: HR@1 0.5941850220, NDCG@5 0.8153243950, MRR 0.7533392070.
- N48 minus M1-48 validation gaps: HR@1 +0.0088105727, NDCG@5 +0.0046919704, MRR +0.0062026432.
- SASRec matched validation gaps remain positive for N-K0 at 24k/48k/96k/200k.

## Unresolved Questions

- Does M1-96 close or reverse the small N-vs-M1 gap seen at 48k?
- After M1-96 validation, should M1-200 be skipped or used as an expensive endpoint?

## Pending Wiki Sync

- Potential report update: record validation-first Y/N exposure scaling outcomes and the decision to stop blind N single-seed scaling beyond 200k.
- Potential guide update: document cloud-local model path/offline preflight practice for LlamaRec training launchers.
- Potential report update after approval and completion: add M1/SASRec matched-exposure alignment findings.

## Invalidating Conditions

- Cloud runs used a different model path, task ratio, batch size, gradient accumulation, candidate set, or random seed than recorded here.
- M1 resume checkpoint lacks optimizer/scheduler/RNG state and the continuation is not a true resume.
- Candidate files differ from fixed `k5_popmatch_seed42` validation/test paths.
