# 采样与候选评价证据

> 2026-09-08：根据用户新授权与跨Agent原文裁决，证据已整合到00-02。以下映射为当前定位；两份原始报告及旧未采用备份保持不变。

日期：2026-09-07。先说明研究对象，再说明结论，不将已有采样理论充当本文hard结果的机制解释。

| 原文/已读位置 | 固定或变化什么 | 可支持的结论 | 不能支持什么 |
| --- | --- | --- | --- |
| Krichene & Rendle，KDD2020官方摘要；同作者IJCAI2021扩展稿§2-4 | 固定评价实例与模型，相关物品加随机非相关物品，比较采样与精确指标 | top-heavy采样指标可不保留模型相对顺序，即使在期望上；扩展稿为单相关物品说明，原KDD覆盖更一般情况 | 并非所有指标都不一致，AUC有特殊地位；不是本文非嵌套hard差距的因果证明 |
| Cañamares & Castells，RecSys2020 §1、§3 | target set是待评分候选集合T_u并N_u；固定已评分测试物品T_u，改变额外未评分物品N_u | 候选采样范围能改变比较，并与缺失反馈和模型偏好有关；全库也非自动无偏 | “target sampling只选择正样本目标”是错误解释；不能把该研究等同于只改正例身份 |
| Dallmann et al.，RecSys2021 §4.3-4.4、§5.1-5.2 | 同一批训练模型，在full、uniform、popularity抽样下重评估，考察负例数 | 均匀与流行度采样都可能与full模型次序不一致，且彼此不同 | 20次候选抽样重复不是20训练seed；full也不等于线上真实效用 |
| InstructRec，§3.3.1-3.3.2 | hard实验为二塔检索9负例加真值；100候选实验另为个性化搜索且分组推理 | 推荐LLM的困难候选和较大候选评估已有明确先例 | 不能说本文首次hard评估；不能把两组结果当同一实验只增加候选数 |

原文：[KDD官方摘要](https://research.google/pubs/on-sampled-metrics-for-item-recommendation/)、[IJCAI同作者扩展稿](https://www.ijcai.org/proceedings/2021/0651.pdf)、[Cañamares原文](https://castells.github.io/papers/recsys2020.pdf)、[Dallmann原文](https://arxiv.org/pdf/2107.13045)、[InstructRec原文](https://arxiv.org/pdf/2305.07001)。

## 术语纠正

上一版rw.evaluation.p01按题名把target-item sampling理解成仅选择正样本评估目标，这与Cañamares原文不符。本轮纠正为候选集合采样，并在introduction的背景句使用“candidate construction”。概念上可以区分持出相关目标、为该目标构造候选集合、在集合上计算指标；但不能把这三个概念逐一硬派给三篇论文。

## 对本文的落点

- 已冻结C6及hard_candidate表才是N/M在k5与较难协议下差异的直接证据。
- 外部文献仅支持“评价结论依赖候选构造与指标，协议需要报告”这一方法学动机。
- 本文协议非嵌套，候选数量、内容与难度没有因果解耦；不能写“增加数量导致差距扩大”。
- k5小差距不能自动外推稳健持平，也不等于统计等效性检验。
- SAMPLING_EFFECT_DETAILS的有限证据RESOLVED；本轮正文已REWRITTEN_AND_RESOLVED，正确候选定义及有限敏感性已经进入中英两版。S05只用于零样本背景，不采用未核的LLMRank候选细节。

## 获取边界

KDD完整PDF下载未成功，不能写成已通读。官方KDD摘要直接支持正文中“不保证保持模型排序”的有限结论；IJCAI同作者扩展稿提供定义、例子与条件。没有把该扩展稿计作一篇新近邻，没有复制未检查的数值表。
