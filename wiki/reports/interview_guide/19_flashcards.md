---
title: "19 flashcards"
type: report
status: current
authority: descriptive
source: agent
created: 2026-08-23
updated: 2026-08-23
last_verified: 2026-08-23
related_code:
  - configs/experiment.yaml
  - src/data/build_step2.py
  - src/data/split.py
  - src/data/build_preference.py
  - src/data/build_next_item.py
  - src/eval/candidate_sets.py
  - src/eval/ranking_metrics.py
  - src/eval/binary_metrics.py
  - src/train/train_y.py
  - src/train/train_n.py
  - src/train/train_m.py
  - src/inference/scoring.py
  - src/inference/evaluate_y_adapter.py
  - src/inference/evaluate_n_adapter.py
  - src/inference/evaluate_m_adapter.py
---
# 19 Flashcards

用法：看 Q，先闭眼答，再看 A。不要顺读。

## Card 1

Q:
LlamaRec 的一句话问题是什么？

A:
它问 preference prediction 和 next-interaction prediction 是否让同一个 LLM 学到同一种推荐能力，并用 Y/N/M、hard candidates、SASRec sample exposure、multi-seed 和 Amazon 验证边界。

## Card 2

Q:
Y-K0 的概率语义是什么？

A:
`P(Like | History, Target Item)`。

## Card 3

Q:
N-K0 的概率语义是什么？

A:
`P(Next Interaction Candidate Label | History, Candidate Set)`。

## Card 4

Q:
M1 是什么？

A:
一个 Y+N multi-task adapter，按 1:1 interleaving 混合 Y 和 N 样本训练，评测时分别走 Y 和 N 接口。

## Card 5

Q:
为什么 N target 不是 next positive item？

A:
因为 N 的 ground truth 是 full sequence 里的下一次真实交互，不按 rating 过滤。低 rating interaction 仍然是用户实际发生的下一步行为。

## Card 6

Q:
`rating >= 4` 在项目里表示什么？

A:
Y 任务的 `Yes` label；`rating < 4` 是 `No`。这个阈值只定义 preference label，不过滤 N target。

## Card 7

Q:
strict temporal protocol 的核心规则是什么？

A:
history 只能包含 `timestamp < target_timestamp` 的 interactions。

## Card 8

Q:
为什么不能用 `timestamp <= target_timestamp`？

A:
同 timestamp 没有真实先后顺序，`<=` 可能把 target 或同桶未来信息放入 history，造成泄漏。

## Card 9

Q:
Y 怎么处理同 timestamp 多个 target？

A:
它们共享同一段严格历史，因为 Y 不需要判断同桶内先后顺序。

## Card 10

Q:
N 怎么处理同 timestamp 多个 next item？

A:
如果 next timestamp bucket 不是 singleton，只跳过这个 ambiguous N sample，不跳过整个 user。

## Card 11

Q:
A(5), B(2), C(4), D(1), E(5) 的 N transitions 是什么？

A:
`A -> B`, `A,B -> C`, `A,B,C -> D`, `A,B,C,D -> E`。B 和 D 低 rating 也合法。

## Card 12

Q:
Y 的 `P(Yes)` 为什么可以排序候选？

A:
可以对每个 candidate 单独构造 Y prompt，计算 `P(Yes)`，再按这个偏好分数排序。

## Card 13

Q:
为什么 Y 的 `P(Yes)` ranking 不等于 N ranking？

A:
Y 分数是喜欢概率；N 分数是候选在当前集合中成为下一次交互的概率。喜欢多个 item 不等于下一次只交互哪个 item。

## Card 14

Q:
N 为什么输出 A/B/C/D/E，而不是生成 item title？

A:
候选 label 更稳定，能直接取 single-token logits 做概率比较，避免生成长 title 的不确定性。

## Card 15

Q:
score_yesno() 做什么？

A:
取 prompt 后 `Yes/No` token logits，softmax 得到 `P(Yes)` 和 `P(No)`。

## Card 16

Q:
score_candidates() 做什么？

A:
取 A/B/C/... candidate label logits，softmax 得到每个候选 label 的概率。

## Card 17

Q:
为什么不能只看生成字符串？

A:
评测 AUC 和 ranking 需要连续分数；生成字符串只给离散答案，信息太少。

## Card 18

Q:
k50 为什么要 tokenizer check？

A:
因为 A 到 AX 如果不是 single token，就不能简单用下一 token logits 比较，需要 sequence likelihood。

## Card 19

Q:
当前 base model 是什么？

A:
`meta-llama/Llama-3.2-3B-Instruct`。

## Card 20

Q:
当前 QLoRA 关键配置是什么？

A:
4-bit NF4，LoRA r=16，alpha=32，dropout=0.05，target modules 包括 attention 和 MLP projection。

