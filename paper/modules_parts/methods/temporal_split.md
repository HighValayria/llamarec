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

Each user's sequence is grouped into ordered timestamp buckets. A target at t uses only events strictly before t, so same-bucket Y targets share the preceding history. The last bucket supplies Y test targets, the previous bucket supplies validation, and earlier buckets supply training; a held-out bucket may yield several Y targets. Prompts retain the 10 most recent eligible events.

**ZH**

每位用户的序列按时间戳分为有序时间桶。时刻t的目标只使用严格早于t的事件，因此同桶Y目标共享此前历史。末桶提供Y测试目标，前一桶提供验证目标，更早时间桶提供训练样本；一个留出桶可产生多个Y目标。提示保留最近10条合法事件。

<!-- PARAGRAPH: methods.temporal.p02 -->
<!-- EVIDENCE: M1 -->

**EN**

N requires preceding history and one unique next item, so legal targets are single-interaction buckets after the initial bucket. Multi-interaction buckets are skipped as targets but remain in later histories. The last two legal N examples become validation and test; earlier legal examples form training. Inputs again retain at most 10 strictly earlier interactions.

**ZH**

N同时要求先前历史和唯一下一物品，因此合法目标来自首桶之后的单交互时间桶。多交互桶不作为目标，但其事件仍进入后续历史。末两个合法N样本依次作为验证和测试，更早合法样本用于训练；输入同样最多保留10条严格更早交互。
