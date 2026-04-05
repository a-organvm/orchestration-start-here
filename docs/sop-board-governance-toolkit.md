# SOP-IV-BGT-001: Board Governance Toolkit

**Version:** 1.0
**Date:** 2026-04-05
**Scope:** System-wide (ORGAN-IV governs, all organs invoke)
**Lifecycle Stage:** ABSORB (proven on Sovereign Systems engagement, 2026-03-20 to 2026-04-04)
**Provenance:** Extracted from `organvm-iii-ergon/sovereign-systems--elevate-align/docs/process-extraction/2026-04-04-reusable-processes.md`

> Config-driven shell scripts managing a GitHub Project board with state machine validation, audit logging, drift detection, and redundancy analysis — portable by swapping `board.config.json`.

---

## 1. When This Protocol Applies

Six invariant conditions, all of which must hold:

| # | Condition | Negative Test (does NOT apply) |
|---|-----------|-------------------------------|
| 1 | Work is tracked on a GitHub Project board | Tracking lives elsewhere (Notion, spreadsheet, local files) |
| 2 | Board has >20 items | Small boards where manual oversight suffices |
| 3 | Multiple phases or states exist | Flat backlog with no lifecycle transitions |
| 4 | More than one person or agent writes to the board | Single operator, no drift risk |
| 5 | Audit trail is required | Disposable/ephemeral tracking |
| 6 | Redundancy is a known or suspected problem | Fresh board with no history |

If conditions 1-3 hold but 4-6 do not, a manual board review on a cadence is sufficient.
If condition 1 fails, adapt the scripts to the alternative tracking system's API before proceeding.

---

## 2. Protocol Phases

```
NEW PROJECT BOARD (or existing board needing governance)
    │
    ├── Phase 1: CONFIGURE     Create board.config.json with all instance-specific IDs
    ├── Phase 2: SETUP         Instantiate fields, print view filter specs
    ├── Phase 3: POPULATE      Fill required fields on every issue
    ├── Phase 4: GATE          All transitions via transition-issue.sh (state machine enforced)
    ├── Phase 5: SYNC          Materialize board state as read-only markdown table
    ├── Phase 6: AUDIT         Detect drift, incomplete fields, stale items
    └── Phase 7: DEDUPLICATE   Find similar issues, cluster, recommend merges
```

### Phase 1: CONFIGURE

**Purpose:** Create the single configuration file that binds the generic scripts to a specific project board instance.

**Invariant steps:**
1. Retrieve the GitHub Project ID (`PVT_...`) via `gh project list --owner <org>`
2. Retrieve all custom field IDs via `gh api graphql` against the ProjectV2 schema
3. Map the 5-state lifecycle values to their GraphQL option IDs:
   - `GATED` — issue exists but is not yet actionable
   - `SPEC` — requirements/specification in progress
   - `WIP` — active implementation
   - `DONE` — complete, awaiting closure review
   - `CLOSED` — archived, no further action
4. Map the field model to field IDs:
   - **Phase** — which lifecycle phase the issue belongs to
   - **Issue Type** — categorization (bug, feature, task, epic, decision)
   - **Priority** — P0 (critical) through P3 (low)
   - **Status** — the 5-state value from the lifecycle above
   - **Gate Met** — boolean, whether the exit criteria for current state are satisfied
   - **Next Action** — free text, the immediate next step
   - **External Party** — who outside the team this depends on (if any)
5. Record all view IDs for pre-configured board views
6. Write `board.config.json` with all of the above

**Outputs:** `board.config.json`

**Ledger emission:** `configured_board` with `{project_id, field_count, state_count}`

### Phase 2: SETUP

**Purpose:** Instantiate the field schema on the board and generate view filter specifications.

**Invariant steps:**
1. Read `board.config.json`
2. Run `setup-board.sh` which:
   - Verifies all field IDs resolve against the live project
   - Creates any fields that don't yet exist (idempotent)
   - Prints view filter specs for each standard view:
     - **Triage** — `Status = GATED AND Gate Met = false`
     - **Active** — `Status = WIP`
     - **Blocked** — `External Party IS NOT EMPTY AND Status != CLOSED`
     - **Review** — `Status = DONE AND Gate Met = false`
