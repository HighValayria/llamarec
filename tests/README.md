# 测试说明

每个 STEP 的实现应同时补充可执行测试。当前已提供 STEP 2 的最小单元测试，覆盖新版 timestamp bucket 划分和无泄漏规则。

STEP 2 数据测试：

- 用户序列按时间顺序排列。
- Y history 只包含 `timestamp < target_timestamp` 的交互。
- 同一 timestamp bucket 内的多个 Y target 不会互相进入 history。
- timestamp tie 不会导致整个用户从 Y split 删除。
- N 只保留 singleton target bucket 对应的合法 next-item sample。
- N 遇到歧义 target bucket 时只跳过该 sample，不跳过整个用户。
- N validation/test 来自每个用户最后两个合法 next-item samples。
- seed 42 能复现 split 与候选采样结果。

STEP 3 候选集与指标测试：

- ground truth 在 candidates 中恰好出现一次。
- candidate 数量等于 5。
- negative candidate 不得等于 ground truth。
- 大量样本中 ground truth 位置不能固定。
- 固定候选文件被每个模型复用。
- 人工构造指标案例必须先于模型实验通过。

STEP 4+ 模型接口测试：

- 检查 `Yes`、`No`、`A`、`B`、`C`、`D`、`E` 的 tokenization。
- scoring 返回连续概率。
- adapter 保存/重载后推理行为保持一致。
