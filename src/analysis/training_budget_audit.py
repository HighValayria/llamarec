"""Audit training exposure for fair-budget baseline positioning."""

from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path
from typing import Any

from src.data.config import load_experiment_config


UNAVAILABLE = "unavailable"
NOT_RECOVERABLE = "not recoverable"


def run_training_budget_audit(
    config_path: str | Path,
    output_dir: str | Path | None = None,
) -> dict[str, Any]:
    """Write CSV and Markdown artifacts for the current budget audit."""

    config = load_experiment_config(config_path)
    repo_root = Path(config["_repo_root"])
    output_path = _resolve_output_dir(repo_root, output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    rows = _audit_rows(repo_root)
    payload = {
        "dataset": "movielens-1m",
        "comparison_scope": "Fair-Budget Baseline Positioning Workstream A",
        "rows": rows,
        "answers": _answer_rows(rows),
        "notes": _notes(),
    }

    csv_path = output_path / "training_budget_audit.csv"
    markdown_path = output_path / "training_budget_audit.md"
    json_path = output_path / "training_budget_audit.json"
    _write_csv(csv_path, rows)
    _write_json(json_path, payload)
    _write_markdown(markdown_path, payload)

    return {
        "dataset": "movielens-1m",
        "rows": len(rows),
        "paths": {
            "csv": str(csv_path),
            "json": str(json_path),
            "markdown": str(markdown_path),
        },
    }


def _audit_rows(repo_root: Path) -> list[dict[str, Any]]:
    next_item_train_size = _count_lines(repo_root / "data/processed/movielens-1m/next_item_train.jsonl")
    preference_train_size = _count_lines(
        repo_root / "data/processed/movielens-1m/preference_train.jsonl"
    )
    n_loaded = 200_000
    m_y_loaded = 200_000
    m_n_loaded = 200_000
    llm_per_device_batch = 1
    llm_gradient_accumulation = 8
    llm_effective_batch = llm_per_device_batch * llm_gradient_accumulation

    rows: list[dict[str, Any]] = [
        {
            "model": "N-K0",
            "run": "outputs/n/movielens-1m/pool200k_1m_n_1500",
            "evidence_status": "stage-local report; formal trainer_state not present in local workspace",
            "optimizer_steps": 1500,
            "per_device_batch_size": llm_per_device_batch,
            "gradient_accumulation_steps": llm_gradient_accumulation,
            "effective_batch_size": llm_effective_batch,
            "world_size_or_gpu_count": 1,
            "training_dataset_size": next_item_train_size,
            "loaded_training_instances": n_loaded,
            "processed_training_instances_total": 1500 * llm_effective_batch,
            "processed_n_instances": 1500 * llm_effective_batch,
            "processed_y_instances": 0,
            "unique_training_instances_seen": NOT_RECOVERABLE,
            "equivalent_epochs_loaded_pool": _ratio(1500 * llm_effective_batch, n_loaded),
            "equivalent_epochs_full_dataset": _ratio(1500 * llm_effective_batch, next_item_train_size),
            "mean_exposure_per_loaded_instance": _ratio(1500 * llm_effective_batch, n_loaded),
            "wall_clock_training_time": UNAVAILABLE,
            "gpu_model": UNAVAILABLE,
            "total_parameters": "3B base model plus LoRA adapter",
            "trainable_parameters": UNAVAILABLE,
            "total_processed_tokens": UNAVAILABLE,
            "mean_sequence_length": UNAVAILABLE,
            "median_sequence_length": UNAVAILABLE,
            "task_schedule": "N only; HF Trainer sampler state not locally recoverable",
            "source": ".agent/strict_aligned_sasrec_llm_report.md; src/train/train_n.py",
        },
        {
            "model": "M1",
            "run": "outputs/m/movielens-1m/diag_m1_1m_m_200k_3000",
            "evidence_status": "stage-local report; formal trainer_state not present in local workspace",
            "optimizer_steps": 3000,
            "per_device_batch_size": llm_per_device_batch,
            "gradient_accumulation_steps": llm_gradient_accumulation,
            "effective_batch_size": llm_effective_batch,
            "world_size_or_gpu_count": 1,
            "training_dataset_size": f"Y={preference_train_size}; N={next_item_train_size}",
            "loaded_training_instances": m_y_loaded + m_n_loaded,
            "processed_training_instances_total": 3000 * llm_effective_batch,
            "processed_n_instances": 1500 * llm_effective_batch,
            "processed_y_instances": 1500 * llm_effective_batch,
            "unique_training_instances_seen": "Y=12000; N=12000 under sequential 1:1 schedule",
            "equivalent_epochs_loaded_pool": _ratio(3000 * llm_effective_batch, m_y_loaded + m_n_loaded),
            "equivalent_epochs_full_dataset": (
                f"Y={_ratio(1500 * llm_effective_batch, preference_train_size)}; "
                f"N={_ratio(1500 * llm_effective_batch, next_item_train_size)}"
            ),
            "mean_exposure_per_loaded_instance": (
                f"Y={_ratio(1500 * llm_effective_batch, m_y_loaded)}; "
                f"N={_ratio(1500 * llm_effective_batch, m_n_loaded)}"
            ),
            "wall_clock_training_time": UNAVAILABLE,
            "gpu_model": UNAVAILABLE,
            "total_parameters": "3B base model plus LoRA adapter",
            "trainable_parameters": UNAVAILABLE,
            "total_processed_tokens": UNAVAILABLE,
            "mean_sequence_length": UNAVAILABLE,
            "median_sequence_length": UNAVAILABLE,
            "task_schedule": "ratio_ordered_y_n_examples, 1:1; 1500 Y updates and 1500 N updates",
            "source": ".agent/strict_aligned_sasrec_llm_report.md; src/train/train_m.py",
        },
        _sasrec_row(
            label="SASRec s1500",
            optimizer_steps=1500,
            train_pool_size=200_000,
            full_train_size=next_item_train_size,
            source=".agent/strict_aligned_sasrec_llm_report.md; src/baselines/sasrec.py",
        ),
        _sasrec_row(
            label="SASRec s3000",
            optimizer_steps=3000,
            train_pool_size=200_000,
            full_train_size=next_item_train_size,
            source=".agent/strict_aligned_sasrec_llm_report.md; src/baselines/sasrec.py",
        ),
    ]
    return rows


def _sasrec_row(
    label: str,
    optimizer_steps: int,
    train_pool_size: int,
    full_train_size: int,
    source: str,
) -> dict[str, Any]:
    batch_size = 512
    processed = sasrec_processed_instances(
        train_examples=train_pool_size,
        batch_size=batch_size,
        optimizer_steps=optimizer_steps,
    )
    return {
        "model": label,
        "run": f"outputs/baselines/movielens-1m/sasrec_fixed_popmatch_k5_200k_s{optimizer_steps}_eval",
        "evidence_status": "stage-local report plus SASRec training-loop calculation; run directory not present in local workspace",
        "optimizer_steps": optimizer_steps,
        "per_device_batch_size": batch_size,
        "gradient_accumulation_steps": 1,
        "effective_batch_size": batch_size,
        "world_size_or_gpu_count": 1,
        "training_dataset_size": full_train_size,
        "loaded_training_instances": train_pool_size,
        "processed_training_instances_total": processed,
        "processed_n_instances": processed,
        "processed_y_instances": 0,
        "unique_training_instances_seen": train_pool_size,
        "equivalent_epochs_loaded_pool": _ratio(processed, train_pool_size),
        "equivalent_epochs_full_dataset": _ratio(processed, full_train_size),
        "mean_exposure_per_loaded_instance": _ratio(processed, train_pool_size),
        "wall_clock_training_time": UNAVAILABLE,
        "gpu_model": UNAVAILABLE,
        "total_parameters": 489_171,
        "trainable_parameters": 489_171,
        "total_processed_tokens": "not applicable",
        "mean_sequence_length": 10,
        "median_sequence_length": UNAVAILABLE,
        "task_schedule": "N only; SASRec shuffled full pool each epoch, no gradient accumulation",
        "source": source,
    }


def sasrec_processed_instances(
    train_examples: int,
    batch_size: int,
    optimizer_steps: int,
) -> int:
    """Return exact SASRec row exposures under the current training loop."""

    if train_examples <= 0:
        raise ValueError("train_examples must be positive")
    if batch_size <= 0:
        raise ValueError("batch_size must be positive")
    if optimizer_steps < 0:
        raise ValueError("optimizer_steps must be non-negative")
    full_batches, remainder = divmod(train_examples, batch_size)
    batches_per_epoch = full_batches + (1 if remainder else 0)
    complete_epochs, partial_steps = divmod(optimizer_steps, batches_per_epoch)
    processed = complete_epochs * train_examples
    processed += min(partial_steps, full_batches) * batch_size
    if partial_steps > full_batches:
        processed += remainder
    return processed


def _answer_rows(rows: list[dict[str, Any]]) -> dict[str, Any]:
    by_model = {row["model"]: row for row in rows}
    n_exposure = int(by_model["N-K0"]["processed_n_instances"])
    s1500_exposure = int(by_model["SASRec s1500"]["processed_n_instances"])
    s3000_exposure = int(by_model["SASRec s3000"]["processed_n_instances"])
    m1_n_exposure = int(by_model["M1"]["processed_n_instances"])
    return {
        "sasrec_s1500_vs_n_k0_n_exposure_ratio": _ratio(s1500_exposure, n_exposure),
        "sasrec_s1500_minus_n_k0_n_exposures": s1500_exposure - n_exposure,
        "sasrec_s3000_vs_n_k0_n_exposure_ratio": _ratio(s3000_exposure, n_exposure),
        "sasrec_s3000_minus_n_k0_n_exposures": s3000_exposure - n_exposure,
        "m1_n_task_processed_instances": m1_n_exposure,
        "m1_y_task_processed_instances": int(by_model["M1"]["processed_y_instances"]),
        "m1_y_n_update_ratio": "1:1",
    }


def _notes() -> list[str]:
    return [
        "Do not use optimizer steps alone as training budget.",
        "N-K0 and M1 formal trainer_state/config files are not present in this local workspace; fields not recoverable from stage-local evidence are marked unavailable.",
        "LLM processed instance counts use the recorded train_batch_size=1, max/global steps, and the script-level gradient_accumulation_steps=8.",
        "SASRec processed instance counts account for the short final batch in each 200000-example epoch at batch size 512.",
        "Parameter counts are directly known only for SASRec from architecture dimensions; LLM trainable parameter counts require missing formal metrics or adapter metadata.",
    ]


def _count_lines(path: Path) -> int:
    with path.open("r", encoding="utf-8") as handle:
        return sum(1 for _ in handle)


def _ratio(numerator: int | float, denominator: int | float) -> float:
    if denominator == 0:
        return math.nan
    return round(float(numerator) / float(denominator), 6)


def _resolve_output_dir(repo_root: Path, output_dir: str | Path | None) -> Path:
    path = Path(output_dir) if output_dir is not None else Path(
        "outputs/fair_budget_baseline_positioning"
    )
    if path.is_absolute():
        return path
    return repo_root / path


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fieldnames = [
        "model",
        "run",
        "evidence_status",
        "optimizer_steps",
        "per_device_batch_size",
        "gradient_accumulation_steps",
        "effective_batch_size",
        "world_size_or_gpu_count",
        "training_dataset_size",
        "loaded_training_instances",
        "processed_training_instances_total",
        "processed_n_instances",
        "processed_y_instances",
        "unique_training_instances_seen",
        "equivalent_epochs_loaded_pool",
        "equivalent_epochs_full_dataset",
        "mean_exposure_per_loaded_instance",
        "wall_clock_training_time",
        "gpu_model",
        "total_parameters",
        "trainable_parameters",
        "total_processed_tokens",
        "mean_sequence_length",
        "median_sequence_length",
        "task_schedule",
        "source",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def _write_markdown(path: Path, payload: dict[str, Any]) -> None:
    rows = payload["rows"]
    answers = payload["answers"]
    lines = [
        "# Training Budget Audit",
        "",
        "## Scope",
        "",
        "- Models: N-K0, M1, SASRec s1500, SASRec s3000.",
        "- Dataset: MovieLens-1M.",
        "- Purpose: quantify sample exposure mismatch in the current step-aligned diagnostic.",
        "",
        "## Budget Table",
        "",
        "| Model | Optimizer steps | Effective batch | Loaded train instances | Processed total | Processed N | Processed Y | Equivalent epochs on loaded pool | Evidence status |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in rows:
        lines.append(
            f"| {row['model']} | {row['optimizer_steps']} | {row['effective_batch_size']} | "
            f"{row['loaded_training_instances']} | {row['processed_training_instances_total']} | "
            f"{row['processed_n_instances']} | {row['processed_y_instances']} | "
            f"{row['equivalent_epochs_loaded_pool']} | {row['evidence_status']} |"
        )

    lines += [
        "",
        "## Direct Answers",
        "",
        f"- SASRec s1500 saw {answers['sasrec_s1500_vs_n_k0_n_exposure_ratio']}x the N-task instance exposure of N-K0, a difference of {answers['sasrec_s1500_minus_n_k0_n_exposures']} instances.",
        f"- SASRec s3000 saw {answers['sasrec_s3000_vs_n_k0_n_exposure_ratio']}x the N-task instance exposure of N-K0, a difference of {answers['sasrec_s3000_minus_n_k0_n_exposures']} instances.",
        f"- M1 received {answers['m1_n_task_processed_instances']} N-task processed instances and {answers['m1_y_task_processed_instances']} Y-task processed instances, with a Y:N update ratio of {answers['m1_y_n_update_ratio']}.",
        "",
        "## Missing Evidence",
        "",
        "- LLM formal trainer_state/config files are not present in this local workspace.",
        "- Wall-clock time, GPU model for the formal runs, trainable adapter parameter count, and exact token counts are unavailable from current local evidence.",
        "",
        "## Boundary",
        "",
        "This audit shows that the current optimizer-step-aligned SASRec comparison has a large N-sample-exposure mismatch. It does not by itself establish compute-matched or sample-exposure-matched superiority.",
        "",
        "## Notes",
        "",
    ]
    lines.extend(f"- {note}" for note in payload["notes"])
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Write training budget audit artifacts")
    parser.add_argument("--config", default="configs/experiment.yaml")
    parser.add_argument("--output-dir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    summary = run_training_budget_audit(
        config_path=args.config,
        output_dir=args.output_dir,
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
