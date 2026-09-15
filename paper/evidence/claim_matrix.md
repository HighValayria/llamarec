# 段落与可用措辞

证据 ID 在 `source_of_truth.md` 定义。每个正文段落的 `EVIDENCE` 注释使用此 ID；表格保留完整数字，正文按统一精度显示。

| 段落前缀 | 证据 | 允许表述 | 必须保留的限制 | pending |
| --- | --- | --- | --- | --- |
| problem.* / methods.task.* | C1,M1 | 不同监督目标及接口 | N 是 next interaction；非对潜在认知机制的鉴定 | 无 |
| methods.temporal.* | M1 | 用户内按时间桶切分，历史严格早于目标 | Y/N 不同划分；同时间桶无唯一 next item 时跳过该样本 | 无 |
| methods.datasets.* | M8,C8,S29,S30 | MovieLens-1M与Amazon Reviews 2023 5-core Musical Instruments的数据身份及处理后规模 | 外部来源只支撑数据身份/版本；处理后划分和计数由本地证据支撑 | 无 |
| methods.training.* | M2,M3,M4,M9,S26,S27,S28 | 共用底座、QLoRA、响应 token loss、两接口单 adapter；正式run的seed、最终checkpoint、batch/accum与评测路径已有台账 | exact CLI/base revision未留存；M每任务曝光仍为依赖正确resume data skipping的预期值 | 无；RUN_METADATA已RESOLVED |
| methods.exposure.* | M3,C3,C7 | task-sample exposure 为累计消耗样本 | 非 unique interactions / compute；M 每任务为预期调度计数 | 无 |
| methods.baseline.* | M7,M9,C7,S08 | SASRec的64维、2头、2层、FFN 256、GELU、dropout 0.2、LayerNorm、dot-product+bias评分、AdamW配置及四个预设独立训练运行点 | 只对齐下游task-sample exposure；不对齐预训练、token、步数、FLOPs、时间、硬件、延迟、参数或计算资源 | 无；SASRec disclosure已RESOLVED |
| methods.evaluation.* | M4,M5,M10,C10 | fixed candidates、评分接口与M1-N cross-task-safe evaluation-side restriction；共同subset用于seed42 48k/96k | PopMatch用全序列流行度；协议非嵌套；不得称训练采用joint cutoff | 无；clean协议已整合 |
| methods.statistics.* | M6,M10,C4,C10,S31 | seed42既有Y侧user-paired percentile CI；clean-subset排序三seed描述统计 | n=3/ddof=1非CI；clean ranking未重新bootstrap；exact shell invocation未留存边界保持 | 无；clean稿件同步已完成 |
| results.rq1.* | C1,C2,C8 | 偏好判别与 next-interaction ranking 的行为差异 | Y-as-ranker 为桥接；不证明单一语义因素的因果机制 | 无 |
| results.rq2.* | C2,C3 | seed42 在被测曝光点的响应 | 不比较 AUC/HR 绝对尺度；不说收敛 | 无 |
| results.rq3.* | C4,C10 | common cross-task-safe validation上seed42 48k到96k三指标收窄；96k三seed均保留小幅N优势；M1-Y保持观察仍由C4支持 | 48k仅seed42；96k仅运行点复现；test不复现收窄；无等价/正迁移 | 无；clean证据已整合 |
| results.rq4.* | C10 | 96k cross-task-safe三seed两split各指标N>M；k20差距最大，k5/k50较小 | k5与k50相对大小依metric/split变化；协议非嵌套；非纯size因果；仅描述统计 | 无；clean证据已整合 |
| results.rq5.* | C7 | 约相同样本曝光的四个点 N 较强 | 单 seed 曲线；SASRec 实现/预训练/计算不等价 | 无 |
| results.amazon.* | C8 | Amazon的Base、Y-as-ranker、N与SASRec旧点排序方向 | seed42、冻结test外部证据；M1未获cross-task-safe认证而退出active表述 | 无 |
| discussion.* | C1-C10及相关M证据 | 解释接口、曝光、协议与模型比较的意义 | M1-N仅使用cross-task-safe证据；不新增机制、普遍定律或全留出M1结果 | 无；clean证据已整合 |
| limitations.* | C1-C10及相关M证据 | 集中说明训练、评估、跨域、计算范围 | 说明evaluation-side restriction、保留人群、非joint cutoff、48k单seed、ranking无bootstrap及Amazon M1未认证 | 无；clean证据已整合 |

验证与测试的区别是选择纪律，不是科学证据优先级。各段先写发现，再写必要边界；审计层的禁用措辞不直接复制进正文。

禁止升级为：跨 seed 等价、multitask positive transfer、M1 全面优于专家、LLM 普遍胜 SASRec、纯 candidate-size effect、N200 fully converged。统计方向、效应大小、置信区间和训练 seed 覆盖必须一起审查。

## 96k措辞验收

对应数值及来源见 [MS96摘要](ms96_integration_summary.md)。contributions.p02与intro.p06分开写seed42验证轨迹、43/44运行点复现；contributions.p03只把明显更大优势归于k20，不概括为所有alternative协议。C2主/C4次/C3支撑/C1界定的贡献层级不变；finding证据ID的同名字母不是贡献排序。
