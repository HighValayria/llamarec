# Missing Prediction Report: Machine C

- generated_utc: 2026-09-11T08:56:22Z
- hostname: ubuntu22
- machine: C
- expected_seed: 44
- repository_root: /root/llamarec
- repository_head: a1fa349141b8ea6060de9f44f89e93d60c277f8d
- training_invoked: NO
- inference_invoked: NO

## Candidate directories

### `/root/llamarec/outputs/n/movielens-1m/exposure_n_s12000_seed44/popmatch_eval`

- status: FOUND
- absolute_path: /root/llamarec/outputs/n/movielens-1m/exposure_n_s12000_seed44/popmatch_eval

#### Identity metadata

- file: /root/llamarec/outputs/n/movielens-1m/exposure_n_s12000_seed44/popmatch_eval/evaluation_summary.json
  size: 651
  mtime: 2026-09-08 09:18:20.190185608 +0800
  sha256: b86de5df34efdaf3d397606dc02ad7065a5a26242be2824e51f757fa06395865
  identity: {"model":"n_k0","dataset":"movielens-1m","seed":null,"splits":["test"],"adapter_dir":"/root/llamarec/outputs/n/movielens-1m/exposure_n_s12000_seed44/adapter","candidate_files":{"test":"/root/llamarec/data/candidates/movielens-1m/variants/k5_popmatch_seed42/test.jsonl"},"counts":{"test":{"n_predictions":5675}},"outputs_dir":"/root/llamarec/outputs/n/movielens-1m/exposure_n_s12000_seed44/popmatch_eval","global_step":null,"max_steps":null}
- file: /root/llamarec/outputs/n/movielens-1m/exposure_n_s12000_seed44/popmatch_eval/evaluation_config_snapshot.yaml
  size: 8112
  mtime: 2026-09-08 09:09:06.353367570 +0800
  sha256: 7aebb51231b2e81ef49bba9aedbce15d41a3c0184b91b3c737f101e2068f108b
  identity: seed:;dataset:;model:;
- file: /root/llamarec/outputs/n/movielens-1m/exposure_n_s12000_seed44/popmatch_eval/valid_metrics.json
  size: 371
  mtime: 2026-09-07 01:14:58.081214826 +0800
  sha256: e74dddfdcc7a8b45df90c18466c4dae7a8d751dc5e6ce5667bf306853bf5b828
  identity: {"model":"n_k0","dataset":"movielens-1m","seed":null,"splits":null,"adapter_dir":"/root/llamarec/outputs/n/movielens-1m/exposure_n_s12000_seed44/adapter","candidate_files":null,"counts":null,"outputs_dir":null,"global_step":null,"max_steps":null}
- file: /root/llamarec/outputs/n/movielens-1m/exposure_n_s12000_seed44/popmatch_eval/test_metrics.json
  size: 366
  mtime: 2026-09-08 09:18:20.190185608 +0800
  sha256: 04bd62daddbf2e4c15a10c96636464979b06c599cae229edfc1497a3fb879075
  identity: {"model":"n_k0","dataset":"movielens-1m","seed":null,"splits":null,"adapter_dir":"/root/llamarec/outputs/n/movielens-1m/exposure_n_s12000_seed44/adapter","candidate_files":null,"counts":null,"outputs_dir":null,"global_step":null,"max_steps":null}
- file: /root/llamarec/outputs/n/movielens-1m/exposure_n_s12000_seed44/run_summary.json
  size: 348
  mtime: 2026-09-06 13:13:32.577612526 +0800
  sha256: 9cf6ae016f239a176f84a44e8d45f7ab5a5874bcd0e4b423731f5f6fb519c495
  identity: {"model":"n_k0","dataset":"movielens-1m","seed":44,"splits":null,"adapter_dir":null,"candidate_files":null,"counts":null,"outputs_dir":null,"global_step":null,"max_steps":null}
- file: /root/llamarec/outputs/n/movielens-1m/exposure_n_s12000_seed44/config_snapshot.yaml
  size: 8112
  mtime: 2026-09-06 13:13:32.573612513 +0800
  sha256: 7aebb51231b2e81ef49bba9aedbce15d41a3c0184b91b3c737f101e2068f108b
  identity: seed:;dataset:;model:;
- file: /root/llamarec/outputs/n/movielens-1m/exposure_n_s12000_seed44/metrics.json
  size: 677
  mtime: 2026-09-07 01:05:38.645322904 +0800
  sha256: 4e251f393aa0034eb365fcf497daa9e1f212531c099068de349d7ea56f89a31d
  identity: {"model":"n_k0","dataset":"movielens-1m","seed":44,"splits":null,"adapter_dir":null,"candidate_files":null,"counts":null,"outputs_dir":null,"global_step":null,"max_steps":null}

#### Prediction candidates

