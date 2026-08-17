# Multi-seed Stability Summary

Dataset: `movielens-1m`.
Protocol: `MovieLens-1M multi-seed stability on fixed k5_popmatch_seed42 candidates`.

## Metrics

| model | seed | regime | binary_AUC | binary_F1 | HR@1 | NDCG@5 | MRR | evidence_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Y-K0 | 42 | binary_preference | 0.769096677 | 0.7799722571 | 0.304845815 | 0.6503957066 | 0.5365521292 | computed |
| Y-K0 | 43 | binary_preference | 0.7638536397 | 0.7770993369 | 0.1948898678 | 0.5869765641 | 0.4531071953 | computed |
| Y-K0 | 44 | binary_preference | 0.7667400862 | 0.7701956507 | 0.2116299559 | 0.5941504467 | 0.4627518355 | computed |
| N-K0 | 42 | popmatch_ranking | unavailable | unavailable | 0.5466079295 | 0.7884963692 | 0.718041116 | computed |
| N-K0 | 43 | popmatch_ranking | unavailable | unavailable | 0.5427312775 | 0.7869133539 | 0.7158825257 | computed |
| N-K0 | 44 | popmatch_ranking | unavailable | unavailable | 0.5383259912 | 0.7831335521 | 0.7110044053 | computed |
| M1 | 42 | popmatch_ranking | 0.7664368902 | 0.7281077294 | 0.523876652 | 0.778191233 | 0.7042525698 | computed |
| M1 | 43 | popmatch_ranking | 0.7669426412 | 0.7356690329 | 0.521938326 | 0.7767052601 | 0.702328928 | computed |
| M1 | 44 | popmatch_ranking | 0.7615278434 | 0.6922447644 | 0.5279295154 | 0.7794587445 | 0.7059941263 | computed |
| SASRec exp-match | 42 | roughly_exposure_matched | unavailable | unavailable | 0.2699559471 | 0.6348928207 | 0.5156622614 | computed |
| SASRec exp-match | 43 | roughly_exposure_matched | unavailable | unavailable | 0.2548017621 | 0.6264308277 | 0.5044816446 | computed |
| SASRec exp-match | 44 | roughly_exposure_matched | unavailable | unavailable | 0.253215859 | 0.6263785286 | 0.5043935389 | computed |
| SASRec high s3000 | 42 | high_exposure | unavailable | unavailable | 0.6243171806 | 0.8283562609 | 0.770866373 | computed |
| SASRec high s3000 | 43 | high_exposure | unavailable | unavailable | 0.6285462555 | 0.8295574494 | 0.7725022026 | computed |
| SASRec high s3000 | 44 | high_exposure | unavailable | unavailable | 0.6304845815 | 0.8294692615 | 0.7724992658 | computed |

## Aggregates

