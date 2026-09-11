# Missing Prediction Report: Machine A

- generated_utc: 2026-09-11T08:50:48Z
- hostname: ubuntu22
- machine: A
- expected_seed: 42
- repository_root: /root/llamarec
- repository_head: a9c6cd959cf32afe046bb05be9eb5096bebfc5fb
- training_invoked: NO
- inference_invoked: NO

## Candidate directories

### `/root/llamarec/outputs/n/movielens-1m/exposure_n_s6000/popmatch_eval`

- status: FOUND
- absolute_path: /root/llamarec/outputs/n/movielens-1m/exposure_n_s6000/popmatch_eval

#### Identity metadata

- file: /root/llamarec/outputs/n/movielens-1m/exposure_n_s6000/popmatch_eval/evaluation_summary.json
  size: 813
  mtime: 2026-08-28 23:58:08.706194262 +0800
  sha256: b14b50bdcf0551c5148f3cbc5b8a3d1bca6aa798c0d8ad0c1a3c207ed9adf91a
  identity: {"model":"n_k0","dataset":"movielens-1m","seed":null,"splits":["validation","test"],"adapter_dir":"/root/llamarec/outputs/n/movielens-1m/exposure_n_s6000/adapter","candidate_files":{"validation":"/root/llamarec/data/candidates/movielens-1m/variants/k5_popmatch_seed42/valid.jsonl","test":"/root/llamarec/data/candidates/movielens-1m/variants/k5_popmatch_seed42/test.jsonl"},"counts":{"validation":{"n_predictions":5675},"test":{"n_predictions":5675}},"outputs_dir":"/root/llamarec/outputs/n/movielens-1m/exposure_n_s6000/popmatch_eval","global_step":null,"max_steps":null}
- file: /root/llamarec/outputs/n/movielens-1m/exposure_n_s6000/popmatch_eval/evaluation_config_snapshot.yaml
  size: 8112
  mtime: 2026-08-28 23:33:14.294638234 +0800
  sha256: 7aebb51231b2e81ef49bba9aedbce15d41a3c0184b91b3c737f101e2068f108b
  identity: seed:;dataset:;model:;
- file: /root/llamarec/outputs/n/movielens-1m/exposure_n_s6000/popmatch_eval/valid_metrics.json
  size: 364
  mtime: 2026-08-28 23:45:38.077502523 +0800
  sha256: 76623b6243b5440326503248073cf3081aaeaa1529c483e7c05e21f179a62e9e
  identity: {"model":"n_k0","dataset":"movielens-1m","seed":null,"splits":null,"adapter_dir":"/root/llamarec/outputs/n/movielens-1m/exposure_n_s6000/adapter","candidate_files":null,"counts":null,"outputs_dir":null,"global_step":null,"max_steps":null}
- file: /root/llamarec/outputs/n/movielens-1m/exposure_n_s6000/popmatch_eval/test_metrics.json
  size: 357
  mtime: 2026-08-28 23:58:08.702194398 +0800
  sha256: 35e06761fb550d06abb015ed546881110c8179015875584f3c476881080a72ad
  identity: {"model":"n_k0","dataset":"movielens-1m","seed":null,"splits":null,"adapter_dir":"/root/llamarec/outputs/n/movielens-1m/exposure_n_s6000/adapter","candidate_files":null,"counts":null,"outputs_dir":null,"global_step":null,"max_steps":null}
- file: /root/llamarec/outputs/n/movielens-1m/exposure_n_s6000/run_summary.json
  size: 340
  mtime: 2026-08-28 10:16:08.231866614 +0800
  sha256: 08175915d123ed755a424bc2150ed69a3ae8b50348f8d5fa581b03534b9fb8c7
  identity: {"model":"n_k0","dataset":"movielens-1m","seed":42,"splits":null,"adapter_dir":null,"candidate_files":null,"counts":null,"outputs_dir":null,"global_step":null,"max_steps":null}
- file: /root/llamarec/outputs/n/movielens-1m/exposure_n_s6000/config_snapshot.yaml
  size: 8112
  mtime: 2026-08-28 10:16:08.231866614 +0800
  sha256: 7aebb51231b2e81ef49bba9aedbce15d41a3c0184b91b3c737f101e2068f108b
  identity: seed:;dataset:;model:;
- file: /root/llamarec/outputs/n/movielens-1m/exposure_n_s6000/metrics.json
  size: 777
  mtime: 2026-08-28 15:32:22.833741106 +0800
  sha256: 8bee85fd6c3777491fc936ddf762f640871a5dba649b29063fdeb7aa48d9e70c
  identity: {"model":"n_k0","dataset":"movielens-1m","seed":42,"splits":null,"adapter_dir":null,"candidate_files":null,"counts":null,"outputs_dir":null,"global_step":null,"max_steps":null}

