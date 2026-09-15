# Missing Prediction Report: Machine B

- generated_utc: 2026-09-11T08:51:52Z
- hostname: ubuntu22
- machine: B
- expected_seed: 43
- repository_root: /root/llamarec
- repository_head: a9c6cd959cf32afe046bb05be9eb5096bebfc5fb
- training_invoked: NO
- inference_invoked: NO

## Candidate directories

### `/root/llamarec/outputs/n/movielens-1m/exposure_n_s12000_seed43/popmatch_eval`

- status: FOUND
- absolute_path: /root/llamarec/outputs/n/movielens-1m/exposure_n_s12000_seed43/popmatch_eval

#### Identity metadata

- file: /root/llamarec/outputs/n/movielens-1m/exposure_n_s12000_seed43/popmatch_eval/evaluation_summary.json
  size: 651
  mtime: 2026-09-08 09:37:00.442175695 +0800
  sha256: ddd76109c942089eb1e9c91d34584e1f11e448a3cebdd1b0e41aa3874a8d02ce
  identity: {"model":"n_k0","dataset":"movielens-1m","seed":null,"splits":["test"],"adapter_dir":"/root/llamarec/outputs/n/movielens-1m/exposure_n_s12000_seed43/adapter","candidate_files":{"test":"/root/llamarec/data/candidates/movielens-1m/variants/k5_popmatch_seed42/test.jsonl"},"counts":{"test":{"n_predictions":5675}},"outputs_dir":"/root/llamarec/outputs/n/movielens-1m/exposure_n_s12000_seed43/popmatch_eval","global_step":null,"max_steps":null}
- file: /root/llamarec/outputs/n/movielens-1m/exposure_n_s12000_seed43/popmatch_eval/evaluation_config_snapshot.yaml
  size: 8112
  mtime: 2026-09-08 09:25:52.410737280 +0800
  sha256: 7aebb51231b2e81ef49bba9aedbce15d41a3c0184b91b3c737f101e2068f108b
  identity: seed:;dataset:;model:;
- file: /root/llamarec/outputs/n/movielens-1m/exposure_n_s12000_seed43/popmatch_eval/valid_metrics.json
  size: 371
  mtime: 2026-09-06 17:55:57.988193706 +0800
  sha256: a826ad1ac65f3c9a43c9cbd4ec19b8e6326ef0323d891826a29c6e3b5e2b1f54
  identity: {"model":"n_k0","dataset":"movielens-1m","seed":null,"splits":null,"adapter_dir":"/root/llamarec/outputs/n/movielens-1m/exposure_n_s12000_seed43/adapter","candidate_files":null,"counts":null,"outputs_dir":null,"global_step":null,"max_steps":null}
- file: /root/llamarec/outputs/n/movielens-1m/exposure_n_s12000_seed43/popmatch_eval/test_metrics.json
  size: 365
  mtime: 2026-09-08 09:37:00.442175695 +0800
  sha256: 32ce581eb11697deb56227cf35bb05161d95f7d0884eb32bd727b2d1a3391c54
  identity: {"model":"n_k0","dataset":"movielens-1m","seed":null,"splits":null,"adapter_dir":"/root/llamarec/outputs/n/movielens-1m/exposure_n_s12000_seed43/adapter","candidate_files":null,"counts":null,"outputs_dir":null,"global_step":null,"max_steps":null}
- file: /root/llamarec/outputs/n/movielens-1m/exposure_n_s12000_seed43/run_summary.json
  size: 348
  mtime: 2026-09-06 09:40:22.828653406 +0800
  sha256: d38266c34dc180e7f8b7fb144cb1694cc835b91d643d5ad743d74ae8b716a039
  identity: {"model":"n_k0","dataset":"movielens-1m","seed":43,"splits":null,"adapter_dir":null,"candidate_files":null,"counts":null,"outputs_dir":null,"global_step":null,"max_steps":null}
- file: /root/llamarec/outputs/n/movielens-1m/exposure_n_s12000_seed43/config_snapshot.yaml
  size: 8112
  mtime: 2026-09-06 09:40:22.828653406 +0800
  sha256: 7aebb51231b2e81ef49bba9aedbce15d41a3c0184b91b3c737f101e2068f108b
  identity: seed:;dataset:;model:;
- file: /root/llamarec/outputs/n/movielens-1m/exposure_n_s12000_seed43/metrics.json
  size: 676
  mtime: 2026-09-06 17:50:14.925642220 +0800
  sha256: a417f7ecaca90a484da19b48129e69b4647434a5e07b7381994b2099579739c0
  identity: {"model":"n_k0","dataset":"movielens-1m","seed":43,"splits":null,"adapter_dir":null,"candidate_files":null,"counts":null,"outputs_dir":null,"global_step":null,"max_steps":null}

#### Prediction candidates

