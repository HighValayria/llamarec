"""Seed42 no-training deep analysis handoff for exposure scaling.

This script only reads existing artifacts. It never trains, resumes training,
creates checkpoints, or launches model inference.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import random
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    from src.eval.binary_metrics import accuracy, auc, f1_score
except Exception:  # pragma: no cover - keeps handoff usable in partial envs
    accuracy = auc = f1_score = None

BOOTSTRAP_SEED = 20260902
DEFAULT_BOOTSTRAPS = 5000
REQUIRED_ARTIFACTS = [
    "README.md",
    "binary_predictions_y96_m96_valid.csv",
    "binary_predictions_y96_m96_test.csv",
    "binary_bootstrap_summary.csv",
    "binary_bootstrap_report.md",
    "binary_calibration_summary.csv",
    "binary_error_overlap.csv",
    "ranking_predictions_k5_valid.csv",
    "ranking_predictions_k20_valid.csv",
    "ranking_predictions_k50_valid.csv",
    "ranking_predictions_k5_test.csv",
    "ranking_predictions_k20_test.csv",
    "ranking_predictions_k50_test.csv",
    "ranking_bootstrap_summary.csv",
    "ranking_win_loss_tie.csv",
    "candidate_protocol_stats.csv",
    "candidate_protocol_audit.md",
    "slice_analysis.csv",
    "training_curve_y96.csv",
    "training_curve_n96.csv",
    "training_curve_m96.csv",
    "training_protocol_comparison.md",
    "exposure_coverage.csv",
    "sasrec_exposure_alignment.csv",
    "seed42_claim_evidence_matrix.md",
    "multiseed_recommendation.md",
]


@dataclass(frozen=True)
class Paths:
    root: Path
    out: Path
    y96: Path
    n96: Path
    m96: Path
    n200: Path
    phase2a: Path


def main() -> None:
    args = parse_args()
    root = Path(args.root).resolve()
    out = (root / args.output_dir).resolve()
    out.mkdir(parents=True, exist_ok=True)
    paths = Paths(
        root=root,
        out=out,
        y96=root / "outputs/y/movielens-1m/exposure_y_s12000",
        n96=root / "outputs/n/movielens-1m/exposure_n_s12000",
        m96=root / "outputs/m/movielens-1m/exposure_m1_s24000",
        n200=root / "outputs/n/movielens-1m/exposure_n_s25000",
        phase2a=root / "outputs/phase2a/current96_ranking_robustness",
    )
    ctx = load_context(root)
    manifest: list[dict[str, Any]] = []

    binary_frames: dict[str, list[dict[str, Any]]] = {}
    for split in ("valid", "test"):
        rows, status = build_binary_predictions(paths, split, ctx)
        binary_frames[split] = rows
        name = f"binary_predictions_y96_m96_{split}.csv"
        write_csv(out / name, rows)
        manifest.append(status_row(name, status, len(rows)))

    binary_boot = binary_bootstrap(binary_frames, args.bootstrap_replicates)
    write_csv(out / "binary_bootstrap_summary.csv", binary_boot)
    write_binary_bootstrap_report(out / "binary_bootstrap_report.md", binary_boot)
    binary_boot_status = ok_or_missing(binary_boot, "paired binary predictions missing")
    manifest.append(status_row("binary_bootstrap_summary.csv", binary_boot_status, len(binary_boot)))
    manifest.append(status_row("binary_bootstrap_report.md", binary_boot_status, 1 if binary_boot else 0))

    cal_rows, rel_rows = binary_calibration(binary_frames)
    write_csv(out / "binary_calibration_summary.csv", cal_rows)
    write_csv(out / "binary_calibration_bins.csv", rel_rows)
    manifest.append(status_row("binary_calibration_summary.csv", ok_or_missing(cal_rows, "paired binary predictions missing"), len(cal_rows)))

    overlap = binary_error_overlap(binary_frames)
    write_csv(out / "binary_error_overlap.csv", overlap)
    manifest.append(status_row("binary_error_overlap.csv", ok_or_missing(overlap, "paired binary predictions missing"), len(overlap)))

    ranking_frames: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for variant in ("k5", "k20", "k50"):
        for split in ("valid", "test"):
            rows, status = build_ranking_predictions(paths, variant, split, ctx)
            ranking_frames[(variant, split)] = rows
            name = f"ranking_predictions_{variant}_{split}.csv"
            write_csv(out / name, rows)
            manifest.append(status_row(name, status, len(rows)))

    rank_boot = ranking_bootstrap(ranking_frames, args.bootstrap_replicates)
    write_csv(out / "ranking_bootstrap_summary.csv", rank_boot)
    manifest.append(status_row("ranking_bootstrap_summary.csv", ok_or_missing(rank_boot, "ranking predictions missing"), len(rank_boot)))

    win_loss = ranking_win_loss_tie(ranking_frames)
    write_csv(out / "ranking_win_loss_tie.csv", win_loss)
    manifest.append(status_row("ranking_win_loss_tie.csv", ok_or_missing(win_loss, "ranking predictions missing"), len(win_loss)))

    cand_stats, cand_audit = candidate_protocol(paths, ctx)
    write_csv(out / "candidate_protocol_stats.csv", cand_stats)
    write_text(out / "candidate_protocol_audit.md", cand_audit)
    cand_status = ok_or_missing([r for r in cand_stats if r.get("status") == "OK"], "candidate files missing")
    manifest.append(status_row("candidate_protocol_stats.csv", cand_status, len(cand_stats)))
    manifest.append(status_row("candidate_protocol_audit.md", cand_status, 1 if cand_stats else 0))

    slices = slice_analysis(ranking_frames)
    write_csv(out / "slice_analysis.csv", slices)
    manifest.append(status_row("slice_analysis.csv", ok_or_missing(slices, "ranking predictions missing"), len(slices)))

    curve_statuses = training_curves(paths)
    manifest.extend(curve_statuses)
    write_text(out / "training_protocol_comparison.md", training_protocol_comparison(paths))
    manifest.append(status_row("training_protocol_comparison.md", "OK", 1))

    coverage = exposure_coverage(paths, ctx)
    write_csv(out / "exposure_coverage.csv", coverage)
    manifest.append(status_row("exposure_coverage.csv", ok_or_missing(coverage, "processed training pools missing"), len(coverage)))

    sasrec = sasrec_alignment(paths.root)
    write_csv(out / "sasrec_exposure_alignment.csv", sasrec)
    sasrec_status = ok_or_missing([r for r in sasrec if r.get("source") != "MISSING"], "SASRec metrics missing")
    manifest.append(status_row("sasrec_exposure_alignment.csv", sasrec_status, len(sasrec)))

    write_claim_matrix(out / "seed42_claim_evidence_matrix.md", binary_boot, rank_boot, cand_stats, slices)
    manifest.append(status_row("seed42_claim_evidence_matrix.md", "OK", 1))
    write_multiseed_recommendation(out / "multiseed_recommendation.md", binary_boot, rank_boot)
    manifest.append(status_row("multiseed_recommendation.md", "OK", 1))

    manifest.append(status_row("README.md", "OK", 1))
    present = {m["artifact"] for m in manifest}
    for name in REQUIRED_ARTIFACTS:
        if name not in present:
            manifest.append(status_row(name, "MISSING: not generated", 0))
    write_csv(out / "artifact_manifest.csv", manifest)
    write_readme(out / "README.md", manifest, args.bootstrap_replicates)
    print(f"Seed42 no-training analysis finished: {out}")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--root", default=".")
    p.add_argument("--output-dir", default=".agent/exposure_scaling/analysis_handoff")
    p.add_argument("--bootstrap-replicates", type=int, default=DEFAULT_BOOTSTRAPS)
    return p.parse_args()


def load_context(root: Path) -> dict[str, Any]:
    popularity = ratings_item_popularity(root)
    return {
        "pref_valid": sample_map(root / "data/processed/movielens-1m/preference_valid.jsonl"),
        "pref_test": sample_map(root / "data/processed/movielens-1m/preference_test.jsonl"),
        "next_valid": sample_map(root / "data/processed/movielens-1m/next_item_valid.jsonl"),
        "next_test": sample_map(root / "data/processed/movielens-1m/next_item_test.jsonl"),
        "train_n": list_jsonl(root / "data/processed/movielens-1m/next_item_train.jsonl", limit=200000),
        "train_y": list_jsonl(root / "data/processed/movielens-1m/preference_train.jsonl", limit=200000),
        "ratings_items": ratings_items(root),
        "metadata_items": metadata_items(root),
        "popularity": popularity or item_popularity(root / "data/processed/movielens-1m/full_sequences.jsonl"),
    }


def list_jsonl(path: Path | None, limit: int | None = None) -> list[dict[str, Any]]:
    if path is None:
        return []
    if not path.exists():
        return []
    rows = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))
                if limit is not None and len(rows) >= limit:
                    break
    return rows


def sample_map(path: Path) -> dict[tuple[str, str], dict[str, Any]]:
    out = {}
    for r in list_jsonl(path):
        uid = str(r.get("user_id", ""))
        tid = str(r.get("target_movie_id", r.get("ground_truth_movie_id", r.get("movie_id", ""))))
        hist = get_history(r)
        out[(uid, tid)] = {
            "history_length": len(hist),
            "rating": r.get("rating", r.get("target_rating")),
            "target_movie_id": tid,
        }
    return out


def get_history(r: dict[str, Any]) -> list[Any]:
    for key in ("history_movie_ids", "history_items", "history", "input_movie_ids"):
        v = r.get(key)
        if isinstance(v, list):
            return v
    return []


def item_popularity(path: Path) -> Counter[str]:
    c: Counter[str] = Counter()
    for r in list_jsonl(path):
        for item in get_history(r):
            c[str(item)] += 1
        tid = r.get("target_movie_id", r.get("ground_truth_movie_id"))
        if tid is not None:
            c[str(tid)] += 1
    return c


def ratings_items(root: Path) -> set[str]:
    path = root / "data/raw/movielens-1m/ratings.dat"
    if not path.exists():
        path = root / "data/ml-1m/ratings.dat"
    items: set[str] = set()
    if path.exists():
        with path.open("r", encoding="latin-1") as f:
            for line in f:
                parts = line.rstrip("\n").split("::")
                if len(parts) >= 2:
                    items.add(parts[1])
    stats = root / "data/processed/movielens-1m/stats.json"
    if not items and stats.exists():
        n = json.loads(stats.read_text(encoding="utf-8")).get("movie_count")
        if n:
            items = {f"__unknown_{i}" for i in range(int(n))}
    return items


def metadata_items(root: Path) -> set[str]:
    path = root / "data/raw/movielens-1m/movies.dat"
    if not path.exists():
        path = root / "data/ml-1m/movies.dat"
    items: set[str] = set()
    if path.exists():
        with path.open("r", encoding="latin-1") as f:
            for line in f:
                parts = line.rstrip("\n").split("::")
                if parts:
                    items.add(parts[0])
    return items


def ratings_item_popularity(root: Path) -> Counter[str]:
    path = root / "data/raw/movielens-1m/ratings.dat"
    if not path.exists():
        path = root / "data/ml-1m/ratings.dat"
    c: Counter[str] = Counter()
    if path.exists():
        with path.open("r", encoding="latin-1") as f:
            for line in f:
                parts = line.rstrip("\n").split("::")
                if len(parts) >= 2:
                    c[parts[1]] += 1
    return c


def first_existing(paths: list[Path]) -> Path | None:
    for p in paths:
        if p.exists():
            return p
    return None


def build_binary_predictions(paths: Paths, split: str, ctx: dict[str, Any]) -> tuple[list[dict[str, Any]], str]:
    y_file = first_existing([
        paths.y96 / f"popmatch_eval_valid_only/y_{split}_predictions.jsonl",
        paths.y96 / f"popmatch_eval/y_{split}_predictions.jsonl",
    ])
    m_file = first_existing([
        paths.m96 / f"popmatch_eval_valid_only/m_y_{split}_predictions.jsonl",
        paths.m96 / f"popmatch_eval/m_y_{split}_predictions.jsonl",
    ])
    if not y_file or not m_file:
        return [], f"MISSING: y_file={bool(y_file)} m_file={bool(m_file)}"
    y = {binary_key(r): r for r in list_jsonl(y_file)}
    m = {binary_key(r): r for r in list_jsonl(m_file)}
    common = sorted(set(y) & set(m))
    ctx_map = ctx["pref_valid" if split == "valid" else "pref_test"]
    pop = ctx["popularity"]
    rows = []
    for key in common:
        yr, mr = y[key], m[key]
        uid, tid, label = key
        meta = ctx_map.get((uid, tid), {})
        p_y = prob_yes(yr)
        p_m = prob_yes(mr)
        rows.append({
            "split": split,
            "user_id": uid,
            "target_movie_id": tid,
            "label": label,
            "label_int": label_int(label),
            "p_yes_y96": p_y,
            "p_yes_m96": p_m,
            "pred_y96_threshold_0_5": int(p_y >= 0.5) if p_y is not None else None,
            "pred_m96_threshold_0_5": int(p_m >= 0.5) if p_m is not None else None,
            "delta_p_yes_m_minus_y": none_sub(p_m, p_y),
            "history_length": meta.get("history_length"),
            "rating": meta.get("rating"),
            "target_popularity": pop.get(tid, 0),
        })
    missing = len(set(y) ^ set(m))
    status = "OK" if rows else "MISSING: no paired rows"
    if missing:
        status += f"; unpaired={missing}"
    return rows, status


def binary_key(r: dict[str, Any]) -> tuple[str, str, str]:
    return (str(r.get("user_id", "")), str(r.get("target_movie_id", r.get("movie_id", ""))), str(r.get("label", "")))


def label_int(v: Any) -> int:
    if isinstance(v, bool):
        return int(v)
    s = str(v).lower()
    if s in {"1", "true", "yes", "positive", "like"}:
        return 1
    return 0


def prob_yes(r: dict[str, Any]) -> float | None:
    for key in ("p_yes", "score", "yes_probability", "prob_yes"):
        if key in r and r[key] is not None:
            return float(r[key])
    return None


def none_sub(a: Any, b: Any) -> float | None:
    if a is None or b is None:
        return None
    return float(a) - float(b)


def binary_delta(rows: list[dict[str, Any]]) -> dict[str, float | None]:
    labels = [int(r["label_int"]) for r in rows]
    y_scores = [float(r["p_yes_y96"]) for r in rows]
    m_scores = [float(r["p_yes_m96"]) for r in rows]
    y_pred = [1 if s >= 0.5 else 0 for s in y_scores]
    m_pred = [1 if s >= 0.5 else 0 for s in m_scores]
    return {
        "AUC": metric_delta(auc, m_scores, y_scores, labels),
        "F1": metric_pair_delta(f1_score, m_pred, y_pred, labels),
        "Accuracy": metric_pair_delta(accuracy, m_pred, y_pred, labels),
    }


def metric_delta(fn: Any, m_scores: list[float], y_scores: list[float], labels: list[int]) -> float | None:
    if fn is None or len(set(labels)) < 2:
        return None
    return float(fn(m_scores, labels) - fn(y_scores, labels))


def metric_pair_delta(fn: Any, m_pred: list[int], y_pred: list[int], labels: list[int]) -> float | None:
    if fn is None:
        return None
    return float(fn(m_pred, labels) - fn(y_pred, labels))


def group_indices(rows: list[dict[str, Any]], key: str) -> dict[str, list[int]]:
    groups: dict[str, list[int]] = defaultdict(list)
    for i, r in enumerate(rows):
        groups[str(r.get(key, ""))].append(i)
    return groups


def bootstrap_rows(rows: list[dict[str, Any]], reps: int, seed: int):
    groups = group_indices(rows, "user_id")
    keys = list(groups)
    rng = random.Random(seed)
    for _ in range(reps):
        idx = []
        for k in rng.choices(keys, k=len(keys)):
            idx.extend(groups[k])
        yield [rows[i] for i in idx], len(keys)


def binary_bootstrap(frames: dict[str, list[dict[str, Any]]], reps: int) -> list[dict[str, Any]]:
    out = []
    for split, rows in frames.items():
        if not rows:
            continue
        point = binary_delta(rows)
        vals = {"AUC": [], "F1": [], "Accuracy": []}
        for sample, _ in bootstrap_rows(rows, reps, BOOTSTRAP_SEED + (0 if split == "valid" else 10000)):
            d = binary_delta(sample)
            for metric, value in d.items():
                if value is not None:
                    vals[metric].append(value)
        user_count = len(group_indices(rows, "user_id"))
        for metric in ("AUC", "F1", "Accuracy"):
            v = vals[metric]
            out.append({
                "split": split,
                "metric": metric,
                "delta_definition": "M1-96 - Y96",
                "point_estimate": point.get(metric),
                "bootstrap_mean": mean(v),
                "ci95_low": percentile(v, 2.5),
                "ci95_high": percentile(v, 97.5),
                "p_delta_gt_0": mean([1.0 if x > 0 else 0.0 for x in v]),
                "bootstrap_unit": "user",
                "replicates": reps,
                "sample_count": len(rows),
                "user_count": user_count,
                "threshold_for_f1_accuracy": 0.5,
            })
    return out


def binary_calibration(frames: dict[str, list[dict[str, Any]]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    summary, bins = [], []
    for split, rows in frames.items():
        if not rows:
            continue
        labels = [int(r["label_int"]) for r in rows]
        for model, score_key in (("Y96", "p_yes_y96"), ("M1-96", "p_yes_m96")):
            scores = [float(r[score_key]) for r in rows]
            summary.append({
                "split": split,
                "model": model,
                "threshold_for_f1_accuracy": 0.5,
                "brier_score": mean([(s - y) ** 2 for s, y in zip(scores, labels)]),
                "ece_10_bin": ece(scores, labels),
                "mean_p_yes": mean(scores),
                "mean_p_yes_positive": mean([s for s, y in zip(scores, labels) if y == 1]),
                "mean_p_yes_negative": mean([s for s, y in zip(scores, labels) if y == 0]),
                "samples": len(rows),
            })
            bins.extend(reliability_bins(split, model, scores, labels))
    return summary, bins


def reliability_bins(split: str, model: str, scores: list[float], labels: list[int], bins: int = 10) -> list[dict[str, Any]]:
    out = []
    n = len(scores)
    for i in range(bins):
        lo, hi = i / bins, (i + 1) / bins
        idx = [j for j, s in enumerate(scores) if lo <= s < hi or (i == bins - 1 and s == hi)]
        conf = mean([scores[j] for j in idx])
        pos = mean([labels[j] for j in idx])
        out.append({
            "split": split,
            "model": model,
            "bin": i,
            "lower": lo,
            "upper": hi,
            "count": len(idx),
            "fraction": len(idx) / n if n else None,
            "mean_confidence": conf,
            "empirical_positive_rate": pos,
            "abs_gap": abs(conf - pos) if conf is not None and pos is not None else None,
        })
    return out


def ece(scores: list[float], labels: list[int]) -> float | None:
    if not scores:
        return None
    total = 0.0
    for row in reliability_bins("", "", scores, labels):
        if row["count"] and row["abs_gap"] is not None:
            total += row["fraction"] * row["abs_gap"]
    return total


def binary_error_overlap(frames: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    out = []
    for split, rows in frames.items():
        if not rows:
            continue
        out.extend(binary_overlap(split, "overall", "all", rows))
        for field, dim in (("rating", "rating"), ("history_length", "history_length_tercile"), ("target_popularity", "target_popularity_tercile")):
            for bucket, part in buckets(rows, field).items():
                out.extend(binary_overlap(split, dim, bucket, part))
    return out


def binary_overlap(split: str, dim: str, bucket: str, rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    c = Counter()
    for r in rows:
        label = int(r["label_int"])
        y_ok = int(r["pred_y96_threshold_0_5"]) == label
        m_ok = int(r["pred_m96_threshold_0_5"]) == label
        name = "both_correct" if y_ok and m_ok else "both_wrong" if not y_ok and not m_ok else "y_only_correct" if y_ok else "m_only_correct"
        c[name] += 1
    total = len(rows)
    return [{"split": split, "dimension": dim, "bucket": bucket, "outcome": k, "count": c[k], "fraction": c[k] / total if total else None, "samples": total} for k in ("both_correct", "both_wrong", "y_only_correct", "m_only_correct")]



def buckets(rows: list[dict[str, Any]], field: str, n: int = 3) -> dict[str, list[dict[str, Any]]]:
    vals = sorted(float(r[field]) for r in rows if r.get(field) not in (None, ""))
    if not vals:
        return {"missing": rows}
    q1 = vals[len(vals) // n]
    q2 = vals[(2 * len(vals)) // n]
    out = {"low": [], "mid": [], "high": [], "missing": []}
    for r in rows:
        v = r.get(field)
        if v in (None, ""):
            out["missing"].append(r)
        elif float(v) <= q1:
            out["low"].append(r)
        elif float(v) <= q2:
            out["mid"].append(r)
        else:
            out["high"].append(r)
    return {k: v for k, v in out.items() if v}


def build_ranking_predictions(paths: Paths, variant: str, split: str, ctx: dict[str, Any]) -> tuple[list[dict[str, Any]], str]:
    n_file, m_file = ranking_prediction_files(paths, variant, split)
    if not n_file or not m_file:
        return [], f"MISSING: n_file={bool(n_file)} m_file={bool(m_file)}"
    n = {ranking_key(r): r for r in list_jsonl(n_file)}
    m = {ranking_key(r): r for r in list_jsonl(m_file)}
    common = sorted(set(n) & set(m))
    ctx_map = ctx["next_valid" if split == "valid" else "next_test"]
    pop = ctx["popularity"]
    rows = []
    for key in common:
        nr, mr = n[key], m[key]
        uid, gt = key
        n_scores = score_list(nr)
        m_scores = score_list(mr)
        n_rank = gt_rank(nr, n_scores)
        m_rank = gt_rank(mr, m_scores)
        candidates = candidate_ids(nr)
        meta = ctx_map.get((uid, gt), {})
        neg_pops = [pop.get(str(c), 0) for c in candidates if str(c) != gt]
        target_pop = pop.get(gt, 0)
        rows.append({
            "variant": variant,
            "split": split,
            "user_id": uid,
            "ground_truth_movie_id": gt,
            "candidate_count_n96": len(candidate_ids(nr)),
            "candidate_count_m96": len(candidate_ids(mr)),
            "same_candidate_order": json.dumps(candidate_ids(nr)) == json.dumps(candidate_ids(mr)),
            "gt_rank_n96": n_rank,
            "gt_rank_m96": m_rank,
            "delta_rank_n_minus_m": none_sub(n_rank, m_rank),
            "n96_HR@1": hr(n_rank, 1),
            "m96_HR@1": hr(m_rank, 1),
            "n96_HR@5": hr(n_rank, 5),
            "m96_HR@5": hr(m_rank, 5),
            "n96_HR@10": hr(n_rank, 10),
            "m96_HR@10": hr(m_rank, 10),
            "n96_HR@20": hr(n_rank, 20),
            "m96_HR@20": hr(m_rank, 20),
            "n96_HR@50": hr(n_rank, 50),
            "m96_HR@50": hr(m_rank, 50),
            "n96_NDCG@5": ndcg(n_rank, 5),
            "m96_NDCG@5": ndcg(m_rank, 5),
            "n96_NDCG@10": ndcg(n_rank, 10),
            "m96_NDCG@10": ndcg(m_rank, 10),
            "n96_NDCG@20": ndcg(n_rank, 20),
            "m96_NDCG@20": ndcg(m_rank, 20),
            "n96_NDCG@50": ndcg(n_rank, 50),
            "m96_NDCG@50": ndcg(m_rank, 50),
            "n96_MRR": mrr(n_rank),
            "m96_MRR": mrr(m_rank),
            "history_length": meta.get("history_length"),
            "target_rating": meta.get("rating"),
            "target_popularity": target_pop,
            "negative_popularity_mean": mean(neg_pops),
            "target_minus_negative_popularity_mean": target_pop - mean(neg_pops) if neg_pops else None,
            "candidate_movie_ids_json": json.dumps(candidates, ensure_ascii=False),
            "candidate_generation_json": json.dumps(nr.get("candidate_generation", {}), ensure_ascii=False),
        })
    missing = len(set(n) ^ set(m))
    status = "OK" if rows else "MISSING: no paired rows"
    if missing:
        status += f"; unpaired={missing}"
    return rows, status


def ranking_prediction_files(paths: Paths, variant: str, split: str) -> tuple[Path | None, Path | None]:
    if variant == "k5":
        n_file = first_existing([
            paths.n96 / f"popmatch_eval/n_{split}_predictions.jsonl",
            paths.n96 / f"popmatch_eval_valid_only/n_{split}_predictions.jsonl",
        ])
        m_file = first_existing([
            paths.m96 / f"popmatch_eval_valid_only/m_n_{split}_predictions.jsonl",
            paths.m96 / f"popmatch_eval/m_n_{split}_predictions.jsonl",
        ])
        return n_file, m_file
    n_dir = paths.phase2a / f"n_k0_{variant}_seed42"
    m_dir = paths.phase2a / f"m1_{variant}_seed42"
    n_file = first_existing([n_dir / f"n_{split}_predictions.jsonl"])
    m_file = first_existing([m_dir / f"m_n_{split}_predictions.jsonl"])
    return n_file, m_file


def ranking_key(r: dict[str, Any]) -> tuple[str, str]:
    return (str(r.get("user_id", "")), str(r.get("ground_truth_movie_id", r.get("target_movie_id", ""))))


def candidate_ids(r: dict[str, Any]) -> list[Any]:
    return r.get("candidate_movie_ids") or r.get("candidates") or []


def score_list(r: dict[str, Any]) -> list[float]:
    for key in ("scores", "label_probabilities", "candidate_p_yes"):
        v = r.get(key)
        if isinstance(v, list):
            return [float(x) for x in v]
    return []


def gt_rank(r: dict[str, Any], scores: list[float]) -> int | None:
    gi = r.get("ground_truth_index")
    if gi is None or not scores:
        return None
    gi = int(gi)
    order = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)
    for rank, idx in enumerate(order, start=1):
        if idx == gi:
            return rank
    return None


def hr(rank: int | None, k: int) -> int | None:
    return None if rank is None else int(rank <= k)


def ndcg(rank: int | None, k: int) -> float | None:
    if rank is None or rank > k:
        return 0.0 if rank is not None else None
    return 1.0 / math.log2(rank + 1)


def mrr(rank: int | None) -> float | None:
    return None if rank is None else 1.0 / rank


def ranking_delta(rows: list[dict[str, Any]]) -> dict[str, float | None]:
    metrics = {}
    for metric in ("HR@1", "NDCG@5", "MRR"):
        n_key = f"n96_{metric}"
        m_key = f"m96_{metric}"
        metrics[metric] = mean([float(r[n_key]) - float(r[m_key]) for r in rows if r.get(n_key) is not None and r.get(m_key) is not None])
    return metrics


def ranking_bootstrap(frames: dict[tuple[str, str], list[dict[str, Any]]], reps: int) -> list[dict[str, Any]]:
    out = []
    variant_offsets = {"k5": 0, "k20": 1000, "k50": 2000}
    split_offsets = {"valid": 0, "test": 10000}
    for (variant, split), rows in frames.items():
        if not rows:
            continue
        point = ranking_delta(rows)
        vals = {"HR@1": [], "NDCG@5": [], "MRR": []}
        seed = BOOTSTRAP_SEED + variant_offsets[variant] + split_offsets[split]
        for sample, _ in bootstrap_rows(rows, reps, seed):
            d = ranking_delta(sample)
            for metric, value in d.items():
                if value is not None:
                    vals[metric].append(value)
        user_count = len(group_indices(rows, "user_id"))
        for metric in ("HR@1", "NDCG@5", "MRR"):
            v = vals[metric]
            out.append({
                "variant": variant,
                "split": split,
                "metric": metric,
                "delta_definition": "N96 - M1-96",
                "point_estimate": point.get(metric),
                "bootstrap_mean": mean(v),
                "ci95_low": percentile(v, 2.5),
                "ci95_high": percentile(v, 97.5),
                "p_delta_gt_0": mean([1.0 if x > 0 else 0.0 for x in v]),
                "bootstrap_unit": "user",
                "replicates": reps,
                "sample_count": len(rows),
                "user_count": user_count,
            })
    return out


def ranking_win_loss_tie(frames: dict[tuple[str, str], list[dict[str, Any]]]) -> list[dict[str, Any]]:
    out = []
    for (variant, split), rows in frames.items():
        if not rows:
            continue
        c = Counter()
        moves = Counter()
        for r in rows:
            nr, mr = r.get("gt_rank_n96"), r.get("gt_rank_m96")
            if nr is None or mr is None:
                continue
            if nr < mr:
                c["n96_win"] += 1
            elif mr < nr:
                c["m1_win"] += 1
            else:
                c["tie"] += 1
            moves[f"M{mr}->N{nr}"] += 1
        total = sum(c.values())
        for outcome in ("n96_win", "m1_win", "tie"):
            out.append({"variant": variant, "split": split, "type": "overall", "bucket": outcome, "count": c[outcome], "fraction": c[outcome] / total if total else None, "samples": total})
        for move, count in moves.most_common(100):
            out.append({"variant": variant, "split": split, "type": "rank_movement", "bucket": move, "count": count, "fraction": count / total if total else None, "samples": total})
    return out



def candidate_protocol(paths: Paths, ctx: dict[str, Any]) -> tuple[list[dict[str, Any]], str]:
    rows = []
    cand_sets: dict[tuple[str, str], dict[tuple[str, str], dict[str, Any]]] = {}
    for variant in ("k5", "k20", "k50"):
        for split in ("valid", "test"):
            p = candidate_file(paths.root, variant, split)
            records = list_jsonl(p) if p else []
            m = {ranking_key(r): r for r in records}
            cand_sets[(variant, split)] = m
            if not p:
                rows.append({"variant": variant, "split": split, "status": "MISSING", "path": "", "reason": "candidate file not found"})
                continue
            counts = [len(candidate_ids(r)) for r in records]
            methods = Counter(json.dumps(r.get("candidate_generation", {}), ensure_ascii=False) for r in records)
            pop = ctx["popularity"]
            gt_pops = [pop.get(str(r.get("ground_truth_movie_id", r.get("target_movie_id", ""))), 0) for r in records]
            neg_pops = []
            for r in records:
                gt = str(r.get("ground_truth_movie_id", r.get("target_movie_id", "")))
                neg_pops.extend(pop.get(str(c), 0) for c in candidate_ids(r) if str(c) != gt)
            expected = ctx["next_valid" if split == "valid" else "next_test"]
            rows.append({
                "variant": variant,
                "split": split,
                "status": "OK",
                "path": rel(paths.root, p),
                "records": len(records),
                "source_records": len(expected),
                "drop_rate_vs_processed_split": 1 - len(records) / len(expected) if expected else None,
                "unique_users": len({str(r.get("user_id", "")) for r in records}),
                "candidate_count_min": min(counts) if counts else None,
                "candidate_count_max": max(counts) if counts else None,
                "candidate_count_mean": mean(counts),
                "candidate_generation_top": methods.most_common(1)[0][0] if methods else "",
                "target_popularity_mean": mean(gt_pops),
                "negative_popularity_mean": mean(neg_pops),
                "target_minus_negative_popularity_mean": mean(gt_pops) - mean(neg_pops) if gt_pops and neg_pops else None,
            })
    for split in ("valid", "test"):
        base = cand_sets.get(("k5", split), {})
        for right in ("k20", "k50"):
            rows.append(nesting_row(split, "k5", right, base, cand_sets.get((right, split), {})))
        rows.append(nesting_row(split, "k20", "k50", cand_sets.get(("k20", split), {}), cand_sets.get(("k50", split), {})))
    audit = candidate_audit_text(rows)
    return rows, audit


def candidate_file(root: Path, variant: str, split: str) -> Path | None:
    split_name = "valid" if split == "valid" else "test"
    names = {
        "k5": [f"data/candidates/movielens-1m/variants/k5_popmatch_seed42/{split_name}.jsonl"],
        "k20": [f"data/candidates/movielens-1m/variants/k20_seed42/{split_name}.jsonl", f"data/candidates/movielens-1m/variants/k20_popmatch_seed42/{split_name}.jsonl"],
        "k50": [f"data/candidates/movielens-1m/variants/k50_seed42/{split_name}.jsonl", f"data/candidates/movielens-1m/variants/k50_popmatch_seed42/{split_name}.jsonl"],
    }
    return first_existing([root / n for n in names[variant]])


def nesting_row(split: str, left: str, right: str, lset: dict[tuple[str, str], dict[str, Any]], rset: dict[tuple[str, str], dict[str, Any]]) -> dict[str, Any]:
    common = set(lset) & set(rset)
    nested = 0
    jacc = []
    for key in common:
        a = {str(x) for x in candidate_ids(lset[key])}
        b = {str(x) for x in candidate_ids(rset[key])}
        nested += int(a <= b)
        jacc.append(len(a & b) / len(a | b) if a | b else None)
    return {
        "variant": f"{left}_in_{right}",
        "split": split,
        "status": "OK" if common else "MISSING",
        "path": "protocol_nesting_check",
        "records": len(common),
        "source_records": len(lset),
        "drop_rate_vs_processed_split": None,
        "unique_users": len({k[0] for k in common}),
        "candidate_count_min": None,
        "candidate_count_max": None,
        "candidate_count_mean": None,
        "candidate_generation_top": "",
        "target_popularity_mean": None,
        "negative_popularity_mean": None,
        "target_minus_negative_popularity_mean": None,
        "nested_fraction": nested / len(common) if common else None,
        "mean_jaccard": mean([x for x in jacc if x is not None]),
    }


def candidate_audit_text(rows: list[dict[str, Any]]) -> str:
    lines = ["# Candidate Protocol Audit", "", "This is CPU-only and reads existing candidate files.", ""]
    lines.append("## Main Findings")
    lines.append("- k5 uses the explicit `k5_popmatch_seed42` path when present.")
    lines.append("- k20/k50 method is taken from each file's `candidate_generation` payload or path existence; do not infer PopMatch from directory names alone.")
    lines.append("- If nesting fractions are below 1.0, k20/k50 comparisons mix candidate size and candidate composition.")
    lines.append("- k20 gap being larger than k50 cannot be explained by candidate count alone without nesting/composition evidence.")
    lines.append("")
    for r in rows:
        if r.get("path") == "protocol_nesting_check":
            lines.append(f"- {r['split']} {r['variant']}: nested_fraction={r.get('nested_fraction')} mean_jaccard={r.get('mean_jaccard')}")
    return "\n".join(lines) + "\n"


def slice_analysis(frames: dict[tuple[str, str], list[dict[str, Any]]]) -> list[dict[str, Any]]:
    out = []
    for (variant, split), rows in frames.items():
        if not rows:
            continue
        out.extend(slice_rows(variant, split, "overall", "all", rows))
        for field, dim in (("history_length", "history_length_tercile"), ("target_popularity", "target_popularity_tercile"), ("target_minus_negative_popularity_mean", "target_vs_negative_pop_gap_tercile")):
            for bucket, part in buckets(rows, field).items():
                out.extend(slice_rows(variant, split, dim, bucket, part))
    return out


def slice_rows(variant: str, split: str, dim: str, bucket: str, rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    d = ranking_delta(rows)
    return [{
        "variant": variant,
        "split": split,
        "dimension": dim,
        "bucket": bucket,
        "samples": len(rows),
        "N96_HR@1": mean([r["n96_HR@1"] for r in rows if r.get("n96_HR@1") is not None]),
        "M1-96_HR@1": mean([r["m96_HR@1"] for r in rows if r.get("m96_HR@1") is not None]),
        "delta_N96_minus_M1-96_HR@1": d.get("HR@1"),
        "delta_N96_minus_M1-96_NDCG@5": d.get("NDCG@5"),
        "delta_N96_minus_M1-96_MRR": d.get("MRR"),
    }]


def training_curves(paths: Paths) -> list[dict[str, Any]]:
    specs = [("y96", paths.y96), ("n96", paths.n96), ("m96", paths.m96)]
    statuses = []
    for name, base in specs:
        rows = []
        state = latest_trainer_state(base)
        if state:
            for item in state.get("log_history", []):
                row = {"run": name}
                row.update(item)
                rows.append(row)
        write_csv(paths.out / f"training_curve_{name}.csv", rows)
        statuses.append(status_row(f"training_curve_{name}.csv", "OK" if rows else f"MISSING: trainer_state not found under {rel(paths.root, base)}", len(rows)))
    return statuses


def latest_trainer_state(base: Path) -> dict[str, Any] | None:
    states = list((base / "checkpoints").glob("checkpoint-*/trainer_state.json")) if (base / "checkpoints").exists() else []
    states += list(base.glob("checkpoint-*/trainer_state.json"))
    if not states:
        return None
    def step(p: Path) -> int:
        try:
            return int(p.parent.name.split("-")[-1])
        except Exception:
            return -1
    return json.loads(max(states, key=step).read_text(encoding="utf-8"))


def training_protocol_comparison(paths: Paths) -> str:
    return """# Training Protocol Comparison

