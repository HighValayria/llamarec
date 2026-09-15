# Canonical procedure: wiki-query

Use this procedure when answering a question about this repository's architecture, behavior, rationale, current state, or implementation.

## Procedure

1. Read `AGENTS.md`, `wiki/index.md`, and `wiki/current_state.md`.
2. Parse the user's question into concrete concepts, components, symbols, paths, or decisions.
3. Search active wiki documents first. Exclude `wiki/archive/` and avoid `wiki/history/` unless the question asks about history.
4. Prefer documents with `status: current`. Treat missing metadata as lower-confidence evidence.
5. Follow `related_code` paths and inspect the relevant implementation, tests, schemas, and configuration.
6. Search the repository for the concrete symbols or behavior named in the question.
7. Compare wiki claims against code/tests rather than repeating the wiki blindly.
8. If current documentation and implementation disagree, explicitly report documentation/architecture drift.
9. Use archived/superseded material only to explain historical context, and label it as historical.
10. Never use chat memory to override repository evidence.

## Answer format

Use concise prose, then include evidence in this structure:

**Conclusion:** direct answer.

**Wiki evidence:** `path:line-range` with a brief statement of what it supports.

**Code evidence:** `path:line-range` with a brief statement of what it supports.

**Consistency:** `consistent`, `partial`, `conflict`, or `insufficient evidence`.

**Confidence:** `high`, `medium`, or `low`, based on the quality and agreement of repository evidence.

When line numbers are not available from the active tool, cite exact file paths and symbol/section names instead of inventing line numbers.
