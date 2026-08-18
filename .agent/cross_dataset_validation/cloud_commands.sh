#!/usr/bin/env bash
set -euo pipefail

cd /root/llamarec
source .venv/bin/activate

echo "== git =="
git rev-parse --short HEAD

echo "== raw Amazon Books files =="
find data/raw/Amazon-books -maxdepth 1 -type f -printf "%p %s bytes\n" | sort

echo "== inspect header =="
python - <<'PY'
import csv, json
from pathlib import Path
p = Path("data/raw/Amazon-books/Amazon_popular_books_dataset.csv")
with p.open(newline="", encoding="utf-8-sig") as f:
    r = csv.DictReader(f)
    first = next(r)
    print(json.dumps({"columns": r.fieldnames, "first_row": first}, ensure_ascii=False, indent=2)[:4000])
PY

echo "== required interaction columns =="
python - <<'PY'
import csv
from pathlib import Path
p = Path("data/raw/Amazon-books/Amazon_popular_books_dataset.csv")
with p.open(newline="", encoding="utf-8-sig") as f:
    cols = csv.DictReader(f).fieldnames or []
lower = {c.lower() for c in cols}
print("has_user_id", bool(lower & {"user_id", "userid", "reviewerid", "reviewer_id"}))
print("has_item_id", bool(lower & {"asin", "item_id", "parent_asin"}))
print("has_rating", "rating" in lower)
print("has_timestamp", "timestamp" in lower or "unixreviewtime" in lower)
print("columns", cols)
PY

echo "== decision =="
echo "STOP before GPU training if has_user_id is False. Current local gate is blocked."
