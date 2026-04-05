# SOP-IV-CBR-001: Cross-Boundary Reference Mapping

**Version:** 1.0
**Date:** 2026-04-05
**Scope:** System-wide (any multi-repo, multi-org, or superproject architecture)
**Lifecycle Stage:** REP (first run performed on ORGAN-IV, 2026-04-04)
**Provenance:** Extracted from `DISSECTION.md` — ORGAN-IV Flattened Hierarchy Post-Mortem

> Traces data flows that cross submodule, organization, or system boundaries to surface undeclared dependencies, caching workarounds, and structural debt invisible to single-repo tooling.

---

## 1. When This Protocol Applies

| # | Condition | Negative Test |
|---|-----------|---------------|
| 1 | System contains two or more independently versioned repositories that share configuration or data files | Single monorepo with unified dependency management |
| 2 | Configuration files (YAML, JSON, TOML) are consumed by components outside the directory that owns them | All consumers co-located with the canonical source |
| 3 | A superproject tracks submodules, and submodules reference each other's files at runtime or build time | Submodules are fully self-contained with no cross-references |
| 4 | Governance or registry files have canonical authority in one org but are read by another | Each org maintains its own independent governance data |
| 5 | Data flows cross from the development system into an external system (e.g., dotfile manager, LaunchAgents, CI) | All consumers operate within the same repository boundary |

---

## 2. Protocol Phases

```
ENUMERATE ──> TRACE ──> CLASSIFY ──> CACHE ──> MAP ──> RECOMMEND
    │            │          │          │        │          │
    │            │          │          │        │          └─ Resolution proposals
    │            │          │          │        └─ Declared vs. actual graph
    │            │          │          └─ Caching chain documentation
    │            │          └─ Boundary classification per edge
    │            └─ Consumer discovery per file
    └─ Candidate file inventory
```

### Phase 1: ENUMERATE
**Purpose:** Build the inventory of configuration and data files that could be consumed across boundaries.
**Invariant steps:**
1. Walk the directory tree of the target scope (superproject, org, or system).
2. Collect all YAML, JSON, and TOML files that serve a configuration or registry function — exclude test fixtures and generated build artifacts.
3. Include fleet definitions, governance rules, registry files, seed contracts, voice constitutions, and any file referenced in more than one `CLAUDE.md` or `AGENTS.md`.
4. For each file, record: canonical path, file type, owning repo/submodule, and declared purpose (from comments, README, or surrounding context).
5. Produce the **Candidate File Inventory** table.
**Outputs:** Candidate File Inventory (path, type, owner, purpose).
**Ledger emission:** `cbr_enumerate_complete` with `{files_found, repos_scanned}`

### Phase 2: TRACE
**Purpose:** For each candidate file, discover every consumer — any code, script, or configuration that reads, imports, copies, or references it.
**Invariant steps:**
1. For each file in the inventory, extract the filename and any known aliases (e.g., `registry-v2.json` might also be referenced as `registry.json`).
2. Search the entire scope for: direct path references, filename references, import statements, `open()` / `fs.readFile()` / `yaml.safe_load()` calls mentioning the file, shell commands (`cat`, `cp`, `jq`) targeting the file.
3. For each discovered consumer, record: consumer path, consumer repo/submodule, reference type (import, path literal, copy command, config lookup), and line number.
4. Flag consumers that reference the file by relative path (fragile) vs. absolute path or environment variable (stable).
**Outputs:** Consumer Registry (file, consumer, consumer_repo, reference_type, line, path_stability).
**Ledger emission:** `cbr_trace_complete` with `{files_traced, total_consumers}`

### Phase 3: CLASSIFY
**Purpose:** Assign a boundary classification to each file-consumer edge.
**Invariant steps:**
1. For each (file, consumer) pair, determine the boundary type:
   - **INTERNAL** — Consumer is in the same repository or submodule as the canonical file.
   - **CROSS-SUBMODULE** — Consumer is in a different submodule within the same superproject.
   - **CROSS-ORG** — Consumer is in a different GitHub organization or organ.
   - **CROSS-SYSTEM** — Consumer is in an external system (dotfile manager, LaunchAgent, CI pipeline, external service).
2. Record the classification alongside the consumer entry.
3. Aggregate counts by classification type.
**Outputs:** Classified Edge Table (file, consumer, boundary_type).
**Ledger emission:** `cbr_classify_complete` with `{internal, cross_submodule, cross_org, cross_system}`

### Phase 4: CACHE
**Purpose:** Identify caching workarounds — files copied to local directories because runtime import across boundaries is not supported.
**Invariant steps:**
1. For each CROSS-SUBMODULE, CROSS-ORG, or CROSS-SYSTEM edge, check whether the consumer reads the canonical file directly or reads a local copy.
2. If a local copy exists, trace the copy chain: canonical source -> first-level cache -> second-level cache -> ...
3. For each cache, document: cache path, hop depth from canonical, freshness mechanism (symlink, copy script, CI sync job, manual copy, none), and last-known sync date if determinable.
4. Flag any cache-of-cache patterns (hop depth >= 2) as high-risk for staleness.
**Outputs:** Caching Chain Table (canonical, cache_path, hop_depth, freshness_mechanism, last_sync).
**Ledger emission:** `cbr_cache_complete` with `{total_caches, max_hop_depth, no_freshness_count}`

