# Bootstrap Provenance Closure

日期：2026-09-09  
状态：**RESOLVED**  
适用对象：论文中 seed42 固定已训练模型的用户级配对 percentile-bootstrap 置信区间。

## Closure decision

`BOOTSTRAP_PROVENANCE` 已闭环。原始 summary、论文当前 CI 所需的 paired-prediction 输入、输出元数据、有效参数和执行时期源码身份均已恢复并交叉核对。**Exact shell invocation 未留存**；这一限制在此显式记录，不用推测命令补造。由于实际生效参数可由生成产物、wrapper 默认值、artifact 状态、Git blob 身份和时间链共同恢复，缺少原始 shell 文本不再视为统计来源 blocker。

本次闭环不表示重新执行或独立重现 bootstrap。没有运行 bootstrap、没有重算 CI、没有运行 inference，也没有生成或修改 prediction。

## Original-machine evidence

| Item | Recovered fact | Evidence |
| --- | --- | --- |
| Project root | `/root/llamarec` | 原机器 `pwd` |
| Retrieval-time HEAD | `a9c6cd959cf32afe046bb05be9eb5096bebfc5fb` | `git rev-parse HEAD` |
| Historical invocation | **NOT RETAINED** | `.bash_history` 没有原始启动命令；命中内容为后续读取、打包和审计命令；`.zsh_history` 不存在 |
| Effective OUT | `/root/llamarec/.agent/exposure_scaling/analysis_handoff` | 原目录实际存在；README、manifest 和 summaries 位于该目录；wrapper 默认 `OUT=.agent/exposure_scaling/analysis_handoff` |
| Effective replicates | `5000` | README 写明 `Bootstrap replicates requested: 5000`；binary/ranking summary 每条记录均为 `replicates=5000`；wrapper 与 Python 默认均为 5000 |
| Reuse behavior | existing paired-prediction CSVs were reused | manifest 对 binary 和六份 ranking prediction 均记录 `OK: reused existing artifact`；wrapper 默认 `REUSE_EXISTING=1` 并据此传入 `--reuse-existing`。精确环境变量赋值文本未留存，但生效行为已由产物记录确认 |
| Bootstrap unit | user | 两份 summary 的 `bootstrap_unit` 为 `user`；脚本按 `user_id` 分组重采样 |
| Base bootstrap seed | `20260902` | 执行时期 Python 源码中的 `BOOTSTRAP_SEED`；binary test 与 ranking protocol/split 使用源码定义的固定偏移 |
| Generation time | `2026-09-02T15:17:38.969826+00:00`，即北京时间约 `2026-09-02 23:17:38` | README；README/manifest 文件 mtime 与该时间一致 |
| Output status | bootstrap summaries OK；所需 prediction inputs reused and OK | `artifact_manifest.csv`；其中 SASRec metrics 的 MISSING 与本 bootstrap CI 链无关 |

## Execution-era source identity

### Python generator

- Path: `/root/llamarec/.agent/exposure_scaling/alignment/commands/seed42_deep_analysis.py`
- Most specific execution-era commit: `eca24e795818734ea86dc9ba13d43bfd997256c3`
- Commit time: `2026-09-02T22:39:47+08:00`
- Commit subject: `Fix seed42 analysis metrics and coverage parsing`
- Git blob/current clean-file SHA256: `e60e2a7cb29e115482a5572e5b4b177b428325ed644684ea5f27e9164d0361cb`
- Original-machine mtime: `2026-09-02 22:40:20.050057940 +0800`

### Wrapper

- Path: `/root/llamarec/.agent/exposure_scaling/alignment/commands/seed42_deep_analysis.sh`
- Most specific execution-era commit: `3b5de95812cb01427259cc210da4713a8cc8d277`
- Commit time: `2026-09-02T22:05:51+08:00`
- Commit subject: `Allow seed42 analysis resume from CSV artifacts`
- Git blob/current clean-file SHA256: `8a1062b7ea3a251be1d1b42e1c508ae8119b23e3d6ea57e5d7d147de4ea8809e`
- Original-machine mtime: `2026-09-02 22:07:00.765311411 +0800`