## Card 21

Q:
训练结束保存什么？

A:
PEFT adapter 和 tokenizer，不保存完整全参数 base model。

## Card 22

Q:
base model 权重是否变化？

A:
训练对象是 LoRA adapter 参数；base model 以 4-bit 加载并作为底座，不做全参数微调。

## Card 23

Q:
训练时 labels 为什么有很多 `-100`？

A:
为了只在答案 token 上计算 loss，不监督 prompt token。

## Card 24

Q:
M1 的 1:1 是什么？

A:
Y/N 样本 interleaving ratio，不是 compute 严格相同，也不是 N 上训练两倍。

## Card 25

Q:
M1 3000 steps 为什么不能说比 N-K0 多训练一倍？

A:
M1 的 steps 分给 Y 和 N；正式表格里 M1 N exposure 是 12000，和 N-K0 anchor 一样，总 exposure 是 24000。

## Card 26

Q:
为什么 M1 是 unified tradeoff？

A:
它能同时做 binary 和 ranking，但 ranking 没超过 N-K0，binary 也只是接近 Y-K0。

## Card 27

Q:
MovieLens Y-K0 binary F1 关键数字是多少？

A:
`0.7831`。

## Card 28

Q:
MovieLens M1 binary F1 关键数字是多少？

A:
`0.7818`。

## Card 29

Q:
MovieLens PopMatch-k5 N-K0 HR@1 是多少？

A:
`0.5447`。

## Card 30

Q:
MovieLens PopMatch-k5 M1 HR@1 是多少？

A:
`0.5244`。

## Card 31

Q:
MovieLens PopMatch-k5 Y-K0 P(Yes) ranking HR@1 是多少？

A:
`0.1854`。

## Card 32

Q:
MovieLens k50 N-K0 vs M1 HR@1 是多少？

A:
N-K0 `0.1995`，M1 `0.1219`。

## Card 33

Q:
Random-k5 为什么不是主 ranking claim？

A:
random negatives 太容易，target 和 negatives popularity 差距大，容易产生 popularity shortcut。

## Card 34

Q:
PopMatch 解决什么问题？

A:
选 popularity 接近 target 的 negatives，减少靠热门程度区分 candidate 的 shortcut。

## Card 35

Q:
MovieLens PopMatch test popularity gap 大约是多少？

A:
约 `44.0`，而 random test gap 约 `663.6`。

## Card 36

Q:
SASRec 是什么？

A:
基于 self-attention 的 specialized sequential recommender，用 item ID 序列预测下一项。

## Card 37

Q:
为什么 SASRec step-aligned 比较不公平？

A:
同样 1500 steps 下，SASRec batch 512，N-K0 effective batch 8，SASRec sample exposure 大约是 N-K0 的 63.952 倍。

## Card 38

Q:
MovieLens N-K0 closest exposure HR@1 是多少？

A:
`0.5466`。

## Card 39

Q:
MovieLens SASRec closest exposure HR@1 是多少？

A:
`0.2700`。

## Card 40

Q:
MovieLens SASRec high exposure s3000 HR@1 是多少？

A:
`0.6243`。

## Card 41

Q:
sample exposure match 是否等于 compute match？

A:
不是。sample exposure 只对齐训练样本数，不对齐 FLOPs、token count、参数量或 wall-clock。

## Card 42

Q:
multi-seed 固定了什么，变化了什么？

A:
固定 `k5_popmatch_seed42` candidate protocol，变化训练 seeds 42/43/44。

## Card 43

Q:
MovieLens multi-seed 中 N-K0 over M1 最小 HR@1 margin 是多少？

A:
`0.0104`。

## Card 44

Q:
MovieLens Y-K0 binary F1 seed range 是多少？

A:
约 `0.0098`。

## Card 45

Q:
Amazon Musical Instruments 规模是多少？

A:
57,439 users，24,584 items，511,792 interactions。

## Card 46

Q:
Amazon PopMatch N-K0 HR@1 是多少？

A:
`0.4669`。

## Card 47

Q:
Amazon PopMatch M1 HR@1 是多少？

A:
`0.4582`。

## Card 48

Q:
Amazon PopMatch SASRec exp-match HR@1 是多少？

A:
`0.1757`。

## Card 49

Q:
Amazon 结果最大的边界是什么？

A:
只有 seed42，不能说 Amazon multi-seed stability；N-K0 over M1 margin 也很小。

## Card 50

Q:
面试里最危险的一句话是什么？

A:
“LLM 全面打败 SASRec”。正确说法是：closest exposure 下 N-K0 更强；远多监督的 SASRec 超过当前 N-K0；完整 high-budget head-to-head 没做。
