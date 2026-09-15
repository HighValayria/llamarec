# Final Manuscript Readiness Audit

> **CURRENT STATUS UPDATE（2026-09-10）**：本审计中的 `RUN_METADATA` 待回收判断已被后续五份原机器JSON与本地冻结证据的交叉核对取代。该项现为 **RESOLVED WITH DISCLOSED LIMITS**；正式run到seed、最终checkpoint、候选和metric已绑定，M1继续保留resume/data-skipping限定，SASRec短尾计数继续取原alignment inventory。两处Methods marker已删除。不得按本文旧P1再次要求用户搜索机器；当前依据见 `paper/evidence/run_metadata_ledger.md`。

日期：2026-09-09。性质：只读审计与后续计划。本文不修改 manuscript，不执行训练、推理、bootstrap、文献检索或模板适配。

## A. Overall status

| 维度 | 当前状态 | 人话判断 |
| --- | --- | --- |
| 科学内容 | `MANUSCRIPT_CONTENT_COMPLETE` | 在当前冻结故事和证据边界内，Abstract、Introduction、Methods、Results、Discussion、Limitations、Conclusion 已形成完整闭环；没有发现必须用新实验补上的科学断点。 |
| 投稿准备 | `NOT_SUBMISSION_READY` | 运行记录尚未完全封口，引用控制资料有一处真实缺口，旧测试契约需要换代，venue/template 尚未指定；bootstrap provenance已于后续取证中关闭。 |
| 当前装配 | draft check 通过 | 11 个模块、84 对双语段落、2 处作者源待补标记；这说明稿件可完整装配，不代表可以投稿。 |
| final gate | 未通过，符合现状 | 2 处RUN_METADATA标记和 35 个作者源文件的 `draft` 状态会阻止 final build。状态切换应放在其余证据和仓库契约闭环之后。 |
| 近期章节 | 已完成 | Conclusion 审查建议 R01/R02 已执行、R03 未执行；Abstract 审查建议 R01/R02 已执行、R03/R04 未执行。两章当前不需要为了本审计再改。 |
| Methods 引用 | 已闭合正文引用 | Llama、LoRA、QLoRA、MovieLens、Amazon、SASRec、bootstrap 的正文引用、BibTeX 与 registry 已存在；遗留问题是 S26-S31 来源笔记未同步，不是重新检索文献。 |

本轮没有发现科学硬 blocker，也没有理由现在改正文。需要先把已有实验和统计结果的来源链整理到投稿可审计程度。若后续确认某项原始来源永久丢失，再决定是否披露 unknown 或缩窄对应句子；不能预先把“尚未取回”当成“实验无效”。

## B. Remaining marker matrix

| 项目 | 精确位置 / 数量 | 实际含义 | 阻塞科学有效性？ | 阻塞正文内容完成？ | 阻塞投稿？ | 最小动作 | 需远端或用户访问？ |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `RUN_METADATA` | `paper/modules_parts/methods/training_setup.md:44`、`baseline_setup.md:11`；2 处 | 当前配置、代码和冻结表已说明方法，但尚缺历史正式 run 到配置、checkpoint、seed、候选及指标文件的完整绑定 | 否；现有点估计不因此自动失效 | 否 | 是，属于方法可复现性与结果来源 blocker | 回收正文实际声称字段的历史记录并建立 run-to-result 映射；不扩展到正文未写的参数 | 是；需原训练/评估机器上的小型元数据文件或命令片段 |
| `BOOTSTRAP_PROVENANCE` | 原Methods marker已于2026-09-09删除 | exact shell invocation未留存；effective OUT、5000次、reuse行为、seed规则、summary/input及执行时期源码Git/blob身份已交叉恢复并登记 | 否 | 否 | 否 | **RESOLVED**；保留闭环记录，不再搜索或重跑 | 否 |
| `TEMPLATE_UNASSIGNED` | `paper/evidence/pending_evidence.md:16`、`paper/templates/README.md:3`；控制记录，不是作者源 marker | 尚未选择投稿 venue，也没有对应模板和 bibliography style | 否 | 否 | 是，属于提交格式 blocker | 用户先确定 venue，再做模板映射、篇幅与格式适配 | 需用户选择 venue；不需实验机器 |
| `S26-S31 notes` | `paper/references/primary_source_notes.md` 在 S25 后结束；缺 6 个已登记来源章节 | registry 已将六条来源标为 VERIFIED，但 primary-source notes 没有同步核读记录 | 否 | 否 | 是，属于证据档案一致性 blocker | 依据已有 registry、claim map 和已核来源补 S26-S31；不新搜文献 | 否 |
| 作者源 `draft` 状态 | 11 个 modules 与其直接 parts，共 35 个当前作者源 | final gate 的发布状态尚未切换 | 否 | 否 | 是，属于最终装配 blocker | 证据、测试契约、模板和用户定稿确认完成后，再统一核验并切换为 `ready` | 需用户定稿确认；不需实验机器 |

