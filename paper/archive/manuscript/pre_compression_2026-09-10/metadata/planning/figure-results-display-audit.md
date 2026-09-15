# Figure and Results Display Audit

## A. Scope and Evidence

本轮只审计展示责任，不执行修改。依据为当前14页English PDF、Results作者源、两张正式PNG及caption/data manifest，以及冻结的T-BALANCED九表方案。Figure 1位于PDF第7页左栏上部，Figure 2位于第8页左栏中部；两图均清晰可读、无裁切。两图都只展示MovieLens seed42 validation HR@1，不展示test或训练随机性区间。

写前冻结指纹：37份作者源`2f208cb1f9d8a8db16e5f1aac81d2d8a10a25056105e67b975bd55d33aec5e9b`；15份table目录文件`1e6a0d521005cb1327de1e0f4a8a9230ded97d96b2afe387378caf7bd7680960`；7份figure目录文件`cdf6ab91046a2b2b74e0a159196d57ffd86705bda48e04fe20cedadff6c5188e`；10份submission文件`39028b9a54081568ce4e8298feeba91bd9c85e5406adc33fcc7d65b6e0c368a9`；English PDF`4e97eeb28adfd849f261bf555bc7feb9bfb2a58d2471f78448f913abfe12d2b3`。

## B. Figure 1 Audit

**Verdict: `KEEP_WITH_PROSE_REDUCTION`.**

- Independent value: Figure 1以收紧的纵轴单独呈现N24/N48/N96/N200，读者能立刻看到N在每个已测曝光点持续上升，以及早期斜率与后段增益不同。Table V适合查精确双split、多metric和M1值，但不如图直观。
- Redundancy: Table V包含Figure 1的四个validation HR@1点；Figure 2的N线也重复这四点，但因Figure 2纵轴需容纳SASRec，N内部增益视觉上被压缩。Figure 1仍有独立的“单模型响应曲线”价值。
- Display responsibility: Figure 1负责RQ2的N trajectory直觉；Table V负责精确值、test方向、NDCG/MRR和M1 matched points；prose只保留端点增量与解释。
- Prose reduction: `results.rq2.p02`不再需要逐点列`0.5774, 0.6030, 0.6238, 0.6516`及四个test值。未来正文保留validation endpoints与`+0.0742`幅度，并说明test同向即可。
- If removed: Table V必须保留全部四个N validation点、双split和至少HR@1，并由prose明确“每个已测点持续改善”；趋势理解会变慢。
- Future-only layout options: caption可缩短，保持单栏；不建议扩大为双栏。不得改变轴、数据或范围。

## C. Figure 2 Audit

**Verdict: `CORE_MAIN`.**

- Independent value: 双线直接展示N始终领先，同时SASRec在200k附近改善更快，validation HR@1 gap从96k到200k明显收窄。这一“领先与追赶同时成立”的张力比表格逐行扫描更容易理解。
- Redundancy: Table XIII包含精确N/SASRec exposure、validation/test HR@1及delta。Figure 2只负责validation趋势，不能替代Table XIII的held-out证据和精确匹配。
- Display responsibility: Figure 2负责RQ5的相对曲线与gap narrowing；Table XIII负责exact exposure、双split、四点数值和delta；prose只保留全四点领先及96k/200k gap anchor。
- Prose reduction: `results.rq5.p01`无需再打印两条四点序列和四个delta；保留结论与两个代表性gap即可。`results.rq5.p02`中的200k test pair可由Table XIII承担，除非作者希望保留一个held-out anchor。
- Table-only sufficiency: Table XIII单独足以支撑RQ5的精确claim，但牺牲“gap随曝光收窄”的即时理解，因此不推荐删图。
- If removed: Table XIII必须保留四个exposure、双split、N/SASRec HR及delta；prose必须保留96k与200k gap。
- Future-only layout options: caption可缩短、legend可简化为N/SASRec；保持单栏。不得重画。

## D. RQ Display Responsibility Map