This report is generated without training or inference.

- LLM effective batch: per_device_train_batch_size 1 * gradient_accumulation_steps 8 * world_size 1 = 8 examples per optimizer step.
- Y96/N96: 12000 optimizer steps -> 96000 single-task examples.
- M1-96: 24000 optimizer steps with 1:1 Y/N sequential multitask mixing -> expected 96000 Y examples and 96000 N examples if resume data skip was honored.
- The repository does not persist per-example sampler traces, so exact sample IDs for resumed partial-epoch LLM runs cannot be reconstructed from aggregate trainer_state alone.
- Internal eval/checkpoint cadence is a training-protocol artifact, not the final evidence criterion; final decisions use explicit fixed-candidate validation first and report-only test after decisions are frozen.
"""


def exposure_coverage(paths: Paths, ctx: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    specs = [
        ("Y96", "Y-K0", 96000, ctx["train_y"], "partial_epoch_random_sampler_exact_ids_not_persisted"),
        ("N96", "N-K0", 96000, ctx["train_n"], "partial_epoch_random_sampler_exact_ids_not_persisted"),
        ("M1-96-Y", "M1", 96000, ctx["train_y"], "expected_sequential_1_to_1_if_resume_skip_honored"),
        ("M1-96-N", "M1", 96000, ctx["train_n"], "expected_sequential_1_to_1_if_resume_skip_honored"),
        ("N200", "N-K0", 200000, ctx["train_n"], "first_200k_pool_no_duplicate_records_expected"),
    ]
    ratings = ctx["ratings_items"]
    metadata = ctx["metadata_items"]
    for run, family, exposure, pool, note in specs:
        subset = pool[:min(exposure, len(pool))]
        targets = {str(r.get("target_movie_id", r.get("ground_truth_movie_id", ""))) for r in subset if r.get("target_movie_id", r.get("ground_truth_movie_id", "")) != ""}
        hist_targets = set(targets)
        for r in subset:
            hist_targets.update(str(x) for x in get_history(r))
        sample_keys = [json.dumps(r, sort_keys=True, ensure_ascii=False) for r in subset]
        dup = len(sample_keys) - len(set(sample_keys))
        rows.append({
            "run": run,
            "family": family,
            "planned_exposure": exposure,
            "pool_records_available": len(pool),
            "records_counted_for_coverage": len(subset),
            "unique_sample_records_in_counted_pool": len(set(sample_keys)),
            "duplicate_sample_records_in_counted_pool": dup,
            "sampler_repetition_observability": note,
            "unique_target_items": len(targets),
            "unique_history_union_target_items": len(hist_targets),
            "ratings_item_universe": len(ratings),
            "metadata_item_universe": len(metadata),
            "target_coverage_vs_ratings_universe": len(targets & ratings) / len(ratings) if ratings else None,
            "history_union_target_coverage_vs_ratings_universe": len(hist_targets & ratings) / len(ratings) if ratings else None,
            "target_coverage_vs_metadata_universe": len(targets & metadata) / len(metadata) if metadata else None,
            "history_union_target_coverage_vs_metadata_universe": len(hist_targets & metadata) / len(metadata) if metadata else None,
        })
    return rows


def sasrec_alignment(root: Path) -> list[dict[str, Any]]:
    specs = [("S23", 11776), ("S47", 24064), ("S94", 48128), ("S188", 96256), ("S391", 200000)]
    rows = []
    for run, exposure in specs:
        for split in ("valid", "test"):
            p = find_sasrec_metric(root, run, split)
            ranking = read_ranking_metrics(p)
            rows.append({"run": run, "family": "SASRec", "exposure": exposure, "split": split, **ranking, "source": rel(root, p) if p else "MISSING"})
    return rows


def find_sasrec_metric(root: Path, run: str, split: str) -> Path | None:
    lower = run.lower()
    candidates = [
        root / f"outputs/sasrec/movielens-1m/{lower}/popmatch_eval/{split}_metrics.json",
        root / f"outputs/sasrec/movielens-1m/{lower}_{split}_metrics.json",
        root / f"outputs/phase2a/sasrec_exposure_alignment/{lower}/popmatch_eval/{split}_metrics.json",
        root / f"outputs/phase2a/sasrec_exposure_alignment/{lower}_{split}_metrics.json",
    ]
    for base in [root / "outputs/sasrec/movielens-1m", root / "outputs/phase2a/sasrec_exposure_alignment", root / "outputs/sasrec_exposure_alignment"]:
        if base.exists():
            candidates.extend(base.glob(f"*{lower}*/**/{split}*_metrics.json"))
    return first_existing(candidates)


def read_ranking_metrics(path: Path | None) -> dict[str, Any]:
    if not path or not path.exists():
        return {"samples": None, "HR@1": None, "HR@5": None, "NDCG@5": None, "MRR": None}
    data = json.loads(path.read_text(encoding="utf-8"))
    r = data.get("ranking", data)
    return {"samples": r.get("samples"), "HR@1": r.get("HR@1"), "HR@5": r.get("HR@5"), "NDCG@5": r.get("NDCG@5"), "MRR": r.get("MRR")}



def write_claim_matrix(path: Path, binary_boot: list[dict[str, Any]], rank_boot: list[dict[str, Any]], cand: list[dict[str, Any]], slices: list[dict[str, Any]]) -> None:
    lines = ["# Seed42 Claim Evidence Matrix", "", "Generated from existing artifacts only; no training or inference was launched.", ""]
    lines.append("| Question | Evidence artifact | Current answer | Caveat |")
    lines.append("| --- | --- | --- | --- |")
    lines.append("| Does M1-96 beat Y96 on Y-native binary beyond uncertainty? | binary_bootstrap_summary.csv | Use CI/p_delta_gt_0; point estimates alone are insufficient. | Seed42 only. |")
    lines.append("| Should wording be positive transfer? | binary_bootstrap_summary.csv, binary_calibration_summary.csv | Prefer `no detectable Y-side degradation`; use `positive transfer` only if CI excludes 0 and multiseed agrees. | Threshold fixed at 0.5. |")
    lines.append("| Is k5 N/M parity real? | ranking_bootstrap_summary.csv | Check k5 validation CI for N96-M1-96. | k5 has HR@5 ceiling effect. |")
    lines.append("| Is k20/k50 gap significant? | ranking_bootstrap_summary.csv | Check k20/k50 CIs and p_delta_gt_0. | Candidate protocol may differ by composition. |")
    lines.append("| Why is k20 gap larger than k50? | candidate_protocol_stats.csv, candidate_protocol_audit.md, slice_analysis.csv | Treat as candidate composition/nesting question, not monotonic candidate-size effect. | Needs candidate file audit. |")
    lines.append("| Are protocols nested/comparable? | candidate_protocol_stats.csv | Nested fraction and Jaccard answer this. | If not nested, do not attribute only to k. |")
    lines.append("| Which slices drive the gap? | slice_analysis.csv | Inspect history length, target popularity, and target-vs-negative popularity gap slices. | Slice tests are exploratory. |")
    lines.append("| Is M1-96 exposure matched? | training_protocol_comparison.md, exposure_coverage.csv | Expected matched 96k Y + 96k N under 1:1 sequential mixing. | Exact sample trace was not persisted. |")
    lines.append("| RQ2/RQ3 conclusion? | all CSV/MD outputs | Freeze as seed42 evidence; do not generalize without multiseed. | Single seed. |")
    lines.append("| Need multiseed? | multiseed_recommendation.md | Yes for near-tie or positive-transfer claims; minimal matrix there. | Stop before launching it. |")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_multiseed_recommendation(path: Path, binary_boot: list[dict[str, Any]], rank_boot: list[dict[str, Any]]) -> None:
    text = """# Multiseed Recommendation

