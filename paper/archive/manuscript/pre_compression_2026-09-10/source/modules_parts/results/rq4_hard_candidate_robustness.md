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

The k20 protocol reveals a substantially larger N-specialist advantage than standard k5 in all three evaluated training seeds. At 96k, every validation and frozen-test comparison favors N96 over M1-N on HR@1, NDCG@5, and MRR. Validation HR@1 differences are +0.11242, +0.08141, and +0.05110 for seeds 42, 43, and 44; the mean is +0.08164 with sample standard deviation 0.03066. The corresponding test mean is +0.07765 with sample standard deviation 0.03448. For seed42, the 95% paired bootstrap intervals for all three metrics are positive on both splits, including [+0.10185, +0.12317] for validation HR@1. Thus, the small k5 gap coexists with a pronounced k20 gap at the same per-task exposure. [TABLE: ms96_protocol_validation] [TABLE: ms96_protocol_test] [TABLE: hard_candidate]

**ZH**

k20协议在三个已评估训练种子下均显示出明显大于标准k5的N专家优势。在96k时，验证集和冻结测试集的每组HR@1、NDCG@5及MRR比较均为N96高于M1-N。seed42、43和44的验证HR@1差值依次为+0.11242、+0.08141和+0.05110，均值为+0.08164，样本标准差为0.03066；对应测试均值为+0.07765，样本标准差为0.03448。seed42在两个划分上三个指标的95%配对bootstrap区间均为正，其中验证HR@1区间为[+0.10185, +0.12317]。因此，在相同每任务曝光下，较小的k5差距与明显的k20差距同时存在。[TABLE: ms96_protocol_validation] [TABLE: ms96_protocol_test] [TABLE: hard_candidate]

<!-- PARAGRAPH: results.rq4.p02 -->
<!-- EVIDENCE: C6 -->

**EN**

The k50 protocol also consistently favors N, but with a smaller gap than k20 and seed-dependent magnitude. All three ranking differences are positive in each seed on both splits. Validation HR@1 differences range from +0.00335 to +0.01709, with mean +0.01028 and sample standard deviation 0.00687; test differences range from +0.00511 to +0.01392, with mean +0.01010 and sample standard deviation 0.00452. For seed42, all three 95% paired bootstrap intervals are positive on both splits, including [+0.01251, +0.02185] for validation HR@1. The k50 gap is not uniformly larger than k5: seed43 test HR@1 differences are +0.00511 and +0.00775, respectively. The specialist advantage persists, but its magnitude does not increase monotonically with candidate count. [TABLE: ms96_delta_summary] [TABLE: hard_candidate]

**ZH**

k50协议也一致偏向N，但差距小于k20，幅度随seed变化。两个划分中，每个seed的三个排序差值均为正。验证HR@1差值范围为+0.00335至+0.01709，均值+0.01028、样本标准差0.00687；测试差值范围为+0.00511至+0.01392，均值+0.01010、样本标准差0.00452。seed42在两个划分上的三个95%配对bootstrap区间均为正，其中验证HR@1区间为[+0.01251, +0.02185]。k50差距并不总大于k5，例如seed43测试HR@1差值分别为+0.00511和+0.00775。专家优势的方向得以保持，但其幅度没有随候选数量单调增大。[TABLE: ms96_delta_summary] [TABLE: hard_candidate]

<!-- PARAGRAPH: results.rq4.p03 -->
<!-- EVIDENCE: C6,M5 -->

**EN**

The N-M1 relationship is therefore protocol-conditioned. Standard k5 uses five popularity-matched candidates, whereas k20 and k50 use 20 and 50 randomly sampled candidates. All use candidate-generation seed42, distinct from the three training seeds. These separately constructed sets are non-nested, so count, composition, sampling method, and difficulty vary jointly rather than isolate a candidate-size effect. Another condition of relative model performance is the downstream supervision exposure received by the sequential baseline.

**ZH**

因此，N与M1的关系受协议条件限定。标准k5使用五个流行度匹配候选，k20和k50则使用20与50个随机采样候选。候选生成均使用seed42，与三个训练种子分开记录。这些独立构造的集合非嵌套，数量、组成、采样方法与难度共同变化，并未单独识别候选规模效应。影响模型相对表现的另一项条件，是序列基线实际获得的下游监督曝光。
