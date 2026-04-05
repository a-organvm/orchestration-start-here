# SOP-IV-RCC-001: Registry Caching Chain Analysis

**Version:** 1.0
**Date:** 2026-04-05
**Scope:** System-wide (any system with shared configuration files consumed across module boundaries)
**Lifecycle Stage:** REP (first run performed on ORGAN-IV, 2026-04-04)
**Provenance:** Extracted from `DISSECTION.md` — ORGAN-IV Flattened Hierarchy Post-Mortem

> Traces canonical-to-cache-to-cache-of-cache data flows for authoritative configuration files, measuring hop depth and freshness guarantees to expose silent staleness risk.

---

## 1. When This Protocol Applies

| # | Condition | Negative Test |
|---|-----------|---------------|
| 1 | System has files designated as "single source of truth" (registries, governance rules, canonical configs) | No file is designated as authoritative; all configs are local and independent |
| 2 | Components in different repos, submodules, or systems need to read these authoritative files | All consumers are co-located with the canonical source in the same directory |
| 3 | Runtime import across module boundaries is not supported (e.g., git submodules cannot import each other's files) | Shared package manager or monorepo tooling provides direct import across all boundaries |
| 4 | Copies of authoritative files exist in multiple locations (identical or near-identical filenames in different directories) | Each directory has its own independently maintained configuration with no pretense of derivation |
| 5 | Staleness has caused or could cause incorrect behavior (e.g., a cached governance file allows a dependency that the canonical version forbids) | All copies are symlinks or hard references with guaranteed atomic freshness |

---

## 2. Protocol Phases

```
IDENTIFY ──> TRACE ──> CHAIN ──> FRESHNESS ──> INTENT ──> RESOLVE
    │           │         │          │            │           │
    │           │         │          │            │           └─ Resolution proposals
    │           │         │          │            └─ INTENTIONAL / WORKAROUND / ACCIDENTAL
    │           │         │          └─ Staleness assessment per cache
    │           │         └─ Hop depth mapping
    │           └─ Copy/cache discovery
    └─ Canonical source inventory
```

### Phase 1: IDENTIFY
**Purpose:** Find all files in the system that serve as authoritative sources of truth — files that other components read to make decisions.
**Invariant steps:**
1. Search for files explicitly declared as canonical: files referenced as "single source of truth" in CLAUDE.md, AGENTS.md, README.md, or governance documents.
2. Search for registry files: `registry*.json`, `governance*.json`, `config*.yaml`, `fleet*.yaml`, `seed.yaml` at org or superproject root level.
3. Search for files with protective guards: code that refuses to write if the file has fewer than N entries (the `save_registry()` pattern), or CI checks that validate file integrity.
4. For each canonical file, record: path, file type, owning repo/org, declared authority (what decisions depend on this file), approximate size, and last modification date.
5. Produce the **Canonical Source Inventory**.
**Outputs:** Canonical Source Inventory (path, type, owner, authority, size, last_modified).
**Ledger emission:** `rcc_identify_complete` with `{canonical_count}`

### Phase 2: TRACE
**Purpose:** For each canonical file, find all copies and caches that exist elsewhere in the system.
**Invariant steps:**
1. For each canonical file, search for:
   - Files with the same name in other directories.
   - Files with similar names (e.g., `governance-rules.json` cached as `governance.json` or `local-governance-rules.json`).
   - JSON/YAML files with overlapping top-level keys (>50% key overlap suggests a partial copy).
   - Code that reads the canonical file and writes a subset to a local file (copy-on-read pattern).
   - Symlinks pointing to the canonical file (these are the healthy case).
2. For each discovered copy, record: cache path, cache repo/submodule, file size (compare to canonical), and discovery method (same name, key overlap, code trace).
3. Distinguish between: full copies (same size, same content), partial copies (subset of keys/entries), and derived files (transformed from canonical but not identical).
**Outputs:** Cache Discovery Table (canonical, cache_path, cache_repo, copy_type, size_comparison).
**Ledger emission:** `rcc_trace_complete` with `{total_caches, full_copies, partial_copies, derived}`

### Phase 3: CHAIN
**Purpose:** Map the caching chain from canonical through intermediate caches to terminal consumers.
**Invariant steps:**
1. For each cache discovered in TRACE, determine its provenance: was it copied from the canonical source directly, or from another cache?
2. Build the chain: `canonical (hop 0) -> first-level cache (hop 1) -> second-level cache (hop 2) -> ...`
3. To determine provenance: check git blame for the copy commit, search for copy scripts or CI jobs that populate the cache, check if the cache's content matches the canonical or matches an intermediate cache (content fingerprinting).
4. Record the hop depth for each terminal cache (the cache that is actually read by application code).
5. Identify the **maximum hop depth** across all chains — this is the system's worst-case staleness amplification.
6. Produce the **Caching Chain Map**: a tree structure showing canonical -> caches -> caches-of-caches.
**Outputs:** Caching Chain Map (tree), Maximum Hop Depth, Chain Table (canonical, cache, hop_depth, provenance).
**Ledger emission:** `rcc_chain_complete` with `{max_hop_depth, chains_with_depth_2_plus}`

### Phase 4: FRESHNESS
**Purpose:** For each cache, assess how fresh it is and what mechanisms (if any) keep it synchronized.
**Invariant steps:**
1. For each cache, search for a freshness mechanism:
   - **Symlink** — Cache is a symbolic link to canonical. Freshness is guaranteed (hop depth effectively 0).
   - **CI sync job** — A GitHub Actions workflow or script copies canonical to cache on a schedule or on change. Record the trigger (schedule, push, manual).
   - **Copy script** — A script in the repo (Makefile target, npm script, shell script) copies canonical to cache. Record whether it's run automatically or manually.
   - **Git submodule pin** — Cache freshness is tied to submodule pointer update. Record how often pointers are synced.
   - **Manual copy** — No automated mechanism; cache was copied by hand. Evidence: single commit with a message like "update local copy of X".
   - **None** — No discernible mechanism. The cache was created once and never updated.
2. For caches with a freshness mechanism, compute the **maximum staleness window**: how long can the cache diverge from canonical before the mechanism triggers?
   - Symlink: 0 (always fresh).
   - CI on push: staleness = time between canonical change and next CI run (typically minutes).
   - CI on schedule: staleness = schedule interval (e.g., daily = 24 hours max).
   - Manual: staleness = unbounded.
3. For each cache, compute **actual current staleness**: diff the cache against canonical. Record: identical, minor drift (whitespace/formatting), content drift (different values), major drift (missing or extra entries).
4. Produce the **Freshness Assessment Table**.
**Outputs:** Freshness Assessment Table (cache, mechanism, max_staleness, actual_staleness, drift_level).
**Ledger emission:** `rcc_freshness_complete` with `{symlinked, ci_synced, scripted, manual, no_mechanism}`

### Phase 5: INTENT
**Purpose:** Classify each caching relationship as intentional, workaround, or accidental.
**Invariant steps:**
1. For each cache, apply the classification rubric:
   - **INTENTIONAL** — The cache is documented (referenced in README, CLAUDE.md, or code comments), has a freshness mechanism, and serves a clear architectural purpose (e.g., local copy for offline builds).
   - **WORKAROUND** — The cache exists because the consumer cannot import across a module boundary (submodule isolation, different org, no shared package). No freshness guarantee. Created to solve a tooling limitation, not an architectural choice.
   - **ACCIDENTAL** — The cache appears to be a copy-paste artifact. No documentation, no freshness mechanism, no clear reason for its existence. Often created during development and never cleaned up.
2. For WORKAROUND caches, document the boundary that prevents direct import: submodule isolation, org boundary, system boundary, or language/runtime limitation.
3. For ACCIDENTAL caches, verify they are not actively consumed (check for imports/reads). Accidental caches with active consumers are reclassified as WORKAROUND.
**Outputs:** Intent Classification Table (cache, classification, boundary_type, justification).
**Ledger emission:** `rcc_intent_complete` with `{intentional, workaround, accidental}`

### Phase 6: RESOLVE
**Purpose:** Propose resolutions to eliminate unnecessary caching and strengthen necessary caching.
**Invariant steps:**
1. For each ACCIDENTAL cache with no active consumers: recommend **DELETE**.
2. For each ACCIDENTAL cache with active consumers: recommend **RECLASSIFY** as WORKAROUND, then apply WORKAROUND resolution.
3. For each WORKAROUND cache:
   - If a shared package or import mechanism could replace it: recommend **IMPORT** (create a shared dependency that both canonical owner and consumer can import).
   - If the boundary cannot be crossed by import: recommend **SYMLINK** (replace copy with symlink if same filesystem) or **SYNC** (add CI job or script to keep cache fresh).
   - If the canonical file could be relocated to a shared location: recommend **CONSOLIDATE**.
4. For each INTENTIONAL cache without a freshness mechanism: recommend **INSTRUMENT** (add sync job or staleness check).
5. For each chain with hop depth >= 2: recommend **FLATTEN** (eliminate intermediate caches; connect terminal cache directly to canonical).
6. Prioritize by: hop depth (deeper = higher priority), consumer count (more consumers = higher priority), staleness (more stale = higher priority).
**Outputs:** Resolution Register (cache, classification, recommendation, priority, effort_estimate).
**Ledger emission:** `caching_chains_analyzed` with `{canonical_count, total_caches, max_hop_depth, workaround_count, accidental_count}`

---

## 3. Outputs

| Output | Phase | Format | Description |
|--------|-------|--------|-------------|
| Canonical Source Inventory | IDENTIFY | Table | All authoritative files with ownership and authority scope |
| Cache Discovery Table | TRACE | Table | Every copy/cache with type classification and size comparison |
| Caching Chain Map | CHAIN | Tree + Table | Full chain from canonical through intermediate to terminal caches |
| Freshness Assessment Table | FRESHNESS | Table | Each cache with mechanism, max staleness, and current drift level |
| Intent Classification Table | INTENT | Table | Each cache classified as INTENTIONAL, WORKAROUND, or ACCIDENTAL |
| Resolution Register | RESOLVE | Prioritized Table | Actionable proposals for each cache (delete, symlink, sync, consolidate, flatten) |

---

## 4. Failure Modes and Recovery

| Failure | Detection | Recovery |
|---------|-----------|---------|
| Canonical source is ambiguous — two files claim authority over the same domain | IDENTIFY phase finds conflicting "source of truth" declarations | Escalate to governance owner; one must be designated canonical and the other reclassified as cache or deprecated |
| Cache content has diverged intentionally — local modifications were made on top of the copy | FRESHNESS phase finds content drift that is not staleness but intentional local extension | Reclassify as DERIVED rather than CACHE; document the delta; recommend extracting the extension into a separate file that overlays the canonical |
| Symlinks broken by submodule operations — `git submodule update` can break cross-submodule symlinks | FRESHNESS phase finds broken symlinks | Replace with CI sync job; symlinks across submodule boundaries are inherently fragile |
| Trace phase produces false positives — files with the same name but unrelated content | TRACE phase flags files that share a name but have <10% key overlap | Apply content similarity threshold; discard candidates below threshold |
| Canonical file is itself a cache of an external source (e.g., registry-v2.json generated from GitHub API) | IDENTIFY phase discovers that the "canonical" file is generated | Extend the chain upstream: external source -> generated canonical -> caches. Document the generation mechanism as the root freshness dependency |

---

## 5. Relationship to Existing SOPs

| SOP | Relationship | Integration Point |
|-----|-------------|-------------------|
| SOP-IV-CBR-001 (Cross-Boundary Reference Mapping) | RCC is a specialized subset of CBR focused exclusively on authoritative config files | CBR Phase 4 (CACHE) generalizes what RCC does; RCC provides deeper analysis for the highest-value files |
| SOP-IV-ICA-001 (Inflated Claims Audit) | Stale caches can cause registry-based claims to be incorrect (e.g., GRADUATED in stale cache, demoted in canonical) | RCC FRESHNESS findings feed ICA as evidence that claims derived from cached registries may be outdated |
| SOP-IV-PAR-001 (Plan Archaeology) | Plan files can reference cached data without knowing it is stale | RCC output identifies which data sources are at staleness risk; PAR can flag plans that depend on those sources |
| Data Integrity Rules (CLAUDE.md) | The "never overwrite production data files wholesale" rule exists because of caching chain risk | RCC formalizes the detection of exactly the patterns that data integrity rules are designed to prevent |
| Governance Rules (Article I) | Article I declares registry.json as single source of truth — RCC verifies this is actually true in practice | RCC IDENTIFY uses Article I declarations as the starting point for canonical file identification |

---

## 6. Protocol Governance

- **Owner:** ORGAN-IV (Taxis)
- **Lifecycle:** REP — needs second run on different target to reach ABSORB
- **Next target:** META-ORGANVM — the canonical home of registry-v2.json and governance-rules.json; running RCC there will trace the full downstream caching chain across all 9 organs and validate that the system's most critical authoritative files have adequate freshness guarantees
