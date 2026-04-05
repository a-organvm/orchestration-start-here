# SOP-IV-CPP-001: Content-to-Product Pipeline

**Version:** 1.0
**Date:** 2026-04-05
**Scope:** Commerce domain (applicable to client engagements across organs)
**Lifecycle Stage:** ABSORB (proven on Sovereign Systems engagement, 2026-03-20 to 2026-04-04)
**Provenance:** Extracted from `organvm-iii-ergon/sovereign-systems--elevate-align/docs/process-extraction/2026-04-04-reusable-processes.md`

> The full journey from raw client material to organized, prioritized, specced work items on a project board with a roadmap.

---

## 1. When This Protocol Applies

Six invariant conditions, all of which must hold:

| # | Condition | Negative Test (does NOT apply) |
|---|-----------|-------------------------------|
| 1 | Client has provided raw material (conversations, documents, recordings) | Client provides a structured brief with clear requirements |
| 2 | Material must be transformed into actionable work | Material is archival or reference-only |
| 3 | A project board is the target output | Output is a single report or document, not a backlog |
| 4 | Multiple work streams exist within the material | All material feeds a single, obvious deliverable |
| 5 | Client IP may be embedded in the material | Material is purely procedural (SOWs, contracts, invoices) |
| 6 | Client decisions are required before build can proceed | Build scope is already fully defined |

If conditions 1-3 hold but 4-6 do not, use a simplified intake (Xenograft Phase 7 STRIKE directly).
If condition 1 fails (client provides a structured brief), skip to Phase 4: BOARD.

---

## 2. Protocol Phases

```
RAW CLIENT MATERIAL ARRIVES (any format, any volume)
    |
    +-- Phase 1: RECEIVE        Intake via Xenograft Protocol (SOP-IV-XGR-001)
    +-- Phase 2: PROCESS        Extract, grade, tag, verify atoms
    +-- Phase 3: ROUTE          Assign atoms to build destinations, identify IP
    +-- Phase 4: BOARD          Create issues, fill fields, link atoms
    +-- Phase 5: REPORT         Generate multi-perspective reports (SOP-IV-MPR-001)
    +-- Phase 6: DECIDE         Send to client, log decisions with dates
    +-- Phase 7: ROADMAP        Build roadmap from confirmed decisions
```

### Phase 1: RECEIVE

**Purpose:** Establish an immutable record of all client material before any transformation.

**Invariant steps:**
1. Invoke SOP-IV-XGR-001 (Xenograft Protocol), Phases 1-6
2. All 127+ files (or whatever the corpus size) pass through ARCHIVE, CONVERT, EXTRACT, ATOMIZE, VERIFY, and COVERAGE
3. The Xenograft Protocol produces the atom registry, verification report, and coverage proof
4. Confirm coverage >= 90% before proceeding. If below, re-enter Xenograft Phase 4.

**Outputs:** Atom registry (ATOM-REGISTRY-reconciled.yaml), coverage proof, verification report

**Ledger emission:** `received_client_material` with `{source, file_count, atom_count, coverage_pct}`

### Phase 2: PROCESS

**Purpose:** Grade, tag, and verify atoms for downstream routing.

**Invariant steps:**
1. GRADE every atom by quality tier:
   - **SIGNAL** — Directly actionable: motivates a strike, decision, or deliverable
   - **CONTEXT** — Supporting material: informs but does not independently motivate action
   - **NOISE** — Boilerplate, duplicates, metadata: excluded from strike planning
2. TAG each atom with the full 17-field schema (see Xenograft Appendix):
   - id, domain, type, source_file, source_section, source_line, summary
   - confidence, provenance, nature, tier, pillar, editorial
   - build_state, nodes, actionability, strike_id
3. VERIFY three ways per Xenograft Phase 5 (if not already completed in Phase 1):
   - Primary decomposer produces atom registry
   - Two independent verifiers produce blind registries
   - Reconciliation resolves agreement, partial, conflict, and novel atoms
4. Mark atoms requiring editorial review with editorial state FLAGGED (invoke SOP-IV-ETP-001)

