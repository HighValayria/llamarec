# Bootstrap Provenance Retrieval Commands

> **COMPLETED / DO NOT RERUN（2026-09-09）**：原机器取证已完成。`BOOTSTRAP_PROVENANCE` 为RESOLVED；exact shell invocation未留存，但effective OUT、5000次、reuse行为、seed规则、summary/input及执行时期源码Git/blob身份已交叉恢复。以后不要重复执行本文命令，也不要重新bootstrap。当前记录见 `paper/evidence/bootstrap_provenance_closure.md`。

本文件只生成给原 seed42 分析机器执行的只读命令。不会重新分析、重新 bootstrap、重新推理或修改项目文件。项目根默认为 `/root/llamarec`；如实际根目录不同，只替换 `ROOT`。

## STEP 1：定位实际 OUT

只在 `.agent` 和 `outputs` 内、有限深度搜索关键文件，不扫描整个磁盘、权重或巨大缓存。

```bash
ROOT=/root/llamarec
for base in "$ROOT/.agent" "$ROOT/outputs"; do [ -d "$base" ] || continue; find "$base" -maxdepth 8 -type f \( -name 'binary_bootstrap_summary.csv' -o -name 'ranking_bootstrap_summary.csv' -o -name 'binary_predictions_y96_m96_valid.csv' \) -print; done | sort -u
```

把同时包含前三个文件的目录记为 `OUT`。不要默认使用 `.agent/exposure_scaling/analysis_handoff`，原命令可能通过 `--out` 覆盖目录。

## STEP 2：检查目标文件

```bash
OUT=/actual/path; test -d "$OUT" || { echo "OUT directory missing: $OUT"; exit 1; }
files=(binary_bootstrap_summary.csv ranking_bootstrap_summary.csv binary_predictions_y96_m96_valid.csv ranking_predictions_k5_valid.csv ranking_predictions_k5_test.csv ranking_predictions_k20_valid.csv ranking_predictions_k20_test.csv ranking_predictions_k50_valid.csv ranking_predictions_k50_test.csv README.md artifact_manifest.csv)
for rel in "${files[@]}"; do path="$OUT/$rel"; if [ -e "$path" ]; then printf 'exists\t%s\n' "$(readlink -f -- "$path")"; else printf 'missing\t%s\n' "$path"; fi; done
```

## STEP 3：打印 hash、大小、时间、header 和行数

CSV 只打印 header 和数据行数；summary 额外打印前 30 行，不打印整份 CSV。

```bash
OUT=/actual/path; export LC_ALL=C
files=(binary_bootstrap_summary.csv ranking_bootstrap_summary.csv binary_predictions_y96_m96_valid.csv ranking_predictions_k5_valid.csv ranking_predictions_k5_test.csv ranking_predictions_k20_valid.csv ranking_predictions_k20_test.csv ranking_predictions_k50_valid.csv ranking_predictions_k50_test.csv README.md artifact_manifest.csv)
for rel in "${files[@]}"; do path="$OUT/$rel"; echo "===== $rel ====="; if [ ! -f "$path" ]; then echo "status=missing"; echo "absolute_path=$path"; continue; fi; echo "status=exists"; echo "absolute_path=$(readlink -f -- "$path")"; stat -c 'bytes=%s modified=%y' -- "$path"; sha256sum -- "$path"; case "$rel" in *.csv) echo 'header:'; head -n 1 -- "$path"; echo "row_count=$(awk 'NR > 1 {n++} END {print n+0}' -- "$path")";; esac; case "$rel" in binary_bootstrap_summary.csv|ranking_bootstrap_summary.csv) echo 'first_30_lines:'; sed -n '1,30p' -- "$path";; esac; done
```

## STEP 4：定位实际执行命令、OUT 覆盖和脚本版本

```bash
ROOT=/root/llamarec
find "$ROOT/.agent" "$ROOT/outputs" -maxdepth 8 -type f \( -name 'seed42_deep_analysis.py' -o -name 'seed42_deep_analysis.sh' \) -print 2>/dev/null | sort -u
find "$ROOT/.agent" "$ROOT/outputs" -maxdepth 8 -type f \( -name 'seed42_deep_analysis.py' -o -name 'seed42_deep_analysis.sh' -o -name '*.sh' -o -name '*.log' -o -name '*.txt' -o -name 'README*' -o -name 'artifact_manifest*' \) -print0 2>/dev/null | while IFS= read -r -d '' path; do if grep -Iq -E 'seed42_deep_analysis|BOOTSTRAP_REPLICATES|--bootstrap|--out|--reuse-existing' -- "$path"; then echo "===== $path ====="; grep -n -I -i -C 2 -E 'seed42_deep_analysis|BOOTSTRAP_REPLICATES|--bootstrap|--out|--reuse-existing' -- "$path" | head -n 80; fi; done
cd "$ROOT"; git status --short; git log --oneline --all -- .agent/exposure_scaling/alignment/commands/seed42_deep_analysis.py; script="$ROOT/.agent/exposure_scaling/alignment/commands/seed42_deep_analysis.py"; [ -f "$script" ] && sha256sum -- "$script"
```

不要执行 `checkout`、`reset`、`pull`、`fetch` 或切换 commit。

## STEP 5：如果 paired CSV 缺失，定位既有原 prediction JSONL

