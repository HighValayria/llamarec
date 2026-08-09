"""BPR-MF baseline for fixed next-item candidate sets."""

from __future__ import annotations

import argparse
from collections import defaultdict
from datetime import datetime, timezone
import json
from pathlib import Path
from random import Random
from typing import Any

import torch

from src.data.config import (
    load_experiment_config,
    resolve_configured_output_path,
    resolve_repo_path_from_config,
)
from src.eval.ranking_metrics import aggregate_ranking_metrics, default_ranking_ks
from src.inference.prediction_io import read_jsonl, write_json, write_jsonl, write_yaml


OUTPUT_SPLIT_NAMES = {
    "validation": "valid",
    "test": "test",
}

SPLIT_ALIASES = {
    "validation": "validation",
    "valid": "validation",
    "val": "validation",
    "test": "test",
}


class BPRMatrixFactorization(torch.nn.Module):
    def __init__(self, user_count: int, item_count: int, embedding_dim: int) -> None:
        super().__init__()
        self.user_embeddings = torch.nn.Embedding(user_count, embedding_dim)
        self.item_embeddings = torch.nn.Embedding(item_count, embedding_dim)
        self.item_bias = torch.nn.Embedding(item_count, 1)
        torch.nn.init.normal_(self.user_embeddings.weight, std=0.05)
        torch.nn.init.normal_(self.item_embeddings.weight, std=0.05)
        torch.nn.init.zeros_(self.item_bias.weight)

    def score(self, user_indices: torch.Tensor, item_indices: torch.Tensor) -> torch.Tensor:
        users = self.user_embeddings(user_indices)
        items = self.item_embeddings(item_indices)
        bias = self.item_bias(item_indices).squeeze(-1)
        return (users * items).sum(dim=-1) + bias


