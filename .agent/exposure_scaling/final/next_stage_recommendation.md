# Next Stage Recommendation

Stay in this stage and run only the first approved GPU batch after the cloud resume inventory passes.

Recommended first batch:

1. Cloud checkpoint inventory and validation-metric inventory.
2. Y-K0 24k and 48k.
3. N-K0 48k, reusing existing N-K0 24k.
4. Validation PopMatch evaluation for all retained points.

Do not start M1, SASRec gap filling, Amazon scaling, multi-seed, or million-level LLM exposure until the Y/N 24k/48k shape is known.
