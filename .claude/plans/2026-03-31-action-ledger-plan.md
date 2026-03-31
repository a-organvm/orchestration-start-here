---
session: S-action-ledger-recording-infrastructure
date: 2026-03-31
supersedes: []
continues: []
status: completed
tags: [action-ledger, recording, infrastructure, synthesizer-paradigm]
---

# Action Ledger — System-Wide Process Recording Infrastructure

**Date:** 2026-03-31
**Status:** COMPLETED
**Scope:** ORGAN-IV (all repos), extensible system-wide
**Conceptual Prior Art:** `organvm-ii-poiesis/alchemical-synthesizer` (Brahma Meta-Rack)

---

## Context

Every AI-assisted session produces outcomes but discards process. The ideas that drive
prompts carry implicit parameters that are in constant flux — parameters that define a
dynamic state. That state is currently invisible: it evaporates when the session ends.
Repeated cycles only become visible after they've already cost multiple sessions.
Without a recording layer, the system cannot learn from its own process, cannot detect
its own patterns, and cannot formalize its own cycles into new systems.

The user's core demand: **pause all other work until the recording infrastructure
exists.** Everything else precedes once actions have atemporal power — once they persist
beyond the session and become queryable, composable, and self-referencing regardless of
when they occurred.

### The Synthesizer Metaphor

The Alchemical Synthesizer (ORGAN-II) already embodies this architecture for audio
signals. The action ledger applies the same paradigm to ideas:

| Brahma (audio) | Action Ledger (ideas) |
|---|---|
| Module Registry — extensible named modules, each with arbitrary params | Action Registry — extensible parameter axes, any action carries whatever params it needs |
| Patch Bay — CV routing with `(src * amount * scale) + offset` | Reference system — typed connections with weight and transformation |
| CHRONOS Automation — per-track parameter lanes, values per step | Parameter trajectories — per-axis values over time |
| Euclidean Rhythms — algorithmic pattern distribution | Cycle detection — algorithmic pattern recognition |
| 7-Stage Signal Path (IA→EG→BC→AE→TE→PR→RR) | Idea lifecycle (observe→gate→bind→extract→transmute→protect→release) |

### What Exists and What's Missing

**Exists:** Fieldwork system records observations about external repos.
Campaign/outreach/backflow record domain-specific state transitions. Conductor tracks
session phases. Memory system records persistent feedback rules.

**Missing:** Nothing records THE PROCESS OF DOING — the ideas as they move through
parameter space, their composition into sequences, the sequences' snowball into chains,
the chains' accumulation into a project whole.

---

## Design

### The Atomic Unit: The Action

An action is a **semantic event** captured at state/phase transitions or parameter
changes. It records an idea at a specific point in its parameter trajectory.

Parameters are **open, not fixed** — like a synth module registers whatever params it
has, an action carries whatever parameters are relevant at the moment of capture. The
system discovers its own parameter space over time.

```yaml
actions:
- id: act-S42-0331-001
  timestamp: "2026-03-31T14:22:00"
  session: S42
  verb: explored                    # what was done
  target: fieldwork-intelligence    # what it was done to/with
  context: "understanding Layer 1 to determine reusability for meta-recording"
  params:                           # OPEN dict — any key/value pairs
    abstraction: 0.7                # present when relevant
    maturity: 0.3
    urgency: 1.0
    domain: orchestration
  produced:
    - type: insight
      ref: "fieldwork spectrum model is reusable but domain-specific"
    - type: artifact
      ref: "docs/superpowers/specs/2026-03-30-fieldwork-intelligence-system-design.md"
  sequence_id: seq-S42-001
  routes:                           # Patch bay — typed connections with weight
    - kind: consumed                # connection type
      target: "contrib_engine/fieldwork.py"
      amount: 1.0                   # influence weight (attenuverter)
    - kind: informed_by
      target: "memory://project_fieldwork_system"
      amount: 0.6
    - kind: feeds
      target: act-S42-0331-002
      amount: 1.0
```

### Parameter Registry

