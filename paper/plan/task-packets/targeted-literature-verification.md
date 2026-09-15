# 定向文献核验任务包

## 最新范围覆盖原安排

2026-09-07用户后续明确：本轮仅文献证据收集，不修改稿件。原安排中的局部稿件修改已回滚，备份存references/UNAPPLIED_MANUSCRIPT_EDIT_SNAPSHOT.md；综合报告为references/LITERATURE_VERIFICATION_AND_NOVELTY_REPORT.md。下面保留最初任务安排作为来由，任何改稿步骤均不再执行。


日期：2026-09-07。用户附件：b7f8d80f-85b4-4d53-8b6d-7862a4e3f3f8/pasted-text.txt。

## 范围

仅处理JOINT_CONDITIONING_COVERAGE、UNIFIED_TASK_ALLOCATION、SAMPLING_EFFECT_DETAILS、EXPOSURE_BUDGET_COMPARISONS、INSTRUCTION_TASK_DETAILS、RATING_TARGETS。允许primary-source定向检索、引用资产更新、00-02及相关工作parts局部修改。03-08、表图、旧稿和MS96证据不动。

## 检索顺序与停止

1. 先核P5、TALLRec、SASRec、Krichene、Cañamares、Dallmann、Dacrema、iALS原文。
2. 先回答P0联合条件覆盖，再查统一/多任务与准确OneRec身份；已有评估论文提供采样原文证据。
3. 再查直接下游数据预算比较，补最多1-3篇接口代表作，核Koren/Hu历史目标。
4. 每次查询绑定具体缺口。近邻表覆盖最相关5-10篇，不把全领域“没人做过”作为证明目标。
5. 新文献以10-20篇高相关候选为参考范围，不为数量补库。满足可引用定位及统一/采样/预算原文覆盖即停。
6. 如一篇同时覆盖相近Y/N任务、共享多任务LLM、匹配每任务预算及候选协议鲁棒性，立即写HIGH冲突报告并停止，等待用户判断。

## 作者源与证据

沿用7段引言和四主题相关工作蓝图，不改问题链。原文每篇提取1-3条定向事实并记录准确章节/表格/页码或原文定位；记录身份、作者、年份、venue/arXiv、URL/DOI与核验范围。没有读到的细节记未确认，不凭摘要反推全套训练配置。

先形成landscape与句子证据映射，再改正文。六个占位句分别决定RESOLVED_WITH_CITATION、REWRITTEN_TO_SUPPORTED_CLAIM或REMOVED；不得无依据删标记。P0优先改成正向研究问题而不是全领域否定断言。

## 必需产物

references/的citation_inventory、citation_claim_map、literature_gaps、joint_conditioning_landscape、unified_multitask_landscape、evaluation_sampling_evidence、exposure_budget_landscape；必要时novelty_conflict_report。维护结构化引用和缺口注册表、检索记录、证据定位及任务状态。仅重建独立审校件，不拼整篇。

## 拒绝条件

二手摘要代替原文；将唯一样本数等同累计曝光；将步骤/算力/预训练预算视为样本匹配；用非嵌套hard结果推纯候选大小因果；升级跨seed措辞；把统一任务接口本身包装为新方法；未授权实验或Wiki访问。

## 核验与审查

沿用装配/冻结证据/文献资产测试，按引用注册表扩展所需契约；检查每条新引文有对应缺口、每个正文引用有具体支持、中英一致、MS96不变、51项保护文件哈希不变。执行git diff --check与stage_guard。完成范围审查和科学定位审查后按用户14项清单汇报并停止。
