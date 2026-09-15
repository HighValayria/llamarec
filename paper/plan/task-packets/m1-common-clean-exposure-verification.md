# M1 Common-Clean 48k to 96k Exposure Verification

日期：2026-09-11  
裁决：`COMMON_CLEAN_NARROWING_CONFIRMED`

## 1. 范围与口径

本审计只复用已有seed42 prediction与既有M1-48/M1-96 clean mask。未训练、未推理、未bootstrap、未重建候选，也未修改manuscript、tables或claim map。

对validation和test分别取：

```text
common_clean_mask = M1-48 clean mask AND M1-96 clean mask
```

然后将N48、M1-48、N96和M1-96过滤到完全相同的`(user_id, ground_truth_movie_id)`集合。四组prediction的用户、目标、候选列表和候选顺序完全一致；协议均验证为`PopMatch-k5`、`k5_popmatch_seed42`。

## 2. Mask关系

| Split | M1-48 clean | M1-96 clean | Intersection | M1-48 only | M1-96 only | Relationship |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| validation | 5,494 | 5,318 | 5,318 | 176 | 0 | M1-96是M1-48的严格子集 |
| test | 5,600 | 5,535 | 5,535 | 65 | 0 | M1-96是M1-48的严格子集 |

两组mask并不相同。实际验证表明，本批数据中M1-96 clean mask确实是M1-48 clean mask的子集；这一关系来自集合检查，不是预先假设。

## 3. Validation主判断

所有模型均在相同的5,318个common-clean样本上计算。`gap48=N48-M1-48`，`gap96=N96-M1-96`，`gap_change=gap96-gap48`；负值表示gap narrowing。

| Metric | N48 | M1-48 | gap48 | N96 | M1-96 | gap96 | gap_change | Result |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| HR@1 | 0.603234 | 0.592516 | +0.010718 | 0.622226 | 0.620910 | +0.001316 | -0.009402 | narrowing |
| NDCG@5 | 0.819997 | 0.814508 | +0.005489 | 0.829615 | 0.827845 | +0.001770 | -0.003719 | narrowing |
| MRR | 0.759527 | 0.752250 | +0.007277 | 0.772333 | 0.770036 | +0.002297 | -0.004980 | narrowing |

validation的三个主要ranking metric均支持narrowing。相较48k gap，HR@1、NDCG@5和MRR的gap分别约缩小87.7%、67.8%和68.4%。这是点估计关系，不作显著性推断。

## 4. Test方向检查

所有模型均在相同的5,535个common-clean样本上计算。

| Metric | N48 | M1-48 | gap48 | N96 | M1-96 | gap96 | gap_change | Result |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| HR@1 | 0.585005 | 0.575610 | +0.009395 | 0.607407 | 0.593677 | +0.013731 | +0.004336 | widening |
| NDCG@5 | 0.809522 | 0.804988 | +0.004534 | 0.820437 | 0.814388 | +0.006049 | +0.001515 | widening |
| MRR | 0.745748 | 0.739735 | +0.006013 | 0.760277 | 0.752207 | +0.008070 | +0.002057 | widening |

test的三个metric均不支持narrowing，而是出现小幅widening。按照本任务预先指定的判断纪律，test只作为held-out directional check；该分歧必须保留，但不自动推翻以validation trajectory为主的结论。

## 5. Verdict

`COMMON_CLEAN_NARROWING_CONFIRMED`

理由：在严格相同的validation common-clean subset上，HR@1、NDCG@5和MRR三项均显示48k到96k的specialist-M1 gap明显收窄。test三项均未复现该关系，因此裁决只确认原先的**seed42 validation-based trajectory claim**，不确认跨split普遍规律，也不进行显著性或机制推断。

## 6. Execution Record

- training required: `NO`
- inference required: `NO`
- bootstrap performed: `NO`
- candidate regeneration: `NO`
- manuscript modifications: `0`
