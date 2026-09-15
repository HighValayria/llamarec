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

MovieLens-1M [@harper2015movielens] uses task-specific temporal splits summarized in [TABLE: datasets]. Different target and timestamp-bucket rules yield 6,040 Y users and 5,675 legal N users. Ratings cover 3,706 distinct items, while the metadata universe contains 3,883, a distinction retained for coverage interpretation.

**ZH**

MovieLens-1M [@harper2015movielens]采用[TABLE: datasets]汇总的任务特定时间划分。不同目标与时间桶规则产生6,040名Y用户和5,675名合法N用户。评分覆盖3,706个不同物品，元数据全集包含3,883个物品，这一区别用于解释覆盖范围。

<!-- PARAGRAPH: methods.datasets.p02 -->
<!-- EVIDENCE: M8,C8 -->

**EN**

The processed Amazon Reviews 2023 5-core Musical Instruments data [@hou2026amazonreviews] contain 57,439 users, 24,584 items, and 511,792 interactions; task splits appear in the same table. External evidence uses seed42 full-test Random-k5 and PopMatch-k5 ranking at available earlier operating points, covering Y-as-ranker, N, and sequential references.

**ZH**

处理后的Amazon Reviews 2023 5-core Musical Instruments数据 [@hou2026amazonreviews]包含57,439名用户、24,584个物品和511,792次交互，任务划分见同一表。外部证据采用现有较早运行点的seed42完整测试集Random-k5与PopMatch-k5排序，覆盖Y-as-ranker、N及序列参照。