## C. Minimal RUN_METADATA matrix

只恢复当前 Methods 已经写出的事实。学习率、scheduler、optimizer 类别、CUDA/驱动版本目前没有写进 manuscript，不应为了“看起来完整”新增强制任务；若原记录顺手包含，可归档但不作为本轮最低关闭条件。

| Methods statement | Current evidence | Missing? | Must recover before submission? |
| --- | --- | --- | --- |
| 使用 Llama-3.2-3B-Instruct、QLoRA、冻结 4-bit NF4、LoRA r16/alpha32/dropout0.05、指定 target modules、gradient checkpointing、max length 2048 | 当前配置、训练代码、方法引用均支持这些字段 | 缺正式结果所对应历史 run 的生效配置绑定；精确 base revision 若有记录也未统一登记 | 是：至少证明模型身份和正文列出的适配字段确实属于正式 run；精确 revision 若从未保存，可明确披露 unknown |
| Y/N 使用 response-only loss；M1 以 1:1 交错，共享一个 adapter | 数据集与训练实现、当前配置、M1 曝光审计支持设计 | 缺正式 M1 run 的历史配置/命令与 resume、数据跳过状态绑定 | 是：M1 的 1:1 和 resume 条件直接支撑每任务曝光解释 |
| single-device micro-batch 1、gradient accumulation 8、effective batch 8 | 当前代码/配置和曝光表一致 | 缺各正式 LLM run 的 TrainingArguments、config snapshot 或实际命令片段证明生效值 | 是：这是 24k/48k/96k/200k 曝光换算的基础 |
| checkpoint 由累计 optimizer steps 和任务样本曝光标识；seed42 为完整轨迹，43/44 仅复现 96k | 冻结表、MS96 摘要、导入 artifact index 和当前 Methods 一致 | 缺 run/checkpoint/seed 到 validation/test metric 文件及候选文件的最终映射 | 是：只需覆盖论文实际使用的运行点，不恢复未报告 run |
| M1-48/M1-96 每任务曝光是均衡调度下的预期值，总曝光为两倍 | 代码和 `m1_exposure_audit.md` 支持算法与计数规则，正文已明确“预期”及 resume 条件 | 缺原 run 对正确续训、停止点和数据跳过的历史证明 | 是；若逐样本 trace 本来就未保留，保持现有限定即可，不要求重训制造 trace |
| SASRec 为本仓库 full-item CE 实现；四点 batch 512，S391 实际消费 200000，使用同一 PopMatch-k5 候选 | 当前实现、冻结四点表与 SASRec artifact index 支持 | 缺 S47/S94/S188/S391 的原 `run_summary`、valid/test metrics 和 candidate-files 绑定 | 是：尤其要保留 short final batch 的实际消费，不可按 391x512 回推 |

最小交付形式可以是一张有原文件依据的 run ledger，而不是复制全部 checkpoint。每条只需：run ID、dataset、model/config 身份、training seed、micro-batch、accumulation、目标/实际 step、checkpoint、M1 resume 来源、候选文件、split metric 文件及源文件路径。LLM 取相应 `run_summary.json`、`config_snapshot.yaml`、`trainer_state.json` 或命令片段；SASRec 取四个 run 的 `run_summary.json` 与 valid/test metrics。不要权重、optimizer state 或全量日志。

