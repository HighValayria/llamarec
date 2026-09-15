# Task Packet: Text Compression Audit

- Stage: S5 Review
- Scope: audit all current author sections for prose function, cross-section repetition, paragraph-level compression priority, and page-saving scenarios.
- Files to read: `paper/modules/**`, `paper/modules_parts/**`, current English PDF, table evidence audit/judge packet, and figure/results display audit/judge packet.
- Files allowed to edit: this task packet, `text-compression-audit.md`, `text-compression-judge-packet.md`, `paper/plan/progress.md`, `.agent/current_task.md`, and `.agent/stage_state.yaml`.
- Required skills: using-research-writing, paper-orchestration, peer-review, verification, and read-only PDF inspection.
- Evidence/data inputs: current bilingual author sources, current 14-page English IEEE build, frozen T-BALANCED and D-BALANCED plans.
- Required artifacts: section function map; repetition matrix; section word/paragraph/PDF-footprint inventory; per-paragraph priority; `NON_COMPRESSIBLE_CORE`; P-LIGHT/P-BALANCED/P-AGGRESSIVE scenarios; judge packet; old-version recovery check.
- Rejection checks: no manuscript replacement prose; no edits to author source, tables, figures, submission adapter, build, or Wiki; no recompilation; no raw experiment research; no change to the frozen thesis or contribution hierarchy.
- Validation commands: paragraph-ID coverage and word-count checks; before/after aggregate hashes for protected trees and PDF; artifact-content checks; `python tools/stage_guard.py`; `git diff --check` limited to newly written planning/state files.
- Review gates: spec-compliance review and scientific/quality review must both pass before closure.

## Frozen Scientific Core

- Conclusions remain conditioned on supervision formulation, cumulative downstream task-sample exposure, and candidate evaluation protocol.
- Contribution hierarchy remains C2 primary, C4 secondary, C3 supporting, and C1 framing.
- T-BALANCED and D-BALANCED are planning inputs only; this stage does not execute either plan.

