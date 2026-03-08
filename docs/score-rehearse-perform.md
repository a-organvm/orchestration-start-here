# Score / Rehearse / Perform — Per-PR Lifecycle

> **Governance**: Amendment G of `governance-rules.json`
> **Scope**: All pull requests across the eight-organ system
> **Version**: 1.0

---

## Why This Exists

The Frame/Shape/Build/Prove lifecycle governs **single sessions** (90–120 min).
But meaningful work often spans multiple sessions before it's ready to merge. Without
a per-PR lifecycle, branches accumulate silently, reviews happen on incomplete work,
and merges land without verification that the deliverable meets governance standards.

Score/Rehearse/Perform bridges the gap between session-level discipline and
merge-ready delivery. It uses the orchestra metaphor: you study the music (Score),
practice until it's right (Rehearse), then deliver it live (Perform).

---

## Phase Definitions

### SCORE — Define the deliverable before writing code

**Purpose**: Produce a micro-spec in the linked issue so that the scope, acceptance
criteria, and governance requirements are explicit before any branch is created.

**Activities**:
- Write a **1-paragraph scope statement** in the issue body or first comment
- List **3–7 acceptance criteria** (specific, testable)
- Identify the **governance gates** that apply (see checklist below)
- Estimate session count: 1 (small), 2–3 (medium), 4+ (large — consider splitting)
- Assign labels: `organ:I`–`organ:VII` or `organ:META`, plus type label

**Output**: Issue with scope, acceptance criteria, and governance gates identified.

**Exit gate**: A different person reading the issue could implement it without
asking clarifying questions. The acceptance criteria are testable.

**2-Minute Precondition Check**:
Before starting any work, verify:
1. WIP limits not exceeded (`python3 scripts/validate-wip.py`)
2. No conflicting work in the same files (check open PRs)
3. Dependencies respect the I→II→III flow (no back-edges)
4. The issue is assigned and labeled

If any precondition fails, resolve it before proceeding.

---

### REHEARSE — Branch, build, iterate until green

**Purpose**: Create the branch, implement across one or more sessions using
Frame/Shape/Build/Prove, and iterate until all acceptance criteria are met.

**Activities**:
- Create branch: `feat/<slug>`, `fix/<slug>`, or `docs/<slug>`
- Run one or more FSBP sessions (each with its own breadcrumb)
- Push regularly — CI validates on every push
- Self-review the diff before requesting review
- Run the **governance checklist** (see below) against the branch

**Governance Checklist** (run before leaving REHEARSE):

```markdown
- [ ] **Registry**: If this changes repo metadata, is registry.json updated?
- [ ] **Dependencies**: No new back-edges introduced (validate-deps.py passes)
- [ ] **Completeness**: No TBD markers, no placeholder content, no broken links
- [ ] **Stranger Test**: Would a grant reviewer seeing this PR understand it?
- [ ] **Tests**: All existing tests pass; new tests added for new behavior
- [ ] **Lint**: ruff check / tsc --noEmit / yamllint clean
- [ ] **Docs**: README, CHANGELOG, and inline docs updated as needed
- [ ] **Breadcrumbs**: Every completed session has a breadcrumb on the issue
```

**Exit gate**: All acceptance criteria met. CI green. Self-review complete.
Governance checklist passes.

---

### PERFORM — Merge, release, postmortem

**Purpose**: The final act — merge the branch, tag if needed, and leave a record
of what was delivered and what was learned.

**Activities**:
1. **Create PR** using the governance-aware PR template
2. **Final review**: Walk through the diff one more time
3. **Merge**: Squash-merge to main (preserves clean history)
4. **Tag** (if applicable): `vX.Y.Z` for code repos, `YYYY-MM-DD` for doc repos
5. **Close issue** with a final breadcrumb summarizing the full deliverable
6. **Postmortem** (30 seconds): Note one thing that went well and one to improve

**Postmortem Format** (append to the closing breadcrumb):

```markdown
**Retro:**
- (+) <what went well>
- (Δ) <what to change next time>
```

**Exit gate**: PR merged. Issue closed with breadcrumb. If tagged, release notes
exist. Postmortem noted.

---

## The Three Scales

```
┌────────────────────────────────────────────────────────┐
│  PER-MONTH: Capture / Structure / Systematize          │
│  ┌──────────────────────────────────────────────────┐  │
│  │  PER-PR: Score / Rehearse / Perform              │  │
│  │  ┌────────────────────────────────────────────┐  │  │
│  │  │  PER-TASK: Frame / Shape / Build / Prove   │  │  │
│  │  │  (90-120 min session)                      │  │  │
│  │  └────────────────────────────────────────────┘  │  │
│  │  (days to weeks — one or more sessions)          │  │
│  └──────────────────────────────────────────────────┘  │
│  (monthly portfolio synthesis)                         │
└────────────────────────────────────────────────────────┘
```

| Scale | Lifecycle | Unit | Cadence |
|-------|-----------|------|---------|
| **Per-task** | Frame / Shape / Build / Prove | Single session | 90–120 min |
| **Per-PR** | Score / Rehearse / Perform | Pull request | Days to weeks |
| **Per-month** | Capture / Structure / Systematize | Portfolio review | Monthly |

Each per-PR contains one or more per-task sessions. Each per-month contains all
per-PRs that landed that month.

---

## When to Use Each Phase

| Situation | Start At |
|-----------|----------|
| Small fix (< 1 session) | SCORE → single FSBP session in REHEARSE → PERFORM |
| Multi-session feature | SCORE → multiple FSBP sessions in REHEARSE → PERFORM |
| Hotfix / urgent bug | Abbreviated SCORE (scope in commit message) → REHEARSE → PERFORM |
| Documentation-only | SCORE → REHEARSE (no CI needed, but lint) → PERFORM |
| Governance change | Full SCORE with governance gates → REHEARSE → PERFORM with postmortem |

---

## Anti-Patterns

### The Phantom Branch
**Symptom**: Branch exists for weeks with no activity. No issue linked. No breadcrumbs.
**Cure**: Every branch must trace to an issue. Stale branches (>14 days, no commits)
should be cleaned up or explicitly parked with a breadcrumb explaining why.

### The Silent Merge
**Symptom**: PR merged without governance checklist, without breadcrumb, without
closing the linked issue.
**Cure**: PR template enforces the checklist. Closing breadcrumb is part of PERFORM.

### The Infinite Rehearsal
**Symptom**: Branch keeps growing, scope keeps expanding, never reaches PERFORM.
**Cure**: If REHEARSE exceeds the estimated session count by 2×, stop and re-SCORE.
The scope was wrong — split the issue.

### The Skipped Score
**Symptom**: Branch created before the issue has acceptance criteria. "I'll figure
it out as I go."
**Cure**: No branch without acceptance criteria. The 2-minute precondition check
catches this.

---

## References

- **Conductor Playbook**: `docs/conductor-playbook.md` — per-task lifecycle (FSBP)
- **Session Protocol**: `docs/session-protocol.md` — concrete session checklist
- **Breadcrumb Protocol**: `docs/breadcrumb-protocol.md` — session completion format
- **Governance Rules**: `governance-rules.json` — Amendment G codifies this lifecycle
- **PR Template**: `.github/PULL_REQUEST_TEMPLATE.md` — governance-aware PR form
