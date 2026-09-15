# 叙述修订与讨论初稿审查

日期：2026-09-06。审查对象为03-08，不是正式投稿稿。第一版已由用户审阅，本轮为第二次限定交付。

## 范围与交付审查

- 03-06完成Methods/Results叙述修订，07有六部分Discussion，08有独立四主题Limitations。
- 58对EN/ZH：25方法、16结果、13讨论、4局限。稳定段落ID保留；统计p03撤销并记录迁移。
- narrative_revision_log.md、defensive_language_audit.md、ms96_integration_plan.md均存在，另有29段质量审查与扫描JSON。
- 图表仅调整caption；23项受保护资产与章节hash未变。
- 未训练、推理、重算指标、重建候选、轮询MS96、读中途checkpoint或开展文献搜索。
- 未访问Wiki、覆盖旧manuscript、修改最终引言/摘要/结论或拼接完整论文。
- 四组章节各有en/zh/bilingual独立审校件，共12份。

## 科学与文字质量审查

| 要点 | 审查结果 |
| --- | --- |
| 完整序列与输入 | H(u,t)用于样本构造，H_10最多10条严格更早交互；低评分事件保留 |
| 选择纪律与证据解释 | validation用于实验决策，冻结test参与解释；正文和caption去掉test降格措辞 |
| RQ1因果 | 描述完整formulation对应的能力结构，目标、数据、prompt、scoring联合变化明确 |
| RQ2响应 | Y增益减弱/N持续改善基于各自范围；不宣称收敛或识别优化机制 |
| RQ3 split | 验证gap很小、test N优势并列；最后通读修正“两个split都显示gap缩小”的潜在暗示 |
| RQ4协议 | 数据与CI先行；协议非嵌套，组成和数量共同改变，不推断单因素因果 |
| RQ5效率 | 四点N优势与SASRec改善同时呈现；只描述预训练起点，未单独归因预训练收益 |
| Amazon | 先讲重现的ranking方向，后界定MovieLens详细曲线角色 |
| Methods细节 | 七类LoRA投影、response-only、完整答案似然、batch/曝光、0.5阈值、percentile CI均保留 |
| 防御语言 | 55处旧正文匹配逐项处理；现8处均有科学必要性；caption另2处处理 |
| 逐段推进 | Results/Discussion 29对全覆盖中心、新信息、位置和推进作用 |
| 待补证据 | MS96 11处、Y96_STATUS 2处；分split A/B/C未选择；96k复现不扩为整曲线 |
| 双语 | 数字/图表引用自动核对；术语、claim强度、split和seed人工对应审查 |

## 命令与结果

- unittest discover -s paper/assembly/tests -v：25项通过。
- assemble.py --check：11入口、58对段落、24处待补；03-08单独检查为18处待补。
- 四组三语言独立装配：全部成功；最后文字调整后重建Results/Discussion。
- 实际Discussion/Limitations --mode final：子命令exit=2，输出不存在，验证脚本exit=0。
- 23项受保护文件SHA256：全一致；冻结来源/导出校验亦由现有测试通过。
- 定向rg：误导性full-sequence history、report-only、提示词及假想审稿人句式无正文匹配。
- git diff --check：exit=0；87条既有LF/CRLF转换提示，无差异格式错误。
- stage_guard.py：0 errors、0 warnings。
- 最终只读核对：12份审校件的manifest与源文件hash全部对应当前版本；58对段落、8处防御词记录、11处MS96和2处Y96_STATUS与清单完全一致。

## 尚未解决而保持可见的事项

MS96及Y96跨种子覆盖、冻结bootstrap原预测链、历史完整运行参数、方法引文与venue模板均未补造。本轮没有新的数值冲突；原有S391别名差异等按source_of_truth.md既定裁决处理。当前是可审校双语稿，不是所有证据齐全的正式投稿稿。
