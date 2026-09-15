"""Template adapters for the template-independent authoring layer."""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

import yaml


class AssemblyError(ValueError):
    pass


class UniqueKeyLoader(yaml.SafeLoader):
    pass


def _mapping(loader: UniqueKeyLoader, node: yaml.MappingNode, deep: bool = False):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in result:
            raise AssemblyError(f"YAML 重复键：{key}")
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


UniqueKeyLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _mapping)


def parse_yaml(text: str) -> dict[str, Any]:
    try:
        value = yaml.load(text, Loader=UniqueKeyLoader)
    except yaml.YAMLError as exc:
        raise AssemblyError(f"YAML 解析失败：{exc}") from exc
    if not isinstance(value, dict):
        raise AssemblyError("YAML 顶层必须是 mapping")
    return value


def contained_path(root: Path, relative: str) -> Path:
    if not isinstance(relative, str) or not relative:
        raise AssemblyError("路径必须为非空字符串")
    candidate = (root / relative).resolve()
    if not candidate.is_relative_to(root.resolve()):
        raise AssemblyError(f"路径超出允许目录：{relative}")
    return candidate


def detect_template_type(directory: Path) -> str:
    manifest = directory / "template_manifest.yaml"
    if manifest.is_file():
        return str(parse_yaml(manifest.read_text(encoding="utf-8-sig")).get("format", "unknown"))
    found = set()
    for path in directory.iterdir():
        if path.suffix.lower() in {".tex", ".cls", ".sty"}:
            found.add("latex")
        elif path.suffix.lower() in {".docx", ".dotx"}:
            found.add("word")
        elif path.suffix.lower() == ".md":
            found.add("markdown")
    return next(iter(found)) if len(found) == 1 else "unknown"


class TemplateAdapter(ABC):
    """Adapters read structure and map modules before any build is written."""

    @abstractmethod
    def read_structure(self) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def map_modules(self, modules: list[dict]) -> list[dict]:
        raise NotImplementedError

    @abstractmethod
    def insert_content(self, content: str) -> str:
        raise NotImplementedError


class MarkdownAdapter(TemplateAdapter):
    def __init__(self, directory: Path | None = None):
        self.structure: dict[str, Any] = {}
        self.shell = "{{content}}\n"
        if directory is not None:
            manifest = directory / "template_manifest.yaml"
            if not manifest.is_file():
                raise AssemblyError("请先建立 template_manifest.yaml，记录模板结构和模块映射")
            self.structure = parse_yaml(manifest.read_text(encoding="utf-8-sig"))
            entry = contained_path(directory, self.structure.get("entry", ""))
            if not entry.is_file():
                raise AssemblyError(f"模板入口不存在：{entry}")
            self.shell = entry.read_text(encoding="utf-8-sig")
            if self.shell.count("{{content}}") != 1:
                raise AssemblyError("Markdown 模板必须且只能有一个 {{content}}")
            if "{{" in self.shell.replace("{{content}}", ""):
                raise AssemblyError("模板含未支持的插入变量")

    def read_structure(self) -> dict[str, Any]:
        return self.structure

    def map_modules(self, modules: list[dict]) -> list[dict]:
        order = self.structure.get("module_order")
        if order is not None:
            ids = [m["id"] for m in modules]
            if not isinstance(order, list) or len(order) != len(ids) or set(order) != set(ids):
                raise AssemblyError("模板 module_order 必须恰好覆盖所选模块，不可重复或漏节")
            by_id = {m["id"]: m for m in modules}
            modules = [by_id[key] for key in order]
        titles = self.structure.get("section_titles", {})
        if not isinstance(titles, dict):
            raise AssemblyError("section_titles 必须是 mapping")
        return [dict(m, title_override=titles.get(m["id"])) for m in modules]

    def insert_content(self, content: str) -> str:
        return self.shell.replace("{{content}}", content)


def get_adapter(directory: Path | None) -> TemplateAdapter:
    if directory is None:
        return MarkdownAdapter()
    if not directory.is_dir():
        raise AssemblyError(f"模板目录不存在：{directory}")
    kind = detect_template_type(directory)
    if kind != "markdown":
        raise AssemblyError(f"模板类型 {kind}：适配器尚未实现；请先完成实际模板 ingestion")
    return MarkdownAdapter(directory)
