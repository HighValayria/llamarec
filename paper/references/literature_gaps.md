# 文献证据与正文缺口状态

日期：2026-09-08。用户授权的00-02整合已应用。证据状态与正文状态分列；领域穷尽性未被证明，不妨碍将正文改为可支持的具体问题。双语6类CITATION_NEEDED已处理，实验类MS96等不在此表中。

| Gap | Evidence Status | Manuscript Status | Final wording（中文摘要，完整双语见注册表） |
| --- | --- | --- | --- |
| JOINT_CONDITIONING_COVERAGE | PARTIALLY_RESOLVED | REWRITTEN_AND_RESOLVED | 删除对领域覆盖不足的无穷尽依据断言，承认任务、数据和评估的部分重合，提出对应累计监督下关系及候选条件的正向研究问题。 |
| INSTRUCTION_TASK_DETAILS | RESOLVED | RESOLVED_WITH_CITATION | 以P5多任务语言输入输出、TALLRec指令/偏好历史/目标到YesNo、InstructRec多个指令接口替换泛化句。 |
| RATING_TARGETS | RESOLVED | RESOLVED_WITH_CITATION | 引用原文明确区分已观测评分拟合、隐式偏好/置信度和历史到下一物品目标。 |
| UNIFIED_TASK_ALLOCATION | RESOLVED | REWRITTEN_AND_RESOLVED | 承认P5专家及衍生数据量、ITDR分别报告的两类消融、OpenOneRec任务权重及低数据单/多域对照；定位目标任务累计关系。 |
| SAMPLING_EFFECT_DETAILS | RESOLVED | REWRITTEN_AND_RESOLVED | 补限定的模型次序敏感性，纠正target set为待评分候选集合，承认InstructRec已有困难候选；保留非嵌套边界。 |
| EXPOSURE_BUDGET_COMPARISONS | RESOLVED | REWRITTEN_AND_RESOLVED | 承认TALLRec同K选样对照及few-shot曲线、序列模型重复训练；将本文比较明确为四点累计下游消费，不冒充计算公平。 |

## 联合条件缺口的最终句子

EN: Existing studies thus address partially overlapping questions about task formulation, training-data allocation, and candidate evaluation. Building on these connections, we examine how specialist-multitask and LLM-sequential-baseline relationships change with cumulative per-task supervision, and which relationships persist under alternative candidate conditions.

ZH: 因此，已有研究围绕任务形式、训练数据分配和候选评估考察了部分重合的问题。在这些关联的基础上，本文研究专家与多任务模型、LLM与序列基线的关系如何随累计每任务监督变化，以及哪些关系能在不同候选条件下保持。

这不是“找到多篇文献就证明没人做过”；新句承认已有研究并提出具体问题，不需要全领域不存在的前提。原句保留在literature_gap_registry.json的original_claim中。

## 剩余不确定性

- 未证明完整领域唯一性；不写first、never或no prior work。P5、Penha、ITDR、OpenOneRec均有实质部分重合。
- KDD完整PDF未取得；仅使用官方摘要与同作者扩展原文支持的有限次序结论。
- S01/S04/S05为题名主题使用；S09仍PARTIAL且不引用。PerRecBench及LLMRank新增细节未升为已核事实。
- 部分技术报告正式venue未核，保留arXiv身份，不填写猜测的会议。Penha正式RecSys2024身份已核。
- 样本消费与选样池、token、计算、预训练和总成本不等价；不得以不同计量对象按倍数夸大C4。
- MS96、历史运行元信息、统计溯源及Amazon完整曲线仍是独立实验边界；本轮没有读取或更新它们。

## 使用入口

[原文裁决](primary_source_adjudication.md)、[跨Agent对齐](cross_agent_reconciliation.md)、[逐段引用映射](citation_claim_map.md)、[原文定位](primary_source_notes.md)、[声明强度](../evidence/final_novelty_claim_map.md)。

原始两份Agent报告和UNAPPLIED_MANUSCRIPT_EDIT_SNAPSHOT.md保留为历史输入；旧报告中“未应用”的状态不再代表当前作者源。未直接采用旧备份，当前修订由新的原文裁决驱动。检索到此停止。
