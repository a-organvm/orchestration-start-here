# SOP-IV-GID-001: Governance Isotope Detection

**Version:** 1.0
**Date:** 2026-04-05
**Scope:** System-wide (any system where governance rules are consumed across boundaries)
**Lifecycle Stage:** REP (first run performed on ORGAN-IV, 2026-04-04)
**Provenance:** Extracted from `DISSECTION.md` — ORGAN-IV Flattened Hierarchy Post-Mortem
**Etymology:** Isotope — same element (governance concept), different atomic weight (implementation).
Governance primitives reimplemented across locations with varying fidelity, like isotopes of the
same element that behave similarly but decay differently under stress.

> The process of identifying governance primitives that have been independently reimplemented
> in multiple locations, comparing their compatibility, classifying each instance by its
> relationship to the canonical source, and recommending consolidation to eliminate silent
> contradictions.

---

## 1. When This Protocol Applies

Five invariant conditions, all of which must hold:

| # | Condition | Negative Test (does NOT apply) |
|---|-----------|-------------------------------|
| 1 | Governance rules exist and are codified | Governance is informal/oral — codify first |
| 2 | Multiple consumers of the same governance rules exist | Single consumer — no isotope formation possible |
| 3 | Consumers are separated by repo, org, or deployment boundaries | All consumers share a single source file with no copies |
| 4 | Governance rules have been stable long enough for drift to accumulate | Rules were just created — no drift window yet |
| 5 | Silent contradictions are suspected or possible | All copies are known to be generated from a single template with verified sync |

If conditions 1-4 hold but 5 does not (verified sync exists), run Phase 3 (COMPARE) as a
validation check — the sync mechanism itself may have bugs that allow silent drift.

---

## 2. Protocol Phases

```
GOVERNANCE CONTRADICTION SUSPECTED (conflicting behavior, inconsistent state transitions,
                                    "but the other file says...")
    │
    ├── Phase 1: IDENTIFY        List the governance primitives in the system
    ├── Phase 2: SEARCH          Find all implementations of each primitive
    ├── Phase 3: COMPARE         Assess compatibility between implementations
    ├── Phase 4: CLASSIFY        Label each implementation by relationship to canonical
    └── Phase 5: CONSOLIDATE     Recommend resolution for non-canonical instances
```

### Phase 1: IDENTIFY

**Purpose:** Enumerate the governance primitives — the atomic concepts, rules, state machines, and
data structures that constitute the system's governance layer.

**Invariant steps:**
1. List every governance primitive by category:
   - **State machines:** promotion states (LOCAL → CANDIDATE → PUBLIC_PROCESS → GRADUATED → ARCHIVED),
     agent lifecycle states, content pipeline stages
   - **Taxonomies:** organ map (I-VII + META), tier hierarchy (flagship/standard/infrastructure),
     disposition categories
   - **Rules:** dependency direction constraints (I→II→III only), promotion prerequisites,
     naming conventions
   - **Registries:** repo registry, agent registry, skill registry, entity registry
   - **Network maps:** organ-to-org mapping, inter-organ edge definitions, event catalogs
2. For each primitive, identify its expected canonical location (the file/module that should be
   authoritative)
3. Record the primitive's signature — the identifiers that make it searchable:
   - State names (e.g., `GRADUATED`, `CANDIDATE`)
   - Config keys (e.g., `promotion_status`, `organ_map`)
   - Class/function names (e.g., `PromotionState`, `validate_deps`)
   - File patterns (e.g., `governance-rules.json`, `registry*.json`)

**Outputs:** Governance primitive inventory with canonical locations and search signatures

**Ledger emission:** `primitives_identified` with `{primitive_count, state_machines, taxonomies, rules, registries, network_maps}`

### Phase 2: SEARCH

**Purpose:** For each governance primitive, find every implementation across the entire codebase —
every file, module, config, or documentation that encodes or references the primitive.