- file: /root/llamarec/outputs/n/movielens-1m/exposure_n_s12000_seed43/popmatch_eval/n_test_predictions.jsonl
  absolute_path: /root/llamarec/outputs/n/movielens-1m/exposure_n_s12000_seed43/popmatch_eval/n_test_predictions.jsonl
  size: 6286827
  mtime: 2026-09-08 09:37:00.418178094 +0800
  sha256: ed3048e8f3bcbbd4344e9129bd46d1fe7bd4f0cd05d6b458e67cca88290985cb
  rows: 5675
  schema: adapter_dir,candidate_generation,candidate_movie_ids,ground_truth_index,ground_truth_movie_id,inference_mode,label,label_probabilities,label_set,model,predicted_label,prompt_hash,scores,scoring_mode,split,task,user_id
  first_row_identity: {"model":"n_k0","task":"N","inference_mode":"candidate_label_probability","split":"test","user_id":"1","ground_truth_movie_id":"48","candidate_generation":{"method":"popularity_matched","variant_name":"k5_popmatch_seed42","candidate_num":5,"negative_num":4,"seed":244,"pool":"all_movies_minus_current_ground_truth_item","shuffle_order":true,"target_popularity":382,"negative_popularity_mean":387.5,"negative_popularity_min":386,"negative_popularity_max":389},"adapter_dir":"/root/llamarec/outputs/n/movielens-1m/exposure_n_s12000_seed43/adapter"}
- file: /root/llamarec/outputs/n/movielens-1m/exposure_n_s12000_seed43/popmatch_eval/n_valid_predictions.jsonl
  absolute_path: /root/llamarec/outputs/n/movielens-1m/exposure_n_s12000_seed43/popmatch_eval/n_valid_predictions.jsonl
  size: 6320863
  mtime: 2026-09-06 17:55:57.968193777 +0800
  sha256: e3ab2e20e090a249cef1a752694dff80509c3eb86215ba87bb9b685c6d329c0c
  rows: 5675
  schema: adapter_dir,candidate_generation,candidate_movie_ids,ground_truth_index,ground_truth_movie_id,inference_mode,label,label_probabilities,label_set,model,predicted_label,prompt_hash,scores,scoring_mode,split,task,user_id
  first_row_identity: {"model":"n_k0","task":"N","inference_mode":"candidate_label_probability","split":"validation","user_id":"1","ground_truth_movie_id":"527","candidate_generation":{"method":"popularity_matched","variant_name":"k5_popmatch_seed42","candidate_num":5,"negative_num":4,"seed":143,"pool":"all_movies_minus_current_ground_truth_item","shuffle_order":true,"target_popularity":2304,"negative_popularity_mean":2208.75,"negative_popularity_min":2098,"negative_popularity_max":2288},"adapter_dir":"/root/llamarec/outputs/n/movielens-1m/exposure_n_s12000_seed43/adapter"}

### `/root/llamarec/outputs/m/movielens-1m/exposure_m1_s24000_seed43/popmatch_eval`

- status: FOUND
- absolute_path: /root/llamarec/outputs/m/movielens-1m/exposure_m1_s24000_seed43/popmatch_eval

#### Identity metadata

- file: /root/llamarec/outputs/m/movielens-1m/exposure_m1_s24000_seed43/popmatch_eval/evaluation_summary.json
  size: 730
  mtime: 2026-09-08 10:10:50.201565393 +0800
  sha256: 9e7656184ebb4fe299e71d306d3a8e867f5e18f77176ac8b84b820f65e9e718a
  identity: {"model":"m_k0","dataset":"movielens-1m","seed":null,"splits":["test"],"adapter_dir":"/root/llamarec/outputs/m/movielens-1m/exposure_m1_s24000_seed43/adapter","candidate_files":{"test":"/root/llamarec/data/candidates/movielens-1m/variants/k5_popmatch_seed42/test.jsonl"},"counts":{"test":{"m_y_predictions":11544,"m_n_predictions":5675}},"outputs_dir":"/root/llamarec/outputs/m/movielens-1m/exposure_m1_s24000_seed43/popmatch_eval","global_step":null,"max_steps":null}
- file: /root/llamarec/outputs/m/movielens-1m/exposure_m1_s24000_seed43/popmatch_eval/evaluation_config_snapshot.yaml
  size: 8268
  mtime: 2026-09-08 09:37:14.612584670 +0800
  sha256: 444ea827915a8b1dbc99144c5ee7ce4dd8c0a2a8228b932bf5c380d8676d53d4
  identity: seed:;dataset:;model:;
- file: /root/llamarec/outputs/m/movielens-1m/exposure_m1_s24000_seed43/popmatch_eval/valid_metrics.json
  size: 551
  mtime: 2026-09-07 10:54:13.846284808 +0800
  sha256: a9bf461087b834db500d52dfeddbd8a9427edb86f4700db8f31234ae596374f9
  identity: {"model":"m_k0","dataset":"movielens-1m","seed":null,"splits":null,"adapter_dir":"/root/llamarec/outputs/m/movielens-1m/exposure_m1_s24000_seed43/adapter","candidate_files":null,"counts":null,"outputs_dir":null,"global_step":null,"max_steps":null}
- file: /root/llamarec/outputs/m/movielens-1m/exposure_m1_s24000_seed43/popmatch_eval/test_metrics.json
  size: 547
  mtime: 2026-09-08 10:10:50.197565613 +0800
  sha256: 979118051c7c9f1bc1d5a67f28c4b39be40322e9d4c825b9a81301d7f6e8658e
  identity: {"model":"m_k0","dataset":"movielens-1m","seed":null,"splits":null,"adapter_dir":"/root/llamarec/outputs/m/movielens-1m/exposure_m1_s24000_seed43/adapter","candidate_files":null,"counts":null,"outputs_dir":null,"global_step":null,"max_steps":null}
- file: /root/llamarec/outputs/m/movielens-1m/exposure_m1_s24000_seed43/run_summary.json
  size: 886
  mtime: 2026-09-06 17:56:15.308131376 +0800
  sha256: b99a40a43593bdaf7704f611f6c281d70bf3031c4581f6f6b955e4c98f1c039b
  identity: {"model":"m_k0","dataset":"movielens-1m","seed":43,"splits":null,"adapter_dir":null,"candidate_files":null,"counts":null,"outputs_dir":null,"global_step":null,"max_steps":null}
