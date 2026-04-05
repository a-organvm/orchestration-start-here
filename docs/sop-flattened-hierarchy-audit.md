# SOP-IV-FHA-001: Flattened Hierarchy Audit

**Version:** 1.0
**Date:** 2026-04-05
**Scope:** System-wide (ORGAN-IV governs, all organs invoke)
**Lifecycle Stage:** REP (first run performed on ORGAN-IV, 2026-04-04)
**Provenance:** Extracted from `DISSECTION.md` — ORGAN-IV Flattened Hierarchy Post-Mortem

> Project a nested git superproject onto a single structural plane — making overlap, redundancy, phantom directories, and the gap between declared and actual structure visible.

---

## 1. When This Protocol Applies

| # | Condition | Negative Test (does NOT apply) |
|---|-----------|-------------------------------|
| 1 | Target is a git superproject or multi-repo workspace | Single-repo project with no submodules or sibling dirs |
| 2 | Directory count exceeds what one person can hold in working memory (>15) | Small repo where `tree` output fits on one screen |
| 3 | Declared structure (README, .gitmodules, registry) may have drifted from actual | Fresh scaffold with no history of organic growth |
| 4 | Decision about restructuring, dissolving, or migrating is imminent | Routine maintenance with no structural questions |
| 5 | Multiple agents or tools have written into the tree over time | Single-author, single-tool project |

If conditions 1-3 hold but 4-5 do not, the audit is still useful but the MEASURE phase can be abbreviated.

---

## 2. Protocol Phases

```
TARGET DIRECTORY (any git superproject or multi-repo workspace)
    │
    ├── Phase 1: CENSUS        Count all directories and files, including hidden/ignored
    ├── Phase 2: CLASSIFY      Categorize each directory by tracking status
    ├── Phase 3: TABULATE      Create structural classes table with counts and members
    ├── Phase 4: REVEAL        Map hidden infrastructure, caches, orphan artifacts
    └── Phase 5: MEASURE       Compute the gap between declared and actual structure
```

### Phase 1: CENSUS

**Purpose:** Produce a complete, unfiltered count of everything that exists on disk — not just what git tracks.

**Invariant steps:**
1. Count all top-level directories (including hidden: `.github/`, `.atoms/`, `.claude/`, etc.)
2. Count all root-level files (including dotfiles)
3. For each directory, count files by extension: `.py`, `.ts`, `.md`, `.yaml`, `.json`, `.sh`, `.go`
4. Exclude only build artifacts that inflate counts without carrying signal: `node_modules/`, `.venv/`, `__pycache__/`, `.git/` internals
5. Record total file count, total directory count, and primary language per directory (by file-extension majority)

**Outputs:**
- `census-table.md`: Per-directory file counts with language breakdown (the table from DISSECTION Level 1)
- Raw counts: `{total_directories, total_files, total_by_extension}`

**Ledger emission:** `emitted_census_completed` with `{directory_count, file_count, root_file_count}`

### Phase 2: CLASSIFY

**Purpose:** Assign each directory to a structural class based on how it participates in version control.

**Invariant steps:**
1. Read `.gitmodules` — list all declared submodules and their paths
2. Read `.gitignore` — determine the tracking strategy (whitelist vs. blacklist, specific exclusions)
3. For each directory, determine its class:
   - **Tracked submodule**: appears in `.gitmodules` and has a submodule commit pointer
   - **Untracked core repo**: contains `.git/` (is a repo) but not in `.gitmodules` — a local repo invisible to the superproject
   - **Untracked external**: contains `.git/` but is a fork, mirror, or upstream clone — not authored by the system
   - **Phantom**: exists on disk but has no `.git/`, is not in `.gitmodules`, and is not whitelisted — would vanish if the machine were lost
   - **Generated/cache**: created by a build or tool process (`.build/`, `.ruff_cache/`, `.atoms/`)
4. Flag any directory that appears in `.gitmodules` but does not exist on disk (missing submodule)
5. Flag any directory that exists on disk with a `.git/` but is not in `.gitmodules` (rogue repo)

**Outputs:**
- Classification per directory: `{directory_name, class, has_git, in_gitmodules, in_gitignore}`
- Count per class: `{tracked_submodules, untracked_core, untracked_external, phantom, generated}`

**Ledger emission:** `emitted_directories_classified` with `{tracked_count, untracked_count, phantom_count}`

### Phase 3: TABULATE

**Purpose:** Collapse the per-directory classifications into a structural classes table that makes the system's shape legible at a glance.

**Invariant steps:**
1. Group directories by class from Phase 2
2. For each class, list all members with their file counts from Phase 1
3. Produce a single summary table:
   | Class | Count | Members |
   |-------|-------|---------|
   | Tracked submodules | N | list |
   | Untracked core repos | N | list |
   | Untracked contrib/external | N | list |
   | Phantom/generated | N | list |
4. Record root files separately: file name, size, purpose, staleness (last modified vs. current date)
5. Identify the declared canonical structure (README, .gitmodules) and note any discrepancies with the table

**Outputs:**
- Structural classes table (the table from DISSECTION Level 0)
- Root files table with size and purpose

**Ledger emission:** `emitted_structure_tabulated` with `{class_count, total_directories}`

### Phase 4: REVEAL

