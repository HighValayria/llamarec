---
id: datasets
title:
  en: Datasets and Evidence Coverage
  zh: 数据集与证据覆盖
status: draft
---

<!-- PARAGRAPH: methods.datasets.p01 -->
<!-- EVIDENCE: M8 -->

**EN**

MovieLens-1M [@harper2015movielens] supplies 976,284 training, 12,381 validation, and 11,544 test examples for Y. Its legal N split contains 212,725 training examples and 5,675 examples in each evaluation split, with 5,675 eligible N users compared with 6,040 Y users. The ratings cover 3,706 distinct items, while the movie metadata universe contains 3,883 items. Task-specific target and timestamp-bucket rules account for the different Y and N sample populations. [TABLE: datasets] records their task-level sizes.

**ZH**

MovieLens-1M [@harper2015movielens] 的 Y 任务包含 976,284 个训练样本、12,381 个验证样本和 11,544 个测试样本。合法 N 划分包含 212,725 个训练样本，两个评估划分各含 5,675 个样本；符合条件的 N 用户为 5,675 人，Y 用户为 6,040 人。评分记录覆盖 3,706 个不同物品，电影元数据全集则包含 3,883 个物品。Y 与 N 的样本群体差异来自各自的目标和时间桶规则。[TABLE: datasets] 列出任务级规模。

<!-- PARAGRAPH: methods.datasets.p02 -->
<!-- EVIDENCE: M8,C8 -->

**EN**

The processed Amazon Reviews 2023 5-core Musical Instruments collection [@hou2026amazonreviews] contains 57,439 users, 24,584 items, and 511,792 interactions. It provides 396,908 Y training examples and 57,442 examples in each Y evaluation split, together with 339,449 N training examples and 57,439 examples in each N evaluation split. The external analysis uses seed42 full-test ranking evaluations under Random-k5 and PopMatch-k5 at the available earlier operating points. These evaluations compare Y-as-ranker, N, M-N, and sequential baselines in a second recommendation domain.

**ZH**

处理后的 Amazon Reviews 2023 5-core Musical Instruments 数据 [@hou2026amazonreviews] 包含 57,439 名用户、24,584 个物品和 511,792 次交互。Y 训练样本为 396,908 个，两个 Y 评估划分各有 57,442 个样本；N 训练样本为 339,449 个，两个 N 评估划分各有 57,439 个样本。外部分析使用现有较早运行点在 Random-k5 和 PopMatch-k5 下的 seed42 完整测试集排序结果。这些评估在第二个推荐领域中比较 Y-as-ranker、N、M-N 与序列基线。
