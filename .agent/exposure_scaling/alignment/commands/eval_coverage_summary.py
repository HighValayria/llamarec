"""汇总 exposure scaling 阶段的评测覆盖和指标缺口。

这个脚本只读取已经生成的 metrics JSON，不加载模型、不启动训练。
默认面向云端 `/root/llamarec` 运行，也可在本地仓库根目录运行。
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class RunSpec:
    name: str
    family: str
    exposure: int | str
    eval_dirs: tuple[str, ...]
    expected_binary: bool
    expected_ranking: bool
    notes: str = ""


RUNS: tuple[RunSpec, ...] = (
    RunSpec(
        "Y24",
        "Y-K0",
        24000,
        ("outputs/y/movielens-1m/exposure_y_s3000/popmatch_eval",),
        expected_binary=True,
        expected_ranking=True,
        notes="Y 原生二分类 + Y-as-ranker。",
    ),
    RunSpec(
        "Y48",
        "Y-K0",
        48000,
        ("outputs/y/movielens-1m/exposure_y_s6000/popmatch_eval",),
        expected_binary=True,
        expected_ranking=True,
        notes="Y 原生二分类 + Y-as-ranker。",
    ),
    RunSpec(
        "Y96",
        "Y-K0",
        96000,
        (
            "outputs/y/movielens-1m/exposure_y_s12000/popmatch_eval_valid_only",
            "outputs/y/movielens-1m/exposure_y_s12000/popmatch_eval",
        ),
        expected_binary=True,
        expected_ranking=True,
        notes="可选：只有当 Y 原生 binary 仍上涨时才建议训练。",
    ),
    RunSpec(
        "N24",
        "N-K0",
        24000,
        (
            "outputs/n/movielens-1m/sample_efficiency_n_s3000_popmatch_eval",
            "outputs/n/movielens-1m/pool200k_1m_n_3000_popmatch_eval",
        ),
        expected_binary=False,
        expected_ranking=True,
        notes="N 原生候选排序。",
    ),
    RunSpec(
        "N48",
        "N-K0",
        48000,
        ("outputs/n/movielens-1m/exposure_n_s6000/popmatch_eval",),
        expected_binary=False,
        expected_ranking=True,
        notes="N 原生候选排序。",
    ),
    RunSpec(
        "N96",
        "N-K0",
        96000,
        ("outputs/n/movielens-1m/exposure_n_s12000/popmatch_eval",),
        expected_binary=False,
        expected_ranking=True,
        notes="N 原生候选排序。",
    ),
    RunSpec(
        "N200",
        "N-K0",
        200000,
        ("outputs/n/movielens-1m/exposure_n_s25000/popmatch_eval",),
        expected_binary=False,
        expected_ranking=True,
        notes="N 原生候选排序。",
    ),
    RunSpec(
        "M1-48",
        "M1",
        "Y48k+N48k",
        (
            "outputs/m/movielens-1m/exposure_m1_s12000/popmatch_eval_valid_only",
            "outputs/m/movielens-1m/exposure_m1_s12000/popmatch_eval",
        ),
        expected_binary=True,
        expected_ranking=True,
        notes="M-Y 二分类 + M-N 排序。",
    ),
    RunSpec(
        "M1-96",
        "M1",
        "Y96k+N96k",
        (
            "outputs/m/movielens-1m/exposure_m1_s24000/popmatch_eval_valid_only",
            "outputs/m/movielens-1m/exposure_m1_s24000/popmatch_eval",
        ),
        expected_binary=True,
        expected_ranking=True,
        notes="M-Y 二分类 + M-N 排序。",
    ),
    RunSpec(
        "S23",
        "SASRec",
        11776,
        ("outputs/baselines/movielens-1m/alignment_sasrec_s23", "outputs/baselines/movielens-1m/sasrec_exp_match_k5_popmatch_seed42_s23"),
        expected_binary=False,
        expected_ranking=True,
    ),
    RunSpec(
        "S47",
        "SASRec",
        24064,
        ("outputs/baselines/movielens-1m/alignment_sasrec_s47", "outputs/baselines/movielens-1m/sample_efficiency_sasrec_s47_popmatch_eval"),
        expected_binary=False,
        expected_ranking=True,
    ),
    RunSpec(
        "S94",
        "SASRec",
        48128,
        ("outputs/baselines/movielens-1m/alignment_sasrec_s94", "outputs/baselines/movielens-1m/sasrec_exp_match_k5_popmatch_seed42_s94"),
        expected_binary=False,
        expected_ranking=True,
    ),
    RunSpec(
        "S188",
        "SASRec",
        96256,
        ("outputs/baselines/movielens-1m/alignment_sasrec_s188", "outputs/baselines/movielens-1m/sasrec_exp_match_k5_popmatch_seed42_s188"),
        expected_binary=False,
        expected_ranking=True,
    ),
    RunSpec(
        "S391",
        "SASRec",
        200000,
        ("outputs/baselines/movielens-1m/alignment_sasrec_s391", "outputs/baselines/movielens-1m/sasrec_exp_match_k5_popmatch_seed42_s391"),
        expected_binary=False,
        expected_ranking=True,
    ),
)


def main() -> None:
    root = Path.cwd()
    print("== 评测口径 ==")
    print("Y 原生: binary AUC/F1/Accuracy；Y-as-ranker: PopMatch 候选集上按 P(Yes) 排序的 HR@1/NDCG@5/MRR。")
    print("N 原生: PopMatch 候选排序 HR@1/NDCG@5/MRR。")
    print("M 原生: 同时包含 M-Y binary 与 M-N ranking。")
    print("SASRec: PopMatch 候选排序。HR@5 在 k=5 下通常恒为 1.0，主要看 HR@1/NDCG@5/MRR。")
    print()

    loaded: dict[tuple[str, str], dict[str, Any] | None] = {}
    for spec in RUNS:
        for split in ("valid", "test"):
            loaded[(spec.name, split)] = _load_metrics(root, spec, split)

    _print_binary_table(loaded)
    _print_ranking_table(loaded)
    _print_missing_table(loaded)
    _print_decision_hints(loaded)


def _load_metrics(root: Path, spec: RunSpec, split: str) -> dict[str, Any] | None:
    filename = f"{split}_metrics.json"
    for eval_dir in spec.eval_dirs:
        path = root / eval_dir / filename
        if path.exists():
            data = json.loads(path.read_text(encoding="utf-8"))
            data["_metrics_path"] = str(path)
            return data
    return None


def _metric(data: dict[str, Any] | None, section: str, key: str) -> Any:
    if not data:
        return "MISSING"
    value = data.get(section, {}).get(key)
    return "" if value is None else value


def _fmt(value: Any) -> str:
    if value == "MISSING":
        return "MISSING"
    if value == "":
        return ""
    if isinstance(value, float):
        return f"{value:.10f}"
    return str(value)


def _print_binary_table(loaded: dict[tuple[str, str], dict[str, Any] | None]) -> None:
    print("== BINARY：Y 原生 / M-Y 原生 ==")
    print("run\tfamily\texposure\tsplit\tsamples\tAUC\tF1\tAccuracy")
    for spec in RUNS:
        if not spec.expected_binary:
            continue
        for split in ("valid", "test"):
            data = loaded[(spec.name, split)]
            print(
                "\t".join(
                    [
                        spec.name,
                        spec.family,
                        str(spec.exposure),
                        split,
                        _fmt(_metric(data, "binary", "samples")),
                        _fmt(_metric(data, "binary", "AUC")),
                        _fmt(_metric(data, "binary", "F1")),
                        _fmt(_metric(data, "binary", "Accuracy")),
                    ]
                )
            )
    print()


def _print_ranking_table(loaded: dict[tuple[str, str], dict[str, Any] | None]) -> None:
    print("== RANKING：PopMatch-k5 / 候选排序 ==")
    print("run\tfamily\texposure\tsplit\tsamples\tHR@1\tHR@5\tNDCG@5\tMRR")
    for spec in RUNS:
        if not spec.expected_ranking:
            continue
        for split in ("valid", "test"):
            data = loaded[(spec.name, split)]
            print(
                "\t".join(
                    [
                        spec.name,
                        spec.family,
                        str(spec.exposure),
                        split,
                        _fmt(_metric(data, "ranking", "samples")),
                        _fmt(_metric(data, "ranking", "HR@1")),
                        _fmt(_metric(data, "ranking", "HR@5")),
                        _fmt(_metric(data, "ranking", "NDCG@5")),
                        _fmt(_metric(data, "ranking", "MRR")),
                    ]
                )
            )
    print()


def _print_missing_table(loaded: dict[tuple[str, str], dict[str, Any] | None]) -> None:
    print("== 缺口检查 ==")
    missing_rows = []
    for spec in RUNS:
        for split in ("valid", "test"):
            data = loaded[(spec.name, split)]
            if data is None:
                missing_rows.append((spec.name, split, "metrics_file", spec.eval_dirs))
                continue
            if spec.expected_binary and "binary" not in data:
                missing_rows.append((spec.name, split, "binary_section", (data["_metrics_path"],)))
            if spec.expected_ranking and "ranking" not in data:
                missing_rows.append((spec.name, split, "ranking_section", (data["_metrics_path"],)))
    if not missing_rows:
        print("没有发现预期 metrics 缺口。")
    else:
        print("run\tsplit\tmissing\tchecked_paths")
        for name, split, kind, paths in missing_rows:
            print(f"{name}\t{split}\t{kind}\t{';'.join(paths)}")
    print()


def _print_decision_hints(loaded: dict[tuple[str, str], dict[str, Any] | None]) -> None:
    print("== 决策提示 ==")
    y24 = loaded.get(("Y24", "valid"))
    y48 = loaded.get(("Y48", "valid"))
    if y24 and y48 and "binary" in y24 and "binary" in y48:
        print("Y24->Y48 原生 binary validation delta:")
        for key in ("AUC", "F1", "Accuracy"):
            left = y24["binary"].get(key)
            right = y48["binary"].get(key)
            if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                print(f"  {key}: {right - left:+.10f}")
        print("如果这些 delta 仍明显为正，再训练 Y96 才有充分理由；否则 Y96 优先级低。")
    else:
        print("先补/读取 Y24 与 Y48 的 binary validation；目前不能只用 Y-as-ranker NDCG 判断 Y 原生收敛。")
    print("validation 用于选择是否继续训练；test 只在决策冻结后补跑并报告。")


if __name__ == "__main__":
    main()
