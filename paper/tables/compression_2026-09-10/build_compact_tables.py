from __future__ import annotations

import argparse
import csv
from decimal import Decimal
import hashlib
import io
import json
from pathlib import Path


REPO = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
TABLES = REPO / "paper" / "tables"
OUTPUTS = (
    "training_exposure_compact.csv",
    "supervision_semantics_compact.csv",
    "ms96_delta_summary_compact.csv",
    "hard_candidate_compact.csv",
    "lineage.csv",
    "manifest.json",
)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_csv(name: str) -> list[dict[str, str]]:
    with (TABLES / name).open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def csv_bytes(fields: list[str], rows: list[dict[str, str]]) -> bytes:
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue().encode("utf-8")


def row_key(row: dict[str, str], fields: tuple[str, ...]) -> str:
    return "|".join(f"{field}={row[field]}" for field in fields)


def sign(value: str) -> str:
    number = Decimal(value)
    return "+" if number > 0 else "-" if number < 0 else "0"


def ci_status(low: str, high: str) -> str:
    if not low or not high:
        return "NA"
    if Decimal(low) > 0:
        return "POSITIVE"
    if Decimal(high) < 0:
        return "NEGATIVE"
    return "CROSSES_ZERO"


def build() -> tuple[dict[str, bytes], list[dict[str, str]]]:
    outputs: dict[str, bytes] = {}
    lineage: list[dict[str, str]] = []

    exposure = read_csv("training_exposure.csv")
    exposure_fields = ["run", "optimizer_steps", "total_exposure", "Y_exposure", "N_exposure"]
    exposure_rows = [{field: row[field] for field in exposure_fields} for row in exposure]
    outputs["training_exposure_compact.csv"] = csv_bytes(exposure_fields, exposure_rows)
    for index, (source, compact) in enumerate(zip(exposure, exposure_rows), 1):
        key = row_key(compact, ("run",))
        for field in exposure_fields:
            lineage.append({
                "output_file": "training_exposure_compact.csv", "output_row": str(index),
                "output_row_key": key, "output_column": field,
                "source_file": "paper/tables/training_exposure.csv",
                "source_row_key": row_key(source, ("run",)), "source_column": field,
                "transformation": "identity selection",
            })

    binary = read_csv("binary_exposure.csv")
    bridge = read_csv("semantics_bridge.csv")
    binary_index = {(row["run"], row["split"]): row for row in binary}
    bridge_index = {(row["run"], row["split"]): row for row in bridge}
    supervision_fields = [
        "panel", "run", "exposure", "split", "interface",
        "metric_1", "value_1", "metric_2", "value_2", "metric_3", "value_3",
    ]
    supervision_rows: list[dict[str, str]] = []
    supervision_sources: list[tuple[str, dict[str, str], tuple[str, ...]]] = []
    for run, split in (("Y24", "validation"), ("Y48", "validation"), ("Y96", "validation"), ("Y96", "test")):
        source = binary_index[(run, split)]
        supervision_rows.append({
            "panel": "A", "run": run, "exposure": source["exposure"], "split": split,
            "interface": "Y-native preference", "metric_1": "AUC", "value_1": source["AUC"],
            "metric_2": "F1", "value_2": source["F1"], "metric_3": "Accuracy", "value_3": source["Accuracy"],
        })
        supervision_sources.append(("paper/tables/binary_exposure.csv", source, ("run", "split")))
    for run, split in (
        ("Y24", "validation"), ("Y48", "validation"), ("Y96", "validation"),
        ("N96", "validation"), ("Y96", "test"), ("N96", "test"),
    ):
        source = bridge_index[(run, split)]
        supervision_rows.append({
            "panel": "B", "run": run, "exposure": source["exposure"], "split": split,
            "interface": source["interface"], "metric_1": "HR@1", "value_1": source["HR@1"],
            "metric_2": "NDCG@5", "value_2": source["NDCG@5"], "metric_3": "MRR", "value_3": source["MRR"],
        })
        supervision_sources.append(("paper/tables/semantics_bridge.csv", source, ("run", "split")))
    outputs["supervision_semantics_compact.csv"] = csv_bytes(supervision_fields, supervision_rows)
    source_value_columns = {
        "value_1": lambda row: row["metric_1"],
        "value_2": lambda row: row["metric_2"],
        "value_3": lambda row: row["metric_3"],
    }
    for index, (compact, (source_file, source, keys)) in enumerate(zip(supervision_rows, supervision_sources), 1):
        key = row_key(compact, ("panel", "run", "split"))
        for field in supervision_fields:
            if field in source_value_columns:
                source_column = source_value_columns[field](compact)
                transformation = "identity selection"
            elif field in {"run", "exposure", "split", "interface"}:
                source_column = field
                transformation = "identity selection"
            else:
                source_column = ""
                transformation = "static panel/display label"
            lineage.append({
                "output_file": "supervision_semantics_compact.csv", "output_row": str(index),
                "output_row_key": key, "output_column": field, "source_file": source_file,
                "source_row_key": row_key(source, keys), "source_column": source_column,
                "transformation": transformation,
            })

    summary = read_csv("ms96_delta_summary.csv")
    main_by_split = {
        "validation": read_csv("ms96_main_validation.csv"),
        "test": read_csv("ms96_main_test.csv"),
    }
    protocol_by_split = {
        "validation": read_csv("ms96_protocol_validation.csv"),
        "test": read_csv("ms96_protocol_test.csv"),
    }
    compact_summary_rows: list[dict[str, str]] = []
    for source in summary:
        split, protocol, metric = source["split"], source["protocol"], source["metric"]
        directions: list[str] = []
        direction_sources: list[str] = []
        if protocol == "binary":
            for row in sorted(main_by_split[split], key=lambda item: int(item["training_seed"])):
                delta = Decimal(row[f"M1-Y_{metric}"]) - Decimal(row[f"Y96_{metric}"])
                directions.append("+" if delta > 0 else "-" if delta < 0 else "0")
                direction_sources.append(row_key(row, ("training_seed",)))
        else:
            for row in sorted(
                (item for item in protocol_by_split[split] if item["protocol"] == protocol),
                key=lambda item: int(item["training_seed"]),
            ):
                directions.append(sign(row[f"delta_{metric}"]))
                direction_sources.append(row_key(row, ("training_seed", "protocol")))
        normalized_protocol = protocol.replace("_seed42", "")
        compact = {
            "split": split, "protocol": normalized_protocol, "metric": metric,
            "delta_definition": source["delta_definition"], "mean_delta": source["mean"],
            "sample_sd": source["sample_std"], "seed_directions_42_43_44": "/".join(directions),
        }
        compact_summary_rows.append(compact)
        key = row_key(compact, ("split", "protocol", "metric"))
        source_key = row_key(source, ("split", "protocol", "metric"))
        for field in compact:
            if field == "mean_delta":
                source_file, source_column, transform = "paper/tables/ms96_delta_summary.csv", "mean", "identity selection"
            elif field == "sample_sd":
                source_file, source_column, transform = "paper/tables/ms96_delta_summary.csv", "sample_std", "identity selection"
            elif field == "seed_directions_42_43_44":
                source_file = "paper/tables/ms96_main_{split}.csv or paper/tables/ms96_protocol_{split}.csv"
                source_column = f"within-seed delta_{metric}"
                transform = "sign only in seed order 42/43/44 from " + ";".join(direction_sources)
            else:
                source_file, source_column, transform = "paper/tables/ms96_delta_summary.csv", field, "identity selection or protocol label normalization"
            lineage.append({
                "output_file": "ms96_delta_summary_compact.csv", "output_row": str(len(compact_summary_rows)),
                "output_row_key": key, "output_column": field, "source_file": source_file,
                "source_row_key": source_key, "source_column": source_column, "transformation": transform,
            })
    summary_fields = [
        "split", "protocol", "metric", "delta_definition", "mean_delta", "sample_sd", "seed_directions_42_43_44",
    ]
    outputs["ms96_delta_summary_compact.csv"] = csv_bytes(summary_fields, compact_summary_rows)

    hard = read_csv("hard_candidate.csv")
    hard_fields = ["candidate_protocol", "split", "metric", "point_estimate", "ci95_low", "ci95_high", "ci_status"]
    hard_rows: list[dict[str, str]] = []
    for source in hard:
        is_primary = source["metric"] == "HR@1"
        compact = {
            "candidate_protocol": source["candidate_protocol"], "split": source["split"],
            "metric": source["metric"], "point_estimate": source["point_estimate"],
            "ci95_low": source["ci95_low"] if is_primary else "",
            "ci95_high": source["ci95_high"] if is_primary else "",
            "ci_status": ci_status(source["ci95_low"], source["ci95_high"]),
        }
        hard_rows.append(compact)
        key = row_key(compact, ("candidate_protocol", "split", "metric"))
        source_key = row_key(source, ("candidate_protocol", "split", "metric"))
        for field in hard_fields:
            if field == "ci_status":
                source_column, transform = "ci95_low;ci95_high", "deterministic interval-to-zero classification"
            elif field in {"ci95_low", "ci95_high"} and not is_primary:
                source_column, transform = field, "numeric bound omitted from compact display; retained in frozen source/archive"
            else:
                source_column, transform = field, "identity selection"
            lineage.append({
                "output_file": "hard_candidate_compact.csv", "output_row": str(len(hard_rows)),
                "output_row_key": key, "output_column": field,
                "source_file": "paper/tables/hard_candidate.csv", "source_row_key": source_key,
                "source_column": source_column, "transformation": transform,
            })
    outputs["hard_candidate_compact.csv"] = csv_bytes(hard_fields, hard_rows)

    lineage_fields = [
        "output_file", "output_row", "output_row_key", "output_column",
        "source_file", "source_row_key", "source_column", "transformation",
    ]
    outputs["lineage.csv"] = csv_bytes(lineage_fields, lineage)
    source_names = (
        "training_exposure.csv", "binary_exposure.csv", "semantics_bridge.csv",
        "ms96_delta_summary.csv", "ms96_main_validation.csv", "ms96_main_test.csv",
        "ms96_protocol_validation.csv", "ms96_protocol_test.csv", "hard_candidate.csv",
    )
    manifest = {
        "schema_version": 1,
        "snapshot_parent": "paper/archive/manuscript/pre_compression_2026-09-10",
        "transformation": "selection, panel merge, label normalization, and permitted direction/CI-status derivation only",
        "scientific_recomputation": False,
        "source_files": {f"paper/tables/{name}": sha256((TABLES / name).read_bytes()) for name in source_names},
        "outputs": {name: sha256(data) for name, data in outputs.items()},
        "row_counts": {
            "training_exposure_compact.csv": len(exposure_rows),
            "supervision_semantics_compact.csv": len(supervision_rows),
            "ms96_delta_summary_compact.csv": len(compact_summary_rows),
            "hard_candidate_compact.csv": len(hard_rows),
            "lineage.csv": len(lineage),
        },
        "lineage": "paper/tables/compression_2026-09-10/lineage.csv",
    }
    outputs["manifest.json"] = (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode("utf-8")
    return outputs, lineage


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    outputs, lineage = build()
    if args.check:
        mismatches = [name for name, data in outputs.items() if not (OUT / name).is_file() or (OUT / name).read_bytes() != data]
        if mismatches:
            parser.exit(1, "compact table mismatch: " + ", ".join(mismatches) + "\n")
        print(f"Compact tables verified; lineage records={len(lineage)}")
        return 0
    for name, data in outputs.items():
        (OUT / name).write_bytes(data)
    print(f"Compact tables generated; lineage records={len(lineage)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
