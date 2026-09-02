# Resolved Cloud Commands

Date: 2026-08-30

First round does not start GPU. The commands below are for after explicit approval on the cloud machine.

## 1. Sync Code

```bash
cd /root/llamarec && git pull --ff-only
```

## 2. Inventory SASRec Without Starting Training

```bash
cd /root/llamarec && bash .agent/exposure_scaling/alignment/commands/sasrec_commands.sh inventory
```

## 3. Run Minimum SASRec Alignment Batch

This runs with nohup and tails the log. Pressing Ctrl-C stops tail only, not the job.

```bash
cd /root/llamarec && bash .agent/exposure_scaling/alignment/commands/sasrec_commands.sh launch_minimal
```

Expected content:

- Train/evaluate fresh aligned s23/s47/s94/s188/s391 runs.
- Do not reuse old s23/s47 model dirs for eval-only if their `mappings.json` lacks current candidate/history items.
- Keep existing s1500/s3000 PopMatch eval metrics as repeated-exposure anchors, not matched-exposure comparators.

Planning estimate: usually much cheaper than LLM jobs; budget roughly 0.5-2 h including evaluation, but the inventory output should be trusted over this estimate.

## 4. Run Recommended M1-48 Only

This resumes from M1 checkpoint-3000, runs to step 12000, then evaluates validation/test.

```bash
cd /root/llamarec && bash .agent/exposure_scaling/alignment/commands/m1_commands.sh launch_m1_48
```

Planning estimate: 16-24 h total including evaluation.

## 5. Progress Checks

Latest M1 log:

```bash
cd /root/llamarec && LOG=$(ls -t logs/exposure_scaling/m1_48_train_then_eval_*.log 2>/dev/null | head -n 1); echo "LOG=$LOG"; test -n "$LOG" && tail -n 80 -f "$LOG"
```

Latest SASRec alignment log:

```bash
cd /root/llamarec && LOG=$(ls -t logs/exposure_scaling/sasrec_alignment_minimal_*.log 2>/dev/null | head -n 1); echo "LOG=$LOG"; test -n "$LOG" && tail -n 80 -f "$LOG"
```
## 6. Run M1-96 With Internal Eval Disabled

This resumes from `exposure_m1_s12000/checkpoints/checkpoint-12000`, trains to step 24000, saves the adapter, then runs validation-only PopMatch.

```bash
cd /root/llamarec && git pull --ff-only
cd /root/llamarec && bash -n .agent/exposure_scaling/alignment/commands/m1_commands.sh
cd /root/llamarec && bash .agent/exposure_scaling/alignment/commands/m1_commands.sh launch_m1_96
```

Planning estimate after disabling internal eval: 18-24 h total.

## 7. Summarize Evaluation Coverage Before Y96

This is CPU-only and reads existing metrics JSON files. Use it before deciding whether pure Y96 is worth the GPU cost.

```bash
cd /root/llamarec && git pull --ff-only
cd /root/llamarec && python .agent/exposure_scaling/alignment/commands/eval_coverage_summary.py
```

Decision rule: if Y24->Y48 native binary validation AUC/F1/Accuracy still rises meaningfully, run Y96; if binary is flat and Y-as-ranker ranking is flat, skip Y96.

## 8. Conditional Pure Y96 Continuation

This resumes pure Y-K0 from `exposure_y_s6000/checkpoints/checkpoint-6000`, disables Trainer internal eval, trains to 12000 steps, then runs validation-only PopMatch evaluation.

```bash
cd /root/llamarec && git pull --ff-only
cd /root/llamarec && bash .agent/exposure_scaling/alignment/commands/y_commands.sh summary
cd /root/llamarec && bash .agent/exposure_scaling/alignment/commands/y_commands.sh launch_y96
```

Planning estimate: roughly half of M1-48->M1-96 continuation because it adds 6000 optimizer steps instead of 12000, plus about 25-35 minutes for validation-only Y evaluation. On the observed 24 GB class GPU speed, budget about 9-13 hours total.

## 9. Report-Only M1 Test Evaluation

Run this only after validation-based training decisions are frozen. It fills the missing M1-48 and M1-96 test metrics without retraining.

```bash
cd /root/llamarec && git pull --ff-only
cd /root/llamarec && bash .agent/exposure_scaling/alignment/commands/m1_commands.sh launch_m1_tests
```

Planning estimate: about 30 minutes for M1-48 test plus 30 minutes for M1-96 test on the observed 24 GB class GPU, because each test split has 11544 binary prompts and 5675 ranking candidate records.