- file: /root/llamarec/outputs/n/movielens-1m/exposure_n_s12000_seed44/popmatch_eval/n_test_predictions.jsonl
  absolute_path: /root/llamarec/outputs/n/movielens-1m/exposure_n_s12000_seed44/popmatch_eval/n_test_predictions.jsonl
  size: 6287449
  mtime: 2026-09-08 09:18:20.166192680 +0800
  sha256: d9bc5f5850037c77e0ebb674085ea573a1d3557db55fddbbffd5972fe1121273
  rows: 5675
  schema: adapter_dir,candidate_generation,candidate_movie_ids,ground_truth_index,ground_truth_movie_id,inference_mode,label,label_probabilities,label_set,model,predicted_label,prompt_hash,scores,scoring_mode,split,task,user_id
  first_row_identity: {"model":"n_k0","task":"N","inference_mode":"candidate_label_probability","split":"test","user_id":"1","ground_truth_movie_id":"48","candidate_generation":{"method":"popularity_matched","variant_name":"k5_popmatch_seed42","candidate_num":5,"negative_num":4,"seed":244,"pool":"all_movies_minus_current_ground_truth_item","shuffle_order":true,"target_popularity":382,"negative_popularity_mean":387.5,"negative_popularity_min":386,"negative_popularity_max":389},"adapter_dir":"/root/llamarec/outputs/n/movielens-1m/exposure_n_s12000_seed44/adapter"}
- file: /root/llamarec/outputs/n/movielens-1m/exposure_n_s12000_seed44/popmatch_eval/n_valid_predictions.jsonl
  absolute_path: /root/llamarec/outputs/n/movielens-1m/exposure_n_s12000_seed44/popmatch_eval/n_valid_predictions.jsonl
  size: 6322067
  mtime: 2026-09-07 01:14:58.057216020 +0800
  sha256: 84fb2647cefb9e061ed0f0b15e9ed3e535dcd0d43a15a9ef968e080ae0ddf16d
  rows: 5675
  schema: adapter_dir,candidate_generation,candidate_movie_ids,ground_truth_index,ground_truth_movie_id,inference_mode,label,label_probabilities,label_set,model,predicted_label,prompt_hash,scores,scoring_mode,split,task,user_id
  first_row_identity: {"model":"n_k0","task":"N","inference_mode":"candidate_label_probability","split":"validation","user_id":"1","ground_truth_movie_id":"527","candidate_generation":{"method":"popularity_matched","variant_name":"k5_popmatch_seed42","candidate_num":5,"negative_num":4,"seed":143,"pool":"all_movies_minus_current_ground_truth_item","shuffle_order":true,"target_popularity":2304,"negative_popularity_mean":2208.75,"negative_popularity_min":2098,"negative_popularity_max":2288},"adapter_dir":"/root/llamarec/outputs/n/movielens-1m/exposure_n_s12000_seed44/adapter"}

### `/root/llamarec/outputs/m/movielens-1m/exposure_m1_s24000_seed44/popmatch_eval`

- status: FOUND
- absolute_path: /root/llamarec/outputs/m/movielens-1m/exposure_m1_s24000_seed44/popmatch_eval

#### Identity metadata

- file: /root/llamarec/outputs/m/movielens-1m/exposure_m1_s24000_seed44/popmatch_eval/evaluation_summary.json
  size: 730
  mtime: 2026-09-08 09:46:52.780631209 +0800
  sha256: 6a37248df210a2f0e0c599f5aaa6cf698adc596f88b636eb58adf3d824d77d1c
  identity: {"model":"m_k0","dataset":"movielens-1m","seed":null,"splits":["test"],"adapter_dir":"/root/llamarec/outputs/m/movielens-1m/exposure_m1_s24000_seed44/adapter","candidate_files":{"test":"/root/llamarec/data/candidates/movielens-1m/variants/k5_popmatch_seed42/test.jsonl"},"counts":{"test":{"m_y_predictions":11544,"m_n_predictions":5675}},"outputs_dir":"/root/llamarec/outputs/m/movielens-1m/exposure_m1_s24000_seed44/popmatch_eval","global_step":null,"max_steps":null}
- file: /root/llamarec/outputs/m/movielens-1m/exposure_m1_s24000_seed44/popmatch_eval/evaluation_config_snapshot.yaml
  size: 8268
  mtime: 2026-09-08 09:18:30.315201169 +0800
  sha256: 444ea827915a8b1dbc99144c5ee7ce4dd8c0a2a8228b932bf5c380d8676d53d4
  identity: seed:;dataset:;model:;
- file: /root/llamarec/outputs/m/movielens-1m/exposure_m1_s24000_seed44/popmatch_eval/valid_metrics.json
  size: 553
  mtime: 2026-09-08 01:09:33.534343449 +0800
  sha256: a3fd0236c593b61abd1e2d0565ae6bbb2622d93507e9514e197ee94dc24f073f
  identity: {"model":"m_k0","dataset":"movielens-1m","seed":null,"splits":null,"adapter_dir":"/root/llamarec/outputs/m/movielens-1m/exposure_m1_s24000_seed44/adapter","candidate_files":null,"counts":null,"outputs_dir":null,"global_step":null,"max_steps":null}
- file: /root/llamarec/outputs/m/movielens-1m/exposure_m1_s24000_seed44/popmatch_eval/test_metrics.json
  size: 543
  mtime: 2026-09-08 09:46:52.780631209 +0800
  sha256: 34400aa5902d55b0887498e9c79f7ca59495137b5d920990311df8aac436cab3
  identity: {"model":"m_k0","dataset":"movielens-1m","seed":null,"splits":null,"adapter_dir":"/root/llamarec/outputs/m/movielens-1m/exposure_m1_s24000_seed44/adapter","candidate_files":null,"counts":null,"outputs_dir":null,"global_step":null,"max_steps":null}
- file: /root/llamarec/outputs/m/movielens-1m/exposure_m1_s24000_seed44/run_summary.json
  size: 886
  mtime: 2026-09-07 01:15:17.428246730 +0800
  sha256: d7db86cb90e277a38ab509d90e1f54d0e8f2608010e05165ca75340723131876
  identity: {"model":"m_k0","dataset":"movielens-1m","seed":44,"splits":null,"adapter_dir":null,"candidate_files":null,"counts":null,"outputs_dir":null,"global_step":null,"max_steps":null}
