# Figure and Results Display Judge Packet

## Figure Verdicts

- Figure 1: `KEEP_WITH_PROSE_REDUCTION`。负责RQ2 N-native validation exposure trend；Table V负责精确双split、多metric与M1。未来prose只留`0.5774 to 0.6516`和`+0.0742`，不列完整四点valid/test序列。
- Figure 2: `CORE_MAIN`。负责RQ5 N/SASRec相对曲线与gap narrowing；Table XIII负责exact exposure、test与delta。未来prose只留four-point lead及`+0.2957 at 96k`到`+0.1767 at 200k`。

## RQ Display Responsibility

| RQ | Primary display | Precision | Prose minimum |
| --- | --- | --- | --- |
| RQ1 | merged III/IV | table | Y AUC `0.7844`; ranking HR `0.2211 vs 0.6238` |
| RQ2 | Figure1 + merged III/IV | Table V | Y AUC endpoints; N HR endpoints + `+0.0742` |
| RQ3 | compact IX | V/VIII/IX | 48k->96k; Y F1 CI anchor; valid mean `+0.00587`, test `+0.01016`, one positive test CI |
| RQ4 | compact IX | compact X | k20 means `+0.08164/+0.07765`; k50 `+0.01028/+0.01010`; nonmonotonic pair |
| RQ5 | Figure2 | XIII | four-point lead; 96k/200k gaps |
| Amazon | XIV | XIV | N HR `0.4669`; N-M margin `+0.00870` |

Most severe numeric repetition: `results.rq3.p02`, `results.rq3.p03`, `results.rq4.p01`, `results.rq4.p02`, `results.rq5.p01`, `results.amazon.p01`, and `results.rq2.p02`.

## Display Plans

| Plan | Figures | Numeric strategy | Estimated saving |
| --- | ---: | --- | --- |
| D-LIGHT | 2 | remove obvious complete-series repetition | 0.4-0.8 pages |
| D-BALANCED | 2 | trend in figure, precision in table, headline/contrast in prose | 0.8-1.3 pages |
| D-AGGRESSIVE | 1, keep Figure2 | D-BALANCED prose plus remove Figure1 | 1.0-1.6 pages |

Recommend `D-BALANCED`. Combined target with frozen T-BALANCED: `9 main tables + 2 figures`; provisional joint saving about`2.4-3.8`pages, not mechanically additive because floats reflow.

No Figure, manuscript, table, submission adapter, or PDF modification is authorized or executed. No GPT6 Astra call and no independent Text Compression Audit.
