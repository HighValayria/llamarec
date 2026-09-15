# Fast Recovery Ready

Status: READY_TO_RECOVER

TRAINING_STARTED = NO

Run label: RECOVERY / REPLAY RUN

Original paper-run git revision is UNCONFIRMED. Training-critical code was
previously established as identical across `dcd4b9f`, local HEAD `3d83e0c`, and
`origin/main` `a9c6cd9`; these are recovery replay commands, not bitwise
reproduction commands.

## Prepare Data And Candidates

Run only if the dataset or candidate files are missing:

```bash
python -m src.data.build_step2 --config configs/experiment.yaml --dataset movielens-1m
python -m src.eval.candidate_sets --config configs/experiment.yaml --dataset movielens-1m --candidate-num 5 --variant-name k5_popmatch_seed42 --seed 42 --candidate-method popularity_matched --output-dir data/candidates/movielens-1m/variants/k5_popmatch_seed42
```

## N96 Seed42

```bash
python -m src.train.train_n --config configs/n_local_model.yaml --dataset movielens-1m --run-name recovery_replay_n96_seed42 --seed 42 --max-train-samples 200000 --max-valid-samples 200000 --max-steps 12000 --per-device-train-batch-size 1 --gradient-accumulation-steps 8 --learning-rate 0.0002 --bf16 --eval-steps 1000000 --save-steps 3000 --disable-internal-eval
```

```bash
python -m src.inference.evaluate_n_adapter --config configs/n_local_model.yaml --dataset movielens-1m --adapter-dir outputs/n/movielens-1m/recovery_replay_n96_seed42/adapter --mode real --splits validation test --batch-size 1 --valid-candidates data/candidates/movielens-1m/variants/k5_popmatch_seed42/valid.jsonl --test-candidates data/candidates/movielens-1m/variants/k5_popmatch_seed42/test.jsonl --output-dir outputs/n/movielens-1m/recovery_replay_n96_seed42/popmatch_eval
```

## M1-96 Seed42

```bash
python -m src.train.train_m --config configs/m_local_model.yaml --dataset movielens-1m --run-name recovery_replay_m1_96_seed42 --seed 42 --max-y-train-samples 200000 --max-n-train-samples 200000 --max-y-valid-samples 200000 --max-n-valid-samples 200000 --task-ratio-y 1 --task-ratio-n 1 --max-steps 24000 --per-device-train-batch-size 1 --gradient-accumulation-steps 8 --learning-rate 0.0002 --bf16 --eval-steps 1000000 --save-steps 3000 --disable-internal-eval
```

```bash
python -m src.inference.evaluate_m_adapter --config configs/m_local_model.yaml --dataset movielens-1m --adapter-dir outputs/m/movielens-1m/recovery_replay_m1_96_seed42/adapter --mode real --splits validation test --batch-size 1 --valid-candidates data/candidates/movielens-1m/variants/k5_popmatch_seed42/valid.jsonl --test-candidates data/candidates/movielens-1m/variants/k5_popmatch_seed42/test.jsonl --output-dir outputs/m/movielens-1m/recovery_replay_m1_96_seed42/popmatch_eval
```

## Y96 Seed42

```bash
python -m src.train.train_y --config configs/y_local_model.yaml --dataset movielens-1m --run-name recovery_replay_y96_seed42 --seed 42 --max-train-samples 200000 --max-valid-samples 200000 --max-steps 12000 --per-device-train-batch-size 1 --gradient-accumulation-steps 8 --learning-rate 0.0002 --bf16 --eval-steps 1000000 --save-steps 3000 --disable-internal-eval
```

```bash
python -m src.inference.evaluate_y_adapter --config configs/y_local_model.yaml --dataset movielens-1m --adapter-dir outputs/y/movielens-1m/recovery_replay_y96_seed42/adapter --mode real --splits validation test --batch-size 1 --valid-candidates data/candidates/movielens-1m/variants/k5_popmatch_seed42/valid.jsonl --test-candidates data/candidates/movielens-1m/variants/k5_popmatch_seed42/test.jsonl --output-dir outputs/y/movielens-1m/recovery_replay_y96_seed42/popmatch_eval
```

Final status: READY_TO_RECOVER
