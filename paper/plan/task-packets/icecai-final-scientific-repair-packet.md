# ICECAI 2026 Scientific Repair Packet

状态：`MINOR_REPAIR_BEFORE_FREEZE`。本文件只定义下一轮需取得的证据和可能的最小修改，不执行正文修改、训练、推理或重评。

## P1-01 跨任务留出隔离

**问题**：Y按末两个时间桶留出，N按末两个合法单事件目标留出。对同一用户，两套边界可能不一致。当前稿只证明每个目标的历史严格早于目标，没有证明M1的Y训练分支不会包含N验证/测试目标事件，也没有证明反向关系。

**先取证，不先改稿**：

1. 从实际生成M1训练、Y/N验证和测试数据的代码与产物恢复统一事件键，至少包含dataset、user、item、timestamp；同时间桶重复事件需有稳定区分键。
2. 计算`M1.Y_train targets ∩ N.validation/test targets`，并检查M1.Y训练样本的目标/输入历史是否包含N留出目标事件。
3. 对称检查`M1.N_train targets/history ∩ Y.validation/test targets`，分别报告目标重叠与仅历史重叠。
4. 按MovieLens/Amazon、split、训练seed和run给出计数、比例、受影响用户数及可复现命令；确认所有正式M1 checkpoint实际使用的是哪份数据快照。

**裁决分支**：

- 若关键交叉重叠为0：在Methods用一句至两句报告共同隔离规则和审计结果，并保存审计artifact；无需训练。
- 若存在重叠但经既有设计规则可证明不构成目标信息泄漏：必须给出明确定义、原因及量化结果，再由科学审查判断；不得只用“严格早于目标”替代。
- 若M1训练确实接触N或Y留出目标：停止文字修补，升级为科学正确性问题；重新构造无泄漏数据，并重训、重评受影响的M1结果后再审。

## P1-02 核心实验配置与Amazon曝光披露

**问题**：当前正文没有充分给出复现和评估主要比较所需的实际配置。缺口包括LLM优化器、学习率与调度、续训关系、N训练候选构造和具体输入表示；SASRec关键结构、历史长度、损失与优化配置、配置选择依据；以及Amazon各“earlier operating points”的准确任务曝光/检查点映射。

**先取证，不先改稿**：

1. 从正式run metadata、冻结配置和checkpoint身份恢复LLM优化器、学习率、调度、warmup、weight decay、precision、最大步数/停止规则、seed，以及Y/N/M1各曝光点是否连续续训。
2. 恢复N训练时候选数量、正例位置策略、负例抽样池/排除规则、候选顺序、采样seed，以及prompt中历史/候选的实际文本表示。
3. 恢复SASRec的max sequence length、embedding dimension、block/head数、dropout、loss/negative handling、optimizer、learning rate、regularization、batch size、训练步数/曝光点与checkpoint选择依据。
4. 为Amazon表中base/Y/N/M1/SASRec逐项绑定准确run/checkpoint、任务样本曝光和选择规则；若某值无法恢复，明确标记unknown，不猜测。
5. 将恢复值与现有`run_metadata_ledger`、配置哈希和主表逐项交叉核验，确保不是另一次试跑配置。

**最小后续修改范围**：证据齐全且无冲突时，只在Methods/Experimental Setup和Amazon结果或表注中补充紧凑配置与曝光说明；不改变现有结果数值和科学结论。若证据冲突，则先更新provenance并重新科学裁决，不能直接写稿。

## 再冻结条件

- P1-01完成可复现的跨任务隔离审计，并证明正式结果未受留出目标泄漏影响。
- P1-02的关键配置和Amazon曝光由正式artifact闭合，且能在篇幅内准确披露。
- 经授权完成最小正文修复后，重新生成英文稿并由GPT-6 Astra只复核这两个P1及其对RQ3/RQ4/RQ5的影响。
- 仅当复核P0=0且P1=0，才创建`manuscript_contract_icecai_2026_science_frozen_pre_metadata_2026-09-11.json`。
