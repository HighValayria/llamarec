---
title: "09 popmatch and robustness"
type: report
status: current
authority: descriptive
source: agent
created: 2026-08-23
updated: 2026-08-23
last_verified: 2026-08-23
related_code:
  - configs/experiment.yaml
  - src/eval/candidate_sets.py
  - src/data/negative_sampling.py
  - src/analysis/candidate_set_diagnostics.py
  - src/analysis/phase2c_result_summary.py
  - src/analysis/phase2a_robustness_report.py
---

# 09 PopMatch And Robustness

## 先说结论

[FACT] 当前项目里的 PopMatch 是 **hard-candidate evaluation protocol**，不是训练阶段的 hard-negative training。

它做的事是：

```text
固定 N validation/test samples
        |
        v
对每个 ground-truth next item
找 popularity 接近它的 negative items
        |
        v
组成 5-candidate set
        |
        v
让 Base / Y-K0 / N-K0 / M1 / baselines
在同一候选文件上评测 ranking
```

[INTERPRETATION] PopMatch 的目的不是“让模型训练得更难”，而是“让评测别太容易”。它减少 Random-k5 里靠 item popularity 就能做对的 shortcut。

## 为什么 Random-k5 不够

Random-k5 的候选集合是：

```text
1 个真实 next item
+ 4 个随机 negative items
```

在 MovieLens 这类数据里，真实 next item 往往更热门，而随机 negative 很可能很冷。这样模型可能不用真正理解用户序列，只要偏向热门 item 就能拿到不错 ranking。

[FACT] Phase 2C 诊断里，MovieLens canonical random candidate 的 test mean absolute target-negative popularity gap 约 `663.5850`。

这意味着：

```text
target popularity
和
negative popularity
差得很远
```

所以 Random-k5 更像一个 easy-negative protocol。它可以作为参考，但不适合作最终主 ranking claim。

## PopMatch-k5 到底怎么构造

核心代码：

```text
src/eval/candidate_sets.py
  sample_popularity_matched_negatives(...)
```

代码逻辑是：

```text
target_movie_id
        |
        v
读取 target popularity
        |
        v
从 all_movie_ids 中排除 target 本身
        |
        v
按 abs(negative_popularity - target_popularity) 排序
        |
        v
取最接近的一小段 hard pool
        |
        v
从 hard pool 随机采 4 个 negatives
        |
        v
和 target 一起 shuffle 成 A/B/C/D/E
```

更贴近代码的伪代码：

```python
pool = all_items - {target_item}
target_pop = popularity[target_item]

ranked_pool = sorted(
    pool,
    key=lambda item: (
        abs(popularity[item] - target_pop),
        item,
    ),
)

hard_pool = ranked_pool[:negative_num * candidate_pool_multiplier]
negatives = random_sample(hard_pool, negative_num)
candidates = shuffle([target_item] + negatives)
```

[FACT] 当前实现默认 `candidate_pool_multiplier=10`，k5 时 negative_num 是 4，所以会先找 popularity 最接近 target 的最多 40 个候选，再从里面随机采 4 个。

## Popularity 从哪里来

代码入口：

```text
src/eval/candidate_sets.py
  _load_movie_popularity(...)
```

[FACT] 当前实现从 `full_sequences` 统计 item 出现次数，作为 item popularity。

面试里要谨慎说：

[FACT] 当前 PopMatch 是 fixed evaluation candidate protocol。

[INTERPRETATION] 它用于诊断和控制 popularity shortcut，而不是线上部署时的无泄漏候选生成器。

[HYPOTHESIS] 如果要做更严格的生产级或审稿更强版本，可以改成只用 train split 统计 popularity，再复跑 PopMatch。

## PopMatch 和 hard-negative training 的区别

PopMatch hard candidates:

```text
只影响 evaluation candidate files
不改变 Y/N/M 训练样本
不重新训练 adapter
不把 hard negatives 加入训练 loss
```

Hard-negative training:

```text
会把更难的 negatives 放进训练样本
会改变训练分布
可能改变模型能力
属于新的方法或实验阶段
```

[FACT] Phase 2C PopMatch 阶段没有训练新模型。它复用已有 Base/Y/N/M adapter，在 `k5_popmatch_seed42` candidate files 上重新评测。

面试表述：

> 我这里做的是 hard-candidate robustness evaluation，不是 hard-negative training。这样做的好处是可以隔离评测协议的影响：模型不变，只换 candidate difficulty，看结论是否还成立。

## PopMatch 文件长什么样

候选文件路径：

```text
data/candidates/{dataset}/variants/k5_popmatch_seed42/valid.jsonl
data/candidates/{dataset}/variants/k5_popmatch_seed42/test.jsonl
```

每条 record 的关键字段：

```text
user_id
history
target
candidate_movie_ids
ground_truth_movie_id
ground_truth_index
label
label_set
candidate_generation
```

其中：

```text
candidate_movie_ids = [候选 item ids]
ground_truth_index = 真实 next item 在候选数组中的位置
label = label_set[ground_truth_index]
```

模型最后不是猜 item id，而是猜 `A/B/C/D/E`。

## PopMatch 为什么更适合作主 ranking claim

Random-k5 的问题：

```text
negative 太随机
popular target vs cold negative 差距大
Popularity/BPR 可能靠 shortcut 很强
```

PopMatch-k5 的改进：

```text
target 和 negative popularity 接近
更难只靠热门程度判断
更能测试 history + candidate matching
```

[FACT] MovieLens PopMatch test mean absolute popularity gap 是 `44.0283`，random test gap 约 `663.5850`。

