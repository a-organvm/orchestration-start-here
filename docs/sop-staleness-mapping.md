# SOP-IV-STL-001: Staleness Mapping

**Version:** 1.0
**Date:** 2026-04-05
**Scope:** Organ-level or project-level (any bounded set of units with git history)
**Lifecycle Stage:** REP (first run performed on ORGAN-IV, 2026-04-04)
**Provenance:** Extracted from `DISSECTION.md` — ORGAN-IV Flattened Hierarchy Post-Mortem

> The process of measuring temporal decay across a set of units — computing days since last
> meaningful activity, clustering units by staleness band, and surfacing anomalies that reveal
> organizational dysfunction.

---

## 1. When This Protocol Applies

Four invariant conditions, all of which must hold:

| # | Condition | Negative Test (does NOT apply) |
|---|-----------|-------------------------------|
| 1 | A reference date exists (milestone, sprint end, organ close) | No temporal anchor — define one first |
| 2 | Units have git history or dated artifacts | Units are new with no history to measure |
| 3 | Activity recency is decision-relevant | All units are known-active or known-archived |
| 4 | Distinguishing "meaningful" from "ceremonial" activity matters | All commits are treated equally (simple last-commit check suffices) |

If conditions 1-3 hold but 4 does not, a simple `git log --format="%ai" -1` per unit suffices —
this protocol adds value specifically when ceremony commits (metadata-only, scaffolding, CI fixes)
must be separated from substantive work.

---

## 2. Protocol Phases

```
REFERENCE DATE ESTABLISHED (organ close, sprint end, milestone, audit date)
    │
    ├── Phase 1: DEFINE          Establish meaningful activity criteria + reference date
    ├── Phase 2: SCAN            Extract last meaningful commit per unit from git log
    ├── Phase 3: COMPUTE         Calculate days-stale for each unit
    ├── Phase 4: CLUSTER         Group units into staleness bands
    └── Phase 5: ANOMALY         Flag temporal contradictions and dysfunction signals
```

### Phase 1: DEFINE

**Purpose:** Establish the criteria that distinguish meaningful activity from ceremony, and fix
the reference date against which all staleness is measured.

**Invariant steps:**
1. Set the reference date: the date against which staleness is measured
   - Organ close: the declared end date of the dissolving structure
   - Sprint end: the last day of the sprint being audited
   - Audit date: today, if running a health check
2. Define "meaningful activity" for this context:
   - **Includes:** Commits that add, modify, or delete application code, tests, documentation with
     substantive content, configuration that changes behavior
   - **Excludes:** Ceremony-only commits (CLAUDE.md sync, seed.yaml template updates, CI badge changes,
     submodule pointer updates, changelog entries without corresponding code, dependency bumps with
     no code change)
3. Define the commit message patterns to exclude (e.g., `chore: sync`, `docs: update CLAUDE.md`,
   `chore: bump version`)
4. Document the definitions in the output — staleness is only meaningful if the criteria are explicit

**Outputs:** Definition document: reference date, meaningful activity criteria, exclusion patterns

**Ledger emission:** `staleness_criteria_defined` with `{reference_date, exclusion_patterns_count}`

### Phase 2: SCAN

**Purpose:** For each unit, extract the date of its last meaningful commit by walking git history
and filtering against the criteria established in Phase 1.

**Invariant steps:**
1. For each unit (repo, submodule, or directory):
   - Walk `git log` in reverse chronological order
   - For each commit, check:
     - Does the commit message match an exclusion pattern? → skip
     - Does the diff touch only ceremony files? → skip
     - Does the diff include substantive changes? → record this date and stop
   - If no meaningful commit is found, record `last_activity = null` (never active)
2. Record for each unit: `{unit, last_meaningful_date, last_meaningful_commit_hash, commit_summary}`
3. If a unit has no git history (uninitialized submodule, empty directory), record as `no_history`

**Outputs:** Per-unit activity records with dates and commit references

**Ledger emission:** `staleness_scanned` with `{unit_count, scanned, no_history, never_active}`

### Phase 3: COMPUTE

**Purpose:** Calculate the staleness metric for each unit as a simple integer: days between
last meaningful activity and the reference date.

**Invariant steps:**
1. For each unit with a `last_meaningful_date`:
   - `days_stale = reference_date - last_meaningful_date` (in calendar days)
2. For units with `last_activity = null`: assign `days_stale = infinity` (or a sentinel like 9999)
3. For units with `no_history`: assign `days_stale = infinity`
4. Sort all units by `days_stale` ascending (most active first)
5. Calculate summary statistics: median staleness, mean staleness, standard deviation

