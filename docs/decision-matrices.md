# Decision Matrices for Critical Junctures

> **Governance**: Amendment G (Score/Rehearse/Perform lifecycle)
> **Scope**: All conductor-led sessions across the eight-organ system
> **Version**: 1.0

---

## Purpose

Conductors commonly get stuck at four junctures: starting a feature, choosing an approach, debugging, and shipping. These matrices provide structured decision-making for each, with a **default action** when analysis paralysis sets in.

Each matrix follows the same structure:
- **Inputs**: What information you have
- **Options**: What you can do
- **Criteria**: How to choose between options
- **Default**: What to do if you're still unsure after 5 minutes of deliberation

---

## Matrix 1: Starting a Feature

*When: A feature issue exists and you're deciding whether to begin work now.*

### Inputs

| Input | Where to Find It |
|---|---|
| Issue or backlog item | GitHub Issues, FEATURE-BACKLOG.md |
| Backlog position | Priority ranking in FEATURE-BACKLOG.md |
| Dependencies | `seed.yaml` consumes edges, issue cross-references |
| Current WIP count | Active sessions and open PRs |
| Spec quality | Acceptance criteria in the issue |

### Decision Table

| Condition | Action |
|---|---|
| Dependencies unresolved (blocked by another issue) | **Defer** — work on unblocked items first |
| WIP limit reached (3+ active sessions) | **Defer** — finish existing work before starting new |
| Spec has no acceptance criteria | **Park** — add acceptance criteria, then reassess |
| Spec has acceptance criteria but feels too large | **Split** — break into 2-3 smaller issues with own acceptance criteria |
| Dependencies clear, WIP under limit, spec is solid | **Start now** — open a conductor session |

### Default

**If unsure, split.** Splitting a feature into smaller pieces is almost never wrong. It clarifies scope, reduces risk, and makes each piece easier to estimate. The cost of splitting too much (extra issues, minor overhead) is far lower than the cost of starting something too large.

---

## Matrix 2: Choosing an Approach

*When: You're in Shape phase and need to decide how to implement a feature.*

### Inputs

| Input | Where to Find It |
|---|---|
| Spec / acceptance criteria | Issue body, plan file |
| Existing codebase | Grep, read, explore during Frame |
| Constraints (time, complexity, dependencies) | Session budget, tier requirements, seed.yaml |
| Test coverage of affected area | Coverage reports, CI output |

### Decision Table

| Condition | Action |
|---|---|
| No existing code in this area | **Green field** — design from scratch, write interfaces first |
| Existing code is well-tested (>70% coverage) and the change is additive | **Extend** — add to existing code without restructuring |
| Existing code is poorly tested or tightly coupled | **Refactor** — improve structure first, then add feature |
| Requirements are ambiguous or the domain is unfamiliar | **Spike** — time-boxed exploration (30 min max), then decide |
| Multiple viable approaches and you can't choose | **Spike** — prototype the riskiest part of each approach |

### Default

**If unsure, spike first.** A 30-minute spike costs less than 2 hours of implementing the wrong approach. The spike must be time-boxed and disposable — its only output is a decision about which approach to take.

Spike deliverable: a short note (3-5 sentences) explaining what you tried, what you learned, and which approach you're choosing. This goes in the plan file.

---

## Matrix 3: Debugging

*When: Something is failing and you need to fix it.*

### Inputs

| Input | Where to Find It |
|---|---|
| Failing test or error message | CI output, terminal, test runner |
| Error log or stack trace | Application logs, pytest output |
| Reproduction steps | Test case, manual steps |
| Time already spent debugging | Session clock |

### Decision Table

| Condition | Action |
|---|---|
| Error message is clear and points to a specific line | **Read the error** — fix the obvious issue |
| Error is intermittent or non-obvious | **Add logging** — instrument the code path, reproduce, read logs |
| Error appeared after a specific change | **Bisect** — git bisect or manual binary search through recent changes |
| You understand the problem but not the fix | **Ask AI** — describe the problem precisely, include error and context |
| You've spent >15 minutes and have no hypothesis | **Revert** — undo recent changes, verify the baseline works, re-apply changes one at a time |
| You've spent >30 minutes total | **Revert and retry** — see escalation below |

### Default

**If >30 minutes, revert and retry.** Debugging has diminishing returns after 30 minutes on the same issue. Revert to the last known good state, re-read the spec, and try a different approach. This is not failure — it is the fixed-time principle applied to debugging.

### Escalation

If reverting and retrying also fails:
1. Document what you've tried (approaches, hypotheses, results)
2. Create an issue with the debugging notes
3. Move to the next backlog item
4. Return with fresh eyes (next session or next day)

---

## Matrix 4: Shipping

*When: Build is complete and you're deciding whether to merge.*

### Inputs

| Input | Where to Find It |
|---|---|
| Test results | CI output, local test runner |
| CI status | GitHub Actions, CI dashboard |
| Documentation updated | README, CHANGELOG, inline docs |
| Governance checklist | See below |

### Governance Checklist

Before merging, verify:

- [ ] All Must items from the plan are implemented
- [ ] Tests pass locally and in CI
- [ ] No new lint or type errors
- [ ] `seed.yaml` is unchanged or updated intentionally
- [ ] No back-edge dependencies introduced (check with `validate-deps.py`)
- [ ] Coverage has not decreased (for flagship/standard tiers)
- [ ] CHANGELOG updated (if applicable)
- [ ] Commit messages follow conventional format

### Decision Table

| Condition | Action |
|---|---|
| All checklist items pass, low-risk change | **Merge** — squash-merge to main |
| All checklist items pass, high-risk change (flagship, cross-organ) | **Request review** — assign a reviewer, wait for approval |
| Some checklist items fail but are non-blocking | **Defer** — fix the failing items, then re-evaluate |
| Tests pass but coverage dropped significantly | **Split PR** — separate the coverage regression from the feature |
| Unsure about risk level | **Defer** — sleep on it, merge tomorrow if it still looks good |

### Default

**If the governance checklist is incomplete, defer.** Shipping with incomplete governance checks creates technical debt that compounds. The cost of deferring one day is nearly zero. The cost of shipping a governance violation can cascade across the system.

---

## Using These Matrices

These matrices are decision aids, not decision makers. They encode common patterns observed across hundreds of conductor sessions. Use them when:

1. You're stuck at a juncture for more than 5 minutes
2. You're tempted to skip a step (the matrix will remind you why it exists)
3. You're onboarding and need to learn the system's decision culture

The defaults are deliberately conservative. They favor caution over speed because the system optimizes for sustainable throughput, not peak velocity.

---

## References

- [conductor-playbook.md](conductor-playbook.md) — Frame/Shape/Build/Prove lifecycle
- [fixed-time-variable-scope.md](fixed-time-variable-scope.md) — Time budgets and MoSCoW prioritization
- [three-prompt-rule.md](three-prompt-rule.md) — When to stop generating and fix the spec
- [tier-based-testing-matrix.md](tier-based-testing-matrix.md) — Testing requirements by repo tier
- [branching-strategy.md](branching-strategy.md) — Branch naming and merge strategy
