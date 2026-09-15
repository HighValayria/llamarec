# 引言与相关工作任务包

日期：2026-09-07。沿用用户冻结主线，不重新选故事。

## 范围

- 写00贡献工作版、01引言、02相关工作及所需parts，逐段EN/ZH。
- 引言7段，相关工作4主题加综合定位，贡献4段。
- 更新citation_inventory、literature_gaps、citation_claim_map、引言论证图、相关工作定位。
- 补充CITATION_NEEDED的final拦截和针对性测试；只生成独立章节审校件。
- 03-08、其parts、图表、library.bib及旧稿均只读，52项hash作为保护基线。
- 不训练、推理、轮询MS96、重算指标、联网搜文献、读Wiki、写结论/摘要/最终题名或拼完整稿。

## 证据职责

旧verified_sources.md仅证明此前CrossRef书目身份与题名级核验，evidence-map中的延伸判断逐项重新收紧。VERIFIED限定到具体可用claim，不代表全文已读。无法确认的技术结论、覆盖范围和新颖性使用CITATION_NEEDED并进入gaps。

## 段落角色

- Introduction：研究背景、预测目标歧义、曝光预算、评估与联合缺口、研究设计、主要发现、贡献综合。
- Related Work：LLM推荐、任务形式、多任务统一、评估与基线；段落按方向/依据/与本文关系组织。
- Contribution：监督形式、曝光条件化行为、协议敏感性、曝光感知SASRec；Amazon不单列。

## 拒收条件

- 题名级证据被升级成具体实验结果或首创结论。
- 验证gap缩小被扩写成test也缩小，或MS96尚未完成却写跨seed持平。
- Related Work只列论文、Introduction复述实验流水账。
- 用CITATION_NEEDED绕过final，或单语输出隐藏了待补标记。
- 英中引用键、数字、论证强度不对应。

## 核验与交付

使用evidence-driven-writing、literature-review、paper-orchestration、writing-core与verification。先建立evidence-map、blueprints和coverage，再写正文。完成范围审查与科学文字审查，运行装配测试、引用映射检查、hash保护、git diff --check和stage_guard。仅交当前工作稿，等待用户审校。