- file: /root/llamarec/outputs/m/movielens-1m/exposure_m1_s24000_seed43/config_snapshot.yaml
  size: 8268
  mtime: 2026-09-06 17:56:15.308131376 +0800
  sha256: 444ea827915a8b1dbc99144c5ee7ce4dd8c0a2a8228b932bf5c380d8676d53d4
  identity: seed:;dataset:;model:;
- file: /root/llamarec/outputs/m/movielens-1m/exposure_m1_s24000_seed43/metrics.json
  size: 853
  mtime: 2026-09-07 10:35:44.531260236 +0800
  sha256: c5d0043319d92ec264cc0ba652f66fe8b65dfdba5b139f8cc20feb76bf4250ef
  identity: {"model":"m_k0","dataset":"movielens-1m","seed":43,"splits":null,"adapter_dir":null,"candidate_files":null,"counts":null,"outputs_dir":null,"global_step":null,"max_steps":null}

#### Prediction candidates

- file: /root/llamarec/outputs/m/movielens-1m/exposure_m1_s24000_seed43/popmatch_eval/m_n_test_predictions.jsonl
  absolute_path: /root/llamarec/outputs/m/movielens-1m/exposure_m1_s24000_seed43/popmatch_eval/m_n_test_predictions.jsonl
  size: 6328178
  mtime: 2026-09-08 10:10:50.161567586 +0800
  sha256: 63b04b7d92b40ae10aa6834f2762b9189475e91a5220e356a8ebef61ce8948bb
  rows: 5675
  schema: adapter_dir,candidate_generation,candidate_movie_ids,ground_truth_index,ground_truth_movie_id,inference_mode,label,label_probabilities,label_set,model,predicted_label,prompt_hash,scores,scoring_mode,split,task,user_id
  first_row_identity: {"model":"m_k0","task":"N","inference_mode":"m_next_item_candidate_probability","split":"test","user_id":"1","ground_truth_movie_id":"48","candidate_generation":{"method":"popularity_matched","variant_name":"k5_popmatch_seed42","candidate_num":5,"negative_num":4,"seed":244,"pool":"all_movies_minus_current_ground_truth_item","shuffle_order":true,"target_popularity":382,"negative_popularity_mean":387.5,"negative_popularity_min":386,"negative_popularity_max":389},"adapter_dir":"/root/llamarec/outputs/m/movielens-1m/exposure_m1_s24000_seed43/adapter"}
- file: /root/llamarec/outputs/m/movielens-1m/exposure_m1_s24000_seed43/popmatch_eval/m_n_valid_predictions.jsonl
  absolute_path: /root/llamarec/outputs/m/movielens-1m/exposure_m1_s24000_seed43/popmatch_eval/m_n_valid_predictions.jsonl
  size: 6362850
  mtime: 2026-09-07 10:54:13.810284728 +0800
  sha256: 5c4993c79cae1ada54f025d284212b006a8323bb4e0d27bd1609c7ce6d91f4f1
  rows: 5675
  schema: adapter_dir,candidate_generation,candidate_movie_ids,ground_truth_index,ground_truth_movie_id,inference_mode,label,label_probabilities,label_set,model,predicted_label,prompt_hash,scores,scoring_mode,split,task,user_id
  first_row_identity: {"model":"m_k0","task":"N","inference_mode":"m_next_item_candidate_probability","split":"validation","user_id":"1","ground_truth_movie_id":"527","candidate_generation":{"method":"popularity_matched","variant_name":"k5_popmatch_seed42","candidate_num":5,"negative_num":4,"seed":143,"pool":"all_movies_minus_current_ground_truth_item","shuffle_order":true,"target_popularity":2304,"negative_popularity_mean":2208.75,"negative_popularity_min":2098,"negative_popularity_max":2288},"adapter_dir":"/root/llamarec/outputs/m/movielens-1m/exposure_m1_s24000_seed43/adapter"}
- file: /root/llamarec/outputs/m/movielens-1m/exposure_m1_s24000_seed43/popmatch_eval/m_y_test_predictions.jsonl
  absolute_path: /root/llamarec/outputs/m/movielens-1m/exposure_m1_s24000_seed43/popmatch_eval/m_y_test_predictions.jsonl
  size: 4898513
  mtime: 2026-09-08 09:59:44.720483424 +0800
  sha256: dfa11e9567dc69aeba88fb683a6cc7c5031b15b1c2ffbf98fff39235f690c509
  rows: 11544
  schema: adapter_dir,inference_mode,label,model,p_no,p_yes,predicted_label,prompt_hash,score,scoring_mode,split,target_movie_id,task,user_id
  first_row_identity: {"model":"m_k0","task":"Y","inference_mode":"m_yesno_p_yes","split":"test","user_id":"1","ground_truth_movie_id":null,"candidate_generation":null,"adapter_dir":"/root/llamarec/outputs/m/movielens-1m/exposure_m1_s24000_seed43/adapter"}
