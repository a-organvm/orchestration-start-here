# SOP-IV-DCA-001: Domain Cross-Cut Analysis

**Version:** 1.0
**Date:** 2026-04-05
**Scope:** System-wide (ORGAN-IV governs, all organs invoke)
**Lifecycle Stage:** REP (first run performed on ORGAN-IV, 2026-04-04)
**Provenance:** Extracted from `DISSECTION.md` — ORGAN-IV Flattened Hierarchy Post-Mortem

> Slice a flattened hierarchy horizontally across ontological domains — revealing what vertical per-directory reading cannot: where concerns cluster, where they scatter, and where they collide.

---

## 1. When This Protocol Applies

| # | Condition | Negative Test (does NOT apply) |
|---|-----------|-------------------------------|
| 1 | A flattened structural view already exists (from FHA or equivalent) | Raw tree with no prior structural accounting |
| 2 | The system spans multiple concerns that cut across directory boundaries | Single-concern project where each dir maps cleanly to one domain |
| 3 | Vertical reading (per-directory) has already been done but feels incomplete | Vertical reading answered all structural questions |
| 4 | Decision-makers need to understand how a specific concern (e.g., governance, time, plans) is distributed | No pending decisions about cross-cutting restructuring |

If condition 1 fails, run SOP-IV-FHA-001 first. The flattened plane is this protocol's input.

---

## 2. Protocol Phases

```
FLATTENED HIERARCHY (output of FHA or equivalent)
    │
    ├── Phase 1: DEFINE       Select domain lenses appropriate to the system
    ├── Phase 2: APPLY        For each lens, sweep the entire tree and collect findings
    ├── Phase 3: COLLECT      Organize findings per lens into structured tables
    ├── Phase 4: COMPARE      Cross-reference density across directories
    └── Phase 5: SYNTHESIZE   Produce the cross-cut report
```

### Phase 1: DEFINE

**Purpose:** Select the set of domain lenses through which the system will be examined. Each lens asks a single horizontal question across all directories.

**Invariant steps:**
1. Review the flattened hierarchy from FHA to identify cross-cutting concerns
2. Select 4-8 domain lenses. The six lenses used in the ORGAN-IV dissection were:
   - **TIME** — When did things happen? What is stale? Where are activity clusters and gaps?
   - **UNIVERSALS** — What structural patterns repeat across directories? Where do they diverge?
   - **LEDGERS** — What tracking systems exist? Where do they overlap? Which are active vs. frozen?
   - **PLANS** — Where do plan artifacts live? Which were executed? Which are orphaned?
   - **MARKDOWN/RESEARCH** — Where does documentation concentrate? What is organic vs. ceremonial?
   - **CROSS-THRESHOLD INTERACTIONS** — What crosses submodule, organ, or system boundaries?
3. For each lens, write a one-sentence definition of what it seeks
4. Justify each lens: why does this horizontal question matter for the pending decisions?
5. Discard any lens that would duplicate another or that cannot be answered from the available artifacts

**Outputs:**
- Lens definition table: `{lens_name, definition, justification}`
- Recommended lens count (4-8; fewer loses coverage, more dilutes focus)

**Ledger emission:** `emitted_lenses_defined` with `{lens_count, lens_names}`

### Phase 2: APPLY

**Purpose:** Sweep the entire directory tree through each lens, collecting raw findings without yet organizing or judging.

**Invariant steps:**
1. For each lens, scan every directory in the flattened hierarchy
2. Record what the lens reveals per directory. The scan method varies by lens:
   - **TIME**: extract dates from filenames, git logs, frontmatter, changelogs. Build a timeline. Compute staleness.
   - **UNIVERSALS**: check for repeated files (CLAUDE.md, seed.yaml, etc.), note presence/absence, detect template copies vs. unique content.
   - **LEDGERS**: locate all tracking files (JSON registries, YAML streams, action logs, rollup caches). Note their record counts and freshness.
   - **PLANS**: find all `plans/` directories across all tool namespaces. Count plan files. Check for archive patterns. Identify orphans (plans with no corresponding implementation).
   - **MARKDOWN/RESEARCH**: count `.md` files. Distinguish organic documentation from generated/ceremonial. Locate research corpora.
   - **CROSS-THRESHOLD INTERACTIONS**: trace data flows that cross submodule boundaries. Identify cached copies, registry chains, files consumed outside their containing directory.
