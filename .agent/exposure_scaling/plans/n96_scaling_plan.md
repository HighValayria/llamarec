# N96 Scaling Plan

Decision: run N-K0 96k only. Do not run Y-K0 96k.

Validation evidence from cloud PopMatch-k5 seed42:

| model | exposure | HR@1 | NDCG@5 | MRR | decision |
| --- | ---: | ---: | ---: | ---: | --- |
| Y-K0 | 24k | 0.2156828194 | 0.6002715889 | 0.4704082232 | compare |
| Y-K0 | 48k | 0.2165638767 | 0.5994649797 | 0.4694772394 | stop Y |
| N-K0 | 24k | 0.5774449339 | 0.8067686847 | 0.7420058737 | compare |
| N-K0 | 48k | 0.6029955947 | 0.8200163654 | 0.7595418502 | extend N |

N24 -> N48 validation deltas: HR@1 +0.0255506608, NDCG@5 +0.0132476807, MRR +0.0175359765.

Cloud command after pulling the script commit:

```bash
cd /root/llamarec && git pull origin main
bash .agent/exposure_scaling/commands/gpu_n96_train_nohup.sh
```

After training completes:

```bash
cd /root/llamarec && bash .agent/exposure_scaling/commands/gpu_n96_eval_nohup.sh
```
