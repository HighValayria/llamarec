# 跨Agent文献对齐与稿件整合任务包

日期：2026-09-07。用户附件553fc228-2e0a-463d-8e2b-ee2e1e0e12fb/pasted-text.txt授权本轮修改00-02。本轮覆盖此前仅证据收集限制，不授权其他写作或实验工作。

## 工作顺序

先完整读取Codex与Claude报告，再核已有映射，生成逐项对齐；只对决定定位的冲突补核原文。之后冻结中心判断与C2/C4/C3/C1层级，更新段落蓝图和证据覆盖，再分别修订贡献、引言、相关工作。最后作范围和科学叙事两轮审查。

## 输入与优先级

Tier1本轮实际核读原文，Tier2既有带定位VERIFIED记录，Tier3Claude带定位原文claim，Tier4元数据/摘要，Tier5综合判断。两套报告都不是事实裁决源，不按Agent数量投票。保留两份输入和旧建议备份原样。

## 允许与冻结

允许references、00-02、相关work parts、相关论证图、三份新冻结/对齐文件及必要测试/工作记录。固定7段引言、四主题相关工作及4段贡献，逐段EN/ZH和ID不变。保留14处MS96，尤其intro.p06及contributions.p02/p03。

03-08、09/10骨架、表图、旧稿及输入报告共54项建立hash基线。不训练、推理、读新MS96、改指标或实验、不泛搜、不拼整篇、不访问Wiki、不做venue适配、不运行prepare_assets.py。

## 关键争议与补核阈值

- P5的>=4语义重合是否等于相同完整Y/N；总预算不同是否足以断言每任务不匹配。影响C1/C2。
- TALLRec选样预算及所谓“无曝光扫描”：是否混淆K-shot曲线与累计样本曝光。影响C4。
- ITDR的任务删除与分层数据子集是否交叉；不能以多个轴完全隔离概括。影响gap/C2。
- OpenOneRec显式任务配比与低数据对照对“家族低重合”的纠正。影响gap/C2。
- Penha对新增任务数据与共享/专门模型关系的证据深度，是否可以支持Claude强单点/非LLM论断。直接影响C2定位，必要时仅核其指定Fig.4与模型设置。
- 序列规模文献是否仅unique数据还是也含重复训练。影响C4/曝光定义。
- Dacrema两arXiv编号的真实身份。影响既有正文引用。
- gap变化新颖性、PopMatch首创性、交叉处为空属于解释过强，先用既有Tier2和逻辑边界裁决，不追加泛化搜索。
- PerRecBench/LLMRank等新增细节若无足够原文定位，不以完整核验入稿；优先使用已核近邻，不为扩库补检索。

## 交付

cross_agent_reconciliation；story_and_novelty_freeze；final_novelty_claim_map；00-02双语稿；引用库存/对应/缺口/书目。必要时仅写Discussion后续说明，不动Discussion正文。更新引用注册表和既有检查，不绕过final门禁。保留原始备份，不自动采用其整段。

## 审校与能力审计

既有选题和章节结构由用户明确确定，不重复brainstorming。本任务是三部分局部修订，不是全论文重写，不创建新任务或调用无授权子任务。使用using-research-writing、paper-orchestration、evidence-driven-writing、literature-review、writing-chapters、writing-core和verification。保留用户4项贡献结构，优先于技能通用篇章模板。

范围审查：54项hash、14处MS96、段落ID、引用资产、只读装配。
质量审查：正面但校准的表述、C2主/C4次/C3支撑/C1界定、原文对应、中英一致、无Agent过程污染。