### Phase 5: MAP
**Purpose:** Produce the actual dependency graph and compare it against declared dependencies.
**Invariant steps:**
1. Build the **actual dependency graph** from the Classified Edge Table: nodes are repos/submodules, edges are cross-boundary references weighted by count.
2. Build the **declared dependency graph** from seed.yaml `produces`/`consumes` edges, governance-rules.json, and any explicit dependency declarations.
3. Compute the diff: edges present in actual but absent in declared (undeclared dependencies), edges present in declared but absent in actual (stale declarations).
4. For each undeclared dependency, assess severity: does it violate the unidirectional dependency rule (Article II)? Does it create a circular reference?
**Outputs:** Dependency Graph Diff (undeclared edges, stale declarations, violation flags).
**Ledger emission:** `cbr_map_complete` with `{actual_edges, declared_edges, undeclared_count, stale_count, violations}`

### Phase 6: RECOMMEND
**Purpose:** Propose a resolution for each undeclared or problematic reference.
**Invariant steps:**
1. For each undeclared reference, choose one of:
   - **FORMALIZE** — Add the edge to seed.yaml as a declared `consumes` relationship.
   - **IMPORT** — Replace the file read with a proper import mechanism (shared package, API call, submodule pin).
   - **CONSOLIDATE** — Move the canonical file to a location accessible to all consumers without boundary crossing.
   - **ELIMINATE** — The reference is unnecessary; remove the consumer's dependency.
2. For each WORKAROUND cache (Phase 4), propose the replacement mechanism.
3. For each stale declaration, propose removal or reconnection.
4. Prioritize recommendations by: violation severity, hop depth, consumer count.
**Outputs:** Recommendation Register (reference, action, priority, effort_estimate).
**Ledger emission:** `cross_boundary_mapped` with `{files_traced, internal, cross_submodule, cross_org, cross_system, undeclared_count}`

---

## 3. Outputs

| Output | Phase | Format | Description |
|--------|-------|--------|-------------|
| Candidate File Inventory | ENUMERATE | Table | All configuration/data files that could be consumed across boundaries |
| Consumer Registry | TRACE | Table | Every consumer of every candidate file, with reference type and path stability |
| Classified Edge Table | CLASSIFY | Table | Each file-consumer pair with boundary classification |
| Caching Chain Table | CACHE | Table | All caches with hop depth, freshness mechanism, and sync status |
| Dependency Graph Diff | MAP | Graph + Table | Actual vs. declared dependency graph with undeclared/stale edge lists |
| Recommendation Register | RECOMMEND | Prioritized Table | Resolution proposals for each undeclared reference and caching workaround |

---

## 4. Failure Modes and Recovery

| Failure | Detection | Recovery |
|---------|-----------|---------|
| Incomplete enumeration — files with non-standard extensions (`.cfg`, `.env`, `.conf`) missed | Consumer trace discovers references to files not in inventory | Re-run ENUMERATE with expanded file type list; add discovered files to inventory |
| False positive consumers — grep matches in comments, documentation, or test fixtures | Classification phase finds edges that don't represent runtime dependencies | Add exclusion patterns for doc/test directories; mark edges as DOCUMENTATION or TEST |
| Circular dependency detected in MAP phase | Graph analysis finds cycles in actual dependency graph | Escalate immediately — circular dependencies violate Article II and require architectural resolution |
| Caching chain cannot be fully traced — intermediate copy mechanism is opaque | Hop depth is indeterminate; canonical source of a cache is unknown | Mark as UNKNOWN_PROVENANCE; treat as highest-priority recommendation target |
| Declared graph is stale or incomplete — seed.yaml edges were never updated | Large diff between actual and declared graphs (>50% undeclared) | Treat the actual graph as ground truth; batch-update seed.yaml declarations |

---

## 5. Relationship to Existing SOPs

| SOP | Relationship | Integration Point |
|-----|-------------|-------------------|
| SOP-IV-XGR-001 (Xenograft Protocol) | CBR maps the boundaries that xenografts must cross | Phase 3 (CLASSIFY) feeds xenograft boundary assessment |
| SOP-IV-RCC-001 (Registry Caching Chain Analysis) | RCC is a specialized subset of CBR focused on registry files | CBR Phase 4 (CACHE) generalizes RCC's caching chain analysis to all file types |
| SOP-IV-PAR-001 (Plan Archaeology) | Plan files themselves can cross boundaries (plans in .claude/ referencing .gemini/ scope) | CBR ENUMERATE includes plan directories as candidate sources |
| SOP-IV-ICA-001 (Inflated Claims Audit) | Undeclared dependencies can inflate maturity claims (GRADUATED with hidden cross-boundary debt) | CBR MAP output feeds ICA EVIDENCE phase |
| Promotion Readiness Checklist | Undeclared cross-boundary references block promotion | CBR undeclared_count > 0 should block GRADUATED status |

---

## 6. Protocol Governance

- **Owner:** ORGAN-IV (Taxis)
- **Lifecycle:** REP — needs second run on different target to reach ABSORB
- **Next target:** ORGAN-III (Ergon) — highest repo count (31), most likely to have undeclared cross-org references to META and ORGAN-I tooling
