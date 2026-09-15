# ICECAI 2026 Cross-Task-Safe Scientific Repair Execution Report

## 1. Verdict

`PASS — GPT6_REPAIR_VERIFICATION_READY`

本轮完成基于既有证据的科学修复，不执行 science freeze。活动稿件统一采用 final-protocol framing：M1 排序结果来自 cross-task-safe evaluation subset；限制发生在评测侧，稿件明确说明 M1 并未在 joint temporal cutoff 下训练。活动作者源中的事故叙事匹配数为 0。

## 2. Fixed evidence used

- M1-48 coverage：validation 5,494/5,675（96.81%），test 5,600/5,675（98.68%）。
- M1-96 coverage：validation 5,318/5,675（93.71%），test 5,535/5,675（97.53%）。
- 48k/96k common-safe subset：validation 5,318，test 5,535。
- seed42 validation 的 N-M1 gap 从 48k 到 96k 在 HR@1、NDCG@5、MRR 三项均缩小；test 三项均未缩小。
- clean 96k 三 seed：54/54 个 seed-level N-M1 ranking deltas 为正；18/18 个 protocol-split-metric 汇总均为 3/3 正向。
- k20 HR@1 mean delta：validation +0.08042，test +0.07678；k50 为 +0.00990/+0.01048，且相对 k5 的大小依 metric 和 seed 而变。

未进行新 bootstrap、显著性检验或机制推断。原 full-set M1 ranking 数值与旧 ranking bootstrap CI 不再出现在活动证据中。Y96 与 M1-Y96 的 seed42 paired bootstrap 保留，仅用于 Y-side capability comparison。

## 3. Manuscript and display changes

- RQ3：将结论收敛为条件性 specialist/shared 关系。validation 的 common-safe 轨迹支持 3/3 narrowing；test 不支持 narrowing；96k ranking 仍小幅一致偏向 N。Y-side 只表述为 measured comparable performance，不声称 equivalence 或 positive transfer。
- RQ4：改为 alternative candidate protocol sensitivity。k20 显示更大 N advantage；k50 仍偏向 N，但不支持 candidate-count 单调或因果解释。
- Table IV：seed42 common-safe 48k/96k k5 exposure comparison。
- Table V：seed42 Y-side binary paired bootstrap only。
- Table VI：96k cross-task-safe three-seed N-M1 ranking summary。
- Table VII：cross-task-safe subset coverage；保留为独立表。
- Figure 1/2：文件字节与父合同一致，均未修改。
- Amazon：活动表仅保留 Base/Y/N/SASRec；未认证 M1 已移除。
- Abstract、Introduction、Discussion、Limitations、Conclusion：仅同步上述证据边界、validation/test 区分、资源公平限制与外部效度范围。

## 4. SASRec disclosure

Methods 已披露 64-dimensional embedding、2 attention heads、2 causal Transformer layers、256-dimensional GELU FFN、dropout 0.2、final LayerNorm、history length 10、dot-product item scoring with bias、full-item cross-entropy；AdamW、learning rate 0.001、weight decay 0、no scheduler、batch size 512、seed42；四个 operating points 独立从头训练，预定义 step 为 47/94/188/391，对应实际 exposure 24,064/48,128/96,256/200,000，不使用 validation best checkpoint 或 early stopping。比较只对齐 downstream task-sample exposure，不对齐 pretraining、tokens、updates、FLOPs、时间或端到端资源效率。

## 5. Build and layout audit

- English：COMPILED，10 pages，9 tables，2 figures。
- Bilingual：COMPILED，16 pages，9 tables，2 figures；English paragraph SHA256 与英文版一致。
- 两版 undefined citations/references、duplicate labels、overfull h/v boxes、missing characters、float-only pages、unprocessed floats 均为 0。
- 活动引用 25 条；2024-2026 引用 13 条，占 0.52，状态 PASS。
- 100 dpi 全页 raster/layout audit：两版均无空白页、无越界文字/绘图、最外缘暗像素为 0；英语页密度区间 0.056253-0.171267，双语为 0.059308-0.155649。应用内图片查看器因 Windows sandbox refresh error 不可用，因此本轮视觉结论限定为自动渲染与版面审计，不冒充人工逐页目视检查。

## 6. Verification

- `paper/assembly/tests`：57/57 passed。
- `paper/submission/ieee_generic/tests`：11/11 passed。
- `paper/submission/icecai_2026/tests`：6/6 passed。
- 活动事故叙事匹配：0。
- 活动旧 full-set M1 数值签名：0。
- 活动旧 M1 ranking bootstrap CI 表：0。
- `stage_guard`：1 个既有工作区错误，来自本轮开始前即存在的 `wiki/current_state.md`、`wiki/index.md`、`wiki/reports/README.md` 与 `wiki/reports/interview_guide/` 改动；本轮未读取、修改或授权同步 Wiki。
- Author：`DEFERRED`；GenAI：`DEFERRED`。
- Training/retraining/inference/candidate generation/bootstrap/new statistics：`NONE`。

## 7. Contract

新合同：`paper/plan/review/manuscript_contract_icecai_2026_post_scientific_repair_2026-09-11.json`

父合同：`paper/plan/review/manuscript_contract_icecai_2026_pre_final_2026-09-11.json`

合同 stage 为 `POST_SCIENTIFIC_REPAIR_PRE_METADATA`，status 为 `GPT6_REPAIR_VERIFICATION_READY`。合同保护当前双语作者源、9 张活动表、2 幅正式图、证据控制、引用控制、两版 PDF 及其 build manifest 所承载的编译事实，并继承两份历史基线。
