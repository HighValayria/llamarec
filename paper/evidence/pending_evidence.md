# 证据整合与剩余缺口

## M1_CLEAN_SUBSET：INTEGRATED
2026-09-11。GitHub提交`45fd370`、`bc99dfd`、`cb716b9`中的28个逐样本prediction已拉取；archive及源文件SHA256、字节数、5,675行记录全部通过manifest核验。cross-task-safe subset保留M1-48 validation/test的5,494/5,600条及M1-96的5,318/5,535条。共同subset上的seed42 validation 48k到96k三指标均收窄，test三指标均不收窄。96k三seed、两split、三协议的54个seed级差值全部为正，18个汇总项均为3/3正向；这是描述统计，未重新bootstrap。正式稿件已将Tables IV-VII、Methods、RQ3/RQ4及必要依赖段落切换到该证据，旧M1-N ranking CI不再active。Amazon M1未获同口径认证，已从active跨数据集表述和表格移除。完整裁决见[恢复闭环](../plan/task-packets/m1-clean-subset-recovery-closure.md)。

## MS96：INTEGRATED
2026-09-08。seed43/44的Y96、N96、M1-96 validation/test及k20/k50结果已从固定Git提交a9c6cd959cf32afe046bb05be9eb5096bebfc5fb导入，八份文本规范化blob核对一致。seed42采用原冻结值和CI。三个seed原始点估计、72条差值和24组mean/sample std已登记 [整合摘要](ms96_integration_summary.md)，并进入双语Results、引言、贡献、讨论及局限性。
原14处MS96标记已按对应证据整合清除，不是为了绕过final门禁。完整曲线仍seed42；43/44只96k。原先待选A/B/C分支不再适用，改为小差距但N保有优势的具体分split、分协议结论。

## Y96_STATUS：RESOLVED
43/44的Y96与M1-Y原生AUC/F1/Accuracy已有两split汇总，状态未知缺口关闭。三seedtest点估计均M1稍高，seed44验证Accuracy有轻微下降。此关闭只确认运行点指标存在并完成稿件整合，不确认完整运行参数或新增bootstrap；这些属于下面独立缺口。两处旧Y96_STATUS标记已清除。

## 其他待补信息
| ID | 缺口 | 当前处理 | 本轮状态 |
| --- | --- | --- | --- |
| BOOTSTRAP_PROVENANCE | exact shell invocation未留存；其余生成链已恢复 | 原summary、当前CI所需7份paired prediction、README/manifest、5000次、effective OUT、reuse行为、bootstrap seed规则及执行时期脚本Git/blob身份已交叉登记于 [闭环记录](bootstrap_provenance_closure.md) | RESOLVED；无需继续搜索、重跑bootstrap或重算CI |
| RUN_METADATA | exact shell invocation、精确base revision及正文未声称的完整optimizer/scheduler/LR/软件栈未留存 | 五份原机器回收JSON已与冻结N24、M1和SASRec证据交叉登记于 [运行台账](run_metadata_ledger.md)；中间checkpoint误报已排除，M仍按调度预期，S391保留短尾200000 | RESOLVED；披露未留存边界，不再搜索机器或重跑 |
| METHOD_CITATIONS | Llama-3.2、LoRA、QLoRA/NF4、MovieLens-1M、Amazon Reviews 2023 5-core及bootstrap方法引用 | 六项均由一手来源闭环；SASRec复用既有S08 | RESOLVED；两处正文标记已清除 |
| TEMPLATE_UNASSIGNED | venue/template未指定 | 维持双语Markdown作者源和装配接口 | 保留，本轮无模板适配 |

跨数据集边界仍为Amazon旧seed42排序方向；不关闭其未覆盖的完整曝光/高曝光统一/hard协议范围。本轮不建议或执行新实验。

Methods的两处METHOD_CITATIONS标记已在来源、BibTeX、registry和双语正文同步后清除。BOOTSTRAP_PROVENANCE于2026-09-09按“exact shell invocation未留存、effective parameters与源码身份已交叉恢复”的边界正式关闭。RUN_METADATA随后依据五份原机器回收JSON、N24既有评测索引、M1调度审计及SASRec正式inventory完成运行到结果绑定；两处Methods marker已删除。M1仍是依赖正确resume data skipping的预期每任务分配，SASRec实际消费量仍以原alignment inventory为准。TEMPLATE_UNASSIGNED继续作为控制层决定点，稿件draft状态不因上述闭环自动升级ready。更早冻结文件中的旧待处理描述属于历史快照，以本文件及两份闭环记录为当前状态。