- file: /root/llamarec/outputs/m/movielens-1m/exposure_m1_s24000_seed44/config_snapshot.yaml
  size: 8268
  mtime: 2026-09-07 01:15:17.428246730 +0800
  sha256: 444ea827915a8b1dbc99144c5ee7ce4dd8c0a2a8228b932bf5c380d8676d53d4
  identity: seed:;dataset:;model:;
- file: /root/llamarec/outputs/m/movielens-1m/exposure_m1_s24000_seed44/metrics.json
  size: 852
  mtime: 2026-09-08 00:39:31.096001637 +0800
  sha256: 3c4ae024bd0e0a7e67910c9b782ab0eff70d5c316df85a922aa1a3d17a4b223e
  identity: {"model":"m_k0","dataset":"movielens-1m","seed":44,"splits":null,"adapter_dir":null,"candidate_files":null,"counts":null,"outputs_dir":null,"global_step":null,"max_steps":null}

#### Prediction candidates

- file: /root/llamarec/outputs/m/movielens-1m/exposure_m1_s24000_seed44/popmatch_eval/m_n_test_predictions.jsonl
  absolute_path: /root/llamarec/outputs/m/movielens-1m/exposure_m1_s24000_seed44/popmatch_eval/m_n_test_predictions.jsonl
  size: 6327614
  mtime: 2026-09-08 09:46:52.744631796 +0800
  sha256: 5bedc31b9c19197c1a3baf4ee84889de01ce31eb3cb801c4195617ed468189c5
  rows: 5675
  schema: adapter_dir,candidate_generation,candidate_movie_ids,ground_truth_index,ground_truth_movie_id,inference_mode,label,label_probabilities,label_set,model,predicted_label,prompt_hash,scores,scoring_mode,split,task,user_id
  first_row_identity: {"model":"m_k0","task":"N","inference_mode":"m_next_item_candidate_probability","split":"test","user_id":"1","ground_truth_movie_id":"48","candidate_generation":{"method":"popularity_matched","variant_name":"k5_popmatch_seed42","candidate_num":5,"negative_num":4,"seed":244,"pool":"all_movies_minus_current_ground_truth_item","shuffle_order":true,"target_popularity":382,"negative_popularity_mean":387.5,"negative_popularity_min":386,"negative_popularity_max":389},"adapter_dir":"/root/llamarec/outputs/m/movielens-1m/exposure_m1_s24000_seed44/adapter"}
- file: /root/llamarec/outputs/m/movielens-1m/exposure_m1_s24000_seed44/popmatch_eval/m_n_valid_predictions.jsonl
  absolute_path: /root/llamarec/outputs/m/movielens-1m/exposure_m1_s24000_seed44/popmatch_eval/m_n_valid_predictions.jsonl
  size: 6361770
  mtime: 2026-09-08 01:09:33.498343594 +0800
  sha256: 317ad0aab3d3906bc6365f16cabddab5490cfb65bb5e89ec005a3cd3ef772074
  rows: 5675
  schema: adapter_dir,candidate_generation,candidate_movie_ids,ground_truth_index,ground_truth_movie_id,inference_mode,label,label_probabilities,label_set,model,predicted_label,prompt_hash,scores,scoring_mode,split,task,user_id
  first_row_identity: {"model":"m_k0","task":"N","inference_mode":"m_next_item_candidate_probability","split":"validation","user_id":"1","ground_truth_movie_id":"527","candidate_generation":{"method":"popularity_matched","variant_name":"k5_popmatch_seed42","candidate_num":5,"negative_num":4,"seed":143,"pool":"all_movies_minus_current_ground_truth_item","shuffle_order":true,"target_popularity":2304,"negative_popularity_mean":2208.75,"negative_popularity_min":2098,"negative_popularity_max":2288},"adapter_dir":"/root/llamarec/outputs/m/movielens-1m/exposure_m1_s24000_seed44/adapter"}
- file: /root/llamarec/outputs/m/movielens-1m/exposure_m1_s24000_seed44/popmatch_eval/m_y_test_predictions.jsonl
  absolute_path: /root/llamarec/outputs/m/movielens-1m/exposure_m1_s24000_seed44/popmatch_eval/m_y_test_predictions.jsonl
  size: 4897200
  mtime: 2026-09-08 09:37:33.258308236 +0800
  sha256: 88ffd300c06d82cb85d35f87385a2d2d6d8bdc9ace0c87bea6be7ba583996166
  rows: 11544
  schema: adapter_dir,inference_mode,label,model,p_no,p_yes,predicted_label,prompt_hash,score,scoring_mode,split,target_movie_id,task,user_id
  first_row_identity: {"model":"m_k0","task":"Y","inference_mode":"m_yesno_p_yes","split":"test","user_id":"1","ground_truth_movie_id":null,"candidate_generation":null,"adapter_dir":"/root/llamarec/outputs/m/movielens-1m/exposure_m1_s24000_seed44/adapter"}