#### Prediction candidates

- file: /root/llamarec/outputs/n/movielens-1m/exposure_n_s6000/popmatch_eval/n_test_predictions.jsonl
  absolute_path: /root/llamarec/outputs/n/movielens-1m/exposure_n_s6000/popmatch_eval/n_test_predictions.jsonl
  size: 6240327
  mtime: 2026-08-28 23:58:08.578198639 +0800
  sha256: 2571eb44757a98410a6b32f4dde6ab4121a4e4653eca7aa50d9cc39879addf96
  rows: 5675
  schema: adapter_dir,candidate_generation,candidate_movie_ids,ground_truth_index,ground_truth_movie_id,inference_mode,label,label_probabilities,label_set,model,predicted_label,prompt_hash,scores,scoring_mode,split,task,user_id
  first_row_identity: {"model":"n_k0","task":"N","inference_mode":"candidate_label_probability","split":"test","user_id":"1","ground_truth_movie_id":"48","candidate_generation":{"method":"popularity_matched","variant_name":"k5_popmatch_seed42","candidate_num":5,"negative_num":4,"seed":244,"pool":"all_movies_minus_current_ground_truth_item","shuffle_order":true,"target_popularity":382,"negative_popularity_mean":387.5,"negative_popularity_min":386,"negative_popularity_max":389},"adapter_dir":"/root/llamarec/outputs/n/movielens-1m/exposure_n_s6000/adapter"}
- file: /root/llamarec/outputs/n/movielens-1m/exposure_n_s6000/popmatch_eval/n_valid_predictions.jsonl
  absolute_path: /root/llamarec/outputs/n/movielens-1m/exposure_n_s6000/popmatch_eval/n_valid_predictions.jsonl
  size: 6274577
  mtime: 2026-08-28 23:45:38.029502510 +0800
  sha256: 17939eb035919c8304cf02bbd31b1de3194b0e70e0b0136ae96f04dfc2f81dd6
  rows: 5675
  schema: adapter_dir,candidate_generation,candidate_movie_ids,ground_truth_index,ground_truth_movie_id,inference_mode,label,label_probabilities,label_set,model,predicted_label,prompt_hash,scores,scoring_mode,split,task,user_id
  first_row_identity: {"model":"n_k0","task":"N","inference_mode":"candidate_label_probability","split":"validation","user_id":"1","ground_truth_movie_id":"527","candidate_generation":{"method":"popularity_matched","variant_name":"k5_popmatch_seed42","candidate_num":5,"negative_num":4,"seed":143,"pool":"all_movies_minus_current_ground_truth_item","shuffle_order":true,"target_popularity":2304,"negative_popularity_mean":2208.75,"negative_popularity_min":2098,"negative_popularity_max":2288},"adapter_dir":"/root/llamarec/outputs/n/movielens-1m/exposure_n_s6000/adapter"}

### `/root/llamarec/outputs/m/movielens-1m/exposure_m1_s12000/popmatch_eval`

- status: FOUND
- absolute_path: /root/llamarec/outputs/m/movielens-1m/exposure_m1_s12000/popmatch_eval

#### Identity metadata

- file: /root/llamarec/outputs/m/movielens-1m/exposure_m1_s12000/popmatch_eval/evaluation_summary.json
  size: 716
  mtime: 2026-09-02 16:55:39.196849791 +0800
  sha256: 2b7d733c54d3d6a67da3f7a417e84354c4dc30e540d8216758a692382a37719e
  identity: {"model":"m_k0","dataset":"movielens-1m","seed":null,"splits":["test"],"adapter_dir":"/root/llamarec/outputs/m/movielens-1m/exposure_m1_s12000/adapter","candidate_files":{"test":"/root/llamarec/data/candidates/movielens-1m/variants/k5_popmatch_seed42/test.jsonl"},"counts":{"test":{"m_y_predictions":11544,"m_n_predictions":5675}},"outputs_dir":"/root/llamarec/outputs/m/movielens-1m/exposure_m1_s12000/popmatch_eval","global_step":null,"max_steps":null}
- file: /root/llamarec/outputs/m/movielens-1m/exposure_m1_s12000/popmatch_eval/evaluation_config_snapshot.yaml
  size: 8268
  mtime: 2026-09-02 16:27:32.111245203 +0800
  sha256: 444ea827915a8b1dbc99144c5ee7ce4dd8c0a2a8228b932bf5c380d8676d53d4
  identity: seed:;dataset:;model:;