## D. Bootstrap dependency audit

当前本机已找到：binary/ranking 两份 bootstrap summary，均记录 5000 replicates；论文 CI 所需的 binary-valid 一份和 ranking k5/k20/k50 valid/test 六份配对预测均存在，行数分别为 12,381 与每份 5,675。原机器README、manifest、Git history、脚本blob hash与时间链进一步恢复了effective OUT、reuse行为、seed规则和执行时期源码身份。Exact shell invocation未留存并已明确披露。综合证据足以关闭该项，状态为RESOLVED。

| Section | Exact dependency | Current impact | If provenance cannot ultimately be recovered |
| --- | --- | --- | --- |
| Methods | `methods.statistics.p01-p02` 的用户级配对、有放回抽用户、2.5/97.5 百分位、seed42-only uncertainty 定义 | 直接依赖；现有脚本和资产支持方法内容，但缺历史执行版本绑定 | 必须把无法确认的执行细节改成可证实范围，不能声称完整复现链 |
| Results | `rq3_multitask_unification.md:14,25,36` 的 F1 正区间、AUC/Accuracy 与 k5 validation 跨零、k5 test 正区间；`rq4_hard_candidate_robustness.md:14,25` 的 k20/k50 正区间 | 直接依赖精确 CI 与“正/跨零”判断；这是唯一会受该缺口直接影响的主结果文字 | 保留点估计和三 seed 描述结果；删除或降级精确 CI 及由其直接支撑的 inferential 句，不重写故事主干 |
| Discussion | 没有直接引用 CI、bootstrap、跨零或统计显著性；条件性解释来自曝光轨迹和三 seed 点估计 | 不直接依赖 | 无需因该项单独改 Discussion，除非未来把 Results 主张整体降级 |
| Limitations | `08_limitations.md:12-16` 区分三 seed mean/SD 与 seed42 paired-bootstrap uncertainty，并声明不构成跨 seed significance | 直接依赖方法身份，但本句本身是限制而非强推断 | 将其改为仅陈述已确认的描述统计边界 |
| Conclusion | 不报告 CI；“接近/小幅优势”同时由三 seed 点估计和 test 方向支持 | 不直接依赖 | 不需要自动修改 |
| Abstract | 不报告 CI；主结论由曝光轨迹、三 seed 96k 点估计、协议方向及 SASRec 四点支持 | 不直接依赖 | 不需要自动修改 |

当前裁决：`BOOTSTRAP_PROVENANCE` 为 **RESOLVED**。Exact shell invocation未找到，但有效参数和源码身份已通过生成产物与Git证据交叉恢复；完整依据见 `paper/evidence/bootstrap_provenance_closure.md`。不再要求访问原机器，不重新bootstrap，不重算CI。

## E. Test-contract audit

当前测试实际为 47 项、10 个 failure 记录。这里按 failure 记录计数；一个测试可在内部隐藏多个文件差异。

| Failure group | 数量 | 分类 | 判断与后续 |
| --- | ---: | --- | --- |
| `test_export_hashes_match_frozen_inputs_and_current_products`：`library.bib` 旧 hash | 1 | **B HISTORICAL BASELINE SHOULD REMAIN IMMUTABLE** | 旧 asset provenance 描述的是加入 Methods 六条来源之前的 bibliography 快照。保留旧记录，新增当前 reference provenance/versioned baseline；不要覆写历史证据。 |
| `test_actual_citation_positions_match_registry`：S08、S26-S31 | 7 | **A TEST SHOULD BE UPDATED** | registry 的 Methods 位置是正确的；测试的 `setUpClass` 只装配 contributions/introduction/related_work，因此根本看不到 Methods。扫描器应按 manifest 读取全部当前模块，而不是删掉正确引用或把 registry 改回“未引用”。 |
| `test_primary_notes_and_landscapes_exist`：首先报缺 S26 | 1 | **C REAL CURRENT FAILURE** | `primary_source_notes.md` 实际只到 S25，S26-S31 六个章节均缺；registry 却已标 VERIFIED。应依据已有核验材料补齐六节，不需要新文献搜索。 |
| `test_preserved_files_and_append_only_literature_freeze`：旧 MS96 scope hashes | 1 | **B HISTORICAL BASELINE SHOULD REMAIN IMMUTABLE** | 基线保护的是 MS96 整合前范围；之后经过授权的 Results/Discussion、Methods 引用、Conclusion、Abstract 等修改已使多项 hash 合理变化。保留旧快照，另建 post-revision baseline/current-contract test，不回滚正文。 |

