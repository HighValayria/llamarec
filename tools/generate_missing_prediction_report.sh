#!/usr/bin/env bash
set -euo pipefail

MACHINE="${1:-}"
case "$MACHINE" in
  A) SEED=42 ;;
  B) SEED=43 ;;
  C) SEED=44 ;;
  *) echo "Usage: bash generate_missing_prediction_report.sh A|B|C" >&2; exit 2 ;;
esac

ROOT="${ROOT:-/root/llamarec}"
REMOTE="${REMOTE:-https://github.com/HighValayria/llamarec.git}"
BRANCH="codex/missing-prediction-report-machine-$(printf '%s' "$MACHINE" | tr 'A-Z' 'a-z')"
REPORT="$(mktemp "/tmp/llamarec_prediction_report_${MACHINE}_XXXXXX.md")"
PUBLISH_ROOT="$(mktemp -d "/tmp/llamarec_prediction_publish_${MACHINE}_XXXXXX")"
trap 'rm -f "$REPORT"; rm -rf "$PUBLISH_ROOT"' EXIT

declare -a DIRS=()
if [[ "$MACHINE" == "A" ]]; then
  DIRS=(
    "$ROOT/outputs/n/movielens-1m/exposure_n_s6000/popmatch_eval"
    "$ROOT/outputs/m/movielens-1m/exposure_m1_s12000/popmatch_eval"
    "$ROOT/outputs/m/movielens-1m/exposure_m1_s12000/popmatch_eval_valid_only"
  )
else
  DIRS=(
    "$ROOT/outputs/n/movielens-1m/exposure_n_s12000_seed${SEED}/popmatch_eval"
    "$ROOT/outputs/m/movielens-1m/exposure_m1_s24000_seed${SEED}/popmatch_eval"
    "$ROOT/outputs/phase2a/multiseed96_ranking_robustness/seed${SEED}/n_k0_k20_seed42"
    "$ROOT/outputs/phase2a/multiseed96_ranking_robustness/seed${SEED}/m1_k20_seed42"
    "$ROOT/outputs/phase2a/multiseed96_ranking_robustness/seed${SEED}/n_k0_k50_seed42"
    "$ROOT/outputs/phase2a/multiseed96_ranking_robustness/seed${SEED}/m1_k50_seed42"
  )
fi

file_sha() { sha256sum "$1" | awk '{print $1}'; }

