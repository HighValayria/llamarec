from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
EVIDENCE = ROOT / "paper/plan/task-packets"
OUT = Path(__file__).resolve().parent


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, fields: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def build_common_exposure() -> None:
    source = EVIDENCE / "m1-common-clean-exposure-verification.csv"
    rows = read_csv(source)
    assert len(rows) == 6
    output: list[dict[str, object]] = []
    for row in rows:
        for exposure in ("48", "96"):
            output.append(
                {
                    "split": row["split"],
                    "exposure_k": exposure,
                    "retained_n": row["common_clean_n"],
                    "metric": row["metric"],
                    "N": row[f"N{exposure}"],
                    "M1": row[f"M1_{exposure}"],
                    "delta_N_minus_M1": row[f"gap{exposure}"],
                    "delta_change_96_minus_48": row["gap_change"] if exposure == "96" else "",
                }
            )
    write_csv(
        OUT / "m1_common_safe_exposure.csv",
        ["split", "exposure_k", "retained_n", "metric", "N", "M1", "delta_N_minus_M1", "delta_change_96_minus_48"],
        output,
    )


def build_y_bootstrap() -> None:
    source = ROOT / "paper/tables/specialist_multitask.csv"
    rows = [row for row in read_csv(source) if row["comparison"] == "Y96 vs M1-96-Y"]
    assert [row["metric"] for row in rows] == ["AUC", "F1", "Accuracy"]
    fields = ["comparison", "metric", "point_estimate", "ci95_low", "ci95_high"]
    write_csv(
        OUT / "y_side_binary_bootstrap.csv",
        fields,
        [{field: row[field] for field in fields} for row in rows],
    )


def build_multiseed() -> None:
    source = EVIDENCE / "m1-clean-subset-audit/clean_multiseed_96_summary.csv"
    rows = read_csv(source)
    assert len(rows) == 18
    output: list[dict[str, object]] = []
    for row in rows:
        deltas = [float(row[f"seed{seed}_delta"]) for seed in (42, 43, 44)]
        assert int(row["positive_seed_count"]) == sum(value > 0 for value in deltas) == 3
        output.append(
            {
                "split": "validation" if row["split"] == "valid" else row["split"],
                "protocol": row["variant"],
                "metric": row["metric"],
                "delta_definition": "N96 - M1-N",
                "mean_delta": row["delta_mean"],
                "sample_sd": row["delta_sample_sd"],
                "signs_42_43_44": "+/+/+",
            }
        )
    write_csv(
        OUT / "m1_clean_multiseed_96.csv",
        ["split", "protocol", "metric", "delta_definition", "mean_delta", "sample_sd", "signs_42_43_44"],
        output,
    )


def build_coverage() -> None:
    rows = read_csv(EVIDENCE / "m1-common-clean-exposure-verification.csv")
    by_split = {row["split"]: row for row in rows if row["metric"] == "HR@1"}
    output: list[dict[str, object]] = []
    for exposure in ("48", "96"):
        for split in ("validation", "test"):
            retained = int(by_split[split][f"m1_{exposure}_clean_n"])
            output.append(
                {
                    "M1_point": f"M1-{exposure}",
                    "split": split,
                    "retained": retained,
                    "full_holdout": 5675,
                    "coverage_percent": f"{100 * retained / 5675:.2f}",
                }
            )
    expected = [5494, 5600, 5318, 5535]
    assert [int(row["retained"]) for row in output] == expected
    write_csv(
        OUT / "m1_cross_task_safe_coverage.csv",
        ["M1_point", "split", "retained", "full_holdout", "coverage_percent"],
        output,
    )


def build_amazon_safe() -> None:
    source = ROOT / "paper/tables/cross_dataset.csv"
    rows = [row for row in read_csv(source) if row["run"] != "m"]
    assert [row["run"] for row in rows] == ["base", "y", "n", "sasrec"]
    write_csv(OUT / "amazon_certified_models.csv", list(rows[0]), rows)


def main() -> None:
    build_common_exposure()
    build_y_bootstrap()
    build_multiseed()
    build_coverage()
    build_amazon_safe()
    print("scientific repair tables built from existing evidence")


if __name__ == "__main__":
    main()
