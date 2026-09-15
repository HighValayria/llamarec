# ICECAI 2026 GPT6 P1 Closure Evidence Packet

## A. Original P1-01

Y and N use different holdout rules. The prior manuscript established within-task temporal history but did not establish that one M1 training branch was isolated from the other task's validation/test targets. The submission-level question was whether the shared-model ranking evidence preserved cross-task holdout integrity.

## B. Current cross-task-safe evaluation protocol

> To ensure cross-task holdout integrity for the shared adapter, M1-N comparisons are restricted to a cross-task-safe subset of N evaluation examples. For an example e=(u,t), we retain it only when its target was not consumed as an M1 Y-training target, did not enter the history of any later M1 Y-training example, and no M1 Y-training target for user u has a timestamp at or after t. The M1 N-training branch has 0 target or history overlap with the retained N holdouts. N and M1-N are evaluated on exactly the same retained examples. Training follows the task-specific streams; this additional criterion is an evaluation-side restriction, not a joint temporal cutoff used during training.

## C. Coverage

| Operating point | Split | Retained/full | Coverage |
| --- | --- | ---: | ---: |
| M1-48 | validation | 5,494/5,675 | 96.81% |
| M1-48 | test | 5,600/5,675 | 98.68% |
| M1-96 | validation | 5,318/5,675 | 93.71% |
| M1-96 | test | 5,535/5,675 | 97.53% |

## D. Common-safe seed42 comparison

- Validation common-safe n = 5,318; test common-safe n = 5,535.
- The 48k and 96k comparisons use the intersection of the M1-48 and M1-96 masks, hence exactly the same examples at both exposure points within each split.
- Validation: 3/3 metrics narrow from 48k to 96k.
- Test: 0/3 metrics narrow; the manuscript explicitly reports this non-reproduction.

## E. Clean 96k multiseed evidence

- Across k5/k20/k50, validation/test, HR@1/NDCG@5/MRR, and training seeds 42/43/44, 54/54 seed-level N-M1 deltas are positive.
- All 18 protocol-split-metric aggregates have 3/3 positive seed directions.
- k20 has the largest remaining gap; k5 and k50 are smaller. The manuscript does not infer a monotonic candidate-count effect because the protocols are separately constructed and non-nested.

## F. Ranking bootstrap boundary

Cross-task-safe M1-N ranking results use no bootstrap confidence intervals. They report point estimates, equal-weight three-seed means, sample SD with n=3 and ddof=1, and per-seed signs as descriptive training-run variability. The separate seed42 paired user bootstrap remains only for the Y96 versus M1-Y96 binary Y-side comparison. The manuscript states that these summaries do not establish confidence intervals, significance, equivalence, positive transfer, or a multiseed trajectory.

## G. Current RQ3/RQ4 wording

RQ3 states that the common-safe seed42 validation gap narrows across all three metrics from 48k to 96k, while the common-safe test gap does not narrow. It limits the full exposure trajectory to seed42 and reports the independent 96k seeds only as a small, consistently positive N advantage. Y-side evidence supports capability preservation, not equivalence or positive transfer.

RQ4 states that k20 yields the largest N-specialist-M1 gap, all 54 seed-level deltas and 18 aggregate directional items are positive, and k50 also favors N. It explicitly limits the inference to protocol dependence, not candidate-count causality or monotonicity.

## H. Current Limitations wording

> Shared-model ranking comparisons use high-coverage cross-task-safe subsets rather than the entire N holdouts because Y and N use different task-specific temporal splits. This evaluation-side restriction ensures that an N target is not exposed through the shared adapter's Y-training stream; M1 was not trained under a joint temporal cutoff. Retained coverage ranges from 93.71% to 98.68%, so the conclusions apply to these retained populations.

> Only the 96k operating point has independent training seeds 42/43/44; full MovieLens trajectories remain seed42-only. Cross-task-safe ranking means and sample SD describe n=3 training-run variability and have no bootstrap intervals. Neither establishes cross-seed significance.

## I. Original P1-02

The prior manuscript did not provide enough actual configuration and selection-procedure detail to reproduce or assess critical comparisons. For SASRec, the missing submission-level information comprised architecture, history length, objective, optimizer settings, and how S47/S94/S188/S391 were produced and selected rather than merely naming the four points.

## J. Current SASRec disclosure

The current Methods specify 64-dimensional item and position embeddings, 2 attention heads, 2 causal Transformer layers, a 256-dimensional GELU feed-forward block, dropout 0.2, final LayerNorm, maximum history 10, dot-product item scoring plus item bias, and full-item cross-entropy. Optimization uses AdamW, learning rate 0.001, weight decay 0, no scheduler, batch size 512, and training seed42.

## K. S47/S94/S188/S391 production and selection

S47/S94/S188/S391 are predefined 47/94/188/391 optimizer-step operating points. Each is independently trained from scratch. They are neither validation-selected best checkpoints nor early-stopping outputs. Their recorded actual downstream task-sample exposures are 24,064/48,128/96,256/200,000, including the short final batch, and they are paired with N24/N48/N96/N200 on the same seed42 PopMatch-k5 validation and test candidate sets.

## L. RQ5 fairness boundary

The N-SASRec comparison claims only approximately matched downstream task-sample exposure. It does not claim alignment of pretraining, tokens, optimizer updates, FLOPs, wall-clock time, hardware, latency, parameter count, compute, or end-to-end resource efficiency. Validation is the main comparison and frozen test is report-only.

## M. Amazon final state

Active Amazon evidence contains Base, Y-as-ranker, N, and SASRec only. No active Amazon M1/M-N evidence remains. Amazon is used only as an earlier-point ranking-side directional check, not as a second exposure trajectory or clean M1 replication.
