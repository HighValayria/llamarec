# Paper Run Recovery Manifest

Status: READY_TO_RECOVER

TRAINING_STARTED = NO

Run label: RECOVERY / REPLAY RUN

The original paper-run git revision is UNCONFIRMED. Previous read-only audits
established that training-critical code is identical across recovered candidate
revisions `dcd4b9f`, local HEAD `3d83e0c`, and `origin/main` `a9c6cd9`.
Therefore these commands define recovery replay runs, not bitwise reproduction
runs.

## Phase A Preservation

Remote-only reports were exported into `recovery/provenance/`:

- `missing_prediction_report_machine_A.md`
- `missing_prediction_report_machine_B.md`
- `missing_prediction_report_machine_C.md`

Current local recovery assets were snapshotted without modifying originals:

- Snapshot root: `recovery/provenance/local_snapshot_20260914_172323/`
- Checksum file: `recovery/provenance/SHA256SUMS.txt`
- Inventory file: `recovery/provenance/ASSET_INVENTORY.md`

The preservation set covers the requested `paper/evidence/ms96_*`,
`paper/tables/ms96_*`, scientific repair tables, recovery metadata JSON,
imported missing-prediction bundles, MS96 integration artifacts, `outputs/`,
`data/candidates/`, `true_paper/`, and `check_data.py`.

## Shared Configuration

- Dataset: `movielens-1m`
- Base model path: `models/Llama-3.2-3B-Instruct`
- Shared upstream model name: `meta-llama/Llama-3.2-3B-Instruct`
- Max sequence length: 2048
- Per-device train batch size: 1
- Gradient accumulation steps: 8
- World size: 1
- Effective batch size: 8 examples per optimizer step
- Learning rate: 0.0002
- Save interval: 3000 optimizer steps
- Internal eval during training: disabled with `--disable-internal-eval`
- Historical GPU memory class: 24 GB; evidence references RTX 4090 24 GB
- Optimizer: UNCONFIRMED
- Scheduler: UNCONFIRMED
- Warmup: UNCONFIRMED

Dataset construction command:

```bash
python -m src.data.build_step2 --config configs/experiment.yaml --dataset movielens-1m
```

Candidate construction command:

```bash
python -m src.eval.candidate_sets --config configs/experiment.yaml --dataset movielens-1m --candidate-num 5 --variant-name k5_popmatch_seed42 --seed 42 --candidate-method popularity_matched --output-dir data/candidates/movielens-1m/variants/k5_popmatch_seed42
```

Candidate and evaluation assets:

- `data/candidates/movielens-1m/variants/k5_popmatch_seed42/valid.jsonl`
- `data/candidates/movielens-1m/variants/k5_popmatch_seed42/test.jsonl`
- Candidate base seed: 42
- Candidate validation generation seed: 143
- Candidate test generation seed: 244

LoRA settings:

- r: 16
- alpha: 32
- dropout: 0.05
- bias: `none`
- task type: `CAUSAL_LM`
- target modules: `q_proj`, `k_proj`, `v_proj`, `o_proj`, `gate_proj`,
  `up_proj`, `down_proj`

Quantization settings:

- 4-bit QLoRA enabled
- quant type: `nf4`
- double quantization: enabled
- compute dtype: bf16 when supported

Tokenizer and model behavior:

- tokenizer loaded with `use_fast=True`
- missing pad token is set to EOS
- model loaded with quantization config, `device_map="auto"`, and low CPU
  memory loading
- model cache disabled for training
- gradient checkpointing enabled
- explicit persisted chat-template behavior: UNCONFIRMED

Response masking:

- N training: confirmed answer-token-only loss; prompt tokens are ignored.
- M1 N side: confirmed through shared N task behavior.
- Y and M1 Y side: UNCONFIRMED under strict audit because the exact shared
  preference masking function was not re-read during this Phase B continuation.

## N96 Seed42

- Entry point: `python -m src.train.train_n`
- Config: `configs/n_local_model.yaml`
- Seed: 42
- Run name: `recovery_replay_n96_seed42`
- Target optimizer step: 12000
- Target exposure: 96000 N examples
- Historical command source: `.agent/exposure_scaling/commands/gpu_n96_train.sh`
- Recovery adjustment: omit historical `--resume-from-checkpoint` because
  paper-dependent checkpoints are lost.

