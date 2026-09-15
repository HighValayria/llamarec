"""Combine verified seed42 clean results with recovered seed43/44 results."""

from __future__ import annotations

import csv
import json
import statistics
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
AUDIT_DIR = ROOT / "paper/plan/task-packets/m1-clean-subset-audit"
METRICS = ("HR@1", "NDCG@5", "MRR")


def seed42_rows() -> list[dict[str, Any]]:
    source = json.loads((AUDIT_DIR / "audit_summary.json").read_text(encoding="utf-8"))
    rows = []
    for result in source["seed42_clean_results"]:
        for metric, values in result["metrics"].items():
            rows.append(
                {
                    "seed": 42,
                    "variant": result["variant"],
                    "split": result["split"],
                    "metric": metric,
                    "delta_N_minus_M1": float(values["delta_N_minus_M1"]),
                }
            )
    return rows


def recovered_rows() -> list[dict[str, Any]]:
    path = AUDIT_DIR / "recovered_clean_per_seed.csv"
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return [
            {
                "seed": int(row["seed"]),
                "variant": row["variant"],
                "split": row["split"],
                "metric": row["metric"],
                "delta_N_minus_M1": float(row["delta_N_minus_M1"]),
            }
            for row in csv.DictReader(handle)
            if int(row["exposure"]) == 96000
        ]


def main() -> None:
    source = seed42_rows() + recovered_rows()
    output = []
    for variant in ("k5", "k20", "k50"):
        for split in ("valid", "test"):
            for metric in METRICS:
                selected = [
                    row
                    for row in source
                    if row["variant"] == variant
                    and row["split"] == split
                    and row["metric"] == metric
                ]
                seeds = {row["seed"] for row in selected}
                if seeds != {42, 43, 44}:
                    raise ValueError(f"incomplete seeds for {variant}/{split}/{metric}: {sorted(seeds)}")
                deltas = [row["delta_N_minus_M1"] for row in selected]
                output.append(
                    {
                        "variant": variant,
                        "split": split,
                        "metric": metric,
                        "seeds": "42,43,44",
                        "delta_mean": statistics.fmean(deltas),
                        "delta_sample_sd": statistics.stdev(deltas),
                        "seed42_delta": next(row["delta_N_minus_M1"] for row in selected if row["seed"] == 42),
                        "seed43_delta": next(row["delta_N_minus_M1"] for row in selected if row["seed"] == 43),
                        "seed44_delta": next(row["delta_N_minus_M1"] for row in selected if row["seed"] == 44),
                        "positive_seed_count": sum(value > 0 for value in deltas),
                    }
                )
    csv_path = AUDIT_DIR / "clean_multiseed_96_summary.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(output[0]))
        writer.writeheader()
        writer.writerows(output)
    json_path = AUDIT_DIR / "clean_multiseed_96_summary.json"
    json_path.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
