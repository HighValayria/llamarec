# 最终声明强度映射

原文裁决：2026-09-07；正文应用核对：2026-09-08。本表的C1-C4是**贡献编号**；实验finding C1-C9见source_of_truth.md，二者不要混淆。文献新颖性与实验强度独立判断，“主贡献”不等于已跨seed验证。

| Claim | Literature novelty | Empirical strength | Manuscript role | Allowed wording | Forbidden wording |
| --- | --- | --- | --- | --- | --- |
| Y vs N capability distinction | 任务区分已有P5/ITDR先例；本文完整形式的具体画像有经验价值 | 契约+seed42原生/桥接观察；Amazon只有排序方向 | C1 framing，短 | Different supervision formulations define distinct prediction questions and observed capability profiles. / 不同监督形式定义不同预测问题和可观测能力画像 | first preference-vs-next-item distinction；语义单因素导致差异；P5与本文所有任务细节完全一样 |
| Y/N exposure response | 数据量与重复训练已有先例；具体目标在本设置的响应是观测贡献 | Y24/48/96k收益有限且非所有指标单调；N24/48/96/200k继续改善；单seed | 支撑C2的轨迹背景 | In the evaluated MovieLens range, measured Y gains weaken while N ranking continues to improve. / 被测区间内Y增益减弱、N排序继续改善 | Y已收敛；N无限缩放；AUC/HR跨尺度绝对能力比较；数据量研究首创 |
| specialist-vs-M exposure conditioning | C2最强候选；P5专家对照+数据量、Penha辅助量曲线、ITDR/Open部分联合须承认 | 既有seed42每任务对齐观察与用户级区间；M计数为调度预期；标准k5 validation差距缩小，test有N优势 | C2 primary，最长 | Higher matched per-task exposure substantially narrows the specialist-multitask gap on standard k5 validation; the frozen test set retains a modest N advantage. / 更高每任务对齐曝光缩小k5验证差距，冻结测试仍有N小幅优势 | first data-aware specialist comparison；P5 budgets unmatched；跨seed稳定；等价性已证；M全面优于专家 |
| candidate protocol sensitivity | 一般敏感性已知；具体C2结论的协议边界为支撑性实证 | 同一冻结高曝光模型在非嵌套协议下N仍有优势；不隔离组成与数量 | C3 supporting | A small standard-k5 validation gap coexists with larger gaps under the evaluated harder candidate conditions. / 标准k5验证的小差距与被测较难条件中的更大差距并存 | candidate size causes gap；单调gap law；first hard evaluation；PopMatch新方法；gap增长框架首创 |
| N-vs-SASRec exposure trajectory | TALLRec已有同K选样预算对照及曲线；不同计量轴不能比倍数 | seed42四点约对齐累计N任务消费，24k-200k内N较强且SASRec改善；非成本匹配 | C4 secondary | Across four approximately matched downstream exposure points from 24k to 200k, N retains a ranking advantage while SASRec improves with additional supervision. / 四个近似对齐下游曝光点上N较强且SASRec继续改善 | first fair/budget-matched comparison；200k/256倍跨度；LLM总成本更低；SASRec已反超或必将反超；N200收敛；基线loss攻击 |
| three-axis joint framing | 部分联合已有；完整领域排他性未证明，不作first | 多个相互关联比较，非三因子全交叉或机制隔离 | 中心组织；MINOR_REVISE | Existing work covers partially overlapping questions; we examine model relationships under explicit cumulative supervision and candidate conditions. / 从部分重合研究出发考察明确监督与协议条件下的模型关系 | largely in isolation；never studied together；no prior work；广泛检索证明交叉处为空 |

## 文献到证据的对齐

- C1：S02 §3、S15 §3是实质任务先例；S06/S07/S08是目标定义基础。PerRecBench未升级原文核验，不用其替代已核来源。
- C2：S02 §5.6与Appendix C、S25 §7 Fig4、S15 §4.3、S21 §6.3.2/B.5是必要近邻。差异在具体目标任务累计计量及关系轨迹，不否认前人数据分析。
- C3：S10/S11/S12支持有限采样/模型次序命题；S16 §3.3支持已有LLM困难候选。S05只用于零样本排序主题。
- C4：S03 §3支持few-shot选样对照；S23 §IV.C承认重复训练先例；S13/S14只支持基线调优背景，不替代曝光论证。
- 本文数值一律来自既有C1-C9/M1-M8；外部论文不能补造本研究seed覆盖、CI、Amazon曲线或机制证据。