[FACT] Amazon PopMatch-k5 test mean absolute popularity gap 是 `29.3607`，Random-k5 seed42 是 `130.7514`。

[INTERPRETATION] 因此，PopMatch 更适合作“主 ranking evidence”；Random-k5 更适合作 easy-negative reference。

## PopMatch 主要结果怎么讲

MovieLens-1M PopMatch-k5：

```text
Y-K0 P(Yes) ranking HR@1: 0.1854
N-K0 HR@1:                 0.5447
M1 HR@1:                   0.5244
```

解释：

[FACT] N-K0 仍高于 M1，Y-K0 的 `P(Yes)` ranking 明显弱。

[INTERPRETATION] 这支持两个结论：第一，preference score 不能替代 next-item score；第二，M1 是 unified tradeoff，不是 ranking specialist 的替代。

Amazon Musical Instruments PopMatch-k5：

```text
Base HR@1:          0.3573
Y-K0 ranking HR@1: 0.2298
N-K0 HR@1:         0.4669
M1 HR@1:           0.4582
SASRec-exp HR@1:   0.1757
```

解释：

[FACT] N-K0 方向上仍高于 M1，并明显高于 closest-exposure SASRec。

边界：

[FACT] Amazon 只有 seed42，且 N-K0 over M1 margin 小，HR@1 `+0.0087`。只能说 directional replication。

## k20 / k50 是另一种 hard-candidate stress

PopMatch 控制的是：

```text
candidate popularity difficulty
```

k20/k50 控制的是：

```text
candidate set size difficulty
```

从 k5 到 k20/k50，模型要在更多候选中找真实 next item，chance level 更低，label competition 更强。

MovieLens Phase 2A 关键数字：

```text
N-K0 k20 HR@1: 0.4164
M1   k20 HR@1: 0.3711

N-K0 k50 HR@1: 0.1995
M1   k50 HR@1: 0.1219
```

[FACT] N-K0 和 M1 都随 candidate size 增大而下降，但 N-K0 对 M1 的优势在 k50 变大。

[INTERPRETATION] 这说明 candidate-size expansion 是强 stressor，也说明 ranking claim 必须报告 candidate protocol。

## Candidate order perturbation 是什么

candidate order perturbation 做的是：

```text
保留同一批 candidate ids
重新打乱 A/B/C/D/E 位置
看模型是否对候选位置敏感
```

[FACT] Phase 2A 报告里，candidate order effect 相对较小；k20 最大绝对 HR@1 delta 是 `0.0065`。

面试说法：

> LLM 确实可能有 candidate position bias，所以我做了 order perturbation。结果显示它有影响，但相对 candidate-size expansion 小得多。

不要说：

```text
candidate order 完全没有影响
```

要说：

```text
有影响，但在当前实验里不是主导 stressor
```

## 为什么 PopMatch 后 Popularity / BPR 会掉

Random-k5 下：

```text
target 往往更热门
negative 往往更冷
```

所以 Popularity baseline 和 BPR-MF 容易表现强。

[FACT] MovieLens Random-k5 上，BPR-MF test HR@1 是 `0.5611`；PopMatch-k5 下掉到 `0.3352`。

[INTERPRETATION] 这说明 Random-k5 的 ranking 结果有明显 popularity shortcut，不能单独作为主结论。

## PopMatch 会不会对 LLM 有利

简短答法：

> 不排除 PopMatch 本身是一种人为 protocol，但它不是专门给 LLM 放水；远多监督的 SASRec 在 MovieLens PopMatch 下也能超过当前 N-K0 checkpoint。

展开：

[FACT] MovieLens SASRec s3000 PopMatch HR@1 是 `0.6243`，高于当前 N-K0 的 `0.5466`，但二者 exposure 分别约 `1.53M` 与 `12k`。

[INTERPRETATION] 如果 PopMatch 是单向偏向 LLM 的 protocol，远多监督的 SASRec 不应该在同一 PopMatch setting 下表现这么强。更合理的解释是：PopMatch 去掉了 easy popularity shortcut，让不同模型在更难的 same-candidate setting 下比较。

## 面试常用回答模板

如果被问“PopMatch 是怎么构造的？”

回答：

> 对每个 N validation/test 样本，我保留真实 next item 作为 ground truth，然后从全 item pool 里排除它。接着用 item popularity 找和 target popularity 最接近的一批 candidate negatives，再从这批 hard pool 里随机采 4 个，和 target 一起 shuffle 成 A/B/C/D/E。这样 Base、Y、N、M 和 baselines 都在同一固定 candidate file 上评测。

如果被问“这是不是 hard negative training？”

回答：

> 不是。这里是 hard-candidate evaluation。模型训练没变，只是换了 validation/test candidate files。它回答的是模型在更难候选集上是否仍然成立，而不是训练时加入 hard negatives 后性能会不会提高。

如果被问“为什么 PopMatch 更公平？”

回答：

> 它不代表所有公平性都解决了，但它减少了一个明确问题：random negatives 和 target popularity 差距过大。MovieLens random test gap 大约 663.6，PopMatch 降到 44.0，所以它更适合作主 ranking claim。

如果被问“PopMatch 有什么边界？”

回答：

> 第一，它是 fixed-candidate evaluation，不是 full-catalog ranking。第二，当前 popularity 统计来自 full sequences，所以更严格版本可以改成 train-only popularity。第三，它只控制 popularity 这一种难度，不等于覆盖所有 hard negative 类型。

## 一句话记忆

PopMatch 不是训练模型更难，而是评测模型更公平：把 random easy negatives 换成 popularity 接近 target 的 hard candidates，检查 N-K0、M1 和 baselines 的 ranking 结论是否还能站住。
