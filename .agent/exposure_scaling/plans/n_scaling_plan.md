# N-K0 Scaling Plan

N-K0 already has PopMatch-k5 seed42 points at 3k, 6k, 12k, and 24k N-task exposure. The 24k point should be reused rather than retrained, provided its checkpoint and validation artifacts can be found on cloud.

| target N exposure | optimizer steps | status |
|---:|---:|---|
| 12000 | 1500 | current anchor |
| 24000 | 3000 | already exists |
| 48000 | 6000 | first missing N point |
| 96000 | 12000 | conditional |
| 200000 | 25000 | near-full loaded pool, conditional |

First GPU batch should not repeat N 24k. It should inventory N 12k/24k checkpoints, add missing validation PopMatch metrics if needed, then train/resume N-K0 to 48k only after resume safety is confirmed.
