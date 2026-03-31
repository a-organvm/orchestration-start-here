---
name: project_temporal_convergence
description: The action ledger (orchestration-start-here) and the dispatch ledger (tool-interaction-design) are the same system at different scales. Designed independently on consecutive days (S44 + S42). Must converge.
type: project
---

## Temporal System Convergence — Two Ledgers, One Architecture

**Discovery date:** 2026-03-31

The system built TWO recording infrastructures independently on consecutive days:

| tool-interaction-design (S44, 2026-03-30) | action_ledger (S42, 2026-03-31) |
|---|---|
| Dispatch Receipt — what was sent/returned per agent handoff | Action — semantic event at state transition |
| Timecard — punch-in/out with baseline state | Sequence — start/close with intent |
| Energy Ledger — consumed vs produced per dispatch | Parameter trajectories (automation lanes) |
| Scorecard — cumulative agent performance profiles | Cycle detection — repeated patterns across sessions |
| Prompt Patches — evolving handoff prompts from failures | Formalization — turning detected cycles into systems |
| Atomic Clock (3 clocks: Product, Conductor, Corpus) | Composition hierarchy (actions→sequences→chains→project) |
| Conductor Temporal Architecture (52 atomic actions) | The atoms the action ledger should record |

**The action ledger is the general case.** The dispatch receipt/timecard/energy/scorecard system is a specific instantiation for multi-agent fleet dispatch. Both use append-only YAML streams, both generate IDs with date-sequence patterns, both record baseline → delta patterns.

**Why this matters:** This IS the repeated cycle the user described. The idea "build a recording system" entered parameter space in S44 (as dispatch-specific recording) and re-entered in S42 (as universal recording). Without the action ledger, this cycle was invisible. The action ledger's first detected cycle should be: "the idea of recording entered twice at different scales."

**Convergence path:** The action ledger becomes the universal recording layer. The dispatch receipt becomes an action type within it. The timecard becomes sequence start/close. The energy ledger becomes a parameter axis set. The scorecard becomes cycle detection scoped to agent performance.

**Key files in tool-interaction-design:**
- `conductor/contribution_ledger.py` — dispatch receipt
- `conductor/timecard.py` — punch-in/punch-out
- `conductor/energy_ledger.py` — consumed vs produced
- `conductor/scorecard.py` — agent performance profiles
- `conductor/prompt_patches.py` — prompt evolution
- `.claude/plans/2026-03-30-conductor-temporal-architecture.md` — 52 atomic actions
- `.claude/plans/2026-03-30-corpus-temporal-architecture.md` — 21 atomic pairs

**How to apply:** Phase 5 (integration) should wire the dispatch ledger as a consumer of the action ledger, not duplicate it. The Atomic Clock's three clocks (Product, Conductor, Corpus) are three different parameter registries within the same action stream.
