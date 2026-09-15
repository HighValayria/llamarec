---
title: "21 mock interview answers"
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
# 21 Mock Interview Answers

这是 answer key。回答时不用逐字背，但要守住事实和边界。

## Round 1 Answers

1. 30 秒讲项目：
我用 Llama-3.2-3B + QLoRA 比较 preference supervision、next-item supervision 和 Y/N multi-task supervision。核心发现是喜欢预测和下一次交互预测不是同一种推荐能力；Y 强在 binary preference，N 强在 next-item ranking，M1 是统一折中。进一步用 PopMatch、SASRec sample exposure、MovieLens multi-seed 和 Amazon seed42 检验边界。

2. 最大区别：
不是 demo 一个 LLM 推荐效果，而是系统拆监督语义和评测公平性。

3. Y/N/M：
Y 是 history+target -> Yes/No；N 是 history+candidates -> candidate label；M1 是一个 adapter 混合 Y/N。

4. 为什么 Y/N 不一样：
Y 是 `P(Like)`，N 是 `P(Next Interaction)`。用户可能喜欢多个候选，但下一次交互只有一个。

5. 简单序列：
A(5), B(2), C(4), D(1), E(5)。Y 给每个 target 打 Yes/No；N transitions 是 A->B, A,B->C, A,B,C->D, A,B,C,D->E，低分 item 也合法。

6. 模型方法：
`meta-llama/Llama-3.2-3B-Instruct`，4-bit NF4 QLoRA，LoRA r=16 alpha=32 dropout=0.05。

7. 最稳 conclusion：
Supervision semantics matter；N-style supervision 更适合 next-item ranking；M1 unifies but trades off；LLM-vs-SASRec evidence supports N-K0 sample efficiency, not a complete high-budget frontier。

8. 是否新 architecture：
不是。贡献是任务构造、协议、评测和经验发现。

9. 三点：
Y/N 语义差异；M1 是 tradeoff；SASRec 比较必须按 sample exposure。

10. 一个数字：
MovieLens PopMatch N-K0 HR@1 `0.5447`，因为它是主 hard-candidate LLM ranking anchor。也可说 Y-K0 binary F1 `0.7831` 来代表 Y 能力。

## Round 2 Answers

1. N 不是 next-liked：
代码不看 target rating；ground truth 是 full_sequence 下一次真实交互。

2. 负候选含义：
不是本样本 ground truth 的候选 item，不等于用户不喜欢。

3. Random negatives 太容易：
随机 negatives 往往比 target 冷，popularity shortcut 明显。

4. PopMatch：
按 item popularity 接近 target 选 hard negative pool，再随机采样。

5. Popularity baseline：
Random-k5 下强、PopMatch 下掉，说明 random setting 被 popularity shortcut 污染。

6. BPR-MF：
控制传统协同过滤是否足以解释 LLM 表现。

7. SASRec vs LLM 输入：
SASRec 用 item ID embedding 序列；LLM 用语言化 history/title prompt 和 adapter。

8. full-catalog ranking：
没做，当前 claim 是 fixed-candidate ranking；不能直接声称部署级全库检索能力。

9. k20/k50：
candidate size 是强 stressor；N-K0 和 M1 都下降，N-K0 对 M1 的 gap 变大。

10. order perturbation：
candidate order 有影响但相对小，小于 candidate-size stress。

11. cold/tail 目的：
看差异是否集中在冷门或头部 item。

12. 不能说 cold-start：
coldest bucket 只有 26 samples，只能当诊断信号。

## Round 3 Answers

1. 选 3B：
单卡 24GB 可控，适合系统实验和多 seed。

2. QLoRA：
4-bit 加载 base model，只训练 LoRA adapter。

3. 量化谁：
量化 base model 权重的加载/计算表示，不是把 adapter 量化成训练目标。

4. r/alpha：
r 是低秩 adapter 维度，alpha 是 LoRA scaling。

5. target modules：
`q_proj/k_proj/v_proj/o_proj/gate_proj/up_proj/down_proj`。

6. base 是否更新：
不做全参数微调；训练 LoRA adapter。

7. 保存什么：
PEFT adapter + tokenizer。

8. adapter 加载：
先加载 4-bit base model，再 `PeftModel.from_pretrained(base_model, adapter_dir)`。

