"""Clean duplicated prediction JSONL files without overwriting originals."""

from __future__ import annotations

import argparse
import csv
import json
import shutil
from collections import defaultdict
from pathlib import Path
from typing import Any

from src.analysis.prediction_file_audit import _is_ranking_record, _rank_or_none, _record_key


def run_prediction_file_clean(
    input_dir: str | Path,
    output_dir: str | Path,
    pattern: str = "*_predictions.jsonl",
) -> dict[str, Any]:
    """Copy ``input_dir`` to ``output_dir`` and deduplicate prediction JSONL files."""

    input_path = Path(input_dir)
    output_path = Path(output_dir)
    if not input_path.exists():
        raise FileNotFoundError(f"input_dir does not exist: {input_path}")
    if input_path.resolve() == output_path.resolve():
        raise ValueError("output_dir must be different from input_dir")

    if output_path.exists():
        shutil.rmtree(output_path)
    shutil.copytree(input_path, output_path)

    rows = []
    for source_path in sorted(input_path.rglob(pattern)):
        relative_path = source_path.relative_to(input_path)
        target_path = output_path / relative_path
        result = _clean_file(source_path, target_path)
        rows.append({"relative_path": str(relative_path), **result})

    manifest_path = output_path / "prediction_file_clean_manifest.csv"
    _write_csv(manifest_path, rows)
    return {
        "input_dir": str(input_path),
        "output_dir": str(output_path),
        "files": len(rows),
        "manifest": str(manifest_path),
    }


def _clean_file(source_path: Path, target_path: Path) -> dict[str, Any]:
    groups: dict[Any, list[dict[str, Any]]] = defaultdict(list)
    original_rows = 0
    for record in _read_jsonl(source_path):
        original_rows += 1
        groups[_record_key(record)].append(record)

    kept = []
    conflict_count = 0
    for key, records in groups.items():
        conflicts = _duplicate_conflicts(records)
        if conflicts:
            conflict_count += 1
            continue
        kept.append(records[0])

    if conflict_count:
        raise ValueError(
            f"{source_path} has {conflict_count} duplicate key groups with conflicting predictions"
        )

    _write_jsonl(target_path, kept)
    return {
        "original_rows": original_rows,
        "clean_rows": len(kept),
        "removed_rows": original_rows - len(kept),
        "unique_keys": len(groups),
    }


def _duplicate_conflicts(records: list[dict[str, Any]]) -> bool:
    if len(records) <= 1:
        return False
    first = records[0]
    if _is_ranking_record(first):
        ranks = [_rank_or_none(record) for record in records]
        return len(set(ranks)) > 1
    signatures = [_binary_signature(record) for record in records]
    return len(set(signatures)) > 1


def _binary_signature(record: dict[str, Any]) -> tuple[Any, ...]:
    return (
        record.get("label"),
        record.get("predicted_label"),
        _optional_float(record.get("p_yes", record.get("score"))),
        _optional_float(record.get("p_no")),
    )


def _optional_float(value: Any) -> float | None:
    if value is None or value == "":
        return None
    return float(value)


def _read_jsonl(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                yield json.loads(line)


def _write_jsonl(path: Path, records: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Clean duplicated prediction JSONL files")
    parser.add_argument("input_dir")
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--pattern", default="*_predictions.jsonl")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    summary = run_prediction_file_clean(
        input_dir=args.input_dir,
        output_dir=args.output_dir,
        pattern=args.pattern,
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