- file: /root/llamarec/outputs/m/movielens-1m/exposure_m1_s24000_seed44/popmatch_eval/m_y_valid_predictions.jsonl
  absolute_path: /root/llamarec/outputs/m/movielens-1m/exposure_m1_s24000_seed44/popmatch_eval/m_y_valid_predictions.jsonl
  size: 5325481
  mtime: 2026-09-08 01:00:10.450309935 +0800
  sha256: 2d3d3b3a56cb65f58fd360b35313d7ead64f029c4df748b927388438ba43e41a
  rows: 12381
  schema: adapter_dir,inference_mode,label,model,p_no,p_yes,predicted_label,prompt_hash,score,scoring_mode,split,target_movie_id,task,user_id
  first_row_identity: {"model":"m_k0","task":"Y","inference_mode":"m_yesno_p_yes","split":"validation","user_id":"1","ground_truth_movie_id":null,"candidate_generation":null,"adapter_dir":"/root/llamarec/outputs/m/movielens-1m/exposure_m1_s24000_seed44/adapter"}

### `/root/llamarec/outputs/phase2a/multiseed96_ranking_robustness/seed44/n_k0_k20_seed42`

- status: FOUND
- absolute_path: /root/llamarec/outputs/phase2a/multiseed96_ranking_robustness/seed44/n_k0_k20_seed42

#### Identity metadata

- file: /root/llamarec/outputs/phase2a/multiseed96_ranking_robustness/seed44/n_k0_k20_seed42/evaluation_summary.json
  size: 651
  mtime: 2026-09-08 09:56:44.689697779 +0800
  sha256: 628bb658ac87d6a35066fc30e21b5fbcf01607c8598ee1fb3ca7545d5c63ae18
  identity: {"model":"n_k0","dataset":"movielens-1m","seed":null,"splits":["test"],"adapter_dir":"/root/llamarec/outputs/n/movielens-1m/exposure_n_s12000_seed44/adapter","candidate_files":{"test":"/root/llamarec/data/candidates/movielens-1m/variants/k20_seed42/test.jsonl"},"counts":{"test":{"n_predictions":5675}},"outputs_dir":"/root/llamarec/outputs/phase2a/multiseed96_ranking_robustness/seed44/n_k0_k20_seed42","global_step":null,"max_steps":null}
- file: /root/llamarec/outputs/phase2a/multiseed96_ranking_robustness/seed44/n_k0_k20_seed42/evaluation_config_snapshot.yaml
  size: 8112
  mtime: 2026-09-08 09:47:03.040408079 +0800
  sha256: 7aebb51231b2e81ef49bba9aedbce15d41a3c0184b91b3c737f101e2068f108b
  identity: seed:;dataset:;model:;
- file: /root/llamarec/outputs/phase2a/multiseed96_ranking_robustness/seed44/n_k0_k20_seed42/valid_metrics.json
  size: 511
  mtime: 2026-09-08 01:19:27.488833926 +0800
  sha256: 19d8073c1ad380adb07ac432243ecc6c4f237b4cbc0a142f8f348d7310d22ecf
  identity: {"model":"n_k0","dataset":"movielens-1m","seed":null,"splits":null,"adapter_dir":"/root/llamarec/outputs/n/movielens-1m/exposure_n_s12000_seed44/adapter","candidate_files":null,"counts":null,"outputs_dir":null,"global_step":null,"max_steps":null}
- file: /root/llamarec/outputs/phase2a/multiseed96_ranking_robustness/seed44/n_k0_k20_seed42/test_metrics.json
  size: 502
  mtime: 2026-09-08 09:56:44.689697779 +0800
  sha256: a9804ce24b32fe99237c0a44549c982543db2ea931e05e73ba1feb38774dce69
  identity: {"model":"n_k0","dataset":"movielens-1m","seed":null,"splits":null,"adapter_dir":"/root/llamarec/outputs/n/movielens-1m/exposure_n_s12000_seed44/adapter","candidate_files":null,"counts":null,"outputs_dir":null,"global_step":null,"max_steps":null}

#### Prediction candidates

- file: /root/llamarec/outputs/phase2a/multiseed96_ranking_robustness/seed44/n_k0_k20_seed42/n_test_predictions.jsonl
  absolute_path: /root/llamarec/outputs/phase2a/multiseed96_ranking_robustness/seed44/n_k0_k20_seed42/n_test_predictions.jsonl
  size: 10901724
  mtime: 2026-09-08 09:56:44.637697933 +0800
  sha256: 8c52e0342d0fb50d222be1feef0055b2059c5642f8b03d8a41699acd310202e5
  rows: 5675
  schema: adapter_dir,candidate_generation,candidate_movie_ids,ground_truth_index,ground_truth_movie_id,inference_mode,label,label_probabilities,label_set,model,predicted_label,prompt_hash,scores,scoring_mode,split,task,user_id
  first_row_identity: {"model":"n_k0","task":"N","inference_mode":"candidate_label_probability","split":"test","user_id":"1","ground_truth_movie_id":"48","candidate_generation":{"method":"random","variant_name":"k20_seed42","candidate_num":20,"negative_num":19,"seed":244,"pool":"all_movies_minus_current_ground_truth_item","shuffle_order":true},"adapter_dir":"/root/llamarec/outputs/n/movielens-1m/exposure_n_s12000_seed44/adapter"}
