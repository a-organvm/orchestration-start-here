# Conductor Playbook — Frame / Shape / Build / Prove

> **Governance**: Amendment E of `governance-rules.json`
> **Scope**: All development sessions across the eight-organ system
> **Version**: 1.0

---

## Why This Exists

Without a lifecycle, sessions become **labyrinth sessions** — diving straight into implementation without framing the problem, building beyond scope, and ending without verification. The result is half-finished work, undocumented decisions, and mounting technical debt across 100+ repos.

The four-verb lifecycle exists to impose a minimal structure on every unit of work: understand before designing, design before building, verify before declaring done.

---

## Phase Definitions

### FRAME — Explore, read, ask questions

**Purpose**: Build enough understanding to write a scope statement. No code, no design — only observation.

**Activities**:
- Read CLAUDE.md, seed.yaml, and relevant source files
- Check open issues, recent commits, and CI status
- Identify constraints (dependencies, existing patterns, governance rules)
- Ask clarifying questions if the goal is ambiguous

**Entry criteria**: A task, issue, or directive exists.

**Exit criteria**: A **scope statement** is written — one sentence describing what will change and what will not. The scope statement lives in the plan file or issue comment.

**Hard gate**: You cannot exit FRAME without a scope statement. "Build everything" is not a scope statement.

---

### SHAPE — Design the approach, create a plan

**Purpose**: Decide *how* to solve the problem. Produce a plan with acceptance criteria.

**Activities**:
- Draft a plan file (`.claude/plans/YYYY-MM-DD-slug.md`)
- List 3–7 acceptance criteria (testable, specific)
- Identify critical files that will be created/modified
- Note out-of-scope items explicitly
- Consider what could go wrong (anti-patterns, edge cases)

**Entry criteria**: Scope statement from FRAME.

**Exit criteria**: A **plan file** exists with acceptance criteria. The criteria are specific enough that a different agent could verify them.

**Hard gate**: You cannot exit SHAPE without acceptance criteria. "Make it work" is not an acceptance criterion.

---

### BUILD — Implement within plan scope

**Purpose**: Write code, create files, make the changes specified in the plan. Nothing more.

**Activities**:
- Implement changes in the order specified by the plan
- Work in small, testable slices (max 30 minutes without a green test run)
- If scope needs to change, **back-transition to SHAPE** — do not silently expand

**Entry criteria**: Plan file with acceptance criteria from SHAPE.

**Exit criteria**: All acceptance criteria are addressed. Every file listed in the plan has been created or modified.

**Hard gate**: You cannot add work that isn't in the plan. If new work is discovered, note it as a follow-up issue and stay within scope.

---

### PROVE — Test, lint, verify

**Purpose**: Confirm the work is correct, complete, and leaves no mess behind.

**Activities**:
- Run tests (`pytest`, `vitest`, etc.)
- Run linters (`ruff check`, `tsc --noEmit`)
- Validate JSON/YAML files parse correctly
- Verify acceptance criteria one by one
- Check for regressions in adjacent code

**Entry criteria**: BUILD is complete — all acceptance criteria addressed.

**Exit criteria**: CI green (or equivalent local verification). Each acceptance criterion has evidence of completion.

**Hard gate**: You cannot skip PROVE. "It looks right" is not verification.

---

### DONE — Session complete

**Purpose**: Leave a breadcrumb so the next session (or agent) can pick up where you left off.

**Activities**:
- Commit with conventional commit message
- Leave a breadcrumb using the standardized format (`docs/breadcrumb-protocol.md`)
- Post the breadcrumb as an issue comment (primary) or `.breadcrumb.md` (fallback)
- Update CHANGELOG.md if appropriate
- Note any follow-up issues discovered during BUILD

**Entry criteria**: PROVE passed.

**Exit criteria**: Breadcrumb posted (issue comment or `.breadcrumb.md`). Issue updated. No uncommitted changes.

---

## Hard Gates

The lifecycle is **sequential with back-transitions**:

```
FRAME → SHAPE → BUILD → PROVE → DONE
         ↑←←←←←↓
      (back-transition allowed)
```

**Forbidden transitions**:
- FRAME → BUILD (no plan = no implementation)
- FRAME → PROVE (nothing to verify)
- SHAPE → DONE (no implementation)

**Allowed back-transitions**:
- BUILD → SHAPE (scope discovered to be wrong — reshape, don't hack)
- PROVE → BUILD (test failures require fixes)
- PROVE → SHAPE (fundamental approach is wrong — redesign)

---

## Three Lifecycle Scales

The Frame/Shape/Build/Prove lifecycle operates at the **per-task** scale. Two larger scales exist:

| Scale | Lifecycle | Unit | Cadence |
|-------|-----------|------|---------|
| **Per-task** | Frame / Shape / Build / Prove | Single issue or feature | 90–120 min session |
| **Per-PR** | Score / Rehearse / Perform | Pull request or deliverable | Days to weeks (see `docs/score-rehearse-perform.md`) |
| **Per-month** | Capture / Structure / Systematize | Portfolio-level synthesis | Monthly review cycle |

The per-task lifecycle is the atomic unit. The other scales compose from it but are defined separately.

---

## Anti-Patterns

### The Labyrinth
**Symptom**: Building without framing. Jumping into code immediately, discovering requirements mid-implementation, expanding scope continuously.
**Cure**: Enforce FRAME. Write the scope statement before touching code. If you can't write it, you don't understand the task yet.

### The Architect's Trap
**Symptom**: Shaping forever. Producing increasingly detailed plans without building anything. Paralysis by analysis.
**Cure**: Cap SHAPE at 15 minutes for standard tasks. Acceptance criteria should be 3–7 items, not 30. If the plan is longer than the implementation, it's too detailed.

### Scope Creep
**Symptom**: Building beyond the plan. "While I'm here, I might as well..." leads to half-finished tangents and bloated PRs.
**Cure**: If new work is discovered during BUILD, create a follow-up issue. Do not expand scope mid-session. Back-transition to SHAPE if the plan is genuinely wrong, but don't pretend you're reshaping when you're just adding features.

### The Vanishing Breadcrumb
**Symptom**: Session ends without documentation. No issue update, no commit message context, no record of what was tried and abandoned.
**Cure**: DONE phase is mandatory. Even a failed session gets a breadcrumb: "Attempted X, blocked by Y, recommend Z."

---

## References

- **Session Protocol**: `docs/session-protocol.md` — concrete checklist for running a session
- **Breadcrumb Protocol**: `docs/breadcrumb-protocol.md` — standardized breadcrumb format for session completion
- **WIP Limits**: `governance-rules.json` → `wip_limits` — system-wide work-in-progress constraints
- **Governance Rules**: `governance-rules.json` — Amendment E codifies this lifecycle, Amendment F mandates breadcrumbs
- **Gate Definitions**: `docs/flow-patterns/gate-definitions.yaml` — inter-organ flow gates
