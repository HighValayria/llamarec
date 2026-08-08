"""Phase 1.5 STEP C: grouped diagnostics for binary and ranking outputs."""

from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from datetime import datetime, timezone
import json
from pathlib import Path
from statistics import mean
from typing import Any

from src.analysis.threshold_calibration import (
    binary_metrics_at_threshold,
    find_best_threshold,
)
from src.data.config import (
    load_experiment_config,
    open_text_auto,
    resolve_configured_output_path,
    resolve_repo_path_from_config,
)
from src.eval.ranking_metrics import (
    default_ranking_ks,
    ground_truth_rank,
    ranking_metrics_for_rank,
)
from src.inference.prediction_io import read_jsonl, write_json


SPLIT_TO_FILE = {
    "validation": "valid",
    "valid": "valid",
    "test": "test",
}

BINARY_GROUP_FIELDS = [
    "all",
    "target_label",
    "target_rating",
    "history_length_bucket",
    "history_positive_ratio_bucket",
    "user_activity_bucket",
    "target_popularity_bucket",
    "target_sequence_bucket",
]

RANKING_GROUP_FIELDS = [
    "all",
    "target_rating",
    "ground_truth_position",
    "history_length_bucket",
    "history_positive_ratio_bucket",
    "user_activity_bucket",
    "target_popularity_bucket",
    "target_sequence_bucket",
]