- file: /root/llamarec/outputs/phase2a/multiseed96_ranking_robustness/seed44/n_k0_k20_seed42/n_valid_predictions.jsonl
  absolute_path: /root/llamarec/outputs/phase2a/multiseed96_ranking_robustness/seed44/n_k0_k20_seed42/n_valid_predictions.jsonl
  size: 10936372
  mtime: 2026-09-08 01:19:27.440833999 +0800
  sha256: 284a6683422f1adb3c6408cd87db4c8be8d1715ebb8c9fc25135271910e7fc81
  rows: 5675
  schema: adapter_dir,candidate_generation,candidate_movie_ids,ground_truth_index,ground_truth_movie_id,inference_mode,label,label_probabilities,label_set,model,predicted_label,prompt_hash,scores,scoring_mode,split,task,user_id
  first_row_identity: {"model":"n_k0","task":"N","inference_mode":"candidate_label_probability","split":"validation","user_id":"1","ground_truth_movie_id":"527","candidate_generation":{"method":"random","variant_name":"k20_seed42","candidate_num":20,"negative_num":19,"seed":143,"pool":"all_movies_minus_current_ground_truth_item","shuffle_order":true},"adapter_dir":"/root/llamarec/outputs/n/movielens-1m/exposure_n_s12000_seed44/adapter"}

### `/root/llamarec/outputs/phase2a/multiseed96_ranking_robustness/seed44/m1_k20_seed42`

- status: FOUND
- absolute_path: /root/llamarec/outputs/phase2a/multiseed96_ranking_robustness/seed44/m1_k20_seed42

#### Identity metadata

- file: /root/llamarec/outputs/phase2a/multiseed96_ranking_robustness/seed44/m1_k20_seed42/evaluation_summary.json
  size: 727
  mtime: 2026-09-08 10:25:17.256550058 +0800
  sha256: 37568d2cc110cdcd267f66194b2d0caec0f6bc92761441207dc040e609bd7a06
  identity: {"model":"m_k0","dataset":"movielens-1m","seed":null,"splits":["test"],"adapter_dir":"/root/llamarec/outputs/m/movielens-1m/exposure_m1_s24000_seed44/adapter","candidate_files":{"test":"/root/llamarec/data/candidates/movielens-1m/variants/k20_seed42/test.jsonl"},"counts":{"test":{"m_y_predictions":11544,"m_n_predictions":5675}},"outputs_dir":"/root/llamarec/outputs/phase2a/multiseed96_ranking_robustness/seed44/m1_k20_seed42","global_step":null,"max_steps":null}
- file: /root/llamarec/outputs/phase2a/multiseed96_ranking_robustness/seed44/m1_k20_seed42/evaluation_config_snapshot.yaml
  size: 8268
  mtime: 2026-09-08 09:56:54.821661660 +0800
  sha256: 444ea827915a8b1dbc99144c5ee7ce4dd8c0a2a8228b932bf5c380d8676d53d4
  identity: seed:;dataset:;model:;
- file: /root/llamarec/outputs/phase2a/multiseed96_ranking_robustness/seed44/m1_k20_seed42/valid_metrics.json
  size: 692
  mtime: 2026-09-08 01:49:15.141662030 +0800
  sha256: 891b2073653d8b9403a07aa78f5ee42d6eb3daf7a502e8488078ece64b2fc96f
  identity: {"model":"m_k0","dataset":"movielens-1m","seed":null,"splits":null,"adapter_dir":"/root/llamarec/outputs/m/movielens-1m/exposure_m1_s24000_seed44/adapter","candidate_files":null,"counts":null,"outputs_dir":null,"global_step":null,"max_steps":null}
- file: /root/llamarec/outputs/phase2a/multiseed96_ranking_robustness/seed44/m1_k20_seed42/test_metrics.json
  size: 685
  mtime: 2026-09-08 10:25:17.256550058 +0800
  sha256: b8ce6a878ad4421e120ad099e1e5f755ab59ef46660b91050ab64436bff84375
  identity: {"model":"m_k0","dataset":"movielens-1m","seed":null,"splits":null,"adapter_dir":"/root/llamarec/outputs/m/movielens-1m/exposure_m1_s24000_seed44/adapter","candidate_files":null,"counts":null,"outputs_dir":null,"global_step":null,"max_steps":null}

#### Prediction candidates

- file: /root/llamarec/outputs/phase2a/multiseed96_ranking_robustness/seed44/m1_k20_seed42/m_n_test_predictions.jsonl
  absolute_path: /root/llamarec/outputs/phase2a/multiseed96_ranking_robustness/seed44/m1_k20_seed42/m_n_test_predictions.jsonl
  size: 10962381
  mtime: 2026-09-08 10:25:17.192549438 +0800
  sha256: 555ed7c368746b46abbbc1eb27764e50e4a98896c0c865d061b146f831db4e5f
  rows: 5675
  schema: adapter_dir,candidate_generation,candidate_movie_ids,ground_truth_index,ground_truth_movie_id,inference_mode,label,label_probabilities,label_set,model,predicted_label,prompt_hash,scores,scoring_mode,split,task,user_id
  first_row_identity: {"model":"m_k0","task":"N","inference_mode":"m_next_item_candidate_probability","split":"test","user_id":"1","ground_truth_movie_id":"48","candidate_generation":{"method":"random","variant_name":"k20_seed42","candidate_num":20,"negative_num":19,"seed":244,"pool":"all_movies_minus_current_ground_truth_item","shuffle_order":true},"adapter_dir":"/root/llamarec/outputs/m/movielens-1m/exposure_m1_s24000_seed44/adapter"}