Do not launch multiseed automatically in this round.

## Recommendation

Approve a minimal multiseed matrix only if the paper needs claims stronger than seed42 descriptive evidence:

- Y-native: Y96 vs M1-96 binary validation/test prediction-level bootstrap on at least two additional seeds.
- N-side: N96 vs M1-96 k5/k20/k50 validation first, test report-only after the validation decision is fixed.
- Optional endpoint: N200 only if the paper needs the single-task upper-bound curve; avoid M1-200 unless the central claim requires an expensive crossover check.

## Current wording boundary

- Safe from seed42 alone: M1-96 shows no obvious Y-side degradation and approaches N96 on k5 validation.
- Not safe from seed42 alone: M1-96 is globally better than specialized Y/N, or multitask positive transfer is established.
"""
    path.write_text(text, encoding="utf-8")


def write_binary_bootstrap_report(path: Path, rows: list[dict[str, Any]]) -> None:
    lines = ["# Binary Bootstrap Report", "", "Delta is M1-96 - Y96. Bootstrap unit is user. F1/Accuracy threshold is fixed at 0.5.", ""]
    if not rows:
        lines.append("MISSING: paired Y96/M1-96 binary predictions were not available.")
    else:
        lines.append("| split | metric | point | ci95_low | ci95_high | p_delta_gt_0 |")
        lines.append("| --- | --- | ---: | ---: | ---: | ---: |")
        for r in rows:
            lines.append(f"| {r['split']} | {r['metric']} | {fmt(r['point_estimate'])} | {fmt(r['ci95_low'])} | {fmt(r['ci95_high'])} | {fmt(r['p_delta_gt_0'])} |")
        lines.append("")
        lines.append("Use `no detectable Y-side degradation` unless the interval and multiseed evidence support a stronger positive-transfer claim.")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_readme(path: Path, manifest: list[dict[str, Any]], reps: int) -> None:
    ok = sum(1 for m in manifest if str(m.get("status", "")).startswith("OK"))
    missing = len(manifest) - ok
    lines = [
        "# Seed42 Deep Analysis Handoff",
        "",
        f"Generated at UTC: {datetime.now(timezone.utc).isoformat()}",
        f"Bootstrap replicates requested: {reps}",
        "",
        "No training, checkpoint creation, or model inference is performed by this script.",
        "",
        f"Artifacts OK: {ok}; missing/partial: {missing}.",
        "",
        "See `artifact_manifest.csv` for exact status and row counts.",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("status\nMISSING\n", encoding="utf-8")
        return
    fields: list[str] = []
    for r in rows:
        for k in r.keys():
            if k not in fields:
                fields.append(k)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in rows:
            w.writerow(r)


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def status_row(name: str, status: str, rows: int) -> dict[str, Any]:
    return {"artifact": name, "status": status, "rows": rows}


def ok_or_missing(rows: list[Any], reason: str) -> str:
    return "OK" if rows else f"MISSING: {reason}"


def mean(xs: list[Any]) -> float | None:
    vals = [float(x) for x in xs if x is not None]
    return sum(vals) / len(vals) if vals else None


def percentile(xs: list[float], p: float) -> float | None:
    vals = sorted(float(x) for x in xs if x is not None)
    if not vals:
        return None
    if len(vals) == 1:
        return vals[0]
    pos = (len(vals) - 1) * p / 100
    lo = math.floor(pos)
    hi = math.ceil(pos)
    if lo == hi:
        return vals[int(pos)]
    return vals[lo] * (hi - pos) + vals[hi] * (pos - lo)


def fmt(v: Any) -> str:
    return "MISSING" if v is None else f"{float(v):.10f}"


def rel(root: Path, path: Path | None) -> str:
    if path is None:
        return "MISSING"
    try:
        return str(path.relative_to(root)).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


if __name__ == "__main__":
    main()
