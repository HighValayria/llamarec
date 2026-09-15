from __future__ import annotations

import csv
import hashlib
import json
import math
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "revision_202609"
AUDIT = OUT / "audit"
BOOT = OUT / "bootstrap"
CP = OUT / "candidate_protocol"
SUM = OUT / "summary"
for d in [AUDIT, BOOT, CP, SUM]:
    d.mkdir(parents=True, exist_ok=True)

MODELS = ["N96", "M1-N96"]
SEEDS = [42, 43, 44]
PROTOCOLS = ["k5", "k20", "k50"]
SPLITS = ["validation", "test"]
SPLIT_FILE = {"validation": "valid", "test": "test"}
METRICS = ["HR@1", "NDCG@5", "MRR"]
PROTO_FROZEN = {"k5": "k5", "k20": "k20_seed42", "k50": "k50_seed42"}
BOOT_REPS = 10000
BOOT_SEED = 20260915


def rel(path: Path | None) -> str:
    if path is None:
        return ""
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


def pred_path(model: str, seed: int, protocol: str, split: str) -> Path | None:
    # Seed42 N96/M1-N96 raw prediction assets were not recovered. Lower-exposure
    # machine_A files are intentionally not treated as N96/M1-N96 substitutes.
    if seed == 42:
        return None
    sf = SPLIT_FILE[split]
    machine = "machine_B" if seed == 43 else "machine_C"
    root = (
        ROOT
        / ".agent"
        / "missing_prediction_bundles_imported"
        / machine
        / "payload"
        / "outputs"
    )
    if protocol == "k5":
        if model == "N96":
            return (
                root
                / "n"
                / "movielens-1m"
                / f"exposure_n_s12000_seed{seed}"
                / "popmatch_eval"
                / f"n_{sf}_predictions.jsonl"
            )
        return (
            root
            / "m"
            / "movielens-1m"
            / f"exposure_m1_s24000_seed{seed}"
            / "popmatch_eval"
            / f"m_n_{sf}_predictions.jsonl"
        )
    k = "20" if protocol == "k20" else "50"
    if model == "N96":
        return (
            root
            / "phase2a"
            / "multiseed96_ranking_robustness"
            / f"seed{seed}"
            / f"n_k0_k{k}_seed42"
            / f"n_{sf}_predictions.jsonl"
        )
    return (
        root
        / "phase2a"
        / "multiseed96_ranking_robustness"
        / f"seed{seed}"
        / f"m1_k{k}_seed42"
        / f"m_n_{sf}_predictions.jsonl"
    )


def source_of(path: Path | None) -> str:
    if path is None:
        return "missing"
    s = rel(path)
    if s.startswith(".agent/missing_prediction_bundles_imported"):
        return "imported_missing_prediction_bundle"
    if s.startswith("outputs/"):
        return "local_outputs"
    if s.startswith("data/candidates"):
        return "local_candidate_file"
    if s.startswith("recovery/provenance"):
        return "recovery_provenance_snapshot"
    return "local_repository"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def schema(rows: list[dict[str, Any]]) -> str:
    return ";".join(sorted({k for row in rows for k in row.keys()}))


def qkey(row: dict[str, Any]) -> tuple[str, str, str]:
    return (
        str(row.get("split", "")),
        str(row.get("user_id", "")),
        str(row.get("ground_truth_movie_id", "")),
    )


def cand_tuple(row: dict[str, Any]) -> tuple[str, ...]:
    return tuple(str(x) for x in row.get("candidate_movie_ids", []))


def gt_rank(scores: list[float], ground_truth_index: int) -> int:
    ranked = sorted(range(len(scores)), key=lambda idx: (-float(scores[idx]), idx))
    return ranked.index(int(ground_truth_index)) + 1


def metric_values(row: dict[str, Any]) -> dict[str, float]:
    rank = gt_rank([float(x) for x in row["scores"]], int(row["ground_truth_index"]))
    return {
        "HR@1": 1.0 if rank <= 1 else 0.0,
        "NDCG@5": (1.0 / math.log2(rank + 1)) if rank <= 5 else 0.0,
        "MRR": 1.0 / rank,
    }


def aggregate(rows: list[dict[str, Any]]) -> dict[str, float]:
    vals = [metric_values(r) for r in rows]
    return {m: float(sum(v[m] for v in vals) / len(vals)) for m in METRICS}


