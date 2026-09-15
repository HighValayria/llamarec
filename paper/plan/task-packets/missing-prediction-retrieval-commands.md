# Missing Prediction Retrieval Commands

状态：`READ_ONLY_COMMAND_PACKET`  
目的：只找回已有逐样本prediction，不训练、不推理、不评测、不重算指标。  
远程仓库默认：`/root/llamarec`。

## 1. 已恢复的路径与schema规则

| 机器 | Run family | 最可能评测目录 | 预期文件 |
| --- | --- | --- | --- |
| A / seed42 | N48 | `outputs/n/movielens-1m/exposure_n_s6000/popmatch_eval` | `n_valid_predictions.jsonl`, `n_test_predictions.jsonl` |
| A / seed42 | M1-48 | `outputs/m/movielens-1m/exposure_m1_s12000/popmatch_eval`；validation备选`popmatch_eval_valid_only` | `m_n_valid_predictions.jsonl`, `m_n_test_predictions.jsonl` |
| B / seed43 | N96 k5 | `outputs/n/movielens-1m/exposure_n_s12000_seed43/popmatch_eval` | `n_valid_predictions.jsonl`, `n_test_predictions.jsonl` |
| B / seed43 | M1-96 k5 | `outputs/m/movielens-1m/exposure_m1_s24000_seed43/popmatch_eval` | `m_n_valid_predictions.jsonl`, `m_n_test_predictions.jsonl` |
| B / seed43 | N96 k20/k50 | `outputs/phase2a/multiseed96_ranking_robustness/seed43/n_k0_{k20,k50}_seed42` | `n_valid_predictions.jsonl`, `n_test_predictions.jsonl` |
| B / seed43 | M1-96 k20/k50 | `outputs/phase2a/multiseed96_ranking_robustness/seed43/m1_{k20,k50}_seed42` | `m_n_valid_predictions.jsonl`, `m_n_test_predictions.jsonl` |
| C / seed44 | N96 k5 | `outputs/n/movielens-1m/exposure_n_s12000_seed44/popmatch_eval` | `n_valid_predictions.jsonl`, `n_test_predictions.jsonl` |
| C / seed44 | M1-96 k5 | `outputs/m/movielens-1m/exposure_m1_s24000_seed44/popmatch_eval` | `m_n_valid_predictions.jsonl`, `m_n_test_predictions.jsonl` |
| C / seed44 | N96 k20/k50 | `outputs/phase2a/multiseed96_ranking_robustness/seed44/n_k0_{k20,k50}_seed42` | `n_valid_predictions.jsonl`, `n_test_predictions.jsonl` |
| C / seed44 | M1-96 k20/k50 | `outputs/phase2a/multiseed96_ranking_robustness/seed44/m1_{k20,k50}_seed42` | `m_n_valid_predictions.jsonl`, `m_n_test_predictions.jsonl` |

评测器确认N prediction行应含`model, task, split, user_id, candidate_movie_ids, ground_truth_index, ground_truth_movie_id, label, label_set, candidate_generation, label_probabilities, scores, predicted_label, prompt_hash, scoring_mode, adapter_dir`。M1的N侧使用同一主体schema，`model=m_k0`且`inference_mode=m_next_item_candidate_probability`。

## 2. 通用只读检查函数

在每台实验机先执行本段。它不创建或修改文件。

```bash
set -u
ROOT=/root/llamarec

inspect_prediction() {
  p="$1"
  [ -f "$p" ] || return 0
  echo "===== PREDICTION ====="
  printf 'absolute_path='; readlink -f "$p"
  printf 'filename='; basename "$p"
  stat --printf='size_bytes=%s\nmtime=%y\n' "$p"
  du -h "$p"
  sha256sum "$p"
  case "$p" in
    *.csv|*.tsv)
      printf 'row_count_without_header='; awk 'END { print (NR > 0 ? NR-1 : 0) }' "$p"
      printf 'columns='; sed -n '1p' "$p"
      ;;
    *.jsonl)
      printf 'row_count='; wc -l < "$p"
      if command -v jq >/dev/null 2>&1; then
        printf 'schema_keys='; sed -n '1p' "$p" | jq -r 'keys | join(",")'
        echo 'identity_fields_from_first_row:'
        sed -n '1p' "$p" | jq '{model,task,inference_mode,split,user_id,ground_truth_movie_id,candidate_generation,adapter_dir}'
      else
        echo 'first_row_prefix:'
        sed -n '1p' "$p" | cut -c1-2000
      fi
      ;;
    *.json)
      if command -v jq >/dev/null 2>&1; then
        printf 'schema_keys='; jq -r 'keys | join(",")' "$p" 2>/dev/null || true
      else
        sed -n '1,40p' "$p"
      fi
      ;;
    *.pkl|*.parquet|*.npy|*.npz)
      echo 'schema=not_opened_by_read_only_shell_packet'
      ;;
  esac
}

inspect_identity_files() {
  d="$1"
  [ -d "$d" ] || return 0
  echo "===== IDENTITY DIRECTORY: $d ====="
  find "$d" -maxdepth 3 -type f \( \
    -name 'run_summary.json' -o \
    -name 'evaluation_summary.json' -o \
    -name 'config_snapshot.yaml' -o \
    -name 'evaluation_config_snapshot.yaml' -o \
    -name 'metrics.json' -o \
    -name 'valid_metrics.json' -o \
    -name 'test_metrics.json' -o \
    -name 'trainer_state.json' \
  \) -print | sort | while IFS= read -r meta; do
    echo "----- $meta"
    stat --printf='size_bytes=%s mtime=%y\n' "$meta"
    sha256sum "$meta"
    grep -nE -m 40 '"?(model|task|dataset|seed|global_step|max_steps|adapter_dir|candidate_files|variant_name|splits|counts|outputs_dir|ranking_scoring)"?[[:space:]]*[:=]' "$meta" 2>/dev/null || true
  done
}

scan_run_dir() {
  d="$1"
  if [ ! -d "$d" ]; then
    echo "MISSING_DIRECTORY $d"
    return 0
  fi
  inspect_identity_files "$d"
  find "$d" -maxdepth 4 -type f \
    \( -iname '*pred*' -o -iname '*score*' -o -iname '*rank*' \) \
    \( -iname '*.csv' -o -iname '*.json' -o -iname '*.jsonl' -o \
       -iname '*.pkl' -o -iname '*.parquet' -o -iname '*.npy' -o -iname '*.npz' \) \
    -print | sort | while IFS= read -r p; do inspect_prediction "$p"; done
}
```