3. For each directory, if a lens has no findings, record the absence — voids are data
4. Do not filter, grade, or prioritize during this phase — that is COMPARE's job

**Outputs:**
- Raw findings matrix: `{lens × directory}` with observations per cell
- Void list: directories where a lens found nothing (signals a gap or irrelevance)

**Ledger emission:** `emitted_lenses_applied` with `{lens_count, directories_scanned, findings_count}`

### Phase 3: COLLECT

**Purpose:** Organize raw findings from Phase 2 into structured, lens-specific tables that make each domain's landscape readable.

**Invariant steps:**
1. For each lens, create a domain-specific summary table. Proven formats from the ORGAN-IV dissection:
   - **TIME** → Activity timeline (period | what happened) + Staleness map (directory | last activity | days stale)
   - **UNIVERSALS** → Ceremony matrix (directory × ceremony files, Y/N per cell) + Repetition report (file | copy count | canonical location)
   - **LEDGERS** → Ledger inventory (ledger name | location | record count | status) + Registry chain (canonical → cache → cache)
   - **PLANS** → Plan directory topology (namespace | directories | plan files) + Plan concentration table (directory | plan count | date range) + Orphan plan list
   - **MARKDOWN/RESEARCH** → Documentation density table (directory | .md files | key documents) + Research corpus breakdown (cohort | files | overlap %)
   - **CROSS-THRESHOLD INTERACTIONS** → Boundary crossing table (what crosses | from | to | mechanism) + Governance isotope map (concept × directory, tracking reimplementations)
2. Include counts and percentages — the tables must support quantitative comparison in Phase 4
3. Preserve specific evidence: file paths, line counts, dates — not just summaries

**Outputs:**
- One structured table (or table set) per lens
- Evidence trail: specific file paths and metrics backing each table entry

**Ledger emission:** `emitted_findings_collected` with `{lens_count, tables_produced}`

### Phase 4: COMPARE

**Purpose:** Cross-reference findings across lenses and across directories to identify concentrations, voids, and collisions.

**Invariant steps:**
1. **Density analysis**: for each directory, count how many lenses produced significant findings. A directory that appears heavily in 4+ lenses is a concentration point. A directory that appears in 0-1 lenses is a void.
2. **Concentration map**: identify which directories are "heavy" (many concerns converging) and which are "light." In the ORGAN-IV dissection, tool-interaction-design appeared as the heaviest node across nearly all lenses.
3. **Collision detection**: look for the same concern appearing in multiple directories — governance rules in 3 locations, registries cached across 2 hops, plans duplicated between namespaces.
4. **Void detection**: look for expected concerns that no directory owns — no single operational index, no shared dependency resolution, no cleanup protocol.
5. **Temporal correlation**: cross-reference TIME findings with other lenses — do activity gaps correlate with stale ledgers? Do plan orphans cluster in a specific time period?

**Outputs:**
- Density matrix: directory × lens, scored by finding weight (heavy/medium/light/void)
- Concentration report: top 3-5 directories by cross-lens density
- Collision list: concerns found in >1 location
- Void list: expected concerns with no owner

**Ledger emission:** `emitted_cross_cut_compared` with `{concentration_count, collision_count, void_count}`

### Phase 5: SYNTHESIZE

**Purpose:** Produce the final cross-cut report — a single document that answers the question "what does each horizontal lens uniquely reveal that vertical reading missed?"

