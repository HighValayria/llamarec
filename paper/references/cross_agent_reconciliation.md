# 跨Agent文献对齐与最终裁决

原文裁决：2026-09-07；整合完成：2026-09-08。状态：裁决已应用到00-02，当前审校入口见../REVIEW_HANDOFF.md。两份输入报告保持原样，均为证据综合而非事实裁判。

优先级：Tier1本轮实际核读原文；Tier2既有带原文定位的VERIFIED记录；Tier3另一报告带节/表/图定位的claim；Tier4元数据/摘要；Tier5综合解释。以下结论的具体URL、版本、章节及纠正理由见[关键原文裁决](primary_source_adjudication.md)。未通读部分不冒充已通读。

| Topic | Codex finding | Claude finding | Agreement | Conflict | Primary-source status | Final decision |
| --- | --- | --- | --- | --- | --- | --- |
| P5 | 确认>=4、next-item接口、专家对照；作者站版本未覆盖衍生数据附录 | 完全相同Y/N；专家预算不匹配；概括无数据扫描，但附录又列r10-200 | 统一任务与专家比较已有先例 | FACT_CONFLICT / VERIFICATION_DEPTH_DIFFERENCE | Tier1 §3/5.6及arXiv v7 Appendix C/Table16 | 有真实r10-200训练实例量消融；修正Codex遗漏与Claude自相矛盾。阈值相同不等于完整任务相同；预算不匹配未经充分证明，不入稿 |
| TALLRec | K-shot曲线及同K含SASRec对照；不等于累计曝光 | matched-budget先例，但称无曝光扫描并建议突出量级优势 | 少样本比较已存在 | SCOPE_DIFFERENCE / INTERPRETATION_CONFLICT | Tier1 §3 Table3/Fig3b | 承认K=1-256曲线；区分选样与累计消费，不比较200k/256量级倍数，不攻击loss |
| ITDR | 多任务删除与数据子集有部分多轴覆盖 | 两轴没有全交叉，末节仅部分核验 | 任务/数据都已有实验 | VERIFICATION_DEPTH_DIFFERENCE；精确定义后NO_REAL_CONFLICT | Tier1 §4.3 RQ2/3/5，Fig3/4b/Table1 | 有分别报告的两类消融，不是完整交叉网格，也不是彼此孤立 |
| InstructRec | 共享指令适配及检索hard候选已核 | 主表未覆盖 | 无直接事实矛盾 | SCOPE_DIFFERENCE | Tier2 §2、§3.3 | 正文用于具体接口及hard先例，不能说LLM推荐缺少hard评价 |
| Penha et al. | 上轮没有覆盖 | 专门/共享近邻，但描述成单点、非LLM微调 | 共享/专门方向相关 | FACT_CONFLICT / VERIFICATION_DEPTH_DIFFERENCE | Tier1 §5/7 Fig4；RecSys2024原文首页 | Flan-T5适配，新增任务每物品上限5/10/50/500；升为C2重要近邻S25；区别目标任务累计曝光与辅助数据上限 |
| OpenOneRec | 显式任务配比、低数据及单/多域比较 | 家族统称低重合、几乎不报配比 | 统一推荐方向一致 | FACT_CONFLICT / SCOPE_DIFFERENCE | Tier1 §3.2.2、§6.3.2 Fig8、B.5 Table15 | 有明确权重及10%/全量单域/多域对照；未确认配对的每任务累计曝光轨迹 |
| OneReason | 域RL专家、统一学生 | 未单独覆盖 | 无直接矛盾 | SCOPE_DIFFERENCE | Tier2 §6.1-6.4 | 可加入域专家近邻；不混同域与Y/N任务专家 |
| OneRec family | 五篇分开：流程、规模、推理混合、开放任务、域专家 | 多数合并为工业架构低重合 | 早期OneRec统一召回排序这一定位相容 | SCOPE_DIFFERENCE | Tier2 S18-22；S21补Tier1 | 各报告独立记录，不把OpenOneRec/OneReason事实反套早期OneRec，也不抹去部分联合 |
| PerRecBench | 未覆盖 | 支撑rating与分组排序区别 | 与C1收窄相容 | VERIFICATION_DEPTH_DIFFERENCE | 当前包缺足够节/表定位，Tier4/5；非本轮Tier1 | 保留候选，不标为已核、不加入技术正文；P5/ITDR足以决定C1边界，停止可选扩检 |
| LLMRank | S05仅已核身份/零样本主题 | 增加候选构成/流行度效应细节 | 身份和方向相容 | VERIFICATION_DEPTH_DIFFERENCE | S05技术细节未升级 | 正文保留零样本背景；hard技术依据用Tier2 InstructRec |
| Krichene & Rendle | 采样不保证保留精确指标的模型次序 | 概括所有指标随候选缩小向AUC | 采样改变比较的方向一致 | SCOPE_DIFFERENCE | Tier2 KDD官方摘要及同作者IJCAI扩展原文 | 使用有限排序命题；不全指标化，不解释本文非嵌套因果 |
| Cañamares & Castells | target set是待评分候选集合，含T_u与N_u | 小target set影响比较 | 实质一致 | NO_REAL_CONFLICT | Tier2 §3定义 | 修掉旧稿“仅采正目标”误读，不把最大候选集合等同无偏真值 |
| Dallmann et al. | full/uniform/pop可能给不同次序 | 相同 | 一致 | NO_REAL_CONFLICT | Tier2 §4-5 | 支撑协议敏感性；20次采样重评不等于20训练seed |
| Dacrema et al. | 2019论文对应1907.06902 | 建议改1911.07698，末节仍待核 | 基线调优主题一致 | FACT_CONFLICT | Tier1两abs身份页 | 两篇相关但不同的论文；保留2019键/1907编号，1911为TOIS2021扩展研究 |
| Rendle/iALS | 2110.14037及正式RecSys2022，基线调优非预算匹配 | 主要方向相同，包内另有编号线索 | 基线比较需审视 | NO_REAL_CONFLICT | Tier2 §3-4/Table2 | 沿用已有准确身份与限定用途，不为旁支编号扩搜 |
| recommendation scaling-law works | 序列研究包括unique池和重复训练；S24为单epoch | 家族概括成仅unique raw data | 数据规模研究已有 | FACT_CONFLICT / VERIFICATION_DEPTH_DIFFERENCE | Tier1 2311.11351 §IV.C/Fig3；S24沿Tier2 | 明确重复训练已有先例，不把一个单epoch研究泛化为整个领域 |
| A supervision formulation novelty | C1为界定与经验能力画像 | 应承认P5等先例 | 一致 | NO_REAL_CONFLICT | P5/ITDR足够支撑收窄 | C1 framing；不是首次区分偏好与下一物品 |
| B specialist-vs-multitask exposure novelty | 具体累计每任务轨迹有研究价值 | 第一主贡献，但部分理由依赖“无数据曲线” | C2重心一致 | INTERPRETATION_CONFLICT | P5/Penha/ITDR/Open直接限制理由 | 保留C2，以目标任务累计监督对齐下关系变化为主，不声称首次数据感知共享比较 |
| C candidate-protocol sensitivity novelty | 具体N/M关系的协议条件；一般规律不新 | 认可一般先例，但称gap增长框架可新 | 一般敏感性不新 | INTERPRETATION_CONFLICT | Tier2评价文献+冻结非嵌套边界 | C3支撑C2；放弃gap增长首创、单调规律、纯大小因果及PopMatch方法创新 |
| D exposure-aware LLM-vs-SASRec novelty | 四个累计消费点，N强且SASRec继续改善 | 首创预算不能写，但建议跨论文量级与loss解释 | few-shot先例必须承认 | INTERPRETATION_CONFLICT / SCOPE_DIFFERENCE | Tier1 TALLRec/序列缩放 | C4第二主贡献，24k-200k本研究轨迹；不偷换K与累计量，不写交叉点已出现 |
| E joint three-axis research gap | 正向具体问题，不证明领域空白 | SAFE/交叉处为空/largely in isolation | 不写first | INTERPRETATION_CONFLICT | 多篇已有部分联合的原文 | REWRITTEN_AND_RESOLVED：从部分重合研究出发，提出具体关系随监督与协议变化的问题 |

## 综合决策

- 中心判断：MINOR_REVISE。保留条件化结论主线，将“LLM推荐中的普遍结论”限定为本研究已评估的推荐调优设置。
- 层级：C2第一主贡献，C4第二主贡献，C3支撑性分析，C1问题与能力界定。
- 原文纠正两边：P5附录是Codex上轮覆盖遗漏；Penha、OpenOneRec、重复训练与Dacrema身份不能照搬Claude概括。不存在按Agent投票。
- 当前未确认足以推翻中心的HIGH完整设计重合；不等于领域唯一性得到证明。组件重合是必须承认的事实，不是削弱或否认先例的理由。
- 不新增架构，不升级PopMatch，不读取新MS96，不以Amazon重现完整曲线；没有新的实验建议或执行。
- 已完成会改变本轮定位的定向补核，停止搜索。剩余书目深度和领域覆盖不阻塞当前有限措辞，仍在引用登记与冻结文件中明示。
