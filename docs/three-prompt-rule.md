# The Three-Prompt Rule

> **Governance**: Amendment G (Score/Rehearse/Perform lifecycle)
> **Scope**: All AI-assisted conductor sessions
> **Version**: 1.0

---

## Rule

**If three prompt iterations produce unsatisfactory output, STOP generating and fix the spec.**

The problem is upstream. More prompting will not fix unclear requirements, missing context, or wrong framing. The cost of a fourth attempt exceeds the cost of restarting from Frame.

---

## Why Three

- **First attempt**: Tests the spec. If the output is wrong, the spec might be ambiguous.
- **Second attempt**: Refines the prompt. If the output is still wrong, the spec is likely incomplete.
- **Third attempt**: Confirms the pattern. If three different phrasings produce unsatisfactory results, the issue is not the prompt — it is the requirements.

A fourth attempt is sunk-cost thinking. The marginal return on each additional prompt drops sharply after three.

---

## When the Rule Fires

The Three-Prompt Rule triggers when any of these conditions are met after three iterations:

| Condition | Signal |
|---|---|
| **Vague acceptance criteria** | Output is technically correct but not what was wanted. The spec did not define "what was wanted" precisely enough. |
| **Missing edge cases** | Each iteration reveals new edge cases that weren't in the original spec. The problem space was not fully explored during Frame. |
| **Contradictory requirements** | The output satisfies one requirement but violates another. The spec contains internal contradictions. |
| **Wrong abstraction level** | The output is too detailed or too abstract. The spec did not specify the right level of granularity. |
| **Scope drift** | Each iteration adds new requirements that weren't in the original issue. The Shape phase did not define Won't items. |

---

## Response Protocol

When the Three-Prompt Rule fires:

### Step 1: Pause

Stop generating. Do not attempt a fourth prompt. Acknowledge that the problem is upstream.

### Step 2: Re-Read the Issue or Spec

Go back to the original issue, feature request, or plan file. Read it as if you've never seen it before. Identify:
- What is ambiguous?
- What is missing?
- What contradicts something else?

### Step 3: Rewrite Acceptance Criteria

Write new acceptance criteria that are:
- **Observable**: "The function returns X when given Y" (not "the function works correctly")
- **Bounded**: "Handles inputs of type A and B" (not "handles all inputs")
- **Testable**: Each criterion maps to at least one test case

### Step 4: Restart from Frame

Transition back to Frame phase. Re-gather context with the new acceptance criteria. Then proceed through Shape and Build as normal.

This is not failure — it is the system working correctly. The Three-Prompt Rule exists to prevent the far more expensive failure of shipping the wrong thing after 10 iterations.

---

## Examples

### Example 1: Vague Spec

**Issue**: "Add error handling to the ingestion pipeline"

- Prompt 1: Adds try/catch around the main function. User: "No, I meant validation errors."
- Prompt 2: Adds input validation. User: "No, I meant downstream service errors."
- Prompt 3: Adds retry logic for HTTP calls. User: "That's not what I meant either."

**Three-Prompt Rule fires.** The issue did not specify which errors, where they occur, or what "handling" means. Fix: rewrite the issue with specific error scenarios and expected behavior for each.

### Example 2: Missing Context

**Issue**: "Implement the promotion recommender"

- Prompt 1: Builds a simple rules engine. User: "It needs to check CI status."
- Prompt 2: Adds CI status check. User: "It also needs to check dependency health."
- Prompt 3: Adds dependency check. User: "And coverage thresholds, and seed.yaml validity, and..."

**Three-Prompt Rule fires.** The issue did not list the full set of promotion criteria. Each iteration discovered a new one. Fix: return to Frame, enumerate all promotion criteria from governance-rules.json, then reshape.

### Example 3: Contradictory Requirements

**Issue**: "The dashboard should be fast AND show real-time data AND work offline"

- Prompt 1: Implements SSR with caching. User: "It's not real-time."
- Prompt 2: Implements WebSocket streaming. User: "It doesn't work offline."
- Prompt 3: Implements service worker with sync. User: "It's too slow."

**Three-Prompt Rule fires.** Fast, real-time, and offline are in tension. Fix: apply MoSCoW to the three requirements — which is Must, which is Could, which is Won't?

---

## Integration with Conductor Playbook

The Three-Prompt Rule is a named heuristic referenced in the [conductor-playbook.md](conductor-playbook.md). Conductors should:

1. Track prompt iteration count during Build phase
2. When count reaches 3 without satisfactory output, invoke the rule
3. Log the trigger in session notes for retrospective analysis
4. Transition back to Frame or Shape as appropriate

The rule also reinforces [fixed-time-variable-scope.md](fixed-time-variable-scope.md): if three prompts have consumed 30+ minutes of a 90-minute session budget, cutting scope is more efficient than continuing.

---

## References

- [conductor-playbook.md](conductor-playbook.md) — Frame/Shape/Build/Prove lifecycle
- [score-rehearse-perform.md](score-rehearse-perform.md) — Session execution model
- [fixed-time-variable-scope.md](fixed-time-variable-scope.md) — Fixed-time shipping and MoSCoW prioritization
