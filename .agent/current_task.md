# Current Task

## Stage Goal
- Active stage: LLM Exposure Scaling & Convergence Validation.
- Determine whether current low-exposure LLM checkpoints are undertrained, whether Y/N/M relative conclusions survive larger task-sample exposure, and how N-K0 compares with SASRec along a performance-vs-exposure frontier.
- Paper Writing / Submission Package is paused, not completed, because manuscript drafting exposed a claim-relevant training-exposure / convergence gap.
- Current milestone is cloud execution readiness: keep exposure accounting fixed, run cloud jobs through git-synced scripts, and collect validation-first metrics before deciding whether to extend to 96k.

## Scope
- MovieLens-1M only, seed42 first.
- Stage-local artifacts under `.agent/exposure_scaling/`.
- Existing code, configs, formal data files, stage-local result artifacts, and authorized one-time relevant wiki context.
- Y-K0, N-K0, M1, and SASRec exposure accounting and scaling plan.

## Non-Goals
- No untracked/manual GPU commands; cloud runs should use the git-synced `.agent/exposure_scaling/commands/gpu_batch1_train_nohup.sh` and `.agent/exposure_scaling/commands/gpu_batch1_eval_nohup.sh` launchers.
- No Amazon scaling in the first round.
- No new model architecture, KAR, hard negatives, new candidate protocol, third dataset, LoRA sweep, 7B, MovieLens-32M, strict FLOPs matching, or direct million-exposure LLM run.
- Do not directly modify formal `wiki/` during this stage.

## Long-Term Constraints
- Primary x-axis is task-sample exposure: task training examples actually consumed during optimization.
- Do not describe this as compute scaling, FLOPs scaling, token scaling, or wall-clock scaling.
- Main evaluation protocol stays fixed to MovieLens-1M PopMatch-k5 `k5_popmatch_seed42`; Random-k5 is supplementary only.
- Training protocol should isolate exposure/max_steps while keeping base model, QLoRA config, LR, scheduler, prompt, candidate protocol, and inference fixed.
- Test metrics must not guide ad hoc training-budget tuning; validation behavior should drive adaptive continuation where possible.

## Evidence Sources
- User migration directive on 2026-08-24 for LLM Exposure Scaling & Convergence Validation; it explicitly authorized a one-time, directly relevant wiki read.
- One-time stage-start wiki read on 2026-08-24: `wiki/index.md`, `wiki/current_state.md`, `wiki/reports/fair-budget-baseline-positioning.md`, `wiki/reports/sample-efficiency-training-efficiency.md`, `wiki/reports/multiseed-stability.md`, and `wiki/reports/paper-result-consolidation.md`.
- The wiki context was compressed into `.agent/exposure_scaling/stage_context.md`; direct wiki read access is revoked for the rest of the stage.
- Current code/config evidence from `configs/experiment.yaml`, `configs/y.yaml`, `configs/n.yaml`, `configs/m.yaml`, `src/train/train_y.py`, `src/train/train_n.py`, `src/train/train_m.py`, `src/train/preference_dataset.py`, `src/train/next_item_dataset.py`, `src/train/multitask_dataset.py`, `src/baselines/sasrec.py`, `src/analysis/training_budget_audit.py`, and `src/analysis/sample_efficiency_curve.py`.
- Formal local data counts from `data/processed/movielens-1m/stats.json`, `preference_train.jsonl`, `next_item_train.jsonl`, and fixed PopMatch candidate files.

## Related Code
- `configs/experiment.yaml`
- `configs/y.yaml`
- `configs/n.yaml`
- `configs/m.yaml`
- `src/train/train_y.py`
- `src/train/train_n.py`
- `src/train/train_m.py`
- `src/train/multitask_dataset.py`
- `src/baselines/sasrec.py`
- `src/analysis/training_budget_audit.py`
- `src/analysis/sample_efficiency_curve.py`

## Current Progress
- New stage opened and Paper Writing routed to paused/waiting-for-evidence.
- Focused wiki context read once, compressed, and revoked.
- Data pool audit confirms MovieLens-1M has 976,284 Y train samples and 212,725 N train samples. Formal capped training pools are 200,000 samples per task for the audited LLM/SASRec rows.
- Current Y-K0 and N-K0 1500-step anchors each correspond to 12,000 task-sample exposure with effective batch 8.
- Current M1 3000-step anchor corresponds to 24,000 total exposure split as 12,000 Y + 12,000 N under the 1:1 sequential schedule.
- Existing N-K0 curve has 3k, 6k, 12k, 24k, 48k, and now cloud-validated 96k PopMatch-k5 points; 200k near-full-pool is the next validation-approved continuation.
- Existing SASRec curve already has 3,072, 6,144, 11,776, 24,064, 767,424, and 1,534,656 N-task exposure points; 48k, 96k, and near-200k aligned points are missing.
- User-provided cloud inventory confirms Y-K0/N-K0/M1 checkpoints include trainer, optimizer, scheduler, RNG, and training args state; strict resume is available at the inspected anchors.
- User-provided cloud shell evidence on 2026-08-28 shows the base model exists at `models/Llama-3.2-3B-Instruct`; batch scripts now use repo-local model configs instead of the default Hugging Face repo id.
- Cloud batch1 training and evaluation completed. Validation-first result: stop Y at 48k; continue N from 48k to 96k.
- N96 cloud training and evaluation completed. Validation-first result: continue N from 96k to near-full-pool 200k.

## Verification Results
- No GPU job was started.
- Local code audit found LLM TrainingArguments do not explicitly set `lr_scheduler_type`; Transformers default scheduler is total-step-dependent unless the cloud environment proves otherwise. Resume from an existing checkpoint is therefore preferred to changing `max_steps` from scratch.
- M1 uses `SequentialSampler` over an explicitly interleaved Y/N dataset, making per-task exposure accounting deterministic under single-process training.
- SASRec exposure accounting uses the implemented training loop, including the short final batch in each 200,000-sample epoch.

## Unresolved Questions
- Do the formal cloud checkpoints contain `trainer_state.json`, `optimizer.pt`, `scheduler.pt`, and RNG state files at the exact resume point?
- Were the formal LLM runs single-process world size 1 as expected from the configured single-RTX-4090 profile?
- Are validation PopMatch metrics already available for existing 12k/24k N-K0 points, or must they be generated before adaptive stopping?
- Exact GPU hours are not recoverable from local artifacts; estimates need cloud log calibration.
- Token exposure diagnostics are not yet available because formal `encoded_dataset_summary.json` files are not local.

## Pending Wiki Sync
- No formal wiki edits during the stage.
- Proposed stage-end durable sync should be limited to final exposure accounting, convergence finding, stable model comparison, and paper claim revisions after explicit one-time write authorization.

## Invalidating Conditions
- Running GPU jobs outside the git-synced nohup scripts or without preserving logs.
- Claiming N-K0 has plateaued before inspecting N200 validation, or claiming Y benefits from 96k/200k despite 24k->48k validation stagnation.
- Comparing N-K0 X total samples against M1 X total samples instead of matching M1 at X N + X Y exposure.
- Treating high-exposure SASRec as evidence against high-exposure LLM without a matched or clearly separated high-exposure LLM point.
- Reading formal wiki again without renewed authorization.