## 3. 机器A：seed42 N48与M1-48

在保存seed42正式MovieLens曝光实验的机器A执行：

```bash
scan_run_dir "$ROOT/outputs/n/movielens-1m/exposure_n_s6000"
scan_run_dir "$ROOT/outputs/m/movielens-1m/exposure_m1_s12000"

echo '===== EXACT EXPECTED FILES: MACHINE A ====='
for p in \
  "$ROOT/outputs/n/movielens-1m/exposure_n_s6000/popmatch_eval/n_valid_predictions.jsonl" \
  "$ROOT/outputs/n/movielens-1m/exposure_n_s6000/popmatch_eval/n_test_predictions.jsonl" \
  "$ROOT/outputs/m/movielens-1m/exposure_m1_s12000/popmatch_eval/m_n_valid_predictions.jsonl" \
  "$ROOT/outputs/m/movielens-1m/exposure_m1_s12000/popmatch_eval/m_n_test_predictions.jsonl" \
  "$ROOT/outputs/m/movielens-1m/exposure_m1_s12000/popmatch_eval_valid_only/m_n_valid_predictions.jsonl"
do
  if [ -f "$p" ]; then inspect_prediction "$p"; else echo "NOT_FOUND $p"; fi
done
```

身份判定要求：N目录旁证应指向`exposure_n_s6000`、step 6000、seed42；M1目录应指向`exposure_m1_s12000`、step 12000、seed42；evaluation summary须绑定`k5_popmatch_seed42`且样本数为validation/test各5,675。`popmatch_eval_valid_only`只可补validation，不能冒充test。

## 4. 机器B：seed43 N96与M1-96

在保存seed43 multiseed96实验的机器B执行：

```bash
for d in \
  "$ROOT/outputs/n/movielens-1m/exposure_n_s12000_seed43" \
  "$ROOT/outputs/m/movielens-1m/exposure_m1_s24000_seed43" \
  "$ROOT/outputs/phase2a/multiseed96_ranking_robustness/seed43/n_k0_k20_seed42" \
  "$ROOT/outputs/phase2a/multiseed96_ranking_robustness/seed43/m1_k20_seed42" \
  "$ROOT/outputs/phase2a/multiseed96_ranking_robustness/seed43/n_k0_k50_seed42" \
  "$ROOT/outputs/phase2a/multiseed96_ranking_robustness/seed43/m1_k50_seed42"
do
  scan_run_dir "$d"
done

echo '===== EXPECTED PREDICTION COUNT: MACHINE B ====='
find \
  "$ROOT/outputs/n/movielens-1m/exposure_n_s12000_seed43/popmatch_eval" \
  "$ROOT/outputs/m/movielens-1m/exposure_m1_s24000_seed43/popmatch_eval" \
  "$ROOT/outputs/phase2a/multiseed96_ranking_robustness/seed43" \
  -type f \( -name 'n_valid_predictions.jsonl' -o -name 'n_test_predictions.jsonl' -o \
                -name 'm_n_valid_predictions.jsonl' -o -name 'm_n_test_predictions.jsonl' \) \
  -print 2>/dev/null | sort
```

应找到12个目标文件：k5/k20/k50 x N/M1 x validation/test。run summary或adapter path须含`seed43`；k5须绑定`k5_popmatch_seed42`，hard目录分别绑定`k20_seed42`和`k50_seed42`；每文件应为5,675行。

## 5. 机器C：seed44 N96与M1-96

在保存seed44 multiseed96实验的机器C执行：

