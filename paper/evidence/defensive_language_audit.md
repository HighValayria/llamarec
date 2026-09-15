# 英中防御性措辞审计

日期：2026-09-06。自动提取指定关键词后逐位置人工分类，不以关键词归零作为质量目标。

## 扫描口径

- 范围：paper/modules 与 paper/modules_parts 的所有 EN/ZH 正文；作者注释、骨架 TODO 和证据文件不计入论文正文。caption 另审。
- English（大小写不敏感、词边界、同一位置按最长优先匹配）：does not、do not、cannot、not establish、not imply、not intended、should not、rather than、without establishing、we do not claim、not a。
- 中文：不能说明、不能证明、不意味着、并不代表、并非、不是、无法、不应解释为。
- 每次出现单独计数，同一段多个匹配分别登记。旧行号对应本轮开始时快照，新位置以稳定段落 ID 和当前行号定位。匹配不是“错误”判定。
- 初稿关键词命中 55 处（EN 42，ZH 13）；修订后含新增 Discussion/Limitations 共 8 处（EN 5，ZH 3）。八类语义处理见 narrative_revision_log.md。
- 旧匹配分类：REMOVE 5；REWRITE 25；MOVE_TO_LIMITATIONS 18；MOVE_TO_DISCUSSION 5；KEEP 2。
- 关键词外，人工检查了“仅报告测试”、无新架构重复声明、目录/别名审计语言、长串限制和隐性审稿人对话，见段落质量审计。

## 原稿逐出现位置

