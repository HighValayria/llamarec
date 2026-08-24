# SASRec Scaling Plan

Existing SASRec PopMatch-k5 points include 11,776 exposure (`s23`), 24,064 exposure (`s47`), and 767,424/1,534,656 high-exposure anchors.

| target exposure | SASRec steps | exact exposure | status |
|---:|---:|---:|---|
| 48000 | 94 | 48128 | missing |
| 96000 | 188 | 96256 | missing |
| 200000 | 391 | 200000 | missing |

Only fill SASRec gaps that align with final retained N-K0 exposure points.
