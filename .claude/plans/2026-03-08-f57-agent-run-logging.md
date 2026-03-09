# Plan: F-57 — Agent Run Logging Standard

**Date**: 2026-03-08
**Issue**: #107
**Repo**: orchestration-start-here
**Scope**: Spec doc + validation script. No runtime changes to agent--claude-smith or agentic-titan (those are follow-ups).

## Acceptance Criteria

1. `docs/agent-run-logging.md` defines the standard directory layout and required files
2. `scripts/validate-agent-run.py` validates a run directory against the spec
3. CHANGELOG updated
4. Issue #107 gets a breadcrumb comment
5. F-82 audit requirements (NON-INTERACTIVE-AGENT-SAFETY.md) align with this spec

## Critical Files

| File | Action |
|------|--------|
| `docs/agent-run-logging.md` | CREATE — spec document |
| `scripts/validate-agent-run.py` | CREATE — validation script |
| `CHANGELOG.md` | EDIT |

## Out of Scope

- Runtime integration into agent--claude-smith (follow-up)
- Runtime integration into agentic-titan (follow-up)
- CI workflow for automated validation
- Log rotation/retention automation

## Design Decisions

- Directory layout: `$AGENTS_LOG/$AGENT_RUN_ID/` with `manifest.json`, `prompt.md`, `session.log`, `patch.diff`
- manifest.json schema aligns with F-82 audit fields (session_id, agent_name, repo_path, timestamps, files_read/written, etc.)
- Validation script uses argparse + pathlib, no external deps
- breadcrumb:v1 block is extractable from session.log
