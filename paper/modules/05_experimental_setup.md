---
id: experimental_setup
title:
  en: Experimental Setup
  zh: 实验设置
status: draft
---

<!-- PARAGRAPH: setup.p01 -->
<!-- EVIDENCE: C1,C3,C5,C6,C7,C8 -->

**EN**

MovieLens-1M supports the exposure and specialist-multitask analyses; Amazon Musical Instruments supplies an external ranking check. Native preference and ranking metrics are reported separately with split and exposure identified. Validation guides exposure and checkpoint decisions, while frozen-test results are reported only after those decisions.

**ZH**

MovieLens-1M用于曝光及专家-多任务分析，Amazon Musical Instruments提供外部排序检验。原生偏好与排序指标分开报告，并标明划分和曝光。验证集指导曝光与检查点决策，冻结测试结果仅在这些决策完成后报告。

<!-- INCLUDE: paper/modules_parts/methods/datasets.md -->
<!-- INCLUDE: paper/modules_parts/methods/exposure_definition.md -->
<!-- INCLUDE: paper/modules_parts/methods/evaluation_protocol.md -->
<!-- INCLUDE: paper/modules_parts/methods/baseline_setup.md -->
<!-- INCLUDE: paper/modules_parts/methods/bootstrap_and_statistics.md -->