**Invariant steps:**
1. For each lens, write a 2-4 sentence synthesis: what did this lens uniquely reveal?
2. Identify the top findings that only the cross-cut could surface:
   - Redundancies visible only when you see the same file in 5 directories
   - Temporal patterns visible only when you lay all dates on one timeline
   - Governance fragmentation visible only when you trace the same concept across locations
3. Connect findings to pending decisions: for each structural question driving the audit, state what the cross-cut evidence says
4. Feed anomalies into SOP-IV-SGS-001 (Severity-Graded Skeleton Inventory) if a grading pass will follow
5. Append the lens definition table, density matrix, and collision/void lists as appendices

**Outputs:**
- Cross-cut synthesis report (narrative + appendices)
- Anomaly handoff list for SGS if applicable

**Ledger emission:** `emitted_domain_cross_cut_completed` with `{lens_count, directories_analyzed, findings_per_lens}`

---

## 3. Outputs

| Phase | Output | Format |
|-------|--------|--------|
| DEFINE | Lens definition table | Markdown table |
| APPLY | Raw findings matrix, void list | Matrix (lens × directory) |
| COLLECT | Per-lens structured tables with evidence | Markdown tables per domain |
| COMPARE | Density matrix, concentration/collision/void reports | Markdown tables + narrative |
| SYNTHESIZE | Cross-cut synthesis report with appendices | Markdown document |

The combined output constitutes the **Domain Cross-Cut Analysis Report** — the horizontal complement to any vertical per-directory audit.

---

## 4. Failure Modes and Recovery

| Failure | Detection | Recovery |
|---------|-----------|----------|
| Lenses too broad (everything is "found" everywhere) | COMPARE shows near-uniform density across all directories | Narrow lens definitions; split broad lenses into specific sub-lenses |
| Lenses too narrow (most cells empty) | APPLY produces >60% void cells | Merge related lenses or choose lenses at a higher abstraction level |
| Lens selection biased (only looks at concerns already known to be problematic) | Post-hoc review shows the cross-cut confirmed priors but discovered nothing new | Add at least one "adversarial" lens that asks about something not previously investigated |
| COLLECT loses specificity (tables say "yes/no" without evidence) | COMPARE cannot distinguish heavy from light findings | Re-run COLLECT with mandatory file paths, line counts, and dates per cell |
| Temporal lens hindered by missing dates | Many files have no timestamps, git history is squashed | Use git log per-file as fallback; note low-confidence date estimates |

---

## 5. Relationship to Existing SOPs

| SOP | Relationship |
|-----|-------------|
| SOP-IV-FHA-001 (Flattened Hierarchy Audit) | FHA is the prerequisite — it produces the structural plane that DCA slices horizontally. Always run FHA before DCA. |
| SOP-IV-SGS-001 (Severity-Graded Skeleton Inventory) | DCA surfaces anomalies and collisions; SGS grades them by severity. DCA's anomaly handoff list feeds SGS Phase 1 (SWEEP). |
| SOP-IV-VAP-001 (Verb Assignment Protocol) | DCA's concentration analysis reveals which directories carry the most cross-cutting weight, which informs verb assignment — the heaviest directories need the most precise verbs. |
| SOP-IV-XGR-001 (Xenograft Protocol) | DCA can be applied to an ingested xenograft corpus to understand its internal domain distribution before integration. |
| Document Audit & Feature Extraction (system SOP) | Both involve structured reading of a corpus, but document-audit operates on individual documents while DCA operates on directory trees. |
| Dynamic Lens Assembly (system SOP) | DCA Phase 1 (DEFINE) is a constrained instance of dynamic lens assembly — selecting analytical perspectives for a specific purpose. |

---

## 6. Protocol Governance

- **Owner:** ORGAN-IV (Taxis)
- **Lifecycle:** REP — needs second run on different target to reach ABSORB
- **Next target:** `~/Workspace/meta-organvm/` (META-ORGANVM superproject, 13 repos, the governance center — applying DCA to the system that governs all others tests whether the lenses generalize beyond orchestration)
