"""Validate bilingual sources and assemble reviewable Markdown builds."""

from __future__ import annotations

import argparse
from collections import Counter
import csv
import hashlib
import json
import re
import shutil
from pathlib import Path

from template_adapter import AssemblyError, contained_path, get_adapter, parse_yaml


ROOT = Path(__file__).resolve().parents[2]
DIRECTIVE = re.compile(r"<!--\s*(PARAGRAPH|INCLUDE):\s*([^<>]+?)\s*-->")
COMMENT = re.compile(r"<!--.*?-->", re.S)
PENDING = re.compile(r"EVIDENCE_PENDING|\bTODO\b|\bPENDING\b|ABSTRACT_NOT_FINAL|\bCITATION_NEEDED\b", re.I)
ASSET = re.compile(r"\[(TABLE|FIGURE):\s*([a-z][a-z0-9_]*)\]")
IDENTIFIER = re.compile(r"[a-z][a-z0-9_.-]*\Z")
NUMBER = re.compile(r"[-+]?\d+(?:,\d{3})*(?:\.\d+)?k?")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def bilingual_title(value: dict, lang: str) -> str:
    if not isinstance(value, dict) or any(not isinstance(value.get(k), str) or not value[k].strip() for k in ("en", "zh")):
        raise AssemblyError("标题与 caption 必须具有非空 en / zh")
    if lang == "bilingual":
        return f"{value['en']} / {value['zh']}"
    return value[lang]


