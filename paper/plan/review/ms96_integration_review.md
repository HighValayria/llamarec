# MS96证据整合复核

日期：2026-09-08。结论：本轮有限整合完成，稿件仍为draft，不等于投稿稿完成。两轮审查均由当前任务执行，未冒充独立Agent评审。

## 一、范围与科学合规
- 用户授权的轻量Git结果固定于a9c6cd959cf32afe046bb05be9eb5096bebfc5fb；8份文本的规范化blob一致，HEAD保持dcd4b9f6125fd0e7eb7c83b686223d8b9a44f6c1。没有merge/checkout/reset。
- 本轮修改12份作者源的20对双语段落，段落ID不变。intro仅p06，contributions仅p02/p03；07 wrapper无需修改，03/04/05 wrapper未改，仅statistics.p02作最小补充。
- 57份保护文件SHA256一致，含参考文献、Related Work、未授权方法、原图表、RQ1/RQ2/Amazon、摘要/结论和final_novelty_claim_map。freeze原文逐字保留，只在末尾追加MS96更新。
- 144条原生指标来自冻结CSV与43/44汇总；72条同seed差值；24组mean/sample std。summary与validation_summary重复不双计；Y-as-ranker不混入N-native，M-Y样本数不冒充M-N样本数。
- seed42标准k5验证48→96k缩小，与43/44的96k复现分开；全曲线不升级。test三seed均N略强；Y整体相近，seed44验证Accuracy微降保留。
- k20三seed两split三指标均N>M且差值大于k5；k50同方向但小于k20，并非每项均大于k5。采样、组成、数量与难度共同变化，不写纯大小因果。
- bootstrap仍是原seed42区间；n=3/ddof=1是训练seed差值的描述统计，不是CI或显著性。无等价/正迁移检验，不提出或执行新实验。
- validation选择与test留出角色明确；SASRec仍为正式seed42四点，Amazon仍为旧seed42排序方向。索引路径核对不冒充完整远端JSON或运行参数复核。

## 二、叙事与语言质量
Results按Y保留、验证轨迹/96k复现、冻结test、k20、k50、协议解释推进。Discussion先讲“低曝光的模型关系并非固定”“小k5差距不自动推广”的意义，再交代证据范围，未变成先堆局限的答辩清单。
C2篇幅最长、C1最短，C4第二主贡献，C3解释C2的协议边界。引言不堆大量指标，数字主要留在结果与表格；贡献、新颖性和现有引用位置不变。
12份作者源运行style_check.ps1，正文列表、禁用过渡、主观判断和过程泄漏均无命中。加粗提示仅EN/ZH标识，连续行提示为frontmatter元数据，不是正文样式错误。通用chapters完整稿门禁与本项目模块结构不适配，未声称通过，采用仓库装配契约。
危险词命中逐项检查：seed42-only只限定全曲线；positive transfer、equivalence、candidate-size、monotonic均在否定或限制上下文。原冻结CSV的parity历史解释列未改，不在当前展示列中采用。历史文献报告/旧备份不做机械替换。
发现的三处易误读已收紧：seed42 test gap并未从48k缩至96k；k50 gap并非一律大于k5；seed44验证Accuracy并非提升。“k50更seed-sensitive”改为幅度随seed变，不暗指绝对SD大于k20。

## 三、实际验证
| 检查 | 命令/方法 | 结果 |
| --- | --- | --- |
| 描述统计可再生 | python -X utf8 paper/analysis/ms96_evidence.py --check | 8份数据产物一致，无推理或重采样 |
| 回归测试 | python -X utf8 -m unittest discover -s paper/assembly/tests -v | 47通过，其中12项新MS96测试；原测试未放宽 |
| 全模块双语 | python -X utf8 paper/assembly/assemble.py --lang bilingual --check | 11模块、78对、8处剩余标记，exit0 |
| final只读探针 | 同上加--mode final | exit1，按预期由方法引文、RUN_METADATA、BOOTSTRAP_PROVENANCE、骨架与draft阻拦；无稿件输出 |
| 来源/范围 | 新测试与Git规范化blob核对 | 57项保护哈希一致；8导入文本对应固定提交；freeze只追加 |
| ID与引用 | 修改前后段落对照、既有文献资产测试 | 20对修改ID不变；文献引用键/位置/双语一致 |
| 语言 | 12个style_check.ps1 | 正文扫描无问题；元数据提示人工分类 |
| 空白 | git diff --check -- .agent/current_task.md .agent/stage_state.yaml paper | exit0；68条既有换行提示，无其他输出 |
| 任务边界 | python -X utf8 tools/stage_guard.py | 0错误、0警告 |

逐文件记录见 [ms96_integration_audit.json](ms96_integration_audit.json)，修改前基线见 [ms96_scope_baseline.json](ms96_scope_baseline.json)。本轮没有prepare_assets、整稿装配、图重绘、训练、推理、文献搜索或Wiki读写。

## 四、残余限制
MS96与Y96_STATUS已关闭，RUN_METADATA、BOOTSTRAP_PROVENANCE、METHOD_CITATIONS、TEMPLATE_UNASSIGNED独立保留。精确嵌套比例只有用户提供，本轮未取得独立audit原件。新表尚未进行venue版面排版；用户本轮只要求Markdown/CSV与干验证，未宣称PDF视觉核验。旧builds审校件仍是历史版本，当前以作者源为准。本轮到此停止。
