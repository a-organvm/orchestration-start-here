---
session: S-energy-emission
date: 2026-03-31
supersedes: []
continues: [2026-03-31-energy-emission-handoff.md]
status: active
tags: [tasks, archetypes, dispatch, cross-session]
---

# Hanging Task Archetypes — Cross-Session Dispatch Map

22 tasks across 3 workspaces, grouped into 4 archetypes.

---

## Archetype I: ORGANISM GROWTH

**What it is:** Building the third function, resolving signal defects, establishing the organism's self-documentation. The SEED's next metabolic step.

**Directory:** `~/Workspace/a-organvm`

**Character:** Builder. Follows SEED §II Procedure 1 exactly. Runs both functions at session start. Derives from need.

| ID | P | Task | Blocker |
|---|---|---|---|
| IRF-AOR-001 | P1 | Third function — close CHECK 19 cycle | None |
| IRF-AOR-004 | P1 | QUERY boundary signal declaration in signal-graph.yaml | None |
| IRF-AOR-008 | P1 | Write a-organvm CLAUDE.md | None |
| IRF-AOR-002 | P2 | Resolve DEAD_SIGNAL: TEACHING | None |
| IRF-AOR-003 | P2 | Resolve STARVED_CONSUMER: AESTHETIC | None |
| IRF-AOR-005 | P2 | TRIPTYCH framing decision (calcination vs biological) | Operator |
| IRF-AOR-006 | P2 | Register CIR-001, SIG-002, SIG-003, GEN-002 in concordance | None |
| IRF-AOR-007 | P2 | Create GH issues for S47 work on project board | None |

### Prompt: Third Function Build (P1 cluster)

```
cd ~/Workspace/a-organvm

# Session S48 — Third Embodiment

Run both functions at session start:
  python3 skeletal_define.py
  python3 circulatory_route.py

Then:

1. Fix QUERY starvation (IRF-AOR-004): add boundary signal declaration
   to signal-graph.yaml. QUERY is operator-initiated — type: EXTERNAL,
   source: operator, direction: inbound. Same pattern as pyyaml boundary.

2. Select the third function. RELAY.md S47 has candidate analysis.
   The function must:
   - Consume circulatory output (STATE or TRACE)
   - Produce something that completes the metabolic cycle (CHECK 19)
   - Be DERIVED from the most acute capability gap, not chosen for
     cycle-closure convenience
   Candidates assessed: immune--verify, nervous--propose.

3. Build following SEED §II Procedure 1, Steps 1-7.
   After function 3: CHECK 19 becomes assessable. SEED modifications unlock.

4. Write a-organvm/CLAUDE.md (IRF-AOR-008). Document:
   - What this repo is (organism instance, not a standard project)
   - Run commands (both functions, pytest)
   - SEED procedure reference
   - Session protocol (run functions at start, RELAY.md for handoff)

5. Register governance IDs in concordance (IRF-AOR-006):
   CIR-001, SIG-002, SIG-003, GEN-002

6. Create GH issues on a-organvm/a-organvm project board (IRF-AOR-007)
   for all S47 completions and S48 work.
```

### Prompt: Signal Defect Resolution (P2 cluster)

```
cd ~/Workspace/a-organvm

# After third function is built, run circulatory_route.py and examine
# the updated defect list. Then for each remaining defect:

DEAD_SIGNAL TEACHING (IRF-AOR-002):
- Which mechanism should consume TEACHING?
- Or is TEACHING a misclassification in the gate contracts?
- Check memory--remember and reproductive--generate contracts
  for what they actually produce vs what was declared.

STARVED_CONSUMER AESTHETIC (IRF-AOR-003):
- 4 functions need AESTHETIC input. Nobody produces it.
- Is this a boundary signal (operator-originated, like QUERY)?
- Or does a mechanism need to exist that generates aesthetic standards?
- Check integumentary--present and theoria--define-omega contracts.

TRIPTYCH framing (IRF-AOR-005):
- Read SEED.md Procedure 5 ("digest a predecessor") — biological frame.
- Read operator feedback: calcination, not absorption.
- Decision: which vocabulary does the portal document (TRIPTYCH.md) carry?
- Both are valid at different strata. The genome speaks biology.
  The operator speaks alchemy. The portal must choose one primary voice.
```

---

## Archetype II: TRANSMUTATION PROTOCOL

**What it is:** The exit interview / presidential handoff system. V1 artifacts testify in V2 vocabulary, V2 gates counter-testify, rectification diffs both against axioms and actuality.

**Directory:** `~/Workspace/meta-organvm/organvm-engine`

**Character:** Architect. Extends the existing interrogation.py framework. Builds the bridge between two administrations under one constitution. Gate-demand-driven (Approach C) with interrogation-powered testimony (Approach A).