Like `~module_registry` in the Brahma system, the action ledger maintains a registry of
known parameter axes. Any action can introduce new axes — the registry grows as the
system discovers what it needs to track. The registry stores axis metadata:

```yaml
parameter_registry:
  abstraction:
    range: [0.0, 1.0]
    description: "0=concrete implementation, 1=pure abstraction"
    first_seen: "2026-03-31"
    frequency: 47                   # how often this axis appears
  maturity:
    range: [0.0, 1.0]
    description: "0=raw idea, 1=formalized system"
    first_seen: "2026-03-31"
    frequency: 43
  urgency:
    range: [0.0, 1.0]
    description: "0=background, 1=blocking everything"
    first_seen: "2026-03-31"
    frequency: 38
  # New axes appear as actions introduce them — no schema change required
```

### Composition Hierarchy

**Layer 0 — Actions:** Atomic semantic events. Append-only stream. Captured at state
transitions, phase changes, parameter shifts.

**Layer 1 — Sequences:** Actions grouped by shared intent. A sequence emerges when
consecutive actions serve a common purpose. Like CHRONOS tracks — each sequence is a
track with its own automation lanes.

```yaml
sequences:
- id: seq-S42-001
  session: S42
  intent: "determine if fieldwork patterns are reusable for process recording"
  actions: [act-S42-0331-001, act-S42-0331-002, act-S42-0331-003]
  automation:                       # CHRONOS-style parameter lanes
    abstraction: [0.7, 0.5, 0.4]   # descended from abstract to concrete
    maturity: [0.3, 0.3, 0.5]      # matured as understanding grew
  outcome: "fieldwork schema reusable; spectrum model generalizable"
  chain_id: chain-S42-001
```

**Layer 2 — Chains:** Sequences grouped into a complete thought-arc (a prompt-response
cycle or connected chain of prompts). Like a CHRONOS pattern — multiple tracks playing
simultaneously.

```yaml
chains:
- id: chain-S42-001
  session: S42
  prompt_essence: "build process recording infrastructure"
  sequences: [seq-S42-001, seq-S42-002, seq-S42-003]
  arc:                              # trajectory summary across all sequences
    abstraction: descended
    maturity: advanced
  produced_artifacts:
    - "docs/superpowers/specs/2026-03-31-action-ledger-design.md"
  routes:
    - kind: continues
      target: chain-S41-003         # cross-session continuity
```

**Layer 3 — Project:** All chains across all sessions for a given initiative. The
project whole. Where cycles become visible — the same automation lane patterns
repeating, the same ideas re-entering at the same maturity level, the same parameter
trajectories that never reach completion.

### Route System (Patch Bay)

Connections between actions are **typed and weighted**, like the Brahma patch bay's
`(src * amount * scale) + offset` attenuverter:

| Route Kind | Meaning | Default Amount |
|---|---|---|
| `consumed` | Action read/used this resource | 1.0 |
| `produced` | Action created this artifact | 1.0 |
| `informed_by` | Action was influenced by this source | 0.0–1.0 (how much) |
| `feeds` | Action's output routes to another action's input | 1.0 |
| `continues` | Cross-session continuity (chain → chain) | 1.0 |
| `contradicts` | Action invalidates a prior action | -1.0 |
| `refines` | Action sharpens a prior action | 0.5 |

The `amount` field captures influence weight. A `contradicts` route with amount=-1.0
inverts the prior action's contribution. This makes the reference graph not just
connective but *dynamically weighted*.

Bidirectional traversal: every route implies an inverse. If A `feeds` B, then B is
`fed_by` A. The system maintains both directions.

### Cycle Detection Engine

Pattern matching on automation lane data — like recognizing Euclidean rhythms in step
sequences:

1. **Automation lane matching:** Same parameter trajectory across sessions.
   "abstraction descended from 0.8→0.3 in S38, S40, S42 — each time restarting."
2. **Verb sequence matching:** Same verb patterns repeating.
   "explore→design→abandon→redesign appeared 3 times."
3. **Cross-session intent matching:** Same intent re-entering the system.
   "The intent 'build recording infrastructure' appeared in 4 sessions."