class SourceReader:
    def __init__(self, root: Path, manifest: dict, lang: str, mode: str):
        self.root = root.resolve()
        self.manifest = manifest
        self.lang = lang
        self.mode = mode
        self.paragraphs: dict[str, dict] = {}
        self.sources: dict[str, str] = {}
        self.document_ids: set[str] = set()
        self.pending: list[str] = []
        self.unready: list[str] = []
        self.assets: list[tuple[str, str]] = []
        self.stack: list[Path] = []

    def inspect_pending(self, text: str, origin: str):
        for index, line in enumerate(text.splitlines(), 1):
            if PENDING.search(line):
                self.pending.append(f"{origin}:{index}: {line.strip()}")

    def read(self, relative: str, level: int = 1, expected_id: str | None = None, title_override=None) -> str:
        path = contained_path(self.root, relative)
        allowed = [self.root / "paper/modules", self.root / "paper/modules_parts"]
        if not any(path.is_relative_to(base) for base in allowed):
            raise AssemblyError(f"正文只能来自 modules / modules_parts：{relative}")
        if path in self.stack:
            raise AssemblyError(f"循环 INCLUDE：{relative}")
        if not path.is_file():
            raise AssemblyError(f"正文源不存在：{relative}")
        source = path.read_text(encoding="utf-8-sig")
        self.sources[relative] = digest(path)
        self.inspect_pending(source, relative)
        if not source.startswith("---\n") or "\n---\n" not in source[4:]:
            raise AssemblyError(f"缺少 YAML frontmatter：{relative}")
        head, body = source[4:].split("\n---\n", 1)
        meta = parse_yaml(head)
        doc_id = meta.get("id", "")
        if not isinstance(doc_id, str) or not IDENTIFIER.fullmatch(doc_id):
            raise AssemblyError(f"非法 document ID：{relative}")
        if expected_id is not None and expected_id != doc_id:
            raise AssemblyError(f"manifest 与文档 ID 不一致：{relative}")
        if doc_id in self.document_ids:
            raise AssemblyError(f"重复 document ID：{doc_id}")
        self.document_ids.add(doc_id)
        if meta.get("status") not in {"draft", "skeleton", "ready"}:
            raise AssemblyError(f"非法正文状态：{relative}")
        if meta["status"] != "ready":
            self.unready.append(f"{relative}: {meta['status']}")
        output = ["#" * level + " " + bilingual_title(title_override or meta.get("title"), self.lang)]
        tokens = list(DIRECTIVE.finditer(body))
        prefix = body[:tokens[0].start()] if tokens else body
        if COMMENT.sub("", prefix).strip():
            raise AssemblyError(f"发现未配对正文或未支持语法：{relative}")
        if not tokens and meta["status"] != "skeleton":
            raise AssemblyError(f"非 skeleton 文档没有正文：{relative}")
        self.stack.append(path)
        for i, token in enumerate(tokens):
            end = tokens[i + 1].start() if i + 1 < len(tokens) else len(body)
            segment = body[token.end():end]
            kind, identifier = token.group(1), token.group(2).strip()
            if kind == "INCLUDE":
                if COMMENT.sub("", segment).strip():
                    raise AssemblyError(f"INCLUDE 后有未标记正文：{relative}")
                output.append(self.read(identifier, level + 1))
            else:
                output.append(self.paragraph(identifier, segment, relative))
        self.stack.pop()
        return "\n\n".join(output)

    def paragraph(self, identifier: str, segment: str, relative: str) -> str:
        if not IDENTIFIER.fullmatch(identifier) or identifier in self.paragraphs:
            raise AssemblyError(f"重复或非法 paragraph ID：{identifier}")
        evidence = re.findall(r"<!--\s*EVIDENCE:\s*(.*?)\s*-->", segment)
        evidence_ids = [x.strip() for group in evidence for x in group.split(",") if x.strip()]
        if not evidence_ids or set(evidence_ids) - set(self.manifest["evidence_ids"]):
            raise AssemblyError(f"缺失或未知 EVIDENCE：{identifier}")
        clean = COMMENT.sub("", segment).strip()
        pair = re.fullmatch(r"\*\*EN\*\*\s*\n+(.+?)\n+\*\*ZH\*\*\s*\n+(.+)", clean, re.S)
        if pair is None or clean.count("**EN**") != 1 or clean.count("**ZH**") != 1:
            raise AssemblyError(f"EN/ZH 必须各有一个非空且相邻的段落：{identifier}")
        en, zh = (part.strip() for part in pair.groups())
        if not en or not zh:
            raise AssemblyError(f"空语言段落：{identifier}")
        if set(NUMBER.findall(en)) != set(NUMBER.findall(zh)):
            raise AssemblyError(f"EN/ZH 数字不对应：{identifier}; EN={NUMBER.findall(en)}; ZH={NUMBER.findall(zh)}")
        if Counter(ASSET.findall(en)) != Counter(ASSET.findall(zh)):
            raise AssemblyError(f"EN/ZH 图表引用不对应：{identifier}")
        for kind, key in ASSET.findall(en):
            section = "tables" if kind == "TABLE" else "figures"
            if key not in self.manifest.get(section, {}):
                raise AssemblyError(f"未登记图表：{kind}: {key}")
            if (kind, key) not in self.assets:
                self.assets.append((kind, key))
        if re.search(r"\[(?:TABLE|FIGURE):", ASSET.sub("", en + zh)):
            raise AssemblyError(f"图表引用语法错误：{identifier}")
        self.paragraphs[identifier] = {"source": relative, "evidence": evidence_ids}
        if self.lang == "bilingual":
            return f"**EN**\n\n{en}\n\n**ZH**\n\n{zh}"
        return en if self.lang == "en" else zh

    def render_assets(self) -> tuple[str, list[tuple[Path, str]]]:
        sections = []
        copies = []
        for kind, key in self.assets:
            group = "tables" if kind == "TABLE" else "figures"
            spec = self.manifest[group][key]
            self.inspect_pending(json.dumps(spec, ensure_ascii=False), f"{group}.{key}")
            path = contained_path(self.root / "paper", spec["source"])
            if not path.is_file():
                raise AssemblyError(f"图表文件不存在：{path}")
            self.sources[path.relative_to(self.root).as_posix()] = digest(path)
            label = self.asset_label(kind, key)
            caption = bilingual_title(spec.get("caption"), self.lang)
            section = [f'<a id="{kind.lower()}-{key}"></a>', f"### {label}. {caption}"]
            dest = f"assets/{group}/{key}{path.suffix.lower()}"
            copies.append((path, dest))
            if kind == "FIGURE":
                section.append(f"![{caption}]({dest})")
            else:
                with path.open(encoding="utf-8-sig", newline="") as handle:
                    reader = csv.DictReader(handle)
                    columns = spec.get("columns", [])
                    keys = [col["key"] for col in columns]
                    if not keys or len(set(keys)) != len(keys) or not set(keys).issubset(reader.fieldnames or []):
                        raise AssemblyError(f"图表列不合法：{key}")
                    titles = [bilingual_title(col["title"], self.lang) for col in columns]
                    section.append("| " + " | ".join(titles) + " |")
                    section.append("| " + " | ".join(["---"] * len(keys)) + " |")
                    rows = list(reader)
                    if not rows:
                        raise AssemblyError(f"空表格：{key}")
                    for row in rows:
                        if None in row or any(row.get(k) is None for k in keys):
                            raise AssemblyError(f"CSV 行列不齐：{key}")
                        self.inspect_pending(json.dumps(row, ensure_ascii=False), f"{key}.row")
                        section.append("| " + " | ".join(format_cell(row[k]) for k in keys) + " |")
            sections.append("\n\n".join(section[:2]) + "\n\n" + "\n".join(section[2:]))
        return "\n\n".join(sections), copies

    def asset_label(self, kind: str, key: str) -> str:
        same = [entry for entry in self.assets if entry[0] == kind]
        number = same.index((kind, key)) + 1
        label = {"en": {"TABLE": "Table", "FIGURE": "Figure"}, "zh": {"TABLE": "表", "FIGURE": "图"}}
        if self.lang == "bilingual":
            return f"{label['en'][kind]} / {label['zh'][kind]} {number}"
        return f"{label[self.lang][kind]} {number}"