**Outputs:** Graded and tagged atom registry with SIGNAL/CONTEXT/NOISE tiers

**Ledger emission:** `atoms_processed` with `{signal_count, context_count, noise_count, flagged_count}`

### Phase 3: ROUTE

**Purpose:** Assign every SIGNAL atom to a build destination and identify client IP.

**Invariant steps:**
1. ROUTE each SIGNAL atom to its build destination:
   - **Branch** — A website section, feature, or content pillar
   - **Pillar** — A strategic theme the atom contributes to
   - **Social** — Content suitable for social media distribution
   - **Product** — A product, course, program, or offering
2. IDENTIFY client IP by invoking SOP-IV-CIP-001 (Client IP Identification):
   - Named frameworks, unique methodologies, original terminology
   - Classify as LOCAL (client-original) or SHARED (commonly used)
3. Map atoms to the build dependency graph:
   - Which atoms block others?
   - Which atoms cluster into natural work units?
4. Update atom registry with routing metadata: `destination`, `pillar`, `ip_item` fields

**Outputs:** Routed atom registry, IP inventory, dependency map

**Ledger emission:** `atoms_routed` with `{branch_count, pillar_count, social_count, product_count, ip_items_found}`

### Phase 4: BOARD

**Purpose:** Transform routed atoms into project board issues with full field coverage.

**Invariant steps:**
1. CREATE ISSUES from SIGNAL atoms, grouped by natural work units:
   - One issue per strike (Xenograft Phase 7 STRIKE output)
   - Title follows the pattern: `[Pillar] Action: Brief Description`
   - Body contains the atom summaries, source references, and acceptance criteria
2. FILL BOARD FIELDS for every issue:
   - Status (Backlog / Ready / In Progress / Review / Done)
   - Priority (P0 Critical / P1 High / P2 Medium / P3 Low)
   - Pillar assignment
   - Estimated complexity (S / M / L / XL)
   - Dependencies (blocking/blocked-by links)
   - Atom references (which atoms this issue addresses)
3. LINK atoms to issues:
   - Every SIGNAL atom must trace to at least one issue
   - Every issue must trace to at least one atom
   - Orphan check: any SIGNAL atom without an issue is a gap; any issue without an atom is unsupported
4. Create content gap issues for areas where the atom registry reveals missing material

**Outputs:** Populated project board, atom-to-issue traceability matrix

**Ledger emission:** `board_populated` with `{issue_count, gap_count, orphan_atoms, orphan_issues}`

### Phase 5: REPORT

**Purpose:** Generate multi-perspective reports for different audiences.

**Invariant steps:**
1. Invoke SOP-IV-MPR-001 (Multi-Perspective Reporting)
2. Select applicable report types for this engagement:
   - Executive Summary (stakeholders/board)
   - Client Report (client-facing: their content analyzed for them)
   - Technical Audit (build team: architecture assessment)
   - System Health (operations: metrics and coverage)
3. Each report draws from the same atom registry but through a different lens
4. Internal review: confirm no audience-inappropriate content leaks between reports

**Outputs:** Report set (2-4 reports depending on engagement)

**Ledger emission:** `reports_generated` with `{report_types, total_pages, delivery_date}`

### Phase 6: DECIDE

**Purpose:** Present work to client for review and record every decision with a date.

**Invariant steps:**
1. SEND reports and project board to client
2. For editorial-flagged items, include the Editorial Review Document (from SOP-IV-ETP-001)
3. For each decision point, record:
   - Decision ID (DEC-NNNN)
   - Date decided
   - Decision maker
   - Choice made (from options presented)
   - Rationale (if provided)
   - Atoms affected
   - Issues affected
4. Update atom registry and issue board with decision outcomes
5. Mark issues as APPROVED, DEFERRED, or REJECTED based on decisions

**Outputs:** Decision log, updated project board

**Ledger emission:** `decisions_logged` with `{total_decisions, approved, deferred, rejected}`

### Phase 7: ROADMAP

**Purpose:** Build a time-sequenced roadmap from confirmed decisions.

