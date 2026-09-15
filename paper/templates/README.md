# 模板入口

当前没有指定 venue。后续将原始模板、作者须知、示例论文和 bibliography style 放入 `<venue>/`，读取后再编写 `template_manifest.yaml`。文件类型检测不等于已经支持该格式的完整转换。

目前可执行的最小 Markdown 模板契约：

```yaml
format: markdown
entry: template.md
module_order: [problem_formulation, methodology, experimental_setup, results]
section_titles:
  results:
    en: Experimental Results
    zh: 实验结果
```

`template.md` 必须且只能出现一次 `{{content}}`，装配器在此插入内容。`module_order` 如存在，必须恰好包含本次选中的全部模块 ID，不能静默丢节。`section_titles` 只覆盖展示标题。未经确认的动态模板指令不会执行。

LaTeX、Word 或未知混合模板目前明确报“适配器尚未实现”，待实际格式确定后扩展 `TemplateAdapter`。未来转换也必须保留段落映射、图表来源、pending 检查和生成物目录规则。
