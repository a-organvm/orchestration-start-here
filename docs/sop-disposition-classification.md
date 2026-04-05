# SOP-IV-DSC-001: Disposition Classification

**Version:** 1.0
**Date:** 2026-04-05
**Scope:** System-wide (any restructuring, migration, or org dissolution)
**Lifecycle Stage:** REP (first run performed on ORGAN-IV, 2026-04-04)
**Provenance:** Extracted from `DISSECTION.md` — ORGAN-IV Flattened Hierarchy Post-Mortem

> The process of classifying every unit's fate during structural dissolution — assigning each to
> one of five dispositions (ABSORB, PRODUCT, DISSOLVE, ARCHIVE, DELETE) and sequencing the
> execution order to minimize interference.

---

## 1. When This Protocol Applies

Five invariant conditions, all of which must hold:

| # | Condition | Negative Test (does NOT apply) |
|---|-----------|-------------------------------|
| 1 | A structural boundary is closing | Routine maintenance within a stable structure |
| 2 | Multiple units require fate decisions | Single-unit migration (use standard move) |
| 3 | Units have heterogeneous value | All units are equivalent (bulk archive or bulk delete) |
| 4 | A target structure exists or is being designed | No receiving structure — define one first |
| 5 | Contradictions between declared and actual status are suspected | All units are freshly audited and status is trusted |

If conditions 1-3 hold but 4 does not, pause and run the target structure design first.
If condition 5 fails (status is already trusted), Phase 5 (CONTRADICT) can be abbreviated but not skipped.

---

## 2. Protocol Phases

```
STRUCTURAL DISSOLUTION DECLARED (organ, org, team, project cluster)
    │
    ├── Phase 1: INVENTORY       List all units with current status + activity
    ├── Phase 2: ASSESS          Evaluate activity, uniqueness, overlap per unit
    ├── Phase 3: CLASSIFY        Assign one of 5 dispositions
    ├── Phase 4: MAP             Specify target destination for ABSORB dispositions
    ├── Phase 5: CONTRADICT      Flag status-evidence mismatches
    └── Phase 6: SEQUENCE        Order dispositions for execution
```

### Phase 1: INVENTORY

**Purpose:** Produce a complete enumeration of every unit subject to disposition, with its declared
status and observable activity level as baseline evidence.

**Invariant steps:**
1. List every unit (repo, directory, submodule, package) within the dissolving boundary
2. For each unit, record:
   - Name, path, and declared status (e.g., GRADUATED, LOCAL, CANDIDATE)
   - Size (files, LOC, or bytes — whichever is meaningful)
   - Last meaningful commit date (code changes, not ceremony)
   - Owner or primary contributor if known
3. Sort by declared status descending (GRADUATED first), then by last activity date
4. Output as a structured table or YAML manifest

**Outputs:** `disposition-inventory.md` or `disposition-inventory.yaml` — the complete unit list

**Ledger emission:** `inventory_completed` with `{boundary, unit_count, status_distribution}`

### Phase 2: ASSESS

**Purpose:** For each unit, gather the three signals that drive classification: activity recency,
content uniqueness, and overlap with other units.

**Invariant steps:**
1. For each unit in the inventory:
   - **Activity:** Is it active (commits in last 14 days), stale (14-60 days), or abandoned (>60 days)?
   - **Uniqueness:** Does it contain content, logic, or data not found elsewhere in the system?
   - **Overlap:** Does its function duplicate or substantially overlap with another unit?
2. Record the declared status vs. evidence alignment:
   - GRADUATED repo with no tests → misaligned
   - LOCAL repo with active commits → misaligned
   - ARCHIVED repo with recent commits → misaligned
3. Annotate each unit with assessment signals: `{activity, uniqueness, overlap, alignment}`

**Outputs:** Assessment annotations on each inventory entry

**Ledger emission:** `assessment_completed` with `{unit_count, active, stale, abandoned, misaligned}`

### Phase 3: CLASSIFY

**Purpose:** Assign exactly one of five dispositions to each unit based on assessment signals.

**Invariant steps:**
1. Apply the disposition decision tree:
   - **ABSORB** — Valuable content that belongs in the new structure. Active or unique, no standalone identity.
   - **PRODUCT** — Standalone value. Could be published, open-sourced, or promoted independently.
   - **DISSOLVE** — No unique value. Content already exists elsewhere or can be distributed into other units.
   - **ARCHIVE** — Historical or reference value but not active. Freeze in place, mark read-only.
   - **DELETE** — Waste. No value, no historical interest, no downstream consumers.
2. Each unit gets exactly one disposition — no "TBD" or "maybe" allowed at this phase
3. Record the reasoning for each classification (one sentence minimum)
4. Tally: `{absorb_count, product_count, dissolve_count, archive_count, delete_count}`

**Outputs:** Disposition assignments for all units

**Ledger emission:** `dispositions_assigned` with `{absorb_count, product_count, dissolve_count, archive_count, delete_count}`

### Phase 4: MAP

**Purpose:** For every ABSORB disposition, specify the exact target location in the receiving structure.

