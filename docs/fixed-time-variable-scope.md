# Fixed-Time, Variable-Scope Shipping

> **Governance**: Amendment G (Score/Rehearse/Perform lifecycle)
> **Scope**: All planned work across the eight-organ system
> **Version**: 1.0

---

## Principle

**Fix the deadline. Flex the scope.**

Every unit of work in ORGANVM operates under a time constraint, not a scope constraint. When time runs out, the remaining scope is cut — never the other way around. This is adapted from Shape Up's "appetite" concept: you decide how much time a piece of work is worth *before* you start, and the work must fit within that budget.

---

## Time Budgets

| Unit | Duration | Use Case |
|---|---|---|
| **Session** | 90-120 minutes | Single conductor session (Frame through Prove) |
| **Sprint** | 1-2 weeks | Feature cycle across one or more sessions |
| **Season** | 6-8 weeks | Strategic planning cycle aligned to system goals |

### Session Budget

A conductor session is the atomic unit of work. The 90-120 minute budget includes all four lifecycle phases:

| Phase | Budget Share | Notes |
|---|---|---|
| Frame | ~15% (15-20 min) | Context gathering, issue review, dependency check |
| Shape | ~20% (20-25 min) | Approach design, plan file creation, scope definition |
| Build | ~45% (40-55 min) | Implementation, one file at a time |
| Prove | ~20% (20-25 min) | Testing, verification, governance checks |

If Frame takes longer than 20 minutes, the scope is too large. Split the work.

---

## MoSCoW Prioritization

Every feature, issue, or session plan must declare MoSCoW priorities **before Build phase begins**. This is not optional — it is a Shape phase deliverable.

| Priority | Meaning | Example |
|---|---|---|
| **Must** | Without this, the deliverable is broken or useless | Core function works, tests pass, seed.yaml valid |
| **Should** | Important but the deliverable is viable without it | Error messages are helpful, edge cases handled |
| **Could** | Nice to have if time permits | Additional test coverage, polish, documentation |
| **Won't** | Explicitly excluded from this session/sprint | See below |

### The Won't List

The Won't list is the most important artifact of the Shape phase. It defines the boundary of the work. Without it, scope creep is inevitable.

**Every plan file must include a Won't section.** If a plan has zero Won't items, the scope is undefined and the session must not proceed to Build.

Good Won't items are specific and tempting:
- "Won't add CLI flags for optional features (defer to F-34)"
- "Won't handle the edge case where both inputs are empty (tracked in #45)"
- "Won't refactor the existing test suite (separate session)"

Bad Won't items are vague and obvious:
- "Won't rewrite the whole system" (too broad to be useful)
- "Won't add unrelated features" (says nothing)

---

## Cool-Down Periods

### Post-Session Review (5-10 minutes)

After every session, before starting the next:
1. Review what was shipped vs. what was planned
2. Move unfinished Could items to the backlog
3. Note any scope that crept in despite the Won't list

### Weekly Reflection (30 minutes)

Once per week:
1. Review all sessions from the past week
2. Identify patterns: which estimates were wrong? Which Won't items kept reappearing?
3. Adjust time budgets for recurring work types

### Seasonal Rhythm (half-day)

Every 6-8 weeks:
1. Review the feature backlog against system goals
2. Retire stale items (>3 months without activity)
3. Set appetite for the next season's priorities
4. Update the FEATURE-BACKLOG.md with new priorities

---

## Anti-Patterns

### 1. Scope Creep Disguised as Quick Fixes

**Symptom**: "While I'm in here, let me also fix this small thing..."

**Why it's dangerous**: Small fixes compound. Three "quick" changes during Build phase consume 30 minutes and displace the Must items.

**Remedy**: If it's not on the Must/Should list, create an issue and move on. The Three-Prompt Rule (see [three-prompt-rule.md](three-prompt-rule.md)) provides an additional guardrail.

### 2. Infinite Polish

**Symptom**: Spending 40 minutes in Prove phase refining error messages, adding comments, improving variable names.

**Why it's dangerous**: Polish is unbounded. There is always one more thing to improve.

**Remedy**: Polish is a Could item. When the time budget for Prove is spent, stop. Ship what passes tests and governance checks.

### 3. Feature Additions During Prove Phase

**Symptom**: "The tests revealed that we also need to handle X."

**Why it's dangerous**: Prove phase discovers gaps, but filling them belongs in a new Build phase (which means a new session if time is up).

**Remedy**: Log the gap as a new issue. If it's critical (the feature is broken without it), it should have been a Must item — which means the Shape phase missed it. Apply the Three-Prompt Rule: fix the spec, not the code.

### 4. Skipping the Won't List

**Symptom**: Plan file has Must and Should items but no Won't section.

**Why it's dangerous**: Without explicit exclusions, everything is implicitly in scope. The session will overrun.

**Remedy**: Hard gate: the conductor must refuse to transition from Shape to Build without at least 3 Won't items in the plan.

### 5. Extending the Deadline Instead of Cutting Scope

**Symptom**: "We're almost done, let me just spend another 30 minutes."

**Why it's dangerous**: This inverts the core principle. If the deadline moves, fixed-time shipping is meaningless.

**Remedy**: When time is up, ship what's done. Unfinished work becomes the first Must item in the next session.

---

## Integration with Frame/Shape/Build/Prove

| Lifecycle Phase | Fixed-Time Contribution |
|---|---|
| **Frame** | Assess appetite: is this worth a session, a sprint, or a season? |
| **Shape** | Define MoSCoW priorities and the Won't list. Set the time budget. |
| **Build** | Execute Must items first, then Should, then Could. Stop when time is up. |
| **Prove** | Verify Must items pass. Log gaps as issues. Do not extend. |

---

## References

- [conductor-playbook.md](conductor-playbook.md) — Frame/Shape/Build/Prove lifecycle
- [score-rehearse-perform.md](score-rehearse-perform.md) — Session execution model
- [three-prompt-rule.md](three-prompt-rule.md) — When to stop generating and fix the spec
- [decision-matrices.md](decision-matrices.md) — Decision frameworks for common junctures
