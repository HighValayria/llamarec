"""Analyze recovered row-level predictions on the existing M1 clean masks.

This script performs deterministic metric aggregation only. It does not train,
run model inference, regenerate candidates, or bootstrap confidence intervals.
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
import statistics
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
AUDIT_DIR = ROOT / "paper/plan/task-packets/m1-clean-subset-audit"
IMPORT_ROOT = ROOT / ".agent/missing_prediction_bundles_imported"
OUTPUT_JSON = AUDIT_DIR / "recovered_clean_summary.json"
OUTPUT_PER_SEED = AUDIT_DIR / "recovered_clean_per_seed.csv"
OUTPUT_MULTISEED = AUDIT_DIR / "recovered_clean_multiseed.csv"

METRICS = ("HR@1", "NDCG@5", "MRR")


def prediction_paths() -> dict[tuple[int, str, str], tuple[Path, Path]]:
    paths: dict[tuple[int, str, str], tuple[Path, Path]] = {}
    a = IMPORT_ROOT / "machine_A/payload"
    paths[(42, "k5", "valid")] = (
        a / "outputs/n/movielens-1m/exposure_n_s6000/popmatch_eval/n_valid_predictions.jsonl",
        a / "outputs/m/movielens-1m/exposure_m1_s12000/popmatch_eval_valid_only/m_n_valid_predictions.jsonl",
    )
    paths[(42, "k5", "test")] = (
        a / "outputs/n/movielens-1m/exposure_n_s6000/popmatch_eval/n_test_predictions.jsonl",
        a / "outputs/m/movielens-1m/exposure_m1_s12000/popmatch_eval/m_n_test_predictions.jsonl",
    )
    for seed, machine in ((43, "B"), (44, "C")):
        base = IMPORT_ROOT / f"machine_{machine}/payload"
        for split in ("valid", "test"):
            paths[(seed, "k5", split)] = (
                base / f"outputs/n/movielens-1m/exposure_n_s12000_seed{seed}/popmatch_eval/n_{split}_predictions.jsonl",
                base / f"outputs/m/movielens-1m/exposure_m1_s24000_seed{seed}/popmatch_eval/m_n_{split}_predictions.jsonl",
            )
            for variant in ("k20", "k50"):
                paths[(seed, variant, split)] = (
                    base / f"outputs/phase2a/multiseed96_ranking_robustness/seed{seed}/n_k0_{variant}_seed42/n_{split}_predictions.jsonl",
                    base / f"outputs/phase2a/multiseed96_ranking_robustness/seed{seed}/m1_{variant}_seed42/m_n_{split}_predictions.jsonl",
                )
    return paths


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle]


def clean_keys(exposure: int, split: str) -> set[tuple[str, str]]:
    mask_split = "validation" if split == "valid" else "test"
    path = AUDIT_DIR / f"n_{mask_split}_clean_mask_m1_{exposure // 1000}.csv"
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return {
            (row["user_id"], row["target_movie_id"])
            for row in csv.DictReader(handle)
            if row["clean"] == "1"
        }


def index_predictions(rows: list[dict[str, Any]], path: Path) -> dict[tuple[str, str], dict[str, Any]]:
    indexed: dict[tuple[str, str], dict[str, Any]] = {}
    for row in rows:
        key = (str(row["user_id"]), str(row["ground_truth_movie_id"]))
        if key in indexed:
            raise ValueError(f"duplicate prediction key {key} in {path}")
        indexed[key] = row
    return indexed


def rank(record: dict[str, Any]) -> int:
    scores = [float(value) for value in record["scores"]]
    ground_truth_index = int(record["ground_truth_index"])
    order = sorted(range(len(scores)), key=lambda index: (-scores[index], index))
    return order.index(ground_truth_index) + 1


def metric_values(result_rank: int) -> dict[str, float]:
    return {
        "HR@1": float(result_rank == 1),
        "NDCG@5": 1.0 / math.log2(result_rank + 1) if result_rank <= 5 else 0.0,
        "MRR": 1.0 / result_rank,
    }


def analyze_pair(
    seed: int,
    variant: str,
    split: str,
    n_path: Path,
    m_path: Path,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    n_rows = index_predictions(load_jsonl(n_path), n_path)
    m_rows = index_predictions(load_jsonl(m_path), m_path)
    if set(n_rows) != set(m_rows):
        raise ValueError(f"N/M key mismatch for seed={seed} variant={variant} split={split}")
    exposure = 48000 if seed == 42 else 96000
    retained = clean_keys(exposure, split)
    if not retained <= set(n_rows):
        raise ValueError(f"clean mask contains missing prediction keys for seed={seed} variant={variant} split={split}")

    metric_rows: list[dict[str, Any]] = []
    for key in sorted(retained):
        n_record = n_rows[key]
        m_record = m_rows[key]
        if n_record["candidate_movie_ids"] != m_record["candidate_movie_ids"]:
            raise ValueError(f"candidate order mismatch for {key}")
        if int(n_record["ground_truth_index"]) != int(m_record["ground_truth_index"]):
            raise ValueError(f"ground-truth index mismatch for {key}")
        n_metrics = metric_values(rank(n_record))
        m_metrics = metric_values(rank(m_record))
        metric_rows.append(
            {
                "user_id": key[0],
                "ground_truth_movie_id": key[1],
                **{f"n_{metric}": n_metrics[metric] for metric in METRICS},
                **{f"m_{metric}": m_metrics[metric] for metric in METRICS},
            }
        )

    result: dict[str, Any] = {
        "seed": seed,
        "exposure": exposure,
        "variant": variant,
        "split": split,
        "rows_original": len(n_rows),
        "rows_clean": len(metric_rows),
        "n_path": n_path.relative_to(ROOT).as_posix(),
        "m_path": m_path.relative_to(ROOT).as_posix(),
        "n_sha256": sha256(n_path),
        "m_sha256": sha256(m_path),
        "metrics": {},
    }
    for metric in METRICS:
        n_value = statistics.fmean(row[f"n_{metric}"] for row in metric_rows)
        m_value = statistics.fmean(row[f"m_{metric}"] for row in metric_rows)
        result["metrics"][metric] = {
            "N": n_value,
            "M1": m_value,
            "delta_N_minus_M1": n_value - m_value,
        }
    return metric_rows, result


def flatten_results(results: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for result in results:
        for metric, values in result["metrics"].items():
            rows.append(
                {
                    "seed": result["seed"],
                    "exposure": result["exposure"],
                    "variant": result["variant"],
                    "split": result["split"],
                    "rows_original": result["rows_original"],
                    "rows_clean": result["rows_clean"],
                    "metric": metric,
                    "N": values["N"],
                    "M1": values["M1"],
                    "delta_N_minus_M1": values["delta_N_minus_M1"],
                }
            )
    return rows


def multiseed_rows(flat: list[dict[str, Any]]) -> list[dict[str, Any]]:
    output = []
    for variant in ("k5", "k20", "k50"):
        for split in ("valid", "test"):
            for metric in METRICS:
                selected = [
                    row
                    for row in flat
                    if row["exposure"] == 96000
                    and row["variant"] == variant
                    and row["split"] == split
                    and row["metric"] == metric
                ]
                # Seed 42 is supplied by the already verified paired CSV analysis.
                if len(selected) != 2:
                    raise ValueError(f"expected recovered seed43/44 rows for {variant}/{split}/{metric}")
                output.append(
                    {
                        "variant": variant,
                        "split": split,
                        "metric": metric,
                        "recovered_seeds": "43,44",
                        "delta_mean_seed43_44": statistics.fmean(row["delta_N_minus_M1"] for row in selected),
                        "delta_sample_sd_seed43_44": statistics.stdev(row["delta_N_minus_M1"] for row in selected),
                        "seed43_delta": next(row["delta_N_minus_M1"] for row in selected if row["seed"] == 43),
                        "seed44_delta": next(row["delta_N_minus_M1"] for row in selected if row["seed"] == 44),
                        "positive_seed_count": sum(row["delta_N_minus_M1"] > 0 for row in selected),
                    }
                )
    return output


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    results = []
    for (seed, variant, split), (n_path, m_path) in prediction_paths().items():
        _, result = analyze_pair(seed, variant, split, n_path, m_path)
        results.append(result)
    results.sort(key=lambda row: (row["seed"], row["variant"], row["split"]))
    flat = flatten_results(results)
    multiseed = multiseed_rows(flat)
    payload = {
        "analysis_type": "deterministic clean-subset metric recomputation from recovered predictions",
        "training": False,
        "inference": False,
        "evaluation_model_execution": False,
        "bootstrap": False,
        "pair_count": len(results),
        "source_file_count": len(prediction_paths()) * 2,
        "per_seed_results": results,
        "recovered_seed43_44_summary": multiseed,
    }
    write_csv(OUTPUT_PER_SEED, flat)
    write_csv(OUTPUT_MULTISEED, multiseed)
    OUTPUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
