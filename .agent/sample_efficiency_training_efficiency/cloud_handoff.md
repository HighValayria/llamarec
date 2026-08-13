# Sample Efficiency Cloud Handoff

## Goal

Run a small N-task sample-exposure grid for N-K0 and SASRec on
`k5_popmatch_seed42`, then regenerate `sample_efficiency_curve`.

## Grid

| family | point | optimizer steps | effective batch | approximate N exposure |
|---|---|---:|---:|---:|
| N-K0 | n_s375 | 375 | 8 | 3000 |
| N-K0 | n_s750 | 750 | 8 | 6000 |
| N-K0 | n_s1500 | 1500 | 8 | 12000 |
| N-K0 | n_s3000 | 3000 | 8 | 24000 |
| SASRec | sasrec_s6 | 6 | 512 | 3072 |
| SASRec | sasrec_s12 | 12 | 512 | 6144 |
| SASRec | sasrec_s23 | 23 | 512 | 11776 |
| SASRec | sasrec_s47 | 47 | 512 | 24064 |
| SASRec | sasrec_s1500 | 1500 | 512 | 767424 |
| SASRec | sasrec_s3000 | 3000 | 512 | 1534656 |

`n_s1500`, `sasrec_s23`, `sasrec_s1500`, and `sasrec_s3000` may already exist
from earlier stages. The commands below check before running the expensive
parts.

## Commands

```bash
cd /root/llamarec

echo "== git sync =="
git branch --show-current
git status --short
git fetch origin
git pull --ff-only origin main
git rev-parse --short HEAD

echo "== required data =="
test -f data/candidates/movielens-1m/variants/k5_popmatch_seed42/test.jsonl
test -f data/processed/movielens-1m/next_item_train.jsonl

echo "== N-K0 train/eval grid =="
for spec in \
  "375 sample_efficiency_n_s375 sample_efficiency_n_s375_popmatch_eval" \
  "750 sample_efficiency_n_s750 sample_efficiency_n_s750_popmatch_eval" \
  "3000 sample_efficiency_n_s3000 sample_efficiency_n_s3000_popmatch_eval"
do
  set -- $spec
  steps="$1"
  train_run="$2"
  eval_run="$3"
  train_dir="outputs/n/movielens-1m/${train_run}"
  eval_dir="outputs/n/movielens-1m/${eval_run}"

  if [ ! -f "${train_dir}/adapter/adapter_config.json" ]; then
    python -m src.train.train_n \
      --config configs/n.yaml \
      --dataset movielens-1m \
      --output-dir "${train_dir}" \
      --max-train-samples 200000 \
      --max-valid-samples 5675 \
      --per-device-train-batch-size 1 \
      --per-device-eval-batch-size 1 \
      --gradient-accumulation-steps 8 \
      --learning-rate 0.0002 \
      --max-steps "${steps}" \
      --logging-steps 25 \
      --eval-steps 100000 \
      --save-steps 100000 \
      --bf16
  fi

  if [ ! -f "${eval_dir}/test_metrics.json" ]; then
    python -m src.inference.evaluate_n_adapter \
      --config configs/n.yaml \
      --dataset movielens-1m \
      --mode real \
      --adapter-dir "${train_dir}/adapter" \
      --output-dir "${eval_dir}" \
      --splits test \
      --test-candidates data/candidates/movielens-1m/variants/k5_popmatch_seed42/test.jsonl
  fi
done

echo "== ensure existing N-K0 s1500 eval =="
test -f outputs/n/movielens-1m/pool200k_1m_n_1500_popmatch_eval/test_metrics.json

echo "== SASRec train/eval grid =="
for spec in \
  "6 sample_efficiency_sasrec_s6 sample_efficiency_sasrec_s6_popmatch_eval" \
  "12 sample_efficiency_sasrec_s12 sample_efficiency_sasrec_s12_popmatch_eval" \
  "47 sample_efficiency_sasrec_s47 sample_efficiency_sasrec_s47_popmatch_eval"
do
  set -- $spec
  steps="$1"
  train_run="$2"
  eval_run="$3"
  train_dir="outputs/baselines/movielens-1m/${train_run}"
  eval_dir="outputs/baselines/movielens-1m/${eval_run}"

  if [ ! -f "${train_dir}/model.pt" ]; then
    python -m src.baselines.sasrec \
      --config configs/experiment.yaml \
      --dataset movielens-1m \
      --splits test \
      --output-dir "${train_dir}" \
      --valid-candidates data/candidates/movielens-1m/variants/k5_popmatch_seed42/valid.jsonl \
      --test-candidates data/candidates/movielens-1m/variants/k5_popmatch_seed42/test.jsonl \
      --max-train-samples 200000 \
      --max-steps "${steps}" \
      --epochs 1 \
      --batch-size 512 \
      --learning-rate 0.001 \
      --seed 42 \
      --device cuda
  fi

  if [ ! -f "${eval_dir}/test_metrics.json" ]; then
    python -m src.baselines.sasrec \
      --config configs/experiment.yaml \
      --dataset movielens-1m \
      --splits test \
      --output-dir "${eval_dir}" \
      --model-dir "${train_dir}" \
      --test-candidates data/candidates/movielens-1m/variants/k5_popmatch_seed42/test.jsonl \
      --device cuda
  fi
done

echo "== ensure existing SASRec anchor rows =="
test -f outputs/baselines/movielens-1m/sasrec_exp_match_k5_popmatch_seed42_s23/test_metrics.json
test -f outputs/baselines/movielens-1m/sasrec_fixed_popmatch_k5_200k_s1500_eval/test_metrics.json
test -f outputs/baselines/movielens-1m/sasrec_fixed_popmatch_k5_200k_s3000_eval/test_metrics.json

echo "== summarize sample-efficiency curve =="
python -m src.analysis.sample_efficiency_curve \
  --config configs/experiment.yaml \
  --dataset movielens-1m \
  --output-dir outputs/sample_efficiency_training_efficiency

cat outputs/sample_efficiency_training_efficiency/sample_efficiency_curve.md
```