只检查闭合计划第 4.3 节已经记录的优先/备用路径。先按实际执行记录修正三个 run 目录；下面默认值对应计划中的 seed42 目标 run。不要运行 inference 或分析脚本。

```bash
ROOT=/root/llamarec; Y_RUN="$ROOT/outputs/y/movielens-1m/exposure_y_s12000"; N_RUN="$ROOT/outputs/n/movielens-1m/exposure_n_s12000"; M_RUN="$ROOT/outputs/m/movielens-1m/exposure_m1_s24000"
candidates=("$Y_RUN/popmatch_eval_valid_only/y_valid_predictions.jsonl" "$Y_RUN/popmatch_eval_valid_only/y_test_predictions.jsonl" "$Y_RUN/popmatch_eval/y_valid_predictions.jsonl" "$Y_RUN/popmatch_eval/y_test_predictions.jsonl" "$M_RUN/popmatch_eval_valid_only/m_y_valid_predictions.jsonl" "$M_RUN/popmatch_eval_valid_only/m_y_test_predictions.jsonl" "$M_RUN/popmatch_eval/m_y_valid_predictions.jsonl" "$M_RUN/popmatch_eval/m_y_test_predictions.jsonl" "$N_RUN/popmatch_eval/n_valid_predictions.jsonl" "$N_RUN/popmatch_eval/n_test_predictions.jsonl" "$N_RUN/popmatch_eval_valid_only/n_valid_predictions.jsonl" "$N_RUN/popmatch_eval_valid_only/n_test_predictions.jsonl" "$M_RUN/popmatch_eval_valid_only/m_n_valid_predictions.jsonl" "$M_RUN/popmatch_eval_valid_only/m_n_test_predictions.jsonl" "$M_RUN/popmatch_eval/m_n_valid_predictions.jsonl" "$M_RUN/popmatch_eval/m_n_test_predictions.jsonl" "$ROOT/outputs/phase2a/current96_ranking_robustness/n_k0_k20_seed42/n_valid_predictions.jsonl" "$ROOT/outputs/phase2a/current96_ranking_robustness/n_k0_k20_seed42/n_test_predictions.jsonl" "$ROOT/outputs/phase2a/current96_ranking_robustness/n_k0_k50_seed42/n_valid_predictions.jsonl" "$ROOT/outputs/phase2a/current96_ranking_robustness/n_k0_k50_seed42/n_test_predictions.jsonl" "$ROOT/outputs/phase2a/current96_ranking_robustness/m1_k20_seed42/m_n_valid_predictions.jsonl" "$ROOT/outputs/phase2a/current96_ranking_robustness/m1_k20_seed42/m_n_test_predictions.jsonl" "$ROOT/outputs/phase2a/current96_ranking_robustness/m1_k50_seed42/m_n_valid_predictions.jsonl" "$ROOT/outputs/phase2a/current96_ranking_robustness/m1_k50_seed42/m_n_test_predictions.jsonl")
for path in "${candidates[@]}"; do if [ -f "$path" ]; then echo "exists\t$(readlink -f -- "$path")"; stat -c 'bytes=%s modified=%y' -- "$path"; sha256sum -- "$path"; else echo "missing\t$path"; fi; done
```

不要运行分析脚本，不要加 `--reuse-existing`，也不要用新的路径替代缺失路径。

## STEP 6：最小打包

仅在 STEP 2 中 2 个 summary 和 7 个 paired CSV 全部存在后执行。README/manifest 可以缺失；checkpoint、adapter、权重和整个输出目录禁止打包。

```bash
ROOT=/root/llamarec; OUT=/actual/path; ARCHIVE="$ROOT/bootstrap_provenance_minimal.tar.gz"
required=(binary_bootstrap_summary.csv ranking_bootstrap_summary.csv binary_predictions_y96_m96_valid.csv ranking_predictions_k5_valid.csv ranking_predictions_k5_test.csv ranking_predictions_k20_valid.csv ranking_predictions_k20_test.csv ranking_predictions_k50_valid.csv ranking_predictions_k50_test.csv)
for rel in "${required[@]}"; do [ -f "$OUT/$rel" ] || { echo "required file missing: $OUT/$rel"; exit 1; }; done
optional=(README.md artifact_manifest.csv); files=("${required[@]}"); for rel in "${optional[@]}"; do [ -f "$OUT/$rel" ] && files+=("$rel"); done
# STEP 4 中确认过的少量执行记录可加入 records；没有就留空。
records=(); tar -czf "$ARCHIVE" -C "$OUT" "${files[@]}" "${records[@]}"; sha256sum -- "$ARCHIVE"; stat -c 'archive_bytes=%s modified=%y path=%n' -- "$ARCHIVE"
```

## 回传内容与停止条件

请回传 STEP 1 的路径、STEP 2/3 的完整输出、STEP 4 的脚本版本和相关上下文；若有缺失 paired CSV，再回传 STEP 5 的完整输出；若成功打包，再带回 `bootstrap_provenance_minimal.tar.gz` 及 SHA-256。

如果两个 summary 或七个 paired CSV 任意一个缺失：停止，不要重新 bootstrap、不要运行 inference、不要运行 `seed42_deep_analysis.py`，只回传缺失清单和 STEP 5 结果。若 STEP 5 对应原 JSONL 也缺失，同样停止。
