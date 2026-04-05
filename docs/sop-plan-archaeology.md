# SOP-IV-PAR-001: Plan Archaeology

**Version:** 1.0
**Date:** 2026-04-05
**Scope:** System-wide or per-project (any codebase using AI-agent plan directories)
**Lifecycle Stage:** REP (first run performed on ORGAN-IV, 2026-04-04)
**Provenance:** Extracted from `DISSECTION.md` — ORGAN-IV Flattened Hierarchy Post-Mortem

> Catalogues all plan files across tool namespaces, detects duplicates and orphans, and measures the plan-to-execution ratio to expose planning debt and batch-ambition patterns.

---

## 1. When This Protocol Applies

| # | Condition | Negative Test |
|---|-----------|---------------|
| 1 | Project or system accumulates plan files from one or more AI tools (.claude/, .gemini/, .codex/, docs/) | No plan files exist; all work is ad-hoc |
| 2 | Multiple tool namespaces may contain overlapping or duplicated plans | Single tool namespace with no cross-tool plan generation |
| 3 | Plan count exceeds ~20 and manual tracking of completion status is no longer reliable | Small project with <10 plans, all recently created and tracked |
| 4 | Suspicion that planning velocity exceeds execution velocity (plans accumulate faster than they are implemented) | Clear 1:1 plan-to-implementation cadence with explicit completion markers |
| 5 | An organ, project, or system is being audited, dissolved, or handed off | Active ongoing development with no audit trigger |

---

## 2. Protocol Phases

```
SCAN ──> CATALOGUE ──> DUPLICATE ──> ORPHAN ──> RATIO ──> PATTERN
  │          │             │           │          │          │
  │          │             │           │          │          └─ Planning behavior taxonomy
  │          │             │           │          └─ Execution ratio computation
  │          │             │           └─ Implementation evidence cross-reference
  │          │             └─ Cross-namespace duplicate detection
  │          └─ Master plan inventory
  └─ Directory discovery
```

### Phase 1: SCAN
**Purpose:** Discover all directories in the target scope that contain plan files.
**Invariant steps:**
1. Search the target scope for directories matching known plan locations: `.claude/plans/`, `.gemini/plans/`, `.codex/plans/`, `docs/superpowers/plans/`, `_local/plans/`, bare `plans/` directories.
2. Also search for plan-like files outside standard directories: markdown files with date prefixes (`YYYY-MM-DD-*.md`) in `docs/`, `_local/`, or tool-specific directories.
3. For each discovered directory, record: path, tool namespace (claude, gemini, codex, superpowers, local, bare), and containing repo/submodule.
4. Count total plan directories and note any unexpected locations.
**Outputs:** Plan Directory Inventory (path, namespace, repo).
**Ledger emission:** `par_scan_complete` with `{directories_found, namespaces_found}`

### Phase 2: CATALOGUE
**Purpose:** Build the master inventory of every individual plan file.
**Invariant steps:**
1. For each plan directory, list all `.md` files.
2. For each plan file, extract: date (from filename prefix `YYYY-MM-DD`), slug (from filename after date), namespace (from parent directory), containing directory/repo, file size in bytes, and version suffix if present (`-v2`, `-v3`, `-agent-*`).
3. Parse the first 20 lines of each plan to extract: title (first `#` heading), any status markers (COMPLETED, ABANDONED, IN-PROGRESS), and scope description if present.
4. Build the **Master Plan Inventory** sorted by date descending.
5. Compute: total plan count, plans per namespace, plans per directory, date range (earliest to latest).
**Outputs:** Master Plan Inventory (date, slug, namespace, directory, size, version, title, status).
**Ledger emission:** `par_catalogue_complete` with `{total_plans, namespaces, date_range_days}`

### Phase 3: DUPLICATE
**Purpose:** Detect plans that appear in multiple namespaces — same content or intent duplicated across tool frameworks.
**Invariant steps:**
1. Group plans by slug (ignoring namespace prefix and date).
2. For each slug that appears in more than one namespace, compare: titles, dates (same day or within 3 days suggests duplication), file sizes (similar size suggests copy), and first-paragraph content.
3. Classify each duplicate set: EXACT (identical content across namespaces), NEAR (same slug and similar content, minor differences), DIVERGED (same slug but content has evolved independently).
4. For EXACT and NEAR duplicates, identify the canonical copy (earliest date or largest file) and mark others as redundant.
**Outputs:** Duplicate Report (slug, namespaces, classification, canonical_copy).
**Ledger emission:** `par_duplicate_complete` with `{duplicate_sets, exact, near, diverged}`

### Phase 4: ORPHAN
**Purpose:** Identify plans with no evidence of implementation.
**Invariant steps:**
1. For each plan in the Master Plan Inventory, search for implementation evidence:
   - Git commits: search commit messages for the plan slug, plan title keywords, or plan file path.
   - Code changes: search for files created or modified within 14 days after the plan date that match the plan's described scope.
   - Issues/PRs: search for GitHub issues or pull requests referencing the plan slug or title.
   - Explicit status: check if the plan itself declares COMPLETED or links to implementation.
2. Score each plan: IMPLEMENTED (strong evidence), PARTIAL (some evidence but scope not fully covered), ORPHAN (zero implementation evidence).
3. For ORPHAN plans, check if they were superseded by a later plan (same slug with higher version suffix).
**Outputs:** Implementation Evidence Table (plan, evidence_type, evidence_links, score).
**Ledger emission:** `par_orphan_complete` with `{implemented, partial, orphan, superseded}`