| model | regime | metric | seeds | mean | std | min | max | range |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| M1 | popmatch_ranking | binary_AUC | 3 | 0.7649691249 | 0.0024420975 | 0.7615278434 | 0.7669426412 | 0.0054147978 |
| M1 | popmatch_ranking | binary_F1 | 3 | 0.7186738422 | 0.0189414087 | 0.6922447644 | 0.7356690329 | 0.0434242685 |
| M1 | popmatch_ranking | binary_Accuracy | 3 | 0.6905174405 | 0.0116456969 | 0.6741164241 | 0.700017325 | 0.0259009009 |
| M1 | popmatch_ranking | HR@1 | 3 | 0.5245814978 | 0.0024961562 | 0.521938326 | 0.5279295154 | 0.0059911894 |
| M1 | popmatch_ranking | NDCG@5 | 3 | 0.7781184125 | 0.001125284 | 0.7767052601 | 0.7794587445 | 0.0027534844 |
| M1 | popmatch_ranking | MRR | 3 | 0.7041918747 | 0.0014969263 | 0.702328928 | 0.7059941263 | 0.0036651983 |
| N-K0 | popmatch_ranking | HR@1 | 3 | 0.5425550661 | 0.0033833823 | 0.5383259912 | 0.5466079295 | 0.0082819383 |
| N-K0 | popmatch_ranking | NDCG@5 | 3 | 0.7861810917 | 0.0022497567 | 0.7831335521 | 0.7884963692 | 0.0053628171 |
| N-K0 | popmatch_ranking | MRR | 3 | 0.7149760157 | 0.0029433705 | 0.7110044053 | 0.718041116 | 0.0070367107 |
| SASRec exp-match | roughly_exposure_matched | HR@1 | 3 | 0.2593245227 | 0.0075453809 | 0.253215859 | 0.2699559471 | 0.0167400881 |
| SASRec exp-match | roughly_exposure_matched | NDCG@5 | 3 | 0.629234059 | 0.0040014057 | 0.6263785286 | 0.6348928207 | 0.0085142921 |
| SASRec exp-match | roughly_exposure_matched | MRR | 3 | 0.5081791483 | 0.0052914823 | 0.5043935389 | 0.5156622614 | 0.0112687225 |
| SASRec high s3000 | high_exposure | HR@1 | 3 | 0.6277826725 | 0.0025750732 | 0.6243171806 | 0.6304845815 | 0.0061674009 |
| SASRec high s3000 | high_exposure | NDCG@5 | 3 | 0.8291276573 | 0.0005466465 | 0.8283562609 | 0.8295574494 | 0.0012011885 |
| SASRec high s3000 | high_exposure | MRR | 3 | 0.7719559471 | 0.0007704462 | 0.770866373 | 0.7725022026 | 0.0016358296 |
| Y-K0 | binary_preference | binary_AUC | 3 | 0.7665634676 | 0.0021441013 | 0.7638536397 | 0.769096677 | 0.0052430373 |
| Y-K0 | binary_preference | binary_F1 | 3 | 0.7757557482 | 0.0041027983 | 0.7701956507 | 0.7799722571 | 0.0097766064 |
| Y-K0 | binary_preference | binary_Accuracy | 3 | 0.7084488335 | 0.0022867856 | 0.7059078309 | 0.7114518365 | 0.0055440056 |
| Y-K0 | binary_preference | HR@1 | 3 | 0.2371218796 | 0.0483732447 | 0.1948898678 | 0.304845815 | 0.1099559472 |
| Y-K0 | binary_preference | NDCG@5 | 3 | 0.6105075725 | 0.0283568167 | 0.5869765641 | 0.6503957066 | 0.0634191425 |
| Y-K0 | binary_preference | MRR | 3 | 0.4841370533 | 0.0372716148 | 0.4531071953 | 0.5365521292 | 0.0834449339 |

## Comparisons

| comparison | seed | delta_HR@1 | delta_NDCG@5 | delta_MRR | evidence_status |
| --- | --- | --- | --- | --- | --- |
| N-K0_minus_M1 | 42 | 0.0227312775 | 0.0103051362 | 0.0137885462 | computed |
| N-K0_minus_M1 | 43 | 0.0207929515 | 0.0102080938 | 0.0135535977 | computed |
| N-K0_minus_M1 | 44 | 0.0103964758 | 0.0036748076 | 0.005010279 | computed |
| N-K0_minus_SASRec_exp_match | 42 | 0.2766519824 | 0.1536035485 | 0.2023788546 | computed |
| N-K0_minus_SASRec_exp_match | 43 | 0.2879295154 | 0.1604825262 | 0.2114008811 | computed |
| N-K0_minus_SASRec_exp_match | 44 | 0.2851101322 | 0.1567550235 | 0.2066108664 | computed |
| SASRec_high_s3000_minus_N-K0 | 42 | 0.0777092511 | 0.0398598917 | 0.052825257 | computed |
| SASRec_high_s3000_minus_N-K0 | 43 | 0.085814978 | 0.0426440955 | 0.0566196769 | computed |
| SASRec_high_s3000_minus_N-K0 | 44 | 0.0921585903 | 0.0463357094 | 0.0614948605 | computed |

## Direct Answers

- y_k0_binary_stability: available across 3 seeds; F1 range 0.0097766064
- n_k0_above_m1_by_hr1: yes across 3 seeds; minimum margin 0.0103964758
- n_k0_above_sasrec_exp_match_by_hr1: yes across 3 seeds; minimum margin 0.2766519824
- sasrec_high_above_n_k0_by_hr1: yes across 3 seeds; minimum margin 0.0777092511
- candidate_protocol_fixed: yes: all rows use k5_popmatch_seed42
- interpretation: main ranking and sample-efficiency directions are stable across seeds 42/43/44; high-exposure SASRec is a separate budget regime

## Boundary

This is a three-seed stability diagnostic. Candidate sets are fixed at k5_popmatch_seed42 while model training seeds vary.
