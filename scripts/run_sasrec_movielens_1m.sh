#!/usr/bin/env bash
set -euo pipefail

# Formal MovieLens-1M SASRec baseline runs.
# Run from the repository root on the cloud server.

PYTHON_BIN="${PYTHON_BIN:-python}"
DATASET="${DATASET:-movielens-1m}"
MAX_SEQUENCE_LENGTH="${MAX_SEQUENCE_LENGTH:-10}"
EMBEDDING_DIM="${EMBEDDING_DIM:-64}"
NUM_HEADS="${NUM_HEADS:-2}"
NUM_LAYERS="${NUM_LAYERS:-2}"
DROPOUT="${DROPOUT:-0.2}"
EPOCHS="${EPOCHS:-10}"
BATCH_SIZE="${BATCH_SIZE:-512}"
LEARNING_RATE="${LEARNING_RATE:-0.001}"
WEIGHT_DECAY="${WEIGHT_DECAY:-0.0}"
SEED="${SEED:-42}"
DEVICE="${DEVICE:-auto}"

"${PYTHON_BIN}" -m src.baselines.sasrec \
  --config configs/experiment.yaml \
  --dataset "${DATASET}" \
  --splits validation test \
  --output-dir "outputs/baselines/${DATASET}/sasrec_canonical_k5" \
  --max-sequence-length "${MAX_SEQUENCE_LENGTH}" \
  --embedding-dim "${EMBEDDING_DIM}" \
  --num-heads "${NUM_HEADS}" \
  --num-layers "${NUM_LAYERS}" \
  --dropout "${DROPOUT}" \
  --epochs "${EPOCHS}" \
  --batch-size "${BATCH_SIZE}" \
  --learning-rate "${LEARNING_RATE}" \
  --weight-decay "${WEIGHT_DECAY}" \
  --seed "${SEED}" \
  --device "${DEVICE}"

"${PYTHON_BIN}" -m src.baselines.sasrec \
  --config configs/experiment.yaml \
  --dataset "${DATASET}" \
  --splits validation test \
  --output-dir "outputs/baselines/${DATASET}/sasrec_k5_popmatch_seed42" \
  --valid-candidates "data/candidates/${DATASET}/variants/k5_popmatch_seed42/valid.jsonl" \
  --test-candidates "data/candidates/${DATASET}/variants/k5_popmatch_seed42/test.jsonl" \
  --max-sequence-length "${MAX_SEQUENCE_LENGTH}" \
  --embedding-dim "${EMBEDDING_DIM}" \
  --num-heads "${NUM_HEADS}" \
  --num-layers "${NUM_LAYERS}" \
  --dropout "${DROPOUT}" \
  --epochs "${EPOCHS}" \
  --batch-size "${BATCH_SIZE}" \
  --learning-rate "${LEARNING_RATE}" \
  --weight-decay "${WEIGHT_DECAY}" \
  --seed "${SEED}" \
  --device "${DEVICE}"