| RQ | Primary finding | Primary display | Secondary display | Precision source | Trend source | Prose role |
| --- | --- | --- | --- | --- | --- | --- |
| RQ1 | Y-native preference与Y-as-ranker/N-native是不同被测能力 | future merged III/IV | none | merged table | table分panel | 点出能力差异和一个native anchor、一个ranking contrast，不复述全metric |
| RQ2 | Y响应有限/不均匀；N持续改善至200k | Figure 1 for N trend; merged III/IV for Y | Table V | merged III/IV + V | Figure 1 | 给端点幅度与Y/N解释，不列完整序列 |
| RQ3 | 96k Y-side preserved；validation gap缩小而test仍偏N | compact IX | V + VIII | V, VIII, compact IX | prose contrast, no dedicated figure | 明确valid/test tension、一个multiseed headline和CI status，不列逐seed/逐metric网格 |
| RQ4 | gap受protocol条件影响，k20大、k50较小且非单调 | compact IX | compact X | IX multiseed; X seed42 bootstrap | table protocol comparison | headline magnitude、跨seed一致性、CI status、non-monotonic boundary |
| RQ5 | N四点领先，但SASRec继续改善且gap收窄 | Figure 2 | Table XIII | Table XIII | Figure 2 | 全四点方向 + 96k/200k gap，不列两条完整序列 |
| Amazon | 第二领域只复现早期ranking directions | Table XIV | prose boundary | Table XIV | none | 一个N headline和N-M margin；其余模型/metrics由表承担 |

每个finding只有一个主要展示责任。Figure负责趋势，Table负责精度与边界，prose负责解释与少量headline magnitude。

## E. Results Numeric Audit

分类含义：`ESSENTIAL_HEADLINE`保留精确anchor；`NEEDED_FOR_CONTRAST`保留成对或端点差；`ALREADY_IN_TABLE/FIGURE`未来可删精确列举；`SECONDARY_METRIC`由表承担；`REDUNDANT_NUMERIC_RESTATEMENT`是完整数列再次打印。

| Paragraph | Current numeric load | Keep in future prose | Move responsibility | Main classification |
| --- | ---: | --- | --- | --- |
| results.rq1.p01 | 12 values | Y96 validation AUC `0.7844`; Y-as-ranker vs N96 validation HR@1 `0.2211 vs 0.6238` | merged III/IV保存F1/Acc、NDCG及test exact values | ALREADY_IN_TABLE / SECONDARY_METRIC |
| results.rq1.p02 | 0 | no numeric change | prose owns interpretation | ESSENTIAL_INTERPRETATION |
| results.rq2.p01 | 8 metric values + 3 exposures/range | Y AUC endpoint `0.7761 to 0.7844`；说明F1非单调、bridge NDCG窄幅，不必报全值 | merged III/IV | REDUNDANT_NUMERIC_RESTATEMENT |
| results.rq2.p02 | two complete 4-point HR series + endpoints | validation HR@1 `0.5774 to 0.6516` and `+0.0742`; test同向不列四点 | Figure1 trend; Table V precision | REDUNDANT_NUMERIC_RESTATEMENT |
| results.rq2.p03 | 96k/200k | retain both exposure boundaries | prose owns interpretation | ESSENTIAL_HEADLINE |
| results.rq3.p01 | per-seed directions, 4 deltas, one CI | `+0.00553` F1 with CI `[+0.00096,+0.01025]` as Y-side uncertainty anchor；AUC/Acc只写CI跨零 | VIII/compact IX | NEEDED_FOR_CONTRAST; remaining ALREADY_IN_TABLE |
| results.rq3.p02 | 4 absolute points, 3 deltas, CI, two seed deltas, mean+SD | retain `48k to 96k`; three-seed validation HR delta `+0.00587 (SD 0.00767)`；seed42 CI写“crosses zero”不必报bounds | V, VIII, compact IX | most severe REDUNDANT_NUMERIC_RESTATEMENT |
| results.rq3.p03 | three means+three SDs, seed42 delta+CI, 48k gap | retain test mean HR delta `+0.01016 (SD 0.00247)` and seed42 HR CI `[+0.00159,+0.02379]`; other metrics写同向/positive | compact IX/X | REDUNDANT_NUMERIC_RESTATEMENT / SECONDARY_METRIC |
| results.rq4.p01 | 3 seed deltas, valid/test mean+SD, one CI | k20 mean HR delta `+0.08164` validation and `+0.07765` test；all-seed/all-metric方向与seed42 CI positive用文字 | compact IX/X | REDUNDANT_NUMERIC_RESTATEMENT |
| results.rq4.p02 | two ranges, two mean+SD, CI, nonmonotonic pair | k50 mean HR delta `+0.01028` validation, `+0.01010` test；保留seed43 test `+0.00511 vs +0.00775`作为非单调anchor | compact IX/X | REDUNDANT_NUMERIC_RESTATEMENT |
| results.rq4.p03 | candidate counts 5/20/50 | retain protocol counts because they define conditions, while preserving non-nested caveat | prose/methods | ESSENTIAL_HEADLINE |
| results.rq5.p01 | two 4-point series + four deltas | retain “N leads at all four”; validation gap `+0.2957 at 96k` and `+0.1767 at 200k` | Figure2 trend; XIII precision/test | most severe REDUNDANT_NUMERIC_RESTATEMENT |
| results.rq5.p02 | 96k/200k + test pair | retain 96k/200k contrast；`0.6282 vs 0.4511` optional held-out anchor, otherwise Table XIII | XIII | ALREADY_IN_TABLE |
| results.amazon.p01 | 12 metric values + sample count + margin | N HR@1 `0.4669` and N-M margin `+0.00870`; ranking order and larger Y/SASRec gaps in words | XIV stores all rows and secondary metrics | most severe REDUNDANT_NUMERIC_RESTATEMENT |
| results.amazon.p02 | 0 | no numeric change | prose owns scope boundary | ESSENTIAL_INTERPRETATION |

