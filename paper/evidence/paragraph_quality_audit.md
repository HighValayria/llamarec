# Results / Discussion 逐段质量审查

日期：2026-09-06。对 29 对双语段落逐一检查中心、新信息、位置与推进作用；没有仅为“防止误解”而保留的独立段落。此表记录人工判断，不把关键词检索当作论文质量的替代。

| 段落 ID | 中心句/中心判断 | 新信息 | 为什么在这里 | 如何推进论证 |
| --- | --- | --- | --- | --- |
| results.p01 | 研究结果沿接口、曝光和评估条件展开。 | 明确验证的选择职责与测试的解释职责。 | Results 入口，规定阅读路径。 | 建立共同坐标，避免把 test 降为附属数字。 |
| results.rq1.p01 | Y 与 N 对应不同能力结构。 | 给出 native 偏好指标和验证/测试排序对照。 | 先建立待解释的经验现象。 | 用能力分化引出监督形式。 |
| results.rq1.p02 | 喜欢与下一交互回答不同问题。 | 比较单位是包含目标、数据、提示和评分的完整 formulation。 | 承接数据，界定经验发现。 | 从能力差异过渡到曝光响应。 |
| results.rq2.p01 | Y 的额外收益减小。 | AUC 增量减弱，F1 波动，bridge 排序变动小。 | 先观察偏好侧响应。 | 构成与下一段 N 的对照。 |
| results.rq2.p02 | N 在已测范围持续改善。 | 四个点及 test 同向轨迹。 | 与 Y 对照而非孤立列数。 | 说明早期检查点不足以代表后期状态。 |
| results.rq2.p03 | 两种响应形态不同。 | 曝光点会影响模型差距的解释。 | 收束双任务轨迹。 | 把问题推进到每任务曝光对齐的统一比较。 |
| results.rq3.p01 | 高曝光 M1 接近专家并保留偏好能力。 | M-Y/Y96 的效应与三个 CI。 | 先确认双接口中的偏好侧。 | 为同时看排序侧建立基础；未宣称 positive transfer。 |
| results.rq3.p02 | 标准 k5 验证差距随曝光明显缩小。 | 48k 与 96k 对照，三个零跨区间。 | 量化统一能力的变化。 | 先形成接近观察，再由 test 检验其范围。 |
| results.rq3.p03 | 冻结 test 仍保留小幅 N 优势。 | 正向 test CI 与 M-Y test 表现。 | 与 validation 共同得出当前解释。 | 提出较难候选问题；保留 MS96，不锁定持平。 |
| results.rq4.p01 | Hard-k20 显示明显专家优势。 | 三项效应与正向区间。 | 直接检验上一节留下的协议问题。 | 呈现标准协议之外的差距。 |
| results.rq4.p02 | Hard-k50 同样偏向 N。 | 较小 gap、两种 hard test 同向。 | 检验额外候选条件。 | 强调跨已测协议的优势而非 gap 随 k 单调增加。 |
| results.rq4.p03 | 模型关系依赖候选协议。 | 共同改变组成/数量这一解释条件。 | 提炼协议结果，不新增机制。 | 从评估条件过渡到基线的训练条件。 |
| results.rq5.p01 | 四个曝光匹配点 N 排序更高。 | 验证原值、差值及所有 test 同向。 | 回答监督量对齐后的基线比较。 | 先正面建立有限任务监督下的优势。 |
| results.rq5.p02 | SASRec 随额外监督显著改善。 | 200k gap 缩小和独立旧高曝光方向。 | 与 N 优势形成真实 tension。 | 明确样本轴并转入跨数据集检验。 |
| results.amazon.p01 | 主要排序方向在 Amazon 再现。 | N/Y/M/SASRec test 原值及小 N-M margin。 | 外部检验首先报告复现内容。 | 将关键排序发现带到第二领域。 |
| results.amazon.p02 | Amazon 支撑排序方向，MovieLens 支撑详细轨迹。 | 给出两个数据集的证据分工。 | 收束 Results。 | 自然进入含义讨论，缺项细节留给 Limitations。 |
| discussion.p01 | 解释推荐表现需要接口、曝光与协议三个条件。 | 将结果组织为可解释的比较框架。 | Discussion 入口。 | 从“是什么”转向“意味着什么”。 |
| discussion.semantics.p01 | 推荐能力应对应具体预测问题。 | native 效用与下一事件选择各有任务含义。 | 先解释研究主线。 | 将 Y/N 分化提升为能力定义问题，无潜在模块推测。 |
| discussion.semantics.p02 | 监督 formulation 属于基准解释的一部分。 | native 加 bridge 报告揭示能力关系。 | 承接能力定义。 | 提出由结果支撑的评估报告启示。 |
| discussion.exposure.p01 | 比较落在适配轨迹的具体位置。 | 早期点与后期点的关系依任务而变。 | 解释曝光响应的重要性。 | 将曝光提升为主要实验变量。 |
| discussion.exposure.p02 | 按任务统计使预算比较明确。 | M1 总量/分任务、SASRec 实耗各回答不同问题。 | 把观察转为可执行的报告原则。 | 为条件性统一与基线比较搭桥。 |
| discussion.unification.p01 | 专业化和统一的关系随条件改变。 | 将曝光、split、protocol 三种条件联系起来。 | 综合 RQ3/RQ4 的经验关系。 | 解释为什么不能锁定单一专家/多任务排序；MS96。 |
| discussion.unification.p02 | 统一模型的接受标准依任务而定。 | 单 adapter 多接口与不同性能标准分开。 | 从关系解释进入评估含义。 | 明确应测保留多少专家能力，不宣称服务收益；MS96。 |
| discussion.protocol.p01 | 候选条件决定哪些差距可见。 | 同一模型对在不同协议的关系变化。 | 解释 RQ4 的方法学意义。 | 说明单一标准候选集的信息不足；MS96。 |
| discussion.protocol.p02 | 报告协议组合及构造规则更有解释力。 | 协议内配对与跨协议敏感性承担不同职责。 | 将结果转为报告建议。 | 保留联合条件含义，不把规模设为原因；MS96。 |
| discussion.baseline.p01 | N 的下游样本效率与 SASRec 的改善同时成立。 | 区分有限监督表现与继续从监督获益。 | 先解释 RQ5 的正面经验价值。 | 超越单点模型系列排名。 |
| discussion.baseline.p02 | 样本曝光是有用但局部的比较轴。 | 旧高曝光条件和预训练起点进入比较解释。 | 说明效率 finding 的确切含义。 | 资源效率成为不同问题，测量缺口留在 Limitations。 |
| discussion.external.p01 | 核心排序观察延伸到第二领域。 | 明确接口与低曝光基线方向的外部支撑。 | 先解释 Amazon 的贡献。 | 避免把外部验证写成道歉。 |
| discussion.external.p02 | 两个数据集承担互补研究职责。 | 详细条件变化与外部方向检验的分工。 | Discussion 收束。 | 说明进一步跨域主张需要何种对应证据。 |