- file: /root/llamarec/outputs/m/movielens-1m/exposure_m1_s24000_seed43/popmatch_eval/m_y_valid_predictions.jsonl
  absolute_path: /root/llamarec/outputs/m/movielens-1m/exposure_m1_s24000_seed43/popmatch_eval/m_y_valid_predictions.jsonl
  size: 5326821
  mtime: 2026-09-07 10:48:33.013501130 +0800
  sha256: a2efe967c214a7fcb326d257297830456279a09b925af2cecb6bd886664aba66
  rows: 12381
  schema: adapter_dir,inference_mode,label,model,p_no,p_yes,predicted_label,prompt_hash,score,scoring_mode,split,target_movie_id,task,user_id
  first_row_identity: {"model":"m_k0","task":"Y","inference_mode":"m_yesno_p_yes","split":"validation","user_id":"1","ground_truth_movie_id":null,"candidate_generation":null,"adapter_dir":"/root/llamarec/outputs/m/movielens-1m/exposure_m1_s24000_seed43/adapter"}

### `/root/llamarec/outputs/phase2a/multiseed96_ranking_robustness/seed43/n_k0_k20_seed42`

- status: FOUND
- absolute_path: /root/llamarec/outputs/phase2a/multiseed96_ranking_robustness/seed43/n_k0_k20_seed42

#### Identity metadata

- file: /root/llamarec/outputs/phase2a/multiseed96_ranking_robustness/seed43/n_k0_k20_seed42/evaluation_summary.json
  size: 651
  mtime: 2026-09-08 10:22:52.480052791 +0800
  sha256: f94230c1b6fa4284c7a502df8e16e418f4976c400cfea63b6f20cd4e3e9fb019
  identity: {"model":"n_k0","dataset":"movielens-1m","seed":null,"splits":["test"],"adapter_dir":"/root/llamarec/outputs/n/movielens-1m/exposure_n_s12000_seed43/adapter","candidate_files":{"test":"/root/llamarec/data/candidates/movielens-1m/variants/k20_seed42/test.jsonl"},"counts":{"test":{"n_predictions":5675}},"outputs_dir":"/root/llamarec/outputs/phase2a/multiseed96_ranking_robustness/seed43/n_k0_k20_seed42","global_step":null,"max_steps":null}
- file: /root/llamarec/outputs/phase2a/multiseed96_ranking_robustness/seed43/n_k0_k20_seed42/evaluation_config_snapshot.yaml
  size: 8112
  mtime: 2026-09-08 10:11:03.704823990 +0800
  sha256: 7aebb51231b2e81ef49bba9aedbce15d41a3c0184b91b3c737f101e2068f108b
  identity: seed:;dataset:;model:;
- file: /root/llamarec/outputs/phase2a/multiseed96_ranking_robustness/seed43/n_k0_k20_seed42/valid_metrics.json
  size: 509
  mtime: 2026-09-07 11:04:03.223543075 +0800
  sha256: b881508841da5ece6df67eace2d479d49adef4ef737d73aea9fb3299012b14c2
  identity: {"model":"n_k0","dataset":"movielens-1m","seed":null,"splits":null,"adapter_dir":"/root/llamarec/outputs/n/movielens-1m/exposure_n_s12000_seed43/adapter","candidate_files":null,"counts":null,"outputs_dir":null,"global_step":null,"max_steps":null}
- file: /root/llamarec/outputs/phase2a/multiseed96_ranking_robustness/seed43/n_k0_k20_seed42/test_metrics.json
  size: 504
  mtime: 2026-09-08 10:22:52.480052791 +0800
  sha256: 8781827be94f09a2fa4809346b053412a4c7174942843696d513ec64c8bfbb85
  identity: {"model":"n_k0","dataset":"movielens-1m","seed":null,"splits":null,"adapter_dir":"/root/llamarec/outputs/n/movielens-1m/exposure_n_s12000_seed43/adapter","candidate_files":null,"counts":null,"outputs_dir":null,"global_step":null,"max_steps":null}

#### Prediction candidates

- file: /root/llamarec/outputs/phase2a/multiseed96_ranking_robustness/seed43/n_k0_k20_seed42/n_test_predictions.jsonl
  absolute_path: /root/llamarec/outputs/phase2a/multiseed96_ranking_robustness/seed43/n_k0_k20_seed42/n_test_predictions.jsonl
  size: 10891490
  mtime: 2026-09-08 10:22:52.428048891 +0800
  sha256: 1942b3e42c9a2fe0ca03e8a4668e0ac9cfc10a1abb779305b9b9054d27bb13a4
  rows: 5675
  schema: adapter_dir,candidate_generation,candidate_movie_ids,ground_truth_index,ground_truth_movie_id,inference_mode,label,label_probabilities,label_set,model,predicted_label,prompt_hash,scores,scoring_mode,split,task,user_id
  first_row_identity: {"model":"n_k0","task":"N","inference_mode":"candidate_label_probability","split":"test","user_id":"1","ground_truth_movie_id":"48","candidate_generation":{"method":"random","variant_name":"k20_seed42","candidate_num":20,"negative_num":19,"seed":244,"pool":"all_movies_minus_current_ground_truth_item","shuffle_order":true},"adapter_dir":"/root/llamarec/outputs/n/movielens-1m/exposure_n_s12000_seed43/adapter"}