## F. Minimum Numeric Prose by Finding

- RQ1: `0.7844` Y-native validation AUC；`0.2211 vs 0.6238` Y-as-ranker/N96 validation HR@1。Test只说明contrast persists。
- RQ2: Y AUC `0.7761 to 0.7844`；N validation HR@1 `0.5774 to 0.6516`，absolute gain `+0.0742`；test写same direction。
- RQ3: exposure narrowing `48k to 96k`；Y F1 delta/CI `+0.00553 [+0.00096,+0.01025]`；validation mean HR gap `+0.00587 (SD 0.00767)`；test `+0.01016 (SD 0.00247)`及seed42 positive CI `[+0.00159,+0.02379]`。
- RQ4: k20 valid/test means `+0.08164/+0.07765`；k50 `+0.01028/+0.01010`；nonmonotonic seed43 test anchor `+0.00511 vs +0.00775`。CI只需写seed42均positive，不必列bounds。
- RQ5: validation gap `+0.2957 at 96k` and `+0.1767 at 200k`；说明four-point lead和test同向。200k test pair可选，不是必需。
- Amazon: N HR@1 `0.4669`与N-M margin `+0.00870`；Y、M、SASRec完整值及NDCG/MRR留Table XIV。

这些是未来压缩上限，不是本轮编辑指令。实际执行时仍应逐段审阅语法与claim continuity。

## G. Figure/Table/Prose Redundancy

| Finding | Figure | Table | Prose today | Future responsibility |
| --- | --- | --- | --- | --- |
| N exposure trajectory | Fig1 complete 4-point validation trend | V exact both-split/all-metric | repeats both 4-point series | Fig1 trend + V precision + endpoint prose |
| N vs SASRec | Fig2 complete validation curves | XIII exact exposure, both splits, deltas | repeats two curves + four deltas | Fig2 trend + XIII precision + two-gap prose |
| Y semantics/response | none | future merged III/IV | many native/bridge values | table primary + sparse anchors |
| 96k multitask | none | V/VIII/compact IX | many seed/delta/CI values | table primary + valid/test tension prose |
| candidate protocols | none | compact IX/X | means, SDs, ranges, CI and seed values repeated | tables primary + four headline means + boundary |
| Amazon | none | XIV | nearly reprints table | XIV primary + two headline values |

Discussion和Conclusion主要重复finding与边界而非完整数列，当前不属于数值去重的首要对象；本轮不提出对其执行修改。

