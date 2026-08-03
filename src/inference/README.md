# STEP 4：Base Zero-shot 本地推理层

本目录负责 Base LLM 的 zero-shot 推理入口。本地仍优先使用 mock dry-run；
云服务器可用 `--mode real` 加载 `meta-llama/Llama-3.2-3B-Instruct` 做真实概率推理。

## 当前文件

- `prompts.py`：把 Y/N 样本渲染为稳定 prompt，并检查 target rating 或候选 rating 不进入不该出现的位置。
- `scoring.py`：提供 `MockScorer` 和云端真实 scorer，real 模式支持批量单 token logits 推理。
- `tokenization_check.py`：记录 Yes / No / A / B / C / D / E 的 tokenization 检查契约。
- `prediction_io.py`：统一读写 prediction jsonl、metrics json 和配置快照，支持分批追加 prediction。
- `base_zero_shot.py`：STEP 4 CLI，串起读数据、打分、写预测和算指标，支持 `--batch-size`。

## 本地 dry-run 命令

```bash
python -m src.inference.base_zero_shot --config configs/experiment.yaml --dataset movielens-100k --mode mock --limit 20
python -m src.inference.base_zero_shot --config configs/experiment.yaml --dataset movielens-32m --mode mock --limit 20
```

在本机建议使用：

```text
C:\Users\33967\AppData\Local\Programs\Python\Python312\python.exe
```

dry-run 的目标不是得到真实 Base 结果，而是提前验证：

- 能读取对应数据集的 Y validation/test 样本。32M 本地评测包使用 `.jsonl.gz`。
- 能读取 `data/candidates/{dataset}/valid.jsonl` 和 `data/candidates/{dataset}/test.jsonl`。
- Y prediction 能输出 `P(Yes)` / `P(No)`。
- N prediction 能输出 `P(A)` 到 `P(E)`。
- Binary 与 Ranking 指标可以从 prediction 文件计算。
- 所有产物统一写入 `outputs/base/{dataset}/`。

## 输出产物

```text
outputs/base/{dataset}/
  config_snapshot.yaml
  tokenization_report.json
  y_valid_predictions.jsonl
  y_test_predictions.jsonl
  n_valid_predictions.jsonl
  n_test_predictions.jsonl
  valid_metrics.json
  test_metrics.json
  run_summary.json
```

mock 模式下的指标只用于检查文件流和指标流，不代表真实 Base LLM 性能。

## 云端真实运行

真实 Base zero-shot 需要在云服务器上执行：

```text
1. 加载 tokenizer 和 base model。
2. 检查 Yes / No / A / B / C / D / E 是否为单 token。
3. 若答案不是单 token，使用完整答案 sequence likelihood。
4. 对 Yes/No 或 A-E 的答案分数做 softmax。
5. 返回连续概率，而不是只返回 generate 的文本。
```

建议先小样本验证：

```bash
python -m src.inference.base_zero_shot --config configs/experiment.yaml --dataset movielens-32m --mode real --splits validation --limit 20
python -m src.inference.base_zero_shot --config configs/experiment.yaml --dataset movielens-32m --mode real --splits validation --limit 5000 --batch-size 16
```

确认输出正常后再运行全量：

```bash
python -m src.inference.base_zero_shot --config configs/experiment.yaml --dataset movielens-32m --mode real --splits validation test --batch-size 16
```

真实 Base 阶段仍然不训练，也不保存 adapter。`--batch_size` 下划线写法也被兼容，但文档中统一使用 `--batch-size`。
