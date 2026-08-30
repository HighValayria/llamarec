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

- Evaluate existing s23/s47 if model dirs exist.
- Evaluate high repeated anchors s1500/s3000 if model dirs exist.
- Train/evaluate s94, s188, s391 if their alignment outputs are absent.

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
