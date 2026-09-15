# M1 No-Retrain Removal Plan

> 2026-09-11更新：本计划的触发条件已失效。缺失prediction已全部恢复，clean-subset重算完成；本删除方案不再执行。后续仅可按`m1-clean-subset-recovery-closure.md`中的受限claim同步计划，在用户授权后修改稿件。

状态：`PLAN_ONLY`  
触发条件：无法取得seed42 N48/M1-48及seed43/44 N96/M1-96已有逐样本预测，且不授权新推理或重训。  
本文件不执行任何论文修改。

## 1. 保留主线

- 保留RQ1：Y/N监督语义与specialist差异；其证据不依赖M1。
- 保留RQ2：Y/N specialist曝光响应；删除其中任何以污染M1作参照的句子。
- 保留RQ5：N与SASRec的曝光对齐比较；同步已闭合的SASRec架构、优化和运行点披露。

## 2. 删除或降级

- RQ3不再声称“specialization vs unification随曝光变化”，因为N48/M1-48没有可过滤预测，N96也缺少三seed干净子集证据。
- 从主结果表、摘要、贡献、讨论和结论删除由污染M1-N全量评测支持的specialist-vs-M1差值、趋势及多seed稳定性表述。
- RQ4删除M1参与的k5/k20/k50 robustness比较；若保留RQ4，只能改写为N specialist自身随候选协议变化的描述性结果，且不得暗示与M1的干净比较。
- seed42 M1-96干净子集结果只作为审计诊断保存，不进入论文主张，因为它不能补齐预注册式曝光点和多seed结构。

## 3. M1-Y可保留边界

MovieLens Y validation/test目标与Y-train target、N-train target及N-train history的交集均为0。因此M1的Y侧preference结果可作为**次要的任务保持观察**保留，但须满足：

- 不再把它与无效的M1-N结果合并为统一模型成功证据；
- 不声称它证明跨任务正迁移或specialist/unification结论；
- 明确其只回答M1 checkpoint在Y评测上的表现；
- Amazon M-Y在完成同口径隔离审计前不据此类推。

## 4. 执行范围

未来获授权后，按依赖关系更新：`RQ3/RQ4 Results -> specialist_multitask/hard_candidate tables -> Discussion -> Limitations -> Contributions/Introduction -> Conclusion -> Abstract`。RQ1、RQ2 specialist数值和RQ5数值保持不变，只做必要交叉引用调整。

执行前先归档当前科学源并建立claim-to-source删除清单；执行后重编译双语版本，运行冻结证据测试、引用测试、版面审计和全文claim一致性检查。不得借删除M1证据扩写新故事。

## 5. 可逆决策点

优先尝试从原机器取回**已有**逐样本预测，不启动推理。若四组缺失artifact全部取回，则重新运行clean-mask过滤、seed42 N48比较和seed42/43/44 N96描述统计，再决定是否改用clean-subset repair plan；否则执行本删除计划。
