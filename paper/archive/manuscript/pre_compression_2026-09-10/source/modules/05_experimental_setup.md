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

The evaluation examines supervision formulation, task exposure, and candidate protocol as experimental dimensions. MovieLens-1M provides the exposure trajectories and specialist-multitask comparisons, and Amazon Musical Instruments supplies an external ranking check. Native preference metrics and candidate-ranking metrics are reported separately, with the data split and exposure identified for each comparison. Validation guides exposure selection, checkpoint assessment, and decisions about further training; test results are reported after these decisions are frozen and inform the final interpretation.

**ZH**

评估围绕监督形式、任务曝光和候选协议展开。MovieLens-1M 提供曝光轨迹及专家与多任务比较，Amazon Musical Instruments 提供外部排序检验。原生偏好指标与候选排序指标分别报告，每项比较均标明数据划分与曝光。验证集用于曝光点选择、检查点评估及是否继续训练的决策；这些决策冻结后报告测试结果，并将其纳入最终解释。

<!-- INCLUDE: paper/modules_parts/methods/datasets.md -->
<!-- INCLUDE: paper/modules_parts/methods/exposure_definition.md -->
<!-- INCLUDE: paper/modules_parts/methods/evaluation_protocol.md -->
<!-- INCLUDE: paper/modules_parts/methods/baseline_setup.md -->
<!-- INCLUDE: paper/modules_parts/methods/bootstrap_and_statistics.md -->