**Invariant steps:**
1. For each primitive's search signatures:
   - Grep across all repos/directories for state names, config keys, class names, file patterns
   - Search documentation (CLAUDE.md, AGENTS.md, README.md) for narrative references to the primitive
   - Search code (Python, TypeScript, YAML, JSON) for programmatic implementations
   - Search CI/CD configs for enforcement references
2. For each match, record:
   - `{primitive, location (file path), implementation_type (code/config/doc/ci), snippet}`
3. Deduplicate: if a file both documents and enforces a primitive, record both roles
4. Count implementations per primitive — primitives with count=1 are safe (single source of truth);
   count>1 are isotope candidates

**Outputs:** Implementation map — all locations where each primitive is encoded

**Ledger emission:** `implementations_searched` with `{primitive_count, total_implementations, single_source, multi_source}`

### Phase 3: COMPARE

**Purpose:** For each primitive with multiple implementations, determine whether the implementations
agree — same states, same rules, same structure — or have diverged.

**Invariant steps:**
1. For each multi-source primitive, compare all implementations pairwise:
   - **State machines:** Do they have the same states? Same transitions? Same terminal states?
   - **Taxonomies:** Do they have the same categories? Same hierarchy? Same membership?
   - **Rules:** Do they enforce the same constraints? Same exceptions? Same error handling?
   - **Registries:** Do they list the same entries? Same schema? Same update frequency?
   - **Network maps:** Do they show the same edges? Same directions? Same weights?
2. Classify each comparison result:
   - **Identical:** Byte-for-byte or semantically equivalent
   - **Compatible:** Different representation but same meaning (e.g., JSON vs. YAML encoding)
   - **Subset:** One implementation is a strict subset of another (missing states/entries)
   - **Divergent:** Implementations disagree on specific values or rules
   - **Contradictory:** Implementations make mutually exclusive assertions
3. For divergent/contradictory pairs, document the specific disagreement with evidence from both files

**Outputs:** Compatibility matrix for each multi-source primitive with comparison results

**Ledger emission:** `implementations_compared` with `{primitive_count, identical_pairs, compatible_pairs, subset_pairs, divergent_pairs, contradictory_pairs}`

### Phase 4: CLASSIFY

**Purpose:** Assign each implementation instance one of four labels describing its relationship
to the authoritative source.

**Invariant steps:**
1. For each implementation of each primitive, assign exactly one label:
   - **CANONICAL** — The authoritative source. There must be exactly one per primitive.
     If two candidates compete for canonical status, escalate to governance owner.
   - **CACHE** — An intentional copy made for performance, locality, or offline access.
     Expected to drift; should have a freshness mechanism (sync script, CI check, hash comparison).
   - **ISOTOPE** — An independent reimplementation that encodes the same concept with different
     structure. Similar behavior under normal conditions but may diverge under edge cases.
     The implementer may not have known the canonical source existed.
   - **INCOMPATIBLE** — Actively contradicts the canonical source. Cannot coexist without one
     producing incorrect behavior.
2. Validate: exactly one CANONICAL per primitive. If zero → the primitive has no authority
   (governance gap). If more than one → authority is disputed (governance conflict).
3. For each CACHE: does a sync mechanism exist? Record its type and last-sync evidence.
4. For each ISOTOPE: was the reimplementation intentional (documented reason) or accidental
   (no reference to canonical)?

**Outputs:** Classified implementation inventory with labels and authority validation

**Ledger emission:** `implementations_classified` with `{primitive_count, canonical, cache, isotope, incompatible, authority_gaps, authority_conflicts}`

### Phase 5: CONSOLIDATE

**Purpose:** For each non-canonical implementation, recommend a specific resolution that either
eliminates the copy, formalizes it, or documents the intentional divergence.

**Invariant steps:**
1. For **CACHE** implementations:
   - If sync mechanism exists and is healthy → document and retain
   - If sync mechanism exists but is stale → fix the sync, run it, verify
   - If no sync mechanism → add one (CI check, pre-commit hook, or manual SOP) or replace
     with a runtime import/reference to canonical
