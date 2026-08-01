"""STEP 6：N-K0 adapter 独立评测入口。"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any

from src.data.config import resolve_repo_path_from_config
from src.data.preprocess import load_movies
from src.eval.ranking_metrics import aggregate_ranking_metrics
from src.inference.base_zero_shot import (
    OUTPUT_SPLIT_NAMES,
    _answers_to_check,
    _batched,
    _config_snapshot,
    _normalize_splits,
    _progress,
    _read_candidate_records,
    _score_candidates_batch,
)
from src.inference.prediction_io import append_jsonl, write_json, write_jsonl, write_yaml
from src.inference.prompts import (
    assert_no_candidate_rating_in_candidate_prompt,
    prompt_hash,
    render_candidate_prompt,
)
from src.inference.scoring import build_adapter_scorer
from src.inference.tokenization_check import build_tokenization_report
from src.train.train_y import load_training_config


def run_n_adapter_evaluation(
    config_path: str | Path,
    adapter_dir: str | Path | None = None,
    dataset_key: str | None = None,
    mode: str = "mock",
    splits: list[str] | None = None,
    limit: int | None = None,
    batch_size: int = 1,
    output_dir: str | Path | None = None,
) -> dict[str, Any]:
    """评测 N adapter 的 next-item candidate ranking 能力。"""

    if batch_size <= 0:
        raise ValueError("batch_size 必须为正整数。")

    config = load_training_config(config_path)
    dataset_key = dataset_key or config["dataset"]["formal"]
    normalized_splits = _normalize_splits(splits or ["validation", "test"])
    resolved_adapter_dir = _resolve_adapter_dir(config, adapter_dir)
    output_path = _resolve_eval_output_dir(
        config=config,
        dataset_key=dataset_key,
        adapter_dir=resolved_adapter_dir,
        output_dir=output_dir,
    )
    output_path.mkdir(parents=True, exist_ok=True)

    scorer = build_adapter_scorer(mode, config=config, adapter_dir=resolved_adapter_dir)
    movie_lookup = load_movies(dataset_key, config)

    write_yaml(output_path / "evaluation_config_snapshot.yaml", _config_snapshot(config))
    write_json(
        output_path / "evaluation_tokenization_report.json",
        build_tokenization_report(
            mode=mode,
            tokenizer=getattr(scorer, "tokenizer", None),
            answers=_candidate_answers_to_check(config),
        ),
    )

    metrics_by_split = {}
    run_counts = {}
    for split_name in normalized_splits:
        candidate_records = _read_candidate_records(config, dataset_key, split_name, limit)
        output_split = OUTPUT_SPLIT_NAMES[split_name]
        prediction_path = output_path / f"n_{output_split}_predictions.jsonl"
        write_jsonl(prediction_path, [])

        metric_records = predict_candidate_label_records(
            records=candidate_records,
            scorer=scorer,
            movie_lookup=movie_lookup,
            split_name=split_name,
            batch_size=batch_size,
            output_path=prediction_path,
            model_name="n_k0",
            inference_mode="candidate_label_probability",
            adapter_dir=resolved_adapter_dir,
        )

        metrics = _metrics_for_split(
            dataset_key=dataset_key,
            split_name=split_name,
            metric_records=metric_records,
            adapter_dir=resolved_adapter_dir,
            model_name="n_k0",
        )
        write_json(output_path / f"{output_split}_metrics.json", metrics)
        metrics_by_split[split_name] = metrics
        run_counts[split_name] = {"n_predictions": len(metric_records)}

    evaluation_summary = {
        "model": "n_k0",
        "mode": mode,
        "dataset": dataset_key,
        "splits": normalized_splits,
        "limit": limit,
        "batch_size": batch_size,
        "adapter_dir": str(resolved_adapter_dir) if resolved_adapter_dir else None,
        "counts": run_counts,
        "outputs_dir": str(output_path),
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "real_model_loaded": mode == "real",
        "ranking_scoring": "candidate_label_probability",
    }
    write_json(output_path / "evaluation_summary.json", evaluation_summary)

    return {
        "dataset": dataset_key,
        "mode": mode,
        "batch_size": batch_size,
        "adapter_dir": str(resolved_adapter_dir) if resolved_adapter_dir else None,
        "outputs_dir": str(output_path),
        "counts": run_counts,
        "metrics": metrics_by_split,
    }


def predict_candidate_label_records(
    records: list[dict[str, Any]],
    scorer: Any,
    movie_lookup: dict[str, dict[str, str]],
    split_name: str,
    batch_size: int,
    output_path: Path,
    model_name: str,
    inference_mode: str,
    adapter_dir: Path | None,
) -> list[dict[str, Any]]:
    """使用 ``P(A)...P(E)`` 对固定候选集排序并写出 prediction。"""

    metric_records = []
    batches = list(_batched(records, batch_size))
    for batch in _progress(batches, f"{split_name} {model_name} N"):
        prompts = []
        label_sets = []
        for record in batch:
            prompt = render_candidate_prompt(record, movie_lookup)
            assert_no_candidate_rating_in_candidate_prompt(prompt)
            prompts.append(prompt)
            label_sets.append(list(record.get("label_set", ["A", "B", "C", "D", "E"])))

        scored_batch = _score_candidates_batch(scorer, prompts, label_sets)
        if len(scored_batch) != len(batch):
            raise RuntimeError("N adapter 批量打分结果数量与输入样本不一致。")

        predictions = []
        for record, prompt, label_set, score in zip(batch, prompts, label_sets, scored_batch):
            probabilities = score["label_probabilities"]
            scores = [probabilities[label] for label in label_set]
            prediction = {
                "model": model_name,
                "task": "N",
                "inference_mode": inference_mode,
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
                "adapter_dir": str(adapter_dir) if adapter_dir else None,
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
    metric_records: list[dict[str, Any]],
    adapter_dir: Path | None,
    model_name: str,
) -> dict[str, Any]:
    ranking = aggregate_ranking_metrics(metric_records)
    return {
        "model": model_name,
        "dataset": dataset_key,
        "split": split_name,
        "adapter_dir": str(adapter_dir) if adapter_dir else None,
        "ranking": {**ranking, "samples": len(metric_records)},
        "ranking_scoring": "candidate_label_probability",
    }


def _resolve_adapter_dir(
    config: dict[str, Any],
    adapter_dir: str | Path | None,
) -> Path | None:
    if adapter_dir is None:
        return None
    path = Path(adapter_dir)
    if path.is_absolute():
        return path
    return Path(config["_repo_root"]) / path


def _resolve_eval_output_dir(
    config: dict[str, Any],
    dataset_key: str,
    adapter_dir: Path | None,
    output_dir: str | Path | None,
) -> Path:
    if output_dir is not None:
        output_path = Path(output_dir)
        if output_path.is_absolute():
            return output_path
        return Path(config["_repo_root"]) / output_path
    if adapter_dir and adapter_dir.name == "adapter":
        return adapter_dir.parent
    raw_path = config.get("outputs", {}).get("n", "outputs/n/{dataset}")
    return resolve_repo_path_from_config(config, raw_path, dataset_key=dataset_key)


def _candidate_answers_to_check(config: dict[str, Any]) -> list[str]:
    answers = [
        answer
        for answer in _answers_to_check(config)
        if answer not in {"Yes", "No"}
    ]
    return answers or ["A", "B", "C", "D", "E"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="评测 N-K0 adapter")
    parser.add_argument("--config", default="configs/n.yaml", help="N-K0 配置路径")
    parser.add_argument("--dataset", default=None, help="数据集 key；默认使用 dataset.formal")
    parser.add_argument("--adapter-dir", default=None, help="已保存 adapter 目录；real 模式必填")
    parser.add_argument(
        "--mode",
        choices=["mock", "real"],
        default="mock",
        help="mock 用于本地 dry-run；real 在云端加载 base model + adapter。",
    )
    parser.add_argument(
        "--splits",
        nargs="+",
        default=["validation", "test"],
        help="要运行的 split，可选 validation/valid/test。",
    )
    parser.add_argument("--limit", type=int, default=None, help="每个 split 最多处理多少条 N 候选样本。")
    parser.add_argument(
        "--batch-size",
        "--batch_size",
        dest="batch_size",
        type=int,
        default=1,
        help="推理 batch size。",
    )
    parser.add_argument("--output-dir", default=None, help="覆盖评测输出目录")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    summary = run_n_adapter_evaluation(
        config_path=args.config,
        adapter_dir=args.adapter_dir,
        dataset_key=args.dataset,
        mode=args.mode,
        splits=args.splits,
        limit=args.limit,
        batch_size=args.batch_size,
        output_dir=args.output_dir,
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