9. loss 只算答案：
labels 中 prompt token 是 `-100`，只监督 Yes/No 或 A/B/C answer。

10. score_yesno：
取 Yes/No logits 得连续概率，可算 AUC/F1，而不只是生成文本。

11. score_candidates：
取 A/B/C/... logits softmax，按 label probability 排序。

12. k50 tokenization：
A 到 AX 若不是 single token，就不能直接比较下一 token logits。

## Round 4 Answers

1. 防 leakage：
history 永远 `timestamp < target_timestamp`；candidate files 固定；validation threshold 不在 test 调。

2. same timestamp 危险：
同 timestamp 没真实先后，纳入 history 会泄漏同桶信息。

3. Y/N tie policy：
Y 不需要同桶顺序，所以共享历史；N 需要唯一 next item，所以 ambiguous sample 跳过。

4. candidate files 固定：
保证 Base/Y/N/M/SASRec same-candidate comparison。

5. test threshold：
在 test 上调阈值会用 test label 调参。

6. AUC vs F1：
AUC 不用 threshold，F1 依赖 threshold，validation-calibrated F1 更安全。

7. M1 预算：
M1 N exposure 和 N-K0 都是 12000；M1 总 exposure 更多但分给 Y/N。

8. SASRec step 不公平：
SASRec batch 512，N-K0 effective batch 8，同 steps 曝光差约 64 倍。

9. closest exposure 是否严格公平：
不是，只是 sample exposure diagnostic，不是 compute/FLOPs/capacity match。

10. high SASRec 是否推翻：
不推翻 closest-exposure claim；它说明远多监督的 SASRec 可以超过当前低曝光 N-K0，但没有证明双方 high-exposure 对齐后 SASRec 更强。

11. MovieLens multi-seed：
证明主方向跨 seeds 42/43/44 稳定；不是显著性检验或 compute match。

12. Amazon seed42：
方向复现，不是 Amazon multi-seed，不是大 margin 结论。

13. PopMatch bias：
可能有新 bias，但它减少 random popularity shortcut；且远多监督的 SASRec anchor 也能超过当前 N-K0，非单向偏向 LLM。

14. 显著性：
没有正式显著性检验，有三 seed stability；可补 paired bootstrap/randomization。

15. 可信性：
可信在于 strict temporal protocol、same candidates、hard candidates、baselines、sample exposure、multi-seed、Amazon；边界也明确。

## Round 5 Answers

1. 重新做优先级：
Amazon multi-seed、strict compute/token matching、text ablation。

2. strict compute matching：
记录 token count、FLOPs、wall-clock、GPU、trainable params，并按 matched compute 训练多个 checkpoints。

3. 验证预训练知识：
ID-only prompt、shuffled titles、unseen item/title ablation、metadata removal。

4. 改进 M1：
task weighting、curriculum、separate LoRA、adapter routing、gradient surgery。

5. large candidate：
hard-negative training、k20/k50 training、two-stage retrieval reranking、calibration。

6. Amazon multi-seed 不稳定：
收窄为 MovieLens-stable + Amazon seed42 suggestive，不说 cross-dataset stable。

7. Amazon high SASRec 远超：
强调 N vs M supervision semantics 仍可成立，但 LLM-vs-SASRec positioning 更偏向 high-budget SASRec。

8. empirical study：
因为贡献在系统拆解监督语义和评测协议，而不是新模型结构。

9. 最大限制：
非 strict compute/capacity match；Amazon seed42 only；无机制 ablation。

10. 真实系统扩展：
加入 retrieval stage、full-catalog evaluation、latency/cost、online or replay logging。

11. retrieval stage：
用 SASRec/BPR/ANN 召回，再 LLM rerank，评测 recall+reringing。

12. TALLRec 比较：
TALLRec 偏 Yes/No recommendation tuning；本项目继承 Y-style idea，但新增 N 和 M 监督语义比较。

13. LLMRank 比较：
LLMRank 多关注 zero-shot ranking factors；本项目核心是 tuning supervision semantics，也做 candidate order/popularity/candidate size 相关诊断。

14. sample exposure 类比：
step 像“上了多少节课”，batch size 像“每节课看多少题”，sample exposure 是“总共看了多少题”。

15. 研究方法：
先拆清标签语义，再固定协议比较；发现 baseline 不公平后换预算轴；最后用 robustness 和边界声明保护结论。