| Task | Source |
|---|---|
| Write exit interview design spec | S-exit-interview brainstorm |
| Build gate contract parser (Section 1) | Spec |
| Build testimony generator (Section 2) | Spec |
| Build counter-testimony generator (V2 side) | Option 3 addition |
| Build rectification engine (Section 3) | Spec |
| Build CLI: `organvm exit-interview` (Section 4) | Spec |

### Prompt: Write Spec

```
cd ~/Workspace/meta-organvm/organvm-engine

# S-exit-interview — Design Spec

Write docs/specs/exit-interview-protocol.md (or SPEC-022).

The exit interview is A9 (Alchemical Inheritance) formalized.
Four sections, approved design:

Section 1 — Gate Contract Parser:
  Read 35 .yaml contracts from a-organvm. Extract sources mapping.
  Build demand map: for each V1 module referenced by any gate,
  which gates claim it, what signals they expect, which axiom they trace to.
  Flag orphans — V1 artifacts not claimed by any gate.

Section 2 — Testimony Generator:
  For each V1 artifact in the demand map, generate V2-native testimony
  using interrogation.py's 7 dimensions (DIAG-001→007).
  Output: testimony/{mechanism}--{artifact}.yaml
  Automated where possible (file stats, imports, tests).
  Templated where not (axiom alignment).

Section 3 — Counter-Testimony Generator (CRITICAL ADDITION):
  For each gate contract, generate counter-testimony in the SAME
  7-dimension schema. Source material: dna: and defect: sections
  already on all 33 contracts (commit 8ad586a).
  Output: counter-testimony/{mechanism}--{verb}.yaml
  The rectification diffs TWO structured documents, not one
  document against raw YAML.

Section 4 — Rectification Engine:
  Three-column verification per gate:
    testimony_claims | axiom_requires | actuality_shows
  Sources: testimony files, SEED.md 9 axioms + gate conditions,
  file existence + git blame + test results + import graph.
  Output: rectification/{mechanism}--{verb}.md
  Each report: sources covered/orphaned, claims verified/contradicted,
  gate readiness, remediation items with priority.

Section 5 — CLI:
  organvm exit-interview discover
  organvm exit-interview generate
  organvm exit-interview counter
  organvm exit-interview rectify
  organvm exit-interview plan
  organvm exit-interview full
  organvm exit-interview orphans
  Standard: --dry-run default, --write to persist, --gate, --organ.

Key files to read first:
  - src/organvm_engine/governance/interrogation.py (7 dimensions)
  - src/organvm_engine/governance/excavation.py (source analysis)
  - ~/Workspace/a-organvm/*.yaml (gate contracts)
  - ~/Workspace/a-organvm/SEED.md (9 axioms)
  - ~/Workspace/meta-organvm/post-flood/SEED.md (V2 reconstruction spec)
```

### Prompt: Build Implementation

```
cd ~/Workspace/meta-organvm/organvm-engine

# S-exit-interview-build — Implementation

Read docs/specs/exit-interview-protocol.md (or SPEC-022).

Build in src/organvm_engine/governance/:
  testimony.py        — Section 2 + Section 3 (both generators)
  rectification.py    — Section 4
  exit_interview.py   — Section 1 (parser) + orchestration

CLI in src/organvm_engine/cli/:
  exit_interview_cli.py — Section 5

Tests in tests/governance/:
  test_testimony.py
  test_rectification.py
  test_exit_interview.py

The gate contract parser reads from a configurable path
(default: ~/Workspace/a-organvm/*.yaml). The testimony
generator wraps interrogation.py's 7 dimensions but outputs
V2-native YAML. The counter-testimony generator reads dna:
and defect: sections from the same gate contracts.

Existing patterns to follow:
  - excavation.py for source analysis
  - interrogation.py for dimension framework
  - contextmd/generator.py for template-based output
  - cli/ modules for argparse registration
```

---

## Archetype III: EMISSION WIRING

**What it is:** Extending the emission layer built this session to additional subsystems. The system watches more of itself.

**Directory:** `~/Workspace/organvm-iv-taxis/orchestration-start-here`

**Character:** Electrician. Wires emit_state_change() into subsystems that currently mutate silently. Each wire-up is small, independent, testable.

| Task | P | Scope |
|---|---|---|
| Wire emission into Conductor session lifecycle | P1 | FRAME→SHAPE→BUILD→PROVE transitions |
| Wire emission into fieldwork.py | P2 | Observation recording |
| Wire emission into monitor.py PR state changes | P2 | PR state transitions |
| Fix test isolation — existing tests emit to production data | P1 | Test contamination |
| Plan status transition → emission | P2 | active→completed emits |
| Plan index: generated file vs directory structure | P2 | Design decision |

### Prompt: Emission Wiring Sprint

