# 分析模块

`src/analysis` 保存 MVP 与 Phase 1.5 的离线分析入口。这里的脚本默认读取已经生成的
`outputs/**/predictions.jsonl` 与 `metrics.json`，不重新训练模型。

## 当前文件

- `summarize_results.py`：读取 Base、Y-K0、N-K0、M-K0 的 metrics，生成 `outputs/results.csv`
  和 Markdown 主结果表。
- `basic_error_analysis.py`：读取 prediction JSONL，生成 binary confusion、ranking rank/margin/position
  sanity check 和代表性错误样本。
- `threshold_calibration.py`：用 validation 的 best-F1 threshold 校准 Yes/No 二分类阈值，再把同一阈值应用到 test。
- `threshold_comparison.py`：Phase 1.5 STEP B 入口，统一输出三张二分类口径表：
  threshold-free AUC、固定阈值 0.5、validation-calibrated threshold。

## Phase 1.5 STEP B 示例

```bash
python -m src.analysis.threshold_comparison \
  --config configs/experiment.yaml \
  --dataset movielens-1m \
  --y-run pool200k_1m_y_1500 \
  --m-runs pool200k_1m_m_1500 diag_m1_1m_m_200k_3000 diag_m2_1m_m_y2n1_1500 \
  --m-labels M0 M1 M2 \
  --output-dir outputs/calibration/movielens-1m/threshold_comparison
```

输出包括：

```text
binary_auc.csv
binary_fixed_0_5.csv
binary_calibrated.csv
threshold_comparison.json
threshold_comparison.md
```

本脚本只比较 Y-task 的 Yes/No 二分类口径，不包含 N-task ranking 指标。正式 MovieLens-1M
报告需要在包含完整云端 prediction 文件的环境中运行。
