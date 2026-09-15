# MS96双语修订审阅入口

更新：2026-09-08。本轮已将seed42/43/44的96k结果整合进双语作者源。文献与新颖性冻结不变；无训练、推理、新检验、文献搜索或完整稿生成。

## 优先读五份
1. [证据与数值摘要](evidence/ms96_integration_summary.md)：原始逐seed结果、两split、各协议差值、mean/std、原bootstrap和结论边界。
2. [RQ3专家与多任务](modules_parts/results/rq3_multitask_unification.md)：Y保留、seed42验证轨迹、96k三seed小差距及test剩余优势。
3. [RQ4候选协议](modules_parts/results/rq4_hard_candidate_robustness.md)：k20较大差距；k50同方向但较小且不一律大于k5。
4. [贡献](modules/00_contributions.md)：p02/p03更新，C2主、C4次、C3支撑、C1界定未变。
5. [引言](modules/01_introduction.md)：仅发现段p06更新，其他段落与引用保持。

## 讨论与限制
[条件性统一](modules_parts/discussion/conditional_unification.md)、[协议解释](modules_parts/discussion/evaluation_protocol.md)解释为何一次低曝光或k5比较不足以概括共享模型。[局限性](modules/08_limitations.md)区分单seed曲线与三seed96k、评估抽样与训练变异；[统计说明](modules_parts/methods/bootstrap_and_statistics.md)仅最小补充。

## 表格与验收
新表是validation/test各一张96k主表、各一张协议表和一张两split差值描述统计表。raw/delta/provenance保持可追溯，旧CI与原图表不变。
47测试通过，78对双语干验证通过，57保护文件未变。MS96/Y96_STATUS关闭；运行参数、统计原预测链、方法引文和模板缺口保留，final仍按预期被阻止。
[审查记录](plan/review/ms96_integration_review.md)说明修改范围及发现的三处易误读。[文献冻结](evidence/story_and_novelty_freeze.md)仅在末尾追加实验更新。
旧builds/review中的历史审校件没有重建，不代表当前作者源。本轮完成后停止，尚未进入摘要、结论或投稿排版。