- file: /root/llamarec/outputs/phase2a/multiseed96_ranking_robustness/seed43/n_k0_k20_seed42/n_valid_predictions.jsonl
  absolute_path: /root/llamarec/outputs/phase2a/multiseed96_ranking_robustness/seed43/n_k0_k20_seed42/n_valid_predictions.jsonl
  size: 10925118
  mtime: 2026-09-07 11:04:03.183542991 +0800
  sha256: 3ba573d36ab786f5258803738ce89440b8fa343ceef804a829016ed53cd3042e
  rows: 5675
  schema: adapter_dir,candidate_generation,candidate_movie_ids,ground_truth_index,ground_truth_movie_id,inference_mode,label,label_probabilities,label_set,model,predicted_label,prompt_hash,scores,scoring_mode,split,task,user_id
  first_row_identity: {"model":"n_k0","task":"N","inference_mode":"candidate_label_probability","split":"validation","user_id":"1","ground_truth_movie_id":"527","candidate_generation":{"method":"random","variant_name":"k20_seed42","candidate_num":20,"negative_num":19,"seed":143,"pool":"all_movies_minus_current_ground_truth_item","shuffle_order":true},"adapter_dir":"/root/llamarec/outputs/n/movielens-1m/exposure_n_s12000_seed43/adapter"}

### `/root/llamarec/outputs/phase2a/multiseed96_ranking_robustness/seed43/m1_k20_seed42`

- status: FOUND
- absolute_path: /root/llamarec/outputs/phase2a/multiseed96_ranking_robustness/seed43/m1_k20_seed42

#### Identity metadata

- file: /root/llamarec/outputs/phase2a/multiseed96_ranking_robustness/seed43/m1_k20_seed42/evaluation_summary.json
  size: 727
  mtime: 2026-09-08 10:56:42.757313971 +0800
  sha256: 81ff0bffee25d87a2231a1d8ac51ed2ea77b1796aa1882ca3f751084ce107574
  identity: {"model":"m_k0","dataset":"movielens-1m","seed":null,"splits":["test"],"adapter_dir":"/root/llamarec/outputs/m/movielens-1m/exposure_m1_s24000_seed43/adapter","candidate_files":{"test":"/root/llamarec/data/candidates/movielens-1m/variants/k20_seed42/test.jsonl"},"counts":{"test":{"m_y_predictions":11544,"m_n_predictions":5675}},"outputs_dir":"/root/llamarec/outputs/phase2a/multiseed96_ranking_robustness/seed43/m1_k20_seed42","global_step":null,"max_steps":null}
- file: /root/llamarec/outputs/phase2a/multiseed96_ranking_robustness/seed43/m1_k20_seed42/evaluation_config_snapshot.yaml
  size: 8268
  mtime: 2026-09-08 10:23:05.865016311 +0800
  sha256: 444ea827915a8b1dbc99144c5ee7ce4dd8c0a2a8228b932bf5c380d8676d53d4
  identity: seed:;dataset:;model:;
- file: /root/llamarec/outputs/phase2a/multiseed96_ranking_robustness/seed43/m1_k20_seed42/valid_metrics.json
  size: 689
  mtime: 2026-09-07 11:26:23.560715543 +0800
  sha256: 97dbbb57fda1f1ca87b9092ae76129ed7ad78611517fbaa3492d16f35590f4a7
  identity: {"model":"m_k0","dataset":"movielens-1m","seed":null,"splits":null,"adapter_dir":"/root/llamarec/outputs/m/movielens-1m/exposure_m1_s24000_seed43/adapter","candidate_files":null,"counts":null,"outputs_dir":null,"global_step":null,"max_steps":null}
- file: /root/llamarec/outputs/phase2a/multiseed96_ranking_robustness/seed43/m1_k20_seed42/test_metrics.json
  size: 685
  mtime: 2026-09-08 10:56:42.757313971 +0800
  sha256: 27db2eb1b31647cce9d05b3711430b8539806f0613213a8de81459843c43c2e5
  identity: {"model":"m_k0","dataset":"movielens-1m","seed":null,"splits":null,"adapter_dir":"/root/llamarec/outputs/m/movielens-1m/exposure_m1_s24000_seed43/adapter","candidate_files":null,"counts":null,"outputs_dir":null,"global_step":null,"max_steps":null}

#### Prediction candidates

- file: /root/llamarec/outputs/phase2a/multiseed96_ranking_robustness/seed43/m1_k20_seed42/m_n_test_predictions.jsonl
  absolute_path: /root/llamarec/outputs/phase2a/multiseed96_ranking_robustness/seed43/m1_k20_seed42/m_n_test_predictions.jsonl
  size: 10962857
  mtime: 2026-09-08 10:56:42.685313587 +0800
  sha256: 1bb31f854db9d5d11f6101e5f3b5a4d6c71e3c8dbc83374ed1a4622452f7cae1
  rows: 5675
  schema: adapter_dir,candidate_generation,candidate_movie_ids,ground_truth_index,ground_truth_movie_id,inference_mode,label,label_probabilities,label_set,model,predicted_label,prompt_hash,scores,scoring_mode,split,task,user_id
  first_row_identity: {"model":"m_k0","task":"N","inference_mode":"m_next_item_candidate_probability","split":"test","user_id":"1","ground_truth_movie_id":"48","candidate_generation":{"method":"random","variant_name":"k20_seed42","candidate_num":20,"negative_num":19,"seed":244,"pool":"all_movies_minus_current_ground_truth_item","shuffle_order":true},"adapter_dir":"/root/llamarec/outputs/m/movielens-1m/exposure_m1_s24000_seed43/adapter"}
