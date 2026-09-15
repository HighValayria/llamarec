---
id: rq3_multitask_unification
title:
  en: Specialist and Multitask Models at Matched Per-Task Exposure
  zh: 每任务曝光对齐下的专家与多任务模型
status: draft
---

<!-- PARAGRAPH: results.rq3.p01 -->
<!-- EVIDENCE: C4,M3 -->

**EN**

At 96k expected exposure per task, M1 maintains comparable Y-side preference performance across the three evaluated training seeds. Validation AUC and F1 point estimates are slightly higher for M1-Y in each seed; accuracy is higher in seeds 42 and 43 but lower by 0.00089 in seed44. Test AUC, F1, and accuracy point estimates are slightly higher for M1-Y in all three seeds. For seed42 validation, the M1-Y minus Y96 differences are +0.00248 AUC, +0.00553 F1, and +0.00460 accuracy. Of their 95% paired bootstrap intervals, only fixed-threshold F1 is positive, at [+0.00096, +0.01025]; the AUC and accuracy intervals cross zero. These observations support preservation of the measured preference capability at 96k, without establishing positive transfer across training seeds. [TABLE: ms96_main_validation] [TABLE: ms96_main_test] [TABLE: specialist_multitask]

**ZH**

在每任务预期曝光96k时，M1在三个已评估训练种子下保持了与Y专家接近的偏好表现。各seed的M1-Y验证AUC与F1点估计均略高；Accuracy在seed42和43上较高，在seed44上则低0.00089。三个seed的测试AUC、F1和Accuracy点估计均为M1-Y略高。seed42验证集上，M1-Y减Y96的差值分别为AUC +0.00248、F1 +0.00553和Accuracy +0.00460。在相应的95%配对bootstrap区间中，只有固定阈值下的F1区间为正，为[+0.00096, +0.01025]；AUC与Accuracy区间均跨零。这些观察支持96k时保留了被测偏好能力，但不构成跨训练种子正迁移的证据。[TABLE: ms96_main_validation] [TABLE: ms96_main_test] [TABLE: specialist_multitask]

<!-- PARAGRAPH: results.rq3.p02 -->
<!-- EVIDENCE: C5,M3 -->

**EN**

The seed42 trajectory shows a marked reduction in the standard-k5 validation gap from 48k to 96k per task. N48 and M1-48 achieve 0.6030 and 0.5942 HR@1, compared with 0.6238 and 0.6234 for N96 and M1-96. At 96k, seed42 N-M differences in HR@1, NDCG@5, and MRR are +0.00035, +0.00115, and +0.00149, with all three 95% paired bootstrap intervals crossing zero; the HR@1 interval is [-0.01040, +0.01128]. Independent runs with seeds 43 and 44 reproduce a small-gap regime at 96k, with validation HR@1 differences of +0.00264 and +0.01463. The three-seed mean HR@1 difference is +0.00587, with sample standard deviation 0.00767. This replication concerns the 96k operating point; the exposure-dependent narrowing is established on the seed42 validation trajectory, and its zero-crossing intervals do not establish equivalence. [TABLE: exposure_scaling] [TABLE: ms96_delta_summary]

**ZH**

seed42轨迹显示，每任务曝光从48k提高到96k时，标准k5验证差距明显缩小。N48与M1-48的HR@1分别为0.6030和0.5942，N96与M1-96则为0.6238和0.6234。在96k时，seed42的HR@1、NDCG@5和MRR的N-M差值分别为+0.00035、+0.00115和+0.00149，三个对应的95%配对bootstrap区间均跨零，其中HR@1区间为[-0.01040, +0.01128]。seed43和44的独立训练在96k复现了小差距区间，验证HR@1差值分别为+0.00264和+0.01463。三个seed的HR@1平均差值为+0.00587，样本标准差为0.00767。这一复现针对96k运行点；随曝光收窄的证据来自seed42验证轨迹，而跨零区间不构成等价性证明。[TABLE: exposure_scaling] [TABLE: ms96_delta_summary]

<!-- PARAGRAPH: results.rq3.p03 -->
<!-- EVIDENCE: C4,C5 -->

**EN**

The frozen test set consistently retains a modest N-specialist advantage at 96k. N96 exceeds M1-N on all three ranking metrics in every evaluated seed. The mean N-M differences are +0.01016 HR@1, +0.00501 NDCG@5, and +0.00665 MRR, with sample standard deviations 0.00247, 0.00058, and 0.00081 across the three training seeds. For seed42, the HR@1 difference is +0.01269 with a 95% paired bootstrap interval [+0.00159, +0.02379]; its NDCG@5 and MRR intervals are also positive. The corresponding seed42 test HR@1 gap is +0.00934 at 48k, so the validation trajectory's narrowing does not extend to this test comparison. At 96k, the combined evidence describes preserved Y-side performance and a small, remaining k5 ranking gap, whose reach under alternative candidate protocols is examined next. [TABLE: ms96_main_test] [TABLE: ms96_delta_summary] [TABLE: hard_candidate]

**ZH**

冻结测试集在96k时一致保留N专家的小幅优势。每个已评估seed的三个排序指标均为N96高于M1-N。N-M的平均差值分别为HR@1 +0.01016、NDCG@5 +0.00501和MRR +0.00665，三个训练seed间的样本标准差依次为0.00247、0.00058和0.00081。seed42的HR@1差值为+0.01269，95%配对bootstrap区间为[+0.00159, +0.02379]，NDCG@5与MRR区间也为正。对应的seed42测试HR@1差距在48k为+0.00934，因此验证轨迹上的收窄并未延伸到这一测试比较。综合96k证据，M1保留了Y侧表现，k5排序仍有较小差距；下文考察这一关系在其他候选协议下的适用范围。[TABLE: ms96_main_test] [TABLE: ms96_delta_summary] [TABLE: hard_candidate]