def run_bpr_mf_baseline(
    config_path: str | Path,
    dataset_key: str | None = None,
    splits: list[str] | None = None,
    limit: int | None = None,
    output_dir: str | Path | None = None,
    candidate_files: dict[str, str | Path] | None = None,
    embedding_dim: int = 32,
    epochs: int = 5,
    batch_size: int = 1024,
    learning_rate: float = 0.01,
    weight_decay: float = 1e-6,
    seed: int | None = None,
    max_train_samples: int | None = None,
) -> dict[str, Any]:
    """Train BPR-MF on N train targets and score fixed N candidate files."""

    if embedding_dim <= 0:
        raise ValueError("embedding_dim must be positive")
    if epochs < 0:
        raise ValueError("epochs must be non-negative")
    if batch_size <= 0:
        raise ValueError("batch_size must be positive")

    config = load_experiment_config(config_path)
    dataset_key = dataset_key or config["dataset"]["formal"]
    normalized_splits = _normalize_splits(splits or ["validation", "test"])
    output_path = _resolve_output_dir(config, dataset_key, output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    resolved_seed = int(seed if seed is not None else config.get("seed", {}).get("random_seed", 42))
    rng = Random(resolved_seed)
    torch.manual_seed(resolved_seed)

    train_pairs = _load_train_pairs(config, dataset_key, max_train_samples)
    candidate_records_by_split = {
        split_name: _read_candidate_records(
            config,
            dataset_key,
            split_name,
            limit,
            candidate_files=candidate_files,
        )
        for split_name in normalized_splits
    }
    mappings = _build_mappings(train_pairs, candidate_records_by_split)
    encoded_pairs = [
        (mappings["user_to_index"][user_id], mappings["item_to_index"][item_id])
        for user_id, item_id in train_pairs
    ]
    positives_by_user = _positives_by_user(encoded_pairs)

    model = BPRMatrixFactorization(
        user_count=len(mappings["user_to_index"]),
        item_count=len(mappings["item_to_index"]),
        embedding_dim=embedding_dim,
    )
    losses = _train_model(
        model=model,
        pairs=encoded_pairs,
        positives_by_user=positives_by_user,
        item_count=len(mappings["item_to_index"]),
        epochs=epochs,
        batch_size=batch_size,
        learning_rate=learning_rate,
        weight_decay=weight_decay,
        rng=rng,
    )

    write_yaml(output_path / "config_snapshot.yaml", _config_snapshot(config))
    _write_model_artifacts(output_path, model, mappings)

    metrics_by_split = {}
    counts_by_split = {}
    for split_name, records in candidate_records_by_split.items():
        output_split = OUTPUT_SPLIT_NAMES[split_name]
        prediction_path = output_path / f"n_{output_split}_predictions.jsonl"
        predictions, metric_records = _predict_records(
            model=model,
            records=records,
            mappings=mappings,
            split_name=split_name,
        )
        write_jsonl(prediction_path, predictions)

        metrics = _metrics_for_split(dataset_key, split_name, metric_records)
        write_json(output_path / f"{output_split}_metrics.json", metrics)
        metrics_by_split[split_name] = metrics
        counts_by_split[split_name] = {"n_predictions": len(predictions)}

    run_summary = {
        "model": "bpr_mf",
        "dataset": dataset_key,
        "splits": normalized_splits,
        "limit": limit,
        "candidate_files": _resolved_candidate_files_for_summary(
            config,
            dataset_key,
            normalized_splits,
            candidate_files,
        ),
        "outputs_dir": str(output_path),
        "counts": counts_by_split,
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "train_source": "next_item_train.target",
        "train_pairs": len(encoded_pairs),
        "users": len(mappings["user_to_index"]),
        "items": len(mappings["item_to_index"]),
        "embedding_dim": embedding_dim,
        "epochs": epochs,
        "batch_size": batch_size,
        "learning_rate": learning_rate,
        "weight_decay": weight_decay,
        "seed": resolved_seed,
        "epoch_losses": losses,
        "ranking_scoring": "bpr_mf_dot_product",
    }
    write_json(output_path / "run_summary.json", run_summary)

    return {
        "dataset": dataset_key,
        "candidate_files": run_summary["candidate_files"],
        "outputs_dir": str(output_path),
        "counts": counts_by_split,
        "metrics": metrics_by_split,
    }


def _load_train_pairs(
    config: dict[str, Any],
    dataset_key: str,
    max_train_samples: int | None,
) -> list[tuple[str, str]]:
    train_path = resolve_configured_output_path(
        config,
        dataset_key,
        "next_item_samples",
        "train",
    )
    pairs = []
    for record in read_jsonl(train_path, limit=max_train_samples):
        target = record.get("target", {})
        movie_id = target.get("movie_id", record.get("ground_truth_movie_id"))
        pairs.append((str(record["user_id"]), str(movie_id)))
    if not pairs:
        raise ValueError("BPR-MF training requires at least one train pair")
    return pairs


def _build_mappings(
    train_pairs: list[tuple[str, str]],
    candidate_records_by_split: dict[str, list[dict[str, Any]]],
) -> dict[str, dict[str, int]]:
    user_ids = {user_id for user_id, _ in train_pairs}
    item_ids = {item_id for _, item_id in train_pairs}
    for records in candidate_records_by_split.values():
        for record in records:
            user_ids.add(str(record["user_id"]))
            item_ids.update(str(movie_id) for movie_id in record["candidate_movie_ids"])
    return {
        "user_to_index": {user_id: index for index, user_id in enumerate(sorted(user_ids))},
        "item_to_index": {item_id: index for index, item_id in enumerate(sorted(item_ids))},
    }


def _positives_by_user(pairs: list[tuple[int, int]]) -> dict[int, set[int]]:
    positives: dict[int, set[int]] = defaultdict(set)
    for user_index, item_index in pairs:
        positives[user_index].add(item_index)
    return positives


def _train_model(
    model: BPRMatrixFactorization,
    pairs: list[tuple[int, int]],
    positives_by_user: dict[int, set[int]],
    item_count: int,
    epochs: int,
    batch_size: int,
    learning_rate: float,
    weight_decay: float,
    rng: Random,
) -> list[float]:
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate, weight_decay=weight_decay)
    losses = []
    for _ in range(epochs):
        shuffled = list(pairs)
        rng.shuffle(shuffled)
        total_loss = 0.0
        total_examples = 0
        for start in range(0, len(shuffled), batch_size):
            batch = shuffled[start:start + batch_size]
            users = torch.tensor([user for user, _ in batch], dtype=torch.long)
            positives = torch.tensor([item for _, item in batch], dtype=torch.long)
            negatives = torch.tensor(
                [
                    _sample_negative(user, positives_by_user, item_count, rng)
                    for user, _ in batch
                ],
                dtype=torch.long,
            )
            positive_scores = model.score(users, positives)
            negative_scores = model.score(users, negatives)
            loss = -torch.nn.functional.logsigmoid(positive_scores - negative_scores).mean()

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            total_loss += float(loss.detach()) * len(batch)
            total_examples += len(batch)
        losses.append(total_loss / max(total_examples, 1))
    return losses


def _sample_negative(
    user_index: int,
    positives_by_user: dict[int, set[int]],
    item_count: int,
    rng: Random,
) -> int:
    positives = positives_by_user.get(user_index, set())
    if len(positives) >= item_count:
        raise ValueError("negative sampling pool is empty for a user")
    while True:
        candidate = rng.randrange(item_count)
        if candidate not in positives:
            return candidate