- file: /root/llamarec/outputs/m/movielens-1m/exposure_m1_s12000/popmatch_eval/test_metrics.json
  size: 540
  mtime: 2026-09-02 16:55:39.196849791 +0800
  sha256: bf18a9f9a7f19d6ce245ec77a6910297af68067070dc9e36041737d9bfd50b68
  identity: {"model":"m_k0","dataset":"movielens-1m","seed":null,"splits":null,"adapter_dir":"/root/llamarec/outputs/m/movielens-1m/exposure_m1_s12000/adapter","candidate_files":null,"counts":null,"outputs_dir":null,"global_step":null,"max_steps":null}
- file: /root/llamarec/outputs/m/movielens-1m/exposure_m1_s12000/run_summary.json
  size: 879
  mtime: 2026-08-30 13:01:52.293844008 +0800
  sha256: d681b38930f3f7313514180a1908878fe0c618b3c04120e5655fb933129ac2c8
  identity: {"model":"m_k0","dataset":"movielens-1m","seed":42,"splits":null,"adapter_dir":null,"candidate_files":null,"counts":null,"outputs_dir":null,"global_step":null,"max_steps":null}
- file: /root/llamarec/outputs/m/movielens-1m/exposure_m1_s12000/config_snapshot.yaml
  size: 8268
  mtime: 2026-08-30 13:01:52.293844008 +0800
  sha256: 444ea827915a8b1dbc99144c5ee7ce4dd8c0a2a8228b932bf5c380d8676d53d4
  identity: seed:;dataset:;model:;

#### Prediction candidates

- file: /root/llamarec/outputs/m/movielens-1m/exposure_m1_s12000/popmatch_eval/m_n_test_predictions.jsonl
  absolute_path: /root/llamarec/outputs/m/movielens-1m/exposure_m1_s12000/popmatch_eval/m_n_test_predictions.jsonl
  size: 6284311
  mtime: 2026-09-02 16:55:39.164851238 +0800
  sha256: 4d815a424f557edfe1accaf8fa8463074c14d641807eb64372ef4618c5e718bf
  rows: 5675
  schema: adapter_dir,candidate_generation,candidate_movie_ids,ground_truth_index,ground_truth_movie_id,inference_mode,label,label_probabilities,label_set,model,predicted_label,prompt_hash,scores,scoring_mode,split,task,user_id
  first_row_identity: {"model":"m_k0","task":"N","inference_mode":"m_next_item_candidate_probability","split":"test","user_id":"1","ground_truth_movie_id":"48","candidate_generation":{"method":"popularity_matched","variant_name":"k5_popmatch_seed42","candidate_num":5,"negative_num":4,"seed":244,"pool":"all_movies_minus_current_ground_truth_item","shuffle_order":true,"target_popularity":382,"negative_popularity_mean":387.5,"negative_popularity_min":386,"negative_popularity_max":389},"adapter_dir":"/root/llamarec/outputs/m/movielens-1m/exposure_m1_s12000/adapter"}
- file: /root/llamarec/outputs/m/movielens-1m/exposure_m1_s12000/popmatch_eval/m_y_test_predictions.jsonl
  absolute_path: /root/llamarec/outputs/m/movielens-1m/exposure_m1_s12000/popmatch_eval/m_y_test_predictions.jsonl
  size: 4809522
  mtime: 2026-09-02 16:46:25.834471124 +0800
  sha256: 2f6525a28f3a316327cc4902848142ddd066d4ea541447bb1b3cce8551ea10fd
  rows: 11544
  schema: adapter_dir,inference_mode,label,model,p_no,p_yes,predicted_label,prompt_hash,score,scoring_mode,split,target_movie_id,task,user_id
  first_row_identity: {"model":"m_k0","task":"Y","inference_mode":"m_yesno_p_yes","split":"test","user_id":"1","ground_truth_movie_id":null,"candidate_generation":null,"adapter_dir":"/root/llamarec/outputs/m/movielens-1m/exposure_m1_s12000/adapter"}

### `/root/llamarec/outputs/m/movielens-1m/exposure_m1_s12000/popmatch_eval_valid_only`

- status: FOUND
- absolute_path: /root/llamarec/outputs/m/movielens-1m/exposure_m1_s12000/popmatch_eval_valid_only

#### Identity metadata

- file: /root/llamarec/outputs/m/movielens-1m/exposure_m1_s12000/popmatch_eval_valid_only/evaluation_summary.json
  size: 746
  mtime: 2026-09-01 09:23:37.666936054 +0800
  sha256: 51c5b5fd7dc7916613488ef0f96a6268d66ed053673e038cfca5ad4603d2e393
  identity: {"model":"m_k0","dataset":"movielens-1m","seed":null,"splits":["validation"],"adapter_dir":"/root/llamarec/outputs/m/movielens-1m/exposure_m1_s12000/adapter","candidate_files":{"validation":"/root/llamarec/data/candidates/movielens-1m/variants/k5_popmatch_seed42/valid.jsonl"},"counts":{"validation":{"m_y_predictions":12381,"m_n_predictions":5675}},"outputs_dir":"/root/llamarec/outputs/m/movielens-1m/exposure_m1_s12000/popmatch_eval_valid_only","global_step":null,"max_steps":null}