## 六个正文缺口的最终处理

| Label | Evidence Status | Manuscript Status | 处理依据 |
| --- | --- | --- | --- |
| JOINT_CONDITIONING_COVERAGE | PARTIALLY_RESOLVED（领域穷尽性未证明） | REWRITTEN_AND_RESOLVED | 删除存在性否定，改为有近邻支持的具体正向研究问题 |
| INSTRUCTION_TASK_DETAILS | RESOLVED | RESOLVED_WITH_CITATION | P5/TALLRec/InstructRec具体接口 |
| RATING_TARGETS | RESOLVED | RESOLVED_WITH_CITATION | Koren已观测评分、Hu隐式置信度、SASRec下一物品 |
| UNIFIED_TASK_ALLOCATION | RESOLVED | REWRITTEN_AND_RESOLVED | P5/ITDR/OpenOneRec明确部分联合；Penha补具体近邻 |
| SAMPLING_EFFECT_DETAILS | RESOLVED | REWRITTEN_AND_RESOLVED | 限定次序敏感性，纠正target set，承认InstructRec |
| EXPOSURE_BUDGET_COMPARISONS | RESOLVED | REWRITTEN_AND_RESOLVED | 承认TALLRec选样曲线及重复训练，区分累计消费 |

正文关闭标记不意味着所有可能新颖性或书目细节已穷尽。MS96等实验待补标记仍保留，与这六项文献标记无关。

## 当前实证范围更新（R04）

2026-09-08，依据用户批准的R01-R09计划同步。**本节覆盖原表和末段中旧的MS96待补、笼统跨seed限制及hard条件差距更大表述；上方原文保留为历史裁决。** 只更新实证强度、适用措辞和状态，不改变文献近邻、创新等级、首创性裁决、贡献角色或Core Thesis。

- MS96为INTEGRATED，Y96_STATUS已解决。运行元信息、bootstrap原预测/执行来源及其他独立缺口仍按pending_evidence保留，不因运行点复现而关闭。
- 原表specialist-vs-M行：完整曝光轨迹仍仅seed42；48至96k标准k5差距收窄仅指validation。seed43/44独立复现96k小差距运行点，三训练seed的冻结test仍保留N的小幅优势。原“跨seed稳定”禁语不得用于否认这项有限复现，也不能将其升级为完整多seed曲线或普遍稳定。
- 同一96k运行点的M1保持被测Y侧能力；三seed test点估计略高，seed44 validation Accuracy例外保留。不写等价性已证、M全面胜专家或普遍正迁移。
- 原表candidate protocol行：k20在三个训练seed、两划分、三指标上均显示大于k5的N优势；k50方向一致，但差距小于k20、幅度随seed变化，且不总大于k5。因此原“harder条件中的更大差距”不能概括全部替代协议。三协议非嵌套，数量、组成、采样及难度联合变化，不建立数量因果或单调规律。
- 原表Y/N曝光概括仍服从既有finding C2：Y被测收益有限且指标变化不一致；后一段增量较小具体指验证AUC，不推广为所有指标和测试划分均收益递减。N在其已测范围内继续改善，不作收敛或无限增长外推。
- 正式SASRec四点与Amazon旧seed42排序方向的范围不变。固定seed42的bootstrap与三训练seed的描述变异分别解释，不新增显著性或等价检验结论。

数值及当前范围依据：[MS96摘要](F:/Projects/llamarec/paper/evidence/ms96_integration_summary.md)、[事实来源](F:/Projects/llamarec/paper/evidence/source_of_truth.md)、[段落映射](F:/Projects/llamarec/paper/evidence/claim_matrix.md)。本次没有重新检索文献或调整新颖性判断。
