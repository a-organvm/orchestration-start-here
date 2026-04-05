# SOP-IV-DSX-001: The Dissection Protocol

**Version:** 1.0
**Date:** 2026-04-05
**Scope:** System-wide (ORGAN-IV governs, all organs invoke)
**Lifecycle Stage:** REP (first run performed on ORGAN-IV, 2026-04-04)
**Provenance:** Meta-extracted from `DISSECTION.md` — the methodology itself, not any single finding
**Etymology:** dissecāre (Latin: to cut apart) — systematic dismemberment of a living structure to reveal its anatomy

> The complete diagnostic methodology for analyzing a multi-repo system by flattening its hierarchy, slicing across ontological domains, and grading every skeleton found — composed from 12 sub-protocols that can be invoked independently or as a coordinated sequence.

---

## 1. When This Protocol Applies

| # | Condition | Negative Test (does NOT apply) |
|---|-----------|-------------------------------|
| 1 | A bounded system exists with defined boundaries | Unbounded, continuously growing scope |
| 2 | The system has reached a transition point (dissolution, migration, restructuring, audit) | Normal operation, no structural change imminent |
| 3 | Structural truth is unknown or disputed | Architecture is well-documented and recently verified |
| 4 | Multiple stakeholders need a shared factual basis | Single operator with full mental model |
| 5 | The analysis must be reproducible, not impressionistic | Quick estimate or gut-check sufficient |

If conditions 1-3 hold but 4-5 do not, a lighter audit (single sub-protocol) may suffice.
If condition 2 fails (system is stable), use `sop-inflated-claims-audit.md` for spot-checks instead.

---

## 2. Protocol Phases

```
SYSTEM PRESENTED FOR DISSECTION (any multi-repo workspace, organ, or project cluster)
    │
    ├── Phase 1: FLATTEN        Project onto single plane (SOP-IV-FHA-001)
    ├── Phase 2: VERB           Assign essence-verbs to each unit (SOP-IV-VAP-001)
    ├── Phase 3: CROSS-CUT      Slice horizontally across domains (SOP-IV-DCA-001)
    │   ├── Lens: TIME          Activity timeline + staleness (SOP-IV-STL-001)
    │   ├── Lens: UNIVERSALS    Ceremony cost + duplication (SOP-IV-CCA-001)
    │   ├── Lens: LEDGERS       Tracking systems inventory
    │   ├── Lens: PLANS         Plan archaeology (SOP-IV-PAR-001)
    │   ├── Lens: CONTENT       Markdown density + research corpus
    │   └── Lens: BOUNDARIES    Cross-boundary references (SOP-IV-CBR-001)
    │                           + Registry caching chains (SOP-IV-RCC-001)
    │                           + Governance isotopes (SOP-IV-GID-001)
    ├── Phase 4: SKELETON       Grade all anomalies found (SOP-IV-SGS-001)
    │                           + Inflated claims audit (SOP-IV-ICA-001)
    ├── Phase 5: DISPOSE        Classify dispositions (SOP-IV-DSC-001)
    └── Phase 6: REPORT         Synthesize into deliverable dissection document
```

### Phase 1: FLATTEN

**Purpose:** Destroy the hierarchy. Project every directory, file, and hidden artifact onto a single plane where overlap and redundancy become visible.

**Invokes:** [SOP-IV-FHA-001](sop-flattened-hierarchy-audit.md) — Flattened Hierarchy Audit

**Invariant steps:**
1. Run the Flattened Hierarchy Audit on the target system
2. Produce the structural classes table (tracked/untracked/phantom)
3. Map hidden infrastructure (.atoms/, .claude/, caches, orphan artifacts)
4. Compute the declared-vs-actual structure gap

**Outputs:** Level 0 report (structural surface), directory inventory, file count matrix by language

**Ledger emission:** `dissection_flattened` with `{directory_count, file_count, gap_pct}`

### Phase 2: VERB

**Purpose:** Compress each unit to its essential action. Expose redundancy through collision and coverage gaps through absence.

**Invokes:** [SOP-IV-VAP-001](sop-verb-assignment-protocol.md) — Verb Assignment Protocol

**Invariant steps:**
1. For each unit in the flattened inventory, assign a single verb
2. Detect verb collisions (two units with same verb = redundancy signal)
3. Detect verb gaps (needed verbs no unit owns)
4. Produce the verb map with disposition hints

**Outputs:** Verb map table, collision report, gap report

**Ledger emission:** `dissection_verbed` with `{unit_count, unique_verbs, collisions, gaps}`

### Phase 3: CROSS-CUT

**Purpose:** Slice the flattened plane horizontally across ontological domains. Each domain lens reveals what vertical (per-directory) reading misses.

**Invokes:** [SOP-IV-DCA-001](sop-domain-cross-cut-analysis.md) — Domain Cross-Cut Analysis, plus domain-specific sub-protocols

