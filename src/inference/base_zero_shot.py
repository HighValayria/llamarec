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
from src.eval.ranking_metrics import aggregate_ranking_metrics, default_ranking_ks
from src.inference.prediction_io import (
    append_jsonl,
    read_jsonl,
    write_json,
    write_jsonl,
    write_yaml,
)
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
    batch_size: int = 1,
    candidate_files: dict[str, str | Path] | None = None,
    output_dir: str | Path | None = None,
) -> dict[str, Any]:
    """运行 Base zero-shot 推理流程。

    mock 模式只验证本地文件流、prompt、prediction schema 和指标接口。
    """

    config = load_experiment_config(config_path)
    if batch_size <= 0:
        raise ValueError("batch_size 必须为正整数。")

    dataset_key = dataset_key or config["dataset"]["development"]
    normalized_splits = _normalize_splits(splits or ["validation", "test"])
    output_dir = _output_dir(config, dataset_key, output_dir)
    scorer = build_scorer(mode, config=config)
    movie_lookup = load_movies(dataset_key, config)

    output_dir.mkdir(parents=True, exist_ok=True)
    write_yaml(output_dir / "config_snapshot.yaml", _config_snapshot(config))
    write_json(
        output_dir / "tokenization_report.json",
        build_tokenization_report(
            mode=mode,
            tokenizer=getattr(scorer, "tokenizer", None),
            answers=_answers_to_check_for_candidate_files(
                config,
                dataset_key,
                normalized_splits,
                candidate_files,
            ),
        ),
    )

    metrics_by_split = {}
    run_counts = {}
    for split_name in normalized_splits:
        y_samples = _read_y_samples(config, dataset_key, split_name, limit)
        n_records = _read_candidate_records(
            config,
            dataset_key,
            split_name,
            limit,
            candidate_files=candidate_files,
        )

        output_split = OUTPUT_SPLIT_NAMES[split_name]
        y_prediction_path = output_dir / f"y_{output_split}_predictions.jsonl"
        n_prediction_path = output_dir / f"n_{output_split}_predictions.jsonl"
        write_jsonl(y_prediction_path, [])
        write_jsonl(n_prediction_path, [])

        y_metric_records = _predict_y_samples(
            y_samples,
            scorer,
            split_name,
            batch_size,
            y_prediction_path,
        )
        n_metric_records = _predict_n_records(
            n_records,
            scorer,
            movie_lookup,
            split_name,
            batch_size,
            n_prediction_path,
        )

        metrics = _metrics_for_split(
            dataset_key,
            split_name,
            y_metric_records,
            n_metric_records,
        )
        write_json(output_dir / f"{output_split}_metrics.json", metrics)
        metrics_by_split[split_name] = metrics
        run_counts[split_name] = {
            "y_predictions": len(y_metric_records),
            "n_predictions": len(n_metric_records),
        }

    run_summary = {
        "model": "base",
        "mode": mode,
        "dataset": dataset_key,
        "splits": normalized_splits,
        "limit": limit,
        "batch_size": batch_size,
        "candidate_files": _resolved_candidate_files_for_summary(
            config,
            dataset_key,
            normalized_splits,
            candidate_files,
        ),
        "counts": run_counts,
        "outputs_dir": str(output_dir),
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "real_model_loaded": mode == "real",
    }
    write_json(output_dir / "run_summary.json", run_summary)

    return {
        "dataset": dataset_key,
        "mode": mode,
        "batch_size": batch_size,
        "candidate_files": _resolved_candidate_files_for_summary(
            config,
            dataset_key,
            normalized_splits,
            candidate_files,
        ),
        "outputs_dir": str(output_dir),
        "counts": run_counts,
        "metrics": metrics_by_split,
    }