```bash
for d in \
  "$ROOT/outputs/n/movielens-1m/exposure_n_s12000_seed44" \
  "$ROOT/outputs/m/movielens-1m/exposure_m1_s24000_seed44" \
  "$ROOT/outputs/phase2a/multiseed96_ranking_robustness/seed44/n_k0_k20_seed42" \
  "$ROOT/outputs/phase2a/multiseed96_ranking_robustness/seed44/m1_k20_seed42" \
  "$ROOT/outputs/phase2a/multiseed96_ranking_robustness/seed44/n_k0_k50_seed42" \
  "$ROOT/outputs/phase2a/multiseed96_ranking_robustness/seed44/m1_k50_seed42"
do
  scan_run_dir "$d"
done

echo '===== EXPECTED PREDICTION COUNT: MACHINE C ====='
find \
  "$ROOT/outputs/n/movielens-1m/exposure_n_s12000_seed44/popmatch_eval" \
  "$ROOT/outputs/m/movielens-1m/exposure_m1_s24000_seed44/popmatch_eval" \
  "$ROOT/outputs/phase2a/multiseed96_ranking_robustness/seed44" \
  -type f \( -name 'n_valid_predictions.jsonl' -o -name 'n_test_predictions.jsonl' -o \
                -name 'm_n_valid_predictions.jsonl' -o -name 'm_n_test_predictions.jsonl' \) \
  -print 2>/dev/null | sort
```

应找到12个目标文件，身份要求与机器B相同，但run summary或adapter path必须为`seed44`。

## 6. 精确目录未命中时的只读后备搜索

只在对应机器执行；不要在机器A重复搜索已有seed42 N96/M1-96。

```bash
echo '===== FALLBACK PREDICTION SEARCH ====='
find "$ROOT/outputs" -type f \
  \( -iname '*pred*' -o -iname '*score*' -o -iname '*rank*' \) \
  \( -iname '*.csv' -o -iname '*.json' -o -iname '*.jsonl' -o \
     -iname '*.pkl' -o -iname '*.parquet' -o -iname '*.npy' -o -iname '*.npz' \) \
  -print 2>/dev/null | grep -E \
  'exposure_n_s6000|exposure_m1_s12000|s12000_seed4[34]|s24000_seed4[34]|multiseed96_ranking_robustness/seed4[34]' \
  | sort | while IFS= read -r p; do inspect_prediction "$p"; done
```

## 7. 用户需要返回的最小terminal output

请完整返回：

1. 对应机器第3/4/5节的全部输出。
2. 若精确路径缺失，再返回第6节输出。
3. 每个候选prediction的absolute path、size、mtime、SHA256、row count和schema/首行身份字段。
4. 同目录`run_summary.json`、`evaluation_summary.json`、config snapshot、metrics和最终trainer state的身份字段与SHA256。
5. 不需要返回checkpoint、adapter权重或完整日志。

## 8. 第二阶段小文件复制命令

第一轮先不要执行。确认目标文件存在且总大小可接受后，在**接收机器**执行。远程端只读取并向stdout流式打包，不在实验机创建文件；`set -o noclobber`阻止覆盖本地已有包。将主机占位符替换为真实SSH地址。

机器A：

```bash
set -o noclobber
ssh root@MACHINE_A 'cd /root/llamarec && find outputs/n/movielens-1m/exposure_n_s6000/popmatch_eval outputs/m/movielens-1m/exposure_m1_s12000/popmatch_eval outputs/m/movielens-1m/exposure_m1_s12000/popmatch_eval_valid_only -type f \( -name "n_*_predictions.jsonl" -o -name "m_n_*_predictions.jsonl" \) -print0 2>/dev/null | sort -z | tar --null -T - -czf -' > seed42_n48_m148_predictions.tar.gz
```

机器B：

```bash
set -o noclobber
ssh root@MACHINE_B 'cd /root/llamarec && find outputs/n/movielens-1m/exposure_n_s12000_seed43/popmatch_eval outputs/m/movielens-1m/exposure_m1_s24000_seed43/popmatch_eval outputs/phase2a/multiseed96_ranking_robustness/seed43 -type f \( -name "n_*_predictions.jsonl" -o -name "m_n_*_predictions.jsonl" \) -print0 2>/dev/null | sort -z | tar --null -T - -czf -' > seed43_n96_m196_predictions.tar.gz
```

机器C：

```bash
set -o noclobber
ssh root@MACHINE_C 'cd /root/llamarec && find outputs/n/movielens-1m/exposure_n_s12000_seed44/popmatch_eval outputs/m/movielens-1m/exposure_m1_s24000_seed44/popmatch_eval outputs/phase2a/multiseed96_ranking_robustness/seed44 -type f \( -name "n_*_predictions.jsonl" -o -name "m_n_*_predictions.jsonl" \) -print0 2>/dev/null | sort -z | tar --null -T - -czf -' > seed44_n96_m196_predictions.tar.gz
```

这些命令不包含Python、不调用训练/推理/评测入口，也不会改动远程artifact。
