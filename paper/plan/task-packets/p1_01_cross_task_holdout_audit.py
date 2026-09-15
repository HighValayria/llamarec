"""Read-only event-level cross-task holdout audit for MovieLens-1M."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
PATHS = {
    "Y_train": ROOT / "data/processed/movielens-1m/preference_train.jsonl",
    "Y_validation": ROOT / "data/processed/movielens-1m/preference_valid.jsonl",
    "Y_test": ROOT / "data/processed/movielens-1m/preference_test.jsonl",
    "N_train": ROOT / "data/processed/movielens-1m/next_item_train.jsonl",
    "N_validation": ROOT / "data/processed/movielens-1m/next_item_valid.jsonl",
    "N_test": ROOT / "data/processed/movielens-1m/next_item_test.jsonl",
}


def identity(user_id: object, event: dict) -> tuple[str, str, int, int, float]:
    return (
        str(user_id),
        str(event["movie_id"]),
        int(event["timestamp"]),
        int(event.get("sequence_index", -1)),
        float(event["rating"]),
    )


def load_targets(path: Path) -> tuple[set[tuple], int]:
    targets = set()
    rows = 0
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            record = json.loads(line)
            rows += 1
            user_id = str(record["user_id"])
            targets.add(identity(user_id, record["target"]))
    return targets, rows


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def scan_history_overlap(path: Path, heldout_targets: set[tuple]) -> dict:
    matched_events = set()
    matched_examples = 0
    users = set()
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            record = json.loads(line)
            user_id = str(record["user_id"])
            overlap = {
                identity(user_id, event)
                for event in record.get("history", [])
            } & heldout_targets
            if overlap:
                matched_examples += 1
                matched_events.update(overlap)
                users.add(user_id)
    return {
        "train_examples_with_overlap": matched_examples,
        "overlap_unique_events": len(matched_events),
        "overlap_unique_users": len(users),
        "interpretation": "role overlap only; evaluate target overlap separately",
    }


def event_view(event: tuple) -> dict:
    return dict(
        user_id=event[0],
        movie_id=event[1],
        timestamp=event[2],
        sequence_index=event[3],
        rating=event[4],
    )


def main() -> None:
    loaded = {name: load_targets(path) for name, path in PATHS.items()}
    output = {
        "identity_fields": ["user_id", "movie_id", "timestamp", "sequence_index", "rating"],
        "files": {},
        "target_overlaps": {},
        "history_role_overlaps": {},
    }
    for name, path in PATHS.items():
        output["files"][name] = {
            "path": path.relative_to(ROOT).as_posix(),
            "sha256": file_sha256(path),
            "rows": loaded[name][1],
            "unique_targets": len(loaded[name][0]),
        }

    checks = (
        ("A", "Y_train", "N_validation"),
        ("B", "Y_train", "N_test"),
        ("C", "N_train", "Y_validation"),
        ("D", "N_train", "Y_test"),
    )
    for label, left, right in checks:
        overlap = loaded[left][0] & loaded[right][0]
        output["target_overlaps"][label] = {
            "left": left,
            "right": right,
            "left_count": len(loaded[left][0]),
            "right_count": len(loaded[right][0]),
            "overlap_event_count": len(overlap),
            "overlap_unique_users": len({event[0] for event in overlap}),
            "overlap_rate_of_right": len(overlap) / len(loaded[right][0]),
            "examples": [event_view(event) for event in sorted(overlap)[:5]],
        }

    for train, heldout in (
        ("Y_train", "N_validation"),
        ("Y_train", "N_test"),
        ("N_train", "Y_validation"),
        ("N_train", "Y_test"),
    ):
        output["history_role_overlaps"][f"{train}_history_x_{heldout}_targets"] = (
            scan_history_overlap(PATHS[train], loaded[heldout][0])
        )

    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