def _predict_y_samples(
    samples: list[dict[str, Any]],
    scorer: Any,
    split_name: str,
    batch_size: int,
    output_path: Path,
) -> list[dict[str, Any]]:
    metric_records = []
    batches = list(_batched(samples, batch_size))
    for batch in _progress(batches, f"{split_name} Y"):
        prompts = []
        for sample in batch:
            prompt = render_yesno_prompt(sample)
            assert_no_target_rating_in_yesno_prompt(prompt, sample)
            prompts.append(prompt)

        scores = _score_yesno_batch(scorer, prompts)
        if len(scores) != len(batch):
            raise RuntimeError("Y 批量打分结果数量与输入样本不一致。")

        predictions = []
        for sample, prompt, score in zip(batch, prompts, scores):
            prediction = {
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
            predictions.append(prediction)
            metric_records.append(
                {"score": prediction["p_yes"], "label": prediction["label"]}
            )
        append_jsonl(output_path, predictions)
    return metric_records


def _predict_n_records(
    records: list[dict[str, Any]],
    scorer: Any,
    movie_lookup: dict[str, dict[str, str]],
    split_name: str,
    batch_size: int,
    output_path: Path,
) -> list[dict[str, Any]]:
    metric_records = []
    batches = list(_batched(records, batch_size))
    for batch in _progress(batches, f"{split_name} N"):
        prompts = []
        label_sets = []
        for record in batch:
            prompt = render_candidate_prompt(record, movie_lookup)
            assert_no_candidate_rating_in_candidate_prompt(prompt)
            prompts.append(prompt)
            label_sets.append(list(record.get("label_set", ["A", "B", "C", "D", "E"])))

        scored_batch = _score_candidates_batch(scorer, prompts, label_sets)
        if len(scored_batch) != len(batch):
            raise RuntimeError("N 批量打分结果数量与输入样本不一致。")

        predictions = []
        for record, prompt, label_set, score in zip(
            batch,
            prompts,
            label_sets,
            scored_batch,
        ):
            probabilities = score["label_probabilities"]
            scores = [probabilities[label] for label in label_set]
            prediction = {
                "model": "base",
                "task": "N",
                "split": split_name,
                "user_id": record["user_id"],
                "candidate_movie_ids": record["candidate_movie_ids"],
                "ground_truth_index": record["ground_truth_index"],
                "ground_truth_movie_id": str(record["ground_truth_movie_id"]),
                "label": record["label"],
                "label_set": label_set,
                "candidate_generation": record.get("candidate_generation"),
                "label_probabilities": probabilities,
                "scores": scores,
                "predicted_label": score["predicted_label"],
                "prompt_hash": prompt_hash(prompt),
                "scoring_mode": score.get("scoring_mode"),
            }
            predictions.append(prediction)
            metric_records.append(
                {
                    "scores": prediction["scores"],
                    "ground_truth_index": prediction["ground_truth_index"],
                }
            )
        append_jsonl(output_path, predictions)
    return metric_records


def _metrics_for_split(
    dataset_key: str,
    split_name: str,
    y_metric_records: list[dict[str, Any]],
    n_metric_records: list[dict[str, Any]],
) -> dict[str, Any]:
    binary = binary_metrics(y_metric_records)
    ranking = aggregate_ranking_metrics(
        n_metric_records,
        ks=_ranking_metric_ks(n_metric_records),
    )

    return {
        "model": "base",
        "dataset": dataset_key,
        "split": split_name,
        "binary": {**binary, "samples": len(y_metric_records)},
        "ranking": {**ranking, "samples": len(n_metric_records)},
    }


def _score_yesno_batch(scorer: Any, prompts: list[str]) -> list[dict[str, Any]]:
    if hasattr(scorer, "score_yesno_batch"):
        return scorer.score_yesno_batch(prompts)
    return [scorer.score_yesno(prompt) for prompt in prompts]


def _score_candidates_batch(
    scorer: Any,
    prompts: list[str],
    label_sets: list[list[str]],
) -> list[dict[str, Any]]:
    if hasattr(scorer, "score_candidates_batch"):
        return scorer.score_candidates_batch(prompts, label_sets)
    return [
        scorer.score_candidates(prompt, label_set)
        for prompt, label_set in zip(prompts, label_sets)
    ]


def _batched(records: list[dict[str, Any]], batch_size: int):
    for start in range(0, len(records), batch_size):
        yield records[start:start + batch_size]


def _progress(batches: list[list[dict[str, Any]]], description: str):
    try:
        from tqdm import tqdm
    except ImportError:
        return batches
    return tqdm(batches, desc=description, unit="batch")


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
    candidate_files: dict[str, str | Path] | None = None,
) -> list[dict[str, Any]]:
    path = _candidate_path(config, dataset_key, split_name, candidate_files)
    return read_jsonl(path, limit=limit)


