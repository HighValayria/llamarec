# Resolved Commands - Draft

Do not run these until the user approves GPU work and the cloud resume check passes.

## Resume Gate

Confirm current checkpoint directories contain `trainer_state.json`, `optimizer.pt`, `scheduler.pt`, and `rng_state*.pth`. If absent, stop and decide whether to rerun from scratch with a reproducibility gate.

## N-K0 48k

Target: 48,000 N exposure = 6,000 optimizer steps at effective batch 8.

```bash
python -m src.train.train_n \
  --config configs/n.yaml \
  --dataset movielens-1m \
  --run-name exposure_n_s6000 \
  --max-train-samples 200000 \
  --max-valid-samples 200000 \
  --max-steps 6000 \
  --per-device-train-batch-size 1 \
  --gradient-accumulation-steps 8 \
  --learning-rate 0.0002 \
  --bf16 \
  --resume-from-checkpoint /root/llamarec/outputs/n/movielens-1m/sample_efficiency_n_s3000/checkpoints/checkpoint-3000
```

## Y-K0 24k / 48k

```bash
python -m src.train.train_y \
  --config configs/y.yaml \
  --dataset movielens-1m \
  --run-name exposure_y_s3000 \
  --max-train-samples 200000 \
  --max-valid-samples 200000 \
  --max-steps 3000 \
  --per-device-train-batch-size 1 \
  --gradient-accumulation-steps 8 \
  --learning-rate 0.0002 \
  --bf16 \
  --resume-from-checkpoint /root/llamarec/outputs/y/movielens-1m/pool200k_1m_y_1500/checkpoints/checkpoint-1500
```

```bash
python -m src.train.train_y \
  --config configs/y.yaml \
  --dataset movielens-1m \
  --run-name exposure_y_s6000 \
  --max-train-samples 200000 \
  --max-valid-samples 200000 \
  --max-steps 6000 \
  --per-device-train-batch-size 1 \
  --gradient-accumulation-steps 8 \
  --learning-rate 0.0002 \
  --bf16 \
  --resume-from-checkpoint /root/llamarec/outputs/y/movielens-1m/exposure_y_s3000/checkpoints/checkpoint-3000
```

## Evaluation

Use fixed candidate overrides:

```bash
--valid-candidates data/candidates/movielens-1m/variants/k5_popmatch_seed42/valid.jsonl
--test-candidates data/candidates/movielens-1m/variants/k5_popmatch_seed42/test.jsonl
```

Y must run both binary evaluation and P(Yes)-based candidate ranking.
