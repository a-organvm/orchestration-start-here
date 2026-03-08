# ADR-003: SDLC-to-Organ Mapping

> **Governance**: Article II (Dependency Flow), Article VI (Promotion State Machine)
> **Scope**: All organs across the eight-organ system
> **Status**: Accepted
> **Date**: 2026-03-08

---

## Context

The ORGANVM system partitions creative-institutional work across eight organs, each with distinct responsibilities. Traditional software development follows a linear or iterative Software Development Life Cycle (SDLC). To ensure that ORGANVM governance aligns with industry-standard development practices, we need an explicit mapping from canonical SDLC phases to the organ responsible for each.

Without this mapping, contributors default to treating each organ as a mini-SDLC, duplicating responsibilities and creating ambiguity about where requirements analysis ends and implementation begins.

### Decision Drivers

- Article II requires unidirectional dependency flow: `I -> II -> III`. Mapping SDLC phases must respect this constraint.
- Each organ already has an implicit SDLC affinity. Making it explicit reduces routing errors.
- AI agents operating within the conductor model need clear phase-to-organ routing to avoid cross-boundary violations.

---

## Decision

Map canonical SDLC phases to ORGANVM organs as follows:

| SDLC Phase | Organ | Rationale |
|---|---|---|
| **Requirements & Research** | ORGAN-I (Theoria) | Foundational theory, recursive engines, symbolic computing. All requirements originate here as research artifacts. |
| **Design & Prototyping** | ORGAN-II (Poiesis) | Generative art, performance systems, creative coding. Translates research into tangible prototypes and design explorations. |
| **Implementation** | ORGAN-III (Ergon) | Commercial products, SaaS tools, developer utilities. Production-grade code lives here. |
| **Orchestration & CI/CD** | ORGAN-IV (Taxis) | Governance, pipelines, agent orchestration. Owns the build/deploy infrastructure and promotion state machine. |
| **Verification & Documentation** | ORGAN-V (Logos) | Public discourse, essays, editorial, analytics. Dual role: verifies output quality AND publishes discourse about it. |
| **Feedback & Validation** | ORGAN-VI (Koinonia) | Community, reading groups, salons, learning. User feedback loops and community-driven validation. |
| **Deployment & Distribution** | ORGAN-VII (Kerygma) | POSSE distribution, social automation, announcements. Final-mile delivery to audiences. |
| **Cross-Organ Governance** | META | Schemas, dashboard, registry, system-wide metrics. Operates outside the SDLC flow as the meta-layer. |

### Phase Flow Diagram

```
Requirements    Design      Implementation    CI/CD         Verification    Feedback      Distribution
(ORGAN-I)  -->  (ORGAN-II)  -->  (ORGAN-III)  -->  (ORGAN-IV)  -->  (ORGAN-V)  -->  (ORGAN-VI)  -->  (ORGAN-VII)
  Theoria         Poiesis         Ergon             Taxis           Logos          Koinonia        Kerygma
                                                      |
                                                    META (governance overlay)
```

### Dual-Role Tension: ORGAN-V (Logos)

Logos occupies a unique position: it both **verifies** outputs from upstream organs (quality gate) and **publishes** its own discourse (essays, editorials). This creates tension:

- **As Verifier**: Logos reads from ORGAN-III and ORGAN-IV, produces verification reports, and gates promotion decisions. It is a consumer in the dependency graph.
- **As Publisher**: Logos produces essays and analytics that flow downstream to ORGAN-VI (community discussion) and ORGAN-VII (distribution). It is a producer.

This dual role is intentional. Verification and discourse are two sides of the same intellectual act: understanding something well enough to explain it publicly. The constraint is that verification artifacts (test reports, audit logs) must remain separable from editorial artifacts (essays, analyses).

### META as Governance Overlay

META does not map to a single SDLC phase. It operates as a cross-cutting governance layer:

- **Registry** (`registry-v2.json`): single source of truth for all repos
- **Schemas**: `seed.yaml` schema, event catalog, organ-aesthetic definitions
- **Dashboard**: system-wide health metrics and promotion pipeline visualization
- **Governance rules**: dependency validation, promotion constraints

META touches every phase but owns none. It is the referee, not a player.

---

## Consequences

### Positive

- **Clear routing**: When an issue arrives, its SDLC phase determines which organ owns it. No ambiguity.
- **Dependency validation**: `validate-deps.py` can now flag violations where a repo claims an SDLC phase inconsistent with its organ membership.
- **AI agent scoping**: Conductor sessions can be validated against this mapping — an agent working in ORGAN-I should not be generating production code (that belongs in ORGAN-III).

### Negative

- **Rigidity**: Some work naturally spans phases (e.g., a spike that starts as research but produces a working prototype). The mapping requires explicit handoff between organs rather than fluid exploration.
- **Logos complexity**: The dual-role tension means Logos requires more nuanced governance rules than other organs.

### Neutral

- This ADR codifies existing practice rather than introducing new behavior. The organs were already implicitly aligned to these phases.

---

## References

- [governance-rules.json](../../governance-rules.json) — Articles I, II, VI
- [branching-strategy.md](../branching-strategy.md)
- [conductor-playbook.md](../conductor-playbook.md) — Frame/Shape/Build/Prove lifecycle
- [score-rehearse-perform.md](../score-rehearse-perform.md)
- [seed-schema/](../seed-schema/) — `seed.yaml` contract definitions