- file: /root/llamarec/outputs/phase2a/multiseed96_ranking_robustness/seed44/m1_k20_seed42/m_n_valid_predictions.jsonl
  absolute_path: /root/llamarec/outputs/phase2a/multiseed96_ranking_robustness/seed44/m1_k20_seed42/m_n_valid_predictions.jsonl
  size: 10996287
  mtime: 2026-09-08 01:49:15.077661826 +0800
  sha256: 00a2882489d37c2ca3aab433e32bf216e63a33aecc794ff47396135db5d2a97e
  rows: 5675
  schema: adapter_dir,candidate_generation,candidate_movie_ids,ground_truth_index,ground_truth_movie_id,inference_mode,label,label_probabilities,label_set,model,predicted_label,prompt_hash,scores,scoring_mode,split,task,user_id
  first_row_identity: {"model":"m_k0","task":"N","inference_mode":"m_next_item_candidate_probability","split":"validation","user_id":"1","ground_truth_movie_id":"527","candidate_generation":{"method":"random","variant_name":"k20_seed42","candidate_num":20,"negative_num":19,"seed":143,"pool":"all_movies_minus_current_ground_truth_item","shuffle_order":true},"adapter_dir":"/root/llamarec/outputs/m/movielens-1m/exposure_m1_s24000_seed44/adapter"}
- file: /root/llamarec/outputs/phase2a/multiseed96_ranking_robustness/seed44/m1_k20_seed42/m_y_test_predictions.jsonl
  absolute_path: /root/llamarec/outputs/phase2a/multiseed96_ranking_robustness/seed44/m1_k20_seed42/m_y_test_predictions.jsonl
  size: 4897200
  mtime: 2026-09-08 10:15:35.810545727 +0800
  sha256: 88ffd300c06d82cb85d35f87385a2d2d6d8bdc9ace0c87bea6be7ba583996166
  rows: 11544
  schema: adapter_dir,inference_mode,label,model,p_no,p_yes,predicted_label,prompt_hash,score,scoring_mode,split,target_movie_id,task,user_id
  first_row_identity: {"model":"m_k0","task":"Y","inference_mode":"m_yesno_p_yes","split":"test","user_id":"1","ground_truth_movie_id":null,"candidate_generation":null,"adapter_dir":"/root/llamarec/outputs/m/movielens-1m/exposure_m1_s24000_seed44/adapter"}
- file: /root/llamarec/outputs/phase2a/multiseed96_ranking_robustness/seed44/m1_k20_seed42/m_y_valid_predictions.jsonl
  absolute_path: /root/llamarec/outputs/phase2a/multiseed96_ranking_robustness/seed44/m1_k20_seed42/m_y_valid_predictions.jsonl
  size: 5325481
  mtime: 2026-09-08 01:39:33.723287904 +0800
  sha256: 2d3d3b3a56cb65f58fd360b35313d7ead64f029c4df748b927388438ba43e41a
  rows: 12381
  schema: adapter_dir,inference_mode,label,model,p_no,p_yes,predicted_label,prompt_hash,score,scoring_mode,split,target_movie_id,task,user_id
  first_row_identity: {"model":"m_k0","task":"Y","inference_mode":"m_yesno_p_yes","split":"validation","user_id":"1","ground_truth_movie_id":null,"candidate_generation":null,"adapter_dir":"/root/llamarec/outputs/m/movielens-1m/exposure_m1_s24000_seed44/adapter"}

### `/root/llamarec/outputs/phase2a/multiseed96_ranking_robustness/seed44/n_k0_k50_seed42`

- status: FOUND
- absolute_path: /root/llamarec/outputs/phase2a/multiseed96_ranking_robustness/seed44/n_k0_k50_seed42

#### Identity metadata

- file: /root/llamarec/outputs/phase2a/multiseed96_ranking_robustness/seed44/n_k0_k50_seed42/evaluation_summary.json
  size: 651
  mtime: 2026-09-08 10:39:25.299243820 +0800
  sha256: 70c54fda3ae2e7ed56a08d06acfcb34de8dfcd8248608412a91091a5dd05af99
  identity: {"model":"n_k0","dataset":"movielens-1m","seed":null,"splits":["test"],"adapter_dir":"/root/llamarec/outputs/n/movielens-1m/exposure_n_s12000_seed44/adapter","candidate_files":{"test":"/root/llamarec/data/candidates/movielens-1m/variants/k50_seed42/test.jsonl"},"counts":{"test":{"n_predictions":5675}},"outputs_dir":"/root/llamarec/outputs/phase2a/multiseed96_ranking_robustness/seed44/n_k0_k50_seed42","global_step":null,"max_steps":null}
- file: /root/llamarec/outputs/phase2a/multiseed96_ranking_robustness/seed44/n_k0_k50_seed42/evaluation_config_snapshot.yaml
  size: 8112
  mtime: 2026-09-08 10:25:27.460647720 +0800
  sha256: 7aebb51231b2e81ef49bba9aedbce15d41a3c0184b91b3c737f101e2068f108b
  identity: seed:;dataset:;model:;
- file: /root/llamarec/outputs/phase2a/multiseed96_ranking_robustness/seed44/n_k0_k50_seed42/valid_metrics.json
  size: 580
  mtime: 2026-09-08 02:03:21.464209572 +0800
  sha256: dfc364a5410a8abddb730cf213d6e0d2f05b4a4a14c00ed07a9726ec3d9967d8
  identity: {"model":"n_k0","dataset":"movielens-1m","seed":null,"splits":null,"adapter_dir":"/root/llamarec/outputs/n/movielens-1m/exposure_n_s12000_seed44/adapter","candidate_files":null,"counts":null,"outputs_dir":null,"global_step":null,"max_steps":null}