Training command:

```bash
python -m src.train.train_n --config configs/n_local_model.yaml --dataset movielens-1m --run-name recovery_replay_n96_seed42 --seed 42 --max-train-samples 200000 --max-valid-samples 200000 --max-steps 12000 --per-device-train-batch-size 1 --gradient-accumulation-steps 8 --learning-rate 0.0002 --bf16 --eval-steps 1000000 --save-steps 3000 --disable-internal-eval
```

Evaluation command after training:

```bash
python -m src.inference.evaluate_n_adapter --config configs/n_local_model.yaml --dataset movielens-1m --adapter-dir outputs/n/movielens-1m/recovery_replay_n96_seed42/adapter --mode real --splits validation test --batch-size 1 --valid-candidates data/candidates/movielens-1m/variants/k5_popmatch_seed42/valid.jsonl --test-candidates data/candidates/movielens-1m/variants/k5_popmatch_seed42/test.jsonl --output-dir outputs/n/movielens-1m/recovery_replay_n96_seed42/popmatch_eval
```

Expected output paths:

- `outputs/n/movielens-1m/recovery_replay_n96_seed42/adapter/`
- `outputs/n/movielens-1m/recovery_replay_n96_seed42/checkpoints/checkpoint-3000/`
- `outputs/n/movielens-1m/recovery_replay_n96_seed42/checkpoints/checkpoint-6000/`
- `outputs/n/movielens-1m/recovery_replay_n96_seed42/checkpoints/checkpoint-9000/`
- `outputs/n/movielens-1m/recovery_replay_n96_seed42/checkpoints/checkpoint-12000/`
- `outputs/n/movielens-1m/recovery_replay_n96_seed42/popmatch_eval/`

Expected historical metrics:

- Validation: HR@1 0.6237885463, NDCG@5 0.8302923694, MRR 0.7732422907
- Test: HR@1 0.6100440529, NDCG@5 0.8218966233, MRR 0.7622026432

## M1-96 Seed42

- Entry point: `python -m src.train.train_m`
- Config: `configs/m_local_model.yaml`
- Seed: 42
- Run name: `recovery_replay_m1_96_seed42`
- Target optimizer step: 24000
- Target exposure: 96000 Y examples plus 96000 N examples under 1:1 task
  mixing if recovered sampler behavior matches historical notes
- Historical command source:
  `.agent/exposure_scaling/alignment/commands/m1_commands.sh`
- Recovery adjustment: omit historical `--resume-from-checkpoint` because
  paper-dependent checkpoints are lost.

Training command:

```bash
python -m src.train.train_m --config configs/m_local_model.yaml --dataset movielens-1m --run-name recovery_replay_m1_96_seed42 --seed 42 --max-y-train-samples 200000 --max-n-train-samples 200000 --max-y-valid-samples 200000 --max-n-valid-samples 200000 --task-ratio-y 1 --task-ratio-n 1 --max-steps 24000 --per-device-train-batch-size 1 --gradient-accumulation-steps 8 --learning-rate 0.0002 --bf16 --eval-steps 1000000 --save-steps 3000 --disable-internal-eval
```

Evaluation command after training:

```bash
python -m src.inference.evaluate_m_adapter --config configs/m_local_model.yaml --dataset movielens-1m --adapter-dir outputs/m/movielens-1m/recovery_replay_m1_96_seed42/adapter --mode real --splits validation test --batch-size 1 --valid-candidates data/candidates/movielens-1m/variants/k5_popmatch_seed42/valid.jsonl --test-candidates data/candidates/movielens-1m/variants/k5_popmatch_seed42/test.jsonl --output-dir outputs/m/movielens-1m/recovery_replay_m1_96_seed42/popmatch_eval
```

Expected output paths:

