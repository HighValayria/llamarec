# Evidence-Preserving Compression Execution Report

## A. Pre-state

- 执行方案：T-BALANCED + D-BALANCED + modified P-BALANCED（OPTION B）。
- 英文基线：约 6,949 words，14 pages；双语基线：22 pages。
- 父正文快照：`paper/archive/manuscript/pre_compression_2026-09-10/`，35/35 文件校验通过，aggregate SHA256 `0dd7bfc219bb47b1fa1fc649cd71cdfa399b2955ca62e391c0a25bf08f0565b5`。
- 父表快照：`paper/archive/tables/pre_compression_2026-09-10/`，14/14 CSV 校验通过。
- 父合同：`paper/plan/review/manuscript_contract_2026-09-10.json`，SHA256 `d0efaa782237488c5cca99fc0ac61454ce862cc2e0d0e9e2613b37111873b54f`。
- 禁止项得到遵守：未训练、未推理、未评测、未 bootstrap、未重算 CI、未访问或修改 Wiki、未调用 GPT6 Astra。

## B. Table transformations

新建四份确定性 compact/merged CSV：

1. `training_exposure_compact.csv`：9 行，压缩原 Table II 的重复标签与常量。
2. `supervision_semantics_compact.csv`：10 行，合并原 Table III/IV 为 Y-native 与 Y-as-ranker/N-native 双 panel。
3. `ms96_delta_summary_compact.csv`：24 行，保留双 split、binary 三指标、k5/k20/k50 三指标、mean、sample SD 和 42/43/44 逐 seed 方向。
4. `hard_candidate_compact.csv`：18 行，HR@1 保留 seed42 数值 CI；NDCG@5/MRR 保留点估计与各自 CI 状态。

原 VI/VII/XI/XII 已离开主文，但状态均为 `REMOVED_FROM_MAIN; RAW_ARCHIVED`，没有删除。完整映射见 `paper/plan/review/compression_table_mapping_2026-09-10.json`。

## C. Table lineage validation

- 生成器：`paper/tables/compression_2026-09-10/build_compact_tables.py`。
- lineage：`paper/tables/compression_2026-09-10/lineage.csv`，449 条输出单元格记录。
- `--check`、byte reproducibility、每个输出 cell 覆盖、原 14 CSV 与归档逐字节一致测试均通过。
- `scientific_recomputation=false`。只进行了选择、panel 合并、标签正规化和允许的方向/CI 状态显示变换。

## D. Main-table inventory

最终主文共 9 表：I datasets；II compact exposure；III merged supervision semantics；IV exposure scaling；V specialist/multitask；VI compact multiseed summary；VII compact seed42 intervals；VIII N/SASRec exposure；IX cross-dataset。Figure 1 与 Figure 2 均保留。

## E. Paragraph compression map

- 压缩前 submission 段落 80，压缩后 76。
- `results.rq4.p03` 合入 `results.rq4.p02`。
- `discussion.unification.p01/p02` 合入新增 `discussion.exposure.p03`。
- `discussion.external.p02` 合入 `discussion.external.p01`。
- `conclusion.p03` 合入 `conclusion.p02`；旧 `conclusion.p04` 映射到新 `conclusion.p03`。
- 未删除科学 claim。逐段 EN/ZH 哈希及 action 见 `paper/plan/review/compression_paragraph_mapping_2026-09-10.json`。

## F. EN/ZH consistency

- 所有被压缩或合并的段落同步编辑 EN/ZH。
- assembly 检查得到 80 个作者层 paragraph pairs（含 4 个内部 contribution 段）；submission 排除 contributions 后为 76 对。
- 数字配对、语言隔离、段落交错、citation 位置和完整 formulation 边界测试通过。
- Abstract SHA256 仍为 `a3abccd9c4b1bcd57932d8d6956da9650f73a694e90eecdb22eb7d277fc51773`：`ABSTRACT_CONTENT_UNCHANGED=YES`。

## G. Scientific guardrail audit

### Rejection checks

- RC01 PASS：compact VI（原 compact IX 职责）保留 24 行 mean/SD/sign；compact VII（原 compact X 职责）保留 HR 数值 CI 与其余指标独立 CI 状态。
- RC02 PASS：RQ3 valid/test 张力、非等价、完整 formulation、协议整体变化、Amazon 范围均紧邻相关结论。
- RC03 PASS：Discussion 为能力、曝光/共享建模、协议、曝光对齐基线四主题；Amazon 为短收束；C2 > C4 > C3 > C1 层级仍明确。
- RC04 PASS：Abstract 未压；删 Setup 数字前均有表或 caption 接收，94% legal pool、数据 universe 和四点实际消费仍在。
- RC05 PASS：35 源快照、14 表归档、旧合同均可恢复；新合同另建；VI/VII/XI/XII 仅在 compact 覆盖完成后移出主文。

### Approved actions

- A01 PASS：Table II 保留 run、steps、total 与 Y/N per-task exposure，正文保留 effective-batch 关系。
- A02 PASS：Table III 双 panel 保留 validation trajectory 与 test endpoints。
- A03 PASS：原 VI/VII 移出主文，compact summary 保留其 claim coverage。
- A04 PASS：原 XI/XII 移出主文，compact summary/interval 表与 seed43 non-monotonic anchor 接收证据。
- A05 PASS：compact summary 和 interval 表符合 RC01，未重算 CI。
- A06 PASS：原 I/V/VIII/XIII/XIV 与两图保留，Results 只保留必要 headline 数字。
- A07 PASS：Intro 去重且角色完整；Related Work 主题综合并保留四类前作边界。
- A08 PASS：Problem 仍是完整定义主位置；Method/Setup 只压重复说明。
- A09 PASS：Results 保留五 RQ、Amazon finding、最低证据与即时边界。
- A10 PASS：Discussion 四主题，Amazon 跨域解释保留为短收束。
- A11 PASS：Limitations 的统计、协议、外部效度、资源四类完整。
- A12 PASS：Conclusion 三段；EN/ZH 同步；Abstract 不变；合并映射已记录。

