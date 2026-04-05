# SOP-IV-CCA-001: Ceremony Cost Accounting

**Version:** 1.0
**Date:** 2026-04-05
**Scope:** System-wide (any ecosystem with per-project scaffolding files)
**Lifecycle Stage:** REP (first run performed on ORGAN-IV, 2026-04-04)
**Provenance:** Extracted from `DISSECTION.md` — ORGAN-IV Flattened Hierarchy Post-Mortem

> The process of counting per-unit ceremony overhead, identifying inflation patterns where
> scaffolding files multiply beyond their governance value, and recommending consolidation
> strategies to reduce maintenance cost without losing governance signal.

---

## 1. When This Protocol Applies

Five invariant conditions, all of which must hold:

| # | Condition | Negative Test (does NOT apply) |
|---|-----------|-------------------------------|
| 1 | The system has a defined set of per-unit ceremony files | No standard scaffolding — each unit is ad hoc |
| 2 | Multiple units exist within the boundary | Single repo with one set of ceremony files |
| 3 | Ceremony files are suspected of inflation or duplication | All ceremony files are known to be minimal and unique |
| 4 | Maintenance cost of ceremony is a concern | Ceremony files are auto-generated and zero-maintenance |
| 5 | The ecosystem uses nested structures (superproject + submodules, monorepo + packages) | Flat structure with no nesting (no amplification possible) |

If conditions 1-4 hold but 5 does not (flat structure), skip Phase 4 (INFLATE) — nesting
amplification is impossible, but template duplication and orphan ceremony can still occur.

---

## 2. Protocol Phases

```
CEREMONY OVERHEAD SUSPECTED (growing maintenance burden, sync drift, template fatigue)
    │
    ├── Phase 1: DEFINE          Enumerate the ceremony file set
    ├── Phase 2: COUNT           Build the Universal Artifacts matrix
    ├── Phase 3: CALCULATE       Compute totals and coverage ratios
    ├── Phase 4: INFLATE         Identify inflation patterns
    └── Phase 5: CONSOLIDATE     Recommend reduction strategies
```

### Phase 1: DEFINE

**Purpose:** Enumerate every file type that constitutes "ceremony" in this ecosystem — files
required by governance, tooling, or convention that exist per-unit regardless of the unit's
unique needs.

**Invariant steps:**
1. List every file that is expected to exist in each unit by convention or automation:
   - Governance: `CLAUDE.md`, `AGENTS.md`, `GEMINI.md`, `seed.yaml`
   - Build/CI: `.github/workflows/`, `Dockerfile`, `Makefile`, `justfile`
   - Documentation: `README.md`, `CHANGELOG.md`, `LICENSE`
   - Configuration: `ecosystem.yaml`, `organ-aesthetic.yaml`, `.editorconfig`
   - Agent: `.claude/`, `.gemini/`, `.cursor/`
2. Classify each ceremony file by purpose:
   - **Governance** — enforces system rules or declares identity
   - **Tooling** — required by a specific tool to function
   - **Convention** — expected by humans but not enforced by automation
3. Note which ceremony files are templates (same content across units) vs. unique (customized per unit)
4. Record the ceremony set size: `|C|` = number of distinct ceremony file types

**Outputs:** Ceremony file inventory with classification and template/unique designation

**Ledger emission:** `ceremony_set_defined` with `{ceremony_types, governance, tooling, convention}`

### Phase 2: COUNT

**Purpose:** For each unit, check the presence or absence of each ceremony file, producing the
Universal Artifacts matrix.

**Invariant steps:**
1. Create a matrix: rows = units, columns = ceremony file types
2. For each cell, record:
   - **Present (P)** — file exists and has content
   - **Absent (A)** — file does not exist
   - **Empty (E)** — file exists but is a stub, placeholder, or contains only boilerplate
   - **Unique (U)** — file exists with content specific to this unit
3. Calculate per-unit ceremony count: how many ceremony files does each unit have?
4. Calculate per-type coverage: what percentage of units have each ceremony file?
5. Identify fully ceremonied units (all types present) and ceremony-sparse units

**Outputs:** Universal Artifacts matrix (units x ceremony types) with P/A/E/U annotations

**Ledger emission:** `ceremony_counted` with `{unit_count, ceremony_types, total_files, coverage_pct}`

### Phase 3: CALCULATE

**Purpose:** Compute the aggregate ceremony cost and compare actual vs. theoretical maximum.

**Invariant steps:**
1. **Theoretical maximum:** `units × |C|` — if every unit had every ceremony file
2. **Actual count:** Sum of all Present (P) + Empty (E) + Unique (U) cells in the matrix
3. **Coverage ratio:** `actual / theoretical_maximum` — how much of the possible ceremony surface exists
4. **Empty ratio:** `empty_count / actual_count` — what fraction of existing ceremony is hollow
5. **Unique ratio:** `unique_count / actual_count` — what fraction carries unit-specific content
6. Compute per-unit average ceremony file count
7. Flag outliers: units with significantly more or fewer ceremony files than the mean

**Outputs:** Ceremony cost summary with ratios, averages, and outliers

**Ledger emission:** `ceremony_cost_calculated` with `{theoretical_max, actual, coverage_ratio, empty_ratio, unique_ratio}`

