---
id: rq4_hard_candidate_robustness
title:
  en: Robustness under Alternative Candidate Protocols
  zh: 不同候选协议下的鲁棒性
status: draft
---

<!-- PARAGRAPH: results.rq4.p01 -->
<!-- EVIDENCE: C6 -->

**EN**

At 96k, k20 produces the largest N-specialist-M1 gap among the three evaluated protocols. The cross-task-safe three-seed summary in [TABLE: ms96_delta_summary_compact] gives HR@1 mean deltas of +0.08042 on validation and +0.07678 on frozen test. Across k5, k20, and k50, all 54 seed-level deltas are positive and all 18 protocol-split-metric summaries have 3/3 positive seed directions.

**ZH**

在96k时，k20在三种已评估协议中产生最大的N专家-M1差距。[TABLE: ms96_delta_summary_compact]的cross-task-safe三seed汇总给出验证集+0.08042、冻结测试+0.07678的HR@1平均差值。k5、k20和k50合计54个seed级差值全部为正，18个协议-划分-指标汇总项也全部呈现3/3 seed正向。

<!-- PARAGRAPH: results.rq4.p02 -->
<!-- EVIDENCE: C6,M5 -->

**EN**

k50 also favors N across seeds, with three-seed HR@1 mean deltas of +0.00990 on validation and +0.01048 on test, but its relation to k5 is metric dependent. For seed43 test, k50 is smaller than k5 for HR@1 (+0.00560 versus +0.00849) and NDCG@5 (+0.00450 versus +0.00489), while its MRR delta is larger. k5 is popularity matched, whereas k20/k50 are random and all three protocols are separately constructed and non-nested. Candidate count, composition, sampling, and difficulty therefore vary jointly; the evidence establishes protocol dependence, not a causal or monotonic candidate-size effect.

**ZH**

k50在各seed上也偏向N，三seed HR@1平均差值在验证与测试上分别为+0.00990和+0.01048，但它与k5的相对关系依指标而变。seed43测试中，k50的HR@1差值（+0.00560）和NDCG@5差值（+0.00450）小于k5（+0.00849和+0.00489），MRR差值则更大。k5采用流行度匹配，k20/k50采用随机候选，三种协议分别构造且非嵌套。候选数量、组成、采样和难度共同变化，因此证据只支持协议依赖性，不支持候选规模的因果或单调效应。