**Purpose:** Surface hidden infrastructure — directories and files that influence system behavior but are not visible in a casual listing.

**Invariant steps:**
1. Scan for hidden directories at every level: `.atoms/`, `.claude/`, `.github/`, `.build/`, `.conductor/`, `.ci-corpus/`, `.ruff_cache/`, `.venv/`
2. For each hidden directory, document: path, purpose, size, whether it is committed or gitignored
3. Detect **nesting amplification**: `.github/.github/`, tool-specific subdirectories that duplicate parent structure
4. Detect **orphan artifacts**: caches for tools not used at that level (e.g., `.ruff_cache/` at a root with no Python source)
5. Detect **cross-boundary files**: files that exist in one submodule but are consumed by another (e.g., `fleet.yaml` at root consumed by a submodule's Python code)
6. Count hidden infrastructure per directory

**Outputs:**
- Hidden infrastructure table: path, purpose, committed (Y/N), orphan (Y/N)
- Cross-boundary consumption map
- Nesting amplification report

**Ledger emission:** `emitted_hidden_infrastructure_mapped` with `{hidden_dir_count, orphan_count, cross_boundary_count}`

### Phase 5: MEASURE

**Purpose:** Quantify the gap between what the system claims to be (declared structure) and what it actually is (observed structure).

**Invariant steps:**
1. Extract declared structure from all sources: README, .gitmodules, registry.json, seed.yaml files, any architecture docs
2. Extract actual structure from Phases 1-4
3. Compute gap metrics:
   - **Submodule gap**: declared submodules vs. actual repos on disk
   - **Documentation gap**: directories mentioned in docs vs. directories that exist (and vice versa)
   - **Tracking gap**: percentage of directories invisible to git
   - **Ceremony gap**: expected ceremony files (CLAUDE.md, seed.yaml, etc.) vs. actual per directory
4. Produce the gap report: each metric as a fraction (declared / actual) with specific discrepancies listed
5. Flag any gap where declared > actual (claiming things that don't exist) as higher severity than actual > declared (having things that aren't documented)

**Outputs:**
- Gap report with metrics and specific discrepancies
- Overall gap percentage: `1 - (declared ∩ actual) / (declared ∪ actual)`

**Ledger emission:** `emitted_flattened_hierarchy_audited` with `{directory_count, submodule_count, phantom_count, gap_pct}`

---

## 3. Outputs

| Phase | Output | Format |
|-------|--------|--------|
| CENSUS | Per-directory file counts, language breakdown | Markdown table |
| CLASSIFY | Per-directory class assignment | Structured list |
| TABULATE | Structural classes table, root files table | Markdown tables |
| REVEAL | Hidden infrastructure table, cross-boundary map, nesting report | Markdown tables + narrative |
| MEASURE | Gap report with quantified metrics | Markdown with computed fractions |

The combined output constitutes the **Flattened Hierarchy Audit Report** — a single document (or section of a larger post-mortem) that makes the system's actual shape visible on one plane.

---

## 4. Failure Modes and Recovery

| Failure | Detection | Recovery |
|---------|-----------|----------|
| CENSUS undercounts (build artifacts included, inflating) | File counts for a directory exceed 1000 and majority are generated | Re-run CENSUS with tighter exclusion filters; document what was excluded |
| CLASSIFY misassigns (e.g., treating an untracked core repo as external) | Review by someone who knows the authorship history | Override classification manually; add a PROVENANCE note to the directory |
| Hidden directories missed | A later phase discovers behavior that cannot be explained by the revealed infrastructure | Re-run REVEAL with deeper recursion; add the missed pattern to the scan list |
| Gap metrics misleading (e.g., README intentionally omits some dirs) | Gap percentage seems unreasonably high or low | Distinguish intentional omissions from accidental ones; report both raw and adjusted gap |
| Submodule exists in .gitmodules but not on disk | CLASSIFY flags it | Run `git submodule update --init` or remove the stale .gitmodules entry |

---

## 5. Relationship to Existing SOPs

| SOP | Relationship |
|-----|-------------|
| SOP-IV-DCA-001 (Domain Cross-Cut Analysis) | FHA produces the structural plane; DCA then slices it horizontally by domain. FHA is prerequisite to DCA. |
| SOP-IV-SGS-001 (Severity-Graded Skeleton Inventory) | FHA + DCA surface anomalies; SGS grades them. FHA feeds anomalies into SGS Phase 1 (SWEEP). |
| SOP-IV-VAP-001 (Verb Assignment Protocol) | FHA's directory list is the input to VAP's ENUMERATE phase. |
| SOP-IV-XGR-001 (Xenograft Protocol) | Both handle structural accounting, but XGR processes inbound alien material while FHA audits existing native structure. |
| Superproject Topology Audit (`docs/superproject-topology-audit.md`) | The topology audit is a 7+1 step operational procedure; FHA is the diagnostic methodology it operationalizes. FHA is the "why and what," topology audit is the "how to run it." |

---

## 6. Protocol Governance

- **Owner:** ORGAN-IV (Taxis)
- **Lifecycle:** REP — needs second run on different target to reach ABSORB
- **Next target:** `~/Workspace/organvm-ii-poiesis/` (ORGAN-II superproject, ~21 repos, comparable complexity, different domain)
