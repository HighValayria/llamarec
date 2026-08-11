"""SASRec-style baseline for fixed next-item candidate sets."""

from __future__ import annotations

import argparse
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


class SASRec(torch.nn.Module):
    def __init__(
        self,
        item_count: int,
        max_sequence_length: int,
        embedding_dim: int,
        num_heads: int,
        num_layers: int,
        dropout: float,
    ) -> None:
        super().__init__()
        if embedding_dim % num_heads != 0:
            raise ValueError("embedding_dim must be divisible by num_heads")
        self.max_sequence_length = max_sequence_length
        self.item_embeddings = torch.nn.Embedding(item_count + 1, embedding_dim, padding_idx=0)
        self.position_embeddings = torch.nn.Embedding(max_sequence_length, embedding_dim)
        encoder_layer = torch.nn.TransformerEncoderLayer(
            d_model=embedding_dim,
            nhead=num_heads,
            dim_feedforward=embedding_dim * 4,
            dropout=dropout,
            activation="gelu",
            batch_first=True,
        )
        self.encoder = torch.nn.TransformerEncoder(encoder_layer, num_layers=num_layers)
        self.layer_norm = torch.nn.LayerNorm(embedding_dim)
        self.output_bias = torch.nn.Parameter(torch.zeros(item_count + 1))
        self.dropout = torch.nn.Dropout(dropout)
        torch.nn.init.normal_(self.item_embeddings.weight, std=0.02)
        torch.nn.init.normal_(self.position_embeddings.weight, std=0.02)
        with torch.no_grad():
            self.item_embeddings.weight[0].fill_(0.0)

    def sequence_representations(self, sequences: torch.Tensor) -> torch.Tensor:
        batch_size, sequence_length = sequences.shape
        positions = torch.arange(sequence_length, device=sequences.device).unsqueeze(0)
        embeddings = self.item_embeddings(sequences) + self.position_embeddings(positions)
        embeddings = self.dropout(embeddings)
        padding_mask = sequences.eq(0)
        causal_mask = torch.triu(
            torch.ones(sequence_length, sequence_length, device=sequences.device, dtype=torch.bool),
            diagonal=1,
        )
        encoded = self.encoder(
            embeddings,
            mask=causal_mask,
            src_key_padding_mask=padding_mask,
        )
        encoded = self.layer_norm(encoded)
        lengths = sequences.ne(0).sum(dim=1).clamp(min=1)
        last_indices = lengths - 1
        return encoded[torch.arange(batch_size, device=sequences.device), last_indices]

    def logits(self, sequences: torch.Tensor) -> torch.Tensor:
        representations = self.sequence_representations(sequences)
        return representations @ self.item_embeddings.weight.T + self.output_bias

    def score_candidates(
        self,
        sequences: torch.Tensor,
        candidate_indices: torch.Tensor,
    ) -> torch.Tensor:
        representations = self.sequence_representations(sequences)
        candidate_embeddings = self.item_embeddings(candidate_indices)
        candidate_bias = self.output_bias[candidate_indices]
        return (candidate_embeddings * representations.unsqueeze(1)).sum(dim=-1) + candidate_bias


