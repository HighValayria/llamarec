# Cold/Tail Item Slice Diagnostic

Dataset: `movielens-1m`.
Split: `test`.
Candidate file: `/root/llamarec/data/candidates/movielens-1m/variants/k5_popmatch_seed42/test.jsonl`.

## Target Popularity Buckets

| bucket | sample_count |
|---|---:|
| <=10 | 26 |
| 11-50 | 199 |
| 51-200 | 854 |
| 201-500 | 1497 |
| >500 | 3099 |

## Metrics

| model | bucket | samples | HR@1 | NDCG@5 | MRR | mean_rank | evidence_status |
|---|---|---:|---:|---:|---:|---:|---|
| N-K0 | <=10 | 26 | 0.5 | 0.7722156998 | 0.6955128205 | 1.8846153846 | computed_from_prediction_file |
| N-K0 | 11-50 | 199 | 0.5326633166 | 0.7704070304 | 0.6949748744 | 2.040201005 | computed_from_prediction_file |
| N-K0 | 51-200 | 854 | 0.5913348946 | 0.8100663737 | 0.7467213115 | 1.7927400468 | computed_from_prediction_file |
| N-K0 | 201-500 | 1497 | 0.588510354 | 0.8108894302 | 0.7476397239 | 1.7768871075 | computed_from_prediction_file |
| N-K0 | >500 | 3099 | 0.515327525 | 0.7730332778 | 0.6975099494 | 1.9599870926 | computed_from_prediction_file |
| M1 | <=10 | 26 | 0.4615384615 | 0.7489299282 | 0.6647435897 | 2.0 | computed_from_prediction_file |
| M1 | 11-50 | 199 | 0.4422110553 | 0.7391193883 | 0.6520938023 | 2.0804020101 | computed_from_prediction_file |
| M1 | 51-200 | 854 | 0.5608899297 | 0.7973105962 | 0.7295277127 | 1.8302107728 | computed_from_prediction_file |
| M1 | 201-500 | 1497 | 0.5671342685 | 0.7997579927 | 0.7328434647 | 1.8243152973 | computed_from_prediction_file |
| M1 | >500 | 3099 | 0.4985479187 | 0.765258905 | 0.6871571475 | 1.9941916747 | computed_from_prediction_file |
| SASRec exp-match | <=10 | 26 | 0.1153846154 | 0.550834018 | 0.4051282051 | 3.1923076923 | computed_from_prediction_file |
| SASRec exp-match | 11-50 | 199 | 0.2512562814 | 0.6214783103 | 0.4983249581 | 2.8140703518 | computed_from_prediction_file |
| SASRec exp-match | 51-200 | 854 | 0.2540983607 | 0.6255257072 | 0.5032982045 | 2.7599531616 | computed_from_prediction_file |
| SASRec exp-match | 201-500 | 1497 | 0.2745490982 | 0.63837287 | 0.520240481 | 2.6967267869 | computed_from_prediction_file |
| SASRec exp-match | >500 | 3099 | 0.2746047112 | 0.6373597125 | 0.5188985694 | 2.6986124556 | computed_from_prediction_file |
| SASRec s47 | <=10 | 26 | 0.1538461538 | 0.5559382653 | 0.4128205128 | 3.2307692308 | computed_from_prediction_file |
| SASRec s47 | 11-50 | 199 | 0.2311557789 | 0.6163314072 | 0.491038526 | 2.8040201005 | computed_from_prediction_file |
| SASRec s47 | 51-200 | 854 | 0.2646370023 | 0.6359123436 | 0.5168032787 | 2.6978922717 | computed_from_prediction_file |
| SASRec s47 | 201-500 | 1497 | 0.289245157 | 0.6467861072 | 0.531173458 | 2.6359385438 | computed_from_prediction_file |
| SASRec s47 | >500 | 3099 | 0.2913843175 | 0.645482487 | 0.5295740561 | 2.6489190061 | computed_from_prediction_file |
| SASRec s1500 | <=10 | 26 | 0.3076923077 | 0.6566930786 | 0.5442307692 | 2.5769230769 | computed_from_prediction_file |
| SASRec s1500 | 11-50 | 199 | 0.5075376884 | 0.7669956953 | 0.6895309883 | 1.9849246231 | computed_from_prediction_file |
| SASRec s1500 | 51-200 | 854 | 0.6463700234 | 0.8400894782 | 0.7863387978 | 1.6358313817 | computed_from_prediction_file |
| SASRec s1500 | 201-500 | 1497 | 0.6559786239 | 0.8433317461 | 0.7907704297 | 1.6305945224 | computed_from_prediction_file |
| SASRec s1500 | >500 | 3099 | 0.5847047435 | 0.8076080336 | 0.743390341 | 1.7992900936 | computed_from_prediction_file |
| SASRec s3000 | <=10 | 26 | 0.2692307692 | 0.6417932975 | 0.5243589744 | 2.6538461538 | computed_from_prediction_file |
| SASRec s3000 | 11-50 | 199 | 0.5728643216 | 0.7985994133 | 0.7317420436 | 1.864321608 | computed_from_prediction_file |
| SASRec s3000 | 51-200 | 854 | 0.6791569087 | 0.8558128513 | 0.8072794692 | 1.5690866511 | computed_from_prediction_file |
| SASRec s3000 | 201-500 | 1497 | 0.665998664 | 0.8488983103 | 0.7981629927 | 1.6072144289 | computed_from_prediction_file |
| SASRec s3000 | >500 | 3099 | 0.5953533398 | 0.81434299 | 0.7522265247 | 1.7612132946 | computed_from_prediction_file |

