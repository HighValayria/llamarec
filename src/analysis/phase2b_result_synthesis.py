"""Phase 2B paper-ready synthesis from existing analysis artifacts."""

from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any


DEFAULT_DATASET = "movielens-1m"
DEFAULT_OUTPUT_DIR = "outputs/phase2b/result_synthesis"

ROBUSTNESS_VARIANT_ORDER = [
    "k5_perm_seed43",
    "k20_seed42",
    "k20_perm_seed43",
    "k50_seed42",
]
MODEL_ORDER = ["Base", "Y-K0", "N-K0", "M0", "M1", "M2"]
ROBUSTNESS_MODEL_ORDER = ["base", "n_k0", "m1", "y_k0"]


def run_phase2b_result_synthesis(
    threshold_json: str | Path | None = None,
    grouped_json: str | Path | None = None,
    phase2a_metrics_json: str | Path | None = None,
    phase2a_comparison_csv: str | Path | None = None,
    output_dir: str | Path = DEFAULT_OUTPUT_DIR,
    dataset_key: str = DEFAULT_DATASET,
    allow_missing: bool = False,
) -> dict[str, Any]:
    """Write paper-ready Phase 2B tables and interpretation text."""

    paths = _resolve_input_paths(
        dataset_key=dataset_key,
        threshold_json=threshold_json,
        grouped_json=grouped_json,
        phase2a_metrics_json=phase2a_metrics_json,
        phase2a_comparison_csv=phase2a_comparison_csv,
    )
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    missing = _missing_inputs(paths)
    if missing and not allow_missing:
        missing_text = ", ".join(f"{name}={path}" for name, path in missing.items())
        raise FileNotFoundError(f"Missing Phase 2B input artifacts: {missing_text}")

    threshold_payload = _read_json_if_exists(paths["threshold_json"])
    grouped_payload = _read_json_if_exists(paths["grouped_json"])
    phase2a_metrics = _read_json_if_exists(paths["phase2a_metrics_json"]) or []
    phase2a_comparisons = _read_csv_if_exists(paths["phase2a_comparison_csv"])

    binary_rows = _binary_calibrated_test_rows(threshold_payload)
    canonical_ranking_rows = _canonical_ranking_test_rows(grouped_payload)
    robustness_rows = _robustness_test_rows(phase2a_metrics)
    robustness_delta_rows = _selected_robustness_delta_rows(phase2a_comparisons)
    claims = _paper_ready_claims(
        binary_rows=binary_rows,
        canonical_ranking_rows=canonical_ranking_rows,
        robustness_rows=robustness_rows,
        robustness_delta_rows=robustness_delta_rows,
    )

    output_files = {
        "binary_table_csv": output_path / "phase2b_binary_calibrated_test.csv",
        "canonical_ranking_csv": output_path / "phase2b_canonical_ranking_test.csv",
        "robustness_table_csv": output_path / "phase2b_robustness_test.csv",
        "robustness_deltas_csv": output_path / "phase2b_robustness_key_deltas.csv",
        "claims_json": output_path / "phase2b_paper_ready_claims.json",
        "report": output_path / "phase2b_result_synthesis.md",
    }

    _write_csv(output_files["binary_table_csv"], binary_rows)
    _write_csv(output_files["canonical_ranking_csv"], canonical_ranking_rows)
    _write_csv(output_files["robustness_table_csv"], robustness_rows)
    _write_csv(output_files["robustness_deltas_csv"], robustness_delta_rows)
    output_files["claims_json"].write_text(
        json.dumps(claims, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    _write_markdown_report(
        output_files["report"],
        dataset_key=dataset_key,
        input_paths=paths,
        missing_inputs=missing,
        binary_rows=binary_rows,
        canonical_ranking_rows=canonical_ranking_rows,
        robustness_rows=robustness_rows,
        robustness_delta_rows=robustness_delta_rows,
        claims=claims,
    )

    return {
        "dataset": dataset_key,
        "output_dir": str(output_path),
        "allow_missing": allow_missing,
        "missing_inputs": {name: str(path) for name, path in missing.items()},
        "rows": {
            "binary_calibrated_test": len(binary_rows),
            "canonical_ranking_test": len(canonical_ranking_rows),
            "robustness_test": len(robustness_rows),
            "robustness_key_deltas": len(robustness_delta_rows),
            "claims": len(claims),
        },
        "paths": {name: str(path) for name, path in output_files.items()},
    }


def _resolve_input_paths(
    dataset_key: str,
    threshold_json: str | Path | None,
    grouped_json: str | Path | None,
    phase2a_metrics_json: str | Path | None,
    phase2a_comparison_csv: str | Path | None,
) -> dict[str, Path]:
    return {
        "threshold_json": Path(
            threshold_json
            or f"outputs/calibration/{dataset_key}/threshold_comparison/threshold_comparison.json"
        ),
        "grouped_json": Path(
            grouped_json
            or f"outputs/error_analysis/{dataset_key}/grouped/test_grouped_error_analysis.json"
        ),
        "phase2a_metrics_json": Path(
            phase2a_metrics_json
            or "outputs/phase2a/ranking_robustness/phase2a_ranking_robustness_metrics.json"
        ),
        "phase2a_comparison_csv": Path(
            phase2a_comparison_csv
            or "outputs/phase2a/ranking_robustness/phase2a_ranking_robustness_comparison.csv"
        ),
    }


def _missing_inputs(paths: dict[str, Path]) -> dict[str, Path]:
    return {name: path for name, path in paths.items() if not path.exists()}


def _read_json_if_exists(path: Path) -> Any:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _read_csv_if_exists(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _binary_calibrated_test_rows(payload: dict[str, Any] | None) -> list[dict[str, Any]]:
    if not payload:
        return []
    rows = [
        row
        for row in payload.get("tables", {}).get("validation_calibrated", [])
        if row.get("split") == "test"
    ]
    output = []
    for row in sorted(rows, key=lambda item: _model_sort_key(str(item.get("model", "")))):
        output.append(
            {
                "model": row.get("model", ""),
                "run_name": row.get("run_name", ""),
                "threshold": _number(row.get("threshold")),
                "auc": _number(row.get("auc")),
                "f1": _number(row.get("f1")),
                "accuracy": _number(row.get("accuracy")),
                "precision": _number(row.get("precision")),
                "recall": _number(row.get("recall")),
                "fp": row.get("fp", ""),
                "fn": row.get("fn", ""),
            }
        )
    return output


def _canonical_ranking_test_rows(payload: dict[str, Any] | None) -> list[dict[str, Any]]:
    if not payload:
        return []
    rows = [
        row
        for row in payload.get("ranking", [])
        if row.get("split") == "test" and row.get("group_field") == "all"
    ]
    output = []
    for row in sorted(rows, key=lambda item: _model_sort_key(str(item.get("model", "")))):
        output.append(
            {
                "model": row.get("model", ""),
                "run_name": row.get("run_name", ""),
                "samples": row.get("samples", ""),
                "hr_at_1": _number(row.get("hr_at_1")),
                "hr_at_5": _number(row.get("hr_at_5")),
                "ndcg_at_5": _number(row.get("ndcg_at_5")),
                "mrr": _number(row.get("mrr")),
                "mean_rank": _number(row.get("mean_rank")),
                "mean_margin": _number(row.get("mean_margin")),
            }
        )
    return output


def _robustness_test_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    output = []
    for row in rows:
        if row.get("split") != "test":
            continue
        output.append(
            {
                "model_key": row.get("model_key", ""),
                "variant": row.get("variant", ""),
                "samples": row.get("samples", ""),
                "hr_at_1": _number(row.get("HR@1")),
                "hr_at_5": _number(row.get("HR@5")),
                "hr_at_10": _number(row.get("HR@10")),
                "hr_at_20": _number(row.get("HR@20")),
                "hr_at_50": _number(row.get("HR@50")),
                "ndcg_at_5": _number(row.get("NDCG@5")),
                "mrr": _number(row.get("MRR")),
            }
        )
    return sorted(output, key=lambda item: (_robustness_model_sort_key(item["model_key"]), _variant_sort_key(item["variant"])))


def _selected_robustness_delta_rows(rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    selected_prefixes = {
        "n_k0_minus_m1",
        "n_k0_minus_base",
        "m1_minus_base",
        "base_k20_perm_minus_k20",
        "n_k0_k20_perm_minus_k20",
        "m1_k20_perm_minus_k20",
        "base_k20_minus_k5_perm",
        "base_k50_minus_k20",
        "n_k0_k20_minus_k5_perm",
        "n_k0_k50_minus_k20",
        "m1_k20_minus_k5_perm",
        "m1_k50_minus_k20",
    }
    output = []
    for row in rows:
        if row.get("comparison") not in selected_prefixes:
            continue
        output.append(
            {
                "comparison": row.get("comparison", ""),
                "variant": row.get("variant", ""),
                "delta_hr_at_1": _number(row.get("delta_HR@1")),
                "delta_hr_at_5": _number(row.get("delta_HR@5")),
                "delta_ndcg_at_5": _number(row.get("delta_NDCG@5")),
                "delta_mrr": _number(row.get("delta_MRR")),
            }
        )
    return output


def _paper_ready_claims(
    binary_rows: list[dict[str, Any]],
    canonical_ranking_rows: list[dict[str, Any]],
    robustness_rows: list[dict[str, Any]],
    robustness_delta_rows: list[dict[str, Any]],
) -> list[dict[str, str]]:
    claims = []
    if binary_rows:
        best_f1 = _best_row(binary_rows, "f1")
        y_row = _find_row(binary_rows, "model", "Y-K0")
        m1_row = _find_row(binary_rows, "model", "M1")
        if best_f1:
            claims.append(
                _claim(
                    "binary_calibration",
                    f"{best_f1['model']} gives the strongest validation-calibrated binary F1 on the test split.",
                    f"test F1={_fmt(best_f1.get('f1'))}, AUC={_fmt(best_f1.get('auc'))}",
                )
            )
        if y_row and m1_row:
            claims.append(
                _claim(
                    "multi_task_binary_tradeoff",
                    "M1 nearly matches the dedicated Y-K0 preference model after validation-threshold calibration.",
                    f"Y-K0 F1={_fmt(y_row.get('f1'))}; M1 F1={_fmt(m1_row.get('f1'))}",
                )
            )
    if canonical_ranking_rows:
        best_hr1 = _best_row(canonical_ranking_rows, "hr_at_1")
        n_row = _find_row(canonical_ranking_rows, "model", "N-K0")
        m1_row = _find_row(canonical_ranking_rows, "model", "M1")
        if best_hr1:
            claims.append(
                _claim(
                    "canonical_ranking",
                    f"{best_hr1['model']} is the strongest canonical next-item ranking model.",
                    f"test HR@1={_fmt(best_hr1.get('hr_at_1'))}, NDCG@5={_fmt(best_hr1.get('ndcg_at_5'))}, MRR={_fmt(best_hr1.get('mrr'))}",
                )
            )
        if n_row and m1_row:
            gap = _delta(n_row.get("hr_at_1"), m1_row.get("hr_at_1"))
            claims.append(
                _claim(
                    "multi_task_ranking_boundary",
                    "M1 is the strongest multi-task ranking variant but remains below N-K0 on next-item ranking.",
                    f"N-K0 HR@1={_fmt(n_row.get('hr_at_1'))}; M1 HR@1={_fmt(m1_row.get('hr_at_1'))}; gap={_fmt(gap)}",
                )
            )
    if robustness_rows:
        n_k50 = _find_variant_row(robustness_rows, "n_k0", "k50_seed42")
        m1_k50 = _find_variant_row(robustness_rows, "m1", "k50_seed42")
        if n_k50 and m1_k50:
            claims.append(
                _claim(
                    "candidate_size_robustness",
                    "The N-K0 advantage over M1 grows under the k50 candidate-size stress test.",
                    f"N-K0 k50 HR@1={_fmt(n_k50.get('hr_at_1'))}; M1 k50 HR@1={_fmt(m1_k50.get('hr_at_1'))}",
                )
            )
    order_rows = [
        row
        for row in robustness_delta_rows
        if row.get("comparison", "").endswith("k20_perm_minus_k20")
    ]
    if order_rows:
        max_abs = max(abs(float(row["delta_hr_at_1"])) for row in order_rows if row.get("delta_hr_at_1") not in {"", None})
        claims.append(
            _claim(
                "order_sensitivity",
                "Candidate order perturbation has small effects compared with candidate-size expansion.",
                f"maximum absolute k20 order HR@1 delta among reported models={_fmt(max_abs)}",
            )
        )
    return claims


def _claim(topic: str, claim: str, evidence: str) -> dict[str, str]:
    return {"topic": topic, "claim": claim, "evidence": evidence}


def _write_markdown_report(
    path: Path,
    dataset_key: str,
    input_paths: dict[str, Path],
    missing_inputs: dict[str, Path],
    binary_rows: list[dict[str, Any]],
    canonical_ranking_rows: list[dict[str, Any]],
    robustness_rows: list[dict[str, Any]],
    robustness_delta_rows: list[dict[str, Any]],
    claims: list[dict[str, str]],
) -> None:
    lines = [
        "# Phase 2B Result Synthesis",
        "",
        f"Generated at: {datetime.now(timezone.utc).isoformat()}",
        f"Dataset: `{dataset_key}`",
        "",
        "This synthesis uses existing analysis artifacts only. It does not train models or recompute inference.",
        "",
        "## Inputs",
        "",
        *[f"- `{name}`: `{value}`" for name, value in input_paths.items()],
    ]
    if missing_inputs:
        lines.extend(
            [
                "",
                "Missing inputs were allowed for this run:",
                "",
                *[f"- `{name}`: `{value}`" for name, value in missing_inputs.items()],
            ]
        )
    lines.extend(
        [
            "",
            "## Paper-Ready Claims",
            "",
            _claims_list(claims),
            "",
            "## Table 1: Validation-Calibrated Binary Test Metrics",
            "",
            _markdown_table(
                binary_rows,
                ["model", "threshold", "auc", "f1", "accuracy", "precision", "recall", "fp", "fn"],
            ),
            "",
            "## Table 2: Canonical 5-Candidate Ranking Test Metrics",
            "",
            _markdown_table(
                canonical_ranking_rows,
                ["model", "samples", "hr_at_1", "ndcg_at_5", "mrr", "mean_rank", "mean_margin"],
            ),
            "",
            "## Table 3: Phase 2A Robustness Test Metrics",
            "",
            _markdown_table(
                robustness_rows,
                ["model_key", "variant", "samples", "hr_at_1", "hr_at_5", "hr_at_10", "hr_at_20", "hr_at_50", "ndcg_at_5", "mrr"],
            ),
            "",
            "## Table 4: Key Robustness Deltas",
            "",
            _markdown_table(
                robustness_delta_rows,
                ["comparison", "variant", "delta_hr_at_1", "delta_hr_at_5", "delta_ndcg_at_5", "delta_mrr"],
            ),
            "",
            "## Interpretation",
            "",
            "The results support a tradeoff interpretation. Dedicated Y supervision is strongest for calibrated preference prediction, while dedicated N supervision remains strongest for next-interaction ranking. M1 is the best current multi-task compromise: it approaches Y-K0 on calibrated binary metrics and is the strongest M ranking variant, but it does not replace N-K0.",
            "",
            "Phase 2A strengthens this boundary. Order perturbation is comparatively small, whereas larger candidate sets sharply reduce HR@1 and expose a growing gap between N-K0 and M1. Claims about ranking quality should therefore report candidate-set size and should not rely only on the canonical 5-candidate setting.",
            "",
            "## Claim Boundaries",
            "",
            "- Do not claim that M1 surpasses the best single-task models.",
            "- Do not treat Y-K0 `P(Yes)` ranking as next-interaction ranking.",
            "- Do not mix canonical 5-candidate metrics with explicit k20/k50 variant metrics in the same comparison table unless the candidate context is named.",
            "- Treat cold-item ranking as an unresolved weakness rather than a solved robustness result.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def _claims_list(claims: list[dict[str, str]]) -> str:
    if not claims:
        return "_No claims could be generated from the available inputs._"
    return "\n".join(
        f"- **{claim['topic']}**: {claim['claim']} Evidence: {claim['evidence']}."
        for claim in claims
    )


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _markdown_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._"
    lines = [
        "| " + " | ".join(fields) + " |",
        "|" + "|".join("---" for _ in fields) + "|",
    ]
    for row in rows:
        lines.append("| " + " | ".join(_display(row.get(field)) for field in fields) + " |")
    return "\n".join(lines)


def _number(value: Any) -> float | str:
    if value is None or value == "":
        return ""
    return round(float(value), 10)


def _display(value: Any) -> str:
    if value is None or value == "":
        return ""
    if isinstance(value, float):
        return f"{value:.10g}"
    return str(value)


def _fmt(value: Any) -> str:
    if value is None or value == "":
        return "NA"
    return f"{float(value):.4f}"


def _delta(left: Any, right: Any) -> float | None:
    if left in {"", None} or right in {"", None}:
        return None
    return round(float(left) - float(right), 10)


def _best_row(rows: list[dict[str, Any]], field: str) -> dict[str, Any] | None:
    candidates = [row for row in rows if row.get(field) not in {"", None}]
    if not candidates:
        return None
    return max(candidates, key=lambda row: float(row[field]))


def _find_row(rows: list[dict[str, Any]], field: str, value: str) -> dict[str, Any] | None:
    for row in rows:
        if row.get(field) == value:
            return row
    return None


def _find_variant_row(rows: list[dict[str, Any]], model_key: str, variant: str) -> dict[str, Any] | None:
    for row in rows:
        if row.get("model_key") == model_key and row.get("variant") == variant:
            return row
    return None


def _model_sort_key(model: str) -> tuple[int, str]:
    if model in MODEL_ORDER:
        return MODEL_ORDER.index(model), model
    return 99, model


def _robustness_model_sort_key(model_key: str) -> int:
    if model_key in ROBUSTNESS_MODEL_ORDER:
        return ROBUSTNESS_MODEL_ORDER.index(model_key)
    return 99


def _variant_sort_key(variant: str) -> int:
    if variant in ROBUSTNESS_VARIANT_ORDER:
        return ROBUSTNESS_VARIANT_ORDER.index(variant)
    return 99


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Phase 2B result synthesis for paper-ready reporting")
    parser.add_argument("--dataset", default=DEFAULT_DATASET)
    parser.add_argument("--threshold-json", default=None)
    parser.add_argument("--grouped-json", default=None)
    parser.add_argument("--phase2a-metrics-json", default=None)
    parser.add_argument("--phase2a-comparison-csv", default=None)
    parser.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--allow-missing", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    summary = run_phase2b_result_synthesis(
        threshold_json=args.threshold_json,
        grouped_json=args.grouped_json,
        phase2a_metrics_json=args.phase2a_metrics_json,
        phase2a_comparison_csv=args.phase2a_comparison_csv,
        output_dir=args.output_dir,
        dataset_key=args.dataset,
        allow_missing=args.allow_missing,
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
