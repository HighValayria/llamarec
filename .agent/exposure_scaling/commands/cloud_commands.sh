#!/usr/bin/env bash
set -euo pipefail

# Inventory only. Do not launch training from this file until the user approves.
ROOT=/root/llamarec
cd "$ROOT"

find outputs/y/movielens-1m outputs/n/movielens-1m outputs/m/movielens-1m \
  -maxdepth 4 \
  \( -name trainer_state.json -o -name optimizer.pt -o -name scheduler.pt -o -name 'rng_state*.pth' \) \
  -print | sort

find outputs/y/movielens-1m outputs/n/movielens-1m outputs/m/movielens-1m \
  -maxdepth 3 -name encoded_dataset_summary.json -print | sort

find outputs/y/movielens-1m outputs/n/movielens-1m outputs/m/movielens-1m \
  -maxdepth 3 \( -name '*metrics.json' -o -name evaluation_summary.json \) -print | sort
