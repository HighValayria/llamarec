# Exposure Stage Close Readiness

1. Exposure scaling 的主要问题已经在 seed42 范围内回答：Y-side gains weaken by 96k，N-native ranking remains exposure-sensitive through 200k。

2. Seed42 evidence 已经足以进入论文 Results draft，但只能支持限定性表述。

3. 仍然 open 的问题包括 multiseed 稳定性、hard-candidate protocol composition confound、M1-200 是否存在高 exposure crossover，以及 Amazon 是否需要 exposure scaling 复现。

4. 这些 open questions 不是当前 Results draft 的 blocker，只影响 claim strength。

5. Multiseed 的状态是 recommended。若论文追求强泛化结论，它接近 required；若采用 seed42 descriptive language，它是 optional enhancement。

6. M200 当前不必要。它成本高，只在论文核心 claim 需要证明 200k matched multitask endpoint 时才值得运行。

7. 建议关闭 Exposure Scaling stage 的训练部分，并将本阶段切换为 evidence freeze / paper writing。

8. 建议恢复 Paper Writing / Submission Package，但必须使用本目录里的 claim boundaries，而不是旧叙事。
