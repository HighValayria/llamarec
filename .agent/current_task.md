# Current Task

## Stage Goal
- 在 `paper/human_alter/` 建立长期可用的 English MASTER -> Bilingual REVIEW DOCX 同步系统。

## Scope
- 复用 78 个既有 manuscript paragraph IDs，使用不可见 OOXML bookmarks 建立稳定映射。
- 管理正文、标题、caption、9 张表、2 张图、25 条参考文献及必要 metadata。
- 实现 `status`、`sync-en`、`check`、`commit`、`remap`、中文更新队列、语义复核队列、备份和历史快照。
- 创建托管 DOCX，并完成隔离 fixture 与全页视觉回归。

## Non-Goals
- 不修改 manuscript source、科学结论、数字、表图内容或中文翻译。
- 不训练、推理、bootstrap、重新评测、压页、填写 Author/GenAI 或访问 Wiki。

## Long-Term Constraints
- `work/ICECAI_2026_English_MASTER.docx` 是唯一英文真源。
- `work/ICECAI_2026_Bilingual_REVIEW.docx` 是派生审阅稿，英文层只能由工具同步。
- 脚本只保证英文精确同步、数字/引用/已知限定词检查；中文语义必须人工复核。
- 结构变化不得静默猜测，必须进入 `STRUCTURAL_DRIFT` / remap proposal。

## Evidence Sources
- `paper/human_alter/English.docx` 与 `paper/human_alter/Bilingual.docx`（只读初始化输入）。
- `paper/modules/10_abstract.md` 与 `paper/modules/01_*.md` 至 `09_*.md` 的 78 个既有 EN/ZH ID 标记。
- `paper/human_alter/sync_manifest.json`、`INITIALIZATION_REPORT.md` 与 `out/fixture_test_report.json`。

## Related Code
- `paper/human_alter/sync.py`
- `paper/human_alter/docx_model.py`
- `paper/human_alter/mapping.py`
- `paper/human_alter/checks.py`
- `paper/human_alter/test_sync.py`

## Current Progress
- 系统已建立在用户指定的既有 `paper/human_alter/` 目录，原始 DOCX 未覆盖。
- 已生成英文 MASTER 与双语 REVIEW；78 个既有段落 ID 全部复用。
- 共管理 101 个英文块、99 个 EN/ZH pair、2 个无中文块、9 表、2 图、25 references。
- 初始化对派生稿中 15 个既有英文差异块及 references 做 MASTER 对齐；中文块未改。
- `status`、`sync-en`、`check`、`commit --confirm-zh-reviewed`、`remap` 和 `--dry-run` 已实现。
- Windows 入口 `status.bat`、`sync_en.bat`、`check.bat`、`commit.bat` 已建立。
- 新知识已同步到 `wiki/guides/docx_sync_workflow.md`、`wiki/current_state.md`、`wiki/index.md` 与 `wiki/history/2026-09.md`。

## Verification Results
- Python compile 通过。
- 基线：EN_SYNC/TABLE_SYNC/REFERENCE_SYNC/NUMERIC_PARITY/CITATION_PARITY 均 PASS；STRUCTURAL_DRIFT=0；ZH_UPDATE_REQUIRED=0。
- A-G fixture 7/7 PASS；删除/拆分 paragraph 均触发结构漂移。
- OOXML anchor 对英文与双语原稿的 visible digest 变化均为 0。
- Microsoft Word + bundled Poppler 全页渲染：英文 10->10 页，双语 14->14 页；统一 1020x1320；edge intrusion=0。
- 英文 before/after 像素差为 0；双语总览未见 clipping、overlap、表格损坏、分栏或 section break 漂移。
- 授权同步期间 `wiki_guard.py` 为 0 errors（8 个既有 warning），`stage_guard.py` 为 0 errors / 0 warnings。

## Unresolved Questions
- None for this stage. Author 与 GenAI 仍为 DEFERRED。

## Pending Wiki Sync
None.

## Invalidating Conditions
- 用户绕过 MASTER 直接修改双语英文层。
- 删除、合并、拆分正文段落，新增 section，或增删整张表/图而未执行 remap review。
- 变更中文后未完成 numeric/citation/semantic review 即提交 baseline。
