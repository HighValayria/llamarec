# 已冻结实验的写作协议

数据：MovieLens-1M 为主要研究数据，Amazon Musical Instruments 为旧 seed42 排序外部检验。Y 与 N 按各自严格用户内时间规则划分，不能把样本规模写成完全一致。

对照：固定底座的 Y/N/M1 任务接口；N/M 按每任务曝光比，N/SASRec 按实际 N 样本曝光约对齐。前者 M 的总曝光双倍，后者不匹配 FLOPs 或预训练。Popularity/BPR 和旧三 seed 仅作为既有背景，本轮不增加诊断实验。

指标：Y binary AUC/F1/Accuracy；当前96k配对 F1/Accuracy 固定0.5阈值。排序 HR@1/NDCG@5/MRR；hard-k20/k50 中 NDCG 仍截断到5，MRR保留全候选排名。

选择纪律：validation 用于曝光点选择、检查点评估和继续训练决策；冻结后报告 test，二者共同参与科学解释，不能因 test 未用于选择而降低其证据作用。统计上，用户级 paired bootstrap 和训练 multi-seed 分开。MS96已整合：seed42全轨迹，seed43/44只复现96k的Y96/N96/M1-96两split与三协议。bootstrap仍仅seed42；三seed差值等权mean和sample std，n=3/ddof=1，非CI/显著性。只解析已完成轻量汇总，不轮询、不等待。

边界：非新架构所以不安排模型组件消融；无 compute/serving/XAI 贡献，所以不捏造相关评测。外部验证未覆盖 Amazon 曝光曲线或 hard protocol。引用未来增补须获得新的文献任务授权。
