# 装配与验证

入口为 `assemble.py`，正文语法、常用命令与模板 ingestion 见 `../README.md`。只依赖标准库与 PyYAML，不加载模型、训练库或推理流程。

`paper_manifest.yaml` 指定模块顺序、证据 ID、图表文件和双语标题。正文使用 YAML frontmatter 与 `PARAGRAPH` / `INCLUDE` 注释，解析器拒绝无标记正文、重复 ID、缺少 EN/ZH、失效图表引用、数字/引用不对应以及 include 循环。图表在所选内容后集中附上，正文引用转换为稳定锚点。

```bash
python paper/assembly/prepare_assets.py
python paper/assembly/assemble.py --check
python -m unittest discover -s paper/assembly/tests -v
python -m py_compile paper/assembly/assemble.py paper/assembly/template_adapter.py paper/assembly/prepare_assets.py
```

`prepare_assets.py` 只读取列明的冻结 CSV/JSON/图片，生成论文展示表及来源 hash，不构造候选集、不评估模型、不重新做 bootstrap。`--check` 只验证选中源及引用资产，不输出论文。默认 `draft` 会报告待补标记；`final` 在选中源（含双语、递归 parts）、图表标题说明或模板中发现 `EVIDENCE_PENDING`、`TODO`、`PENDING`、`ABSTRACT_NOT_FINAL`、`CITATION_NEEDED` 就失败，源状态也必须为 `ready`。输出前先完成所有预检。文献缺口即使只在被隐藏的另一语言中出现也会阻止正式稿输出。

输出路径限定在 `paper/builds/`，避免覆盖作者源。每份 build 附有 `.build.json`，记录来源文件、段落 ID、语言、模式、图表、hash 和待补标记。Markdown 模板只处理 `{{content}}` 与 module mapping；其它格式以接口保留，不进行猜测转换。
