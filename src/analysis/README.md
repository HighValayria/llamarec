# 分析模块

STEP 8 分析入口已经建立，当前只覆盖 MVP 必需的结果汇总和基础错误分析。

## 当前文件

- `summarize_results.py`：读取 Base、Y-K0、N-K0、M-K0 的 metrics，生成 `outputs/results.csv` 和 Markdown 主结果表。
- `basic_error_analysis.py`：读取 prediction JSONL，生成 binary confusion、ranking rank/margin/position sanity check 和代表性错误样本。
- `threshold_calibration.py`：用 validation 的 best-F1 threshold 校准 Yes/No 二分类阈值，再把同一阈值应用到 test。

## MVP 分析范围

- Y 的偏好判断行为与 N 的序列行为预测差异。
- Y 用 `P(Yes)` 对候选排序时的表现。
- N 用候选标签概率进行 next-item prediction 的表现。
- M 的 Yes/No 推理模式 vs Next-item 推理模式。
- 基础 candidate-position sanity check。
- M-Y 的 threshold / calibration 诊断，尤其用于区分 AUC 接近但默认 0.5 阈值下 F1 偏低的情况。

当前仍不纳入 KAR、SASRec、Hard Negative、Bootstrap、多 seed 或其他 Phase 2 分析。

## Threshold calibration 示例

```bash
python -m src.analysis.threshold_calibration \
  --config configs/experiment.yaml \
  --dataset movielens-1m \
  --y-run pool200k_1m_y_1500 \
  --m-runs pool200k_1m_m_1500 diag_m1_1m_m_200k_3000 diag_m2_1m_m_y2n1_1500 \
  --m-labels M0 M1 M2 \
  --output-dir outputs/calibration/movielens-1m/m_diagnostics
```

输出包括：

```text
threshold_calibration.csv
threshold_calibration.json
threshold_calibration.md
```
