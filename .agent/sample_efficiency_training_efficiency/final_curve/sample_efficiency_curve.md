# Sample-Efficiency Curve

Dataset: `movielens-1m`.
Protocol: `N-task sample-efficiency curve on fixed popmatch candidates`.

## Curve Points

| model | point | N-task exposure | optimizer steps | effective batch | HR@1 | NDCG@5 | MRR | samples | evidence_status |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| N-K0 | n_s375 | 3000 | 375 | 8 | 0.4313656388 | 0.7260192668 | 0.6355653451 | 5675 | computed |
| N-K0 | n_s750 | 6000 | 750 | 8 | 0.5222907489 | 0.776125471 | 0.7016299559 | 5675 | computed |
| N-K0 | n_s1500 | 12000 | 1500 | 8 | 0.5466079295 | 0.7884963692 | 0.718041116 | 5675 | computed |
| N-K0 | n_s3000 | 24000 | 3000 | 8 | 0.5612334802 | 0.7968087155 | 0.7289720999 | 5675 | computed |
| SASRec | sasrec_s6 | 3072 | 6 | 512 | 0.211277533 | 0.6011741153 | 0.4713597651 | 5675 | computed |
| SASRec | sasrec_s12 | 6144 | 12 | 512 | 0.2421145374 | 0.6176512047 | 0.4930631424 | 5675 | computed |
| SASRec | sasrec_s23 | 11776 | 23 | 512 | 0.2699559471 | 0.6348928207 | 0.5156622614 | 5675 | computed |
| SASRec | sasrec_s47 | 24064 | 47 | 512 | 0.2840528634 | 0.6429537473 | 0.5261879589 | 5675 | computed |
| SASRec | sasrec_s1500 | 767424 | 1500 | 512 | 0.6088105727 | 0.8198039644 | 0.7595506608 | 5675 | computed |
| SASRec | sasrec_s3000 | 1534656 | 3000 | 512 | 0.6243171806 | 0.8283562609 | 0.770866373 | 5675 | computed |

## Closest Exposure Gaps

| comparison | n_exposure | sasrec_exposure | mismatch % | delta_HR@1 | delta_NDCG@5 | delta_MRR | evidence_status |
|---|---:|---:|---:|---:|---:|---:|---|
| sasrec_s6_minus_n_s375 | 3000 | 3072 | 2.4 | -0.2200881058 | -0.1248451515 | -0.16420558 | computed |
| sasrec_s12_minus_n_s750 | 6000 | 6144 | 2.4 | -0.2801762115 | -0.1584742663 | -0.2085668135 | computed |
| sasrec_s23_minus_n_s1500 | 12000 | 11776 | -1.8666666667 | -0.2766519824 | -0.1536035485 | -0.2023788546 | computed |
| sasrec_s47_minus_n_s3000 | 24000 | 24064 | 0.2666666667 | -0.2771806168 | -0.1538549682 | -0.202784141 | computed |

## Direct Answers

- curve_status: computed for planned points
- sample_efficiency_claim: SASRec does not exceed N-K0 at closest-exposure points by HR@1
- next_action: interpret curve with candidate-size and cold-slice diagnostics before making durable claims

## Boundary

This is a sample-exposure curve, not strict compute/capacity matching.