- file: /root/llamarec/outputs/phase2a/multiseed96_ranking_robustness/seed44/n_k0_k50_seed42/test_metrics.json
  size: 574
  mtime: 2026-09-08 10:39:25.299243820 +0800
  sha256: 90b85efe030deb250f04ae338240177a177691f1d73e0283969acee94808c778
  identity: {"model":"n_k0","dataset":"movielens-1m","seed":null,"splits":null,"adapter_dir":"/root/llamarec/outputs/n/movielens-1m/exposure_n_s12000_seed44/adapter","candidate_files":null,"counts":null,"outputs_dir":null,"global_step":null,"max_steps":null}

#### Prediction candidates

- file: /root/llamarec/outputs/phase2a/multiseed96_ranking_robustness/seed44/n_k0_k50_seed42/n_test_predictions.jsonl
  absolute_path: /root/llamarec/outputs/phase2a/multiseed96_ranking_robustness/seed44/n_k0_k50_seed42/n_test_predictions.jsonl
  size: 22153635
  mtime: 2026-09-08 10:39:25.207243876 +0800
  sha256: 77c540bf27bfc0dd3f00f259082321b354b105d05eef50e3b17664581568de26
  rows: 5675
  schema: adapter_dir,candidate_generation,candidate_movie_ids,ground_truth_index,ground_truth_movie_id,inference_mode,label,label_probabilities,label_set,model,predicted_label,prompt_hash,scores,scoring_mode,split,task,user_id
  first_row_identity: {"model":"n_k0","task":"N","inference_mode":"candidate_label_probability","split":"test","user_id":"1","ground_truth_movie_id":"48","candidate_generation":{"method":"random","variant_name":"k50_seed42","candidate_num":50,"negative_num":49,"seed":244,"pool":"all_movies_minus_current_ground_truth_item","shuffle_order":true},"adapter_dir":"/root/llamarec/outputs/n/movielens-1m/exposure_n_s12000_seed44/adapter"}
- file: /root/llamarec/outputs/phase2a/multiseed96_ranking_robustness/seed44/n_k0_k50_seed42/n_valid_predictions.jsonl
  absolute_path: /root/llamarec/outputs/phase2a/multiseed96_ranking_robustness/seed44/n_k0_k50_seed42/n_valid_predictions.jsonl
  size: 22189025
  mtime: 2026-09-08 02:03:21.372210175 +0800
  sha256: 1eb440114dd6640eb2d6287e1dd60c67a958eceeb643fedd3e0e1751ca0aa07a
  rows: 5675
  schema: adapter_dir,candidate_generation,candidate_movie_ids,ground_truth_index,ground_truth_movie_id,inference_mode,label,label_probabilities,label_set,model,predicted_label,prompt_hash,scores,scoring_mode,split,task,user_id
  first_row_identity: {"model":"n_k0","task":"N","inference_mode":"candidate_label_probability","split":"validation","user_id":"1","ground_truth_movie_id":"527","candidate_generation":{"method":"random","variant_name":"k50_seed42","candidate_num":50,"negative_num":49,"seed":143,"pool":"all_movies_minus_current_ground_truth_item","shuffle_order":true},"adapter_dir":"/root/llamarec/outputs/n/movielens-1m/exposure_n_s12000_seed44/adapter"}

### `/root/llamarec/outputs/phase2a/multiseed96_ranking_robustness/seed44/m1_k50_seed42`

- status: FOUND
- absolute_path: /root/llamarec/outputs/phase2a/multiseed96_ranking_robustness/seed44/m1_k50_seed42

#### Identity metadata

- file: /root/llamarec/outputs/phase2a/multiseed96_ranking_robustness/seed44/m1_k50_seed42/evaluation_summary.json
  size: 727
  mtime: 2026-09-08 11:12:20.541210745 +0800
  sha256: 79893f9959e3818c71b190e993d30e885ddef963b00d5bf6b4ece5b5c41a7d3d
  identity: {"model":"m_k0","dataset":"movielens-1m","seed":null,"splits":["test"],"adapter_dir":"/root/llamarec/outputs/m/movielens-1m/exposure_m1_s24000_seed44/adapter","candidate_files":{"test":"/root/llamarec/data/candidates/movielens-1m/variants/k50_seed42/test.jsonl"},"counts":{"test":{"m_y_predictions":11544,"m_n_predictions":5675}},"outputs_dir":"/root/llamarec/outputs/phase2a/multiseed96_ranking_robustness/seed44/m1_k50_seed42","global_step":null,"max_steps":null}
- file: /root/llamarec/outputs/phase2a/multiseed96_ranking_robustness/seed44/m1_k50_seed42/evaluation_config_snapshot.yaml
  size: 8268
  mtime: 2026-09-08 10:39:35.659237175 +0800
  sha256: 444ea827915a8b1dbc99144c5ee7ce4dd8c0a2a8228b932bf5c380d8676d53d4
  identity: seed:;dataset:;model:;
- file: /root/llamarec/outputs/phase2a/multiseed96_ranking_robustness/seed44/m1_k50_seed42/valid_metrics.json
  size: 763
  mtime: 2026-09-08 02:37:42.041341746 +0800
  sha256: 40d9f587ffffb7afeaf03b79ccf15d95003f839f046e8f4dabb098344a394182
  identity: {"model":"m_k0","dataset":"movielens-1m","seed":null,"splits":null,"adapter_dir":"/root/llamarec/outputs/m/movielens-1m/exposure_m1_s24000_seed44/adapter","candidate_files":null,"counts":null,"outputs_dir":null,"global_step":null,"max_steps":null}