def _predict_records(
    model: BPRMatrixFactorization,
    records: list[dict[str, Any]],
    mappings: dict[str, dict[str, int]],
    split_name: str,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    predictions = []
    metric_records = []
    user_to_index = mappings["user_to_index"]
    item_to_index = mappings["item_to_index"]
    model.eval()
    with torch.no_grad():
        for record in records:
            label_set = list(record.get("label_set", []))
            if not label_set:
                label_set = [
                    chr(ord("A") + index)
                    for index in range(len(record["candidate_movie_ids"]))
                ]
            user_index = user_to_index[str(record["user_id"])]
            item_indices = [
                item_to_index[str(movie_id)]
                for movie_id in record["candidate_movie_ids"]
            ]
            users = torch.tensor([user_index] * len(item_indices), dtype=torch.long)
            items = torch.tensor(item_indices, dtype=torch.long)
            scores = [float(value) for value in model.score(users, items).tolist()]
            best_index = max(range(len(scores)), key=lambda index: (scores[index], -index))
            prediction = {
                "model": "bpr_mf",
                "task": "N",
                "inference_mode": "bpr_mf_dot_product",
                "split": split_name,
                "user_id": record["user_id"],
                "candidate_movie_ids": [str(movie_id) for movie_id in record["candidate_movie_ids"]],
                "ground_truth_index": int(record["ground_truth_index"]),
                "ground_truth_movie_id": str(record["ground_truth_movie_id"]),
                "label": record.get("label"),
                "label_set": label_set,
                "candidate_generation": record.get("candidate_generation"),
                "label_scores": dict(zip(label_set, scores)),
                "scores": scores,
                "predicted_label": label_set[best_index],
                "scoring_mode": "bpr_mf_dot_product",
            }
            predictions.append(prediction)
            metric_records.append(
                {
                    "scores": scores,
                    "ground_truth_index": int(record["ground_truth_index"]),
                }
            )
    return predictions, metric_records


def _metrics_for_split(
    dataset_key: str,
    split_name: str,
    metric_records: list[dict[str, Any]],
) -> dict[str, Any]:
    ranking = aggregate_ranking_metrics(metric_records, ks=_ranking_metric_ks(metric_records))
    return {
        "model": "bpr_mf",
        "dataset": dataset_key,
        "split": split_name,
        "ranking": {**ranking, "samples": len(metric_records)},
        "ranking_scoring": "bpr_mf_dot_product",
    }


def _ranking_metric_ks(records: list[dict[str, Any]]) -> list[int]:
    candidate_count = max((len(record["scores"]) for record in records), default=5)
    return default_ranking_ks(candidate_count) or [candidate_count]


def _read_candidate_records(
    config: dict[str, Any],
    dataset_key: str,
    split_name: str,
    limit: int | None,
    candidate_files: dict[str, str | Path] | None = None,
) -> list[dict[str, Any]]:
    return read_jsonl(_candidate_path(config, dataset_key, split_name, candidate_files), limit=limit)


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
    return Path(config["_repo_root"]) / "outputs" / "baselines" / dataset_key / "bpr_mf"


def _write_model_artifacts(
    output_path: Path,
    model: BPRMatrixFactorization,
    mappings: dict[str, dict[str, int]],
) -> None:
    torch.save(model.state_dict(), output_path / "model.pt")
    write_json(output_path / "mappings.json", mappings)


def _config_snapshot(config: dict[str, Any]) -> dict[str, Any]:
    return {
        key: value
        for key, value in config.items()
        if key != "_repo_root"
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
            raise ValueError(f"Unknown split: {split}")
        value = SPLIT_ALIASES[key]
        if value not in normalized:
            normalized.append(value)
    return normalized


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train and evaluate BPR-MF on fixed N candidates")
    parser.add_argument("--config", default="configs/experiment.yaml")
    parser.add_argument("--dataset", default=None)
    parser.add_argument("--splits", nargs="+", default=["validation", "test"])
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--output-dir", default=None)
    parser.add_argument("--valid-candidates", default=None)
    parser.add_argument("--test-candidates", default=None)
    parser.add_argument("--embedding-dim", type=int, default=32)
    parser.add_argument("--epochs", type=int, default=5)
    parser.add_argument("--batch-size", type=int, default=1024)
    parser.add_argument("--learning-rate", type=float, default=0.01)
    parser.add_argument("--weight-decay", type=float, default=1e-6)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--max-train-samples", type=int, default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    summary = run_bpr_mf_baseline(
        config_path=args.config,
        dataset_key=args.dataset,
        splits=args.splits,
        limit=args.limit,
        output_dir=args.output_dir,
        candidate_files=_candidate_file_overrides(
            args.valid_candidates,
            args.test_candidates,
        ),
        embedding_dim=args.embedding_dim,
        epochs=args.epochs,
        batch_size=args.batch_size,
        learning_rate=args.learning_rate,
        weight_decay=args.weight_decay,
        seed=args.seed,
        max_train_samples=args.max_train_samples,
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