- file: /root/llamarec/outputs/phase2a/multiseed96_ranking_robustness/seed43/m1_k20_seed42/m_n_valid_predictions.jsonl
  absolute_path: /root/llamarec/outputs/phase2a/multiseed96_ranking_robustness/seed43/m1_k20_seed42/m_n_valid_predictions.jsonl
  size: 10996727
  mtime: 2026-09-07 11:26:23.496717988 +0800
  sha256: cd848bc1e81b30a37642c8f272bc18d303a195048ac807ae52ad6330eae7aca1
  rows: 5675
  schema: adapter_dir,candidate_generation,candidate_movie_ids,ground_truth_index,ground_truth_movie_id,inference_mode,label,label_probabilities,label_set,model,predicted_label,prompt_hash,scores,scoring_mode,split,task,user_id
  first_row_identity: {"model":"m_k0","task":"N","inference_mode":"m_next_item_candidate_probability","split":"validation","user_id":"1","ground_truth_movie_id":"527","candidate_generation":{"method":"random","variant_name":"k20_seed42","candidate_num":20,"negative_num":19,"seed":143,"pool":"all_movies_minus_current_ground_truth_item","shuffle_order":true},"adapter_dir":"/root/llamarec/outputs/m/movielens-1m/exposure_m1_s24000_seed43/adapter"}
- file: /root/llamarec/outputs/phase2a/multiseed96_ranking_robustness/seed43/m1_k20_seed42/m_y_test_predictions.jsonl
  absolute_path: /root/llamarec/outputs/phase2a/multiseed96_ranking_robustness/seed43/m1_k20_seed42/m_y_test_predictions.jsonl
  size: 4898513
  mtime: 2026-09-08 10:45:13.646952938 +0800
  sha256: dfa11e9567dc69aeba88fb683a6cc7c5031b15b1c2ffbf98fff39235f690c509
  rows: 11544
  schema: adapter_dir,inference_mode,label,model,p_no,p_yes,predicted_label,prompt_hash,score,scoring_mode,split,target_movie_id,task,user_id
  first_row_identity: {"model":"m_k0","task":"Y","inference_mode":"m_yesno_p_yes","split":"test","user_id":"1","ground_truth_movie_id":null,"candidate_generation":null,"adapter_dir":"/root/llamarec/outputs/m/movielens-1m/exposure_m1_s24000_seed43/adapter"}
- file: /root/llamarec/outputs/phase2a/multiseed96_ranking_robustness/seed43/m1_k20_seed42/m_y_valid_predictions.jsonl
  absolute_path: /root/llamarec/outputs/phase2a/multiseed96_ranking_robustness/seed43/m1_k20_seed42/m_y_valid_predictions.jsonl
  size: 5326821
  mtime: 2026-09-07 11:16:45.669105789 +0800
  sha256: a2efe967c214a7fcb326d257297830456279a09b925af2cecb6bd886664aba66
  rows: 12381
  schema: adapter_dir,inference_mode,label,model,p_no,p_yes,predicted_label,prompt_hash,score,scoring_mode,split,target_movie_id,task,user_id
  first_row_identity: {"model":"m_k0","task":"Y","inference_mode":"m_yesno_p_yes","split":"validation","user_id":"1","ground_truth_movie_id":null,"candidate_generation":null,"adapter_dir":"/root/llamarec/outputs/m/movielens-1m/exposure_m1_s24000_seed43/adapter"}

### `/root/llamarec/outputs/phase2a/multiseed96_ranking_robustness/seed43/n_k0_k50_seed42`

- status: FOUND
- absolute_path: /root/llamarec/outputs/phase2a/multiseed96_ranking_robustness/seed43/n_k0_k50_seed42

#### Identity metadata

- file: /root/llamarec/outputs/phase2a/multiseed96_ranking_robustness/seed43/n_k0_k50_seed42/evaluation_summary.json
  size: 651
  mtime: 2026-09-08 11:11:07.629015859 +0800
  sha256: 3d6cbd9b75fe0cf4d7f87fbd673d92bbffd852ae421db066460e5be9149f978d
  identity: {"model":"n_k0","dataset":"movielens-1m","seed":null,"splits":["test"],"adapter_dir":"/root/llamarec/outputs/n/movielens-1m/exposure_n_s12000_seed43/adapter","candidate_files":{"test":"/root/llamarec/data/candidates/movielens-1m/variants/k50_seed42/test.jsonl"},"counts":{"test":{"n_predictions":5675}},"outputs_dir":"/root/llamarec/outputs/phase2a/multiseed96_ranking_robustness/seed43/n_k0_k50_seed42","global_step":null,"max_steps":null}
- file: /root/llamarec/outputs/phase2a/multiseed96_ranking_robustness/seed43/n_k0_k50_seed42/evaluation_config_snapshot.yaml
  size: 8112
  mtime: 2026-09-08 10:56:56.753389792 +0800
  sha256: 7aebb51231b2e81ef49bba9aedbce15d41a3c0184b91b3c737f101e2068f108b
  identity: seed:;dataset:;model:;
- file: /root/llamarec/outputs/phase2a/multiseed96_ranking_robustness/seed43/n_k0_k50_seed42/valid_metrics.json
  size: 580
  mtime: 2026-09-07 11:40:38.219193225 +0800
  sha256: 386344dc803b6dfa5dbaaaa476b4d2d17bf8f28e763e53f600bd3f972b4e961c
  identity: {"model":"n_k0","dataset":"movielens-1m","seed":null,"splits":null,"adapter_dir":"/root/llamarec/outputs/n/movielens-1m/exposure_n_s12000_seed43/adapter","candidate_files":null,"counts":null,"outputs_dir":null,"global_step":null,"max_steps":null}
