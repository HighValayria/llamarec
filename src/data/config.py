from pathlib import Path
from typing import Any

import yaml


def load_experiment_config(config_path: str | Path) -> dict[str, Any]:
    """读取实验配置，并记录仓库根目录。

    Args:
        config_path: 例如 ``configs/experiment.yaml``。

    Returns:
        加入 ``_repo_root`` 字段后的配置字典。
    """

    config_path = Path(config_path).resolve()
    if not config_path.exists():
        raise FileNotFoundError(f"配置文件不存在: {config_path}")

    with config_path.open("r", encoding="utf-8") as handle:
        config = yaml.safe_load(handle) or {}

    config["_repo_root"] = _infer_repo_root(config_path)
    return config


def resolve_dataset_paths(config: dict[str, Any], dataset_key: str) -> dict[str, Any]:
    """解析某个 MovieLens 数据集的输入和输出路径。

    返回值只描述文件系统位置和原始格式，不改变 Y/N/M 的任务语义。
    """

    repo_root = Path(config["_repo_root"])
    raw_info = config["raw_files"][dataset_key]

    ratings_path = _resolve_repo_path(repo_root, raw_info["ratings"])
    movies_path = _resolve_repo_path(repo_root, raw_info["movies"])
    output_root = _resolve_repo_path(
        repo_root,
        config.get("paths", {}).get(
            "processed_root",
            config.get("output", {}).get("base_dir", "data/processed"),
        ),
    )

    if not ratings_path.exists():
        raise FileNotFoundError(
            f"数据集 {dataset_key} 的评分文件不存在: {ratings_path}"
        )
    if not movies_path.exists():
        raise FileNotFoundError(
            f"数据集 {dataset_key} 的电影文件不存在: {movies_path}"
        )

    return {
        "ratings_path": ratings_path,
        "movies_path": movies_path,
        "output_dir": output_root / dataset_key,
        "ratings_format": raw_info.get("ratings_format", raw_info.get("format")),
        "movies_format": raw_info.get("movies_format", raw_info.get("format")),
        "columns": raw_info.get("columns", {}),
    }


def resolve_configured_output_path(
    config: dict[str, Any],
    dataset_key: str,
    *keys: str,
) -> Path:
    """解析 ``processed_outputs`` 中带 ``{dataset}`` 占位符的输出路径。

    示例：
        ``resolve_configured_output_path(config, "movielens-100k",
        "preference_samples", "train")``。
    """

    value: Any = config["processed_outputs"]
    for key in keys:
        value = value[key]

    if not isinstance(value, str):
        joined_keys = ".".join(keys)
        raise TypeError(f"processed_outputs.{joined_keys} 不是路径字符串")

    path = resolve_repo_path_from_config(
        config,
        value,
        dataset_key=dataset_key,
    )
    return _with_dataset_compression(path, config, dataset_key)


def resolve_repo_path_from_config(
    config: dict[str, Any],
    path_value: str | Path,
    dataset_key: str | None = None,
    split_name: str | None = None,
) -> Path:
    """解析可带 ``{dataset}`` / ``{split}`` 占位符的仓库路径。"""

    format_values = {
        "dataset": dataset_key or "",
        "split": split_name or "",
    }
    formatted = str(path_value).format(**format_values)
    return _resolve_repo_path(Path(config["_repo_root"]), formatted)


def get_positive_rating_threshold(config: dict[str, Any]) -> float:
    """读取 Y 任务的 Yes/No 标签阈值。"""

    return float(config["dataset"]["positive_rating_threshold"])


def dataset_uses_gzip_outputs(config: dict[str, Any], dataset_key: str) -> bool:
    """判断某个数据集的 processed JSONL 是否应写成 gzip。"""

    gzip_datasets = (
        config.get("storage", {})
        .get("gzip_processed_datasets", [])
    )
    return dataset_key in set(gzip_datasets)


def open_text_auto(path: str | Path, mode: str = "rt", encoding: str = "utf-8"):
    """根据后缀自动打开普通文本或 gzip 文本文件。"""

    import gzip

    path = Path(path)
    if path.suffix == ".gz":
        return gzip.open(path, mode, encoding=encoding, compresslevel=6)
    return path.open(mode, encoding=encoding)


def _infer_repo_root(config_path: Path) -> Path:
    if config_path.parent.name == "configs":
        return config_path.parent.parent
    return config_path.parent


def _resolve_repo_path(repo_root: Path, path_value: str | Path) -> Path:
    path = Path(path_value)
    if path.is_absolute():
        return path
    return repo_root / path


def _with_dataset_compression(
    path: Path,
    config: dict[str, Any],
    dataset_key: str,
) -> Path:
    if not dataset_uses_gzip_outputs(config, dataset_key):
        return path
    if path.suffix == ".gz":
        return path
    if path.suffix == ".jsonl":
        return path.with_suffix(path.suffix + ".gz")
    return path
