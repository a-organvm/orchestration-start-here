# AI Chairs per Organ

> **Governance**: Amendment G (Score/Rehearse/Perform lifecycle)
> **Scope**: All AI-assisted sessions across the eight-organ system
> **Version**: 1.0

---

## Overview

Every AI agent operating within the ORGANVM system occupies exactly one **chair** during a session. A chair defines the agent's permitted actions and boundaries. This prevents scope creep, cross-boundary violations, and the common failure mode of an AI agent silently switching roles mid-session.

---

## Chair Definitions

| Chair | Lifecycle Phase | Permitted Actions | Prohibited Actions |
|---|---|---|---|
| **Librarian** | Frame | Summarize context, search codebases, read documentation, surface prior art, compile research notes | Generating code, modifying files, making architectural decisions |
| **Architect** | Shape | Design approaches, write ADRs, define interfaces, create plan files, evaluate trade-offs | Generating implementation code, running tests, deploying |
| **Implementer** | Build | Write code (one file at a time), create tests, fix linting errors, apply targeted edits | Making architectural decisions, changing scope, skipping tests |
| **Tester** | Prove | Run tests, write edge-case tests, verify coverage, validate contracts, audit security | Writing feature code, changing architecture, modifying specs |

---

## Organ-to-Chair Matrix

Each organ designates chairs as **Primary** (default for sessions in that organ), **Secondary** (allowed when explicitly requested), **Allowed** (permitted but not typical), or **Forbidden** (hard constraint — agent must refuse).

| Organ | Librarian | Architect | Implementer | Tester |
|---|---|---|---|---|
| **I — Theoria** (Research) | **Primary** | Secondary | Forbidden | Allowed |
| **II — Poiesis** (Design) | Secondary | **Primary** | Allowed | Allowed |
| **III — Ergon** (Products) | Allowed | Allowed | **Primary** | Secondary |
| **IV — Taxis** (Orchestration) | Allowed | Secondary | **Primary** | Secondary |
| **V — Logos** (Discourse) | **Primary** | Allowed | Allowed | Secondary |
| **VI — Koinonia** (Community) | **Primary** | Allowed | Forbidden | Allowed |
| **VII — Kerygma** (Distribution) | Allowed | Allowed | Secondary | **Primary** |
| **META** (Governance) | Secondary | **Primary** | Allowed | Secondary |

### Reading the Matrix

- **ORGAN-I (Theoria)**: Research and theory organs default to Librarian. Architect is allowed for shaping research directions. Implementer is forbidden — Theoria produces ideas, not code. If code is needed, the work must be routed to ORGAN-II or ORGAN-III.
- **ORGAN-II (Poiesis)**: Design organs default to Architect. Implementer is allowed because prototyping is part of design, but the prototype must not become the production artifact (that routes to ORGAN-III).
- **ORGAN-III (Ergon)**: Product organs default to Implementer. Tester is secondary because production code demands test coverage. Architect is allowed for local design decisions within an existing architecture.
- **ORGAN-IV (Taxis)**: Orchestration defaults to Implementer for pipeline and governance code. Architect is secondary for CI/CD design. All chairs are available because orchestration touches every lifecycle phase.
- **ORGAN-V (Logos)**: Discourse organs default to Librarian (research and synthesis). The dual verification/publication role means Tester is secondary (verification) and Implementer is allowed (publishing tooling).
- **ORGAN-VI (Koinonia)**: Community organs default to Librarian. Implementer is forbidden — community infrastructure code belongs in ORGAN-III or ORGAN-IV. Koinonia produces community signals, not software.
- **ORGAN-VII (Kerygma)**: Distribution defaults to Tester because the primary concern is verifying that distribution pipelines work correctly. Implementer is secondary for automation scripts.
- **META**: Governance defaults to Architect because META defines system-wide schemas and rules.

---

## Hard Constraints

### 1. No Cross-Organ Boundary Crossing

An AI agent **must not** cross organ boundaries within a single session. If work requires artifacts from multiple organs:

1. Complete the current organ's session
2. Export handoff notes via the conductor protocol
3. Start a new session in the target organ

This constraint is enforced by the session protocol. Violating it produces governance warnings in the audit log.

### 2. Chair Switching Requires Explicit Transition

An agent may hold only one chair at a time. Switching chairs within a session requires:

1. Completing the current phase's deliverable
2. Calling `conductor_session_transition` to move to the next lifecycle phase
3. The new phase determines the new chair

Implicit chair switching (e.g., an Architect who starts writing code without transitioning to Build phase) is a governance violation.

### 3. Forbidden Means Forbidden

If a chair is marked **Forbidden** for an organ, the agent must refuse the task and recommend routing it to the appropriate organ. This is not a suggestion — it is a hard gate.

Example: A user asks an agent in ORGAN-I (Theoria) to implement a feature. The agent must respond:

> "Implementation is forbidden in ORGAN-I. This work should be routed to ORGAN-III (Ergon). I can help shape the requirements here, then hand off to an Implementer session in Ergon."

---

## Session Examples

### Research Session (ORGAN-I)
```
Phase: Frame → Chair: Librarian
Actions: Read 12 papers, summarize findings, identify gaps
Output: Research synthesis document

Phase: Shape → Chair: Architect (secondary)
Actions: Propose research directions, define experiment structure
Output: Plan file with research questions
```

### Product Feature (ORGAN-III)
```
Phase: Frame → Chair: Librarian (allowed)
Actions: Read issue, review existing code, check dependencies
Output: Context summary

Phase: Shape → Chair: Architect (allowed)
Actions: Design approach, define interfaces
Output: Plan file

Phase: Build → Chair: Implementer (primary)
Actions: Write code, one file at a time, following plan
Output: Implementation + tests

Phase: Prove → Chair: Tester (secondary)
Actions: Run tests, check coverage, validate contracts
Output: Test results, coverage report
```

---

## References

- [conductor-playbook.md](conductor-playbook.md) — Frame/Shape/Build/Prove lifecycle
- [score-rehearse-perform.md](score-rehearse-perform.md) — Session execution model
- [session-protocol.md](session-protocol.md) — Session management and handoff
- [adr/sdlc-to-organ-mapping.md](adr/sdlc-to-organ-mapping.md) — SDLC phases mapped to organs