### DO_NOT_COMPRESS 1-20

1. PASS：三条件主命题、RQ1-RQ5、C2>C4>C3>C1 与 empirical-study 定位保留，无 first/new-model 表述。
2. PASS：H/H10、strictly earlier history、timestamp bucket、Y/N 合法目标和留出规则保留；N 未写成 next liked item。
3. PASS：Y 阈值、低评分参与构造、distractor 非 dislike、M1 共享 adapter 双接口和 complete-formulation 边界保留。
4. PASS：response-only loss、1:1、QLoRA、allowed-answer 与 multi-token complete-sequence likelihood 保留。
5. PASS：重复消费、非 unique interactions、M1 total/per-task、resume-skipping 前提及 per-example trace 边界保留。
6. PASS：数据任务/split、曝光身份、双 panel 与不可跨量纲比较均保留。
7. PASS：seed42 48k/96k 双 split、N 到 200k、Y limited/uneven 而非 saturation 均保留。
8. PASS：compact summary 的六类指标/双 split/mean/SD/sign 与 interval 表的分指标身份完整。
9. PASS：validation narrowing、96k replication、frozen-test N gap、Y-side preservation 与非 parity/equivalence 保留。
10. PASS：seed42 trajectory、three-seed 96k、training seed、candidate seed 四者明确区分。
11. PASS：paired user bootstrap 的分组、配对、95% 与 delta 方向保留，并与 training-run variability 区分。
12. PASS：n=3、ddof=1、SD 非 CI、cross-zero 非等价、无 margin/全比较校正/跨 seed 显著性结论均明确。
13. PASS：validation 决策、frozen test held-out、VALID_ONLY 和双 split 身份保留。
14. PASS：协议 separately constructed/non-nested、共同变化、seed43 k50<k5 反例和非因果边界保留。
15. PASS：PopMatch retrospective、residual popularity 与 sampled 非 full-catalog 保留。
16. PASS：四点实际消费、N 四点领先、SASRec 继续改善及最大曝光 gap 收窄并存。
17. PASS：Amazon test-only、earlier seed42、ranking-directional-only 及不支持的跨域范围均保留。
18. PASS：downstream task-sample exposure 不匹配 pretraining/tokens/updates/FLOPs/time/serving/deployment 保留。
19. PASS：Y>96k、N>200k 未知，exposure 同时改变 coverage 与 optimization history，无新增机制推断。
20. PASS：旧表、旧正文、旧合同、映射、EN/ZH 同步与 claim 等强度均完整。

## H. Citation audit

- 25 个正文引用键全部解析，引用位置与 registry 一致。
- unresolved citations：0；unresolved references：0；library.bib SHA256 `16a80cece100edf8be186d4d7f25c368a5f388869d79279769cacd2a3169e6b3`，相对父合同 0 修改。

## I. Post-compression contract

- 新合同：`paper/plan/review/manuscript_contract_post_compression_2026-09-10.json`。
- 保护 35 author sources、9 current main tables、2 formal figures 和 17 evidence/reference controls，共 63 项。
- 显式记录 parent snapshot aggregate、table snapshot 与父合同 path/id/SHA256；未覆盖旧合同。

## J. Compile results

- English：pdflatex + bibtex + pdflatex + pdflatex，`COMPILED`。
- Bilingual：xelatex + bibtex + xelatex + xelatex，`COMPILED`。
- 两者 undefined citations/references、duplicate labels、overfull boxes、missing characters、unprocessed floats 均为 0。

## K. Page counts and words

- English pages：14 -> 10。
- Bilingual pages：22 -> 15。
- English words：压缩前约 6,949；压缩后 4,151（对 76 个正式英文段落采用字母/数字及内部连字符的统一词法计数）。本机 `texcount` 因 MiKTeX 缺 Perl 不可用，未将失败结果冒充正式计数。

## L. Visual inspection

- 实际渲染 English 10/10 页并全部查看；实际渲染 bilingual 15/15 页，重点查看第一页、Table III、compact VI/VII、Figure 1/2、Discussion、Conclusion 与最后一页。
- 9 表均可读；Table III 双 panel、compact VI、compact VII 已额外做高分辨率局部检查。
- 两图清晰；float 顺序、section fragmentation、reference transition、末页平衡正常。
- 中文无乱码、tofu、重叠或裁切。

## M. Test results

- assembly/manuscript/evidence/citation/contract/table tests：53/53 PASS。
- submission/reference/render-contract tests：11/11 PASS。
- 合计：64/64 PASS。
- `python paper/assembly/assemble.py --check`：PASS。
- `git diff --check`：无 whitespace error；仅报告工作区既有 LF/CRLF 提示。

## N. Known unrelated guard issues

`python tools/stage_guard.py` 仍返回 1 个 `UNAUTHORIZED_WIKI_MODIFICATION`：工作区在本阶段开始前已有 `wiki/current_state.md`、`wiki/index.md`、`wiki/reports/README.md` 和 `wiki/reports/interview_guide/` 改动，而本阶段没有 Wiki 写授权。状态为 `PRE_EXISTING_WIKI_GUARD_CONFLICT`。本轮未读取、修改或清理 Wiki；该冲突不属于正文、表格、编译或证据失败。

## O. Stop recommendation

English 为 10 页，五 RQ、9 表、2 图、EN/ZH 配对、引用闭合与全部科学护栏均通过。因此结论为：`COMPRESSION_STOP_RECOMMENDED`。不进入第二轮压缩。