## 双语与篇幅复核

| 段落 ID | 英文词数 | 中文字符数 | 复核结果 |
| --- | --- | --- | --- |
| results.p01 | 71 | 174 | 中心判断、split/seed 范围及论证作用对应 |
| results.rq1.p01 | 114 | 366 | 中心判断、split/seed 范围及论证作用对应 |
| results.rq1.p02 | 77 | 154 | 中心判断、split/seed 范围及论证作用对应 |
| results.rq2.p01 | 81 | 226 | 中心判断、split/seed 范围及论证作用对应 |
| results.rq2.p02 | 98 | 295 | 中心判断、split/seed 范围及论证作用对应 |
| results.rq2.p03 | 76 | 159 | 中心判断、split/seed 范围及论证作用对应 |
| results.rq3.p01 | 95 | 309 | 中心判断、split/seed 范围及论证作用对应 |
| results.rq3.p02 | 94 | 324 | 中心判断、split/seed 范围及论证作用对应 |
| results.rq3.p03 | 125 | 367 | 中心判断、split/seed 范围及论证作用对应 |
| results.rq4.p01 | 99 | 297 | 中心判断、split/seed 范围及论证作用对应 |
| results.rq4.p02 | 105 | 338 | 中心判断、split/seed 范围及论证作用对应 |
| results.rq4.p03 | 54 | 108 | 中心判断、split/seed 范围及论证作用对应 |
| results.rq5.p01 | 107 | 366 | 中心判断、split/seed 范围及论证作用对应 |
| results.rq5.p02 | 82 | 228 | 中心判断、split/seed 范围及论证作用对应 |
| results.amazon.p01 | 103 | 354 | 中心判断、split/seed 范围及论证作用对应 |
| results.amazon.p02 | 71 | 158 | 中心判断、split/seed 范围及论证作用对应 |
| discussion.p01 | 70 | 142 | 中心判断、split/seed 范围及论证作用对应 |
| discussion.semantics.p01 | 80 | 141 | 中心判断、split/seed 范围及论证作用对应 |
| discussion.semantics.p02 | 68 | 138 | 中心判断、split/seed 范围及论证作用对应 |
| discussion.exposure.p01 | 71 | 151 | 中心判断、split/seed 范围及论证作用对应 |
| discussion.exposure.p02 | 71 | 151 | 中心判断、split/seed 范围及论证作用对应 |
| discussion.unification.p01 | 74 | 164 | 中心判断、split/seed 范围及论证作用对应 |
| discussion.unification.p02 | 75 | 181 | 中心判断、split/seed 范围及论证作用对应 |
| discussion.protocol.p01 | 68 | 177 | 中心判断、split/seed 范围及论证作用对应 |
| discussion.protocol.p02 | 60 | 136 | 中心判断、split/seed 范围及论证作用对应 |
| discussion.baseline.p01 | 78 | 169 | 中心判断、split/seed 范围及论证作用对应 |
| discussion.baseline.p02 | 76 | 181 | 中心判断、split/seed 范围及论证作用对应 |
| discussion.external.p01 | 61 | 156 | 中心判断、split/seed 范围及论证作用对应 |
| discussion.external.p02 | 72 | 147 | 中心判断、split/seed 范围及论证作用对应 |

- RQ1 的“能力结构”对应 observed capability profiles；英文未使用 isolated semantics causes 的因果表述，中文也未作该归因。
- RQ3 两种语言均保留 validation gap 很小与 test 的 N 优势，未把跨零 CI 写成持平证明。
- RQ4 两种语言均按协议解释差距，未改写成候选规模的单因素机制。
- RQ5 的 sample efficiency 指给定预训练起点的下游任务监督量；资源效率的含义另行说明。
- Amazon 先报告重现方向，完整曲线/hard/native binary 范围集中处理。
- Discussion 的推论属于对现有结果的解释与报告建议，不宣称已经验证模型内部机制、普遍定律或新架构。
- MS96 与 Y96_STATUS 保留在作者注释；待补元数据和书目不以推测填充。
