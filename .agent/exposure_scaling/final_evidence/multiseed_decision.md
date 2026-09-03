# Multiseed Decision

## Version A: no additional multiseed

论文措辞保持限定：seed42 exposure analysis suggests。可使用的证据组合包括低 exposure 3-seed evidence、seed42 exposure trajectory、prediction-level bootstrap，以及 Amazon directional validation。这个版本可以支持 descriptive paper claims，但不能把 M1 positive transfer 或 N/M parity 写成跨 seed 定论。

## Version B: minimal strengthening

若后续批准，最小补强矩阵为 seed43 与 seed44 的 Y96、N96、M96。每个 seed 需要 Y-native binary、N k5/k20/k50 validation-first 评测，并在决策冻结后补 report-only test。按 seed42 经验粗估，单 seed 的 Y96+N96+M96 训练和评测可能需要数十小时单卡时间；实际取决于云端卡型、是否续训、I/O 和候选评测批大小。信息增益主要体现在三类 claim：Y-side no degradation 是否稳定，k5 N/M near-parity 是否稳定，hard-candidate robustness gap 是否稳定。

## Current recommendation

Multiseed is recommended, not required, for the current Results draft. 如果论文只写 seed42 descriptive findings，可以不补。若目标是提交时使用 stronger generalization wording，则应补最小 multiseed。