## Deltas

| comparison | bucket | samples | delta_HR@1 | delta_NDCG@5 | delta_MRR | delta_mean_rank | evidence_status |
|---|---|---:|---:|---:|---:|---:|---|
| N-K0_minus_M1 | <=10 | 26 | 0.0384615385 | 0.0232857716 | 0.0307692308 | -0.1153846154 | computed |
| N-K0_minus_M1 | 11-50 | 199 | 0.0904522613 | 0.0312876421 | 0.0428810721 | -0.0402010051 | computed |
| N-K0_minus_M1 | 51-200 | 854 | 0.0304449649 | 0.0127557775 | 0.0171935988 | -0.037470726 | computed |
| N-K0_minus_M1 | 201-500 | 1497 | 0.0213760855 | 0.0111314375 | 0.0147962592 | -0.0474281898 | computed |
| N-K0_minus_M1 | >500 | 3099 | 0.0167796063 | 0.0077743728 | 0.0103528019 | -0.0342045821 | computed |
| SASRec exp-match_minus_N-K0 | <=10 | 26 | -0.3846153846 | -0.2213816818 | -0.2903846154 | 1.3076923077 | computed |
| SASRec exp-match_minus_N-K0 | 11-50 | 199 | -0.2814070352 | -0.1489287201 | -0.1966499163 | 0.7738693468 | computed |
| SASRec exp-match_minus_N-K0 | 51-200 | 854 | -0.3372365339 | -0.1845406665 | -0.243423107 | 0.9672131148 | computed |
| SASRec exp-match_minus_N-K0 | 201-500 | 1497 | -0.3139612558 | -0.1725165602 | -0.2273992429 | 0.9198396794 | computed |
| SASRec exp-match_minus_N-K0 | >500 | 3099 | -0.2407228138 | -0.1356735653 | -0.17861138 | 0.738625363 | computed |
| SASRec s47_minus_N-K0 | <=10 | 26 | -0.3461538462 | -0.2162774345 | -0.2826923077 | 1.3461538462 | computed |
| SASRec s47_minus_N-K0 | 11-50 | 199 | -0.3015075377 | -0.1540756232 | -0.2039363484 | 0.7638190955 | computed |
| SASRec s47_minus_N-K0 | 51-200 | 854 | -0.3266978923 | -0.1741540301 | -0.2299180328 | 0.9051522249 | computed |
| SASRec s47_minus_N-K0 | 201-500 | 1497 | -0.299265197 | -0.164103323 | -0.2164662659 | 0.8590514363 | computed |
| SASRec s47_minus_N-K0 | >500 | 3099 | -0.2239432075 | -0.1275507908 | -0.1679358933 | 0.6889319135 | computed |
| SASRec s1500_minus_N-K0 | <=10 | 26 | -0.1923076923 | -0.1155226212 | -0.1512820513 | 0.6923076923 | computed |
| SASRec s1500_minus_N-K0 | 11-50 | 199 | -0.0251256282 | -0.0034113351 | -0.0054438861 | -0.0552763819 | computed |
| SASRec s1500_minus_N-K0 | 51-200 | 854 | 0.0550351288 | 0.0300231045 | 0.0396174863 | -0.1569086651 | computed |
| SASRec s1500_minus_N-K0 | 201-500 | 1497 | 0.0674682699 | 0.0324423159 | 0.0431307058 | -0.1462925851 | computed |
| SASRec s1500_minus_N-K0 | >500 | 3099 | 0.0693772185 | 0.0345747558 | 0.0458803916 | -0.160696999 | computed |
| SASRec s3000_minus_N-K0 | <=10 | 26 | -0.2307692308 | -0.1304224023 | -0.1711538461 | 0.7692307692 | computed |
| SASRec s3000_minus_N-K0 | 11-50 | 199 | 0.040201005 | 0.0281923829 | 0.0367671692 | -0.175879397 | computed |
| SASRec s3000_minus_N-K0 | 51-200 | 854 | 0.0878220141 | 0.0457464776 | 0.0605581577 | -0.2236533957 | computed |
| SASRec s3000_minus_N-K0 | 201-500 | 1497 | 0.07748831 | 0.0380088801 | 0.0505232688 | -0.1696726786 | computed |
| SASRec s3000_minus_N-K0 | >500 | 3099 | 0.0800258148 | 0.0413097122 | 0.0547165753 | -0.198773798 | computed |

## Direct Answers

- cold_tail_status: computed for requested prediction files
- n_k0_cold_tail_advantage: N-K0 exceeds M1
- sasrec_exposure_matched_cold_tail_advantage: N-K0 exceeds SASRec exp-match
- sasrec_high_exposure_cold_tail_advantage: N-K0 exceeds high-exposure SASRec in the coldest bucket
- next_action: inspect low-sample cold buckets before making durable claims

## Boundary

This is a target-popularity slice diagnostic on fixed candidate prediction files, not a multi-seed or strict compute-matched claim.
