# Current Task

## Stage Goal

Validate LlamaRec exposure scaling and convergence behavior for MovieLens-1M, then align follow-up comparisons against M1 and SASRec by actual per-task exposure.

## Scope

- Stage-local artifacts under `.agent/exposure_scaling/`.
- Training/evaluation launchers for cloud execution, including Phase2A k20/k50 current96 robustness checks.
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

- Cloud user-provided logs and metric tables for Y24/Y48/Y96, N24/N48/N96/N200, SASRec s23/s47/s94/s188/s391, M1-48, M1-96, and current96 k20/k50 robustness.
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

- Completed Y scaling through Y96. Y-as-ranker PopMatch ranking remains nearly flat through Y96, while Y-native binary validation shows weak mixed gains: AUC rises, Accuracy barely rises, and F1 drops from Y48 to Y96.
- Completed N scaling through N200. Validation keeps improving: N24 HR@1 0.5774, N48 0.6030, N96 0.6238, N200 0.6516.
- Confirmed M1 existing point is M1-12: 3000 steps, 12000 Y exposure, 12000 N exposure, total 24000.
- Completed fresh SASRec alignment runs for s23/s47/s94/s188/s391.
- Completed M1-48 and M1-96 validation/test PopMatch evaluations. Test metrics are report-only and do not change validation-first decisions.
- Validation-first matched comparisons show N-K0 beats SASRec at 24k/48k/96k/200k.
- Validation-first matched M1 comparisons show N48 narrowly beats M1-48, and N96 is effectively tied with M1-96 despite a tiny positive numerical gap for N.
- Completed Phase2A k20/k50 current96 validation/test robustness checks for N96 vs M1-96. PopMatch-k5 near parity does not fully generalize to larger candidate sets; N96 remains stronger under k20/k50, especially k20.
- Added a no-training Seed42 deep-analysis handoff script for prediction-level bootstrap, calibration, error overlap, ranking win/loss/tie, candidate protocol audit, slice analysis, exposure coverage, training curve export, claim evidence matrix, and multiseed recommendation. The script only reads existing artifacts and writes missing statuses when cloud prediction files are absent.
- Generated the no-training final evidence package under `.agent/exposure_scaling/final_evidence/`, including main tables, SASRec artifact index, claim matrix, revised claims, paper Results draft, discussion outline, multiseed decision, stage close readiness, and PNG/SVG figures. SASRec aligned runs are now traced to alignment artifacts and marked VERIFIED.

## Verification Results

- Y24 native binary validation: AUC 0.7761274819, F1 0.7791746032, Accuracy 0.7190856958.
- Y48 native binary validation: AUC 0.7816111073, F1 0.7848403087, Accuracy 0.7230433729.
- Y24->Y48 native binary validation deltas: AUC +0.0054836254, F1 +0.0056657055, Accuracy +0.0039576771.
- Y96 native binary validation: AUC 0.7843504067, F1 0.7783174665, Accuracy 0.7235279864.
- Y48->Y96 native binary validation deltas: AUC +0.0027392994, F1 -0.0065228422, Accuracy +0.0004846135.
- Y96 Y-as-ranker validation: HR@1 0.2211453744, NDCG@5 0.6030699894, MRR 0.4741791483.
- Y96 native binary test: AUC 0.7853511126, F1 0.7780238029, Accuracy 0.7221067221.
- Y96 Y-as-ranker test: HR@1 0.2065198238, NDCG@5 0.5921565513, MRR 0.4600528634.
- M1-96 minus Y96 native binary validation gaps: AUC +0.0024848682, F1 +0.0055253283, Accuracy +0.0046038285.
- M1-96 minus Y96 native binary report-only test gaps: AUC +0.0011326158, F1 +0.0055408528, Accuracy +0.0050242550.
- M1-96 native M-Y validation: AUC 0.7868352749, F1 0.7838427948, Accuracy 0.7281318149.
- N48 validation: HR@1 0.6029955947, NDCG@5 0.8200163654, MRR 0.7595418502.
- M1-48 validation: HR@1 0.5941850220, NDCG@5 0.8153243950, MRR 0.7533392070.
- N48 minus M1-48 validation gaps: HR@1 +0.0088105727, NDCG@5 +0.0046919704, MRR +0.0062026432.
- N96 validation: HR@1 0.6237885463, NDCG@5 0.8302923694, MRR 0.7732422907.
- M1-96 validation: HR@1 0.6234361233, NDCG@5 0.8291402759, MRR 0.7717533040.
- N96 minus M1-96 validation gaps: HR@1 +0.0003524229, NDCG@5 +0.0011520935, MRR +0.0014889868.
- N96 minus M1-96 report-only test gaps: HR@1 +0.0126872247, NDCG@5 +0.0056658345, MRR +0.0075535977.
- SASRec matched validation gaps remain positive for N-K0 at 24k/48k/96k/200k.
- Current96 k20/k50 validation robustness: N96 beats M1-96 on k20 by HR@1 +0.1124229075, NDCG@5 +0.1269794216, MRR +0.1062560801; on k50 by HR@1 +0.0170925110, NDCG@5 +0.0289555766, MRR +0.0258293602.
- Current96 k20/k50 report-only test robustness: N96 beats M1-96 on k20 by HR@1 +0.1147136564, NDCG@5 +0.1259325434, MRR +0.1058693094; on k50 by HR@1 +0.0139207048, NDCG@5 +0.0277780808, MRR +0.0234179986.
- Final coverage summary reports no expected metrics gaps.
- Local verification for the no-training handoff script: `python -m py_compile .agent/exposure_scaling/alignment/commands/seed42_deep_analysis.py` passed; dry run with `--bootstrap-replicates 5` completed against local partial artifacts and produced explicit MISSING statuses for cloud-only prediction files.
- Local verification for final evidence package: `python -m py_compile .agent/exposure_scaling/final_evidence/build_final_evidence.py` passed; package generation completed; required tables/docs/figures were created; PNG files have non-empty dimensions and pixel variation.

## Unresolved Questions

- Should M1-200 be skipped as too expensive, or run as an endpoint/crossover check? Current recommendation: skip unless essential for the final paper claim.
- Is multi-seed validation needed for the near-tie N96 vs M1-96 result?
- No experimental blocker remains for a seed42 descriptive Results draft. Multiseed remains recommended for stronger generalization claims, but is not required for the current evidence freeze. M1-200 remains deferred unless the paper's central claim requires it.

## Pending Wiki Sync

- Potential report update: record validation-first Y/N exposure scaling outcomes and the decision to stop blind N single-seed scaling beyond 200k.
- Potential guide update: document cloud-local model path/offline preflight practice for LlamaRec training launchers.
- Potential report update after approval and completion: add M1/SASRec matched-exposure alignment findings.
- Potential report update: clarify that Y scaling was only paused by Y-as-ranker PopMatch evidence until Y-native binary metrics are summarized.

## Invalidating Conditions

- Cloud runs used a different model path, task ratio, batch size, gradient accumulation, candidate set, or random seed than recorded here.
- M1 resume checkpoint lacks optimizer/scheduler/RNG state and the continuation is not a true resume.
- Candidate files differ from the explicitly named protocol for the claim: `k5_popmatch_seed42` for PopMatch claims, or `k20_seed42`/`k50_seed42`/`k20_perm_seed43` for Phase2A robustness claims.
