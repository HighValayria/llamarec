# 叙述修订记录

日期：2026-09-06。范围为 03-08 与对应 parts、caption、证据和审校文件。主线仍为 Supervision Semantics Under Exposure；没有新增实验、指标或文献主张。

| location | old issue | revision | reason |
| --- | --- | --- | --- |
| problem.p01；methods.task.p01/p02；methods.temporal.* | full-sequence history 容易被理解为全部历史输入模型 | 定义 H(u,t) 与 H_10(u,t)；完整交互序列负责合法性、时间桶、目标与划分；模型输入最多最近 10 条严格更早交互 | 区分样本构造与实际输入，保留低评分事件 |
| setup.p01；results.p01；methods.baseline.p02；各 caption | validation-first 被写成证据优先级；test 反复被称为 report-only | validation 用于选点、解释检查点和继续训练决策；冻结后报告 test，并用于最终科学解释 | 保留选择纪律，同时赋予测试观察应有的解释作用 |
| results.rq1.p01/p02；problem.p02 | 先否定 Y 排序表现，再连续阻止因果误读 | 先报告 Y 原生偏好判别与 Y/N 排序对照，再明确比较单元是完整监督 formulation | 有效的能力结构发现；不归因于孤立标签位 |
| methods.evaluation.p02 | PopMatch 多次被用于自我辩护 | 一次说明全语料流行度、最近流行度池、固定候选与回顾性离线控制；在线检索区别压成一句 | 保留构造细节和真实信息范围 |
| methods.statistics.p01/p02 | 三段统计说明混合等价性、多重比较、旧 seed 与原始记录问题 | 压为两段：用户配对 percentile CI；评估抽样与训练不确定性；跨零描述性解释 | 方法信息先行，多重性与复现范围集中到 Limitations |
| methods.statistics.p03 | 原段主要承担范围防御 | 撤销该段 ID；训练种子定义并入 p02，MS96 标记移至 p02，整曲线范围移至 limitations.training.p01 | 旧 ID 不复用，保证回填记录可追踪 |
| methods.training.* | all-linear、输出评分和历史别名均采用反驳句式 | 直接列七类投影、response-only loss、完整答案似然、micro-batch 与更新步数 | 保留可复现细节，去掉无新架构/非首 token 等重复辩解 |
| methods.exposure.* | 同一曝光定义旁多次列出不匹配项目 | 保留累计样本、重复消费、M1 总量及预期每任务量、resume 条件、S391 实际计数 | 计算范围集中；实际计数与模型比较可复核 |
| results.rq2.* | 轨迹后堆叠未收敛、未隔离因素和非 scaling law | 突出 Y 增益减弱、N 持续改善；仅一次解释比较响应形态而非指标大小；以曝光对齐转入 RQ3 | 由发现推动后续问题 |
| results.rq3.* | near parity 的辩护过多，test 被写成附属限制 | 同时给出很小的 k5 validation gap 与正向 test gap；以更强的高曝光统一能力概括当前观察 | 不锁定持平，也不否定有意义的接近；保留 MS96/Y96_STATUS |
| results.rq4.* | 整节重心偏向无法证明 candidate-size effect | 先写 hard-k20/k50 的 N 优势及测试一致方向；组成和数量共同变化保留一句 | 把协议敏感性作为结果，单因素边界集中说明 |
| results.rq5.* | N 优势被计算、公平性和系列优越性免责声明冲淡 | 明确四个曝光对齐点 N 均优于被评估 SASRec，且 SASRec 随监督改善、200k 差距缩小 | 保留真实 tension；计算详细讨论移至 Discussion 7.5/Limitations |
| results.amazon.* | 第二数据集先解释没有复现什么 | 先呈现 N 相对 Y-as-ranker、M1、低曝光 SASRec 的排序方向，再交代 MovieLens 负责详细轨迹 | 外部支撑先于范围界定 |
| discussion.* | 仅有骨架 | 新增六节、13 对双语段落，解释接口、曝光、统一、协议、样本效率与外部效度 | Discussion 解释意义，独立于限制清单 |
| limitations.* | 仅有边界注释 | 建立训练、评估、跨数据集、计算与服务四段双语初稿 | 将影响解释的边界集中，而非逐节道歉 |
| paper/assembly/paper_manifest.yaml | caption 含连线非收敛、test 仅报告等重复说明 | 改成模型、协议、划分、曝光与 seed 的内容说明；保留非嵌套、M1 计数条件及 N-K0 旧图例解释 | 图表数值与图片原样保留，减少正文与 caption 的重复 |

## 防御性表达的八类处理

1. 无新架构/无新增预测头的重复定位：改为直接任务与模块定义。
2. Y 较弱桥接排序不等于失败的辩论：改为 native 与 bridge 能力对照，解释进入 Discussion 7.1。
3. 等价/非劣效/校正 p 值的统计串联：保留一句描述性 CI 解释，多重性集中到 Limitations。
4. 单 seed、全曲线与收敛边界：集中到训练不确定性段，Results 仅保留必要 seed 与待补说明。
5. 候选规模、嵌套与流行度边界：Methods 说明构造，Results 简述共同变化，Limitations 集中范围。
6. 样本与计算、预训练、服务成本差异：解释进入 Discussion 7.5，测量范围进入 Limitations。
7. Amazon 未覆盖项目：Methods 保留评估设置，Results 先讲重现方向，Limitations 汇总缺项。
8. 验证/测试与旧别名、内部过程语言：改为选择纪律及正面报告，删除面向审计流程的句子。

逐出现位置的处理见 defensive_language_audit.md；段落的中心句、新信息、位置与推进作用见 paragraph_quality_audit.md。

## 证据变更检查

本轮没有新增数值来源，没有重算任何指标或区间。RQ1 补写的测试排序数值和 RQ5 的测试方向直接来自现有冻结表。未发现新的数值冲突。原有 S391 别名差异、bootstrap 预测链缺口、运行元数据缺口继续按 source_of_truth.md 与 pending_evidence.md 处理。此次修复的是 full-sequence 术语歧义和验证/测试叙述偏差，未改变实验事实。末轮通读还将 RQ3 的“差距缩小”明确限定为验证比较，避免扩写为测试差距也缩小；Discussion 7.5 仅描述预训练起点，不声称单独识别了预训练收益。