**Invariant steps:**
1. From APPROVED issues, construct the dependency-ordered build sequence
2. Group into milestones based on:
   - Dependency chains (what must be built first)
   - Pillar clusters (related work done together)
   - Client priority (P0/P1 before P2/P3)
3. Assign estimated timelines to each milestone
4. Identify critical path: the longest dependency chain determines minimum timeline
5. Produce the roadmap document:
   - Milestone name, issues included, dependencies, estimated duration
   - Visual timeline (Gantt-style or sequential list)
   - Risk items: milestones with unresolved decisions or external dependencies
6. Present roadmap to client for confirmation

**Outputs:** Roadmap document, milestone plan, critical path analysis

**Ledger emission:** `roadmap_built` with `{milestone_count, total_issues, critical_path_length, estimated_duration}`

---

## 3. Outputs

| Phase | Primary Output | Format | Audience |
|-------|---------------|--------|----------|
| RECEIVE | Atom registry, coverage proof | YAML, Markdown | Internal |
| PROCESS | Graded and tagged atom registry | YAML | Internal |
| ROUTE | Routed atoms, IP inventory, dependency map | YAML, Markdown | Internal |
| BOARD | Populated project board, traceability matrix | GitHub Issues, Markdown | Internal + Client |
| REPORT | Multi-perspective report set | Markdown | Audience-specific |
| DECIDE | Decision log, updated board | YAML, GitHub Issues | Internal + Client |
| ROADMAP | Roadmap, milestone plan, critical path | Markdown | Client + Build team |

---

## 4. Failure Modes and Recovery

| Failure | Detection | Recovery |
|---------|-----------|----------|
| Xenograft coverage < 90% | Phase 1 coverage proof | Re-enter Xenograft Phase 4 with tighter atomization |
| SIGNAL/CONTEXT/NOISE ratio heavily skewed to NOISE | Phase 2 tier distribution | Review source material quality; may indicate wrong material was provided |
| Orphan atoms after board creation | Phase 4 orphan check | Create additional issues or merge orphans into existing issues |
| Client non-responsive on decisions | Phase 6 decision log stalls | Escalate with summary of blocked items and timeline impact |
| Dependency cycle in roadmap | Phase 7 critical path analysis | Break cycle by identifying which dependency is softer (preference vs. requirement) |
| Editorial flags overwhelm client | Phase 6 flagged item count > 50 | Batch flagged items by category; present highest-risk first |
| IP items contested | Phase 3 IP inventory | Defer protection recommendations; document the dispute |

---

## 5. Relationship to Existing SOPs

| SOP | Relationship | Integration Point |
|-----|-------------|-------------------|
| SOP-IV-XGR-001 (Xenograft Protocol) | Invoked by Phase 1 | Phases 1-6 of Xenograft produce the atom registry |
| SOP-IV-ETP-001 (Editorial Triage Protocol) | Invoked by Phase 2 | FLAGGED atoms routed to editorial triage |
| SOP-IV-CIP-001 (Client IP Identification) | Invoked by Phase 3 | IP inventory produced during routing |
| SOP-IV-MPR-001 (Multi-Perspective Reporting) | Invoked by Phase 5 | Report generation from shared atom data |
| `document-audit-feature-extraction` | Alternative path | Use when client provides structured docs instead of raw material |
| `styx-pipeline-traversal` | Downstream consumer | Roadmap milestones may trigger cross-organ traversal |
| `cross-agent-handoff` | Used during Phases 1-2 | Multi-model verification requires handoff envelopes |

---

## 6. Protocol Governance

- **Owner:** ORGAN-IV (Taxis)
- **Primary domain:** ORGAN-III (Ergon) client engagements
- **Invocable by:** Any organ with client-facing work
- **Versioning:** SemVer. New phases increment major. New fields or routing destinations increment minor.
- **Review cadence:** After every 3rd client engagement, review the 14-step process for adequacy and the SIGNAL/CONTEXT/NOISE thresholds for calibration.
- **Sovereign Systems instance:** 127 files, 1,821 atoms, 104 flagged, 6 IP items identified. This is the reference instance for all future engagements.