def run_sasrec_baseline(
    config_path: str | Path,
    dataset_key: str | None = None,
    splits: list[str] | None = None,
    limit: int | None = None,
    output_dir: str | Path | None = None,
    candidate_files: dict[str, str | Path] | None = None,
    max_sequence_length: int | None = None,
    embedding_dim: int = 64,
    num_heads: int = 2,
    num_layers: int = 2,
    dropout: float = 0.2,
    epochs: int = 5,
    batch_size: int = 256,
    learning_rate: float = 0.001,
    weight_decay: float = 0.0,
    seed: int | None = None,
    max_train_samples: int | None = None,
    device: str = "auto",
    model_dir: str | Path | None = None,
) -> dict[str, Any]:
    """Train SASRec from N train sequences and score fixed N candidate files."""

    if embedding_dim <= 0:
        raise ValueError("embedding_dim must be positive")
    if num_heads <= 0:
        raise ValueError("num_heads must be positive")
    if num_layers <= 0:
        raise ValueError("num_layers must be positive")
    if epochs < 0:
        raise ValueError("epochs must be non-negative")
    if batch_size <= 0:
        raise ValueError("batch_size must be positive")
    if dropout < 0 or dropout >= 1:
        raise ValueError("dropout must be in [0, 1)")

    config = load_experiment_config(config_path)
    dataset_key = dataset_key or config["dataset"]["formal"]
    normalized_splits = _normalize_splits(splits or ["validation", "test"])
    output_path = _resolve_output_dir(config, dataset_key, output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    resolved_seed = int(seed if seed is not None else config.get("seed", {}).get("random_seed", 42))
    rng = Random(resolved_seed)
    torch.manual_seed(resolved_seed)
    resolved_device = _resolve_device(device)

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
    source_model_dir = _resolve_model_dir(config, model_dir)
    if source_model_dir is None:
        train_records = _load_train_records(config, dataset_key, max_train_samples)
        mappings = _build_mappings(train_records, candidate_records_by_split)
        resolved_max_sequence_length = int(
            max_sequence_length
            if max_sequence_length is not None
            else config.get("dataset", {}).get("history_length", 10)
        )
        if resolved_max_sequence_length <= 0:
            raise ValueError("max_sequence_length must be positive")

        examples = _encode_training_examples(
            train_records,
            mappings["item_to_index"],
            resolved_max_sequence_length,
        )
        if not examples:
            raise ValueError("SASRec training requires at least one non-empty history example")

        model = SASRec(
            item_count=len(mappings["item_to_index"]),
            max_sequence_length=resolved_max_sequence_length,
            embedding_dim=embedding_dim,
            num_heads=num_heads,
            num_layers=num_layers,
            dropout=dropout,
        ).to(resolved_device)
        losses = _train_model(
            model=model,
            examples=examples,
            epochs=epochs,
            batch_size=batch_size,
            learning_rate=learning_rate,
            weight_decay=weight_decay,
            rng=rng,
            device=resolved_device,
        )
        train_examples = len(examples)
        item_count = len(mappings["item_to_index"])
    else:
        model, mappings, loaded_summary = _load_model_artifacts(source_model_dir, resolved_device)
        resolved_max_sequence_length = int(loaded_summary["max_sequence_length"])
        embedding_dim = int(loaded_summary["embedding_dim"])
        num_heads = int(loaded_summary["num_heads"])
        num_layers = int(loaded_summary["num_layers"])
        dropout = float(loaded_summary["dropout"])
        losses = []
        train_examples = int(loaded_summary.get("train_examples", 0))
        item_count = len(mappings["item_to_index"])
        _validate_candidate_items(candidate_records_by_split, mappings["item_to_index"])

    write_yaml(output_path / "config_snapshot.yaml", _config_snapshot(config))
    if source_model_dir is None:
        _write_model_artifacts(output_path, model, mappings)
    else:
        write_json(output_path / "mappings.json", mappings)

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
            max_sequence_length=resolved_max_sequence_length,
            device=resolved_device,
        )
        write_jsonl(prediction_path, predictions)

        metrics = _metrics_for_split(dataset_key, split_name, metric_records)
        write_json(output_path / f"{output_split}_metrics.json", metrics)
        metrics_by_split[split_name] = metrics
        counts_by_split[split_name] = {"n_predictions": len(predictions)}

    run_summary = {
        "model": "sasrec",
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
        "train_source": "next_item_train.history_target",
        "train_examples": train_examples,
        "items": item_count,
        "max_sequence_length": resolved_max_sequence_length,
        "embedding_dim": embedding_dim,
        "num_heads": num_heads,
        "num_layers": num_layers,
        "dropout": dropout,
        "epochs": epochs,
        "batch_size": batch_size,
        "learning_rate": learning_rate,
        "weight_decay": weight_decay,
        "seed": resolved_seed,
        "device": str(resolved_device),
        "epoch_losses": losses,
        "ranking_scoring": "sasrec_sequence_dot_product",
        "model_dir": str(source_model_dir) if source_model_dir is not None else None,
        "eval_only": source_model_dir is not None,
    }
    write_json(output_path / "run_summary.json", run_summary)

    return {
        "dataset": dataset_key,
        "candidate_files": run_summary["candidate_files"],
        "outputs_dir": str(output_path),
        "counts": counts_by_split,
        "metrics": metrics_by_split,
    }


def _load_train_records(
    config: dict[str, Any],
    dataset_key: str,
    max_train_samples: int | None,
) -> list[dict[str, Any]]:
    train_path = resolve_configured_output_path(
        config,
        dataset_key,
        "next_item_samples",
        "train",
    )
    records = read_jsonl(train_path, limit=max_train_samples)
    if not records:
        raise ValueError("SASRec training requires at least one train record")
    return records


