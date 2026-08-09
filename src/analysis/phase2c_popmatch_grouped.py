"""Phase 2C grouped ranking diagnostics for popmatch candidate evaluations."""

from __future__ import annotations

import argparse
import csv
import json
import math
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from src.data.config import load_experiment_config, open_text_auto, resolve_configured_output_path


DEFAULT_RUNS = {
    "Base": "base_k5_popmatch_seed42/n_test_predictions.jsonl",
    "N-K0": "n_k0_k5_popmatch_seed42/n_test_predictions.jsonl",
    "M1": "m1_k5_popmatch_seed42/m_n_test_predictions.jsonl",
    "Y-K0": "y_k0_k5_popmatch_seed42/n_test_predictions.jsonl",
}


def run_phase2c_popmatch_grouped(
    config_path: str | Path,
    dataset_key: str = "movielens-1m",
    split_name: str = "test",
    candidate_file: str | Path | None = None,
    eval_dir: str | Path | None = None,
    output_dir: str | Path | None = None,
    runs: dict[str, str | Path] | None = None,
) -> dict[str, Any]:
    """Summarize popmatch ranking metrics by target popularity bucket."""

    config = load_experiment_config(config_path)
    repo_root = Path(config["_repo_root"])
    eval_path = _resolve_path(
        repo_root,
        eval_dir or "outputs/phase2c/movielens-1m/popmatch_eval",
    )
    output_path = _resolve_path(
        repo_root,
        output_dir or "outputs/phase2c/movielens-1m/popmatch_grouped",
    )
    output_path.mkdir(parents=True, exist_ok=True)

    candidate_path = _resolve_path(
        repo_root,
        candidate_file
        or f"data/candidates/{dataset_key}/variants/k5_popmatch_seed42/{_split_file(split_name)}.jsonl",
    )
    movie_popularity = _load_movie_popularity(config, dataset_key)
    buckets = _candidate_target_buckets(candidate_path, movie_popularity)

    resolved_runs = runs or DEFAULT_RUNS
    rows = []
    for model, prediction_path in resolved_runs.items():
        path = _resolve_path(eval_path, prediction_path)
        rows.extend(_model_bucket_rows(model, path, buckets))

    csv_path = output_path / f"{split_name}_ranking_by_target_popularity.csv"
    markdown_path = output_path / f"{split_name}_ranking_by_target_popularity.md"
    json_path = output_path / f"{split_name}_ranking_by_target_popularity.json"

    _write_csv(csv_path, rows)
    _write_json(json_path, {"dataset": dataset_key, "split": split_name, "rows": rows})
    _write_markdown(markdown_path, dataset_key, split_name, rows)

    return {
        "dataset": dataset_key,
        "split": split_name,
        "models": len(resolved_runs),
        "rows": len(rows),
        "paths": {
            "csv": str(csv_path),
            "json": str(json_path),
            "markdown": str(markdown_path),
        },
    }


def _model_bucket_rows(
    model: str,
    prediction_path: Path,
    buckets: list[str],
) -> list[dict[str, Any]]:
    ranks_by_bucket: dict[str, list[int]] = defaultdict(list)
    predictions = list(_read_jsonl(prediction_path))
    if len(predictions) != len(buckets):
        raise ValueError(
            f"{model} predictions do not match candidate records: "
            f"predictions={len(predictions)}, candidates={len(buckets)}"
        )

    for index, prediction in enumerate(predictions):
        rank = _rank(prediction["scores"], int(prediction["ground_truth_index"]))
        ranks_by_bucket[buckets[index]].append(rank)

    rows = []
    for bucket in ["<=10", "11-50", "51-200", "201-500", ">500"]:
        ranks = ranks_by_bucket.get(bucket, [])
        if not ranks:
            continue
        rows.append(
            {
                "model": model,
                "group_field": "target_popularity_bucket",
                "group_value": bucket,
                "samples": len(ranks),
                "HR@1": _round(sum(rank == 1 for rank in ranks) / len(ranks)),
                "NDCG@5": _round(sum(_ndcg_at_5(rank) for rank in ranks) / len(ranks)),
                "MRR": _round(sum(1 / rank for rank in ranks) / len(ranks)),
                "mean_rank": _round(sum(ranks) / len(ranks)),
            }
        )
    return rows