**Invariant steps:**
1. Define domain lenses (minimum 6: TIME, UNIVERSALS, LEDGERS, PLANS, CONTENT, BOUNDARIES)
2. For each lens, invoke the appropriate sub-protocol:
   - **TIME:** [SOP-IV-STL-001](sop-staleness-mapping.md) — activity timeline, staleness clusters, anomalies
   - **UNIVERSALS:** [SOP-IV-CCA-001](sop-ceremony-cost-accounting.md) — ceremony files, duplication, inflation patterns
   - **LEDGERS:** Manual inventory of all tracking systems (task ledgers, registries, changelogs, code-based ledgers)
   - **PLANS:** [SOP-IV-PAR-001](sop-plan-archaeology.md) — plan directory topology, orphans, execution ratio
   - **CONTENT:** Manual analysis of markdown density, research corpus, documentation concentration
   - **BOUNDARIES:** Three sub-protocols in sequence:
     - [SOP-IV-CBR-001](sop-cross-boundary-reference-mapping.md) — data flows crossing boundaries
     - [SOP-IV-RCC-001](sop-registry-caching-chain-analysis.md) — canonical→cache chains
     - [SOP-IV-GID-001](sop-governance-isotope-detection.md) — reimplemented governance primitives
3. Collect findings per lens
4. Compare density and findings across directories

**Outputs:** Per-lens domain reports, cross-directory density comparison

**Ledger emission:** `dissection_cross_cut` with `{lens_count, findings_total, directories_with_anomalies}`

### Phase 4: SKELETON

**Purpose:** Catalogue every structural problem found across all lenses, grade by severity, and present with evidence.

**Invokes:** [SOP-IV-SGS-001](sop-severity-graded-skeleton-inventory.md) — Severity-Graded Skeleton Inventory, plus [SOP-IV-ICA-001](sop-inflated-claims-audit.md) — Inflated Claims Audit

**Invariant steps:**
1. Aggregate anomalies from Phase 3 lenses into a single candidate list
2. Run Inflated Claims Audit on all status/maturity claims
3. Grade each skeleton S1 through S5:
   - **S1 — Structural Contradictions:** Hard to fix, systemic impact
   - **S2 — Dead Weight:** Easy to fix, wasting resources
   - **S3 — Inflated Claims:** Dangerous, trust-eroding
   - **S4 — Accumulation / Drift:** Gradual, attention-requiring
   - **S5 — Missing Links:** Gaps, incomplete connections
4. Document evidence for every skeleton
5. Triage: S1 first (undermine everything), S3 next (trust), then S2/S4/S5

**Outputs:** Skeleton inventory with severity grades, evidence, and remediation recommendations

**Ledger emission:** `dissection_skeletons_graded` with `{s1, s2, s3, s4, s5, total}`

### Phase 5: DISPOSE

**Purpose:** Classify the fate of each unit based on all evidence gathered.

**Invokes:** [SOP-IV-DSC-001](sop-disposition-classification.md) — Disposition Classification

**Invariant steps:**
1. For each unit, integrate evidence from Phases 1-4:
   - Structural class (from FLATTEN)
   - Verb assignment (from VERB)
   - Staleness band (from TIME lens)
   - Skeleton grade (from SKELETON)
   - Claims status (from INFLATED CLAIMS)
2. Assign disposition: ABSORB, PRODUCT, DISSOLVE, ARCHIVE, DELETE
3. For ABSORB: specify target destination in the new structure
4. Flag contradictions (e.g., GRADUATED + S1 skeleton)
5. Sequence dispositions: DELETE → DISSOLVE → ARCHIVE → ABSORB → PRODUCT

**Outputs:** Disposition table with target mappings, contradiction flags, execution sequence

**Ledger emission:** `dissection_dispositions_assigned` with `{absorb, product, dissolve, archive, delete, contradictions}`

### Phase 6: REPORT

**Purpose:** Synthesize all findings into a single deliverable document.

**Invariant steps:**
1. Compose the Dissection Document with these sections:
   - **Level 0: Surface** — structural classes, root files, hidden infrastructure (from Phase 1)
   - **Level 1: Per-Directory Reports** — file counts, language distribution, verb map (from Phases 1-2)
   - **Level 2: Domain Cross-Cuts** — one section per lens (from Phase 3)
   - **Level 3: Skeletons** �� severity-graded inventory (from Phase 4)
   - **Appendix: Dispositions** — fate of each unit (from Phase 5)
   - **Appendix: Dependencies** — dependency files, cross-boundary map
2. Include provenance: date, auditor, companion documents
3. Cross-reference all findings to source evidence (specific files, line counts, git logs)

**Outputs:** `DISSECTION.md` — the complete post-mortem document

**Ledger emission:** `dissection_completed` with `{skeleton_count, disposition_count, document_size_bytes}`

---

## 3. Outputs