- `outputs/m/movielens-1m/recovery_replay_m1_96_seed42/adapter/`
- `outputs/m/movielens-1m/recovery_replay_m1_96_seed42/checkpoints/checkpoint-3000/`
- `outputs/m/movielens-1m/recovery_replay_m1_96_seed42/checkpoints/checkpoint-6000/`
- `outputs/m/movielens-1m/recovery_replay_m1_96_seed42/checkpoints/checkpoint-9000/`
- `outputs/m/movielens-1m/recovery_replay_m1_96_seed42/checkpoints/checkpoint-12000/`
- `outputs/m/movielens-1m/recovery_replay_m1_96_seed42/checkpoints/checkpoint-15000/`
- `outputs/m/movielens-1m/recovery_replay_m1_96_seed42/checkpoints/checkpoint-18000/`
- `outputs/m/movielens-1m/recovery_replay_m1_96_seed42/checkpoints/checkpoint-21000/`
- `outputs/m/movielens-1m/recovery_replay_m1_96_seed42/checkpoints/checkpoint-24000/`
- `outputs/m/movielens-1m/recovery_replay_m1_96_seed42/popmatch_eval/`

Expected historical metrics:

- Validation M1-Y: AUC 0.7868352749, F1 0.7838427948, Accuracy 0.7281318149
- Validation M1-N: HR@1 0.6234361233, NDCG@5 0.8291402759, MRR 0.771753304
- Test M1-Y: AUC 0.7864837284, F1 0.7835646558, Accuracy 0.7271309771
- Test M1-N: HR@1 0.5973568282, NDCG@5 0.8162307888, MRR 0.7546490455

## Y96 Seed42

- Entry point: `python -m src.train.train_y`
- Config: `configs/y_local_model.yaml`
- Seed: 42
- Run name: `recovery_replay_y96_seed42`
- Target optimizer step: 12000
- Target exposure: 96000 Y examples
- Historical command source:
  `.agent/exposure_scaling/alignment/commands/y_commands.sh`
- Recovery adjustment: omit historical `--resume-from-checkpoint` because
  paper-dependent checkpoints are lost.

Training command:

```bash
python -m src.train.train_y --config configs/y_local_model.yaml --dataset movielens-1m --run-name recovery_replay_y96_seed42 --seed 42 --max-train-samples 200000 --max-valid-samples 200000 --max-steps 12000 --per-device-train-batch-size 1 --gradient-accumulation-steps 8 --learning-rate 0.0002 --bf16 --eval-steps 1000000 --save-steps 3000 --disable-internal-eval
```

Evaluation command after training:

```bash
python -m src.inference.evaluate_y_adapter --config configs/y_local_model.yaml --dataset movielens-1m --adapter-dir outputs/y/movielens-1m/recovery_replay_y96_seed42/adapter --mode real --splits validation test --batch-size 1 --valid-candidates data/candidates/movielens-1m/variants/k5_popmatch_seed42/valid.jsonl --test-candidates data/candidates/movielens-1m/variants/k5_popmatch_seed42/test.jsonl --output-dir outputs/y/movielens-1m/recovery_replay_y96_seed42/popmatch_eval
```

Expected output paths:

- `outputs/y/movielens-1m/recovery_replay_y96_seed42/adapter/`
- `outputs/y/movielens-1m/recovery_replay_y96_seed42/checkpoints/checkpoint-3000/`
- `outputs/y/movielens-1m/recovery_replay_y96_seed42/checkpoints/checkpoint-6000/`
- `outputs/y/movielens-1m/recovery_replay_y96_seed42/checkpoints/checkpoint-9000/`
- `outputs/y/movielens-1m/recovery_replay_y96_seed42/checkpoints/checkpoint-12000/`
- `outputs/y/movielens-1m/recovery_replay_y96_seed42/popmatch_eval/`

Expected historical metrics:

- Validation: AUC 0.7843504067, F1 0.7783174665, Accuracy 0.7235279864
- Test: AUC 0.7853511126, F1 0.7780238029, Accuracy 0.7221067221

## Unconfirmed Parameters

These are intentionally not guessed:

- Original paper-run git revision
- Optimizer implementation beyond repository/runtime defaults
- Scheduler implementation beyond repository/runtime defaults
- Warmup behavior beyond repository/runtime defaults
- Explicit persisted chat-template behavior
- Exact Y-side response masking function under strict audit

RECOVERY_DECISION = READY_TO_RECOVER
