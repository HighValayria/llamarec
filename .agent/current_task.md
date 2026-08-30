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
- Do not start new GPU work in the first M1/SASRec alignment planning round.
- Do not claim convergence from test metrics.
- Do not run blind single-seed N-K0 beyond 200k as part of the current minimum plan.

## Long-Term Constraints

- Validation metrics decide continuation; test metrics are report-only after decisions are fixed.
- For LLM runs, effective exposure is `per_device_train_batch_size * gradient_accumulation_steps * world_size * optimizer_steps`.
- Current formal LLM runs use `per_device_train_batch_size=1`, `gradient_accumulation_steps=8`, `world_size=1`, so effective batch is 8 examples per optimizer step.
- M1 uses 1:1 Y/N task sampling; with the current effective batch 8, each optimizer step consumes 4 Y and 4 N examples.
- SASRec aligned accounting uses batch size 512, no gradient accumulation, and processed-example exposure.

## Evidence Sources

- Cloud user-provided logs and metric tables for Y24/Y48 and N24/N48/N96/N200.
- `.agent/exposure_scaling/exposure_accounting.json`.
- `.agent/exposure_scaling/seed42/m1_curve.csv`.
- `.agent/exposure_scaling/sasrec_existing_curve.csv`.
- `.agent/sample_efficiency_training_efficiency/final_curve/sample_efficiency_curve.csv`.
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

- Confirmed the earlier 12k exposure inference: 1500 LLM optimizer steps times effective batch 8 equals 12000 examples.
- Confirmed actual cloud LLM settings from trainer state: per-device batch 1, gradient accumulation 8, world size 1.
- Added cloud-local model configs using `models/Llama-3.2-3B-Instruct` to avoid accidental Hugging Face resolution/download attempts.
- Added and pushed nohup/offline/preflight scripts for Y/N scaling and N96/N200 continuations.
- Completed Y scaling through Y48 and stopped Y because validation does not improve meaningfully.
- Completed N scaling through N200. Validation keeps improving: N24 HR@1 0.5774, N48 0.6030, N96 0.6238, N200 0.6516.
- Started M1 + SASRec alignment planning without launching GPU jobs.
- Confirmed M1 existing point is M1-12: 3000 steps, 12000 Y exposure, 12000 N exposure, total 24000.
- Confirmed M1 matched N-task exposure targets: M1-48 = 12000 steps, M1-96 = 24000 steps, M1-200 = 50000 steps.
- Confirmed SASRec aligned targets with batch 512: s23 ~= 12k, s47 ~= 24k, s94 ~= 48k, s188 ~= 96k, s391 = 200k.
- Created alignment artifacts under `.agent/exposure_scaling/alignment/` with audit, plans, tables, and guarded cloud command scripts.

## Verification Results

- Y-K0 validation:
  - Y24 HR@1 0.2156828194, NDCG@5 0.6002715889, MRR 0.4704082232.
  - Y48 HR@1 0.2165638767, NDCG@5 0.5994649797, MRR 0.4694772394.
- N-K0 validation:
  - N24 HR@1 0.5774449339, NDCG@5 0.8067686847, MRR 0.7420058737.
  - N48 HR@1 0.6029955947, NDCG@5 0.8200163654, MRR 0.7595418502.
  - N96 HR@1 0.6237885463, NDCG@5 0.8302923694, MRR 0.7732422907.
  - N200 HR@1 0.6516299559, NDCG@5 0.8431902590, MRR 0.7904170338.
- N validation deltas remain positive through N200.
- SASRec currently has known test-only curve entries for s6/s12/s23/s47/s1500/s3000 in stage-local artifacts; cloud inventory is still needed for actual model directories and validation files.

## Unresolved Questions

- Which SASRec model directories are present on the cloud for s23/s47/s1500/s3000?
- Do existing SASRec points already have validation metrics on the cloud, or must they be re-evaluated?
- How close is M1-48 to N48 under validation-first comparison?
- Should M1-96 be run after M1-48, or does M1-48 already settle the claim?

## Pending Wiki Sync

- Potential report update: record validation-first Y/N exposure scaling outcomes and the decision to stop blind N single-seed scaling beyond 200k.
- Potential guide update: document cloud-local model path/offline preflight practice for LlamaRec training launchers.
- Potential report update after approval and completion: add M1/SASRec matched-exposure alignment findings.

## Invalidating Conditions

- Cloud runs used a different model path, task ratio, batch size, gradient accumulation, candidate set, or random seed than recorded here.
- M1 resume checkpoint lacks optimizer/scheduler/RNG state and the continuation is not a true resume.
- SASRec existing checkpoints cannot be found, requiring fresh reruns of supposed existing points.
- Candidate files differ from fixed `k5_popmatch_seed42` validation/test paths.
