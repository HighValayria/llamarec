# 用户已确认的内容结构

| 模块 | 当前状态 | 论证职责 |
| --- | --- | --- |
| 00 Contributions | 4对双语，p02/p03整合MS96 | C1界定、C2主、C3支撑、C4次 |
| 01 Introduction | 7对双语，仅发现段整合MS96 | 背景 → 预测问题 → 累计曝光 → 协议与部分重合问题 → 设计 → 发现 → 分层贡献 |
| 02 Related Work | 9对双语，六项文献缺口已处理 | 四主题、实质近邻与具体问题，不是系统综述 |
| 03 Problem Formulation | 已审校，基本冻结 | 历史、标签、Y/N/M1和RQ1-RQ5 |
| 04 Methodology | 已审校，基本冻结 | 时间切分、训练与评分输出 |
| 05 Experimental Setup | wrapper不变，统计p02最小补充 | 数据、曝光、候选协议、统计及基线 |
| 06 Results | 结构不变，MS96局部更新完成 | 五个RQ及Amazon方向检验 |
| 07 Discussion | MS96已整合；R01-R09局部修订完成，待用户审阅 | 六方面的结果含义 |
| 08 Limitations | 已更新96k训练seed与统计/协议范围 | 训练、评估、外部效度、计算与服务范围 |
| 09 Conclusion | 骨架，未续写 | 等待后续授权 |
| 10 Abstract | skeleton + ABSTRACT_NOT_FINAL | 等待最后定稿 |

RQ1监督语义；RQ2曝光响应；RQ3每任务曝光对齐下多任务统一；RQ4较难候选协议鲁棒性；RQ5曝光感知SASRec比较。2026-09-08保持RQ结构与冻结中心，只作MS96局部整合；无新增RQ。

Related Work依次为LLMs for Recommendation、Recommendation Supervision and Task Formulation、Multitask and Unified Recommendation Modeling、Evaluation and Baseline Comparison。7段引言直接放在01，没有建立空的introduction parts；四主题相关工作使用独立parts作为唯一正文源。
