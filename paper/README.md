# LlamaRec 模块化双语论文

主线：**Supervision Semantics Under Exposure**。定位：empirical study 与 evaluation methodology insights。当前正式内容源从此目录开始；投稿模板尚未指定。

## 审校入口

- [Introduction](modules/01_introduction.md)：7段双语初稿，研究空白和主要发现需优先审校。
- [Related Work](modules/02_related_work.md)：四主题和综合定位，正文在 `modules_parts/related_work/`。
- [贡献工作版](modules/00_contributions.md)：4项实证与评估贡献。

- [问题定义](modules/03_problem_formulation.md)：符号、任务语义与固定 RQ。
- [方法](modules/04_methodology.md) 与 [实验设置](modules/05_experimental_setup.md)：主文件规定顺序，正文细节在 `modules_parts/methods/`。
- [Results](modules/06_results.md)：总述与六个独立小节，实际段落在 `modules_parts/results/`。
- [Discussion](modules/07_discussion.md) 与 [Limitations](modules/08_limitations.md)：六节含义讨论与四主题独立限制。
- [修订交付](REVIEW_HANDOFF.md)：审校入口、验证结果和停止范围。
- [待补证据](evidence/pending_evidence.md)：MS96 和其他复现信息缺口。

00-02本轮新增20对双语段落，03-08的58对已审校正文保持不变，当前共78对。Conclusion与Abstract仍是骨架；Abstract保留 `ABSTRACT_NOT_FINAL`。文献主题结构已完成，引用覆盖仍未完备，具体见 [引用缺口](references/literature_gaps.md)。

## 内容与证据规则

实验事实以 `evidence/source_of_truth.md` 指向的冻结材料为准。`modules/` 是模块入口与正文主源；`modules_parts/` 是其引用的唯一细分正文源，不复制两份段落。模块通过 `INCLUDE` 指定组成和顺序，manifest 决定模块装配顺序。`builds/` 全是生成物，应回到正文源修改后重建。

所有正文先把问题、发现和意义讲清楚，再给必要边界；Methods 侧重准确、紧凑、可复现，Results 侧重观察，Discussion 侧重含义，Limitations 集中证据范围。避免假想审稿人对话、提示词痕迹和重复自我辩护。

验证集负责选择纪律，不构成科学证据等级；冻结测试结果参与最终解释。MS96 回填顺序与 split-specific A/B/C 见 [回填计划](evidence/ms96_integration_plan.md)。

每个论证单元使用稳定 ID，英文后紧接语义对应的中文。修改既有段落时保留 ID；拆段时新增 ID。

```markdown
<!-- PARAGRAPH: results.rq3.p02 -->
<!-- EVIDENCE: C5 -->
<!-- EVIDENCE_PENDING: MS96 -->

**EN**

English paragraph.

**ZH**

对应中文段落。
```

标题由各文件 YAML 头部的 `title.en` / `title.zh` 提供。`EVIDENCE` 注释中的C/M连接内部claim与方法证据，S编号连接文献注册表；`[TABLE: id]` / `[FIGURE: id]` 连接独立资产。单语输出剥离作者标记，保留所选语言的标题与正文。

## 装配入口

从仓库根目录运行，依赖 Python 3.10+ 与 PyYAML：

```bash
python paper/assembly/assemble.py --manifest paper/assembly/paper_manifest.yaml --check
python paper/assembly/assemble.py --manifest paper/assembly/paper_manifest.yaml --lang bilingual --modules problem_formulation methodology experimental_setup --output paper/builds/review/methods_bilingual.md
python paper/assembly/assemble.py --manifest paper/assembly/paper_manifest.yaml --lang bilingual --modules results --output paper/builds/review/results_bilingual.md
```

当前默认是 `--mode draft`。`--lang en`、`--lang zh`、`--lang bilingual` 均支持；不传 `--output` 时对应输出为 `paper/builds/paper_<lang>.md`。本轮只新增贡献、引言和相关工作的三语言独立审校件；旧方法、结果、讨论与局限性审校件保留，不生成整篇论文。`--mode final` 会拒绝任何所选模块及其引用部分、图表说明或模板中的 `EVIDENCE_PENDING`、`TODO`、`PENDING`、`ABSTRACT_NOT_FINAL`、`CITATION_NEEDED` 或未就绪状态，且报错时不覆盖旧 build。双语关系、数字核对和 pending 检查仍不能替代人工科学审校。

## 收到模板后

1. 把模板放入 `paper/templates/<venue>/`。
2. 让 Codex 定向读取模板文件、author instructions、example manuscript 与 bibliography style。
3. 生成 `template_manifest.yaml`，记录模板类型、入口和 module → venue section mapping。
4. 如需篇幅适配，另建 `paper/adaptations/<venue>/section_mapping.yaml`、`length_budget.yaml`、`venue_specific_edits.md`。
5. 在适配层处理顺序、节名、长度、关键词及附录要求，事实与证据边界仍由通用模块控制。
6. 装配到 `paper/builds/<venue>/`，审查后再决定提交。

```bash
python paper/assembly/assemble.py --template paper/templates/<venue>/ --manifest paper/assembly/paper_manifest.yaml --lang en --output paper/builds/<venue>/
```

当前仅实现基本 Markdown 装配和模板适配接口。LaTeX/Word 能识别类型，但等待实际模板后实现适配；不宣称现在就能编译任意格式。