3. Operator manually applies view filters (GitHub Projects API does not support programmatic view creation)

**Outputs:** Verified field schema, printed view filter specs

**Ledger emission:** `setup_board` with `{fields_verified, fields_created, views_specified}`

### Phase 3: POPULATE

**Purpose:** Ensure every issue on the board has all required fields filled.

**Invariant steps:**
1. Query all items on the board via GraphQL
2. For each item, check that all 7 fields have non-empty values
3. Items missing required fields are flagged in a population report
4. Operator fills missing fields (manual or batch script)
5. Re-run population check until 100% field coverage

**Outputs:** Population report, 100% field coverage

**Ledger emission:** `populated_board` with `{total_items, items_complete, items_incomplete}`

### Phase 4: GATE

**Purpose:** Enforce the state machine on every status transition, logging each change to an append-only audit trail.

**Invariant steps:**
1. All state transitions go through `transition-issue.sh <issue-number> <target-state>`
2. The script validates the transition against the state machine:
   ```
   GATED → SPEC        (allowed)
   SPEC  → WIP         (allowed)
   SPEC  → GATED       (allowed: send-back)
   WIP   → DONE        (allowed)
   WIP   → SPEC        (allowed: send-back)
   DONE  → CLOSED      (allowed)
   DONE  → WIP         (allowed: reopen)
   *     → *           (all other transitions: REJECTED)
   ```
3. If valid: update the field value via GraphQL, append to `audit-log.yaml`:
   ```yaml
   - issue: 42
     from: SPEC
     to: WIP
     timestamp: 2026-04-05T14:30:00Z
     actor: claude
   ```
4. If invalid: print rejection reason, do not mutate board state, log the rejected attempt

**Outputs:** Updated board state, append-only `audit-log.yaml`

**Ledger emission:** `transitioned_issue` with `{issue, from_state, to_state, valid}`

### Phase 5: SYNC

**Purpose:** Materialize the current board state as a read-only markdown tracking table.

**Invariant steps:**
1. Run `sync-tracking-table.sh`
2. Query all board items with full field values via GraphQL
3. Generate `TRACKING-TABLE.md`:
   ```markdown
   | # | Title | Phase | Type | Priority | Status | Gate | Next Action | External |
   |---|-------|-------|------|----------|--------|------|-------------|----------|
   | 1 | Setup DNS records | Foundation | task | P1 | WIP | false | Waiting on registrar | GoDaddy |
   ```
4. Write the table to the designated location (repo `docs/` or project root)
5. The table is **read-only** — it is a derived view of the board, not an independent source of truth

**Outputs:** `TRACKING-TABLE.md` (derived, read-only)

**Ledger emission:** `synced_tracking_table` with `{item_count, timestamp}`

### Phase 6: AUDIT

**Purpose:** Detect drift between intended and actual board state.

**Invariant steps:**
1. Run `audit-board.sh`
2. Check for:
   - **Field drift** — Status says WIP but Gate Met is true (should have transitioned to DONE)
   - **Incomplete fields** — any of the 7 required fields empty
   - **Stale items** — items in WIP with no update in >7 days
   - **Orphaned items** — items in GATED with no Next Action
   - **Audit log gaps** — items whose current state has no corresponding audit log entry
