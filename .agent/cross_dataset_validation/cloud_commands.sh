#!/usr/bin/env bash
set -euo pipefail

cd /root/llamarec
git fetch origin main
git checkout main
git pull --ff-only origin main
source .venv/bin/activate

echo "== environment check =="
python - <<'PY'
import importlib.util as u
print("yaml", bool(u.find_spec("yaml")))
print("pandas", bool(u.find_spec("pandas")))
print("pyarrow", bool(u.find_spec("pyarrow")))
print("fastparquet", bool(u.find_spec("fastparquet")))
PY

echo "== raw file check =="
find data/raw/amazon_reviews_2023/musical_instruments -maxdepth 3 -type f -printf "%p %s bytes\n" | sort
head -5 data/raw/amazon_reviews_2023/musical_instruments/interactions/Musical_Instruments.csv

echo "== strict step2 build =="
python -m src.data.build_step2 \
  --config configs/experiment.yaml \
  --dataset amazon-musical-instruments \
  --inspection-limit 20

echo "== random-k5 candidates =="
python -m src.eval.candidate_sets \
  --config configs/experiment.yaml \
  --dataset amazon-musical-instruments \
  --candidate-num 5 \
  --variant-name random_k5_seed42 \
  --seed 42 \
  --candidate-method random \
  --output-dir data/candidates/amazon-musical-instruments/variants/random_k5_seed42

echo "== popmatch-k5 candidates =="
python -m src.eval.candidate_sets \
  --config configs/experiment.yaml \
  --dataset amazon-musical-instruments \
  --candidate-num 5 \
  --variant-name popmatch_k5_seed42 \
  --seed 42 \
  --candidate-method popularity_matched \
  --output-dir data/candidates/amazon-musical-instruments/variants/popmatch_k5_seed42

echo "== candidate diagnostics =="
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

echo "== stop point summary =="
cat data/processed/amazon-musical-instruments/stats.json
find data/candidates/amazon-musical-instruments/variants -maxdepth 2 -type f -printf "%p %s bytes\n" | sort
find outputs/cross_dataset_validation/amazon-musical-instruments/candidate_diagnostics -maxdepth 3 -type f -printf "%p %s bytes\n" | sort