| # | 原位置（文件:行；段落） | 语言 / 匹配 | 分类 | 处理与去向 |
| --- | --- | --- | --- | --- |
| 1 | paper/modules/03_problem_formulation.md:27；problem.p02 | EN / rather than | REMOVE | 直接保留实证研究定位；删除架构/潜在机制的反衬。 |
| 2 | paper/modules/06_results.md:14；results.p01 | EN / rather than | REWRITE | 改成验证用于决策、测试参与最终解释，见 results.p01。 |
| 3 | paper/modules_parts/methods/baseline_setup.md:15；methods.baseline.p01 | EN / rather than | REWRITE | 以本地实现与训练条件正面界定 SASRec，见 methods.baseline.p01。 |
| 4 | paper/modules_parts/methods/baseline_setup.md:19；methods.baseline.p01 | ZH / 并不代表 | REWRITE | 同一实现范围改为直接陈述，不枚举所有可能变体。 |
| 5 | paper/modules_parts/methods/baseline_setup.md:26；methods.baseline.p02 | EN / does not | MOVE_TO_LIMITATIONS | 服务延迟、吞吐和成本范围集中至 limitations.compute.p01。 |
| 6 | paper/modules_parts/methods/bootstrap_and_statistics.md:26；methods.statistics.p02 | EN / does not | REWRITE | 等价性解释压为 methods.statistics.p02 一句；详细范围集中至 limitations.evaluation.p01。 |
| 7 | paper/modules_parts/methods/bootstrap_and_statistics.md:26；methods.statistics.p02 | EN / do not | MOVE_TO_LIMITATIONS | 多重性推断范围集中至 limitations.evaluation.p01。 |
| 8 | paper/modules_parts/methods/bootstrap_and_statistics.md:30；methods.statistics.p02 | ZH / 不意味着 | MOVE_TO_LIMITATIONS | 中文多重性边界同样集中至 limitations.evaluation.p01。 |
| 9 | paper/modules_parts/methods/bootstrap_and_statistics.md:38；methods.statistics.p03 | EN / not establish | MOVE_TO_LIMITATIONS | 96k 与整曲线覆盖区分集中至 limitations.training.p01。 |
| 10 | paper/modules_parts/methods/datasets.md:19；methods.datasets.p01 | ZH / 并非 | REWRITE | 直接说明不同任务规则产生不同样本群体。 |
| 11 | paper/modules_parts/methods/datasets.md:26；methods.datasets.p02 | EN / do not | MOVE_TO_LIMITATIONS | Amazon 未覆盖的曲线、hard 与偏好复现集中至 limitations.cross_dataset.p01。 |
| 12 | paper/modules_parts/methods/evaluation_protocol.md:25；methods.evaluation.p02 | EN / rather than | REWRITE | 回顾性定义保留，改为与在线检索区别的一句 methods.evaluation.p02。 |
| 13 | paper/modules_parts/methods/evaluation_protocol.md:25；methods.evaluation.p02 | EN / without establishing | MOVE_TO_LIMITATIONS | 残余流行度影响集中至 limitations.evaluation.p01。 |
| 14 | paper/modules_parts/methods/evaluation_protocol.md:29；methods.evaluation.p02 | ZH / 并非 | REWRITE | 明确全语料流行度与离线用途，保留科学必要的信息范围。 |
| 15 | paper/modules_parts/methods/evaluation_protocol.md:29；methods.evaluation.p02 | ZH / 不意味着 | MOVE_TO_LIMITATIONS | 中文残余流行度影响集中至 limitations.evaluation.p01。 |
| 16 | paper/modules_parts/methods/evaluation_protocol.md:36；methods.evaluation.p03 | EN / rather than | MOVE_TO_LIMITATIONS | 单因素候选规模边界集中至 limitations.evaluation.p01。 |
| 17 | paper/modules_parts/methods/evaluation_protocol.md:40；methods.evaluation.p03 | ZH / 并非 | REWRITE | 直接说明候选集独立、非嵌套；Methods 保留构造事实。 |
| 18 | paper/modules_parts/methods/exposure_definition.md:14；methods.exposure.p01 | EN / does not | MOVE_TO_DISCUSSION | 曝光与资源效率的区别在 discussion.baseline.p02 解释，测量边界进入 Limitations。 |
| 19 | paper/modules_parts/methods/exposure_definition.md:18；methods.exposure.p01 | ZH / 不意味着 | MOVE_TO_DISCUSSION | 中文同步迁移到 discussion.baseline.p02 与计算范围段。 |
| 20 | paper/modules_parts/methods/exposure_definition.md:25；methods.exposure.p02 | EN / do not | MOVE_TO_LIMITATIONS | 逐样本 trace 缺失集中至 limitations.training.p01；Methods 保留 resume 前提。 |
| 21 | paper/modules_parts/methods/exposure_definition.md:36；methods.exposure.p03 | EN / not a | MOVE_TO_LIMITATIONS | 有限曝光窗口与收敛边界集中至 limitations.training.p01。 |
| 22 | paper/modules_parts/methods/exposure_definition.md:36；methods.exposure.p03 | EN / rather than | REWRITE | 直接写 actual consumed-example counts including short final batch。 |
| 23 | paper/modules_parts/methods/task_definition.md:14；methods.task.p01 | EN / does not | REWRITE | 改为 native 任务与 bridge 评估的正面定义。 |
| 24 | paper/modules_parts/methods/task_definition.md:25；methods.task.p02 | EN / does not | REWRITE | 改为覆盖全部评分等级的完整序列样本构造。 |
| 25 | paper/modules_parts/methods/task_definition.md:25；methods.task.p02 | EN / not a | KEEP | 干扰候选不等于确定负偏好，直接影响 N 任务标签解释。 |
| 26 | paper/modules_parts/methods/task_definition.md:29；methods.task.p02 | ZH / 不是 | REWRITE | 中文改成“不是已确认的负偏好”，保持关键语义而非重复目标定义。 |
| 27 | paper/modules_parts/methods/task_definition.md:36；methods.task.p03 | EN / rather than | REWRITE | 直接写 M1 总曝光为两个任务之和；每任务匹配照常定义。 |
| 28 | paper/modules_parts/methods/task_definition.md:40；methods.task.p03 | ZH / 并非 | REMOVE | M-Y/M-N 已定义为接口，删除新增预测头反衬。 |
| 29 | paper/modules_parts/methods/temporal_split.md:25；methods.temporal.p02 | EN / does not | REWRITE | 以合法 N 目标的正面条件说明唯一下一物品。 |
| 30 | paper/modules_parts/methods/temporal_split.md:25；methods.temporal.p02 | EN / do not | REWRITE | 说明多交互桶跳过目标但保留历史事件。 |
| 31 | paper/modules_parts/methods/temporal_split.md:29；methods.temporal.p02 | ZH / 无法 | REWRITE | 中文同步改为合法桶定义，时间规则完整保留。 |
| 32 | paper/modules_parts/methods/training_setup.md:15；methods.training.p01 | EN / rather than | REMOVE | 保留七类投影列表，删除嵌入/输出头反衬句。 |
| 33 | paper/modules_parts/methods/training_setup.md:26；methods.training.p02 | EN / rather than | REWRITE | 直接说明 prompt/padding 被 mask 与 response-only loss。 |
| 34 | paper/modules_parts/methods/training_setup.md:37；methods.training.p03 | EN / rather than | REWRITE | 直接说明 allowed-answer likelihood 评分。 |
| 35 | paper/modules_parts/methods/training_setup.md:37；methods.training.p03 | EN / rather than | REWRITE | 直接说明完整多 token 答案 log-likelihood。 |
| 36 | paper/modules_parts/methods/training_setup.md:49；methods.training.p04 | EN / rather than | REMOVE | 删除历史别名对照；累计步数与曝光足以标识检查点。 |
| 37 | paper/modules_parts/methods/training_setup.md:49；methods.training.p04 | EN / do not | REWRITE | 直接说明固定候选比较和验证/测试决策顺序。 |
| 38 | paper/modules_parts/results/cross_dataset_validation.md:25；results.amazon.p02 | EN / rather than | MOVE_TO_LIMITATIONS | Amazon 的运行点及未复现高曝光范围集中说明。 |
| 39 | paper/modules_parts/results/cross_dataset_validation.md:29；results.amazon.p02 | ZH / 并非 | MOVE_TO_LIMITATIONS | 中文同步集中；Results 先保留重现的排序方向。 |
| 40 | paper/modules_parts/results/rq1_supervision_semantics.md:14；results.rq1.p01 | EN / does not | REWRITE | 以能力结构差异为中心句，先给 native 与 ranking 结果。 |
| 41 | paper/modules_parts/results/rq1_supervision_semantics.md:25；results.rq1.p02 | EN / should not | MOVE_TO_DISCUSSION | native 效用与下一事件选择的区别在 discussion.semantics.p01 正面解释。 |
| 42 | paper/modules_parts/results/rq1_supervision_semantics.md:29；results.rq1.p02 | ZH / 不应解释为 | MOVE_TO_DISCUSSION | 中文同步解释任务适用性，去掉假想失败质疑。 |
| 43 | paper/modules_parts/results/rq2_exposure_response.md:14；results.rq2.p01 | EN / rather than | REWRITE | 直接列出 F1 的实际变化，不再用反衬句。 |
| 44 | paper/modules_parts/results/rq2_exposure_response.md:14；results.rq2.p01 | EN / without establishing | MOVE_TO_LIMITATIONS | Y 后续行为与收敛未定集中至训练范围。 |
| 45 | paper/modules_parts/results/rq2_exposure_response.md:25；results.rq2.p02 | EN / rather than | MOVE_TO_LIMITATIONS | 单 seed 曲线范围集中至 limitations.training.p01；Results 开头保留 seed42。 |
| 46 | paper/modules_parts/results/rq2_exposure_response.md:29；results.rq2.p02 | ZH / 并非 | MOVE_TO_LIMITATIONS | 中文曲线复现边界同步集中。 |
| 47 | paper/modules_parts/results/rq2_exposure_response.md:36；results.rq2.p03 | EN / not a | KEEP | 跨指标只比响应形态的说明直接影响解读，压缩保留。 |
| 48 | paper/modules_parts/results/rq2_exposure_response.md:36；results.rq2.p03 | EN / do not | MOVE_TO_LIMITATIONS | 有限测量区间及覆盖/优化共同变化集中至训练范围。 |
| 49 | paper/modules_parts/results/rq3_multitask_unification.md:16；results.rq3.p01 | EN / rather than | MOVE_TO_LIMITATIONS | 等价/非劣效边界由统计方法与评估局限统一承担；结果写实际效应。 |
| 50 | paper/modules_parts/results/rq3_multitask_unification.md:28；results.rq3.p02 | EN / do not | REMOVE | 重复等价性提醒由 methods.statistics.p02 统一承担。 |
| 51 | paper/modules_parts/results/rq3_multitask_unification.md:40；results.rq3.p03 | EN / does not | REWRITE | 直接写很小 validation gap 与正向 test gap，保留分 split 含义。 |
| 52 | paper/modules_parts/results/rq4_hard_candidate_robustness.md:15；results.rq4.p01 | EN / does not | REWRITE | 以 hard-k20 的专家优势为中心句，后接数据。 |
| 53 | paper/modules_parts/results/rq4_hard_candidate_robustness.md:38；results.rq4.p03 | EN / rather than | REWRITE | 改为协议关系及非嵌套共同变化；k20/k50 大小对照保留在 p02。 |
| 54 | paper/modules_parts/results/rq4_hard_candidate_robustness.md:38；results.rq4.p03 | EN / does not | MOVE_TO_LIMITATIONS | 单因素因果边界集中至 limitations.evaluation.p01。 |
| 55 | paper/modules_parts/results/rq5_sasrec_exposure.md:25；results.rq5.p02 | EN / rather than | MOVE_TO_DISCUSSION | 资源和模型系列比较在 discussion.baseline.p02 解释；Results 留一句监督非计算匹配。 |

