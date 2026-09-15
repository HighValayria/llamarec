# 既有图资产

本轮不新增科学图，不重新绘制数据；复制冻结图及关联 CSV，图在英文工作稿中引用，中文说明由 manifest 提供。图内英文标签保留原样。

| 稳定 ID | 图文件 | 数据 | 类型 | 原始来源 |
| --- | --- | --- | --- | --- |
| n_native_exposure | fig_n_native_exposure.png / .svg | data/fig_n_native_exposure.csv | 真实冻结 seed42 指标 | .agent/exposure_scaling/final_evidence/figures/ 同名文件 |
| n_vs_sasrec_exposure | fig_n_vs_sasrec_exposure.png / .svg | data/fig_n_vs_sasrec_exposure.csv | 真实冻结 seed42 对齐指标 | 同上 |

原生成代码：`.agent/exposure_scaling/final_evidence/build_final_evidence.py`。本轮不执行该脚本；由 `assembly/prepare_assets.py` 做字节不变复制。绘图并不补充训练随机性区间，不能从连线推断未测曝光点。任何未来重画仍从冻结数据派生，并保留图注边界。
