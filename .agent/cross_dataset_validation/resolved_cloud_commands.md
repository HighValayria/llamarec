# Resolved Cloud Commands

## Status

These commands are CPU-only and prepare the Amazon Musical Instruments data
gate. They do not start Base inference, LLM fine-tuning, or SASRec training.

Run after pulling the latest `main` that contains the Amazon adapter.

## Sync

```bash
cd /root/llamarec
git fetch origin main
git checkout main
git pull --ff-only origin main
source .venv/bin/activate
```

## Environment Check

```bash
python - <<'PY'
import importlib.util as u
print("yaml", bool(u.find_spec("yaml")))
print("pandas", bool(u.find_spec("pandas")))
print("pyarrow", bool(u.find_spec("pyarrow")))
print("fastparquet", bool(u.find_spec("fastparquet")))
PY
```

Need `yaml`, `pandas`, and either `pyarrow` or `fastparquet` for formal local
build.

## Raw File Check

```bash
cd /root/llamarec
find data/raw/amazon_reviews_2023/musical_instruments -maxdepth 3 -type f -printf "%p %s bytes\n" | sort
head -5 data/raw/amazon_reviews_2023/musical_instruments/interactions/Musical_Instruments.csv
```

Expected interaction columns:

```text
user_id,parent_asin,rating,timestamp
```

## Strict Step2 Build

```bash
cd /root/llamarec
source .venv/bin/activate

python -m src.data.build_step2 \
  --config configs/experiment.yaml \
  --dataset amazon-musical-instruments \
  --inspection-limit 20
```

Expected outputs:

```text
data/processed/amazon-musical-instruments/full_sequences.jsonl
data/processed/amazon-musical-instruments/positive_sequences.jsonl
data/processed/amazon-musical-instruments/split.json
data/processed/amazon-musical-instruments/preference_samples.jsonl
data/processed/amazon-musical-instruments/preference_train.jsonl
data/processed/amazon-musical-instruments/preference_valid.jsonl
data/processed/amazon-musical-instruments/preference_test.jsonl
data/processed/amazon-musical-instruments/next_item_train.jsonl
data/processed/amazon-musical-instruments/next_item_valid.jsonl
data/processed/amazon-musical-instruments/next_item_test.jsonl
data/processed/amazon-musical-instruments/stats.json
data/processed/amazon-musical-instruments/inspection_samples.md
```

## Random-k5 Candidates

```bash
cd /root/llamarec
source .venv/bin/activate

python -m src.eval.candidate_sets \
  --config configs/experiment.yaml \
  --dataset amazon-musical-instruments \
  --candidate-num 5 \
  --variant-name random_k5_seed42 \
  --seed 42 \
  --candidate-method random \
  --output-dir data/candidates/amazon-musical-instruments/variants/random_k5_seed42
```

## PopMatch-k5 Candidates

```bash
cd /root/llamarec
source .venv/bin/activate

python -m src.eval.candidate_sets \
  --config configs/experiment.yaml \
  --dataset amazon-musical-instruments \
  --candidate-num 5 \
  --variant-name popmatch_k5_seed42 \
  --seed 42 \
  --candidate-method popularity_matched \
  --output-dir data/candidates/amazon-musical-instruments/variants/popmatch_k5_seed42
```

## Candidate Diagnostics

```bash
cd /root/llamarec
source .venv/bin/activate

python -m src.analysis.candidate_set_diagnostics \
  --config configs/experiment.yaml \
  --dataset amazon-musical-instruments \
  --valid-candidates data/candidates/amazon-musical-instruments/variants/random_k5_seed42/valid.jsonl \
  --test-candidates data/candidates/amazon-musical-instruments/variants/random_k5_seed42/test.jsonl \
  --output-dir outputs/cross_dataset_validation/amazon-musical-instruments/candidate_diagnostics/random_k5_seed42

python -m src.analysis.candidate_set_diagnostics \
  --config configs/experiment.yaml \
  --dataset amazon-musical-instruments \
  --valid-candidates data/candidates/amazon-musical-instruments/variants/popmatch_k5_seed42/valid.jsonl \
  --test-candidates data/candidates/amazon-musical-instruments/variants/popmatch_k5_seed42/test.jsonl \
  --output-dir outputs/cross_dataset_validation/amazon-musical-instruments/candidate_diagnostics/popmatch_k5_seed42
```

## Stop Point

After these commands, stop and paste:

```bash
cat data/processed/amazon-musical-instruments/stats.json
find data/candidates/amazon-musical-instruments/variants -maxdepth 2 -type f -printf "%p %s bytes\n" | sort
find outputs/cross_dataset_validation/amazon-musical-instruments/candidate_diagnostics -maxdepth 3 -type f -printf "%p %s bytes\n" | sort
```