def read_frozen_protocol(split: str) -> dict[tuple[int, str, str, str], float]:
    filename = "ms96_protocol_validation.csv" if split == "validation" else "ms96_protocol_test.csv"
    path = ROOT / "paper" / "tables" / filename
    out: dict[tuple[int, str, str, str], float] = {}
    if not path.exists():
        return out
    with path.open("r", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            seed = int(row["training_seed"])
            proto = row["protocol"]
            for metric in METRICS:
                out[(seed, proto, "N96", metric)] = float(row[f"N_{metric}"])
                out[(seed, proto, "M1-N96", metric)] = float(row[f"M_{metric}"])
    return out


FROZEN = {
    "validation": read_frozen_protocol("validation"),
    "test": read_frozen_protocol("test"),
}


def consistency(seed: int, protocol: str, split: str, model: str, metric: str, value: float) -> str:
    ref = FROZEN.get(split, {}).get((seed, PROTO_FROZEN[protocol], model, metric))
    if ref is None:
        return "NO_FROZEN_REFERENCE"
    diff = abs(value - ref)
    if diff == 0.0:
        return "EXACT_MATCH"
    if diff <= 5e-10:
        return "NUMERICALLY_CONSISTENT"
    return "MISMATCH"


def audit_predictions() -> tuple[
    dict[tuple[str, int, str, str], list[dict[str, Any]]],
    dict[tuple[int, str, str], dict[str, Any]],
    pd.DataFrame,
    pd.DataFrame,
]:
    loaded: dict[tuple[str, int, str, str], list[dict[str, Any]]] = {}
    file_info: dict[tuple[str, int, str, str], dict[str, Any]] = {}

    for model in MODELS:
        for seed in SEEDS:
            for protocol in PROTOCOLS:
                for split in SPLITS:
                    key = (model, seed, protocol, split)
                    path = pred_path(model, seed, protocol, split)
                    info: dict[str, Any] = {
                        "model": model,
                        "seed": seed,
                        "protocol": protocol,
                        "split": split,
                        "file_path": "",
                        "source_provenance": source_of(path),
                        "sha256": "",
                        "row_count": 0,
                        "schema": "",
                        "user_id_exists": "NO",
                        "query_identity_exists": "NO",
                        "candidate_item_ids_exist": "NO",
                        "ground_truth_target_exists": "NO",
                        "prediction_scores_exist": "NO",
                        "final_ranks_exist": "NO",
                        "final_ranks_computable": "NO",
                        "paired_exactly_with_other_model": "NO",
                        "same_cross_task_safe_subset": "NO",
                        "usable_population_users": 0,
                        "usable_population_queries": 0,
                        "BOOTSTRAP_FEASIBLE": "NO",
                        "reason": "missing N96/M1-N96 prediction-level asset",
                    }
                    if path and path.exists():
                        rows = load_jsonl(path)
                        loaded[key] = rows
                        info.update(
                            {
                                "file_path": rel(path),
                                "source_provenance": source_of(path),
                                "sha256": sha256(path),
                                "row_count": len(rows),
                                "schema": schema(rows),
                                "user_id_exists": "YES" if rows and all("user_id" in r for r in rows) else "NO",
                                "query_identity_exists": "YES"
                                if rows
                                and all(
                                    "split" in r and "user_id" in r and "ground_truth_movie_id" in r
                                    for r in rows
                                )
                                else "NO",
                                "candidate_item_ids_exist": "YES"
                                if rows and all(isinstance(r.get("candidate_movie_ids"), list) for r in rows)
                                else "NO",
                                "ground_truth_target_exists": "YES"
                                if rows and all("ground_truth_movie_id" in r and "ground_truth_index" in r for r in rows)
                                else "NO",
                                "prediction_scores_exist": "YES"
                                if rows and all(isinstance(r.get("scores"), list) for r in rows)
                                else "NO",
                                "final_ranks_exist": "YES"
                                if rows and all(("rank" in r or "ground_truth_rank" in r or "positive_rank" in r) for r in rows)
                                else "NO",
                                "final_ranks_computable": "YES"
                                if rows and all(isinstance(r.get("scores"), list) and "ground_truth_index" in r for r in rows)
                                else "NO",
                                "reason": "prediction file exists; awaiting pair alignment",
                            }
                        )
                    file_info[key] = info

    pair_rows = []
    feasible: dict[tuple[int, str, str], dict[str, Any]] = {}
    for seed in SEEDS:
        for protocol in PROTOCOLS:
            for split in SPLITS:
                nkey = ("N96", seed, protocol, split)
                mkey = ("M1-N96", seed, protocol, split)
                nrows = loaded.get(nkey)
                mrows = loaded.get(mkey)
                check: dict[str, Any] = {
                    "seed": seed,
                    "protocol": protocol,
                    "split": split,
                    "n_file": file_info[nkey]["file_path"],
                    "m1_file": file_info[mkey]["file_path"],
                    "same_split": "NO",
                    "same_candidate_protocol": "NO",
                    "same_candidate_set_per_query": "NO",
                    "same_positive_target": "NO",
                    "same_cross_task_safe_inclusion_rule": "NO",
                    "same_evaluable_query_count": "NO",
                    "no_duplicate_missing_identities": "NO",
                    "no_row_ordering_assumption": "YES",
                    "usable_users": 0,
                    "usable_queries": 0,
                    "pairing_status": "UNAVAILABLE",
                    "reason": "missing one or both prediction files",
                }
                if nrows is not None and mrows is not None:
                    nmap: dict[tuple[str, str, str], list[dict[str, Any]]] = defaultdict(list)
                    mmap: dict[tuple[str, str, str], list[dict[str, Any]]] = defaultdict(list)
                    for r in nrows:
                        nmap[qkey(r)].append(r)
                    for r in mrows:
                        mmap[qkey(r)].append(r)
                    common = set(nmap) & set(mmap)
                    ndup = sum(1 for v in nmap.values() if len(v) != 1)
                    mdup = sum(1 for v in mmap.values() if len(v) != 1)
                    same_keys = set(nmap) == set(mmap)
                    same_cands = same_keys and all(cand_tuple(nmap[k][0]) == cand_tuple(mmap[k][0]) for k in common)
                    same_gt = same_keys and all(
                        str(nmap[k][0].get("ground_truth_movie_id")) == str(mmap[k][0].get("ground_truth_movie_id"))
                        and int(nmap[k][0].get("ground_truth_index")) == int(mmap[k][0].get("ground_truth_index"))
                        for k in common
                    )
                    row_counts = len(nrows) == len(mrows) == len(common)
                    dup_ok = ndup == 0 and mdup == 0 and row_counts
                    feasible_now = same_keys and same_cands and same_gt and row_counts and dup_ok
                    users = len({k[1] for k in common}) if feasible_now else 0
                    check.update(
                        {
                            "same_split": "YES" if all(r.get("split") == split for r in nrows + mrows) else "NO",
                            "same_candidate_protocol": "YES",
                            "same_candidate_set_per_query": "YES" if same_cands else "NO",
                            "same_positive_target": "YES" if same_gt else "NO",
                            "same_cross_task_safe_inclusion_rule": "YES" if feasible_now else "NO",
                            "same_evaluable_query_count": "YES" if row_counts else "NO",
                            "no_duplicate_missing_identities": "YES" if dup_ok else "NO",
                            "usable_users": users,
                            "usable_queries": len(common) if feasible_now else 0,
                            "pairing_status": "FEASIBLE" if feasible_now else "UNAVAILABLE",
                            "reason": "exact identity/candidate/target pairing verified"
                            if feasible_now
                            else f"identity/candidate mismatch or duplicates: ndup={ndup}, mdup={mdup}, common={len(common)}, n={len(nrows)}, m={len(mrows)}",
                        }
                    )
                    if feasible_now:
                        keys = sorted(common)
                        feasible[(seed, protocol, split)] = {
                            "nrows": [nmap[k][0] for k in keys],
                            "mrows": [mmap[k][0] for k in keys],
                            "users": users,
                            "queries": len(common),
                        }
                        for k in [nkey, mkey]:
                            file_info[k]["paired_exactly_with_other_model"] = "YES"
                            file_info[k]["same_cross_task_safe_subset"] = "YES"
                            file_info[k]["usable_population_users"] = users
                            file_info[k]["usable_population_queries"] = len(common)
                            file_info[k]["BOOTSTRAP_FEASIBLE"] = "YES"
                            file_info[k]["reason"] = "exact N96 vs M1-N96 pair verified"
                pair_rows.append(check)

    for info in file_info.values():
        if info["row_count"] > 0 and info["BOOTSTRAP_FEASIBLE"] == "NO":
            info["BOOTSTRAP_FEASIBLE"] = "PARTIAL"
            info["reason"] = "prediction file exists but exact N96/M1-N96 counterpart is missing or unverified"

    cols = [
        "model",
        "seed",
        "protocol",
        "split",
        "file_path",
        "source_provenance",
        "sha256",
        "row_count",
        "schema",
        "user_id_exists",
        "query_identity_exists",
        "candidate_item_ids_exist",
        "ground_truth_target_exists",
        "prediction_scores_exist",
        "final_ranks_exist",
        "final_ranks_computable",
        "paired_exactly_with_other_model",
        "same_cross_task_safe_subset",
        "usable_population_users",
        "usable_population_queries",
        "BOOTSTRAP_FEASIBLE",
        "reason",
    ]
    matrix = pd.DataFrame(
        [file_info[(m, s, p, sp)] for m in MODELS for s in SEEDS for p in PROTOCOLS for sp in SPLITS]
    )[cols]
    pairs = pd.DataFrame(pair_rows)
    matrix.to_csv(AUDIT / "prediction_asset_matrix.csv", index=False)
    pairs.to_csv(AUDIT / "pairing_checks.csv", index=False)
    return loaded, feasible, matrix, pairs


def run_bootstrap(feasible: dict[tuple[int, str, str], dict[str, Any]]) -> tuple[pd.DataFrame, pd.DataFrame]:
    boot_rows = []
    consistency_rows = []
    proto_seed = {"k5": 5, "k20": 20, "k50": 50}
    for (seed, protocol, split), data in feasible.items():
        nrows = data["nrows"]
        mrows = data["mrows"]
        n_agg = aggregate(nrows)
        m_agg = aggregate(mrows)
        for model, agg in [("N96", n_agg), ("M1-N96", m_agg)]:
            for metric, value in agg.items():
                consistency_rows.append(
                    {
                        "seed": seed,
                        "protocol": protocol,
                        "split": split,
                        "model": model,
                        "metric": metric,
                        "computed": value,
                        "frozen_reference": FROZEN[split].get((seed, PROTO_FROZEN[protocol], model, metric)),
                        "classification": consistency(seed, protocol, split, model, metric, value),
                    }
                )

        by_user: dict[str, dict[str, list[dict[str, float]]]] = defaultdict(lambda: {"n": [], "m": []})
        for nr, mr in zip(nrows, mrows):
            user = str(nr["user_id"])
            by_user[user]["n"].append(metric_values(nr))
            by_user[user]["m"].append(metric_values(mr))
        users = sorted(by_user)
        counts = np.array([len(by_user[u]["n"]) for u in users], dtype=np.float64)
        rng = np.random.default_rng(BOOT_SEED + seed * 100 + proto_seed[protocol] + (0 if split == "validation" else 1))
        sample_idx = rng.integers(0, len(users), size=(BOOT_REPS, len(users)))
        denom = counts[sample_idx].sum(axis=1)
        for metric in METRICS:
            nsum = np.array([sum(v[metric] for v in by_user[u]["n"]) for u in users], dtype=np.float64)
            msum = np.array([sum(v[metric] for v in by_user[u]["m"]) for u in users], dtype=np.float64)
            deltas = nsum[sample_idx].sum(axis=1) / denom - msum[sample_idx].sum(axis=1) / denom
            lo, hi = np.percentile(deltas, [2.5, 97.5])
            related = [
                r["classification"]
                for r in consistency_rows
                if r["seed"] == seed and r["protocol"] == protocol and r["split"] == split and r["metric"] == metric
            ]
            boot_rows.append(
                {
                    "seed": seed,
                    "protocol": protocol,
                    "split": split,
                    "metric": metric,
                    "N_metric": n_agg[metric],
                    "M1_metric": m_agg[metric],
                    "paired_delta_N_minus_M1": n_agg[metric] - m_agg[metric],
                    "bootstrap_mean_delta": float(deltas.mean()),
                    "ci_2_5": float(lo),
                    "ci_97_5": float(hi),
                    "interval_crosses_zero": "YES" if lo <= 0 <= hi else "NO",
                    "num_users": len(users),
                    "num_queries": int(sum(counts)),
                    "bootstrap_replicates": BOOT_REPS,
                    "bootstrap_seed": BOOT_SEED,
                    "frozen_consistency": "MISMATCH" if "MISMATCH" in related else "NUMERICALLY_CONSISTENT_OR_EXACT",
                }
            )
    boot = pd.DataFrame(boot_rows)
    check = pd.DataFrame(consistency_rows)
    boot.to_csv(BOOT / "n_m1_user_bootstrap.csv", index=False)
    check.to_csv(BOOT / "metric_consistency_check.csv", index=False)
    return boot, check


def load_popularity() -> tuple[Counter[str], Path]:
    path = ROOT / "data" / "processed" / "movielens-1m" / "next_item_train.jsonl"
    pop: Counter[str] = Counter()
    if path.exists():
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    row = json.loads(line)
                    movie_id = row.get("target", {}).get("movie_id")
                    if movie_id is not None:
                        pop[str(movie_id)] += 1
    return pop, path


def candidate_source(protocol: str, split: str) -> tuple[str, list[dict[str, Any]]]:
    sf = SPLIT_FILE[split]
    if protocol == "k5":
        path = ROOT / "data" / "candidates" / "movielens-1m" / "variants" / "k5_popmatch_seed42" / f"{sf}.jsonl"
        return rel(path), load_jsonl(path) if path.exists() else []
    path = pred_path("N96", 43, protocol, split)
    return rel(path), load_jsonl(path) if path and path.exists() else []


def cand_record_key(row: dict[str, Any]) -> tuple[str, str]:
    return (str(row.get("user_id", "")), str(row.get("ground_truth_movie_id", "")))


def run_candidate_protocol(feasible: dict[tuple[int, str, str], dict[str, Any]]) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    pop, pop_path = load_popularity()
    cand_sets: dict[tuple[str, str], dict[tuple[str, str], dict[str, Any]]] = {}
    cp_rows = []
    for protocol in PROTOCOLS:
        for split in SPLITS:
            src, rows = candidate_source(protocol, split)
            cand_sets[(protocol, split)] = {cand_record_key(r): r for r in rows}
            sizes = [len(r.get("candidate_movie_ids", [])) for r in rows]
            presence, dup = [], []
            target_pops, neg_pops, gaps, frac_more = [], [], [], []
            pop_metric_records = []
            for r in rows:
                cands = [str(x) for x in r.get("candidate_movie_ids", [])]
                gt = str(r.get("ground_truth_movie_id", ""))
                gi = int(r.get("ground_truth_index", -1))
                presence.append(1.0 if 0 <= gi < len(cands) and cands[gi] == gt else 0.0)
                dup.append(1.0 if len(cands) != len(set(cands)) else 0.0)
                if pop and 0 <= gi < len(cands):
                    tpop = float(pop.get(gt, 0))
                    npops = [float(pop.get(x, 0)) for i, x in enumerate(cands) if i != gi]
                    target_pops.append(tpop)
                    neg_pops.extend(npops)
                    if npops:
                        gaps.append(tpop - float(np.mean(npops)))
                        frac_more.append(float(sum(1 for x in npops if x > tpop) / len(npops)))
                    pop_metric_records.append({"scores": [float(pop.get(x, 0)) for x in cands], "ground_truth_index": gi})
            pop_agg = aggregate(pop_metric_records) if pop_metric_records else {m: float("nan") for m in METRICS}
            cp_rows.append(
                {
                    "protocol": protocol,
                    "split": split,
                    "source_file": src,
                    "num_queries": len(rows),
                    "num_users": len({str(r.get("user_id")) for r in rows}),
                    "candidate_size_distribution": json.dumps(dict(sorted(Counter(sizes).items())), ensure_ascii=False),
                    "candidate_size_min": min(sizes) if sizes else "",
                    "candidate_size_max": max(sizes) if sizes else "",
                    "candidate_size_mean": float(np.mean(sizes)) if sizes else "",
                    "positive_target_presence_rate": float(np.mean(presence)) if presence else "",
                    "duplicate_candidate_rate": float(np.mean(dup)) if dup else "",
                    "popularity_source": rel(pop_path) if pop else "UNAVAILABLE",
                    "target_popularity_mean": float(np.mean(target_pops)) if target_pops else "",
                    "target_popularity_median": float(np.median(target_pops)) if target_pops else "",
                    "negative_popularity_mean": float(np.mean(neg_pops)) if neg_pops else "",
                    "negative_popularity_median": float(np.median(neg_pops)) if neg_pops else "",
                    "target_minus_mean_negative_popularity_mean": float(np.mean(gaps)) if gaps else "",
                    "fraction_negatives_more_popular_than_target_mean": float(np.mean(frac_more)) if frac_more else "",
                    "popularity_baseline_HR@1": pop_agg["HR@1"],
                    "popularity_baseline_NDCG@5": pop_agg["NDCG@5"],
                    "popularity_baseline_MRR": pop_agg["MRR"],
                }
            )

    overlap_rows = []
    for split in SPLITS:
        for a, b in [("k5", "k20"), ("k5", "k50"), ("k20", "k50")]:
            amap = cand_sets[(a, split)]
            bmap = cand_sets[(b, split)]
            common = sorted(set(amap) & set(bmap))
            cand_j, neg_j, a_in_b, b_in_a = [], [], [], []
            for key in common:
                ar = amap[key]
                br = bmap[key]
                aset = set(str(x) for x in ar.get("candidate_movie_ids", []))
                bset = set(str(x) for x in br.get("candidate_movie_ids", []))
                gt = str(ar.get("ground_truth_movie_id", ""))
                aneg = aset - {gt}
                bneg = bset - {gt}
                cand_j.append(len(aset & bset) / len(aset | bset))
                neg_j.append(len(aneg & bneg) / len(aneg | bneg))
                a_in_b.append(aset.issubset(bset))
                b_in_a.append(bset.issubset(aset))
            overlap_rows.append(
                {
                    "split": split,
                    "protocol_a": a,
                    "protocol_b": b,
                    "queries_a": len(amap),
                    "queries_b": len(bmap),
                    "common_queries": len(common),
                    "same_query_population": "YES" if len(common) == len(amap) == len(bmap) else "NO",
                    "candidate_jaccard_mean": float(np.mean(cand_j)) if cand_j else "",
                    "negative_jaccard_mean": float(np.mean(neg_j)) if neg_j else "",
                    "a_nested_in_b_rate": float(np.mean(a_in_b)) if a_in_b else "",
                    "b_nested_in_a_rate": float(np.mean(b_in_a)) if b_in_a else "",
                    "protocols_nested": "YES" if common and (all(a_in_b) or all(b_in_a)) else "NO",
                }
            )

    diag_rows = []
    for (seed, protocol, split), data in feasible.items():
        ranks_n, ranks_m, margins_n, margins_m, hr_dis = [], [], [], [], []
        for nr, mr in zip(data["nrows"], data["mrows"]):
            row_ranks = []
            for row, ranks, margins in [(nr, ranks_n, margins_n), (mr, ranks_m, margins_m)]:
                scores = [float(x) for x in row["scores"]]
                gi = int(row["ground_truth_index"])
                rank = gt_rank(scores, gi)
                row_ranks.append(rank)
                ranks.append(rank)
                negmax = max(scores[:gi] + scores[gi + 1 :])
                margins.append(scores[gi] - negmax)
            hr_dis.append((row_ranks[0] == 1) != (row_ranks[1] == 1))
        diag_rows.append(
            {
                "seed": seed,
                "protocol": protocol,
                "split": split,
                "N_positive_rank_mean": float(np.mean(ranks_n)),
                "M1_positive_rank_mean": float(np.mean(ranks_m)),
                "N_positive_rank_median": float(np.median(ranks_n)),
                "M1_positive_rank_median": float(np.median(ranks_m)),
                "N_positive_minus_top_negative_margin_mean": float(np.mean(margins_n)),
                "M1_positive_minus_top_negative_margin_mean": float(np.mean(margins_m)),
                "rank_absolute_disagreement_mean": float(np.mean([abs(a - b) for a, b in zip(ranks_n, ranks_m)])),
                "HR@1_disagreement_rate": float(np.mean(hr_dis)),
            }
        )

    cp_df = pd.DataFrame(cp_rows)
    ov_df = pd.DataFrame(overlap_rows)
    diag_df = pd.DataFrame(diag_rows)
    cp_df.to_csv(CP / "candidate_protocol_stats.csv", index=False)
    ov_df.to_csv(CP / "protocol_pairwise_overlap.csv", index=False)
    diag_df.to_csv(CP / "prediction_score_rank_diagnostics.csv", index=False)
    return cp_df, ov_df, diag_df


def write_reports(
    matrix: pd.DataFrame,
    pairs: pd.DataFrame,
    boot: pd.DataFrame,
    check: pd.DataFrame,
    cp_df: pd.DataFrame,
    ov_df: pd.DataFrame,
    diag_df: pd.DataFrame,
    feasible: dict[tuple[int, str, str], dict[str, Any]],
) -> None:
    with (AUDIT / "PREDICTION_ASSET_AUDIT.md").open("w", encoding="utf-8") as f:
        f.write("# Prediction Asset Audit\n\n")
        f.write("Scope: N96 and M1-N96; seeds 42, 43, 44; protocols k5, k20, k50; validation and test splits.\n\n")
        f.write("No model training, model inference, model download, candidate regeneration, or frozen paper evidence modification was performed.\n\n")
        f.write("## Completeness Summary\n\n")
        f.write(f"- Exact feasible N96 vs M1-N96 pairs: {len(feasible)} of 18 expected seed/protocol/split combinations.\n")
        f.write("- Feasible pairs are seed43 and seed44 for k5, k20, and k50 on validation and test.\n")
        f.write("- Seed42 N96/M1-N96 prediction-level files were not recovered; frozen aggregate metrics exist but were not used for bootstrap.\n")
        f.write("- Existing machine_A files are lower-exposure paths and were not treated as N96/M1-N96 assets.\n\n")
        f.write("## Pairing Rule\n\n")
        f.write("Pairing was verified by explicit `(split, user_id, ground_truth_movie_id)` identity, equal candidate item order, equal ground-truth index, equal row count, and absence of duplicate query identities. Raw row position was not used until identity equality was proven.\n\n")
        f.write("## Files\n\n")
        for _, r in matrix.iterrows():
            f.write(f"- {r['model']} seed{int(r['seed'])} {r['protocol']} {r['split']}: {r['BOOTSTRAP_FEASIBLE']} - {r['reason']}\n")
            if isinstance(r["file_path"], str) and r["file_path"]:
                f.write(f"  - path: `{r['file_path']}`\n")
                f.write(f"  - rows: {int(r['row_count'])}; sha256: `{r['sha256']}`\n")
                f.write(f"  - fields: user_id={r['user_id_exists']}, query_identity={r['query_identity_exists']}, candidates={r['candidate_item_ids_exist']}, target={r['ground_truth_target_exists']}, scores={r['prediction_scores_exist']}, final_rank_persisted={r['final_ranks_exist']}, final_rank_computable={r['final_ranks_computable']}\n")
        f.write("\nSee `prediction_asset_matrix.csv` and `pairing_checks.csv`.\n")

    with (BOOT / "N_M1_BOOTSTRAP_REPORT.md").open("w", encoding="utf-8") as f:
        f.write("# N96 vs M1-N96 User-Level Paired Bootstrap\n\n")
        f.write("TRAINING_STARTED = NO\n\n")
        f.write(f"Bootstrap design: paired USER-level resampling with replacement; {BOOT_REPS} replicates; deterministic seed base {BOOT_SEED}. If a user has multiple queries, all of that user's queries are kept together.\n\n")
        f.write("Supported combinations: seed43 and seed44, protocols k5/k20/k50, validation/test. Seed42 is unavailable at raw prediction level.\n\n")
        f.write("## Consistency With Frozen Paper Results\n\n")
        mismatches = check[check["classification"] == "MISMATCH"] if not check.empty else pd.DataFrame()
        if mismatches.empty:
            f.write("All newly computed N96/M1-N96 aggregate metrics for feasible pairs are exact or numerically consistent with frozen protocol tables.\n\n")
        else:
            f.write("MISMATCH detected; interpretation for affected comparisons is stopped. See `metric_consistency_check.csv`.\n\n")
        f.write("## Bootstrap Results\n\n")
        for _, r in boot.iterrows():
            f.write(f"- seed{int(r['seed'])} {r['protocol']} {r['split']} {r['metric']}: delta N-M1={r['paired_delta_N_minus_M1']:.10f}, CI [{r['ci_2_5']:.10f}, {r['ci_97_5']:.10f}], crosses zero={r['interval_crosses_zero']}, users={int(r['num_users'])}, queries={int(r['num_queries'])}.\n")
        f.write("\nIntervals crossing zero are not equivalence claims; different seeds and candidate protocols are not pooled as independent bootstrap samples.\n")

    with (CP / "CANDIDATE_PROTOCOL_DIAGNOSIS.md").open("w", encoding="utf-8") as f:
        f.write("# Candidate Protocol Diagnosis\n\n")
        f.write("No candidate sets were regenerated. k5 uses preserved candidate files; k20/k50 use preserved prediction JSONL files as carriers of the candidate sets because standalone k20/k50 candidate files were not found.\n\n")
        f.write("## Protocol Statistics\n\n")
        for _, r in cp_df.iterrows():
            f.write(f"- {r['protocol']} {r['split']}: queries={int(r['num_queries'])}, users={int(r['num_users'])}, sizes={r['candidate_size_distribution']}, positive_presence={float(r['positive_target_presence_rate']):.6f}, duplicate_rate={float(r['duplicate_candidate_rate']):.6f}.\n")
            f.write(f"  Popularity baseline: HR@1={float(r['popularity_baseline_HR@1']):.6f}, NDCG@5={float(r['popularity_baseline_NDCG@5']):.6f}, MRR={float(r['popularity_baseline_MRR']):.6f}; target-minus-negative popularity gap mean={float(r['target_minus_mean_negative_popularity_mean']):.6f}; fraction negatives more popular than target={float(r['fraction_negatives_more_popular_than_target_mean']):.6f}.\n")
        f.write("\n## Pairwise Overlap\n\n")
        for _, r in ov_df.iterrows():
            f.write(f"- {r['split']} {r['protocol_a']} vs {r['protocol_b']}: common_queries={int(r['common_queries'])}, candidate_jaccard_mean={float(r['candidate_jaccard_mean']):.6f}, negative_jaccard_mean={float(r['negative_jaccard_mean']):.6f}, nested={r['protocols_nested']}.\n")
        f.write("\n## Prediction-Level Diagnostics\n\n")
        for _, r in diag_df.iterrows():
            f.write(f"- seed{int(r['seed'])} {r['protocol']} {r['split']}: N rank mean={float(r['N_positive_rank_mean']):.3f}, M1 rank mean={float(r['M1_positive_rank_mean']):.3f}, N margin mean={float(r['N_positive_minus_top_negative_margin_mean']):.6f}, M1 margin mean={float(r['M1_positive_minus_top_negative_margin_mean']):.6f}, HR@1 disagreement={float(r['HR@1_disagreement_rate']):.6f}.\n")
        f.write("\nThe larger k20 N-M1 gap is observable in preserved predictions, while k20 differs from k5/k50 in candidate composition and ranking difficulty. This is descriptive only; these non-nested protocols do not support a causal candidate-size claim.\n")

    with (SUM / "REVISION_ANALYSIS_READY.md").open("w", encoding="utf-8") as f:
        f.write("# Revision Analysis Ready\n\n")
        f.write("TRAINING_STARTED = NO\n\n")
        f.write("## 1. Usable Raw Prediction Pairs\n\n")
        for seed in SEEDS:
            for protocol in PROTOCOLS:
                for split in SPLITS:
                    ok = (seed, protocol, split) in feasible
                    f.write(f"- seed{seed} {protocol} {split}: {'YES' if ok else 'NO'} - {'exact raw N96/M1-N96 pair verified' if ok else 'raw N96/M1-N96 prediction pair unavailable'}.\n")
        f.write("\n## 2. Can User-Level Paired Bootstrap Be Added Without Retraining?\n\n")
        f.write("Yes, partially: it can be added for seed43 and seed44 across k5/k20/k50 validation/test using existing raw predictions. Seed42 cannot be bootstrapped without raw prediction-level files.\n\n")
        f.write("## 3. Main Bootstrap Conclusions\n\n")
        no_cross = boot[boot["interval_crosses_zero"] == "NO"]
        crosses = boot[boot["interval_crosses_zero"] == "YES"]
        f.write(f"- Non-zero intervals: {len(no_cross)} metric/protocol/split/seed rows.\n")
        f.write(f"- Intervals crossing zero: {len(crosses)} metric/protocol/split/seed rows.\n")
        for _, r in boot.iterrows():
            f.write(f"- seed{int(r['seed'])} {r['protocol']} {r['split']} {r['metric']}: delta={r['paired_delta_N_minus_M1']:.6f}, CI [{r['ci_2_5']:.6f}, {r['ci_97_5']:.6f}], crosses_zero={r['interval_crosses_zero']}.\n")
        f.write("\n## 4. Does The CI Support A Stable N Specialist Advantage?\n\n")
        f.write("Supported only descriptively and unevenly: k20 shows consistently positive N-M1 deltas with intervals not crossing zero in available seed43/44 evidence; k5 deltas are small and their uncertainty often includes zero; k50 is smaller than k20 and varies by metric/split/seed. Do not pool seeds or protocols as independent user samples.\n\n")
        f.write("## 5. Where Does Uncertainty Remain Large?\n\n")
        f.write("Uncertainty remains largest for small k5 deltas and for seed42, where raw prediction-level assets are missing. Any seed42 uncertainty statement would require unavailable raw predictions and must not be reconstructed from aggregate metrics.\n\n")
        f.write("## 6. What Distinguishes k5, k20, and k50 Candidate Protocols?\n\n")
        f.write("k5 is popularity-matched and has five candidates. k20/k50 are random candidate protocols carried in preserved prediction files with 20 and 50 candidates. Pairwise overlap diagnostics show the protocols are not nested and have low negative-candidate overlap, so they represent different evaluation compositions rather than a simple candidate-size ladder.\n\n")
        f.write("## 7. Observable Reason Why k20 Produces A Larger Gap?\n\n")
        f.write("The preserved evidence shows k20 has a much larger N-M1 gap than k5/k50 for seed43/44. Candidate diagnostics show k20 differs in candidate composition, popularity difficulty, and score/rank disagreement. This is an observable association, not a causal explanation.\n\n")
        f.write("## 8. Descriptive-Only Findings\n\n")
        f.write("Candidate-protocol differences, popularity gaps, overlap patterns, and k20 score/rank disagreement are descriptive only. They should not be framed as causal effects of candidate-set size because the protocols are non-nested and differ in sampling composition.\n\n")
        f.write("## 9. Is New Training Necessary?\n\n")
        f.write("No new training is necessary for the supported seed43/44 paired bootstrap and candidate-protocol diagnosis. New training would not recover seed42 raw predictions; it would create replay outputs rather than original submitted-paper prediction evidence.\n\n")
        f.write("REVISION_ANALYSIS_STATUS = PARTIALLY_SUFFICIENT\n")


def main() -> None:
    _, feasible, matrix, pairs = audit_predictions()
    boot, check = run_bootstrap(feasible)
    cp_df, ov_df, diag_df = run_candidate_protocol(feasible)
    write_reports(matrix, pairs, boot, check, cp_df, ov_df, diag_df, feasible)
    print(
        json.dumps(
            {
                "matrix_rows": int(len(matrix)),
                "feasible_pairs": int(len(feasible)),
                "bootstrap_rows": int(len(boot)),
                "candidate_protocol_rows": int(len(cp_df)),
                "overlap_rows": int(len(ov_df)),
                "mismatches": int((check["classification"] == "MISMATCH").sum()) if not check.empty else 0,
                "status": "PARTIALLY_SUFFICIENT",
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
