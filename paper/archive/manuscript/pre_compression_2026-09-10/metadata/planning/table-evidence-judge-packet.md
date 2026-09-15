# Table Evidence Judge Packet

## Decision Target

在不损失RQ1-RQ5所需task、split、seed、protocol、metric和uncertainty维度的前提下裁决主文表格压缩强度。旧表已永久归档；本文件不授权执行。

## Minimum Evidence

- RQ1: III+IV，Y-native、Y-as-ranker与N-native监督语义对照。
- RQ2: II+III/IV+V，曝光定义及Y/N不同响应；V与Figure1只部分重复。
- RQ3: V+VIII+IX，Y-side preservation、validation narrowing、frozen-test modest N gap。
- RQ4: IX+X；三seed mean/SD与seed42 paired bootstrap必须分开，XI/XII是raw detail。
- RQ5: XIII，四个matched exposure的valid/test HR；Figure2只重复validation。
- External boundary: XIV，Amazon只支持早期seed42 test ranking directions。

## Verdicts

| PDF | RQ | Verdict | Valid/Test | Future identity |
| --- | --- | --- | --- | --- |
| I | setup all | CORE_MAIN | BOTH counts | unchanged |
| II | 2/3/5 | COMPACT_MAIN | N/A | training_exposure_compact.csv |
| III | 1/2/3 | COMPACT_MAIN | SUMMARY_BOTH | binary_exposure_compact.csv |
| IV | 1/2 | MERGE_CANDIDATE | SUMMARY_BOTH | supervision_semantics_compact.csv |
| V | 2/3 | CORE_MAIN | BOTH | unchanged |
| VI | 3 | SUPPLEMENT_CANDIDATE | RAW_TO_SUPPLEMENT | ms96_native_summary_compact.csv |
| VII | 3 | SUPPLEMENT_CANDIDATE | RAW_TO_SUPPLEMENT | ms96_native_summary_compact.csv |
| VIII | 3 | CORE_MAIN | VALID_ONLY | unchanged |
| IX | 3/4 | COMPACT_MAIN | SUMMARY_BOTH | ms96_delta_summary_compact.csv |
| X | 3/4 | COMPACT_MAIN | BOTH | hard_candidate_compact.csv |
| XI | 4 | SUPPLEMENT_CANDIDATE | RAW_TO_SUPPLEMENT | ms96_protocol_summary_compact.csv |
| XII | 3/4 | SUPPLEMENT_CANDIDATE | RAW_TO_SUPPLEMENT | ms96_protocol_summary_compact.csv |
| XIII | 5 | CORE_MAIN | BOTH | unchanged |
| XIV | external | CORE_MAIN | TEST_ONLY | unchanged |

`REDUNDANT_MAIN=0`。VI/VII/XI/XII仍有raw审计价值，应后移而不是删除。

## Plans

| Plan | Main | Compact | Merge | Raw detail moved | Estimated saving | Risk |
| --- | ---: | ---: | --- | --- | --- | --- |
| T-LIGHT | 12 | 2 | 0 | XI/XII | 0.8-1.4 pages | page reduction limited |
| T-BALANCED | 9 | 4 | III+IV | VI/VII/XI/XII + full IX/X | 1.8-2.8 pages | compact IX/X must preserve two uncertainty sources |
| T-AGGRESSIVE | 6 | 6 | III-V and VIII-X | most raw/secondary metrics | 2.8-4.0 pages | may flatten scientific distinctions |

## Recommendation

Recommend `T-BALANCED`: I; compact II; merged III/IV; V; VIII; compact IX; compact X; XIII; XIV。选择性保留validation/test，不采用全局规则。Supplement允许时后移full VI/VII/XI/XII和full IX/X；不允许时，compact IX/X必须包含split、protocol、training-seed variability、seed42 CI status、metric-consistency indicators和关键range，使主文自足。

Archive: `paper/archive/tables/pre_compression_2026-09-10/`，14/14 byte-identical snapshots with SHA256 manifest。No active table or manuscript source modification is authorized or executed。