3. Generate `AUDIT-REPORT.md` with findings grouped by severity:
   - **CRITICAL** — state machine violations (items in states they couldn't have reached via valid transitions)
   - **WARNING** — drift, staleness, incomplete fields
   - **INFO** — orphaned items, minor hygiene issues

**Outputs:** `AUDIT-REPORT.md`

**Ledger emission:** `audited_board` with `{critical_count, warning_count, info_count}`

### Phase 7: DEDUPLICATE

**Purpose:** Find duplicate or near-duplicate issues and recommend merges.

**Invariant steps:**
1. Run `detect-redundancy.sh`
2. Compare all issue titles and descriptions pairwise using:
   - Exact title match (after lowercasing and stripping punctuation)
   - Substring containment (one title is a substring of another)
   - Semantic similarity (embedding cosine > 0.85, if embeddings available; otherwise Jaccard on word sets > 0.6)
3. Cluster matches into redundancy groups
4. For each cluster, recommend:
   - **MERGE** — genuinely duplicate, consolidate into the item with the most detail
   - **LINK** — related but distinct, add cross-references
   - **KEEP** — false positive, different concerns despite surface similarity
5. Generate `REDUNDANCY-REPORT.md`

**Outputs:** `REDUNDANCY-REPORT.md` with clusters and recommendations

**Ledger emission:** `detected_redundancy` with `{clusters_found, items_mergeable, items_linked}`

**Field-tested result:** Styx board (504 items) — found 55 redundancy clusters, ~75 mergeable items.

---

## 3. Outputs

| Phase | Output | Type | Location |
|-------|--------|------|----------|
| CONFIGURE | `board.config.json` | Config | Project root |
| SETUP | View filter specs | Printed | stdout |
| POPULATE | Population report | Report | stdout or `docs/` |
| GATE | `audit-log.yaml` | Append-only log | Project root |
| SYNC | `TRACKING-TABLE.md` | Derived view (read-only) | `docs/` |
| AUDIT | `AUDIT-REPORT.md` | Report | `docs/` |
| DEDUPLICATE | `REDUNDANCY-REPORT.md` | Report | `docs/` |

---

## 4. Failure Modes and Recovery

| Failure | Detection | Recovery |
|---------|-----------|----------|
| GraphQL field IDs stale (GitHub changed them) | SETUP phase verification fails | Re-run CONFIGURE to refresh `board.config.json` |
| State machine bypass (manual board edit) | AUDIT detects state without audit log entry | Log the gap, backfill audit entry with `actor: manual`, re-gate |
| Redundancy false positives flood report | DEDUPLICATE produces >50% KEEP recommendations | Raise similarity threshold, add domain stop-words |
| Sync table diverges from board | Manual edit to `TRACKING-TABLE.md` | Delete and re-generate — it is a derived view, never a source |
| Rate limiting on GraphQL queries | HTTP 429 or 502 from GitHub API | Implement exponential backoff with >=2s base delay |
| Board exceeds 1000 items | Pagination required in all queries | Implement cursor-based pagination in all scripts |

---

## 5. Relationship to Existing SOPs

| SOP | Relationship | Integration Point |
|-----|-------------|-------------------|
| `SOP-IV-SAD-001` (Single-Authority Data Model) | Governing principle | Board is the canonical record; `TRACKING-TABLE.md` is a derived view |
| `SOP-IV-SBM-001` (Spiral Build Methodology) | Phase model consumer | Board phases (Foundation, First Pass, Return, Second Pass, Completion) map to spiral waves |
| `SOP-IV-XGR-001` (Xenograft Protocol) | Upstream supplier | Xenograft Phase 7 strikes become board issues |
| `promotion-and-state-transitions` | Conceptual parallel | Both enforce state machines; BGT governs project boards, promotion governs repo lifecycle |
| `session-self-critique` | Applied within AUDIT | Audit phase is a structural self-critique of board hygiene |
| `document-audit-feature-extraction` | Complementary | Board audit is operational; document audit is content-level |

---

## 6. Protocol Governance

- **Owner:** ORGAN-IV (Taxis)
- **Invocable by:** Any organ managing a GitHub Project board
- **Portability:** Scripts are the process; `board.config.json` is the instance. Swap config = new project, same process.
- **Versioning:** SemVer. New required fields increment major. New scripts or optional checks increment minor.
- **Review cadence:** After every 3rd board reaches >200 items, review state machine transitions and audit thresholds for adequacy.
- **Script inventory:**
  - `transition-issue.sh` — gatekeeper with state machine validation + audit log
  - `sync-tracking-table.sh` — materializes board state into read-only markdown
  - `audit-board.sh` — detects drift and incomplete fields
  - `detect-redundancy.sh` — finds duplicate/near-duplicate issues
  - `setup-board.sh` — instantiates fields + prints view specs from config
