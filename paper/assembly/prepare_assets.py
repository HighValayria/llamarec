"""Export display assets from frozen evidence, without model evaluation."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[2]
FROZEN = ROOT / ".agent/exposure_scaling/final_evidence"
PAPER = ROOT / "paper"


def read_csv(path: Path) -> list[dict]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def export() -> dict:
    sources: dict[str, str] = {}
    products: dict[str, dict] = {}

    def record(path: Path):
        sources[path.relative_to(ROOT).as_posix()] = file_hash(path)

    def table(name: str, rows: list[dict], inputs: list[Path]):
        if not rows:
            raise ValueError(f"空导出表：{name}")
        target = PAPER / "tables" / f"{name}.csv"
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
            writer.writeheader()
            writer.writerows(rows)
        for path in inputs:
            record(path)
        products[target.relative_to(ROOT).as_posix()] = {
            "rows": len(rows), "sha256": file_hash(target),
            "sources": [p.relative_to(ROOT).as_posix() for p in inputs],
        }

    def copy(source: Path, target: Path):
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        record(source)
        products[target.relative_to(ROOT).as_posix()] = {
            "sha256": file_hash(target), "sources": [source.relative_to(ROOT).as_posix()],
            "transformation": "byte-identical copy",
        }

    main = FROZEN / "exposure_main_table.csv"
    rows = read_csv(main)
    if len(rows) != 28 or {r["seed"] for r in rows} != {"42"}:
        raise ValueError("冻结主表结构或 seed 范围变化，需要重新审查")
    expanded = []
    for row in rows:
        expanded.append(dict(row, metrics={row["primary_metric"]: row["primary_value"], **json.loads(row["secondary_metrics"])}))
    binary, ranking, bridge = [], [], []
    for row in expanded:
        common = {"run": row["run"], "exposure": row["exposure"], "split": row["split"], "seed": row["seed"]}
        if "binary" in row["task"]:
            binary.append({**common, **{key: row["metrics"][key] for key in ("AUC", "F1", "Accuracy")}})
        elif "bridge" not in row["task"]:
            ranking.append({**common, **{key: row["metrics"][key] for key in ("HR@1", "NDCG@5", "MRR")}})
        if "bridge" in row["task"] or row["run"] == "N96":
            bridge.append({**common, "interface": row["task"], **{key: row["metrics"][key] for key in ("HR@1", "NDCG@5", "MRR")}})
    table("binary_exposure", binary, [main])
    table("exposure_scaling", ranking, [main])
    table("semantics_bridge", bridge, [main])
    for name in ("specialist_multitask", "hard_candidate"):
        source = FROZEN / "tables" / f"table_{name}.csv"
        copy(source, PAPER / "tables" / f"{name}.csv")
    sasrec = FROZEN / "sasrec_exposure_alignment.csv"
    aligned = {r["run_name"]: r for r in read_csv(sasrec)}
    pairs = [("N24", "sasrec_s47"), ("N48", "sasrec_s94"), ("N96", "sasrec_s188"), ("N200", "sasrec_s391")]
    output = []
    for n_run, s_run in pairs:
        s = aligned[s_run]
        for split, prefix in (("validation", "valid"), ("test", "test")):
            n = next(row for row in expanded if row["run"] == n_run and row["split"] == split)
            output.append({
                "N_run": n_run, "SASRec_run": s_run, "N_exposure": n["exposure"],
                "SASRec_exposure": s["actual_exposure"], "split": split, "seed": "42",
                "N_HR@1": n["metrics"]["HR@1"], "SASRec_HR@1": s[f"{prefix}_hr1"],
                "delta_HR@1": float(n["metrics"]["HR@1"]) - float(s[f"{prefix}_hr1"]),
                "N_NDCG@5": n["metrics"]["NDCG@5"], "SASRec_NDCG@5": s[f"{prefix}_ndcg"],
                "N_MRR": n["metrics"]["MRR"], "SASRec_MRR": s[f"{prefix}_mrr"],
            })
    table("n_vs_sasrec_exposure", output, [main, sasrec])
    amazon_path = ROOT / ".agent/cross_dataset_validation/seed42_result_summary.json"
    amazon = json.loads(amazon_path.read_text(encoding="utf-8-sig"))
    amazon_rows = []
    for key, result in amazon["metrics"].items():
        if key.endswith("_popmatch"):
            amazon_rows.append({"run": key.removesuffix("_popmatch"), "protocol": "PopMatch-k5", "split": "test", "seed": "42", **result["ranking"]})
    if len(amazon_rows) != 5:
        raise ValueError("Amazon 冻结排序条目变化，需要审查")
    table("cross_dataset", amazon_rows, [amazon_path])
    for stem in ("fig_n_native_exposure", "fig_n_vs_sasrec_exposure"):
        for suffix in (".png", ".svg"):
            copy(FROZEN / "figures" / (stem + suffix), PAPER / "figures" / (stem + suffix))
        copy(FROZEN / "figures/data" / (stem + ".csv"), PAPER / "figures/data" / (stem + ".csv"))
    copy(ROOT / ".agent/paper_writing_submission/refs/bib_candidates.bib", PAPER / "references/library.bib")
    report = {"operation": "frozen-evidence display export; no training or inference", "sources_sha256": sources, "products": products}
    (PAPER / "evidence/asset_provenance.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    return report


if __name__ == "__main__":
    result = export()
    print(f"已从 {len(result['sources_sha256'])} 个冻结文件导出 {len(result['products'])} 项展示资产。")