4. **Parameter stall detection:** An axis that stops moving signals a stuck idea.
   "maturity has been 0.4 for the last 3 sequences — something is blocking formalization."

Cycle detection **surfaces** patterns. Human decides what to formalize. The surfacing
is automatic.

### Self-Referencing Property

"Artifacts cause quickly artifact references or elsewhuse."

Every action that produces an artifact carries a forward reference to it. The system
injects a provenance marker back into the artifact:

- Action → `produced` route → artifact path (forward)
- Artifact → provenance header/comment → action ID (backward)

The graph becomes a self-referencing instrument log where you can traverse from any
artifact to the chain of ideas that produced it, and from any idea to all the artifacts
it generated.

---

## Where It Lives

```
orchestration-start-here/
├── action_ledger/                # NEW — top-level module
│   ├── __init__.py
│   ├── schemas.py                # Action, Sequence, Chain, Project, Route, ParamRegistry
│   ├── ledger.py                 # record(), load/save, compose_sequence(), compose_chain()
│   ├── routes.py                 # Patch bay — typed weighted connections, bidirectional traversal
│   ├── cycles.py                 # Cycle detection — automation lane pattern matching
│   ├── cli.py                    # CLI interface
│   └── data/
│       ├── actions.yaml          # Layer 0: append-only action stream
│       ├── sequences.yaml        # Layer 1: composed sequences
│       ├── chains.yaml           # Layer 2: thought-arc chains
│       ├── param_registry.yaml   # Known parameter axes (grows over time)
│       └── cycles.yaml           # Detected cycle patterns
├── contrib_engine/               # EXISTING — becomes a consumer of action_ledger
│   ├── fieldwork.py              # Will call ledger.record() for its own actions
│   └── ...
```

---

## Build Phases (MVP)

**Critical constraint:** Recording IS composing IS manifesting. When an action enters
the CLI, it simultaneously (1) appends to the stream, (2) auto-slots into the current
active sequence, and (3) manifests in the temporal record. These are not separate
phases of functionality — they are one atomic operation. The build phases below reflect
construction order, not runtime separation.

### Phase 1 — The Record Button (recording + composition + manifestation)
The `record()` function does THREE things atomically:
1. Append the action to the stream (`actions.yaml`)
2. Slot the action into the current active sequence (creates one if none exists)
3. Register any new parameter axes in the parameter registry

**Files:** `schemas.py`, `ledger.py`, `cli.py`, `__init__.py`
**Data:** `actions.yaml`, `sequences.yaml`, `param_registry.yaml`
**Reuses:** `fieldwork.py` load/save/append pattern, `schemas.py` Pydantic conventions,
`cli.py` dual-mode prefix registration
**Tests:** action creation, auto-sequence slotting, open params, parameter registry
growth, YAML round-trip, sequence automation lane extraction
**CLI:** `action_ledger record`, `action_ledger show`, `action_ledger sequence`

### Phase 2 — The Patch Bay (routes + provenance)
Route system: typed weighted connections, bidirectional traversal, artifact provenance.
Routes are part of the `record()` call — when an action is recorded with routes, they
are resolved and stored immediately.

**Files:** `routes.py`, extend `schemas.py` with Route model
**Tests:** route creation, bidirectional resolution, weight semantics, provenance injection
**CLI:** `action_ledger routes`, `action_ledger show --routes`

### Phase 3 — Chain Composition
Chain composition from sequences. Auto-chain on session boundaries.

**Files:** extend `ledger.py` with `compose_chain()`, `close_session()`
**Data:** `chains.yaml`
**Tests:** chain arc computation, cross-session continuity
**CLI:** `action_ledger chain`

### Phase 4 — Cycle Detection
Pattern matching on automation lanes across sessions.

**Files:** `cycles.py`
**Data:** `cycles.yaml`
**Tests:** trajectory matching, verb sequence matching, stall detection
**CLI:** `action_ledger cycles --min-recurrence N`

### Phase 5 — Integration
Wire existing systems to emit actions into the ledger.

