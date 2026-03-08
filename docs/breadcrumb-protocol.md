# Breadcrumb Protocol

> **Governance**: Amendment F of `governance-rules.json`
> **Scope**: All development sessions across the eight-organ system
> **Version**: 1.0

---

## Why This Exists

During a multi-agent coordination incident, an auto-sync agent modified files in
`orchestration-start-here/` while another agent was committing there. No audit trail
identified which agent touched which files, when, or why.

The breadcrumb protocol ensures that every completed session — interactive or not —
leaves a machine-parseable record of what happened. This is the "who touched this?"
problem, solved at the protocol level.

---

## Breadcrumb Format

```markdown
<!-- breadcrumb:v1 -->
**Session**: <agent-name> | <date> | <repo>
**Phase**: DONE | <organ>/<repo> | <issue-ref>

**Done:**
- <what was completed, 1-3 bullets>

**Next:**
- <what should happen next, max 3 bullets>

**Pipeline**: <promotion_status> (no change | promoted from X)
**Commit**: <sha or "no commit">
<!-- /breadcrumb -->
```

### Field Descriptions

| Field | Required | Description |
|-------|----------|-------------|
| `agent-name` | Yes | Human or agent identifier (e.g., `claude-code`, `auto-sync`, `@4444j99`) |
| `date` | Yes | ISO 8601 date (`YYYY-MM-DD`) |
| `repo` | Yes | Repository name (e.g., `orchestration-start-here`) |
| `organ/repo` | Yes | Full path (e.g., `ORGAN-IV/orchestration-start-here`) |
| `issue-ref` | No | GitHub issue reference (e.g., `#87`) or `none` |
| `Done` | Yes | 1-3 bullet points describing completed work |
| `Next` | No | Up to 3 bullet points for follow-up work |
| `Pipeline` | Yes | Current promotion status and whether it changed |
| `Commit` | Yes | Commit SHA or `no commit` if no changes were made |

### Version Tag

The `<!-- breadcrumb:v1 -->` delimiter includes a version tag. If the format evolves,
increment the version (v2, v3). Parsers should check the version before extracting fields.

---

## When to Write

**Always at DONE phase.** Every session that reaches DONE must leave a breadcrumb.

- **Successful sessions**: Full breadcrumb with Done/Next/Commit
- **Failed sessions**: Breadcrumb with Done describing what was attempted, Next describing blockers
- **Non-interactive sessions**: Breadcrumb is mandatory per the safety protocol (`petasum-super-petasum/docs/NON-INTERACTIVE-AGENT-SAFETY.md`)

---

## Where to Write

### Primary: Issue Comment

If the session is linked to a GitHub issue, post the breadcrumb as an issue comment.
This keeps the audit trail attached to the work item.

```bash
gh issue comment <number> --body "$(cat <<'EOF'
<!-- breadcrumb:v1 -->
**Session**: claude-code | 2026-03-08 | orchestration-start-here
**Phase**: DONE | ORGAN-IV/orchestration-start-here | #87

**Done:**
- Standardized breadcrumb format with machine-parseable delimiters
- Updated session protocol and conductor playbook

**Next:**
- Implement breadcrumb parser script (F-57)

**Pipeline**: PUBLIC_PROCESS (no change)
**Commit**: abc1234
<!-- /breadcrumb -->
EOF
)"
```

### Fallback: Standalone File

If no issue is linked, write to `.breadcrumb.md` in the repo root. This file is
overwritten each session (it records only the most recent breadcrumb).

### CHANGELOG

For user-visible changes, also add an entry to `CHANGELOG.md`. The CHANGELOG is
for humans; the breadcrumb is for machines and agent handoff.

---

## Parsing

The HTML comment delimiters (`<!-- breadcrumb:v1 -->` ... `<!-- /breadcrumb -->`)
enable machine parsing without visual noise in rendered markdown.

To extract breadcrumbs from issue comments:

```bash
gh issue view <number> --json comments \
  | jq '.comments[].body' \
  | grep -A 20 'breadcrumb:v1'
```

A formal parser script is planned as part of F-57 (Agent Run Logging Standard).

---

## Examples

### Successful Feature Session

```markdown
<!-- breadcrumb:v1 -->
**Session**: claude-code | 2026-03-08 | orchestration-start-here
**Phase**: DONE | ORGAN-IV/orchestration-start-here | #87

**Done:**
- Created breadcrumb-protocol.md with format spec
- Updated session-protocol.md Step 6 with standard format
- Added Amendment F to governance-rules.json

**Next:**
- Implement breadcrumb parser (F-57)
- Add breadcrumb validation to CI

**Pipeline**: PUBLIC_PROCESS (no change)
**Commit**: abc1234
<!-- /breadcrumb -->
```

### Failed Session

```markdown
<!-- breadcrumb:v1 -->
**Session**: claude-code | 2026-03-08 | agentic-titan
**Phase**: DONE | ORGAN-IV/agentic-titan | #29

**Done:**
- Attempted Redis adapter integration
- Discovered incompatible version (requires Redis 7+, CI has 6.2)

**Next:**
- Upgrade Redis in CI matrix
- Retry integration after CI fix

**Pipeline**: PUBLIC_PROCESS (no change)
**Commit**: no commit
<!-- /breadcrumb -->
```

### Non-Interactive Agent Session

```markdown
<!-- breadcrumb:v1 -->
**Session**: auto-sync | 2026-03-08 | orchestration-start-here
**Phase**: DONE | ORGAN-IV/orchestration-start-here | none

**Done:**
- Synced AGENTS.md with latest agent registry
- Updated GEMINI.md with new model references

**Next:**
- none

**Pipeline**: PUBLIC_PROCESS (no change)
**Commit**: def5678
<!-- /breadcrumb -->
```

---

## References

- **Session Protocol**: `docs/session-protocol.md` — Step 6 references this protocol
- **Conductor Playbook**: `docs/conductor-playbook.md` — DONE phase references this protocol
- **Safety Protocol**: `petasum-super-petasum/docs/NON-INTERACTIVE-AGENT-SAFETY.md` — requires breadcrumbs for non-interactive sessions
- **Governance**: `governance-rules.json` — Amendment F codifies the breadcrumb mandate