def _candidate_path(
    config: dict[str, Any],
    dataset_key: str,
    split_name: str,
    candidate_files: dict[str, str | Path] | None = None,
) -> Path:
    save_key = "validation" if split_name == "validation" else "test"
    if candidate_files and save_key in candidate_files:
        path = Path(candidate_files[save_key])
        if path.is_absolute():
            return path
        return Path(config["_repo_root"]) / path
    raw_path = config["candidates"]["save_files"][save_key]
    return resolve_repo_path_from_config(
        config,
        raw_path,
        dataset_key=dataset_key,
        split_name=split_name,
    )


def _output_dir(
    config: dict[str, Any],
    dataset_key: str,
    output_dir: str | Path | None = None,
) -> Path:
    if output_dir is not None:
        path = Path(output_dir)
        if path.is_absolute():
            return path
        return Path(config["_repo_root"]) / path
    raw_path = config.get("outputs", {}).get("base", "outputs/base")
    return resolve_repo_path_from_config(config, raw_path, dataset_key=dataset_key)


def _config_snapshot(config: dict[str, Any]) -> dict[str, Any]:
    snapshot = dict(config)
    snapshot.pop("_repo_root", None)
    return snapshot


def _answers_to_check(config: dict[str, Any]) -> list[str]:
    answer_config = config.get("model", {}).get("answer_tokens_to_check", {})
    answers = []
    for answer in answer_config.get("yesno", []):
        answers.append(str(answer))
    for answer in answer_config.get("candidate_labels", []):
        answers.append(str(answer))
    return list(dict.fromkeys(answers))


def _answers_to_check_for_candidate_files(
    config: dict[str, Any],
    dataset_key: str,
    splits: list[str],
    candidate_files: dict[str, str | Path] | None = None,
) -> list[str]:
    answers = _answers_to_check(config)
    for split_name in splits:
        try:
            path = _candidate_path(config, dataset_key, split_name, candidate_files)
            for record in read_jsonl(path, limit=1):
                answers.extend(str(label) for label in record.get("label_set", []))
        except FileNotFoundError:
            continue
    return list(dict.fromkeys(answers))


def _ranking_metric_ks(records: list[dict[str, Any]]) -> list[int]:
    candidate_count = max((len(record["scores"]) for record in records), default=5)
    return default_ranking_ks(candidate_count) or [candidate_count]


def _resolved_candidate_files_for_summary(
    config: dict[str, Any],
    dataset_key: str,
    splits: list[str],
    candidate_files: dict[str, str | Path] | None = None,
) -> dict[str, str]:
    return {
        split_name: str(_candidate_path(config, dataset_key, split_name, candidate_files))
        for split_name in splits
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
    parser.add_argument(
        "--batch-size",
        "--batch_size",
        dest="batch_size",
        type=int,
        default=1,
        help="推理 batch size；real 模式建议先试 8/16，再根据显存调整。",
    )
    parser.add_argument("--valid-candidates", default=None)
    parser.add_argument("--test-candidates", default=None)
    parser.add_argument("--output-dir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    summary = run_base_zero_shot(
        config_path=args.config,
        dataset_key=args.dataset,
        mode=args.mode,
        splits=args.splits,
        limit=args.limit,
        batch_size=args.batch_size,
        candidate_files=_candidate_file_overrides(
            args.valid_candidates,
            args.test_candidates,
        ),
        output_dir=args.output_dir,
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