The output was generated at approximately 23:17 +08:00, after both identified source versions were committed and written. Retrieval-time `git status --short` showed no tracked modification to either script. The output does not embed a source hash, so this is a cross-recovered execution-era identity rather than a claim that the missing shell command was found.

## Retained bootstrap artifacts

原机器的正式目录已打包并复制到本机；本机当前镜像位于 `.agent/.agent/exposure_scaling/analysis_handoff/`。双层 `.agent` 是解压落点，不是原机器的 effective OUT。

| Artifact | Rows / role | Retrieval-copy SHA256 |
| --- | --- | --- |
| `binary_bootstrap_summary.csv` | 6 summary rows | `77451f65c825316d615ea480e810de20bc74585c8da20b48feee96a33ad2ebe0` |
| `ranking_bootstrap_summary.csv` | 18 summary rows | `34635d54b43c6f6c1d08b0fd5d6d5efbb128e1c680bfd6d24c8e548df1a69bd8` |
| `binary_predictions_y96_m96_valid.csv` | 12,381 paired rows | `3d2adc5ef3cf516aaf8b109fb501f74c7b90bfd73565c515fda6340496ae7104` |
| `ranking_predictions_k5_valid.csv` | 5,675 paired rows | `7b9d2a49469eb5aac523ff1eb768fd342dbeb035072d1cd505b84632069f651b` |
| `ranking_predictions_k5_test.csv` | 5,675 paired rows | `62293fbd8d29870e1f09a08d9c7c131943b5f5358bf9c7e1e253cc0ec73cac00` |
| `ranking_predictions_k20_valid.csv` | 5,675 paired rows | `bc054bfff0a0ca761a80f84164b32462e189f0af34ea88b9b25ff883cad8d790` |
| `ranking_predictions_k20_test.csv` | 5,675 paired rows | `a962d6b08d883010089d69ec31e75fb67a9446198dfc45999bd180a22f3cf840` |
| `ranking_predictions_k50_valid.csv` | 5,675 paired rows | `69ed7c4ed768ff9b56c4a69308d9d279c8f2f8badbbf02c22f8c3f064a173e10` |
| `ranking_predictions_k50_test.csv` | 5,675 paired rows | `60404b92414e4078d8d1c6e3948decfcebc5561a023ef04b7e752b4874343d74` |
| `README.md` | generation metadata | `da2d7a4e0a7808798807037ffad0c26163a50dc6cffe98c4f4e33db385e7aca2` |
| `artifact_manifest.csv` | artifact status and row counts | `b454b7b971873fc4ee56904eef465bf86c1a36b34f7858834ae78fd10a89b915` |

`binary_predictions_y96_m96_test.csv` is retained in the handoff but is not part of the seven-input minimum used by the current manuscript CI sentences. It was not rehashed in this closure because its existing transfer identity was already recorded separately and the closure task prohibited unnecessary repeat work.

## Effective execution specification

The exact historical shell text is unknown. The recoverable effective specification is:

```text
root=/root/llamarec
output_dir=.agent/exposure_scaling/analysis_handoff
bootstrap_replicates=5000
reuse_existing=true
bootstrap_seed_base=20260902
python_source_sha256=e60e2a7cb29e115482a5572e5b4b177b428325ed644684ea5f27e9164d0361cb
wrapper_source_sha256=8a1062b7ea3a251be1d1b42e1c508ae8119b23e3d6ea57e5d7d147de4ea8809e
```

This specification records recovered behavior; it is not presented as a verbatim historical command.

## Closure boundary

- Status: **RESOLVED**
- Further search of shell history, logs, output metadata or Git history: **NOT REQUIRED**
- Re-running bootstrap or CI computation: **NOT REQUIRED AND NOT PERFORMED**
- Re-running inference or regenerating predictions: **NOT REQUIRED AND NOT PERFORMED**
- Scientific wording in Results, Discussion, Limitations, Conclusion and Abstract: **UNCHANGED**
- Remaining limitation: exact shell invocation text was not retained.

