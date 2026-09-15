"""Compare canonical N96 replay metrics against frozen seed42 references."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def metric_block(metrics: dict, split: str) -> dict[str, float]:
    ranking = metrics.get("ranking", metrics)
    return {
        "HR@1": float(ranking["HR@1"]),
        "NDCG@5": float(ranking["NDCG@5"]),
        "MRR": float(ranking["MRR"]),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--metrics-dir", default="recovery_runs/seed42_96/n/canonical_replay_seed42/canonical_replay_n_s12000_seed42/popmatch_eval")
    parser.add_argument("--historical", default="recovery/seed42_96_replay_plan/manifests/expected_historical_metrics.json")
    parser.add_argument("--out", default="recovery_runs/seed42_96/n/canonical_replay_seed42/canonical_replay_n_s12000_seed42/n96_historical_comparison.json")
    parser.add_argument("--tolerance", type=float, default=0.01)
    args = parser.parse_args()

    metrics_dir = Path(args.metrics_dir)
    historical = json.loads(Path(args.historical).read_text(encoding="utf-8"))["N96"]
    replay = {
        "validation": metric_block(json.loads((metrics_dir / "valid_metrics.json").read_text(encoding="utf-8")), "validation"),
        "test": metric_block(json.loads((metrics_dir / "test_metrics.json").read_text(encoding="utf-8")), "test"),
    }

    comparisons = {}
    primary_pass = True
    for split, values in replay.items():
        comparisons[split] = {}
        for metric, value in values.items():
            ref = float(historical[split][metric])
            delta = value - ref
            passed = abs(delta) <= args.tolerance
            if split == "validation" and not passed:
                primary_pass = False
            comparisons[split][metric] = {
                "historical": ref,
                "replay": value,
                "delta": delta,
                "absolute_tolerance": args.tolerance,
                "passed": passed,
            }

    status = "REPLAY_ACCEPTED" if primary_pass else "REPLAY_ACCEPTED_WITH_DRIFT"
    payload = {
        "schema": "n96_replay_comparison_v1",
        "status": status,
        "note": "Structural gate must be checked separately before final acceptance.",
        "comparisons": comparisons,
    }
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
