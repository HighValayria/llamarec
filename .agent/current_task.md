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
- Y-native convergence must be judged with binary AUC/F1/Accuracy; PopMatch ranking for Y is a Y-as-ranker bridge metric, not the native Y objective.
- SASRec aligned accounting uses batch size 512, no gradient accumulation, and processed-example exposure.

## Evidence Sources

- Cloud user-provided logs and metric tables for Y24/Y48, N24/N48/N96/N200, SASRec s23/s47/s94/s188/s391, M1-48, and M1-96.
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

- Completed Y scaling through Y48. Y-as-ranker PopMatch ranking is flat from Y24 to Y48, but Y-native binary validation still rises slightly, so pure Y96 is conditional rather than dismissed.
- Completed N scaling through N200. Validation keeps improving: N24 HR@1 0.5774, N48 0.6030, N96 0.6238, N200 0.6516.
- Confirmed M1 existing point is M1-12: 3000 steps, 12000 Y exposure, 12000 N exposure, total 24000.
- Completed fresh SASRec alignment runs for s23/s47/s94/s188/s391.
- Completed M1-48 and M1-96 validation-only PopMatch evaluations. M1 report-only test metrics are still missing and should be run only after validation decisions are frozen.
- Validation-first matched comparisons show N-K0 beats SASRec at 24k/48k/96k/200k.
- Validation-first matched M1 comparisons show N48 narrowly beats M1-48, and N96 is effectively tied with M1-96 despite a tiny positive numerical gap for N.

## Verification Results

- Y24 native binary validation: AUC 0.7761274819, F1 0.7791746032, Accuracy 0.7190856958.
- Y48 native binary validation: AUC 0.7816111073, F1 0.7848403087, Accuracy 0.7230433729.
- Y24->Y48 native binary validation deltas: AUC +0.0054836254, F1 +0.0056657055, Accuracy +0.0039576771.
- M1-96 native M-Y validation: AUC 0.7868352749, F1 0.7838427948, Accuracy 0.7281318149.- N48 validation: HR@1 0.6029955947, NDCG@5 0.8200163654, MRR 0.7595418502.
- M1-48 validation: HR@1 0.5941850220, NDCG@5 0.8153243950, MRR 0.7533392070.
- N48 minus M1-48 validation gaps: HR@1 +0.0088105727, NDCG@5 +0.0046919704, MRR +0.0062026432.
- N96 validation: HR@1 0.6237885463, NDCG@5 0.8302923694, MRR 0.7732422907.
- M1-96 validation: HR@1 0.6234361233, NDCG@5 0.8291402759, MRR 0.7717533040.
- N96 minus M1-96 validation gaps: HR@1 +0.0003524229, NDCG@5 +0.0011520935, MRR +0.0014889868.
- SASRec matched validation gaps remain positive for N-K0 at 24k/48k/96k/200k.

## Unresolved Questions

- Should pure Y96 be run for fair Y-native comparison against M1-96? Current evidence supports it only conditionally: Y-native binary rises slightly, while Y-as-ranker ranking is flat.
- Should M1-200 be skipped as too expensive, or run as an endpoint/crossover check?
- Is multi-seed validation needed for the near-tie N96 vs M1-96 result?

## Pending Wiki Sync

- Potential report update: record validation-first Y/N exposure scaling outcomes and the decision to stop blind N single-seed scaling beyond 200k.
- Potential guide update: document cloud-local model path/offline preflight practice for LlamaRec training launchers.
- Potential report update after approval and completion: add M1/SASRec matched-exposure alignment findings.
- Potential report update: clarify that Y scaling was only paused by Y-as-ranker PopMatch evidence until Y-native binary metrics are summarized.

## Invalidating Conditions

- Cloud runs used a different model path, task ratio, batch size, gradient accumulation, candidate set, or random seed than recorded here.
- M1 resume checkpoint lacks optimizer/scheduler/RNG state and the continuation is not a true resume.
- Candidate files differ from fixed `k5_popmatch_seed42` validation/test paths.
