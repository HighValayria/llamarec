# ICECAI 2026 Final Scientific Review Report

日期：2026-09-11  
状态：`SCIENTIFIC_REPAIR_REQUIRED`

## Mechanical Preflight

- 结果：PASS。
- English PDF：`paper/builds/icecai_2026/en/main.pdf`，10页，English-only。
- 9 tables，2 figures，5 keywords。
- 25 active references；2024--2026为13条，比例52%，PASS。
- Undefined citations=0；undefined references=0；无孤立Table III，Tables V/VI/VII正文路由正确，表图引用语法正常。
- Build manifest为COMPILED；overfull h/v boxes=0，unprocessed floats=0，missing characters=0。
- 当前PDF SHA256：`0c450fe976aaeb3d4a2d9a5f18540b393d1676a0b3409b9b17f46c308a9fc2c4`，与pre-final合同一致。既有自动布局审计为PASS，本轮重新渲染10页成功。
- ICECAI submission tests：6/6 PASS。本轮没有重建submission。
- `AUTHOR INFORMATION REQUIRED`与未启用GenAI槽按要求视为`DEFERRED_USER_METADATA`，不计FAIL。
- `stage_guard.py`仅因工作区已有、未授权的Wiki修改报错；本轮未读取或修改Wiki，该既有仓库状态不改变上述论文preflight结果。

## GPT-6 Astra Verdict

`OVERALL_VERDICT: MINOR_REPAIR_BEFORE_FREEZE`

- P0=0。
- P1=2。
- P2=0。
- P3=0。

### P1-01 跨任务留出隔离未闭合

Y与N使用不同的留出规则，现有Methods没有说明共同时间截断、跨任务排除或事件重叠审计。因而尚不能确认M1的一个训练分支没有接触另一任务的验证/测试目标。审查未断言已经发生泄漏；若审计发现真实重叠，则需升级处理并重评受影响结果。

### P1-02 核心实验配置披露不足

当前稿缺少足以复现或评估主要比较的若干实际配置：LLM优化器/学习率/调度与续训关系、N训练候选构造和输入表示、SASRec关键结构与优化/选择依据，以及Amazon早期运行点的准确曝光映射。

## Dimension Status

| Dimension | Status | Reason |
| --- | --- | --- |
| RQ1 | PASS | 完整formulation与native/bridge能力边界清楚，无孤立语义因果或跨指标比较。 |
| RQ2 | PASS | Y仅写limited/uneven，N仅写至200k已测点，均限定seed42。 |
| RQ3 | FAIL | 结果措辞正确，但M1跨任务留出隔离尚无方法保证。 |
| RQ4 | FAIL | 非嵌套协议解释正确，但M1比较仍受P1-01影响。 |
| RQ5 | FAIL | 四点结果支持当前方向，但SASRec配置与选择依据不足。 |
| Statistical interpretation | PASS | fixed-model bootstrap与三seed mean/sample SD严格分开，跨零未写等价。 |
| Novelty positioning | PASS | C2/C4/C3/C1层级及非首创边界准确。 |
| Reference-refresh fit | PASS | Pereira、Milogradskii、Shehzad/Jannach均未越权承载证据。 |
| Methods | FAIL | 任务与曝光定义清楚，但跨任务隔离和关键配置披露不足。 |
| Evaluation design | FAIL | 协议和资源边界充分；共享训练的跨任务留出安全性未建立。 |
| Table/Figure sufficiency | PASS | 9表2图覆盖主张；Table VI/VII职责清楚；Figures不替代test证据。 |
| Discussion | PASS | 主要解释条件与意义，未虚构机制。 |
| Limitations | PASS | 统计/训练、评估、外部有效性、资源四类均覆盖。 |
| Conclusion | PASS | 三段结论未扩大为等价、普遍优势或候选数量因果。 |

## Freeze Decision

因P1>0，本轮不执行science freeze，不创建science-frozen contract，不自动修改论文。下一步仅按`paper/plan/task-packets/icecai-final-scientific-repair-packet.md`取证；作者信息与GenAI披露继续延期。