```
cd ~/Workspace/organvm-iv-taxis/orchestration-start-here

# S-emission-wiring — Extend emission layer

The emission infrastructure exists (action_ledger/emissions.py).
emit_state_change() is wired into:
  - action_ledger: close_sequence, compose_chain, close_session
  - contrib_engine: campaign.complete_action, absorption.mark_formalized,
    absorption.deposit_to_backflow

Still silent:

1. FIX TEST ISOLATION (P1):
   Existing tests that call close_sequence/close_session with
   default emit=True trigger real disk I/O via emit_state_change().
   The emit function loads/saves from DATA_DIR.
   Fix: add `emit=False` to all existing test calls in
   test_action_ledger.py, OR monkeypatch DATA_DIR in a
   session-scoped fixture. The emission-specific tests in
   test_emissions.py already handle this correctly.

2. Wire contrib_engine/monitor.py (P2):
   PR state changes (OPEN→MERGED, OPEN→CLOSED) should emit.
   Find the status assignment points, add emission calls
   with the same try/except pattern used in absorption.py.

3. Wire contrib_engine/fieldwork.py (P2):
   When observations are recorded, emit. The fieldwork module
   has a record() function — add emission at the end.

4. Plan status transitions (P2):
   When a plan file's frontmatter status changes
   (active→completed), emit via the emission layer.
   This connects plans to the action ledger's route graph.
   Design question: should this be manual (CLI command) or
   automatic (file watcher)? Manual is simpler and sufficient.

Run: pytest tests/ -v  (expect 233+ passing)
```

---

## Archetype IV: HOUSEKEEPING

**What it is:** Index updates, concordance entries, GitHub issues. The bureaucracy that keeps the system legible.

**Directory:** `~/Workspace/meta-organvm/organvm-corpvs-testamentvm` (IRF, concordance) + `~/Workspace/a-organvm` (GH issues)

**Character:** Registrar. No code. Pure governance bookkeeping.

| Task | Target |
|---|---|
| Register CIR-001, SIG-002, SIG-003, GEN-002 in concordance.md | concordance.md |
| Create GH issues for S47 + S-energy-emission work | a-organvm board + OSH board |
| Update IRF statistics section | IRF footer |
| Log S-energy-emission completions in IRF | IRF completed section |

### Prompt: Housekeeping Sprint

```
# Split across two directories:

## Part A: Concordance + IRF (meta-organvm)
cd ~/Workspace/meta-organvm/organvm-corpvs-testamentvm

1. Register new IDs in concordance.md:
   - CIR-001: circulatory_route.py embodiment decision
   - SIG-002: CONTRACT signal type
   - SIG-003: STATE signal type
   - GEN-002: canonical '--' maps to '_' in Python filenames

2. Add S-energy-emission completions to IRF:
   - Emission layer (action_ledger/emissions.py)
   - ActionOrigin enum (manual/emitted)
   - Plan archive + frontmatter protocol
   - 12 new tests (233 total)

3. Update IRF statistics.

## Part B: GitHub Issues (a-organvm)
cd ~/Workspace/a-organvm

Use gh CLI to create issues on a-organvm/a-organvm:
   - Third function build (IRF-AOR-001)
   - QUERY boundary signal (IRF-AOR-004)
   - CLAUDE.md for a-organvm (IRF-AOR-008)
   - Signal defect triage (IRF-AOR-002/003)
   Link to project board.

unset GITHUB_TOKEN before using gh project commands.
```

---

## Dispatch Priority

| Order | Archetype | First Task | Why First |
|---|---|---|---|
| 1 | III (Emission Wiring) | Fix test isolation | Silent data contamination — tests write to production |
| 2 | I (Organism Growth) | Third function | CHECK 19 unlocks SEED modifications |
| 3 | II (Transmutation) | Write spec | Design approved, needs formalization before build |
| 4 | IV (Housekeeping) | Concordance + IRF | Can batch with any session close |

---

## Forward

### Next Session Context
- Emission layer shipped (211c98b). Plan archive + frontmatter live.
- a-organvm at 2 functions, 49 tests, 1 INFORMATION edge.
- Exit interview design approved (A+C hybrid + counter-testimony).
- 22 tasks grouped into 4 archetypes with ready prompts.

### Handoff Prompt
> Four workstreams ready for dispatch. Emission wiring has a P1 test isolation bug. Organism growth needs the third function (CHECK 19). Transmutation protocol needs its spec written. Housekeeping can piggyback on any session close. Each archetype has a complete prompt — copy-paste into the target directory's Claude session.

### Open Questions
- Third function selection: immune--verify vs nervous--propose vs something derived from need
- TRIPTYCH framing: calcination vs biological vocabulary for the portal document
- Plan index: generated file (like skills lockfile) vs directory structure as implicit index