- file: /root/llamarec/outputs/phase2a/multiseed96_ranking_robustness/seed44/m1_k50_seed42/test_metrics.json
  size: 756
  mtime: 2026-09-08 11:12:20.537211255 +0800
  sha256: b86daf12a7dc88e68934906af6433b803b25e30b8ea04c20b93c8c663f701327
  identity: {"model":"m_k0","dataset":"movielens-1m","seed":null,"splits":null,"adapter_dir":"/root/llamarec/outputs/m/movielens-1m/exposure_m1_s24000_seed44/adapter","candidate_files":null,"counts":null,"outputs_dir":null,"global_step":null,"max_steps":null}

#### Prediction candidates

- file: /root/llamarec/outputs/phase2a/multiseed96_ranking_robustness/seed44/m1_k50_seed42/m_n_test_predictions.jsonl
  absolute_path: /root/llamarec/outputs/phase2a/multiseed96_ranking_robustness/seed44/m1_k50_seed42/m_n_test_predictions.jsonl
  size: 22218036
  mtime: 2026-09-08 11:12:20.437223990 +0800
  sha256: 74ecea2df70581170302b3e7421ed4ddec657006f701a5132994205fe6186ddf
  rows: 5675
  schema: adapter_dir,candidate_generation,candidate_movie_ids,ground_truth_index,ground_truth_movie_id,inference_mode,label,label_probabilities,label_set,model,predicted_label,prompt_hash,scores,scoring_mode,split,task,user_id
  first_row_identity: {"model":"m_k0","task":"N","inference_mode":"m_next_item_candidate_probability","split":"test","user_id":"1","ground_truth_movie_id":"48","candidate_generation":{"method":"random","variant_name":"k50_seed42","candidate_num":50,"negative_num":49,"seed":244,"pool":"all_movies_minus_current_ground_truth_item","shuffle_order":true},"adapter_dir":"/root/llamarec/outputs/m/movielens-1m/exposure_m1_s24000_seed44/adapter"}
- file: /root/llamarec/outputs/phase2a/multiseed96_ranking_robustness/seed44/m1_k50_seed42/m_n_valid_predictions.jsonl
  absolute_path: /root/llamarec/outputs/phase2a/multiseed96_ranking_robustness/seed44/m1_k50_seed42/m_n_valid_predictions.jsonl
  size: 22251140
  mtime: 2026-09-08 02:37:41.937340694 +0800
  sha256: 186e1390d60ee9d49846bafc5ba834a19fe03ee2ad6f57f93cea69726a2c9a33
  rows: 5675
  schema: adapter_dir,candidate_generation,candidate_movie_ids,ground_truth_index,ground_truth_movie_id,inference_mode,label,label_probabilities,label_set,model,predicted_label,prompt_hash,scores,scoring_mode,split,task,user_id
  first_row_identity: {"model":"m_k0","task":"N","inference_mode":"m_next_item_candidate_probability","split":"validation","user_id":"1","ground_truth_movie_id":"527","candidate_generation":{"method":"random","variant_name":"k50_seed42","candidate_num":50,"negative_num":49,"seed":143,"pool":"all_movies_minus_current_ground_truth_item","shuffle_order":true},"adapter_dir":"/root/llamarec/outputs/m/movielens-1m/exposure_m1_s24000_seed44/adapter"}
- file: /root/llamarec/outputs/phase2a/multiseed96_ranking_robustness/seed44/m1_k50_seed42/m_y_test_predictions.jsonl
  absolute_path: /root/llamarec/outputs/phase2a/multiseed96_ranking_robustness/seed44/m1_k50_seed42/m_y_test_predictions.jsonl
  size: 4897200
  mtime: 2026-09-08 10:58:22.265317929 +0800
  sha256: 88ffd300c06d82cb85d35f87385a2d2d6d8bdc9ace0c87bea6be7ba583996166
  rows: 11544
  schema: adapter_dir,inference_mode,label,model,p_no,p_yes,predicted_label,prompt_hash,score,scoring_mode,split,target_movie_id,task,user_id
  first_row_identity: {"model":"m_k0","task":"Y","inference_mode":"m_yesno_p_yes","split":"test","user_id":"1","ground_truth_movie_id":null,"candidate_generation":null,"adapter_dir":"/root/llamarec/outputs/m/movielens-1m/exposure_m1_s24000_seed44/adapter"}
- file: /root/llamarec/outputs/phase2a/multiseed96_ranking_robustness/seed44/m1_k50_seed42/m_y_valid_predictions.jsonl
  absolute_path: /root/llamarec/outputs/phase2a/multiseed96_ranking_robustness/seed44/m1_k50_seed42/m_y_valid_predictions.jsonl
  size: 5325481
  mtime: 2026-09-08 02:23:46.269077669 +0800
  sha256: 2d3d3b3a56cb65f58fd360b35313d7ead64f029c4df748b927388438ba43e41a
  rows: 12381
  schema: adapter_dir,inference_mode,label,model,p_no,p_yes,predicted_label,prompt_hash,score,scoring_mode,split,target_movie_id,task,user_id
  first_row_identity: {"model":"m_k0","task":"Y","inference_mode":"m_yesno_p_yes","split":"validation","user_id":"1","ground_truth_movie_id":null,"candidate_generation":null,"adapter_dir":"/root/llamarec/outputs/m/movielens-1m/exposure_m1_s24000_seed44/adapter"}