### Phase 5: RATIO
**Purpose:** Compute quantitative metrics on planning effectiveness.
**Invariant steps:**
1. **Plan-to-execution ratio:** implemented_count / total_plans (excluding superseded).
2. **Planning velocity:** plans per week, computed over the full date range.
3. **Execution latency:** for implemented plans, median days between plan date and first evidence of implementation.
4. **Density metrics:** plans per directory, plans per namespace, plans per repo.
5. **Age distribution:** histogram of plan ages (days since creation).
6. **Abandonment rate:** orphan_count / total_plans.
**Outputs:** Planning Metrics Summary (ratio, velocity, latency, density, age_distribution, abandonment_rate).
**Ledger emission:** `par_ratio_complete` with `{execution_ratio, velocity_per_week, median_latency_days, abandonment_rate}`

### Phase 6: PATTERN
**Purpose:** Identify recurring planning behaviors — both productive and pathological.
**Invariant steps:**
1. **Burst planning:** Detect windows where 3+ plans were created within 48 hours. For each burst, compute: plans created, plans implemented from that burst, burst-to-execution ratio.
2. **Ambitious batches:** Detect single-session plan sets (same date, sequential slugs) where scope exceeds reasonable execution capacity. Flag batches where 0 of N plans were implemented.
3. **Steady cadence:** Detect periods of regular planning (1-2 plans/week) with high execution ratio (>0.6).
4. **Evergreen plans:** Plans referenced in multiple later plans or commits but never marked complete — perpetual scope that keeps getting deferred.
5. **Namespace drift:** Tool namespaces that accumulated plans but stopped receiving new ones (abandoned tool adoption).
6. Produce the **Planning Pattern Report** with named pattern instances and recommendations.
**Outputs:** Planning Pattern Report (pattern_type, instances, dates, recommendation).
**Ledger emission:** `plan_archaeology_completed` with `{total_plans, namespaces, duplicates, orphans, execution_ratio}`

---

## 3. Outputs

| Output | Phase | Format | Description |
|--------|-------|--------|-------------|
| Plan Directory Inventory | SCAN | Table | All directories containing plan files, by namespace |
| Master Plan Inventory | CATALOGUE | Table | Every plan file with metadata (date, slug, namespace, size, title, status) |
| Duplicate Report | DUPLICATE | Grouped Table | Plans appearing in multiple namespaces with classification |
| Implementation Evidence Table | ORPHAN | Table | Each plan scored by implementation evidence |
| Planning Metrics Summary | RATIO | Metrics Report | Quantitative planning effectiveness measures |
| Planning Pattern Report | PATTERN | Narrative + Table | Named behavioral patterns with instances and recommendations |

---

## 4. Failure Modes and Recovery

| Failure | Detection | Recovery |
|---------|-----------|---------|
| Plan files use non-standard naming (no date prefix, no slug) | CATALOGUE phase finds unparseable filenames | Fall back to file modification date and first heading as slug; flag for manual review |
| Git history is shallow or unavailable — ORPHAN phase cannot search commits | Git log returns limited history or errors | Use file system evidence only (co-located implementation files, README references); note reduced confidence |
| Plans reference work done in a different repo than where the plan lives | ORPHAN phase finds zero evidence but plan describes cross-repo work | Expand search scope to sibling repos in the same organ; re-run ORPHAN for those plans |
| Duplicate detection produces false positives — similar slugs but unrelated plans | DUPLICATE phase flags plans with same slug but completely different content | Add content similarity threshold (e.g., >40% first-paragraph overlap) to confirm duplicates |
| Namespace drift misidentified — tool namespace is new, not abandoned | PATTERN phase flags a namespace with few plans as drifted | Check namespace creation date; exclude namespaces less than 30 days old from drift analysis |

---

## 5. Relationship to Existing SOPs

| SOP | Relationship | Integration Point |
|-----|-------------|-------------------|
| SOP-IV-CBR-001 (Cross-Boundary Reference Mapping) | Plan files themselves cross boundaries when duplicated across namespaces | CBR ENUMERATE includes plan directories; PAR DUPLICATE feeds CBR classification |
| SOP-IV-ICA-001 (Inflated Claims Audit) | Plans claiming "COMPLETED" without evidence are a form of inflated claim | PAR ORPHAN output feeds ICA ENUMERATE as additional claim sources |
| Plan File Discipline (CLAUDE.md) | PAR validates adherence to the plan naming and versioning rules | PAR CATALOGUE checks for: date prefix, slug format, version suffixes, archive directory usage |
| SOP-IV-XGR-001 (Xenograft Protocol) | Xenograft plans should follow the same plan discipline and be discoverable by PAR | PAR SCAN includes xenograft-related plan directories |
| Project Orchestration (conductor) | Conductor session plans should appear in PAR inventory with implementation evidence from session logs | PAR ORPHAN cross-references conductor session completion records |

---

## 6. Protocol Governance

- **Owner:** ORGAN-IV (Taxis)
- **Lifecycle:** REP — needs second run on different target to reach ABSORB
- **Next target:** META-ORGANVM — largest plan accumulation site (praxis-perpetua library with 269 indexed plans), ideal for stress-testing the RATIO and PATTERN phases at scale
