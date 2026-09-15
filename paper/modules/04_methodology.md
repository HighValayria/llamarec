---
id: methodology
title:
  en: Methodology
  zh: 研究方法
status: draft
---

<!-- PARAGRAPH: methodology.p01 -->
<!-- EVIDENCE: M1,M2,M3,M4 -->

**EN**

The pipeline constructs temporally legal examples, adapts a common base model with task-specific prompts, and scores allowed responses. Complete user sequences define examples, bounded recent histories form prompts, and the Y and N interfaces produce preference scores or candidate orderings.

**ZH**

实验流程构造时间合法样本，以任务特定提示适配共同底座，并为允许响应评分。完整用户序列用于定义样本，受限近期历史构成提示，Y与N接口分别输出偏好分数或候选排序。

<!-- INCLUDE: paper/modules_parts/methods/temporal_split.md -->
<!-- INCLUDE: paper/modules_parts/methods/training_setup.md -->