def format_cell(value: str) -> str:
    try:
        if re.fullmatch(r"[-+]?\d+\.\d+(?:[eE][-+]?\d+)?", value):
            value = f"{float(value):.5f}"
    except (ValueError, OverflowError):
        pass
    return value.replace("|", "\\|").replace("\n", " ")


def assemble(manifest_path: Path, lang="bilingual", mode="draft", module_ids=None, template=None, output=None, check=False, root=ROOT) -> dict:
    root = root.resolve()
    if lang not in {"en", "zh", "bilingual"} or mode not in {"draft", "final"}:
        raise AssemblyError("不支持的语言或模式")
    manifest = parse_yaml(manifest_path.read_text(encoding="utf-8-sig"))
    if manifest.get("version") != 1 or not isinstance(manifest.get("evidence_ids"), list):
        raise AssemblyError("manifest 需要 version: 1 与 evidence_ids")
    modules = manifest.get("modules")
    if not isinstance(modules, list) or not modules:
        raise AssemblyError("manifest.modules 必须是非空列表")
    ids = [m["id"] for m in modules]
    if len(ids) != len(set(ids)):
        raise AssemblyError("manifest 中模块 ID 重复")
    if module_ids is not None:
        if not module_ids or len(module_ids) != len(set(module_ids)) or set(module_ids) - set(ids):
            raise AssemblyError("所选模块为空、重复或不存在")
        modules = [m for m in modules if m["id"] in module_ids]
    adapter = get_adapter(template)
    modules = adapter.map_modules(modules)
    reader = SourceReader(root, manifest, lang, mode)
    reader.inspect_pending(json.dumps(adapter.read_structure(), ensure_ascii=False), "template_manifest")
    content = "\n\n".join(reader.read(m["source"], expected_id=m["id"], title_override=m.get("title_override")) for m in modules)
    assets_text, copies = reader.render_assets()
    content = ASSET.sub(lambda match: f"[{reader.asset_label(*match.groups())}](#{match.group(1).lower()}-{match.group(2)})", content)
    if assets_text:
        title = bilingual_title({"en": "Tables and Figures", "zh": "表格与图"}, lang)
        content += f"\n\n## {title}\n\n{assets_text}"
    content = adapter.insert_content(content).rstrip() + "\n"
    reader.inspect_pending(content, "rendered_content")
    if lang != "bilingual" and ("**EN**" in content or "**ZH**" in content):
        raise AssemblyError("单语输出残留作者语言标记")
    if mode == "final" and (reader.pending or reader.unready):
        details = reader.pending + reader.unready
        raise AssemblyError("final build 被未完成证据/模块阻止：\n" + "\n".join(details))
    result = {
        "language": lang, "mode": mode, "modules": [m["id"] for m in modules],
        "paragraphs": reader.paragraphs, "sources_sha256": reader.sources,
        "manifest_sha256": digest(manifest_path), "pending": reader.pending,
        "unready": reader.unready, "assets": reader.assets,
    }
    if check:
        return result
    target = Path(output) if output is not None else root / "paper/builds" / f"paper_{lang}.md"
    if not target.is_absolute():
        target = root / target
    if target.suffix.lower() != ".md":
        target = target / f"paper_{lang}.md"
    target = target.resolve()
    if not target.is_relative_to((root / "paper/builds").resolve()):
        raise AssemblyError("输出必须位于 paper/builds/，不能覆盖作者源")
    # Complete validation before touching generated output or copied assets.
    for _, destination in copies:
        contained_path(root / "paper/builds", str((target.parent / destination).relative_to(root / "paper/builds")))
    target.parent.mkdir(parents=True, exist_ok=True)
    for source, destination in copies:
        dest = target.parent / destination
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, dest)
    target.write_text(content, encoding="utf-8", newline="\n")
    result["output"] = str(target)
    target.with_suffix(".build.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="双语模块验证与 Markdown 装配")
    parser.add_argument("--manifest", type=Path, default=ROOT / "paper/assembly/paper_manifest.yaml")
    parser.add_argument("--lang", choices=["en", "zh", "bilingual"], default="bilingual")
    parser.add_argument("--mode", choices=["draft", "final"], default="draft")
    parser.add_argument("--modules", nargs="+")
    parser.add_argument("--template", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        result = assemble(args.manifest, args.lang, args.mode, args.modules, args.template, args.output, args.check)
    except (AssemblyError, OSError, KeyError, TypeError) as exc:
        parser.exit(2, f"装配失败：{exc}\n")
    print(f"检查通过：{len(result['modules'])} 个模块，{len(result['paragraphs'])} 对段落，{len(result['pending'])} 处待补标记。")
    if "output" in result:
        print(f"已生成：{result['output']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