## 修订后逐出现位置

以下全部为 KEEP，理由是它们改变任务定义、统计解读或结论范围；没有以此作为整段防御的中心。

| # | 当前位置（文件:行；段落） | 语言 / 匹配 | 分类 | 科学必要性 |
| --- | --- | --- | --- | --- |
| 1 | paper/modules_parts/methods/task_definition.md:25；methods.task.p02 | EN / not a | KEEP | 干扰候选不等于已确认负偏好，属于任务定义的必要区别。 |
| 2 | paper/modules_parts/methods/task_definition.md:29；methods.task.p02 | ZH / 不是 | KEEP | 干扰候选不等于已确认负偏好，属于任务定义的必要区别。 |
| 3 | paper/modules_parts/methods/evaluation_protocol.md:25；methods.evaluation.p02 | EN / rather than | KEEP | 回顾性离线控制与在线检索用途不同，直接影响外推。 |
| 4 | paper/modules_parts/methods/bootstrap_and_statistics.md:27；methods.statistics.p02 | EN / rather than | KEEP | 跨零 CI 不承担等价性检验功能，保留一处核心统计解释。 |
| 5 | paper/modules_parts/results/rq2_exposure_response.md:40；results.rq2.p03 | ZH / 不是 | KEEP | 防止跨 AUC/HR 数值尺度比较，正文仅此一处。 |
| 6 | paper/modules_parts/results/rq5_sasrec_exposure.md:25；results.rq5.p02 | EN / rather than | KEEP | 说明样本监督匹配这一比较轴，详细计算范围已集中。 |
| 7 | paper/modules/08_limitations.md:18；limitations.training.p01 | ZH / 不是 | KEEP | 96k 复现与整曲线复现不同，决定训练不确定性范围。 |
| 8 | paper/modules/08_limitations.md:25；limitations.evaluation.p01 | EN / rather than | KEEP | 非嵌套协议不足以单独识别候选规模，保留于专门局限性段。 |