所以，10 个 failure 记录中，**真正表示当前资料缺失的是 1 个**；它具体代表 S26-S31 六节来源笔记未同步。7 个是扫描范围错误，2 个是历史快照没有版本化。没有 D 类模板相关测试失败，也不能为了得到 47/47 去回滚已经授权的正文或覆盖历史 hash。

## F. Template status

`TEMPLATE_UNASSIGNED` 的裁决是 **INTENTIONALLY_OPEN**。当前没有 venue、作者指南、页数限制、模板入口、section mapping 或 bibliography style；这是有意保留的决定点。

- 它不是科学 blocker。
- 它不是 manuscript-content blocker。
- 它是 submission-format blocker，因此当前不能声称 submission ready。
- 先由用户确定 venue；之后才读取官方模板并进行格式、篇幅、图表和参考文献样式适配。本轮不选择 venue、不下载模板、不推测页数要求。

## G. Content-complete verdict

**`MANUSCRIPT_CONTENT_COMPLETE`**。

这一结论指“当前冻结研究问题与可辩护证据范围内，正文故事和各章节内容已经完整”，不等于其余证据档案、自动测试或投稿格式已完成。RUN metadata 不要求新增科学结果；bootstrap provenance已闭环。现在不建议改正文。

## H. Submission-ready verdict

**`NOT_SUBMISSION_READY`**。

投稿前至少还要完成：最小 RUN metadata 绑定、S26-S31 笔记同步、测试契约版本化与全绿、venue/template 适配、35 个作者源的最终状态核验。这里没有一项要求新训练或新实验。

## I. Ordered next actions and model recommendation

| Priority | Task | Why now | Recommended model | Needs user / remote access? | Strict scope |
| --- | --- | --- | --- | --- | --- |
| P1 | 回收最小 RUN metadata 并建立 run ledger | 正文明确写了 batch、accumulation、seed、曝光、M1 比例与 SASRec 实际消费，投稿前必须能指回正式 run | 低成本模型生成逐机器只读命令；中档模型做 run-to-result 对齐 | 是，seed42/43/44、SASRec 和 Amazon 的原机器；可分批 | 只取正文所需字段与小型 JSON/YAML/日志片段，不取权重，不补 LR/scheduler/CUDA 任务 |
| P1 | 修复 reference/test contract | 这是目前唯一的本地真实资料缺口，也是 10 个失败清零的正确路径 | 低成本 coding 模型 | 否 | 补 S26-S31；让 citation scanner 覆盖 manifest 全模块；保留旧 hash，新增版本化 baseline；不改 manuscript |
| P1 | 用户确定 venue 后做模板适配 | 内容完整不等于满足投稿格式 | 中档 writing/coding 模型 | 需要用户给 venue；不需实验机器 | 只处理官方模板、篇幅、图表和 bibliography style，不改科学故事 |
| P2 | 最终装配、契约全检与科学一致性复核 | 前三项完成后才能把 35 个作者源从 draft 审定为 ready，并形成真正 final build | 中档模型做机械核验；GPT-6 高推理做最后一轮科学/一致性 review | 需要用户最终定稿确认 | 先 assembly/tests/marker 检查，再审 claim 边界；发现问题先报告，不自动扩写 |

原审计验证为47项、10个failure记录及3个marker。2026-09-09后续只删除Methods中的BOOTSTRAP_PROVENANCE注释，科学正文未改；重新装配已确认11模块、84对段落、2个RUN_METADATA marker。其余测试状态需在后续契约同步后重新验收。
