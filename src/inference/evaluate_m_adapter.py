"""STEP 7：M-K0 adapter 双接口评测入口。"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any

from src.data.config import resolve_repo_path_from_config
from src.data.preprocess import load_movies
from src.eval.binary_metrics import binary_metrics
from src.eval.ranking_metrics import aggregate_ranking_metrics
from src.inference.base_zero_shot import (
    OUTPUT_SPLIT_NAMES,
    _answers_to_check_for_candidate_files,
    _batched,
    _candidate_file_overrides,
    _config_snapshot,
    _normalize_splits,
    _progress,
    _read_candidate_records,
    _ranking_metric_ks,
    _resolved_candidate_files_for_summary,
    _read_y_samples,
    _score_yesno_batch,
)
from src.inference.evaluate_n_adapter import predict_candidate_label_records
from src.inference.prediction_io import append_jsonl, write_json, write_jsonl, write_yaml
from src.inference.prompts import (
    assert_no_target_rating_in_yesno_prompt,
    prompt_hash,
    render_yesno_prompt,
)
from src.inference.scoring import build_adapter_scorer
from src.inference.tokenization_check import build_tokenization_report
from src.train.train_y import load_training_config


def run_m_adapter_evaluation(
    config_path: str | Path,
    adapter_dir: str | Path | None = None,
    dataset_key: str | None = None,
    mode: str = "mock",
    splits: list[str] | None = None,
    limit: int | None = None,
    batch_size: int = 1,
    output_dir: str | Path | None = None,
    candidate_files: dict[str, str | Path] | None = None,
) -> dict[str, Any]:
    """评测 M adapter 的 M-Y 与 M-N 两个推理接口。"""

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
        candidate_records = _read_candidate_records(
            config,
            dataset_key,
            split_name,
            limit,
            candidate_files=candidate_files,
        )

        output_split = OUTPUT_SPLIT_NAMES[split_name]
        y_prediction_path = output_path / f"m_y_{output_split}_predictions.jsonl"
        n_prediction_path = output_path / f"m_n_{output_split}_predictions.jsonl"
        write_jsonl(y_prediction_path, [])
        write_jsonl(n_prediction_path, [])

        y_metric_records = _predict_y_samples(
            samples=y_samples,
            scorer=scorer,
            split_name=split_name,
            batch_size=batch_size,
            output_path=y_prediction_path,
            adapter_dir=resolved_adapter_dir,
        )
        n_metric_records = predict_candidate_label_records(
            records=candidate_records,
            scorer=scorer,
            movie_lookup=movie_lookup,
            split_name=split_name,
            batch_size=batch_size,
            output_path=n_prediction_path,
            model_name="m_k0",
            inference_mode="m_next_item_candidate_probability",
            adapter_dir=resolved_adapter_dir,
        )

        metrics = _metrics_for_split(
            dataset_key=dataset_key,
            split_name=split_name,
            y_metric_records=y_metric_records,
            n_metric_records=n_metric_records,
            adapter_dir=resolved_adapter_dir,
        )
        write_json(output_path / f"{output_split}_metrics.json", metrics)
        metrics_by_split[split_name] = metrics
        run_counts[split_name] = {
            "m_y_predictions": len(y_metric_records),
            "m_n_predictions": len(n_metric_records),
        }

    evaluation_summary = {
        "model": "m_k0",
        "mode": mode,
        "dataset": dataset_key,
        "splits": normalized_splits,
        "limit": limit,
        "batch_size": batch_size,
        "adapter_dir": str(resolved_adapter_dir) if resolved_adapter_dir else None,
        "candidate_files": _resolved_candidate_files_for_summary(
            config,
            dataset_key,
            normalized_splits,
            candidate_files,
        ),
        "counts": run_counts,
        "outputs_dir": str(output_path),
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "real_model_loaded": mode == "real",
        "binary_scoring": "m_yesno_p_yes",
        "ranking_scoring": "m_next_item_candidate_probability",
    }
    write_json(output_path / "evaluation_summary.json", evaluation_summary)

    return {
        "dataset": dataset_key,
        "mode": mode,
        "batch_size": batch_size,
        "adapter_dir": str(resolved_adapter_dir) if resolved_adapter_dir else None,
        "candidate_files": _resolved_candidate_files_for_summary(
            config,
            dataset_key,
            normalized_splits,
            candidate_files,
        ),
        "outputs_dir": str(output_path),
        "counts": run_counts,
        "metrics": metrics_by_split,
    }


def _predict_y_samples(
    samples: list[dict[str, Any]],
    scorer: Any,
    split_name: str,
    batch_size: int,
    output_path: Path,
    adapter_dir: Path | None,
) -> list[dict[str, Any]]:
    metric_records = []
    batches = list(_batched(samples, batch_size))
    for batch in _progress(batches, f"{split_name} M-Y adapter"):
        prompts = []
        for sample in batch:
            prompt = render_yesno_prompt(sample)
            assert_no_target_rating_in_yesno_prompt(prompt, sample)
            prompts.append(prompt)

        scores = _score_yesno_batch(scorer, prompts)
        if len(scores) != len(batch):
            raise RuntimeError("M-Y 批量打分结果数量与输入样本不一致。")

        predictions = []
        for sample, prompt, score in zip(batch, prompts, scores):
            prediction = {
                "model": "m_k0",
                "task": "Y",
                "inference_mode": "m_yesno_p_yes",
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
                "adapter_dir": str(adapter_dir) if adapter_dir else None,
            }
            predictions.append(prediction)
            metric_records.append(
                {"score": prediction["p_yes"], "label": prediction["label"]}
            )
        append_jsonl(output_path, predictions)
    return metric_records


def _metrics_for_split(
    dataset_key: str,
    split_name: str,
    y_metric_records: list[dict[str, Any]],
    n_metric_records: list[dict[str, Any]],
    adapter_dir: Path | None,
) -> dict[str, Any]:
    binary = binary_metrics(y_metric_records)
    ranking = aggregate_ranking_metrics(n_metric_records, ks=_ranking_metric_ks(n_metric_records))
    return {
        "model": "m_k0",
        "dataset": dataset_key,
        "split": split_name,
        "adapter_dir": str(adapter_dir) if adapter_dir else None,
        "binary": {**binary, "samples": len(y_metric_records)},
        "ranking": {**ranking, "samples": len(n_metric_records)},
        "binary_scoring": "m_yesno_p_yes",
        "ranking_scoring": "m_next_item_candidate_probability",
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
    raw_path = config.get("outputs", {}).get("m", "outputs/m/{dataset}")
    return resolve_repo_path_from_config(config, raw_path, dataset_key=dataset_key)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="评测 M-K0 adapter")
    parser.add_argument("--config", default="configs/m.yaml", help="M-K0 配置路径")
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
    parser.add_argument("--limit", type=int, default=None, help="每个 split 每个接口最多处理多少条样本。")
    parser.add_argument(
        "--batch-size",
        "--batch_size",
        dest="batch_size",
        type=int,
        default=1,
        help="推理 batch size。",
    )
    parser.add_argument("--output-dir", default=None, help="覆盖评测输出目录")
    parser.add_argument("--valid-candidates", default=None)
    parser.add_argument("--test-candidates", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    summary = run_m_adapter_evaluation(
        config_path=args.config,
        adapter_dir=args.adapter_dir,
        dataset_key=args.dataset,
        mode=args.mode,
        splits=args.splits,
        limit=args.limit,
        batch_size=args.batch_size,
        output_dir=args.output_dir,
        candidate_files=_candidate_file_overrides(
            args.valid_candidates,
            args.test_candidates,
        ),
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
