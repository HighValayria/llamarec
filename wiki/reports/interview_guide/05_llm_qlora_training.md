---
title: "05 llm qlora training"
type: report
status: current
authority: descriptive
source: agent
created: 2026-08-24
updated: 2026-08-24
last_verified: 2026-08-24
related_code:
  - configs/experiment.yaml
  - configs/y.yaml
  - configs/n.yaml
  - configs/m.yaml
  - src/train/train_y.py
  - src/train/train_n.py
  - src/train/train_m.py
  - src/train/preference_dataset.py
  - src/train/next_item_dataset.py
  - src/train/multitask_dataset.py
---

# 05 LLM QLoRA Training

## 当前模型配置

[FACT] Base model:

```text
meta-llama/Llama-3.2-3B-Instruct
```

[FACT] Training method:

```text
4-bit QLoRA + PEFT adapter
```

[FACT] max sequence length:

```text
2048
```

## 为什么选 3B

简短回答：

> 3B 在单卡 24GB 预算下能系统跑 Y/N/M、baseline diagnostics 和 multi-seed，而不是只做一次昂贵大模型演示。

边界：

[INTERPRETATION] 这不是说 3B 是最优模型规模；它是当前实验预算和系统比较目标下的可行选择。

## QLoRA 是什么

面试版：

> QLoRA 是把 base LLM 以低比特量化加载，冻结大部分 base 权重，只训练很小的 LoRA adapter。这样显存占用低，可以在 24GB 单卡上微调 3B 模型。

代码证据：`src/train/train_y.py::_load_tokenizer_and_model()`

[FACT] 使用：

```text
BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4")
prepare_model_for_kbit_training(model)
LoraConfig(...)
get_peft_model(model, lora_config)
```

## 4-bit quantization 量化的是谁

[FACT] 量化加载的是 base model 权重。LoRA adapter 是训练出来的增量参数。

不要说：

```text
训练的是被完全量化后的所有参数
```

要说：

```text
base model 4-bit 加载，LoRA adapter 作为可训练参数插入
```

## LoRA 参数怎么解释

当前配置：

```text
r = 16
alpha = 32
dropout = 0.05
bias = none
task_type = CAUSAL_LM
```

解释：

- `r=16`: 低秩矩阵的 rank，决定 adapter 容量。
- `alpha=32`: LoRA scaling，控制 adapter 更新幅度。
- `dropout=0.05`: adapter 训练正则，降低过拟合风险。

## target modules

[FACT] 当前 target modules:

```text
q_proj
k_proj
v_proj
o_proj
gate_proj
up_proj
down_proj
```

面试说法：

> 它覆盖 attention projection 和 MLP projection，所以不是只改最后一层，而是在 transformer block 的主要 linear modules 上插 LoRA。

## BF16 / FP16

[FACT] 代码根据 CUDA 支持选择 dtype；如果 GPU 支持 BF16，就用 BF16，否则用 FP16。CLI 也支持 `--bf16` / `--fp16` 传给 TrainingArguments。

面试说法：

> BF16 是混合精度训练/推理里常用的数值格式，动态范围比 FP16 更稳。当前代码在可用时优先 BF16。

## gradient checkpointing

[FACT] 配置 `gradient_checkpointing: true`，训练入口会 `model.gradient_checkpointing_enable()`。

解释：

> 它用更多计算换更低显存，不保存所有中间激活，反向时重新计算一部分。

## batch / accumulation / steps

CLI defaults:

```text
per_device_train_batch_size = 1
gradient_accumulation_steps = 8
learning_rate = 2e-4
```

[FACT] 正式结果解释中的 N-K0 anchor:

```text
optimizer steps = 1500
effective batch = 8
N-task exposure = 12000
```

[FACT] M1:

```text
optimizer steps = 3000
effective batch = 8
N-task exposure = 12000
total exposure = 24000
```

## Y/N/M 训练入口

Y:

```text
python -m src.train.train_y --config configs/y.yaml
```

N:

```text
python -m src.train.train_n --config configs/n.yaml
```

M:

```text
python -m src.train.train_m --config configs/m.yaml
```

## 训练样本如何监督答案

Y:

```text
prompt + answer Yes/No
loss only on answer tokens
```

N:

```text
prompt + answer A/B/C/D/E
loss only on candidate label token
```

M:

```text
Y example, N example, Y example, N example...
同一个 adapter 学两种答案格式
```

[FACT] `labels` 中 prompt token 是 `-100`，只有答案 token 是监督目标。

## seed 在哪里设置

[FACT] `_set_training_seed()` 设置：

```text
Python random
NumPy
Torch
CUDA
Transformers set_seed
```

[FACT] 它在模型初始化前调用。

面试说法：

> seed 必须在 model init 前设，否则初始化和 dropout/data order 等随机性仍可能不同。

## 保存和加载

训练保存：

```text
output_dir/adapter
```

内容：

```text
PEFT adapter weights
tokenizer files
```

推理加载：

```text
4-bit base model
+ PeftModel.from_pretrained(base_model, adapter_dir)
```

## 面试红线

不要说：

```text
我全参数微调了 Llama
M1 的 3000 steps 等于 N 上训练两倍
QLoRA 证明了 compute efficiency
```

要说：

```text
训练的是 LoRA adapter
M1 的 steps 在 Y/N 间分配
当前只支持 sample-exposure 维度，不能声称 strict compute/FLOPs matched
```
