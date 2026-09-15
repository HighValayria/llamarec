# Canonical procedure: wiki-audit

Use this procedure to audit project documentation freshness and consistency. The audit may update documentation only when the intended correction is supported by repository evidence.

## Procedure

1. Read `AGENTS.md`, `wiki/index.md`, and `wiki/current_state.md`.
2. Run `python tools/wiki_guard.py` when Python is available.
3. Enumerate active wiki documents, prioritizing `status: current`.
4. Validate index coverage and local links.
5. Validate `related_code` paths.
6. For each high-value current document, inspect its claims and compare them with relevant code, tests, schemas, and configuration.
7. Use Git history/modification times only as a staleness heuristic, never as proof that a document is wrong.
8. Classify findings:
   - `OK`: evidence agrees.
   - `STALE`: current document is contradicted by clear repository evidence.
   - `POTENTIALLY_STALE`: evidence is incomplete or code changed after verification.
   - `ORPHAN`: active durable document missing from the active index.
   - `BROKEN_LINK`: referenced file/path does not exist.
   - `CONFLICT`: normative design and implementation disagree.
9. When a safe, obvious documentation-only correction exists, update the canonical document and metadata.
10. Do not silently resolve normative conflicts by rewriting the decision to match current code.
11. If a formerly correct document has been replaced, mark it superseded/archived and keep it out of the active index.
12. Update `wiki/current_state.md` only when the high-level current state is affected.
13. Record a semantic history entry when the audit discovers and resolves material drift.

## Audit output

Summarize:

- documents checked;
- deterministic guard results;
- stale or potentially stale documents;
- code/documentation conflicts;
- changes made;
- unresolved items requiring a human decision.

Cite file paths and code/tests that support each material finding.
