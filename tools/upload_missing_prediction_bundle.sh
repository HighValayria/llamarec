#!/usr/bin/env bash
set -euo pipefail

MACHINE="${1:-}"
case "$MACHINE" in
  A) SEED=42 ;;
  B) SEED=43 ;;
  C) SEED=44 ;;
  *) echo "Usage: bash upload_missing_prediction_bundle.sh A|B|C" >&2; exit 2 ;;
esac

ROOT="${ROOT:-/root/llamarec}"
REMOTE="${REMOTE:-https://github.com/HighValayria/llamarec.git}"
BRANCH="codex/missing-prediction-bundle-machine-$(printf '%s' "$MACHINE" | tr 'A-Z' 'a-z')"
WORK="$(mktemp -d "/tmp/llamarec_prediction_bundle_${MACHINE}_XXXXXX")"
PUBLISH="$WORK/publish"
ARCHIVE="$WORK/machine_${MACHINE}_predictions.tar.gz"
MANIFEST="$WORK/manifest.md"
trap 'rm -rf "$WORK"' EXIT

declare -a FILES=()
if [[ "$MACHINE" == "A" ]]; then
  FILES=(
    outputs/n/movielens-1m/exposure_n_s6000/popmatch_eval/n_valid_predictions.jsonl
    outputs/n/movielens-1m/exposure_n_s6000/popmatch_eval/n_test_predictions.jsonl
    outputs/m/movielens-1m/exposure_m1_s12000/popmatch_eval_valid_only/m_n_valid_predictions.jsonl
    outputs/m/movielens-1m/exposure_m1_s12000/popmatch_eval/m_n_test_predictions.jsonl
  )
else
  FILES=(
    outputs/n/movielens-1m/exposure_n_s12000_seed${SEED}/popmatch_eval/n_valid_predictions.jsonl
    outputs/n/movielens-1m/exposure_n_s12000_seed${SEED}/popmatch_eval/n_test_predictions.jsonl
    outputs/m/movielens-1m/exposure_m1_s24000_seed${SEED}/popmatch_eval/m_n_valid_predictions.jsonl
    outputs/m/movielens-1m/exposure_m1_s24000_seed${SEED}/popmatch_eval/m_n_test_predictions.jsonl
    outputs/phase2a/multiseed96_ranking_robustness/seed${SEED}/n_k0_k20_seed42/n_valid_predictions.jsonl
    outputs/phase2a/multiseed96_ranking_robustness/seed${SEED}/n_k0_k20_seed42/n_test_predictions.jsonl
    outputs/phase2a/multiseed96_ranking_robustness/seed${SEED}/m1_k20_seed42/m_n_valid_predictions.jsonl
    outputs/phase2a/multiseed96_ranking_robustness/seed${SEED}/m1_k20_seed42/m_n_test_predictions.jsonl
    outputs/phase2a/multiseed96_ranking_robustness/seed${SEED}/n_k0_k50_seed42/n_valid_predictions.jsonl
    outputs/phase2a/multiseed96_ranking_robustness/seed${SEED}/n_k0_k50_seed42/n_test_predictions.jsonl
    outputs/phase2a/multiseed96_ranking_robustness/seed${SEED}/m1_k50_seed42/m_n_valid_predictions.jsonl
    outputs/phase2a/multiseed96_ranking_robustness/seed${SEED}/m1_k50_seed42/m_n_test_predictions.jsonl
  )
fi

for rel in "${FILES[@]}"; do
  path="$ROOT/$rel"
  [[ -f "$path" ]] || { echo "MISSING $path" >&2; exit 3; }
  rows="$(wc -l < "$path")"
  [[ "$rows" == "5675" ]] || { echo "BAD_ROW_COUNT rows=$rows path=$path" >&2; exit 4; }
done

tar -C "$ROOT" -czf "$ARCHIVE" "${FILES[@]}"
split -b 45m -d -a 2 "$ARCHIVE" "$WORK/predictions.tar.gz.part-"

{
  echo "# Missing Prediction Bundle: Machine $MACHINE"
  echo
  echo "- generated_utc: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "- hostname: $(hostname)"
  echo "- machine: $MACHINE"
  echo "- seed: $SEED"
  echo "- repository_head: $(git -C "$ROOT" rev-parse HEAD 2>/dev/null || echo UNKNOWN)"
  echo "- training_invoked: NO"
  echo "- inference_invoked: NO"
  echo "- evaluation_invoked: NO"
  echo "- archive_bytes: $(stat -c %s "$ARCHIVE")"
  echo "- archive_sha256: $(sha256sum "$ARCHIVE" | awk '{print $1}')"
  echo
  echo "## Source files"
  echo
  for rel in "${FILES[@]}"; do
    path="$ROOT/$rel"
    echo "- $rel | bytes=$(stat -c %s "$path") | rows=$(wc -l < "$path") | sha256=$(sha256sum "$path" | awk '{print $1}')"
  done
  echo
  echo "## Archive parts"
  echo
  for part in "$WORK"/predictions.tar.gz.part-*; do
    echo "- $(basename "$part") | bytes=$(stat -c %s "$part") | sha256=$(sha256sum "$part" | awk '{print $1}')"
  done
  echo
  echo "## Restore"
  echo
  echo '```bash'
  echo 'cat predictions.tar.gz.part-* > predictions.tar.gz'
  echo 'sha256sum predictions.tar.gz'
  echo 'tar -tzf predictions.tar.gz'
  echo '```'
} > "$MANIFEST"

git clone --quiet --filter=blob:none --no-checkout "$REMOTE" "$PUBLISH"
git -C "$PUBLISH" config user.name "LlamaRec Artifact Reporter"
git -C "$PUBLISH" config user.email "artifact-reporter@llamarec.local"
if git -C "$PUBLISH" ls-remote --exit-code --heads origin "$BRANCH" >/dev/null 2>&1; then
  git -C "$PUBLISH" fetch --quiet origin "$BRANCH"
  git -C "$PUBLISH" switch --quiet -c "$BRANCH" --track "origin/$BRANCH"
else
  git -C "$PUBLISH" checkout --quiet origin/main
  git -C "$PUBLISH" switch --quiet -c "$BRANCH"
fi

DEST="$PUBLISH/paper/metadata/missing_prediction_bundles/machine_${MACHINE}"
mkdir -p "$DEST"
cp "$MANIFEST" "$DEST/manifest.md"
cp "$WORK"/predictions.tar.gz.part-* "$DEST/"
git -C "$PUBLISH" add -f "paper/metadata/missing_prediction_bundles/machine_${MACHINE}"
git -C "$PUBLISH" commit --quiet -m "Add machine $MACHINE missing prediction bundle"
git -C "$PUBLISH" push --quiet -u origin "$BRANCH"
echo "BUNDLE_PUSHED branch=$BRANCH archive_sha256=$(sha256sum "$ARCHIVE" | awk '{print $1}')"
