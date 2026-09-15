# Generic IEEE Submission Layer Adaptation

## Task Packet

- Stage: S5 submission engineering.
- Scope: 建立同一adapter驱动的English与bilingual IEEE LaTeX生成层、静态验证、轻量测试和可再生成build。
- Files to read: template-adaptation-preflight.md、IEEE通用模板、paper_manifest.yaml、assemble.py、template_adapter.py、library.bib及正式图表登记。
- Files allowed to edit: paper/submission/ieee_generic、paper/builds/ieee_generic生成物、独立submission tests、本任务包、paper/plan/progress.md、.agent/current_task.md、.agent/stage_state.yaml。
- Frozen inputs: paper/modules、paper/modules_parts、paper/references/library.bib、paper/tables CSV、paper/figures正式图片及科学证据控制文件。
- Required skills: using-research-writing、paper-orchestration、latex-output、peer-review、verification。
- Build variants: en为未来投稿候选；bilingual为逐段EN/ZH内部审阅稿，两者共享内容adapter和source of truth。
- Title source: 既有稿件metadata中的英文和中文标题；不从framing猜标题。
- Author mode: 默认anonymous_placeholder；camera_ready保留参数接口但没有真实作者时拒绝生成。
- Unknowns: venue、track、匿名政策、References页数政策、Appendix、Supplement、Abstract限制。
- Rejection checks: 不改作者源、不复制手写正文、不新建第二套bib、不改数据、不安装LaTeX、不泄漏内部marker或绝对路径、不把双语稿称为submission-ready。
- Required artifacts: submission_config.yaml、main_template.tex、build_submission.py、README、submission tests，以及en/bilingual两套生成结果。
- Validation: 原47项测试、submission独立测试、双语与英文assembly check、静态路径/引用/label/marker/CJK/配对/资产一致性、可重复生成、stage_guard、diff-check和作者源current contract。

## Implementation decisions

- 复用SourceReader做递归include、双语配对、数字和资产契约校验。
- 使用Mistune AST处理Markdown块和行内结构；只对项目自定义citation与asset标记使用受限解析。
- 生成表格保持CSV全部数据，按manifest展示列输出真实LaTeX tabular。
- 两版复制同一IEEEtran.cls、library.bib和figure字节到各自build包；这些是可再生成产物，不是第二套维护源。
- 无本地TeX工具时分别报告EN COMPILE_PENDING与BILINGUAL COMPILE_PENDING，不把静态生成判为失败。

## Review gates

1. Spec compliance: 两版、同一adapter、80个投稿paragraph pair、9个正文section、14表、2图、同一citation/bib/asset身份。
2. Quality and isolation: 英文无中文，双语逐段配对，内部metadata与本机路径不泄漏，作者源hash不变，生成结果可重复。

## Completion record

- 状态：COMPLETED，2026-09-10。
- 生成路径：`paper/builds/ieee_generic/en/`与`paper/builds/ieee_generic/bilingual/`。
- 共享链路：同一`build_submission.py`调用现有`SourceReader`，再由同一Mistune AST renderer生成两种语言变体；没有复制手写正文。
- 内容结构：9个投稿正文section、1个Abstract、80个paragraph pair；内部`contributions`模块的4对工作段落不进入投稿结构。
- 引用与资产：两版均为25个citation key、16个图表引用、14张真实LaTeX表、2张同字节figure；英文内容指纹、表格数据载荷和figure哈希跨版本一致。
- 静态验收：两版均PASSED；英文无CJK正文，双语严格80次EN/ZH交错，所有input、figure、citation、ref、label和内部marker检查通过。
- 编译状态：本机无latexmk、pdflatex、xelatex或bibtex；英文为`COMPILE_PENDING / LATEX_TOOLCHAIN_UNAVAILABLE`，双语为`COMPILE_PENDING / BILINGUAL_COMPILE_PENDING_CJK_ENV`。未安装任何环境，页数和排版warnings不可得。
- 测试：既有47项全部通过；新增8项全部通过；两种作者源assembly check均为11模块、84对段落、0 marker；stage_guard为0错误0警告。
- 冻结边界：current manuscript contract继续通过；未修改`paper/modules/**`、`paper/modules_parts/**`、`library.bib`、表格CSV、正式图片或科学证据控制文件。

## Capability-use audit

- 使用：using-research-writing、paper-orchestration、latex-output、peer-review、verification；实现时复用SourceReader、Mistune、PyYAML与现有manifest。
- 未使用：Wiki、网络检索、实验训练/推理、bootstrap、统计重算、LaTeX安装、字体下载或venue-specific模板猜测。
- 留待用户：venue、track、匿名政策、3至10个keywords、作者信息、References页数、Appendix/Supplement政策和Abstract字数上限。
