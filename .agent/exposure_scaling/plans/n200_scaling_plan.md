# N200 Near-Full-Pool Scaling Plan

Decision: run N-K0 near-full-pool point only. Do not run Y-K0 96k/200k.

Validation evidence from cloud PopMatch-k5 seed42:

| model | exposure | HR@1 | NDCG@5 | MRR | decision |
| --- | ---: | ---: | ---: | ---: | --- |
| Y-K0 | 24k | 0.2156828194 | 0.6002715889 | 0.4704082232 | compare |
| Y-K0 | 48k | 0.2165638767 | 0.5994649797 | 0.4694772394 | stop Y |
| N-K0 | 24k | 0.5774449339 | 0.8067686847 | 0.7420058737 | compare |
| N-K0 | 48k | 0.6029955947 | 0.8200163654 | 0.7595418502 | extend N |
| N-K0 | 96k | 0.6237885463 | 0.8302923694 | 0.7732422907 | extend N to 200k |

Validation deltas:

- N24 -> N48: HR@1 +0.0255506608, NDCG@5 +0.0132476807, MRR +0.0175359765.
- N48 -> N96: HR@1 +0.0207929515, NDCG@5 +0.0102760040, MRR +0.0137004405.

Cloud command after pulling the script commit:

```bash
cd /root/llamarec && git pull origin main && bash .agent/exposure_scaling/commands/gpu_n200_train_then_eval_nohup.sh
```

Progress check:

```bash
cd /root/llamarec && bash .agent/exposure_scaling/commands/gpu_n200_progress.sh
```