def _build_mappings(
    train_records: list[dict[str, Any]],
    candidate_records_by_split: dict[str, list[dict[str, Any]]],
) -> dict[str, dict[str, int]]:
    item_ids: set[str] = set()
    for record in train_records:
        item_ids.update(_history_movie_ids(record))
        item_ids.add(_target_movie_id(record))
    for records in candidate_records_by_split.values():
        for record in records:
            item_ids.update(_history_movie_ids(record))
            item_ids.update(str(movie_id) for movie_id in record["candidate_movie_ids"])
    return {
        "item_to_index": {
            item_id: index + 1
            for index, item_id in enumerate(sorted(item_ids))
        },
    }


def _encode_training_examples(
    records: list[dict[str, Any]],
    item_to_index: dict[str, int],
    max_sequence_length: int,
) -> list[tuple[list[int], int]]:
    examples = []
    for record in records:
        history = [
            item_to_index[movie_id]
            for movie_id in _history_movie_ids(record)
            if movie_id in item_to_index
        ][-max_sequence_length:]
        if not history:
            continue
        target_index = item_to_index[_target_movie_id(record)]
        examples.append((_left_pad(history, max_sequence_length), target_index))
    return examples


def _train_model(
    model: SASRec,
    examples: list[tuple[list[int], int]],
    epochs: int,
    batch_size: int,
    learning_rate: float,
    weight_decay: float,
    rng: Random,
    device: torch.device,
) -> list[float]:
    optimizer = torch.optim.AdamW(model.parameters(), lr=learning_rate, weight_decay=weight_decay)
    losses = []
    for _ in range(epochs):
        model.train()
        shuffled = list(examples)
        rng.shuffle(shuffled)
        total_loss = 0.0
        total_examples = 0
        for start in range(0, len(shuffled), batch_size):
            batch = shuffled[start:start + batch_size]
            sequences = torch.tensor(
                [sequence for sequence, _ in batch],
                dtype=torch.long,
                device=device,
            )
            targets = torch.tensor(
                [target for _, target in batch],
                dtype=torch.long,
                device=device,
            )
            logits = model.logits(sequences)
            logits[:, 0] = -1e9
            if not torch.isfinite(logits).all():
                raise FloatingPointError("SASRec produced non-finite logits during training")
            loss = torch.nn.functional.cross_entropy(logits, targets)
            if not torch.isfinite(loss):
                raise FloatingPointError("SASRec training loss became non-finite")

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            total_loss += float(loss.detach()) * len(batch)
            total_examples += len(batch)
        losses.append(total_loss / max(total_examples, 1))
    return losses


