# Discussion Outline

## Why supervision semantics matter

Y supervision directly优化偏好判断，N supervision 则要求模型在用户历史之后区分下一交互候选。二者都与推荐相关，但评价对象并不等价。Discussion 可以围绕这种语义差异解释为什么 Y-native 表现不能自动转化为 next-item ranking 能力。

## Why N benefits more from exposure

N 任务在 200k near-full-pool anchor 仍然提升，可能与下一交互预测对 item coverage、历史上下文组合和候选辨别边界更敏感有关。这个解释只能作为 hypothesis，不能写成机制证明。

## Why multitask interference decreases on Y/k5 but remains under hard ranking

M1-96 在 Y-side 没有可检测退化，在 k5 validation 上接近 N96，但 k20/k50 仍落后。Discussion 可以把这写成多任务共享表示对简单协议足够，但在更强候选干扰下仍缺少 N specialist 的排序锐度。

## Why random or easy candidates can hide model differences

k5 validation 的 near-parity 与 k20/k50 差距并存，说明候选协议会改变模型差异的可见性。由于当前 k20/k50 候选集不嵌套，文本必须把 candidate size 与 composition confound 一起写入限制。

## Why training-sample exposure matters in LLM-vs-SASRec comparison

SASRec 的高 epoch 或高步数结果不能直接和低 exposure LLM 比较。Exposure-aware comparison 让 baseline 更公平，但仍不等于 FLOP matching 或成本 matching。