**Outputs:** Sorted staleness table with `{unit, days_stale, last_meaningful_date}`

**Ledger emission:** `staleness_computed` with `{unit_count, median_days, mean_days, max_days}`

### Phase 4: CLUSTER

**Purpose:** Group units into named staleness bands that map to organizational health categories.

**Invariant steps:**
1. Assign each unit to one of four bands:
   - **Active Core** (0-2 days stale) — work happened at or near the reference date
   - **Recent** (3-7 days stale) — work happened within the last sprint/week
   - **Stale** (8-14 days stale) — no activity for 1-2 weeks
   - **Abandoned** (>14 days stale, including infinity) — no meaningful activity in recent memory
2. Band thresholds are defaults — adjust for context (a quarterly audit might use 0-7/8-30/31-90/>90)
3. Calculate band sizes and percentages
4. Identify the dominant band — if >60% of units are in one band, that is the system's characteristic
5. Visualize (optional): histogram or heatmap of staleness distribution

**Outputs:** Clustered units with band assignments and distribution summary

**Ledger emission:** `staleness_mapped` with `{unit_count, active_core, recent, stale, abandoned, anomalies}`

### Phase 5: ANOMALY

**Purpose:** Surface temporal patterns that contradict expectations and reveal organizational
dysfunction, misdeclared status, or hidden work.

**Invariant steps:**
1. Check for **post-close activity**: units with meaningful commits after the reference date
   - This means work continued after a declared end — either the end was premature or the work
     was unauthorized/unaware
2. Check for **inverse staleness**: a unit in the Active Core band that is declared ARCHIVED,
   or a unit in the Abandoned band that is declared ACTIVE/GRADUATED
3. Check for **journal gaps**: units that show active git history but have no dated artifacts
   (no changelogs, no dated docs, no sprint references) — activity without narrative
4. Check for **cemetery clusters**: 3+ adjacent units (by declared hierarchy or dependency) all
   in the Abandoned band — an entire subsystem went dark
5. For each anomaly, record: `{unit, anomaly_type, evidence, implication}`

**Outputs:** Anomaly report with typed entries and evidence

**Ledger emission:** `staleness_anomalies_detected` with `{post_close, inverse, journal_gaps, cemetery_clusters}`

---

## 3. Outputs

| Phase | Output | Format |
|-------|--------|--------|
| DEFINE | Criteria document | Markdown with reference date and exclusion patterns |
| SCAN | Per-unit activity records | Table with dates and commit hashes |
| COMPUTE | Sorted staleness table | Table with days-stale metric |
| CLUSTER | Band assignments and distribution | Grouped table with percentages |
| ANOMALY | Anomaly report | Typed issue list with evidence |

---

## 4. Failure Modes and Recovery

| Failure | Detection | Recovery |
|---------|-----------|----------|
| Ceremony filter too aggressive (excludes real work) | Active units show as abandoned despite known recent work | Relax exclusion patterns; re-scan with broader "meaningful" definition |
| Ceremony filter too permissive (includes noise) | All units show as active despite known staleness | Tighten exclusion patterns; add specific commit message patterns to exclude list |
| Submodule not initialized (no git history) | SCAN returns `no_history` for a unit with known content | Run `git submodule update --init` and re-scan |
| Reference date disputed | Stakeholders disagree on when the boundary closed | Run COMPUTE with multiple reference dates; present as sensitivity analysis |
| Monorepo with shared history | All subdirectories show same last-commit date | Use path-scoped git log (`git log -- path/`) instead of repo-level |

---

## 5. Relationship to Existing SOPs

| SOP | Relationship | Integration Point |
|-----|-------------|-------------------|
| SOP-IV-DSC-001 (Disposition Classification) | Downstream consumer | Staleness bands feed ASSESS phase activity signals for disposition decisions |
| SOP-IV-CCA-001 (Ceremony Cost Accounting) | Shared exclusion set | Ceremony file definitions overlap — coordinate to avoid contradictory criteria |
| SOP-IV-GID-001 (Governance Isotope Detection) | Anomaly correlation | Cemetery clusters may indicate governance isotopes — same subsystem reimplemented elsewhere |
| Document Audit & Feature Extraction | Complementary diagnostic | Staleness mapping measures temporal health; document audit measures content health |
| Autopoietic Systems Diagnostics | Upstream framework | Staleness is one vital sign within the broader autopoietic health model |

---

## 6. Protocol Governance

- **Owner:** ORGAN-IV (Taxis)
- **Lifecycle:** REP — needs second run on a different target to reach ABSORB
- **Next target:** ORGAN-III (Ergon) — 31 repos with suspected high staleness variance across tiers
