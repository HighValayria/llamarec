# 定向检索日志

日期：2026-09-07。先核已有8篇，再围绕缺口扩展；不以关键词未命中证明没有前人。

## 1. 已有原文

对应缺口：INSTRUCTION_TASK_DETAILS, RATING_TARGETS, SAMPLING_EFFECT_DETAILS, JOINT_CONDITIONING_COVERAGE。

- `"Recommendation as Language Processing" P5 pdf`；限制域：arxiv.org, dl.acm.org, yongfeng.me
- `"TALLRec" "2305" arxiv`；限制域：arxiv.org, dl.acm.org
- `"Self-Attentive Sequential Recommendation" pdf`；限制域：arxiv.org, cseweb.ucsd.edu
- `"On Sampled Metrics for Item Recommendation" pdf`；限制域：arxiv.org, research.google, dl.acm.org



## 2. 已有原文

对应缺口：INSTRUCTION_TASK_DETAILS, SAMPLING_EFFECT_DETAILS, EXPOSURE_BUDGET_COMPARISONS。

- `"TALLRec: An Effective and Efficient" arxiv`；限制域：arxiv.org
- `"On Target Item Sampling" pdf`；限制域：uam.es, dl.acm.org
- `"A Case Study on Sampling Strategies" Dallmann pdf`；限制域：arxiv.org, uni-wuerzburg.de, dl.acm.org
- `"Revisiting the Performance of iALS" "Are We Really Making Much Progress"`；限制域：arxiv.org



## 3. 已有原文

对应缺口：SAMPLING_EFFECT_DETAILS, EXPOSURE_BUDGET_COMPARISONS。

- `"On Target Item Sampling in Offline Recommender System Evaluation"`
- `"Are We Really Making Much Progress" arxiv`
- `"Revisiting the Performance of iALS" arxiv`



## 4. 已有原文纠正定位

对应缺口：SAMPLING_EFFECT_DETAILS。

- `"On Sampled Metrics for Item Recommendation" Krichene Rendle arxiv pdf`；限制域：arxiv.org, research.google, storage.googleapis.com, dl.acm.org

一个未确认arXiv地址返回无关物理论文，已排除，不入库；后续仅使用原文页给出的链接。

## 5. 已有原文补取

对应缺口：SAMPLING_EFFECT_DETAILS。

- `"On Sampled Metrics for Item Recommendation" filetype:pdf`



## 6. P0近邻

对应缺口：JOINT_CONDITIONING_COVERAGE。

- `"LLM recommendation" "instruction tuning" "training data" "evaluation" benchmark`；限制域：arxiv.org, aclanthology.org, dl.acm.org, openreview.net
- `"LLM recommendation" "multitask" "sample" "candidate"`；限制域：arxiv.org, aclanthology.org, dl.acm.org, openreview.net
- `"recommendation" "supervision" "data scale" "large language models"`；限制域：arxiv.org, aclanthology.org, dl.acm.org, openreview.net



## 7. P0近邻收窄索引

对应缺口：JOINT_CONDITIONING_COVERAGE。

- `large language model recommendation instruction tuning task data scale evaluation candidate benchmark`；限制域：arxiv.org
- `recommendation language model multitask single-task data allocation exposure`；限制域：arxiv.org
- `LLM recommender training data size evaluation protocols empirical study`；限制域：arxiv.org

前次组合返回会议目录噪声，未纳入；本次限定原始论文arXiv索引。

## 8. 统一多任务与曝光预算

对应缺口：JOINT_CONDITIONING_COVERAGE, UNIFIED_TASK_ALLOCATION, EXPOSURE_BUDGET_COMPARISONS。

- `"OneRec" recommendation arxiv`；限制域：arxiv.org
- `recommendation "multitask" "data mixing" LLM`；限制域：arxiv.org
- `LLM recommendation "data scaling" fine tuning empirical`；限制域：arxiv.org



## 9. 近邻预算边界

对应缺口：UNIFIED_TASK_ALLOCATION, EXPOSURE_BUDGET_COMPARISONS。

- `"OpenOneRec" arxiv`；限制域：arxiv.org
- `"recommendation" "fine-tuning" "data efficiency" LLM`；限制域：arxiv.org
- `"Scaling Law" "Recommendation" "data"`；限制域：arxiv.org



## 10. 目标定义与正式书目核验

对应缺口：RATING_TARGETS, UNIFIED_TASK_ALLOCATION, EXPOSURE_BUDGET_COMPARISONS。

- `"Matrix Factorization Techniques for Recommender Systems" pdf Koren Bell Volinsky`
- `"Collaborative Filtering for Implicit Feedback Datasets" pdf Hu Koren Volinsky`
- `"OneRec: Unifying Retrieve" KDD 2025`
- `"Scaling Law of Large Sequential Recommendation Models" venue`



## 11. 基础原文定向获取

对应缺口：RATING_TARGETS。

- `"Matrix Factorization Techniques" "pdf" Koren`；限制域：research.google, yifanhu.net, volinsky.com, ieee.org, computer.org
- `"Collaborative Filtering for Implicit Feedback Datasets"`；限制域：yifanhu.net, research.google, volinsky.com



## 12. Koren原文补取

对应缺口：RATING_TARGETS。

- `"Koren" "Bell" "Volinsky" "2009" "pdf" "factorization"`



## 13. 原文与出版信息最后定向核验

对应缺口：RATING_TARGETS, UNIFIED_TASK_ALLOCATION, EXPOSURE_BUDGET_COMPARISONS。

- `"Matrix Factorization Techniques for Recommender Systems" filetype:pdf site:edu`
- `"OneRec: Unifying Retrieve and Rank" site:dl.acm.org`
- `"Scaling Law of Large Sequential Recommendation Models" site:dl.acm.org`



## 检索结果与停止

前5组核已有8篇。第6组索引噪声，未当证据；第7组取得ITDR/InstructRec/LLMRec benchmark。第8-9组核OneRec家族与直接预算邻居。第10-13组补目标定义及出版身份；若正式venue未核实，使用arXiv身份而非猜测。Koren最终取到原论文排版副本，Hu取作者PDF。

选入10个新候选：S15-S24。联合对照重点为8篇最近邻，工业OneRec报告和两篇预算论文补足边界。相关方法/实验章节已核；不再泛搜。无训练、推理、本地新实验或结果重算。
