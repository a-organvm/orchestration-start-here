---
session: S-energy-emission
date: 2026-03-31
supersedes: []
continues: [2026-03-31-action-ledger-plan.md]
status: active
tags: [emissions, state-changes, plans, handoff, infrastructure]
---

# Energy-Expelling State Changes + Claude Plans Handoff Infrastructure

## Context

Two structural deficits in the orchestration hub:

1. **Every state machine mutates silently.** The action ledger writes YAML but emits nothing. The contrib engine transitions targets through 5-status lifecycles, campaigns through 5 phases, absorption through 4 stages, backflow through 4 stages — all via field mutation with zero observable side effects. State changes are dark matter: they happen, but nothing in the system can detect them happening. The route graph and cycle detector are read-time analytics only. The `logger` instances exist but carry no structured state-change semantics.

2. **Plans are write-and-forget.** 11 plan files in `.claude/plans/`, no archive directory, no forward-reference protocol, no plan-to-plan continuity graph. The `CONTINUES` RouteKind exists in schemas but nothing connects plans to it. A future session must grep through all files to reconstruct context. Handoff is implicit at best.

Both deficits violate the same principle: **state changes that don't expel energy are invisible to the system's own intelligence layer.** The action ledger was designed to be the system's self-awareness — but currently, only manually-invoked CLI commands produce ledger entries. The subsystems that change state most frequently (recording, composing, transitioning) do so in silence.

---

## Part 1: State Change Emission Layer

### Design: Self-Recording State Changes

State transitions in any subsystem auto-record themselves as action ledger entries. The system watches itself. This extends the recursive proof pattern (backflow's first capture was formalizing its own rules).

### Implementation

#### 1a. `action_ledger/emissions.py` — new module

A lightweight emission protocol. Not a pub/sub bus (over-engineering). A single function that subsystems call when state changes:

```python
def emit_state_change(
    subsystem: str,       # "action_ledger", "contrib_engine", "promotion"
    verb: str,            # "closed_sequence", "advanced_phase", "promoted"
    target: str,          # the entity that changed
    from_state: str,      # prior state
    to_state: str,        # new state
    session: str = "",    # session context if available
    params: dict = None,  # additional parameter axes
) -> Action | None:
    """Record a state change as an action ledger entry.

    Returns the recorded Action, or None if ledger is unavailable.
    Emitted actions carry a `_meta:emission` param to distinguish
    them from manually recorded actions.
    """
```

This function:
- Loads the current action/sequence/param indexes
- Calls `record()` with verb, target, and a standardized params dict including `from_state`, `to_state`, and `_meta: "emission"`
- Adds a route of kind `CONTINUES` pointing at the entity being transitioned
- Saves all indexes atomically
- Returns the action (or None on failure — emissions never crash the caller)

#### 1b. Wire emissions into `action_ledger/ledger.py`

Add emission calls to:
- `close_sequence()` → emits `closed_sequence` with from_state=open, to_state=closed
- `close_session()` → emits `closed_session` with chain ID in produced
- `compose_chain()` → emits `composed_chain` with sequence count in params

These are **opt-in**: a `emit: bool = True` parameter on each function, defaulting True. CLI and tests can suppress.

#### 1c. Wire emissions into `contrib_engine/`

Add emission calls to:
- `campaign.complete_action()` → emits `completed_campaign_action`
- `monitor.py` state transitions (PR state changes) → emits `pr_state_changed`
- `absorption.py` status transitions → emits `absorption_advanced`

Same opt-in pattern.

#### 1d. `action_ledger/schemas.py` — add emission metadata

Add a `EMITTED = "emitted"` value to a new `ActionOrigin` StrEnum:
```python
class ActionOrigin(StrEnum):
    MANUAL = "manual"      # CLI-recorded
    EMITTED = "emitted"    # Auto-emitted by state change
```

Add `origin: ActionOrigin = ActionOrigin.MANUAL` field to `Action`.

### Files Modified
- `action_ledger/emissions.py` — **new** (~60 lines)
- `action_ledger/schemas.py` — add `ActionOrigin` enum + field
- `action_ledger/ledger.py` — add emission calls to close/compose functions
- `contrib_engine/campaign.py` — add emission call to `complete_action()`
- `contrib_engine/absorption.py` — add emission on status advancement
- `action_ledger/cli.py` — add `--origin` filter to `show` command

### Tests
- `tests/test_emissions.py` — **new**: verify emission creates action with correct origin, verify opt-out suppresses, verify failure doesn't crash caller
- Update existing tests to account for emitted actions in indexes

---

## Part 2: Claude Plans Handoff Infrastructure

### Design: Structured Plan Continuity

Plans get frontmatter metadata and a forward-reference protocol. The plan directory gets an archive subdirectory. An index mechanism connects plans into a traversable graph.

### Implementation

#### 2a. Plan frontmatter standard

Every plan file gets YAML frontmatter:
```yaml
---
session: S-energy-emission     # session identifier
date: 2026-03-31
supersedes: []                 # plan files this replaces
continues: []                  # plan files this builds on
status: active                 # active | completed | superseded | archived
tags: [action-ledger, emissions, infrastructure]
---
```

#### 2b. `## Forward` block protocol

Every plan ends with a `## Forward` section:
```markdown
## Forward

### Next Session Context
- What was completed
- What remains
- Critical state to preserve

### Handoff Prompt
> [Structured prompt a future session can use to resume]

### Open Questions
- Unresolved decisions carried forward
```

#### 2c. Archive directory + migration

Create `.claude/plans/archive/2026-03/` and move the 5 plans from before 2026-03-30 (the older, completed ones) into it. Active plans stay in the root.

#### 2d. Retrofit existing plans

Add frontmatter + Forward blocks to the 3 most recent active plans:
- `2026-03-31-action-ledger-plan.md`
- `2026-03-31-gravitas-culturalis.md`
- `2026-03-31-cross-session-health-audit.md`

#### 2e. Connect to action ledger

When a plan transitions status (active → completed), emit a state change via the new emission layer. Plans become first-class entities in the route graph.

### Files Modified
- `.claude/plans/archive/2026-03/` — **new directory**, 5 files moved
- `.claude/plans/2026-03-31-*.md` — frontmatter + Forward blocks added (3 files)
- `.claude/plans/dynamic-bouncing-lagoon.md` — this plan, properly formatted

---

## Verification

1. **Emission layer**: Record an action via CLI, close the sequence, verify that the close produced an emitted action in `data/actions.yaml` with `origin: emitted`
2. **Contrib emission**: Call `complete_action()` in a test, verify emission appears
3. **All existing tests pass**: `pytest tests/ -v` — 221+ tests
4. **Plan archive**: Verify moved files exist in `archive/2026-03/`, old paths are gone
5. **Plan frontmatter**: Verify all active plans have valid YAML frontmatter
6. **Forward blocks**: Verify the 3 retrofitted plans have `## Forward` sections

---

## Forward

### Next Session Context
- This plan establishes emission infrastructure + plan handoff protocol
- The emission layer is intentionally minimal — no pub/sub, no async, no external deps
- The `CONTINUES` route kind already exists in schemas and is ready to use

### Open Questions
- Should emission actions count toward cycle detection? (Probably yes — if the system keeps closing sequences in the same pattern, that's a real cycle)
- Should the plan index be a generated file (like skills lockfile) or just the archive directory structure?