def run_grouped_error_analysis(
    config_path: str | Path,
    dataset_key: str | None = None,
    y_run: str | None = None,
    n_run: str | None = None,
    m_runs: list[str] | None = None,
    m_labels: list[str] | None = None,
    split_name: str = "test",
    threshold_mode: str = "validation_best_f1",
    output_dir: str | Path | None = None,
    min_group_samples: int = 1,
    candidate_files: dict[str, str | Path] | None = None,
) -> dict[str, Any]:
    """Join predictions to fixed samples and write grouped diagnostic tables."""

    config = load_experiment_config(config_path)
    dataset_key = dataset_key or config["dataset"]["formal"]
    split_name = _normalize_split(split_name)
    split_file = SPLIT_TO_FILE[split_name]
    output_path = _resolve_output_dir(config, dataset_key, output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    user_activity, movie_popularity = _load_sequence_stats(config, dataset_key)
    y_metadata = _load_y_metadata(config, dataset_key, split_name, user_activity, movie_popularity)
    n_metadata = _load_n_metadata(
        config,
        dataset_key,
        split_name,
        user_activity,
        movie_popularity,
        candidate_files,
    )

    binary_specs = _binary_specs(config, dataset_key, y_run, m_runs, m_labels)
    ranking_specs = _ranking_specs(config, dataset_key, y_run, n_run, m_runs, m_labels)

    binary_rows: list[dict[str, Any]] = []
    ranking_rows: list[dict[str, Any]] = []
    join_summaries: list[dict[str, Any]] = []

    for spec in binary_specs:
        records = _enrich_binary_records(
            read_jsonl(spec[f"{split_file}_path"]),
            y_metadata,
            spec,
        )
        threshold = _resolve_binary_threshold(spec, threshold_mode)
        binary_rows.extend(
            _binary_group_rows(
                spec,
                split_name,
                records,
                threshold,
                threshold_mode,
                min_group_samples,
            )
        )
        join_summaries.append(_join_summary(spec, records))

    for spec in ranking_specs:
        records = _enrich_ranking_records(
            read_jsonl(spec[f"{split_file}_path"]),
            n_metadata,
            spec,
        )
        ranking_rows.extend(
            _ranking_group_rows(
                spec,
                split_name,
                records,
                min_group_samples,
            )
        )
        join_summaries.append(_join_summary(spec, records))

    paths = {
        "binary_csv": output_path / f"{split_file}_binary_group_metrics.csv",
        "ranking_csv": output_path / f"{split_file}_ranking_group_metrics.csv",
        "json": output_path / f"{split_file}_grouped_error_analysis.json",
        "report": output_path / f"{split_file}_grouped_error_analysis.md",
    }
    _write_csv(paths["binary_csv"], binary_rows)
    _write_csv(paths["ranking_csv"], ranking_rows)
    write_json(
        paths["json"],
        {
            "dataset": dataset_key,
            "split": split_name,
            "created_at_utc": datetime.now(timezone.utc).isoformat(),
            "threshold_mode": threshold_mode,
            "candidate_files": _candidate_files_for_summary(
                config,
                dataset_key,
                split_name,
                candidate_files,
            ),
            "min_group_samples": min_group_samples,
            "join_summaries": join_summaries,
            "binary": binary_rows,
            "ranking": ranking_rows,
        },
    )
    _write_markdown_report(
        paths["report"],
        dataset_key,
        split_name,
        threshold_mode,
        binary_rows,
        ranking_rows,
    )

    return {
        "dataset": dataset_key,
        "split": split_name,
        "binary_models": len(binary_specs),
        "ranking_models": len(ranking_specs),
        "rows": {
            "binary": len(binary_rows),
            "ranking": len(ranking_rows),
        },
        "output_dir": str(output_path),
        "paths": {name: str(path) for name, path in paths.items()},
    }


def _binary_specs(
    config: dict[str, Any],
    dataset_key: str,
    y_run: str | None,
    m_runs: list[str] | None,
    m_labels: list[str] | None,
) -> list[dict[str, Any]]:
    base_path = resolve_repo_path_from_config(config, config["outputs"]["base"], dataset_key=dataset_key)
    y_base = resolve_repo_path_from_config(config, config["outputs"]["y"], dataset_key=dataset_key)
    m_base = resolve_repo_path_from_config(config, config["outputs"]["m"], dataset_key=dataset_key)

    y_run = y_run or _latest_run_name(y_base)
    m_runs = m_runs or [_latest_run_name(m_base)]
    _validate_m_labels(m_runs, m_labels)

    specs = [
        _prediction_spec("base", "Base", "", "binary", base_path, "y"),
        _prediction_spec("y", "Y-K0", y_run, "binary", y_base / y_run, "y"),
    ]
    for index, m_run in enumerate(m_runs):
        label = m_labels[index] if m_labels else ("M-K0" if len(m_runs) == 1 else f"M-K0:{m_run}")
        specs.append(_prediction_spec("m", label, m_run, "binary", m_base / m_run, "m_y"))
    return specs


def _ranking_specs(
    config: dict[str, Any],
    dataset_key: str,
    y_run: str | None,
    n_run: str | None,
    m_runs: list[str] | None,
    m_labels: list[str] | None,
) -> list[dict[str, Any]]:
    base_path = resolve_repo_path_from_config(config, config["outputs"]["base"], dataset_key=dataset_key)
    y_base = resolve_repo_path_from_config(config, config["outputs"]["y"], dataset_key=dataset_key)
    n_base = resolve_repo_path_from_config(config, config["outputs"]["n"], dataset_key=dataset_key)
    m_base = resolve_repo_path_from_config(config, config["outputs"]["m"], dataset_key=dataset_key)

    y_run = y_run or _latest_run_name(y_base)
    n_run = n_run or _latest_run_name(n_base)
    m_runs = m_runs or [_latest_run_name(m_base)]
    _validate_m_labels(m_runs, m_labels)

    specs = [
        _prediction_spec("base", "Base", "", "ranking", base_path, "n"),
        _prediction_spec("y", "Y-K0", y_run, "ranking", y_base / y_run, "n"),
        _prediction_spec("n", "N-K0", n_run, "ranking", n_base / n_run, "n"),
    ]
    for index, m_run in enumerate(m_runs):
        label = m_labels[index] if m_labels else ("M-K0" if len(m_runs) == 1 else f"M-K0:{m_run}")
        specs.append(_prediction_spec("m", label, m_run, "ranking", m_base / m_run, "m_n"))
    return specs


def _prediction_spec(
    model_key: str,
    model: str,
    run_name: str,
    task: str,
    base_path: Path,
    file_prefix: str,
) -> dict[str, Any]:
    return {
        "model_key": model_key,
        "model": model,
        "run_name": run_name,
        "task": task,
        "valid_path": base_path / f"{file_prefix}_valid_predictions.jsonl",
        "test_path": base_path / f"{file_prefix}_test_predictions.jsonl",
    }


def _load_sequence_stats(
    config: dict[str, Any],
    dataset_key: str,
) -> tuple[dict[str, int], Counter[str]]:
    full_sequences_path = resolve_configured_output_path(
        config,
        dataset_key,
        "full_sequences",
    )
    user_activity: dict[str, int] = {}
    movie_popularity: Counter[str] = Counter()
    with open_text_auto(full_sequences_path, "rt", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            record = json.loads(line)
            interactions = record.get("interactions", [])
            user_id = str(record["user_id"])
            user_activity[user_id] = len(interactions)
            for interaction in interactions:
                movie_popularity[str(interaction["movie_id"])] += 1
    return user_activity, movie_popularity


def _load_y_metadata(
    config: dict[str, Any],
    dataset_key: str,
    split_name: str,
    user_activity: dict[str, int],
    movie_popularity: Counter[str],
) -> dict[str, Any]:
    path = resolve_configured_output_path(
        config,
        dataset_key,
        "preference_samples",
        split_name,
    )
    rows = [
        _sample_metadata(record, user_activity, movie_popularity)
        for record in _iter_jsonl(path)
    ]
    return _metadata_indexes(rows, task="binary")


def _load_n_metadata(
    config: dict[str, Any],
    dataset_key: str,
    split_name: str,
    user_activity: dict[str, int],
    movie_popularity: Counter[str],
    candidate_files: dict[str, str | Path] | None,
) -> dict[str, Any]:
    path = _candidate_path(config, dataset_key, split_name, candidate_files)
    rows = [
        _sample_metadata(record, user_activity, movie_popularity)
        for record in _iter_jsonl(path)
    ]
    return _metadata_indexes(rows, task="ranking")


def _candidate_path(
    config: dict[str, Any],
    dataset_key: str,
    split_name: str,
    candidate_files: dict[str, str | Path] | None = None,
) -> Path:
    candidate_key = "validation" if split_name == "validation" else "test"
    if candidate_files and candidate_key in candidate_files:
        path = Path(candidate_files[candidate_key])
        if path.is_absolute():
            return path
        return Path(config["_repo_root"]) / path
    configured_candidate_files = config.get("candidates", {}).get("save_files", {})
    if candidate_key in configured_candidate_files:
        return resolve_repo_path_from_config(
            config,
            configured_candidate_files[candidate_key],
            dataset_key=dataset_key,
        )
    return resolve_configured_output_path(config, dataset_key, "next_item_samples", split_name)


def _candidate_files_for_summary(
    config: dict[str, Any],
    dataset_key: str,
    split_name: str,
    candidate_files: dict[str, str | Path] | None = None,
) -> dict[str, str]:
    return {
        split_name: str(_candidate_path(config, dataset_key, split_name, candidate_files))
    }


def _candidate_file_overrides(
    valid_candidates: str | None,
    test_candidates: str | None,
) -> dict[str, str] | None:
    overrides = {}
    if valid_candidates:
        overrides["validation"] = valid_candidates
    if test_candidates:
        overrides["test"] = test_candidates
    return overrides or None


def _sample_metadata(
    record: dict[str, Any],
    user_activity: dict[str, int],
    movie_popularity: Counter[str],
) -> dict[str, Any]:
    target = record.get("target", {})
    history = record.get("history", [])
    ratings = [float(item["rating"]) for item in history if "rating" in item]
    positive_count = sum(1 for rating in ratings if rating >= 4.0)
    user_id = str(record["user_id"])
    target_movie_id = str(target.get("movie_id", record.get("ground_truth_movie_id", "")))
    target_rating = _optional_float(target.get("rating"))
    target_sequence_index = _optional_int(target.get("sequence_index"))
    history_length = len(history)
    history_positive_ratio = positive_count / len(ratings) if ratings else 0.0
    activity = int(user_activity.get(user_id, history_length))
    popularity = int(movie_popularity.get(target_movie_id, 0))

    return {
        "user_id": user_id,
        "target_movie_id": target_movie_id,
        "candidate_movie_ids": [str(item) for item in record.get("candidate_movie_ids", [])],
        "ground_truth_index": _optional_int(record.get("ground_truth_index")),
        "target_title": target.get("title", ""),
        "target_label": record.get("label"),
        "target_rating": target_rating,
        "target_timestamp": _optional_int(target.get("timestamp")),
        "target_sequence_index": target_sequence_index,
        "history_length": history_length,
        "history_mean_rating": _round(mean(ratings)) if ratings else 0.0,
        "history_positive_ratio": _round(history_positive_ratio),
        "user_activity": activity,
        "target_popularity": popularity,
        "target_rating_bucket": _rating_bucket(target_rating),
        "history_length_bucket": _range_bucket(history_length, [(5, "<=5"), (10, "6-10"), (20, "11-20")], ">20"),
        "history_positive_ratio_bucket": _ratio_bucket(history_positive_ratio),
        "user_activity_bucket": _range_bucket(activity, [(50, "<=50"), (100, "51-100"), (200, "101-200"), (400, "201-400")], ">400"),
        "target_popularity_bucket": _range_bucket(popularity, [(10, "<=10"), (50, "11-50"), (200, "51-200"), (500, "201-500")], ">500"),
        "target_sequence_bucket": _range_bucket(target_sequence_index, [(20, "<=20"), (50, "21-50"), (100, "51-100"), (200, "101-200")], ">200"),
        "ground_truth_position": str(record.get("ground_truth_index", "")),
    }


def _metadata_indexes(rows: list[dict[str, Any]], task: str) -> dict[str, Any]:
    by_position = list(rows)
    user_movie_groups: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    candidate_groups: dict[tuple[str, str, tuple[str, ...]], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        user_movie_groups[(row["user_id"], row["target_movie_id"])].append(row)
        candidate_key = (
            row["user_id"],
            row["target_movie_id"],
            tuple(row.get("candidate_movie_ids", [])),
        )
        candidate_groups[candidate_key].append(row)
    return {
        "task": task,
        "by_position": by_position,
        "by_user_movie": _unique_groups(user_movie_groups),
        "by_candidate_set": _unique_groups(candidate_groups),
    }


def _unique_groups(groups: dict[tuple[Any, ...], list[dict[str, Any]]]) -> dict[tuple[Any, ...], dict[str, Any]]:
    return {key: values[0] for key, values in groups.items() if len(values) == 1}


def _enrich_binary_records(
    predictions: list[dict[str, Any]],
    metadata: dict[str, Any],
    spec: dict[str, Any],
) -> list[dict[str, Any]]:
    rows = []
    for index, prediction in enumerate(predictions):
        meta = _lookup_binary_metadata(prediction, index, metadata)
        score = float(prediction.get("p_yes", prediction.get("score", 0.0)))
        rows.append(
            {
                **meta,
                "model_key": spec["model_key"],
                "model": spec["model"],
                "run_name": spec["run_name"],
                "label": prediction["label"],
                "score": score,
                "p_yes": score,
                "joined_metadata": bool(meta),
            }
        )
    _raise_if_unmatched(spec, rows)
    return rows


def _enrich_ranking_records(
    predictions: list[dict[str, Any]],
    metadata: dict[str, Any],
    spec: dict[str, Any],
) -> list[dict[str, Any]]:
    rows = []
    for index, prediction in enumerate(predictions):
        meta = _lookup_ranking_metadata(prediction, index, metadata)
        scores = [float(score) for score in prediction["scores"]]
        gt_index = int(prediction["ground_truth_index"])
        rank = ground_truth_rank(scores, gt_index)
        gt_score = scores[gt_index]
        best_negative = max(
            score for item_index, score in enumerate(scores) if item_index != gt_index
        )
        rows.append(
            {
                **meta,
                "model_key": spec["model_key"],
                "model": spec["model"],
                "run_name": spec["run_name"],
                "scores": scores,
                "ground_truth_index": gt_index,
                "rank": rank,
                "margin": gt_score - best_negative,
                "joined_metadata": bool(meta),
            }
        )
    _raise_if_unmatched(spec, rows)
    return rows


def _lookup_binary_metadata(
    prediction: dict[str, Any],
    index: int,
    metadata: dict[str, Any],
) -> dict[str, Any]:
    key = (str(prediction.get("user_id", "")), str(prediction.get("target_movie_id", "")))
    if key in metadata["by_user_movie"]:
        return metadata["by_user_movie"][key]
    return _position_fallback(prediction, index, metadata, key)


def _lookup_ranking_metadata(
    prediction: dict[str, Any],
    index: int,
    metadata: dict[str, Any],
) -> dict[str, Any]:
    user_id = str(prediction.get("user_id", ""))
    target_movie_id = str(prediction.get("ground_truth_movie_id", ""))
    candidate_key = (
        user_id,
        target_movie_id,
        tuple(str(item) for item in prediction.get("candidate_movie_ids", [])),
    )
    if candidate_key in metadata["by_candidate_set"]:
        return metadata["by_candidate_set"][candidate_key]
    key = (user_id, target_movie_id)
    if key in metadata["by_user_movie"]:
        return metadata["by_user_movie"][key]
    return _position_fallback(prediction, index, metadata, key)


def _position_fallback(
    prediction: dict[str, Any],
    index: int,
    metadata: dict[str, Any],
    key: tuple[str, str],
) -> dict[str, Any]:
    if index >= len(metadata["by_position"]):
        return {}
    row = metadata["by_position"][index]
    expected_movie = key[1]
    row_movie = row.get("target_movie_id")
    if str(row.get("user_id")) == key[0] and (not expected_movie or str(row_movie) == expected_movie):
        return row
    return {}


def _raise_if_unmatched(spec: dict[str, Any], rows: list[dict[str, Any]]) -> None:
    missing = sum(1 for row in rows if not row.get("joined_metadata"))
    if missing:
        raise ValueError(
            f"{spec['model']} {spec['task']} has {missing} predictions that could not be joined to fixed samples"
        )


def _resolve_binary_threshold(spec: dict[str, Any], threshold_mode: str) -> float:
    if threshold_mode == "fixed_0.5":
        return 0.5
    if threshold_mode != "validation_best_f1":
        raise ValueError(f"Unsupported threshold_mode: {threshold_mode}")
    records = [
        {
            "label": record["label"],
            "score": float(record.get("p_yes", record.get("score", 0.0))),
        }
        for record in read_jsonl(spec["valid_path"])
    ]
    return find_best_threshold(records)


def _binary_group_rows(
    spec: dict[str, Any],
    split_name: str,
    records: list[dict[str, Any]],
    threshold: float,
    threshold_mode: str,
    min_group_samples: int,
) -> list[dict[str, Any]]:
    output = []
    for group_field in BINARY_GROUP_FIELDS:
        for group_value, group_records in _groups(records, group_field).items():
            if len(group_records) < min_group_samples:
                continue
            metrics = binary_metrics_at_threshold(group_records, threshold)
            output.append(
                {
                    "model_key": spec["model_key"],
                    "model": spec["model"],
                    "run_name": spec["run_name"],
                    "split": split_name,
                    "group_field": group_field,
                    "group_value": group_value,
                    "threshold_source": threshold_mode,
                    **metrics,
                    "positive_ratio": _round(metrics["yes_labels"] / metrics["samples"] if metrics["samples"] else 0.0),
                    "mean_score": _round(mean(record["score"] for record in group_records)),
                }
            )
    return output


def _ranking_group_rows(
    spec: dict[str, Any],
    split_name: str,
    records: list[dict[str, Any]],
    min_group_samples: int,
) -> list[dict[str, Any]]:
    output = []
    for group_field in RANKING_GROUP_FIELDS:
        for group_value, group_records in _groups(records, group_field).items():
            if len(group_records) < min_group_samples:
                continue
            output.append(
                {
                    "model_key": spec["model_key"],
                    "model": spec["model"],
                    "run_name": spec["run_name"],
                    "split": split_name,
                    "group_field": group_field,
                    "group_value": group_value,
                    **_ranking_metrics(group_records),
                }
            )
    return output


def _ranking_metrics(records: list[dict[str, Any]]) -> dict[str, Any]:
    candidate_count = max((len(record["scores"]) for record in records), default=5)
    metric_ks = default_ranking_ks(candidate_count) or [candidate_count]
    totals = {"HR@1": 0.0, "MRR": 0.0}
    for metric_k in metric_ks:
        totals[f"HR@{metric_k}"] = 0.0
        totals[f"NDCG@{metric_k}"] = 0.0
    rank_counts = Counter()
    for record in records:
        metrics = ranking_metrics_for_rank(int(record["rank"]), ks=metric_ks)
        for key, value in metrics.items():
            totals[key] += value
        rank_counts[int(record["rank"])] += 1
    sample_count = len(records)
    output = {
        "samples": sample_count,
        "mrr": _round(totals["MRR"] / sample_count if sample_count else 0.0),
        "mean_rank": _round(mean(record["rank"] for record in records)),
        "mean_margin": _round(mean(record["margin"] for record in records)),
        "rank_distribution": json.dumps({str(key): rank_counts[key] for key in sorted(rank_counts)}, sort_keys=True),
    }
    for metric_k in metric_ks:
        output[f"hr_at_{metric_k}"] = _round(
            totals[f"HR@{metric_k}"] / sample_count if sample_count else 0.0
        )
        output[f"ndcg_at_{metric_k}"] = _round(
            totals[f"NDCG@{metric_k}"] / sample_count if sample_count else 0.0
        )
    output["hr_at_1"] = _round(totals["HR@1"] / sample_count if sample_count else 0.0)
    return output


def _groups(records: list[dict[str, Any]], group_field: str) -> dict[str, list[dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    if group_field == "all":
        grouped["ALL"] = list(records)
        return dict(grouped)
    for record in records:
        grouped[str(record.get(group_field, "UNKNOWN"))].append(record)
    return dict(sorted(grouped.items(), key=lambda item: item[0]))


def _join_summary(spec: dict[str, Any], rows: list[dict[str, Any]]) -> dict[str, Any]:
    joined = sum(1 for row in rows if row.get("joined_metadata"))
    return {
        "model": spec["model"],
        "run_name": spec["run_name"],
        "task": spec["task"],
        "predictions": len(rows),
        "joined_metadata": joined,
        "missing_metadata": len(rows) - joined,
    }


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def _write_markdown_report(
    path: Path,
    dataset_key: str,
    split_name: str,
    threshold_mode: str,
    binary_rows: list[dict[str, Any]],
    ranking_rows: list[dict[str, Any]],
) -> None:
    lines = [
        f"# {dataset_key} Grouped Error Analysis ({split_name})",
        "",
        f"Generated at: {datetime.now(timezone.utc).isoformat()}",
        "",
        f"Binary threshold mode: `{threshold_mode}`.",
        "",
        "## Binary Overview",
        "",
        _markdown_table(
            [row for row in binary_rows if row["group_field"] == "all"],
            ["model", "run_name", "samples", "threshold", "auc", "f1", "accuracy", "precision", "recall", "fp", "fn"],
        ),
        "",
        "## Binary By Group",
        "",
        _markdown_table(
            [row for row in binary_rows if row["group_field"] != "all"],
            ["model", "group_field", "group_value", "samples", "auc", "f1", "accuracy", "fp", "fn"],
        ),
        "",
        "## Ranking Overview",
        "",
        _markdown_table(
            [row for row in ranking_rows if row["group_field"] == "all"],
            ["model", "run_name", "samples", "hr_at_1", "hr_at_5", "ndcg_at_5", "mrr", "mean_rank", "mean_margin"],
        ),
        "",
        "## Ranking By Group",
        "",
        _markdown_table(
            [row for row in ranking_rows if row["group_field"] != "all"],
            ["model", "group_field", "group_value", "samples", "hr_at_1", "ndcg_at_5", "mrr", "mean_rank", "mean_margin"],
        ),
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def _markdown_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._"
    output = [
        "| " + " | ".join(fields) + " |",
        "|" + "|".join("---" for _ in fields) + "|",
    ]
    for row in rows:
        output.append("| " + " | ".join(str(row.get(field, "")) for field in fields) + " |")
    return "\n".join(output)


def _iter_jsonl(path: Path):
    with open_text_auto(path, "rt", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                yield json.loads(line)


def _validate_m_labels(m_runs: list[str], m_labels: list[str] | None) -> None:
    if m_labels and len(m_labels) != len(m_runs):
        raise ValueError("m_labels must have the same length as m_runs")


def _latest_run_name(base_dir: Path) -> str:
    if not base_dir.exists():
        raise FileNotFoundError(f"Output directory does not exist: {base_dir}")
    candidates = [path for path in base_dir.iterdir() if path.is_dir()]
    if not candidates:
        raise FileNotFoundError(f"Output directory has no run: {base_dir}")
    return max(candidates, key=lambda path: path.stat().st_mtime).name


def _resolve_output_dir(
    config: dict[str, Any],
    dataset_key: str,
    output_dir: str | Path | None,
) -> Path:
    if output_dir is not None:
        path = Path(output_dir)
        if path.is_absolute():
            return path
        return Path(config["_repo_root"]) / path
    return Path(config["_repo_root"]) / "outputs" / "error_analysis" / dataset_key / "grouped"


def _normalize_split(split_name: str) -> str:
    if split_name == "valid":
        return "validation"
    if split_name not in {"validation", "test"}:
        raise ValueError(f"Unsupported split: {split_name}")
    return split_name


def _optional_float(value: Any) -> float | None:
    if value is None or value == "":
        return None
    return float(value)


def _optional_int(value: Any) -> int | None:
    if value is None or value == "":
        return None
    return int(value)


def _rating_bucket(value: float | None) -> str:
    if value is None:
        return "UNKNOWN"
    return f"rating_{value:g}"


def _ratio_bucket(value: float) -> str:
    if value < 0.4:
        return "<0.4"
    if value < 0.6:
        return "0.4-0.6"
    if value < 0.8:
        return "0.6-0.8"
    return ">=0.8"


def _range_bucket(
    value: int | None,
    buckets: list[tuple[int, str]],
    overflow_label: str,
) -> str:
    if value is None:
        return "UNKNOWN"
    previous = None
    for upper_bound, label in buckets:
        if value <= upper_bound:
            return label
        previous = upper_bound
    return overflow_label if previous is not None else "UNKNOWN"


def _round(value: float) -> float:
    return round(float(value), 10)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Phase 1.5 STEP C grouped diagnostics")
    parser.add_argument("--config", default="configs/experiment.yaml")
    parser.add_argument("--dataset", default=None)
    parser.add_argument("--y-run", default=None)
    parser.add_argument("--n-run", default=None)
    parser.add_argument("--m-runs", nargs="*", default=None)
    parser.add_argument("--m-labels", nargs="*", default=None)
    parser.add_argument("--split", default="test", choices=["validation", "valid", "test"])
    parser.add_argument(
        "--threshold-mode",
        default="validation_best_f1",
        choices=["validation_best_f1", "fixed_0.5"],
    )
    parser.add_argument("--output-dir", default=None)
    parser.add_argument("--min-group-samples", type=int, default=1)
    parser.add_argument("--valid-candidates", default=None)
    parser.add_argument("--test-candidates", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    summary = run_grouped_error_analysis(
        config_path=args.config,
        dataset_key=args.dataset,
        y_run=args.y_run,
        n_run=args.n_run,
        m_runs=args.m_runs,
        m_labels=args.m_labels,
        split_name=args.split,
        threshold_mode=args.threshold_mode,
        output_dir=args.output_dir,
        min_group_samples=args.min_group_samples,
        candidate_files=_candidate_file_overrides(
            args.valid_candidates,
            args.test_candidates,
        ),
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