- file: /root/llamarec/outputs/m/movielens-1m/exposure_m1_s12000/popmatch_eval_valid_only/evaluation_config_snapshot.yaml
  size: 8268
  mtime: 2026-09-01 08:59:46.815481862 +0800
  sha256: 444ea827915a8b1dbc99144c5ee7ce4dd8c0a2a8228b932bf5c380d8676d53d4
  identity: seed:;dataset:;model:;
- file: /root/llamarec/outputs/m/movielens-1m/exposure_m1_s12000/popmatch_eval_valid_only/valid_metrics.json
  size: 546
  mtime: 2026-09-01 09:23:37.666936054 +0800
  sha256: 170585bf2160edcb2aebdd026eda4632fe220128321e011980454ac1e59ca014
  identity: {"model":"m_k0","dataset":"movielens-1m","seed":null,"splits":null,"adapter_dir":"/root/llamarec/outputs/m/movielens-1m/exposure_m1_s12000/adapter","candidate_files":null,"counts":null,"outputs_dir":null,"global_step":null,"max_steps":null}
- file: /root/llamarec/outputs/m/movielens-1m/exposure_m1_s12000/run_summary.json
  size: 879
  mtime: 2026-08-30 13:01:52.293844008 +0800
  sha256: d681b38930f3f7313514180a1908878fe0c618b3c04120e5655fb933129ac2c8
  identity: {"model":"m_k0","dataset":"movielens-1m","seed":42,"splits":null,"adapter_dir":null,"candidate_files":null,"counts":null,"outputs_dir":null,"global_step":null,"max_steps":null}
- file: /root/llamarec/outputs/m/movielens-1m/exposure_m1_s12000/config_snapshot.yaml
  size: 8268
  mtime: 2026-08-30 13:01:52.293844008 +0800
  sha256: 444ea827915a8b1dbc99144c5ee7ce4dd8c0a2a8228b932bf5c380d8676d53d4
  identity: seed:;dataset:;model:;

#### Prediction candidates

- file: /root/llamarec/outputs/m/movielens-1m/exposure_m1_s12000/popmatch_eval_valid_only/m_n_valid_predictions.jsonl
  absolute_path: /root/llamarec/outputs/m/movielens-1m/exposure_m1_s12000/popmatch_eval_valid_only/m_n_valid_predictions.jsonl
  size: 6318411
  mtime: 2026-09-01 09:23:37.598936206 +0800
  sha256: f4e93f3d6ac735b8853ccabe83fd177682b35323255232f46c2e5f69d190f39a
  rows: 5675
  schema: adapter_dir,candidate_generation,candidate_movie_ids,ground_truth_index,ground_truth_movie_id,inference_mode,label,label_probabilities,label_set,model,predicted_label,prompt_hash,scores,scoring_mode,split,task,user_id
  first_row_identity: {"model":"m_k0","task":"N","inference_mode":"m_next_item_candidate_probability","split":"validation","user_id":"1","ground_truth_movie_id":"527","candidate_generation":{"method":"popularity_matched","variant_name":"k5_popmatch_seed42","candidate_num":5,"negative_num":4,"seed":143,"pool":"all_movies_minus_current_ground_truth_item","shuffle_order":true,"target_popularity":2304,"negative_popularity_mean":2208.75,"negative_popularity_min":2098,"negative_popularity_max":2288},"adapter_dir":"/root/llamarec/outputs/m/movielens-1m/exposure_m1_s12000/adapter"}
- file: /root/llamarec/outputs/m/movielens-1m/exposure_m1_s12000/popmatch_eval_valid_only/m_y_valid_predictions.jsonl
  absolute_path: /root/llamarec/outputs/m/movielens-1m/exposure_m1_s12000/popmatch_eval_valid_only/m_y_valid_predictions.jsonl
  size: 5230914
  mtime: 2026-09-01 09:16:09.281347539 +0800
  sha256: 3571649cba966c330c3e59ad71c91fe11d177ee99a9b654e5a7e18ffae7d2c37
  rows: 12381
  schema: adapter_dir,inference_mode,label,model,p_no,p_yes,predicted_label,prompt_hash,score,scoring_mode,split,target_movie_id,task,user_id
  first_row_identity: {"model":"m_k0","task":"Y","inference_mode":"m_yesno_p_yes","split":"validation","user_id":"1","ground_truth_movie_id":null,"candidate_generation":null,"adapter_dir":"/root/llamarec/outputs/m/movielens-1m/exposure_m1_s12000/adapter"}