def _predict_records(
    model: SASRec,
    records: list[dict[str, Any]],
    mappings: dict[str, dict[str, int]],
    split_name: str,
    max_sequence_length: int,
    device: torch.device,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    predictions = []
    metric_records = []
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
            history = [
                item_to_index[str(movie_id)]
                for movie_id in _history_movie_ids(record)
            ][-max_sequence_length:]
            sequence = torch.tensor(
                [_left_pad(history, max_sequence_length)],
                dtype=torch.long,
                device=device,
            )
            candidate_indices = torch.tensor(
                [[item_to_index[str(movie_id)] for movie_id in record["candidate_movie_ids"]]],
                dtype=torch.long,
                device=device,
            )
            scores = [
                float(value)
                for value in model.score_candidates(sequence, candidate_indices).squeeze(0).tolist()
            ]
            if not all(_is_finite(score) for score in scores):
                raise FloatingPointError("SASRec produced non-finite candidate scores")
            best_index = max(range(len(scores)), key=lambda index: (scores[index], -index))
            prediction = {
                "model": "sasrec",
                "task": "N",
                "inference_mode": "sasrec_sequence_dot_product",
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
                "scoring_mode": "sasrec_sequence_dot_product",
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
        "model": "sasrec",
        "dataset": dataset_key,
        "split": split_name,
        "ranking": {**ranking, "samples": len(metric_records)},
        "ranking_scoring": "sasrec_sequence_dot_product",
    }


def _history_movie_ids(record: dict[str, Any]) -> list[str]:
    return [str(item["movie_id"]) for item in record.get("history", [])]


def _target_movie_id(record: dict[str, Any]) -> str:
    target = record.get("target", {})
    return str(target.get("movie_id", record.get("ground_truth_movie_id")))


def _left_pad(values: list[int], length: int) -> list[int]:
    trimmed = values[-length:]
    return trimmed + [0] * (length - len(trimmed))


def _resolve_model_dir(config: dict[str, Any], model_dir: str | Path | None) -> Path | None:
    if model_dir is None:
        return None
    path = Path(model_dir)
    if not path.is_absolute():
        path = Path(config["_repo_root"]) / path
    return path


def _load_model_artifacts(
    model_dir: Path,
    device: torch.device,
) -> tuple[SASRec, dict[str, dict[str, int]], dict[str, Any]]:
    mappings_path = model_dir / "mappings.json"
    summary_path = model_dir / "run_summary.json"
    weights_path = model_dir / "model.pt"
    if not mappings_path.exists() or not summary_path.exists() or not weights_path.exists():
        raise FileNotFoundError("model_dir must contain mappings.json, run_summary.json, and model.pt")
    mappings = json.loads(mappings_path.read_text(encoding="utf-8"))
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    model = SASRec(
        item_count=len(mappings["item_to_index"]),
        max_sequence_length=int(summary["max_sequence_length"]),
        embedding_dim=int(summary["embedding_dim"]),
        num_heads=int(summary["num_heads"]),
        num_layers=int(summary["num_layers"]),
        dropout=float(summary["dropout"]),
    ).to(device)
    model.load_state_dict(torch.load(weights_path, map_location=device))
    return model, mappings, summary


def _validate_candidate_items(
    candidate_records_by_split: dict[str, list[dict[str, Any]]],
    item_to_index: dict[str, int],
) -> None:
    missing = set()
    for records in candidate_records_by_split.values():
        for record in records:
            missing.update(
                str(movie_id)
                for movie_id in record["candidate_movie_ids"]
                if str(movie_id) not in item_to_index
            )
            missing.update(
                movie_id
                for movie_id in _history_movie_ids(record)
                if movie_id not in item_to_index
            )
    if missing:
        sample = ", ".join(sorted(missing)[:10])
        raise ValueError(f"model_dir mappings do not contain candidate/history items: {sample}")


def _is_finite(value: float) -> bool:
    return value == value and value not in {float("inf"), float("-inf")}


def _resolve_device(device: str) -> torch.device:
    normalized = device.strip().lower()
    if normalized == "auto":
        return torch.device("cuda" if torch.cuda.is_available() else "cpu")
    if normalized == "cuda" and not torch.cuda.is_available():
        raise ValueError("CUDA requested but torch.cuda.is_available() is false")
    if normalized not in {"cpu", "cuda"}:
        raise ValueError("device must be one of: auto, cpu, cuda")
    return torch.device(normalized)


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
    return Path(config["_repo_root"]) / "outputs" / "baselines" / dataset_key / "sasrec"


def _write_model_artifacts(
    output_path: Path,
    model: SASRec,
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
    parser = argparse.ArgumentParser(description="Train and evaluate SASRec on fixed N candidates")
    parser.add_argument("--config", default="configs/experiment.yaml")
    parser.add_argument("--dataset", default=None)
    parser.add_argument("--splits", nargs="+", default=["validation", "test"])
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--output-dir", default=None)
    parser.add_argument("--valid-candidates", default=None)
    parser.add_argument("--test-candidates", default=None)
    parser.add_argument("--max-sequence-length", type=int, default=None)
    parser.add_argument("--embedding-dim", type=int, default=64)
    parser.add_argument("--num-heads", type=int, default=2)
    parser.add_argument("--num-layers", type=int, default=2)
    parser.add_argument("--dropout", type=float, default=0.2)
    parser.add_argument("--epochs", type=int, default=5)
    parser.add_argument("--batch-size", type=int, default=256)
    parser.add_argument("--learning-rate", type=float, default=0.001)
    parser.add_argument("--weight-decay", type=float, default=0.0)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--max-train-samples", type=int, default=None)
    parser.add_argument("--device", choices=["auto", "cpu", "cuda"], default="auto")
    parser.add_argument("--model-dir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    summary = run_sasrec_baseline(
        config_path=args.config,
        dataset_key=args.dataset,
        splits=args.splits,
        limit=args.limit,
        output_dir=args.output_dir,
        candidate_files=_candidate_file_overrides(
            args.valid_candidates,
            args.test_candidates,
        ),
        max_sequence_length=args.max_sequence_length,
        embedding_dim=args.embedding_dim,
        num_heads=args.num_heads,
        num_layers=args.num_layers,
        dropout=args.dropout,
        epochs=args.epochs,
        batch_size=args.batch_size,
        learning_rate=args.learning_rate,
        weight_decay=args.weight_decay,
        seed=args.seed,
        max_train_samples=args.max_train_samples,
        device=args.device,
        model_dir=args.model_dir,
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
