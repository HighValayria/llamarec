"""STEP 4：Base zero-shot 本地 dry-run / 云端入口。"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any

from src.data.config import (
    load_experiment_config,
    resolve_configured_output_path,
    resolve_repo_path_from_config,
)
from src.data.preprocess import load_movies
from src.eval.binary_metrics import binary_metrics
from src.eval.ranking_metrics import aggregate_ranking_metrics
from src.inference.prediction_io import read_jsonl, write_json, write_jsonl, write_yaml
from src.inference.prompts import (
    assert_no_candidate_rating_in_candidate_prompt,
    assert_no_target_rating_in_yesno_prompt,
    prompt_hash,
    render_candidate_prompt,
    render_yesno_prompt,
)
from src.inference.scoring import build_scorer
from src.inference.tokenization_check import build_tokenization_report

SPLIT_ALIASES = {
    "valid": "validation",
    "validation": "validation",
    "test": "test",
}

OUTPUT_SPLIT_NAMES = {
    "validation": "valid",
    "test": "test",
}


def run_base_zero_shot(
    config_path: str | Path,
    dataset_key: str | None = None,
    mode: str = "mock",
    splits: list[str] | None = None,
    limit: int | None = None,
) -> dict[str, Any]:
    """运行 Base zero-shot 推理流程。

    mock 模式只验证本地文件流、prompt、prediction schema 和指标接口。
    """

    config = load_experiment_config(config_path)
    dataset_key = dataset_key or config["dataset"]["development"]
    normalized_splits = _normalize_splits(splits or ["validation", "test"])
    output_dir = _output_dir(config, dataset_key)
    scorer = build_scorer(mode)
    movie_lookup = load_movies(dataset_key, config)

    output_dir.mkdir(parents=True, exist_ok=True)
    write_yaml(output_dir / "config_snapshot.yaml", _config_snapshot(config))
    write_json(
        output_dir / "tokenization_report.json",
        build_tokenization_report(mode=mode, tokenizer=None),
    )

    metrics_by_split = {}
    run_counts = {}
    for split_name in normalized_splits:
        y_samples = _read_y_samples(config, dataset_key, split_name, limit)
        n_records = _read_candidate_records(config, dataset_key, split_name, limit)

        y_predictions = _predict_y_samples(y_samples, scorer, split_name)
        n_predictions = _predict_n_records(n_records, scorer, movie_lookup, split_name)

        output_split = OUTPUT_SPLIT_NAMES[split_name]
        write_jsonl(output_dir / f"y_{output_split}_predictions.jsonl", y_predictions)
        write_jsonl(output_dir / f"n_{output_split}_predictions.jsonl", n_predictions)

        metrics = _metrics_for_split(
            dataset_key,
            split_name,
            y_predictions,
            n_predictions,
        )
        write_json(output_dir / f"{output_split}_metrics.json", metrics)
        metrics_by_split[split_name] = metrics
        run_counts[split_name] = {
            "y_predictions": len(y_predictions),
            "n_predictions": len(n_predictions),
        }

    run_summary = {
        "model": "base",
        "mode": mode,
        "dataset": dataset_key,
        "splits": normalized_splits,
        "limit": limit,
        "counts": run_counts,
        "outputs_dir": str(output_dir),
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "real_model_loaded": mode == "real",
    }
    write_json(output_dir / "run_summary.json", run_summary)

    return {
        "dataset": dataset_key,
        "mode": mode,
        "outputs_dir": str(output_dir),
        "counts": run_counts,
        "metrics": metrics_by_split,
    }


def _predict_y_samples(
    samples: list[dict[str, Any]],
    scorer: Any,
    split_name: str,
) -> list[dict[str, Any]]:
    predictions = []
    for sample in samples:
        prompt = render_yesno_prompt(sample)
        assert_no_target_rating_in_yesno_prompt(prompt, sample)
        score = scorer.score_yesno(prompt)
        predictions.append(
            {
                "model": "base",
                "task": "Y",
                "split": split_name,
                "user_id": sample["user_id"],
                "target_movie_id": str(sample["target"]["movie_id"]),
                "label": sample["label"],
                "p_yes": score["p_yes"],
                "p_no": score["p_no"],
                "score": score["p_yes"],
                "predicted_label": score["predicted_label"],
                "prompt_hash": prompt_hash(prompt),
                "scoring_mode": score.get("scoring_mode"),
            }
        )
    return predictions


def _predict_n_records(
    records: list[dict[str, Any]],
    scorer: Any,
    movie_lookup: dict[str, dict[str, str]],
    split_name: str,
) -> list[dict[str, Any]]:
    predictions = []
    for record in records:
        prompt = render_candidate_prompt(record, movie_lookup)
        assert_no_candidate_rating_in_candidate_prompt(prompt)
        label_set = list(record.get("label_set", ["A", "B", "C", "D", "E"]))
        score = scorer.score_candidates(prompt, label_set)
        probabilities = score["label_probabilities"]
        scores = [probabilities[label] for label in label_set]
        predictions.append(
            {
                "model": "base",
                "task": "N",
                "split": split_name,
                "user_id": record["user_id"],
                "candidate_movie_ids": record["candidate_movie_ids"],
                "ground_truth_index": record["ground_truth_index"],
                "ground_truth_movie_id": str(record["ground_truth_movie_id"]),
                "label": record["label"],
                "label_probabilities": probabilities,
                "scores": scores,
                "predicted_label": score["predicted_label"],
                "prompt_hash": prompt_hash(prompt),
                "scoring_mode": score.get("scoring_mode"),
            }
        )
    return predictions


def _metrics_for_split(
    dataset_key: str,
    split_name: str,
    y_predictions: list[dict[str, Any]],
    n_predictions: list[dict[str, Any]],
) -> dict[str, Any]:
    y_metric_records = [
        {"score": prediction["p_yes"], "label": prediction["label"]}
        for prediction in y_predictions
    ]
    n_metric_records = [
        {
            "scores": prediction["scores"],
            "ground_truth_index": prediction["ground_truth_index"],
        }
        for prediction in n_predictions
    ]
    binary = binary_metrics(y_metric_records)
    ranking = aggregate_ranking_metrics(n_metric_records)

    return {
        "model": "base",
        "dataset": dataset_key,
        "split": split_name,
        "binary": {**binary, "samples": len(y_predictions)},
        "ranking": {**ranking, "samples": len(n_predictions)},
    }


def _read_y_samples(
    config: dict[str, Any],
    dataset_key: str,
    split_name: str,
    limit: int | None,
) -> list[dict[str, Any]]:
    path = resolve_configured_output_path(
        config,
        dataset_key,
        "preference_samples",
        split_name,
    )
    return read_jsonl(path, limit=limit)


def _read_candidate_records(
    config: dict[str, Any],
    dataset_key: str,
    split_name: str,
    limit: int | None,
) -> list[dict[str, Any]]:
    save_key = "validation" if split_name == "validation" else "test"
    raw_path = config["candidates"]["save_files"][save_key]
    path = resolve_repo_path_from_config(
        config,
        raw_path,
        dataset_key=dataset_key,
        split_name=split_name,
    )
    return read_jsonl(path, limit=limit)


def _output_dir(config: dict[str, Any], dataset_key: str) -> Path:
    raw_path = config.get("outputs", {}).get("base", "outputs/base")
    return resolve_repo_path_from_config(config, raw_path, dataset_key=dataset_key)


def _config_snapshot(config: dict[str, Any]) -> dict[str, Any]:
    snapshot = dict(config)
    snapshot.pop("_repo_root", None)
    return snapshot


def _normalize_splits(splits: list[str]) -> list[str]:
    normalized = []
    for split in splits:
        key = split.strip().lower()
        if key not in SPLIT_ALIASES:
            raise ValueError(f"未知 split: {split}")
        value = SPLIT_ALIASES[key]
        if value not in normalized:
            normalized.append(value)
    return normalized


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="运行 Base zero-shot 推理流程")
    parser.add_argument(
        "--config",
        default="configs/experiment.yaml",
        help="共享实验配置路径",
    )
    parser.add_argument(
        "--dataset",
        default=None,
        help="数据集 key；默认使用配置中的 dataset.development",
    )
    parser.add_argument(
        "--mode",
        choices=["mock", "real"],
        default="mock",
        help="mock 用于本地 dry-run；real 留给云端真实模型。",
    )
    parser.add_argument(
        "--splits",
        nargs="+",
        default=["validation", "test"],
        help="要运行的 split，可选 validation/valid/test。",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="每个 split 每个任务最多处理多少条样本；本地 dry-run 建议 20。",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    summary = run_base_zero_shot(
        config_path=args.config,
        dataset_key=args.dataset,
        mode=args.mode,
        splits=args.splits,
        limit=args.limit,
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
