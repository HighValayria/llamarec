"""Build leakage-free N-evaluation masks and reuse existing paired predictions.

This script performs no training or model inference. It treats the first 48k/96k
Y records as the Y exposure consumed by the sequential 1:1 M1 runs.
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable

import numpy as np


ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "paper/plan/task-packets/m1-clean-subset-audit"
Y_TRAIN = ROOT / "data/processed/movielens-1m/preference_train.jsonl"
N_TRAIN = ROOT / "data/processed/movielens-1m/next_item_train.jsonl"
N_EVAL = {
    "validation": ROOT / "data/processed/movielens-1m/next_item_valid.jsonl",
    "test": ROOT / "data/processed/movielens-1m/next_item_test.jsonl",
}
PREDICTION_ROOT = ROOT / ".agent/.agent/exposure_scaling/analysis_handoff"
EXPOSURES = (48000, 96000)
VARIANTS = ("k5", "k20", "k50")
BOOTSTRAP_SEED = 20260902
BOOTSTRAP_REPLICATES = 5000


def load_jsonl(path: Path, limit: int | None = None) -> list[dict[str, Any]]:
    rows = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if limit is not None and len(rows) >= limit:
                break
            rows.append(json.loads(line))
    return rows


def event_id(user_id: object, event: dict[str, Any]) -> tuple[str, str, int, int, float]:
    return (
        str(user_id),
        str(event["movie_id"]),
        int(event["timestamp"]),
        int(event.get("sequence_index", -1)),
        float(event["rating"]),
    )


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def y_indexes(rows: Iterable[dict[str, Any]]) -> dict[str, Any]:
    targets: set[tuple[str, str, int, int, float]] = set()
    max_target_timestamp: dict[str, int] = {}
    later_history_events: set[tuple[str, str, int, int, float]] = set()
    for record in rows:
        user = str(record["user_id"])
        target = record["target"]
        target_ts = int(target["timestamp"])
        targets.add(event_id(user, target))
        max_target_timestamp[user] = max(max_target_timestamp.get(user, -1), target_ts)
        for history_event in record.get("history", []):
            later_history_events.add(event_id(user, history_event))
    return {
        "targets": targets,
        "max_target_timestamp": max_target_timestamp,
        "later_history_events": later_history_events,
    }


def build_mask(
    eval_rows: list[dict[str, Any]], indexes: dict[str, Any], exposure: int, split: str
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    mask_rows = []
    for record in eval_rows:
        user = str(record["user_id"])
        target = record["target"]
        identity = event_id(user, target)
        eval_ts = int(target["timestamp"])
        max_y_ts = indexes["max_target_timestamp"].get(user)
        violation_a = identity in indexes["targets"]
        violation_b = identity in indexes["later_history_events"]
        violation_c = max_y_ts is not None and max_y_ts >= eval_ts
        clean = not violation_c
        mask_rows.append(
            {
                "exposure": exposure,
                "split": split,
                "user_id": user,
                "target_movie_id": str(target["movie_id"]),
                "target_timestamp": eval_ts,
                "target_sequence_index": int(target.get("sequence_index", -1)),
                "clean": int(clean),
                "max_m1_y_target_timestamp": "" if max_y_ts is None else max_y_ts,
                "violation_a_exact_training_target": int(violation_a),
                "violation_b_present_in_later_y_history": int(violation_b),
                "violation_c_same_user_y_target_at_or_after": int(violation_c),
                "reason": "retained" if clean else "same_user_y_target_at_or_after_eval",
            }
        )
    retained = [row for row in mask_rows if row["clean"] == 1]
    summary = {
        "exposure": exposure,
        "split": split,
        "original_examples": len(mask_rows),
        "clean_examples": len(retained),
        "removed_examples": len(mask_rows) - len(retained),
        "clean_ratio": len(retained) / len(mask_rows),
        "unique_users_original": len({row["user_id"] for row in mask_rows}),
        "unique_users_clean": len({row["user_id"] for row in retained}),
        "retained_violation_a": sum(row["violation_a_exact_training_target"] for row in retained),
        "retained_violation_b": sum(row["violation_b_present_in_later_y_history"] for row in retained),
        "retained_violation_c": sum(row["violation_c_same_user_y_target_at_or_after"] for row in retained),
    }
    return mask_rows, summary


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def metric_mean(rows: list[dict[str, str]], key: str) -> float:
    return sum(float(row[key]) for row in rows) / len(rows)


def metric_block(rows: list[dict[str, str]]) -> dict[str, Any]:
    metrics = {}
    for metric in ("HR@1", "NDCG@5", "MRR"):
        n_value = metric_mean(rows, f"n96_{metric}")
        m_value = metric_mean(rows, f"m96_{metric}")
        metrics[metric] = {"N96": n_value, "M1-96": m_value, "delta_N_minus_M1": n_value - m_value}
    return metrics


def percentile(values: list[float], percent: float) -> float:
    ordered = sorted(values)
    position = (len(ordered) - 1) * percent / 100.0
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return ordered[lower]
    return ordered[lower] * (upper - position) + ordered[upper] * (position - lower)


def bootstrap(rows: list[dict[str, str]], variant: str, split: str) -> list[dict[str, Any]]:
    groups: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        groups[row["user_id"]].append(row)
    users = list(groups)
    variant_offset = {"k5": 0, "k20": 1000, "k50": 2000}[variant]
    split_offset = {"valid": 0, "test": 10000}[split]
    rng = np.random.default_rng(BOOTSTRAP_SEED + variant_offset + split_offset)
    metric_names = ("HR@1", "NDCG@5", "MRR")
    per_user = np.asarray(
        [
            [
                sum(float(row[f"n96_{metric}"]) - float(row[f"m96_{metric}"]) for row in groups[user])
                / len(groups[user])
                for metric in metric_names
            ]
            for user in users
        ],
        dtype=float,
    )
    distributions = {metric: [] for metric in metric_names}
    batch_size = 100
    for start in range(0, BOOTSTRAP_REPLICATES, batch_size):
        current = min(batch_size, BOOTSTRAP_REPLICATES - start)
        indexes = rng.integers(0, len(users), size=(current, len(users)))
        sampled_means = per_user[indexes].mean(axis=1)
        for metric_index, metric in enumerate(metric_names):
            distributions[metric].extend(sampled_means[:, metric_index].tolist())
    point = metric_block(rows)
    output = []
    for metric, values in distributions.items():
        output.append(
            {
                "variant": variant,
                "split": split,
                "metric": metric,
                "delta_definition": "N96 - M1-96",
                "point_estimate": point[metric]["delta_N_minus_M1"],
                "bootstrap_mean": sum(values) / len(values),
                "ci95_low": percentile(values, 2.5),
                "ci95_high": percentile(values, 97.5),
                "p_delta_gt_0": sum(value > 0 for value in values) / len(values),
                "bootstrap_unit": "user",
                "replicates": BOOTSTRAP_REPLICATES,
                "sample_count": len(rows),
                "user_count": len(users),
            }
        )
    return output


def check_n_branch(n_train: list[dict[str, Any]], eval_rows: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
    train_targets = {event_id(row["user_id"], row["target"]) for row in n_train}
    train_history = {
        event_id(row["user_id"], event)
        for row in n_train
        for event in row.get("history", [])
    }
    output = {}
    for split, records in eval_rows.items():
        heldout = {event_id(row["user_id"], row["target"]) for row in records}
        output[split] = {
            "eval_targets_in_n_train_targets": len(heldout & train_targets),
            "eval_targets_in_n_train_histories": len(heldout & train_history),
        }
    return output


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    eval_rows = {split: load_jsonl(path) for split, path in N_EVAL.items()}
    n_train = load_jsonl(N_TRAIN)
    mask_summaries = []
    clean_keys: dict[tuple[int, str], set[tuple[str, str]]] = {}
    for exposure in EXPOSURES:
        indexes = y_indexes(load_jsonl(Y_TRAIN, exposure))
        for split, records in eval_rows.items():
            mask_rows, summary = build_mask(records, indexes, exposure, split)
            write_csv(OUT / f"n_{split}_clean_mask_m1_{exposure // 1000}.csv", mask_rows)
            mask_summaries.append(summary)
            clean_keys[(exposure, split)] = {
                (row["user_id"], row["target_movie_id"])
                for row in mask_rows
                if row["clean"] == 1
            }

    prediction_availability = []
    seed42_results = []
    bootstrap_rows = []
    for variant in VARIANTS:
        for split in ("valid", "test"):
            path = PREDICTION_ROOT / f"ranking_predictions_{variant}_{split}.csv"
            available = path.exists()
            prediction_availability.append(
                {
                    "seed": 42,
                    "comparison": "N96_vs_M1-96",
                    "variant": variant,
                    "split": split,
                    "available": available,
                    "path": path.relative_to(ROOT).as_posix(),
                }
            )
            if available:
                rows = read_csv(path)
                keys = clean_keys[(96000, "validation" if split == "valid" else "test")]
                filtered = [row for row in rows if (row["user_id"], row["ground_truth_movie_id"]) in keys]
                seed42_results.append(
                    {
                        "variant": variant,
                        "split": split,
                        "rows_original": len(rows),
                        "rows_clean": len(filtered),
                        "metrics": metric_block(filtered),
                    }
                )
                bootstrap_rows.extend(bootstrap(filtered, variant, split))

    for seed, comparison in ((42, "N48_vs_M1-48"), (43, "N96_vs_M1-96"), (44, "N96_vs_M1-96")):
        for variant in VARIANTS:
            for split in ("valid", "test"):
                prediction_availability.append(
                    {
                        "seed": seed,
                        "comparison": comparison,
                        "variant": variant,
                        "split": split,
                        "available": False,
                        "path": None,
                    }
                )

    payload = {
        "audit_semantics": {
            "clean_definition": "no M1 Y-branch training target for the same user has timestamp >= N evaluation target timestamp",
            "m1_sampling": "ratio_ordered_y_n_examples with SequentialSampler, batch_size=1, gradient_accumulation=8",
            "m1_exposure_mapping": {"M1-48": "first 48000 Y and first 48000 N records", "M1-96": "first 96000 Y and first 96000 N records"},
            "training": False,
            "inference": False,
            "new_checkpoint": False,
        },
        "input_hashes": {str(path.relative_to(ROOT)): sha256(path) for path in (Y_TRAIN, N_TRAIN, *N_EVAL.values())},
        "mask_summaries": mask_summaries,
        "n_branch_split_verification": check_n_branch(n_train, eval_rows),
        "prediction_availability": prediction_availability,
        "seed42_clean_results": seed42_results,
        "seed42_clean_bootstrap": bootstrap_rows,
        "multiseed_clean_summary": None,
        "multiseed_unavailable_reason": "seed43/44 row-level predictions are absent locally; summary metrics cannot be filtered by the clean mask",
        "verdict": "CLEAN_SUBSET_NOT_FEASIBLE",
        "verdict_reason": "The clean subset exists and seed42 N96/M1-96 can be recomputed, but required N48/M1-48 and seed43/44 row-level predictions are absent; inference is prohibited.",
    }
    (OUT / "audit_summary.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_csv(OUT / "seed42_clean_bootstrap.csv", bootstrap_rows)
    print(json.dumps(payload, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
