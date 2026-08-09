"""Audit prediction JSONL files for duplicate writes and rank conflicts."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


def run_prediction_file_audit(
    input_dir: str | Path,
    output_dir: str | Path | None = None,
    pattern: str = "*_predictions.jsonl",
) -> dict[str, Any]:
    """Inspect prediction files below ``input_dir`` and write audit tables."""

    input_path = Path(input_dir)
    if not input_path.exists():
        raise FileNotFoundError(f"input_dir does not exist: {input_path}")

    output_path = Path(output_dir) if output_dir else input_path / "audit"
    output_path.mkdir(parents=True, exist_ok=True)

    rows = [_audit_file(path, input_path) for path in sorted(input_path.rglob(pattern))]
    paths = {
        "csv": output_path / "prediction_file_audit.csv",
        "json": output_path / "prediction_file_audit.json",
        "markdown": output_path / "prediction_file_audit.md",
    }
    _write_csv(paths["csv"], rows)
    _write_json(paths["json"], {"input_dir": str(input_path), "files": rows})
    _write_markdown(paths["markdown"], rows)

    return {
        "input_dir": str(input_path),
        "files": len(rows),
        "paths": {key: str(path) for key, path in paths.items()},
    }


def _audit_file(path: Path, root: Path) -> dict[str, Any]:
    split_counts: Counter[str] = Counter()
    groups: dict[Any, list[int | None]] = defaultdict(list)
    row_count = 0
    ranking_rows = 0
    binary_rows = 0

    for record in _read_jsonl(path):
        row_count += 1
        split_counts[str(record.get("split"))] += 1
        if _is_ranking_record(record):
            ranking_rows += 1
        else:
            binary_rows += 1
        groups[_record_key(record)].append(_rank_or_none(record))

    duplicate_dist = Counter(len(values) for values in groups.values())
    rank_conflicts = sum(
        1
        for values in groups.values()
        if all(value is not None for value in values) and len(set(values)) > 1
    )
    duplicated_keys = sum(1 for values in groups.values() if len(values) > 1)

    return {
        "path": str(path),
        "relative_path": str(path.relative_to(root)),
        "rows": row_count,
        "unique_keys": len(groups),
        "duplicated_keys": duplicated_keys,
        "ranking_rows": ranking_rows,
        "binary_rows": binary_rows,
        "split_counts": json.dumps(dict(sorted(split_counts.items())), sort_keys=True),
        "duplicate_count_distribution": json.dumps(
            {str(key): duplicate_dist[key] for key in sorted(duplicate_dist)},
            sort_keys=True,
        ),
        "rank_conflicts": rank_conflicts,
        "safe_exact_rank_duplicates": duplicated_keys > 0 and rank_conflicts == 0,
    }


def _record_key(record: dict[str, Any]) -> tuple[Any, ...]:
    if _is_ranking_record(record):
        return (
            str(record.get("split")),
            str(record.get("user_id")),
            str(record.get("ground_truth_movie_id")),
            tuple(str(movie_id) for movie_id in record.get("candidate_movie_ids", [])),
        )
    return (
        str(record.get("split")),
        str(record.get("user_id")),
        str(record.get("target_movie_id")),
        str(record.get("label")),
    )


def _is_ranking_record(record: dict[str, Any]) -> bool:
    return "scores" in record and "ground_truth_index" in record


def _rank_or_none(record: dict[str, Any]) -> int | None:
    if not _is_ranking_record(record):
        return None
    scores = record["scores"]
    ground_truth_index = int(record["ground_truth_index"])
    ranked = sorted(range(len(scores)), key=lambda index: (-float(scores[index]), index))
    return ranked.index(ground_truth_index) + 1


def _read_jsonl(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                yield json.loads(line)


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def _write_markdown(path: Path, rows: list[dict[str, Any]]) -> None:
    lines = [
        "# Prediction File Audit",
        "",
        "| file | rows | unique_keys | duplicated_keys | split_counts | duplicate_count_distribution | rank_conflicts |",
        "|---|---:|---:|---:|---|---|---:|",
    ]
    for row in rows:
        lines.append(
            f"| {row['relative_path']} | {row['rows']} | {row['unique_keys']} | "
            f"{row['duplicated_keys']} | `{row['split_counts']}` | "
            f"`{row['duplicate_count_distribution']}` | {row['rank_conflicts']} |"
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit prediction JSONL files")
    parser.add_argument("input_dir")
    parser.add_argument("--output-dir", default=None)
    parser.add_argument("--pattern", default="*_predictions.jsonl")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    summary = run_prediction_file_audit(
        input_dir=args.input_dir,
        output_dir=args.output_dir,
        pattern=args.pattern,
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