**Modifies:** `contrib_engine/fieldwork.py`, `contrib_engine/cli.py`
**Tests:** end-to-end: fieldwork command → action appears in ledger

---

## Reusable Primitives

| Pattern | Source | Reuse |
|---|---|---|
| Append-only YAML stream | `fieldwork.py` load_fieldwork/save_fieldwork | `ledger.py` load_actions/save_actions |
| ID generation | `fo-{ws}-{MMDD}-{seq:03d}` | `act-{session}-{MMDD}-{seq:03d}` |
| Pydantic BaseModel + Field(default_factory) | `contrib_engine/schemas.py` | All schema definitions |
| CLI dual-mode prefix | `contrib_engine/cli.py` | `action_ledger/cli.py` |
| Data directory convention | `contrib_engine/data/` | `action_ledger/data/` |
| Module registry pattern | Brahma `01_module_registry.scd` | `param_registry.yaml` growth model |
| Automation lanes | Brahma `09_chronos_automation.scd` | Sequence parameter trajectories |
| Patch bay routing | Brahma `08_patch_bay.scd` | Route system with weighted connections |

---

## Verification

```bash
# Phase 1:
cd orchestration-start-here
python -m pytest tests/test_action_ledger.py -v
python -m action_ledger record --session S42 --verb explored --target fieldwork \
  --context "test" --param abstraction=0.7 --param maturity=0.3
python -m action_ledger show --session S42

# Phase 2:
python -m action_ledger show --session S42 --routes
# Verify bidirectional route resolution

# Phase 3:
python -m action_ledger sequence create --session S42 --intent "test sequence" \
  --actions act-S42-0331-001,act-S42-0331-002
python -m action_ledger sequence show seq-S42-001
# Verify automation lanes extracted from action params

# Phase 4:
# Seed test data with repeated patterns across sessions
python -m action_ledger cycles --min-recurrence 2
# Verify cycle detection output

# Phase 5:
python -m contrib_engine fieldwork record --workspace test --category tooling \
  --signal "test" --spectrum 0 --source repo_exploration
python -m action_ledger show --session current
# Verify fieldwork action appears in ledger
```

---

## Critical Files

| File | Role |
|---|---|
| `action_ledger/schemas.py` | NEW — Action, Sequence, Chain, Route, ParamAxis, ParamRegistry |
| `action_ledger/ledger.py` | NEW — record, load, save, compose |
| `action_ledger/routes.py` | NEW — patch bay, weighted connections, traversal |
| `action_ledger/cycles.py` | NEW — cycle detection engine |
| `action_ledger/cli.py` | NEW — CLI interface |
| `contrib_engine/schemas.py` | EXISTING — pattern source |
| `contrib_engine/fieldwork.py` | EXISTING — pattern source, future consumer |
| `contrib_engine/cli.py` | EXISTING — pattern source, future integration point |
| `brahma/sc/01_module_registry.scd` | REFERENCE — extensible registry pattern |
| `brahma/sc/08_patch_bay.scd` | REFERENCE — weighted routing pattern |
| `brahma/sc/09_chronos_automation.scd` | REFERENCE — automation lane pattern |

## Forward

### Next Session Context
- Phases 1-4 implemented and tested (57 tests). Phase 5 (emission layer) added in session S-energy-emission.
- The emission layer (`action_ledger/emissions.py`) makes state changes self-recording.
- Cycle detection operates on emitted actions — the system can now detect patterns in its own state transitions.

### Handoff Prompt
> Continue from action ledger Phases 1-4 + emission layer. The ledger records, composes, routes, detects cycles, and now self-records state transitions. Next work: integrate emission into the Conductor OS session lifecycle (FRAME→SHAPE→BUILD→PROVE transitions should emit). Consider whether the plan index should be a generated file or directory structure.

### Open Questions
- Fieldwork intelligence (Layer 2-4) should emit when observations are recorded
- The Conductor session lifecycle transitions need emission wiring
- Plan status transitions (active→completed) should emit — protocol defined but not yet wired
