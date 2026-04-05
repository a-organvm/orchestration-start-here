# SOP-IV-SAD-001: Single-Authority Data Model

**Version:** 1.0
**Date:** 2026-04-05
**Scope:** System-wide (ORGAN-IV governs, all organs invoke)
**Lifecycle Stage:** ABSORB (proven on Sovereign Systems engagement, 2026-03-20 to 2026-04-04)
**Provenance:** Extracted from `organvm-iii-ergon/sovereign-systems--elevate-align/docs/process-extraction/2026-04-04-reusable-processes.md`

> Architectural principle SOP: one canonical record per entity, everything else derives — eliminating manual sync between systems by reducing N independent sources to 1 canonical + (N-1) derived views.

---

## 1. When This Protocol Applies

Five invariant conditions, all of which must hold:

| # | Condition | Negative Test (does NOT apply) |
|---|-----------|-------------------------------|
| 1 | An entity is tracked by multiple systems | Entity lives in exactly one system |
| 2 | Systems maintain independent copies (not pointers) | Systems reference a shared record via ID/URL |
| 3 | Manual effort is required to keep copies in sync | Sync is already automated and provably correct |
| 4 | Drift between copies has been observed or is likely | Systems are write-once (no updates after initial creation) |
| 5 | The entity has a clear lifecycle (created, updated, archived) | Ephemeral data with no update semantics |

If conditions 1-2 hold but 3-5 do not, the existing multi-source architecture is likely adequate.
If condition 2 fails (systems already use pointers), this protocol is already in effect — verify the pointer integrity instead.

---

## 2. Protocol Phases

```
ENTITY TRACKED BY N SYSTEMS (N > 1, each claiming truth)
    │
    ├── Phase 1: IDENTIFY      List all systems claiming truth about the entity
    ├── Phase 2: ELECT         Choose one canonical source
    ├── Phase 3: DERIVE        Convert non-canonical systems to read-only derived views
    ├── Phase 4: GATE          Implement single write path with validation
    ├── Phase 5: SYNC          Implement materialization scripts for derived views
    └── Phase 6: AUDIT         Detect and report divergence between canonical and derived
```

### The Pattern

```
Canonical record (one write path)
  ├── written by → gatekeeper script (validates + logs)
  ├── generates → derived view 1 (read-only, materialized by sync script)
  ├── generates → derived view 2 (read-only, materialized by sync script)
  └── referenced by → pointer documents (contain pointers, not copies)
```

### Phase 1: IDENTIFY

**Purpose:** Map the full territory of truth-claims — every system that independently maintains data about a given entity.

**Invariant steps:**
1. Name the entity being governed (e.g., "issue lifecycle state", "project task list", "client contact record")
2. Enumerate every system that stores data about this entity:
   - GitHub Project board fields
   - Local markdown tracking tables
   - IRF (Index Rerum Faciendarum) entries
   - YAML/JSON data files
   - Spreadsheets, Notion databases, external tools
3. For each system, record:
   - **Write frequency** — how often is data updated here?
   - **Read frequency** — how often is data consumed from here?
   - **Data richness** — how many attributes/fields does this copy carry?
   - **Update mechanism** — manual, scripted, automated?
   - **Staleness risk** — how quickly does this copy fall behind reality?
4. Produce an **Authority Map**:
   ```
   Entity: "Issue lifecycle state"
   Systems claiming truth:
     1. GitHub Project board (Status field)     — writes: daily,  reads: hourly, fields: 7, update: manual+script
     2. docs/TRACKING-TABLE.md                  — writes: weekly, reads: daily,  fields: 5, update: manual
     3. IRF entry                               — writes: monthly,reads: weekly, fields: 2, update: manual
   ```

**Outputs:** Authority Map for each governed entity

**Ledger emission:** `identified_authority_conflict` with `{entity, system_count, highest_write_frequency}`

### Phase 2: ELECT

**Purpose:** Choose one canonical source per entity. This is a governance decision, not a technical one.

**Invariant steps:**
1. Apply election criteria in priority order:
   - **Closest to the work** — the system where the actual state change happens (e.g., the board where issues move between columns, not the markdown table that summarizes them)
   - **Most frequently updated** — the system with the highest write frequency is most likely to reflect current reality
   - **Richest data model** — the system carrying the most attributes per record preserves the most information
   - **Most automatable** — the system with the best API/scripting surface for gatekeeper and sync scripts