| Phase | Output | Format |
|-------|--------|--------|
| FLATTEN | Structural surface report, directory inventory | Markdown tables |
| VERB | Verb map, collision report, gap report | Markdown tables |
| CROSS-CUT | Per-lens domain reports (6+) | Markdown sections |
| SKELETON | Severity-graded inventory | Markdown tables with evidence |
| DISPOSE | Disposition table with targets | Markdown table |
| REPORT | `DISSECTION.md` | Complete markdown document |

---

## 4. Failure Modes and Recovery

| Failure | Detection | Recovery |
|---------|-----------|----------|
| Hierarchy too deep to flatten in one pass | >100 directories, >5 nesting levels | Flatten in tiers: superproject → organ → repo |
| Verb assignment deadlocked (unit defies single verb) | Multiple equally valid verbs | Assign compound verb with `/` separator, flag for split |
| Lens produces no findings | Empty results from a domain lens | Document the absence — "no ledgers found" is itself a finding |
| Skeleton count overwhelming (>50) | Triage backlog exceeds session capacity | Batch by severity: S1+S3 in current session, S2+S4+S5 deferred to IRF |
| Disposition contradictions unresolvable | ABSORB and DISSOLVE equally justified | Escalate to human. Document both arguments. |
| System changes during dissection | Git activity between phases | Snapshot (git stash/tag) at Phase 1 start. Dissect the snapshot, not the live system. |

---

## 5. Relationship to Existing SOPs

| SOP | Relationship | Integration Point |
|-----|-------------|-------------------|
| [SOP-IV-FHA-001](sop-flattened-hierarchy-audit.md) | Sub-protocol | Phase 1: FLATTEN |
| [SOP-IV-VAP-001](sop-verb-assignment-protocol.md) | Sub-protocol | Phase 2: VERB |
| [SOP-IV-DCA-001](sop-domain-cross-cut-analysis.md) | Sub-protocol | Phase 3: CROSS-CUT |
| [SOP-IV-STL-001](sop-staleness-mapping.md) | Sub-protocol | Phase 3: TIME lens |
| [SOP-IV-CCA-001](sop-ceremony-cost-accounting.md) | Sub-protocol | Phase 3: UNIVERSALS lens |
| [SOP-IV-PAR-001](sop-plan-archaeology.md) | Sub-protocol | Phase 3: PLANS lens |
| [SOP-IV-CBR-001](sop-cross-boundary-reference-mapping.md) | Sub-protocol | Phase 3: BOUNDARIES lens |
| [SOP-IV-RCC-001](sop-registry-caching-chain-analysis.md) | Sub-protocol | Phase 3: BOUNDARIES lens |
| [SOP-IV-GID-001](sop-governance-isotope-detection.md) | Sub-protocol | Phase 3: BOUNDARIES lens |
| [SOP-IV-SGS-001](sop-severity-graded-skeleton-inventory.md) | Sub-protocol | Phase 4: SKELETON |
| [SOP-IV-ICA-001](sop-inflated-claims-audit.md) | Sub-protocol | Phase 4: SKELETON |
| [SOP-IV-DSC-001](sop-disposition-classification.md) | Sub-protocol | Phase 5: DISPOSE |
| [SOP-IV-XGR-001](sop-xenograft-protocol.md) | Inverse | Xenograft ingests foreign material IN; Dissection analyzes existing material OUT |
| `superproject-topology-audit.md` | Predecessor | The topology audit was Phase 1 before the other phases existed |

---

## 6. Protocol Governance

- **Owner:** ORGAN-IV (Taxis)
- **Invocable by:** Any organ (though most commonly invoked during organ transitions or system audits)
- **Lifecycle:** REP → needs second run on a different target to reach ABSORB
- **Next target:** META-ORGANVM or ORGAN-II (both have multi-repo structure suitable for dissection)
- **Versioning:** SemVer. New sub-protocols added as minor versions. Changes to phase ordering are major versions.
- **Review cadence:** After every dissection, review sub-protocol adequacy — did any lens produce nothing? Did any phase feel missing?

---

## 7. The Genus-Species Relationship

This protocol is the **genus**. The 12 sub-protocols are **species** — each can be invoked independently for targeted diagnosis, or composed together for full dissection.

| Invocation | What You Get |
|------------|-------------|
| Full Dissection (all 6 phases) | Complete structural post-mortem with dispositions |
| Phases 1-2 only (FLATTEN + VERB) | Quick structural overview with essence mapping |
| Phase 3 single lens (e.g., TIME only) | Focused domain analysis (staleness mapping) |
| Phase 4 only (SKELETON) | Anomaly scan against existing knowledge |
| Any single sub-protocol | Standalone diagnostic (e.g., run SOP-IV-CCA-001 for ceremony cost check) |

The sub-protocols maintain no dependencies on each other except:
- Phase 2 (VERB) requires Phase 1 (FLATTEN) output as input
- Phase 4 (SKELETON) aggregates Phase 3 (CROSS-CUT) findings
- Phase 5 (DISPOSE) integrates all prior phases
- Phase 6 (REPORT) composes all prior outputs

Phases 1 and 3 (and all sub-protocols within Phase 3) can run in parallel.
