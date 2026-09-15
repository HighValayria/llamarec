---
id: temporal_split
title:
  en: Temporal Sample Construction
  zh: 时间约束下的样本构造
status: draft
---

<!-- PARAGRAPH: methods.temporal.p01 -->
<!-- EVIDENCE: M1 -->

**EN**

Sample construction groups each user's full interaction sequence into ordered timestamp buckets. A target at t uses only events with timestamps strictly below t, so Y targets within the same bucket share a common preceding history. The final timestamp bucket supplies Y test targets, the preceding bucket supplies validation targets, and earlier buckets define the training region. A held-out bucket containing several interactions yields multiple Y targets for that user. Prompt construction subsequently retains at most the 10 most recent events from the strictly earlier history.

**ZH**

样本构造将每位用户的完整交互序列组织为有序时间桶。时刻 t 的目标只使用时间戳严格小于 t 的事件，因此同一时间桶内的 Y 目标共享此前历史。用户的末尾时间桶提供 Y 测试目标，前一个时间桶提供验证目标，更早的时间桶组成训练区域。留出时间桶包含多次交互时，该用户会产生多个 Y 目标。构造提示时，再从严格更早的历史中最多保留最近 10 条事件。

<!-- PARAGRAPH: methods.temporal.p02 -->
<!-- EVIDENCE: M1 -->

**EN**

N targets require both preceding history and a unique next item, so eligible targets come from single-interaction buckets after the initial bucket. A bucket with several interactions is skipped as an N target while its events remain available in the history of later legal examples. The last two legal N examples are assigned to validation and test, respectively, and the preceding legal examples to training. As in Y, model inputs retain at most the 10 most recent strictly earlier interactions.

**ZH**

N 目标要求同时具有先前历史和唯一的下一物品，因此合法目标来自首个时间桶之后仅含一次交互的时间桶。包含多次交互的时间桶不作为 N 目标，但其中事件仍可进入后续合法样本的历史。末尾两个合法 N 样本依次分配给验证集和测试集，其前面的合法样本进入训练集。与 Y 相同，模型输入最多保留严格更早的最近 10 条交互。
