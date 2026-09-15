# Methods/Results 叙述修订与 Discussion 初稿

日期：2026-09-06。第一版已由用户审阅；本轮为局部正文修订与两章续写，不是整篇重写。

## 范围与输入

- 作者源：03-08 及对应 parts；保留逐段 EN/ZH 和稳定段落 ID。
- 依据：现有 paper/evidence、冻结表图及其来源索引；必要时定向核对已完成 artifact。
- 允许修改：上述正文、caption、paper/evidence 审计与回填计划、写作计划、独立审校件、当前任务记录。
- 禁止：训练、推理、重算指标、重建候选、轮询或等待 MS96、读中途 checkpoint、文献搜索、Wiki 读写、修改旧稿、续写 Introduction/Abstract/Conclusion、拼整篇稿。

## 论证职责

- Methods：区分完整序列样本构造与最近 10 条模型输入，保留可复现细节，压缩重复边界。
- Results：能力差异、曝光响应、多任务接近程度、较难协议、曝光感知 SASRec、Amazon 外部方向检验。
- Discussion：监督接口、曝光变量、条件性统一、协议影响、样本效率、外部效度六节；每节解释意义，不复制结果清单。
- Limitations：训练不确定性、评估协议、跨数据集覆盖、计算与服务范围四段。
- 长度：以完整论证段为单位，通常每个语言段 3-7 句；不为长度填充免责声明。

## 必交与拒收项

- 03-08 双语工作稿；narrative_revision_log、defensive_language_audit、ms96_integration_plan；逐段 Results/Discussion 质量审查。
- 验证负责实验决策；冻结测试结果参与科学解释，尤其保留 k5 test 的 N 优势。
- RQ1 描述监督 formulation 的能力结构，不作单因素因果归因。
- MS96 继续标记，不选择 A/B/C；Y96 43/44 仍未确认。
- 拒收：数值或资产变动、英中 claim 强度不一致、提示词/过程语言进入正文、重复免责声明取代发现。

## 检查方式

- 自动检索英中防御词，逐位置分类；人工检查 Results/Discussion 的中心句、新信息、位置和推进作用。
- 复用 assemble.py 的逐段、证据 ID、数字和引用检查；运行现有 25 项测试。
- 分别生成 Methods、Results、Discussion、Limitations 的 en/zh/bilingual 审校件；不生成完整稿。
- 对照资产 hash；运行 git diff --check 与 stage_guard.py。
- 使用 paper-orchestration、writing-chapters、writing-core、experiment-results-planning 与 verification；不进行文献或图形生成任务。

## 交付边界

先做范围审查，再做科学与文字质量审查。完成后汇报十项指定内容并停止，不推进 Introduction。