- file: /root/llamarec/outputs/phase2a/multiseed96_ranking_robustness/seed43/n_k0_k50_seed42/test_metrics.json
  size: 577
  mtime: 2026-09-08 11:11:07.629015859 +0800
  sha256: 6445cf2c52526fc47bfc02e75488e54551542446d3a5001722c8ceaaeba7c48c
  identity: {"model":"n_k0","dataset":"movielens-1m","seed":null,"splits":null,"adapter_dir":"/root/llamarec/outputs/n/movielens-1m/exposure_n_s12000_seed43/adapter","candidate_files":null,"counts":null,"outputs_dir":null,"global_step":null,"max_steps":null}

#### Prediction candidates

- file: /root/llamarec/outputs/phase2a/multiseed96_ranking_robustness/seed43/n_k0_k50_seed42/n_test_predictions.jsonl
  absolute_path: /root/llamarec/outputs/phase2a/multiseed96_ranking_robustness/seed43/n_k0_k50_seed42/n_test_predictions.jsonl
  size: 22142807
  mtime: 2026-09-08 11:11:07.509014544 +0800
  sha256: c09a276d6f0c348020e06588da4dd33b7b0cf0c9536ddfa70da8026988ef1df9
  rows: 5675
  schema: adapter_dir,candidate_generation,candidate_movie_ids,ground_truth_index,ground_truth_movie_id,inference_mode,label,label_probabilities,label_set,model,predicted_label,prompt_hash,scores,scoring_mode,split,task,user_id
  first_row_identity: {"model":"n_k0","task":"N","inference_mode":"candidate_label_probability","split":"test","user_id":"1","ground_truth_movie_id":"48","candidate_generation":{"method":"random","variant_name":"k50_seed42","candidate_num":50,"negative_num":49,"seed":244,"pool":"all_movies_minus_current_ground_truth_item","shuffle_order":true},"adapter_dir":"/root/llamarec/outputs/n/movielens-1m/exposure_n_s12000_seed43/adapter"}
- file: /root/llamarec/outputs/phase2a/multiseed96_ranking_robustness/seed43/n_k0_k50_seed42/n_valid_predictions.jsonl
  absolute_path: /root/llamarec/outputs/phase2a/multiseed96_ranking_robustness/seed43/n_k0_k50_seed42/n_valid_predictions.jsonl
  size: 22173869
  mtime: 2026-09-07 11:40:38.143194005 +0800
  sha256: b74adbda18bdd7e2c25b8d34a1c2a463dd5e8b4ceb76e550ce88b4a151016463
  rows: 5675
  schema: adapter_dir,candidate_generation,candidate_movie_ids,ground_truth_index,ground_truth_movie_id,inference_mode,label,label_probabilities,label_set,model,predicted_label,prompt_hash,scores,scoring_mode,split,task,user_id
  first_row_identity: {"model":"n_k0","task":"N","inference_mode":"candidate_label_probability","split":"validation","user_id":"1","ground_truth_movie_id":"527","candidate_generation":{"method":"random","variant_name":"k50_seed42","candidate_num":50,"negative_num":49,"seed":143,"pool":"all_movies_minus_current_ground_truth_item","shuffle_order":true},"adapter_dir":"/root/llamarec/outputs/n/movielens-1m/exposure_n_s12000_seed43/adapter"}

### `/root/llamarec/outputs/phase2a/multiseed96_ranking_robustness/seed43/m1_k50_seed42`

- status: FOUND
- absolute_path: /root/llamarec/outputs/phase2a/multiseed96_ranking_robustness/seed43/m1_k50_seed42

#### Identity metadata

- file: /root/llamarec/outputs/phase2a/multiseed96_ranking_robustness/seed43/m1_k50_seed42/evaluation_summary.json
  size: 727
  mtime: 2026-09-08 11:48:06.411262623 +0800
  sha256: cdd2987178dbaedd82d5ade52d25028ff14d9f563d36a41d3b6f1b419082a904
  identity: {"model":"m_k0","dataset":"movielens-1m","seed":null,"splits":["test"],"adapter_dir":"/root/llamarec/outputs/m/movielens-1m/exposure_m1_s24000_seed43/adapter","candidate_files":{"test":"/root/llamarec/data/candidates/movielens-1m/variants/k50_seed42/test.jsonl"},"counts":{"test":{"m_y_predictions":11544,"m_n_predictions":5675}},"outputs_dir":"/root/llamarec/outputs/phase2a/multiseed96_ranking_robustness/seed43/m1_k50_seed42","global_step":null,"max_steps":null}
- file: /root/llamarec/outputs/phase2a/multiseed96_ranking_robustness/seed43/m1_k50_seed42/evaluation_config_snapshot.yaml
  size: 8268
  mtime: 2026-09-08 11:11:21.765171143 +0800
  sha256: 444ea827915a8b1dbc99144c5ee7ce4dd8c0a2a8228b932bf5c380d8676d53d4
  identity: seed:;dataset:;model:;
- file: /root/llamarec/outputs/phase2a/multiseed96_ranking_robustness/seed43/m1_k50_seed42/valid_metrics.json
  size: 763
  mtime: 2026-09-07 12:07:33.606579685 +0800
  sha256: 0614f9b7c842d1b9abdb538e0bd71fff04be2d350153b1a1489d7a03fccfa136
  identity: {"model":"m_k0","dataset":"movielens-1m","seed":null,"splits":null,"adapter_dir":"/root/llamarec/outputs/m/movielens-1m/exposure_m1_s24000_seed43/adapter","candidate_files":null,"counts":null,"outputs_dir":null,"global_step":null,"max_steps":null}