## H. Page-Saving Scenarios

页面收益是基于当前双栏落版的区间估计，reflow会造成非线性，不能与table savings机械相加。

- A. 只删除最明显的Results逐点数字列举，不重写解释：约`0.4-0.8`页。
- B. 两图均保留，并让prose严格缩到headline+contrast+interpretation：约`0.8-1.3`页。
- C. 在B基础上删除Figure 1：额外约`0.2-0.35`页，总计约`1.0-1.6`页。
- D. 在B基础上删除两图：额外约`0.45-0.75`页，总计约`1.2-1.9`页，但显著损失趋势理解，不推荐。

## I. Display Compression Plans

### D-LIGHT

- Keep both figures。
- 删除完整四点数列的重复打印，但保留较多CI/mean/SD anchors。
- Estimated saving: `0.4-0.8`页。
- Risk: RQ3/RQ4和Amazon仍有较高table-prose重复。

### D-BALANCED

- Figure 1 `KEEP_WITH_PROSE_REDUCTION`；Figure 2 `CORE_MAIN`。
- 按Section E/F的minimum numeric prose压缩，Table承担精确值，Figure承担趋势。
- Estimated saving: `0.8-1.3`页。
- Risk: 执行时必须保留RQ3 valid/test tension、两类uncertainty和RQ4 non-monotonic boundary。

### D-AGGRESSIVE

- 只保留Figure 2；Figure 1改为`REMOVE_MAIN`候选，由Table V和Figure 2的N线共同承接RQ2。
- 采用D-BALANCED的prose reduction。
- Estimated saving: `1.0-1.6`页。
- Risk: Figure 2宽纵轴压缩N内部增益，RQ2 trajectory理解变弱；不值得为约四分之一页默认牺牲。

## J. Interaction with T-BALANCED

`T-BALANCED + D-BALANCED`目标为`9 tables + 2 figures`。这一密度仍合理，因为两图分别承担不同主视觉：Figure 1是单模型曝光响应，Figure 2是跨模型相对曲线。九表承担setup、精度、双split、multiseed和bootstrap边界，不与图完全重合。

- Figure 1 + Table V: 双留。Figure 1负责validation trajectory直觉；V负责双split、三指标与M1。
- Figure 2 + Table XIII: 双留。Figure 2负责gap narrowing；XIII负责exact exposure、test与delta。
- Combined page estimate: T-BALANCED原估计节省`1.8-2.8`页，D-BALANCED另估`0.8-1.3`页；由于float/reflow重叠，联合收益只能暂记为约`2.4-3.8`页，而非简单相加的保证。

## K. Recommendation

推荐`D-BALANCED`。两张Figure都保留，但Figure 1配合缩减RQ2逐点数字，Figure 2配合缩减RQ5双序列与四delta复述。页面优先从Results的第三层数值复述中回收，而不是从有独立趋势价值的Figure中回收。

## L. Review and Execution Boundary

- Future caption shortening、legend simplification或placement调整可另行规划；本轮不执行。
- 本轮不改Figure数据、坐标、范围、caption、文件或布局。
- 本轮不改Results、Discussion、Conclusion或任何manuscript source。
- 本轮不执行T-BALANCED或D-BALANCED，只生成后续裁决材料。

## M. Review and Verification

- Spec review: PASS。两图各有唯一verdict；15个Results段落全部进入numeric audit；RQ1-RQ5及Amazon均有primary display、precision source、trend source和minimum prose；D-LIGHT/BALANCED/AGGRESSIVE及页面区间齐全。
- Quality review: PASS。Figure/Table同源没有被自动判为冗余；valid/test tension、multiseed SD、seed42 bootstrap和protocol non-monotonic boundary均保留；推荐顺序遵循scientific comprehension、precision traceability、page saving。
- Isolation verification: 37份author source、15份table目录文件、7份figure目录文件、10份submission文件及English PDF的aggregate/SHA256均与写前一致。
- Execution boundary: 未重新编译，未修改或重画Figure，未修改manuscript/table/submission/build，未执行任何display compression。