def _candidate_target_buckets(
    candidate_path: Path,
    movie_popularity: Counter[str],
) -> list[str]:
    buckets = []
    for record in _read_jsonl(candidate_path):
        movie_id = str(record["ground_truth_movie_id"])
        buckets.append(_popularity_bucket(int(movie_popularity.get(movie_id, 0))))
    return buckets


def _load_movie_popularity(config: dict[str, Any], dataset_key: str) -> Counter[str]:
    path = resolve_configured_output_path(config, dataset_key, "full_sequences")
    popularity: Counter[str] = Counter()
    with open_text_auto(path, "rt", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            record = json.loads(line)
            for interaction in record.get("interactions", []):
                popularity[str(interaction["movie_id"])] += 1
    return popularity


def _popularity_bucket(value: int) -> str:
    if value <= 10:
        return "<=10"
    if value <= 50:
        return "11-50"
    if value <= 200:
        return "51-200"
    if value <= 500:
        return "201-500"
    return ">500"


def _rank(scores: list[float], ground_truth_index: int) -> int:
    ranked = sorted(range(len(scores)), key=lambda index: (-float(scores[index]), index))
    return ranked.index(ground_truth_index) + 1


def _ndcg_at_5(rank: int) -> float:
    return 1 / math.log2(rank + 1) if rank <= 5 else 0.0


def _round(value: float) -> float:
    return round(float(value), 10)


def _split_file(split_name: str) -> str:
    if split_name in {"validation", "valid"}:
        return "valid"
    if split_name == "test":
        return "test"
    raise ValueError(f"Unsupported split: {split_name}")


def _resolve_path(base: Path, path: str | Path) -> Path:
    output = Path(path)
    if output.is_absolute():
        return output
    return base / output


def _read_jsonl(path: Path):
    with open_text_auto(path, "rt", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                yield json.loads(line)


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def _write_markdown(
    path: Path,
    dataset_key: str,
    split_name: str,
    rows: list[dict[str, Any]],
) -> None:
    lines = [
        f"# {dataset_key} Phase 2C Popmatch Ranking by Target Popularity ({split_name})",
        "",
        "| model | bucket | samples | HR@1 | NDCG@5 | MRR | mean_rank |",
        "|---|---|---:|---:|---:|---:|---:|",
    ]
    for row in rows:
        lines.append(
            f"| {row['model']} | {row['group_value']} | {row['samples']} | "
            f"{row['HR@1']:.10f} | {row['NDCG@5']:.10f} | "
            f"{row['MRR']:.10f} | {row['mean_rank']:.4f} |"
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _run_overrides(values: list[str] | None) -> dict[str, str] | None:
    if not values:
        return None
    runs = {}
    for value in values:
        if "=" not in value:
            raise ValueError("--run values must be MODEL=path")
        model, path = value.split("=", 1)
        runs[model] = path
    return runs


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Phase 2C popmatch grouped diagnostics")
    parser.add_argument("--config", default="configs/experiment.yaml")
    parser.add_argument("--dataset", default="movielens-1m")
    parser.add_argument("--split", default="test", choices=["validation", "valid", "test"])
    parser.add_argument("--candidate-file", default=None)
    parser.add_argument("--eval-dir", default=None)
    parser.add_argument("--output-dir", default=None)
    parser.add_argument(
        "--run",
        action="append",
        default=None,
        help="Override model prediction paths as MODEL=relative_or_absolute_path.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    summary = run_phase2c_popmatch_grouped(
        config_path=args.config,
        dataset_key=args.dataset,
        split_name=args.split,
        candidate_file=args.candidate_file,
        eval_dir=args.eval_dir,
        output_dir=args.output_dir,
        runs=_run_overrides(args.run),
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