- file: /root/llamarec/outputs/phase2a/multiseed96_ranking_robustness/seed43/m1_k50_seed42/test_metrics.json
  size: 757
  mtime: 2026-09-08 11:48:06.411262623 +0800
  sha256: d75667a6fca0cb6eca63abe3d49e74dae7f808c78ab36d35c35b33a243891481
  identity: {"model":"m_k0","dataset":"movielens-1m","seed":null,"splits":null,"adapter_dir":"/root/llamarec/outputs/m/movielens-1m/exposure_m1_s24000_seed43/adapter","candidate_files":null,"counts":null,"outputs_dir":null,"global_step":null,"max_steps":null}

#### Prediction candidates

- file: /root/llamarec/outputs/phase2a/multiseed96_ranking_robustness/seed43/m1_k50_seed42/m_n_test_predictions.jsonl
  absolute_path: /root/llamarec/outputs/phase2a/multiseed96_ranking_robustness/seed43/m1_k50_seed42/m_n_test_predictions.jsonl
  size: 22223552
  mtime: 2026-09-08 11:48:06.287262146 +0800
  sha256: 0c082288a842c78caab580fa0fb4ec71490df95f5765225e73971f2bf72909c3
  rows: 5675
  schema: adapter_dir,candidate_generation,candidate_movie_ids,ground_truth_index,ground_truth_movie_id,inference_mode,label,label_probabilities,label_set,model,predicted_label,prompt_hash,scores,scoring_mode,split,task,user_id
  first_row_identity: {"model":"m_k0","task":"N","inference_mode":"m_next_item_candidate_probability","split":"test","user_id":"1","ground_truth_movie_id":"48","candidate_generation":{"method":"random","variant_name":"k50_seed42","candidate_num":50,"negative_num":49,"seed":244,"pool":"all_movies_minus_current_ground_truth_item","shuffle_order":true},"adapter_dir":"/root/llamarec/outputs/m/movielens-1m/exposure_m1_s24000_seed43/adapter"}
- file: /root/llamarec/outputs/phase2a/multiseed96_ranking_robustness/seed43/m1_k50_seed42/m_n_valid_predictions.jsonl
  absolute_path: /root/llamarec/outputs/phase2a/multiseed96_ranking_robustness/seed43/m1_k50_seed42/m_n_valid_predictions.jsonl
  size: 22258110
  mtime: 2026-09-07 12:07:33.510579982 +0800
  sha256: 4b614a5240c25154b36879cd7aa9dfb31e76db4439197ce135ed5c53599ec547
  rows: 5675
  schema: adapter_dir,candidate_generation,candidate_movie_ids,ground_truth_index,ground_truth_movie_id,inference_mode,label,label_probabilities,label_set,model,predicted_label,prompt_hash,scores,scoring_mode,split,task,user_id
  first_row_identity: {"model":"m_k0","task":"N","inference_mode":"m_next_item_candidate_probability","split":"validation","user_id":"1","ground_truth_movie_id":"527","candidate_generation":{"method":"random","variant_name":"k50_seed42","candidate_num":50,"negative_num":49,"seed":143,"pool":"all_movies_minus_current_ground_truth_item","shuffle_order":true},"adapter_dir":"/root/llamarec/outputs/m/movielens-1m/exposure_m1_s24000_seed43/adapter"}
- file: /root/llamarec/outputs/phase2a/multiseed96_ranking_robustness/seed43/m1_k50_seed42/m_y_test_predictions.jsonl
  absolute_path: /root/llamarec/outputs/phase2a/multiseed96_ranking_robustness/seed43/m1_k50_seed42/m_y_test_predictions.jsonl
  size: 4898513
  mtime: 2026-09-08 11:34:05.217464022 +0800
  sha256: dfa11e9567dc69aeba88fb683a6cc7c5031b15b1c2ffbf98fff39235f690c509
  rows: 11544
  schema: adapter_dir,inference_mode,label,model,p_no,p_yes,predicted_label,prompt_hash,score,scoring_mode,split,target_movie_id,task,user_id
  first_row_identity: {"model":"m_k0","task":"Y","inference_mode":"m_yesno_p_yes","split":"test","user_id":"1","ground_truth_movie_id":null,"candidate_generation":null,"adapter_dir":"/root/llamarec/outputs/m/movielens-1m/exposure_m1_s24000_seed43/adapter"}
- file: /root/llamarec/outputs/phase2a/multiseed96_ranking_robustness/seed43/m1_k50_seed42/m_y_valid_predictions.jsonl
  absolute_path: /root/llamarec/outputs/phase2a/multiseed96_ranking_robustness/seed43/m1_k50_seed42/m_y_valid_predictions.jsonl
  size: 5326821
  mtime: 2026-09-07 11:53:31.609696612 +0800
  sha256: a2efe967c214a7fcb326d257297830456279a09b925af2cecb6bd886664aba66
  rows: 12381
  schema: adapter_dir,inference_mode,label,model,p_no,p_yes,predicted_label,prompt_hash,score,scoring_mode,split,target_movie_id,task,user_id
  first_row_identity: {"model":"m_k0","task":"Y","inference_mode":"m_yesno_p_yes","split":"validation","user_id":"1","ground_truth_movie_id":null,"candidate_generation":null,"adapter_dir":"/root/llamarec/outputs/m/movielens-1m/exposure_m1_s24000_seed43/adapter"}