### Phase 4: INFLATE

**Purpose:** Identify specific patterns where ceremony files multiply beyond their governance
value — the structural mechanisms that turn N ceremony files into 2N or 3N.

**Invariant steps:**
1. **Nesting amplification:** When a wrapper structure (superproject, monorepo root) and its inner
   units (submodules, packages) both carry ceremony files:
   - Count: how many ceremony files exist at both wrapper and inner levels?
   - For each pair: does the wrapper version add information beyond what the inner version says?
   - If not → the wrapper copy is pure amplification
2. **Template duplication:** Identical or near-identical content across N units:
   - Hash each ceremony file's content (or a normalized version stripping dates/names)
   - Group by hash — groups of size >1 are duplicates
   - Count total duplicated files and unique templates
3. **Orphan ceremony:** Ceremony files that outlived their unit:
   - Ceremony file present for a dissolved, empty, or deleted unit
   - README.md describing features that no longer exist
   - seed.yaml declaring edges to repos that have been archived
4. For each inflation pattern, calculate the waste: files that could be eliminated without
   losing governance signal

**Outputs:** Inflation report with pattern instances, waste counts, and evidence

**Ledger emission:** `ceremony_inflation_detected` with `{nesting_amplification, template_duplicates, orphan_ceremony, total_waste}`

### Phase 5: CONSOLIDATE

**Purpose:** For each inflation pattern, recommend a specific reduction strategy that preserves
governance value while eliminating maintenance burden.

**Invariant steps:**
1. For **nesting amplification:**
   - Recommend: single ceremony file at the highest applicable level with inheritance
   - Inner units override only the fields that differ
   - Pattern: `root/CLAUDE.md` contains shared context; `inner/CLAUDE.md` contains only deltas
2. For **template duplication:**
   - Recommend: single-source template with per-unit variable substitution
   - If using chezmoi/cookiecutter: template once, render per-unit
   - If no templating: reference link instead of copy (`See root CLAUDE.md for shared context`)
3. For **orphan ceremony:**
   - Recommend: delete if the unit is dissolved/deleted
   - Recommend: archive with the unit if the unit is archived
   - Recommend: update if the unit is active but ceremony is stale
4. Calculate projected savings: files eliminated, sync operations avoided per maintenance cycle
5. Prioritize recommendations by waste-to-effort ratio (most waste eliminated per unit of effort)

**Outputs:** Consolidation recommendations with projected savings, ordered by priority

**Ledger emission:** `ceremony_cost_accounted` with `{unit_count, ceremony_files_total, inflation_patterns, duplicate_count}`

---

## 3. Outputs

| Phase | Output | Format |
|-------|--------|--------|
| DEFINE | Ceremony file inventory | Table with classification |
| COUNT | Universal Artifacts matrix | Unit x ceremony-type matrix with P/A/E/U |
| CALCULATE | Cost summary with ratios | Metrics table with outlier flags |
| INFLATE | Inflation report | Pattern instances with waste counts |
| CONSOLIDATE | Reduction recommendations | Prioritized action list with projected savings |

---

## 4. Failure Modes and Recovery

| Failure | Detection | Recovery |
|---------|-----------|----------|
| Ceremony set incomplete (missed file types) | Post-count discovery of uncounted ceremony files | Add to set and re-count; matrix columns are additive |
| False duplicate (same hash but legitimately different purpose) | Consolidation merges files that serve different audiences | Review duplicates manually before merging; check if different agents consume different copies |
| Orphan misidentified (ceremony file for a unit in transition, not dead) | Deletion recommended for a unit about to be reactivated | Cross-reference with Disposition Classification — only delete ceremony for DELETE-disposition units |
| Nesting amplification is intentional (wrapper adds real value) | All wrapper ceremony flagged as waste but some carries system-level context | Distinguish system-context ceremony (valuable at wrapper level) from passthrough duplication |
| Political resistance to consolidation | Recommendations accepted but not executed | Tie ceremony reduction to a measurable metric (sync time, drift incidents) to justify the change |

---

## 5. Relationship to Existing SOPs

| SOP | Relationship | Integration Point |
|-----|-------------|-------------------|
| SOP-IV-DSC-001 (Disposition Classification) | Downstream consumer | Ceremony cost informs DISSOLVE decisions — high ceremony, low value units are dissolution candidates |
| SOP-IV-STL-001 (Staleness Mapping) | Shared exclusion criteria | Ceremony-only commits are excluded from meaningful activity — coordinate definitions |
| SOP-IV-GID-001 (Governance Isotope Detection) | Complementary diagnostic | Ceremony duplication is a symptom; isotope detection finds the governance primitives underneath |
| Repo Onboarding & Habitat Creation | Upstream producer | Onboarding creates ceremony files — this SOP measures whether the creation was justified |
| Stranger Test Protocol | Validation tool | Apply stranger test to consolidated ceremony — can a new contributor still orient? |

---

## 6. Protocol Governance

- **Owner:** ORGAN-IV (Taxis)
- **Lifecycle:** REP — needs second run on a different target to reach ABSORB
- **Next target:** Full ORGANVM system (all 128 repos) — measure total ceremony surface across 9 organs
