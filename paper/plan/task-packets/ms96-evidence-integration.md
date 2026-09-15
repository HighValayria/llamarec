# 96k 证据整合任务包

日期：2026-09-08。用户已确定实证论文类型、双语模块结构、论点和局部修改范围，继续指令授权完成本轮各部分，不重复选题或逐章等待。本轮是局部证据修订，不是整篇重写。

## 范围与输入
读取现有作者源、冻结 seed42 final_evidence、Git 提交 a9c6cd959cf32afe046bb05be9eb5096bebfc5fb 的 artifacts/multiseed96 八份轻量文本。已 fetch/archive，无 merge、checkout 或重置。本地 HEAD 保持 dcd4b9f6125fd0e7eb7c83b686223d8b9a44f6c1。
文献与新颖性冻结；不检索、不重开 Related Work、不访问 Wiki。只哈希保护文件，不重复读取其内容。

## 所有权与交付
本任务控制器负责 00/01/06/07/08 及必要结果/讨论 parts；05 wrapper 不改，仅 statistics.p02 补充已有训练种子覆盖。生成描述统计程序、新表、ms96_integration_summary、更新事实/措辞/待补映射；freeze 只追加。
旧数值与 CI 表、参考文献、02/03/04、其余方法、摘要/结论、旧稿不改。输出新表，不重建全稿或旧审校稿。

## 写作前论证链
- results.rq3.p01：96k Y 表现保留 → 三 seed 两 split → seed42 CI 与 seed44 验证 Accuracy 例外。
- results.rq3.p02：seed42 验证轨迹收窄 → 43/44 只复现 96k 小差距 → 原验证 CI，非等价。
- results.rq3.p03：冻结 test 三 seed N 小幅领先 → 差值均值 → seed42 CI → 转入候选协议。
- results.rq4.p01/p02：k20 三 seed 较大 N 优势；k50 同方向但较小且幅度随 seed 变，不总大于 k5。
- results.rq4.p03：三种非嵌套协议的采样、组成、数量共同变化 → 不识别纯大小因果。
- intro.p06 与 contributions.p02/p03：只升级对应发现，保持 C2 主、C4 次、C3 支撑、C1 界定。
- discussion：先讲条件性关系的意义，再说明单 seed 轨迹与多 seed 运行点的边界。
- limitations.training/evaluation：全曲线 seed42；96k 三 seed；评估抽样、训练变异、选择/留出证据各有不同作用。
篇幅保持现有段落论证密度；EN 后 ZH、ID 稳定，正文不得混入任务说明。

## 数据契约
CSV/TSV 用结构化解析；summary 与 validation_summary 是重复，不重复计数。Y-M 的 samples 是 binary 样本数，不能当成 M-N 排序目标数。
差值 Y=M1-Y减Y96，排序=N96减M1-N。均值等权，sample std ddof=1，n=3训练seed。只算已有汇总值的差和描述统计，不重算预测指标、bootstrap或统计检验。
seed42 k5原点只有10位小数，允许与冻结原bootstrap delta末位不同；CI原样保持。
新表：validation/test宽主表、validation/test协议表、两split差值mean/std汇总、原始来源与Y逐seed差值附表。
精确候选嵌套比例只有用户提供，未独立取到原audit；正文仅保留已冻结非嵌套结论。

## 拒收条件与验证
训练/推理/新实验/新bootstrap；修改文献定位；跨seed曝光收窄；parity/等价/positive transfer；k50一律比k5大；全曲线或Amazon被升级跨seed。
运行新数据程序 --check、unittest、assembly --check、双语/数字/引文/证据/表图引用与危险词逐项审查、保护hash、git diff --check、stage_guard。
两轮审查：范围/科学合规、语言/叙事质量。记录技能使用审计后停止。