**Invariant steps:**
1. For each ABSORB unit:
   - Identify the target organ, repo, or directory in the new structure
   - Specify the path within the target (not just "goes to repo X" but "goes to repo X under src/foo/")
   - Note any transformation required (rename, restructure, merge with existing content)
2. For each PRODUCT unit:
   - Identify whether it needs a new repo, a new org, or stays in place with elevated status
3. Validate that no two ABSORB units map to the same target path without an explicit merge plan
4. Produce a cocoon map: `source_path → target_path` for every ABSORB and PRODUCT unit

**Outputs:** Cocoon mapping table — source-to-target for all non-terminal dispositions

**Ledger emission:** `cocoon_mapped` with `{absorb_mapped, product_mapped, conflicts_detected}`

### Phase 5: CONTRADICT

**Purpose:** Surface contradictions between declared status, assessment evidence, and assigned
disposition that indicate either a classification error or a governance failure.

**Invariant steps:**
1. Check each unit for contradiction patterns:
   - GRADUATED repo assigned DISSOLVE → governance promoted something without value?
   - PRODUCTION repo with no tests → quality gate failure
   - Active repo assigned ARCHIVE → why freeze something alive?
   - LOCAL repo assigned ABSORB → absorbing something never validated?
   - Flagship tier assigned DELETE → tier assignment was wrong, or deletion is wrong
2. For each contradiction, record:
   - The conflicting signals
   - Whether the contradiction invalidates the disposition (reclassify) or reveals a governance gap (document)
3. Reclassify units where contradictions invalidate the disposition
4. Document governance gaps for post-dissolution process improvement

**Outputs:** Contradiction report with resolutions or escalations

**Ledger emission:** `contradictions_resolved` with `{contradictions_found, reclassified, governance_gaps}`

### Phase 6: SEQUENCE

**Purpose:** Order the execution of dispositions to minimize interference and dependencies.

**Invariant steps:**
1. DELETE first — reduce noise, free resources, eliminate distractions
2. DISSOLVE second — distribute content to receiving units before those units move
3. ARCHIVE third — freeze historical records while references are still valid
4. ABSORB fourth — most complex, requires the target structure to be ready
5. PRODUCT last — standalone promotions after all migrations are complete
6. Within each disposition group, order by dependency (units consumed by others go first)
7. Produce the sequenced execution plan with estimated effort per step

**Outputs:** Ordered execution plan with disposition groups and dependency ordering

**Ledger emission:** `dispositions_classified` with `{absorb_count, product_count, dissolve_count, archive_count, delete_count, contradictions}`

---

## 3. Outputs

| Phase | Output | Format |
|-------|--------|--------|
| INVENTORY | Unit inventory with status and activity | Table or YAML |
| ASSESS | Assessment annotations per unit | Annotated inventory |
| CLASSIFY | Disposition assignments with reasoning | Table with rationale column |
| MAP | Cocoon mapping (source → target) | Two-column mapping table |
| CONTRADICT | Contradiction report | Issue list with resolutions |
| SEQUENCE | Ordered execution plan | Sequenced checklist |

---

## 4. Failure Modes and Recovery

| Failure | Detection | Recovery |
|---------|-----------|----------|
| Incomplete inventory (units missed) | Post-classification discovery of unmapped units | Re-run INVENTORY with broader search scope; new units enter at ASSESS |
| Disposition deadlock (unit fits two categories) | Operator cannot choose between ABSORB and PRODUCT | Apply tiebreaker: if the unit has external consumers → PRODUCT; if only internal → ABSORB |
| Cocoon conflict (two units targeting same path) | MAP phase validation catch | Design explicit merge plan or split target path |
| Contradiction cascade (>30% of units contradicted) | CONTRADICT phase count exceeds threshold | Halt — the governance model is unreliable; run a fresh audit before proceeding |
| Target structure not ready | ABSORB units have no valid destination | Pause ABSORB group; execute DELETE/DISSOLVE/ARCHIVE while target is designed |

---

## 5. Relationship to Existing SOPs

| SOP | Relationship | Integration Point |
|-----|-------------|-------------------|
| SOP-IV-XGR-001 (Xenograft Protocol) | Upstream consumer | ABSORB dispositions may trigger Xenograft for foreign material entering the new structure |
| SOP-IV-STL-001 (Staleness Mapping) | Input provider | Staleness data feeds the ASSESS phase activity signals |
| SOP-IV-CCA-001 (Ceremony Cost Accounting) | Parallel diagnostic | Ceremony overhead informs DISSOLVE decisions — high ceremony, low value → dissolve |
| SOP-IV-GID-001 (Governance Isotope Detection) | Contradiction source | Isotopes detected across dissolving units inform the CONTRADICT phase |
| Promotion & State Transitions | Governance authority | Disposition must respect promotion state — cannot DELETE a GRADUATED unit without escalation |

---

## 6. Protocol Governance

- **Owner:** ORGAN-IV (Taxis)
- **Lifecycle:** REP — needs second run on a different target to reach ABSORB
- **Next target:** ORGAN-II (Poiesis) submodule restructuring or META-ORGANVM corpus reorganization