{
  echo "# Missing Prediction Report: Machine $MACHINE"
  echo
  echo "- generated_utc: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "- hostname: $(hostname)"
  echo "- machine: $MACHINE"
  echo "- expected_seed: $SEED"
  echo "- repository_root: $ROOT"
  echo "- repository_head: $(git -C "$ROOT" rev-parse HEAD 2>/dev/null || echo UNKNOWN)"
  echo "- training_invoked: NO"
  echo "- inference_invoked: NO"
  echo
  echo "## Candidate directories"
  echo

  for dir in "${DIRS[@]}"; do
    echo "### \`$dir\`"
    if [[ ! -d "$dir" ]]; then
      echo
      echo "- status: MISSING_DIRECTORY"
      echo
      continue
    fi
    echo
    echo "- status: FOUND"
    echo "- absolute_path: $(readlink -f "$dir")"
    echo
    echo "#### Identity metadata"
    echo
    for meta in \
      "$dir/evaluation_summary.json" \
      "$dir/evaluation_config_snapshot.yaml" \
      "$dir/valid_metrics.json" \
      "$dir/test_metrics.json" \
      "$(dirname "$dir")/run_summary.json" \
      "$(dirname "$dir")/config_snapshot.yaml" \
      "$(dirname "$dir")/metrics.json"
    do
      [[ -f "$meta" ]] || continue
      echo "- file: $meta"
      echo "  size: $(stat -c %s "$meta")"
      echo "  mtime: $(stat -c %y "$meta")"
      echo "  sha256: $(file_sha "$meta")"
      if [[ "$meta" == *.json ]] && command -v jq >/dev/null 2>&1; then
        identity="$(jq -c '{model,dataset,seed,splits,adapter_dir,candidate_files,counts,outputs_dir,global_step,max_steps}' "$meta" 2>/dev/null || true)"
        [[ -n "$identity" ]] && echo "  identity: $identity"
      else
        identity="$(grep -E -m 12 '^(model|dataset|seed|splits|adapter_dir|candidate_files|outputs_dir|global_step|max_steps):' "$meta" 2>/dev/null | tr '\n' ';' || true)"
        [[ -n "$identity" ]] && echo "  identity: $identity"
      fi
    done
    echo
    echo "#### Prediction candidates"
    echo
    found=0
    while IFS= read -r pred; do
      [[ -n "$pred" ]] || continue
      found=$((found + 1))
      echo "- file: $pred"
      echo "  absolute_path: $(readlink -f "$pred")"
      echo "  size: $(stat -c %s "$pred")"
      echo "  mtime: $(stat -c %y "$pred")"
      echo "  sha256: $(file_sha "$pred")"
      case "$pred" in
        *.jsonl)
          echo "  rows: $(wc -l < "$pred")"
          if command -v jq >/dev/null 2>&1; then
            echo "  schema: $(sed -n '1p' "$pred" | jq -r 'keys | join(",")' 2>/dev/null || echo UNREADABLE)"
            echo "  first_row_identity: $(sed -n '1p' "$pred" | jq -c '{model,task,inference_mode,split,user_id,ground_truth_movie_id,candidate_generation,adapter_dir}' 2>/dev/null || echo UNREADABLE)"
          else
            echo "  first_row_prefix: $(sed -n '1p' "$pred" | cut -c1-1000)"
          fi
          ;;
        *.csv|*.tsv)
          echo "  rows_without_header: $(awk 'END {print NR > 0 ? NR-1 : 0}' "$pred")"
          echo "  columns: $(sed -n '1p' "$pred")"
          ;;
        *) echo "  schema: NOT_OPENED" ;;
      esac
    done < <(
      find "$dir" -maxdepth 1 -type f \
        \( -iname '*pred*' -o -iname '*score*' -o -iname '*rank*' \) \
        \( -iname '*.csv' -o -iname '*.json' -o -iname '*.jsonl' -o \
           -iname '*.pkl' -o -iname '*.parquet' -o -iname '*.npy' -o -iname '*.npz' \) \
        -print | sort
    )
    [[ "$found" -gt 0 ]] || echo "- status: NO_PREDICTION_CANDIDATE"
    echo
  done
} > "$REPORT"

git clone --quiet --filter=blob:none --no-checkout "$REMOTE" "$PUBLISH_ROOT/repo"
git -C "$PUBLISH_ROOT/repo" config user.name "LlamaRec Artifact Reporter"
git -C "$PUBLISH_ROOT/repo" config user.email "artifact-reporter@llamarec.local"
if git -C "$PUBLISH_ROOT/repo" ls-remote --exit-code --heads origin "$BRANCH" >/dev/null 2>&1; then
  git -C "$PUBLISH_ROOT/repo" fetch --quiet origin "$BRANCH"
  git -C "$PUBLISH_ROOT/repo" switch --quiet -c "$BRANCH" --track "origin/$BRANCH"
else
  git -C "$PUBLISH_ROOT/repo" checkout --quiet origin/main
  git -C "$PUBLISH_ROOT/repo" switch --quiet -c "$BRANCH"
fi

DEST="$PUBLISH_ROOT/repo/paper/metadata/missing_prediction_report_machine_${MACHINE}.md"
mkdir -p "$(dirname "$DEST")"
cp "$REPORT" "$DEST"
git -C "$PUBLISH_ROOT/repo" add -f "paper/metadata/missing_prediction_report_machine_${MACHINE}.md"
if git -C "$PUBLISH_ROOT/repo" diff --cached --quiet; then
  echo "REPORT_UNCHANGED branch=$BRANCH"
  exit 0
fi
git -C "$PUBLISH_ROOT/repo" commit --quiet -m "Add machine $MACHINE missing prediction report"
git -C "$PUBLISH_ROOT/repo" push --quiet -u origin "$BRANCH"
echo "REPORT_PUSHED branch=$BRANCH path=paper/metadata/missing_prediction_report_machine_${MACHINE}.md"