2. For **ISOTOPE** implementations:
   - If the isotope is accidental → replace with import/reference to canonical
   - If the isotope adds value the canonical lacks → merge the improvements into canonical,
     then replace the isotope with a reference
   - If the isotope serves a genuinely different audience → document the intentional fork with
     a cross-reference explaining the divergence and its rationale
3. For **INCOMPATIBLE** implementations:
   - Determine which version is correct by consulting the governance owner
   - Update the incorrect version to match the correct one
   - If the incompatibility reveals a design flaw in the canonical → fix canonical first, then
     propagate
   - Add a CI/automation guard to prevent future incompatible reimplementations
4. Prioritize consolidation actions by blast radius: INCOMPATIBLE first (active harm),
   then stale CACHE (silent drift), then ISOTOPE (potential future harm)

**Outputs:** Consolidation action plan ordered by blast radius

**Ledger emission:** `governance_isotopes_detected` with `{primitive_count, implementation_count, canonical, cache, isotope, incompatible}`

---

## 3. Outputs

| Phase | Output | Format |
|-------|--------|--------|
| IDENTIFY | Governance primitive inventory | Table with canonical locations and search signatures |
| SEARCH | Implementation map | Per-primitive list of all locations |
| COMPARE | Compatibility matrix | Pairwise comparison results per primitive |
| CLASSIFY | Classified inventory | Implementation list with CANONICAL/CACHE/ISOTOPE/INCOMPATIBLE labels |
| CONSOLIDATE | Action plan | Prioritized resolution list ordered by blast radius |

---

## 4. Failure Modes and Recovery

| Failure | Detection | Recovery |
|---------|-----------|----------|
| Primitive inventory incomplete (missed a governance concept) | SEARCH finds implementations that map to no known primitive | Add the newly discovered primitive to the inventory; re-run from Phase 1 |
| SEARCH misses an implementation (false negative) | Post-consolidation, a forgotten copy resurfaces | Add grep patterns from the missed implementation's vocabulary; re-search |
| Canonical disputed (two teams claim authority) | Phase 4 finds >1 CANONICAL candidate | Escalate to system governance owner; resolution must be recorded in governance-rules.json |
| Intentional isotope misclassified as accidental | Consolidation recommends deleting a version that serves a distinct audience | Before deleting any implementation, verify with its consumers that the canonical version meets their needs |
| Consolidation creates regression | After replacing an isotope with canonical, consumers break | The isotope had edge-case behavior canonical lacks; roll back, merge the edge-case handling into canonical, then re-consolidate |

---

## 5. Relationship to Existing SOPs

| SOP | Relationship | Integration Point |
|-----|-------------|-------------------|
| SOP-IV-DSC-001 (Disposition Classification) | Contradiction source | Isotopes found across dissolving units feed the CONTRADICT phase of disposition |
| SOP-IV-STL-001 (Staleness Mapping) | Correlation signal | Cemetery clusters (abandoned subsystems) often contain stale isotopes — dead copies that are never updated |
| SOP-IV-CCA-001 (Ceremony Cost Accounting) | Symptom-to-cause | Ceremony duplication is the visible symptom; governance isotopes are the underlying structural cause |
| SOP-IV-XGR-001 (Xenograft Protocol) | Import guard | Foreign material (xenografts) may carry their own governance implementations — screen for isotopes at ingestion |
| Promotion & State Transitions | Primary isotope target | The promotion state machine is the most commonly reimplemented governance primitive across the system |
| Network Testament Protocol | Verification complement | Testament protocol captures what-happened; isotope detection catches what-drifted |

---

## 6. Protocol Governance

- **Owner:** ORGAN-IV (Taxis)
- **Lifecycle:** REP — needs second run on a different target to reach ABSORB
- **Next target:** Cross-organ isotope sweep — specifically the promotion state machine and organ map
  primitives, which were found in 3-4 locations during the ORGAN-IV dissection
