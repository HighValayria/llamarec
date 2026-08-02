"""STEP 8：基础 error analysis。"""

from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from datetime import datetime, timezone
import json
from pathlib import Path
from statistics import mean
from typing import Any

from src.data.config import load_experiment_config, resolve_repo_path_from_config
from src.inference.prediction_io import read_jsonl, write_json, write_jsonl


SPLIT_TO_FILE = {
    "validation": "valid",
    "valid": "valid",
    "test": "test",
}


def run_basic_error_analysis(
    config_path: str | Path,
    dataset_key: str | None = None,
    y_run: str | None = None,
    n_run: str | None = None,
    m_run: str | None = None,
    split_name: str = "test",
    output_dir: str | Path | None = None,
    example_limit: int = 20,
) -> dict[str, Any]:
    """读取 prediction JSONL 并输出基础错误分析。"""

    config = load_experiment_config(config_path)
    dataset_key = dataset_key or config["dataset"]["formal"]
    split_name = _normalize_split(split_name)
    split_file = SPLIT_TO_FILE[split_name]
    output_path = _resolve_output_dir(config, dataset_key, output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    specs = _prediction_specs(config, dataset_key, y_run, n_run, m_run, split_file)
    binary_rows = []
    ranking_rows = []
    examples: dict[str, list[dict[str, Any]]] = {}

    for spec in specs:
        path = spec["path"]
        records = read_jsonl(path)
        if spec["task"] == "binary":
            summary, error_examples = _summarize_binary_predictions(
                records,
                spec,
                example_limit,
            )
            binary_rows.append(summary)
            examples[f"{spec['model_key']}_binary"] = error_examples
        else:
            summary, error_examples = _summarize_ranking_predictions(
                records,
                spec,
                example_limit,
            )
            ranking_rows.append(summary)
            examples[f"{spec['model_key']}_ranking"] = error_examples

    _write_csv(output_path / f"{split_file}_binary_error_summary.csv", binary_rows)
    _write_csv(output_path / f"{split_file}_ranking_error_summary.csv", ranking_rows)
    write_json(
        output_path / f"{split_file}_error_summary.json",
        {
            "dataset": dataset_key,
            "split": split_name,
            "created_at_utc": datetime.now(timezone.utc).isoformat(),
            "binary": binary_rows,
            "ranking": ranking_rows,
        },
    )
    write_jsonl(
        output_path / f"{split_file}_error_examples.jsonl",
        _flatten_examples(examples),
    )
    _write_markdown_report(
        output_path / f"{split_file}_error_analysis.md",
        dataset_key,
        split_name,
        binary_rows,
        ranking_rows,
    )

    return {
        "dataset": dataset_key,
        "split": split_name,
        "output_dir": str(output_path),
        "binary_models": len(binary_rows),
        "ranking_models": len(ranking_rows),
    }


def _prediction_specs(
    config: dict[str, Any],
    dataset_key: str,
    y_run: str | None,
    n_run: str | None,
    m_run: str | None,
    split_file: str,
) -> list[dict[str, Any]]:
    base_path = resolve_repo_path_from_config(
        config,
        config["outputs"]["base"],
        dataset_key=dataset_key,
    )
    y_base = resolve_repo_path_from_config(
        config,
        config["outputs"]["y"],
        dataset_key=dataset_key,
    )
    n_base = resolve_repo_path_from_config(
        config,
        config["outputs"]["n"],
        dataset_key=dataset_key,
    )
    m_base = resolve_repo_path_from_config(
        config,
        config["outputs"]["m"],
        dataset_key=dataset_key,
    )
    y_run = y_run or _latest_run_name(y_base)
    n_run = n_run or _latest_run_name(n_base)
    m_run = m_run or _latest_run_name(m_base)

    return [
        {
            "model_key": "base",
            "model": "Base",
            "task": "binary",
            "path": base_path / f"y_{split_file}_predictions.jsonl",
        },
        {
            "model_key": "base",
            "model": "Base",
            "task": "ranking",
            "path": base_path / f"n_{split_file}_predictions.jsonl",
        },
        {
            "model_key": "y",
            "model": "Y-K0",
            "task": "binary",
            "path": y_base / y_run / f"y_{split_file}_predictions.jsonl",
        },
        {
            "model_key": "y",
            "model": "Y-K0",
            "task": "ranking",
            "path": y_base / y_run / f"n_{split_file}_predictions.jsonl",
        },
        {
            "model_key": "n",
            "model": "N-K0",
            "task": "ranking",
            "path": n_base / n_run / f"n_{split_file}_predictions.jsonl",
        },
        {
            "model_key": "m",
            "model": "M-K0",
            "task": "binary",
            "path": m_base / m_run / f"m_y_{split_file}_predictions.jsonl",
        },
        {
            "model_key": "m",
            "model": "M-K0",
            "task": "ranking",
            "path": m_base / m_run / f"m_n_{split_file}_predictions.jsonl",
        },
    ]


def _summarize_binary_predictions(
    records: list[dict[str, Any]],
    spec: dict[str, Any],
    example_limit: int,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    counts = Counter()
    p_yes_by_label: dict[str, list[float]] = defaultdict(list)
    false_positives = []
    false_negatives = []

    for record in records:
        label = str(record["label"])
        p_yes = float(record.get("p_yes", record.get("score", 0.0)))
        predicted = str(record.get("predicted_label") or ("Yes" if p_yes >= 0.5 else "No"))
        counts[f"label_{label}"] += 1
        counts[f"predicted_{predicted}"] += 1
        p_yes_by_label[label].append(p_yes)
        if label == "Yes" and predicted == "Yes":
            counts["tp"] += 1
        elif label == "No" and predicted == "No":
            counts["tn"] += 1
        elif label == "No" and predicted == "Yes":
            counts["fp"] += 1
            false_positives.append(_compact_binary_record(record, p_yes))
        elif label == "Yes" and predicted == "No":
            counts["fn"] += 1
            false_negatives.append(_compact_binary_record(record, p_yes))

    total = len(records)
    accuracy = (counts["tp"] + counts["tn"]) / total if total else 0.0
    false_positives.sort(key=lambda item: item["p_yes"], reverse=True)
    false_negatives.sort(key=lambda item: item["p_yes"])
    examples = [
        {"error_type": "false_positive", **item}
        for item in false_positives[:example_limit]
    ] + [
        {"error_type": "false_negative", **item}
        for item in false_negatives[:example_limit]
    ]

    return (
        {
            "model_key": spec["model_key"],
            "model": spec["model"],
            "prediction_path": str(spec["path"]),
            "samples": total,
            "yes_labels": counts["label_Yes"],
            "no_labels": counts["label_No"],
            "predicted_yes": counts["predicted_Yes"],
            "predicted_no": counts["predicted_No"],
            "tp": counts["tp"],
            "tn": counts["tn"],
            "fp": counts["fp"],
            "fn": counts["fn"],
            "accuracy_at_threshold": _round(accuracy),
            "mean_p_yes_for_yes": _round(_safe_mean(p_yes_by_label["Yes"])),
            "mean_p_yes_for_no": _round(_safe_mean(p_yes_by_label["No"])),
        },
        examples,
    )


def _summarize_ranking_predictions(
    records: list[dict[str, Any]],
    spec: dict[str, Any],
    example_limit: int,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    rank_counts = Counter()
    gt_position_counts = Counter()
    predicted_position_counts = Counter()
    hit_by_gt_position: dict[int, Counter] = defaultdict(Counter)
    positive_scores = []
    best_negative_scores = []
    margins = []
    misses = []

    for record in records:
        scores = [float(score) for score in record["scores"]]
        ground_truth_index = int(record["ground_truth_index"])
        ranked_indices = sorted(range(len(scores)), key=lambda index: scores[index], reverse=True)
        predicted_index = ranked_indices[0]
        rank = ranked_indices.index(ground_truth_index) + 1
        gt_score = scores[ground_truth_index]
        negative_scores = [
            score for index, score in enumerate(scores) if index != ground_truth_index
        ]
        best_negative = max(negative_scores) if negative_scores else 0.0
        margin = gt_score - best_negative

        rank_counts[rank] += 1
        gt_position_counts[ground_truth_index] += 1
        predicted_position_counts[predicted_index] += 1
        hit_by_gt_position[ground_truth_index]["total"] += 1
        if rank == 1:
            hit_by_gt_position[ground_truth_index]["hits"] += 1
        positive_scores.append(gt_score)
        best_negative_scores.append(best_negative)
        margins.append(margin)
        if rank != 1:
            misses.append(_compact_ranking_record(record, rank, predicted_index, margin))

    total = len(records)
    hits_at_1 = rank_counts[1]
    misses.sort(key=lambda item: item["margin"])
    return (
        {
            "model_key": spec["model_key"],
            "model": spec["model"],
            "prediction_path": str(spec["path"]),
            "samples": total,
            "hit_at_1": _round(hits_at_1 / total if total else 0.0),
            "mean_ground_truth_score": _round(_safe_mean(positive_scores)),
            "mean_best_negative_score": _round(_safe_mean(best_negative_scores)),
            "mean_margin": _round(_safe_mean(margins)),
            "rank_distribution": _json_counter(rank_counts),
            "ground_truth_position_distribution": _json_counter(gt_position_counts),
            "predicted_position_distribution": _json_counter(predicted_position_counts),
            "hit_at_1_by_ground_truth_position": _json_hit_by_position(hit_by_gt_position),
        },
        [
            {"error_type": "ranking_miss", **item}
            for item in misses[:example_limit]
        ],
    )


def _compact_binary_record(record: dict[str, Any], p_yes: float) -> dict[str, Any]:
    return {
        "model": record.get("model"),
        "task": record.get("task"),
        "split": record.get("split"),
        "user_id": record.get("user_id"),
        "target_movie_id": record.get("target_movie_id"),
        "label": record.get("label"),
        "predicted_label": record.get("predicted_label"),
        "p_yes": p_yes,
    }


def _compact_ranking_record(
    record: dict[str, Any],
    rank: int,
    predicted_index: int,
    margin: float,
) -> dict[str, Any]:
    return {
        "model": record.get("model"),
        "task": record.get("task"),
        "split": record.get("split"),
        "user_id": record.get("user_id"),
        "ground_truth_index": record.get("ground_truth_index"),
        "predicted_index": predicted_index,
        "rank": rank,
        "margin": _round(margin),
        "ground_truth_movie_id": record.get("ground_truth_movie_id"),
        "candidate_movie_ids": record.get("candidate_movie_ids"),
        "scores": record.get("scores"),
    }


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _write_markdown_report(
    path: Path,
    dataset_key: str,
    split_name: str,
    binary_rows: list[dict[str, Any]],
    ranking_rows: list[dict[str, Any]],
) -> None:
    lines = [
        f"# {dataset_key} Error Analysis ({split_name})",
        "",
        f"Generated at: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Binary",
        "",
        _markdown_table(
            binary_rows,
            ["model", "samples", "accuracy_at_threshold", "fp", "fn", "mean_p_yes_for_yes", "mean_p_yes_for_no"],
        ),
        "",
        "## Ranking",
        "",
        _markdown_table(
            ranking_rows,
            ["model", "samples", "hit_at_1", "mean_margin", "rank_distribution", "predicted_position_distribution"],
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


def _flatten_examples(examples: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows = []
    for group, group_examples in examples.items():
        for item in group_examples:
            rows.append({"group": group, **item})
    return rows


def _json_counter(counter: Counter) -> str:
    return json.dumps(
        {str(key): counter[key] for key in sorted(counter)},
        ensure_ascii=False,
        sort_keys=True,
    )


def _json_hit_by_position(position_counts: dict[int, Counter]) -> str:
    payload = {}
    for position in sorted(position_counts):
        total = position_counts[position]["total"]
        hits = position_counts[position]["hits"]
        payload[str(position)] = {
            "hits": hits,
            "total": total,
            "hit_at_1": _round(hits / total if total else 0.0),
        }
    return json.dumps(payload, ensure_ascii=False, sort_keys=True)


def _safe_mean(values: list[float]) -> float:
    return mean(values) if values else 0.0


def _round(value: float) -> float:
    return round(float(value), 10)


def _latest_run_name(base_dir: Path) -> str:
    if not base_dir.exists():
        raise FileNotFoundError(f"找不到输出目录: {base_dir}")
    candidates = [path for path in base_dir.iterdir() if path.is_dir()]
    if not candidates:
        raise FileNotFoundError(f"输出目录下没有 run: {base_dir}")
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
    return Path(config["_repo_root"]) / "outputs" / "error_analysis" / dataset_key


def _normalize_split(split_name: str) -> str:
    if split_name == "valid":
        return "validation"
    if split_name not in {"validation", "test"}:
        raise ValueError(f"不支持的 split: {split_name}")
    return split_name


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="生成基础 error analysis")
    parser.add_argument("--config", default="configs/experiment.yaml")
    parser.add_argument("--dataset", default=None)
    parser.add_argument("--y-run", default=None)
    parser.add_argument("--n-run", default=None)
    parser.add_argument("--m-run", default=None)
    parser.add_argument("--split", default="test", choices=["validation", "valid", "test"])
    parser.add_argument("--output-dir", default=None)
    parser.add_argument("--example-limit", type=int, default=20)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    summary = run_basic_error_analysis(
        config_path=args.config,
        dataset_key=args.dataset,
        y_run=args.y_run,
        n_run=args.n_run,
        m_run=args.m_run,
        split_name=args.split,
        output_dir=args.output_dir,
        example_limit=args.example_limit,
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