2. If criteria conflict (e.g., richest model is not the most frequently updated), prefer "closest to the work" — all other criteria are secondary to proximity to the actual state change
3. Document the election decision:
   ```
   Entity: "Issue lifecycle state"
   Canonical source: GitHub Project board
   Reason: Closest to work (transitions happen here), highest write frequency, richest field model
   Runners-up: TRACKING-TABLE.md (frequent reads but derivative), IRF (too coarse-grained)
   ```
4. Gain operator sign-off on the election (this cannot be automated — it is a governance decision)

**Outputs:** Election decision document per entity

**Ledger emission:** `elected_canonical_source` with `{entity, canonical_system, runner_up_count}`

### Phase 3: DERIVE

**Purpose:** Convert every non-canonical system from "independent source of truth" to "derived view" — read-only materializations of canonical data.

**Invariant steps:**
1. For each non-canonical system identified in Phase 1:
   - Remove all manual write paths (or mark them as deprecated/forbidden)
   - Add a header or comment marking it as derived:
     ```markdown
     <!-- DERIVED VIEW — canonical source: GitHub Project board -->
     <!-- Do not edit manually. Regenerate via sync-tracking-table.sh -->
     ```
   - Document which fields in the derived view map to which fields in the canonical record
2. For pointer documents (documents that reference the entity but don't maintain a full copy):
   - Replace inline data with pointers:
     ```markdown
     ## Active Issues
     See [TRACKING-TABLE.md](./TRACKING-TABLE.md) for current state.
     Board: https://github.com/orgs/<org>/projects/<id>
     ```
   - Pointers are cheaper than copies — they never drift
3. Produce a **Derivation Map**:
   ```
   Canonical: GitHub Project board
   Derived:
     1. TRACKING-TABLE.md → materialized by sync-tracking-table.sh (scheduled: daily)
     2. IRF entries         → replaced by pointers to board items
   ```

**Outputs:** Derivation Map, modified non-canonical documents with derived-view headers

**Ledger emission:** `derived_authority` with `{entity, derived_count, pointer_count}`

### Phase 4: GATE

**Purpose:** Implement a single, validated write path into the canonical record.

**Invariant steps:**
1. Build or designate a gatekeeper script/function that:
   - Validates all writes against business rules (e.g., state machine transitions, required fields)
   - Rejects invalid writes with a clear error message
   - Logs every accepted write to an append-only audit trail
   - Is the ONLY mechanism permitted to mutate the canonical record
2. Disable or restrict direct writes:
   - If the canonical source is a GitHub board: all transitions go through `transition-issue.sh`
   - If the canonical source is a YAML file: all mutations go through a dedicated CLI command
   - If the canonical source is a database: all writes go through the application layer (no raw SQL)
3. The gatekeeper emits structured log entries:
   ```yaml
   - entity: issue-42
     action: transition
     from: SPEC
     to: WIP
     timestamp: 2026-04-05T14:30:00Z
     actor: claude
     validation: passed
   ```
4. Test the gate: attempt an invalid write, verify rejection and logging

**Outputs:** Gatekeeper script/function, audit trail, documented write policy

**Ledger emission:** `gated_canonical_source` with `{entity, gatekeeper, audit_trail_path}`

### Phase 5: SYNC

**Purpose:** Implement materialization scripts that regenerate each derived view from the canonical record.

**Invariant steps:**
1. For each derived view identified in Phase 3:
   - Build a sync script that reads the canonical record and writes the derived view
   - The sync script is the ONLY mechanism that writes to the derived view
   - The derived view output is deterministic: same canonical input always produces same derived output
2. Define the sync schedule:
   - **On-demand** — operator runs manually when needed
   - **On-commit** — triggered by changes to the canonical record (CI hook or pre-commit)
   - **Scheduled** — cron/LaunchAgent on a cadence (hourly, daily)
3. The sync script overwrites the entire derived view on each run — it is a full materialization, not a delta update. This eliminates accumulation of drift.
4. Test the sync: modify canonical, run sync, verify derived view reflects the change

**Outputs:** Sync scripts per derived view, sync schedule documentation

**Ledger emission:** `synced_derived_view` with `{entity, view_name, item_count, schedule}`

### Phase 6: AUDIT

**Purpose:** Detect and report divergence between the canonical record and its derived views.

**Invariant steps:**
1. Build an audit script that:
   - Reads the canonical record
   - Reads each derived view
   - Compares field-by-field for each entity
   - Reports any divergence with:
     - Which derived view diverged
     - Which field(s) differ
     - The canonical value vs. the derived value
     - Likely cause (manual edit to derived view, sync script bug, stale schedule)
2. Run the audit on a regular cadence (at least as often as the sync schedule)
3. Divergence should be treated as a defect in the sync pipeline, not as data to reconcile manually
4. Generate `DRIFT-REPORT.md`:
   ```
   Entity: Issue lifecycle state
   Canonical: GitHub Project board
   Derived: TRACKING-TABLE.md
   Divergences found: 3
     - Issue #42: Status canonical=WIP, derived=SPEC (sync not run since transition)
     - Issue #87: Priority canonical=P1, derived=P2 (manual edit to derived view)
     - Issue #103: Missing from derived view entirely (created after last sync)
   Resolution: Re-run sync-tracking-table.sh
   ```

**Outputs:** `DRIFT-REPORT.md`, list of divergences

**Ledger emission:** `audited_authority` with `{entity, divergence_count, resolution}`

---

## 3. Outputs

| Phase | Output | Type | Purpose |
|-------|--------|------|---------|
| IDENTIFY | Authority Map | Analysis | Shows all systems claiming truth per entity |
| ELECT | Election Decision | Governance decision | Names the canonical source with rationale |
| DERIVE | Derivation Map | Architecture doc | Maps canonical to derived views |
| GATE | Gatekeeper + audit trail | Infrastructure | Enforces single write path |
| SYNC | Sync scripts + schedule | Infrastructure | Regenerates derived views |
| AUDIT | Drift Report | Health check | Detects divergence for remediation |

---

## 4. Failure Modes and Recovery

| Failure | Detection | Recovery |
|---------|-----------|----------|
| Operator edits derived view directly | AUDIT phase detects divergence without corresponding canonical change | Re-run sync to overwrite manual edit; reinforce derived-view header as warning |
| Sync script fails silently | AUDIT finds derived views increasingly stale | Add health check to sync (exit code + timestamp file); alert on missed schedule |
| Canonical source becomes unavailable | Gatekeeper cannot reach API | Derived views remain as last-known-good; restore canonical access before accepting new writes |
| Multiple entities elected to same canonical system | Authority Map shows system overload | Split the canonical system or shard by entity type |
| Election decision was wrong (canonical drifts more than derived) | Write frequency in Authority Map reverses over time | Re-run Phase 2 ELECT with updated frequency data; migrate canonical |
| New system introduced that bypasses the model | AUDIT finds entity data in unregistered system | Re-run Phase 1 IDENTIFY, then DERIVE the new system or ELECT it if superior |

---

## 5. Relationship to Existing SOPs

| SOP | Relationship | Integration Point |
|-----|-------------|-------------------|
| `SOP-IV-BGT-001` (Board Governance Toolkit) | Primary consumer | BGT implements this principle: board is canonical, TRACKING-TABLE.md is derived |
| `SOP-IV-XGR-001` (Xenograft Protocol) | Structural parallel | Xenograft's `raw/` directory is the canonical record; all subsequent phases produce derived artifacts |
| `promotion-and-state-transitions` | Governed entity | Promotion status in `registry.json` is the canonical source; seed.yaml promotion fields are derived |
| `document-audit-feature-extraction` | Complementary | Document audit identifies information; this SOP governs where that information lives |
| `drift-detection` | Operationalizes Phase 6 | Existing drift detection tooling can be wrapped as the AUDIT phase implementation |
| `session-self-critique` | Applied within ELECT | Election decisions benefit from self-critique to avoid anchoring on the first candidate |

---

## 6. Protocol Governance

- **Owner:** ORGAN-IV (Taxis)
- **Invocable by:** Any organ, any project — this is an architectural principle, not a tool
- **Core invariant:** If you have N systems claiming truth about the same entity, reduce to 1 + (N-1) derived views. No exceptions. Manual "parity rituals" (keeping two sources in sync by hand) are a protocol violation.
- **Versioning:** SemVer. Changes to the election criteria or derivation rules increment major. New audit checks or sync patterns increment minor.
- **Review cadence:** Whenever a new tracking system is introduced to the workspace, re-run Phase 1 IDENTIFY across all governed entities to check for new authority conflicts.
- **Anti-pattern registry:**
  - "I'll just update both places" — this is the manual parity ritual. It always drifts. Derive instead.
  - "The spreadsheet has extra columns the board doesn't" — the richer system should be canonical. Enrich the board, not the spreadsheet.
  - "We need a backup copy in case the board goes down" — a derived view IS a backup. It just doesn't pretend to be authoritative.