## Caption 审查

caption 中的指定词另有两处原稿命中，未计入正文的 55 处统计；修订后为 0。

| 原位置 | 语言 / 匹配 | 分类 | 处理 |
| --- | --- | --- | --- |
| paper/assembly/paper_manifest.yaml:101；cross_dataset | ZH / 并非 | REWRITE | 保留较早运行点身份，删除“并非96k”反衬。 |
| paper/assembly/paper_manifest.yaml:111；n_native_exposure | EN / do not | REMOVE | 连线非外推/非收敛的重复说明删除，有限测量范围留在 Limitations。 |


- training_exposure：KEEP，resume 前提和总量/每任务区别决定表的解释。
- binary_exposure、semantics_bridge、exposure_scaling、hard_candidate：REWRITE，删除 test 仅报告的重复措辞，正面列明 validation/test、协议和 seed。
- specialist_multitask：KEEP，配对方向、95% CI 与验证划分必须保留。
- n_vs_sasrec_exposure 表：MOVE_TO_DISCUSSION / REWRITE，资源解释集中到 Discussion 7.5，caption 保留实际比较内容。
- cross_dataset：REWRITE，保留较早运行点这一身份，删除“不是 96k”的反衬。
- n_native_exposure 图：REMOVE，删去连线不估计未测点/不说明收敛的重复声明；范围由 Limitations 统一说明。
- n_vs_sasrec_exposure 图：REWRITE，保留 N-K0 图例对应 N24/N48/N96/N200，删除计算/跨种子区间的重复防御。

原图、CSV 与引用库不因措辞修改而变化。数字/语言一致性由装配器检查，科学解释由逐段审查检查；关键词减少本身不能证明行文质量。
