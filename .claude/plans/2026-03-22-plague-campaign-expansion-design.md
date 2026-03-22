# The Plague Campaign — Contribution Engine Full Expansion

**Date:** 2026-03-22
**Scope:** contrib_engine expansion + 7-workspace activation + campaign roadmap
**Approach:** Fortified C — parallel engine fixes, workspace activation, roadmap creation, logic-ordered

---

## 1. Proven State (Audit Baseline)

### Engine

| Module | Imports | Tests | Functional |
|--------|---------|-------|------------|
| schemas.py | OK | 0 dedicated (tested via others) | Pydantic models work |
| capabilities.py | OK | 5 pass | 8 capabilities, keyword matching works |
| scanner.py | OK | 7 pass | Finds 2 targets offline (contacts + outreach-log only) |
| orchestrator.py | OK | 4 pass | Workspace scaffolding works |
| monitor.py | OK | 9 pass | Discovery works; `_infer_target()` fails on 6/7 seed.yaml formats |
| github_client.py | OK | 0 dedicated | `gh` CLI wrapper, all functions untested |
| cli.py | OK | 0 dedicated | `register_contrib_commands()` not wired to any entry point |

**25 tests total, 0 failures, 0.08s.**

### Workspaces

| Workspace | Target | Stars | Fork | PR | PR State | Blocker |
|-----------|--------|------:|------|---:|----------|---------|
| contrib--adenhq-hive | adenhq/hive | 9,766 | 4444J99/hive | #6707 | OPEN | CI fail — "PR requirements warning" (issue not claimed/assigned) |
| contrib--anthropic-skills | anthropics/skills | 99,735 | 4444J99/skills | #723 | OPEN | Silent — no checks, no reviews, no comments |
| contrib--dbt-mcp | dbt-labs/dbt-mcp | 516 | 4444J99/dbt-mcp | #669 | OPEN | Silent — no checks, no reviews |
| contrib--ipqwery-ipapi-py | ipqwery/ipapi-py | 151 | 4444J99/ipapi-py | #8 | OPEN | Silent — small repo, may need patience |
| contrib--langchain-langgraph | langchain-ai/langgraph | 27,129 | 4444J99/langgraph | #7237 | OPEN | Codex bot review only — no human eyes |
| contrib--primeinc-github-stars | primeinc/github-stars | 0 | 4444J99/github-stars | #39 | OPEN | Missing changeset, Codex bot review only |
| contrib--temporal-sdk-python | temporalio/sdk-python | 1,001 | 4444J99/sdk-python | #1385 | OPEN | **CLA not signed** — hard blocker |

**All 7 have shipped PRs. Zero have human engagement. The engine works mechanically but the protocol layer is missing.**

### What Exists vs What's Missing

| Layer | Exists | Missing |
|-------|--------|---------|
| Data models | Pydantic schemas, lifecycle enum | Campaign model, outreach model, backflow model |
| Discovery | contacts.yaml + outreach-log.yaml scanner | GitHub stars, fork graph, dependency scan, PR history |
| Workspace scaffolding | Full (seed.yaml, README, CLAUDE.md, journal) | CONTRIBUTION-PROMPT.md for 6/7, deep issue identification |
| PR submission | All 7 submitted | Blocker resolution, issue claiming, CLA signing |
| Monitoring | PR state polling, journal writing | Campaign sequencing, priority ordering, next-action prescription |
| Outreach | None | Discord/Slack joins, email threads, issue comments, maintainer engagement |
| Backflow | None | Theory extraction, pattern formalization, narrative publishing, distribution |
| CLI | Functions defined | Not wired to any entry point |

---

## 2. Engine Fixes

### 2a. CLI Entry Point

Create `contrib_engine/__main__.py` as standalone entry:

```python
python -m contrib_engine scan
python -m contrib_engine list
python -m contrib_engine approve <target>
python -m contrib_engine status
python -m contrib_engine monitor
python -m contrib_engine campaign     # NEW
python -m contrib_engine outreach     # NEW
python -m contrib_engine backflow     # NEW
```

Self-contained — no dependency on external `organvm` CLI. `__main__.py` creates its own `ArgumentParser` with its own subparsers using clean names (`scan`, `list`, `approve`, etc.). The existing `cli.py` `register_contrib_commands()` is refactored to accept an optional `prefix` parameter (default `""`) so it can register either as `scan` (standalone) or `contrib-scan` (when embedded in a parent CLI). `__main__.py` calls `register_contrib_commands(subparsers, prefix="")` and adds the new subcommands directly. This preserves backward compatibility if an `organvm` CLI ever wires in `register_contrib_commands(subparsers, prefix="contrib-")`.

### 2b. Monitor Seed.yaml Parsing

`_infer_target()` currently only handles `pr_to_{owner}_{repo}` string format. The 6 newer workspaces use:

```yaml
produces:
  - type: contribution
    consumers: [owner/repo]
```

Fix: parse both formats. Check for string `pr_to_*` pattern first, then check for dict with `type: contribution` and `consumers` list.

### 2c. Scanner Data Source Expansion

Add four new signal sources to `scanner.py`:

1. **GitHub stars** — call existing `who_starred_my_repos()` from github_client (already built, never wired)
2. **Fork graph** — `gh repo list 4444J99 --json name,isFork,parent` to find all forks and their upstream repos
3. **Dependency scan** — read `pyproject.toml` / `requirements.txt` across ORGANVM repos, extract package names, resolve to GitHub repos via PyPI metadata
4. **Active PR scan** — read all `contrib--*/journal/*.md` files, extract PR numbers and target repos

Each source produces `ContributionTarget` entries with appropriate `signal_type` (inbound for stars, outbound for forks, mutual for bidirectional).

---

## 3. New Modules

**Model placement convention:** All new Pydantic models (enums + BaseModel subclasses) are defined in `schemas.py`, following the existing pattern where `ContributionTarget`, `RankedTargets`, `PRState`, `ContributionStatus`, and `ContributionStatusIndex` all live in `schemas.py`. The new module files (`campaign.py`, `outreach.py`, `backflow.py`) import from `schemas.py` and contain only business logic, persistence (`save_*`/`load_*`), and CLI handlers.

**Persistence convention:** Each new module follows the existing `save_*`/`load_*` pattern from `scanner.py` and `monitor.py`: YAML serialization via `yaml.safe_dump()`, loading via `yaml.safe_load()` with `None` fallback on missing files, returning empty index objects. All data files go to `contrib_engine/data/` and are **committed** (living campaign state, not ephemeral).

### 3a. Campaign Sequencer (`contrib_engine/campaign.py`)

Central prescriptive engine. Reads all workspace states + PR states + outreach states and outputs a priority-ordered action queue.

**Campaign phases per workspace:**

```
UNBLOCK -> ENGAGE -> CULTIVATE -> HARVEST -> INJECT
```

- **UNBLOCK**: Fix technical blockers (CLA, CI, changesets, issue claiming)
- **ENGAGE**: First human contact (issue comment, Discord join, email thread)
- **CULTIVATE**: Respond to reviews, iterate code, deepen relationship
- **HARVEST**: PR merged — extract theory, patterns, artifacts
- **INJECT**: Backflow into ORGANVM organs (I, II, V, VI, VII)

**Data model:**

```python
class CampaignPhase(StrEnum):
    UNBLOCK = "unblock"
    ENGAGE = "engage"
    CULTIVATE = "cultivate"
    HARVEST = "harvest"
    INJECT = "inject"

class CampaignAction(BaseModel):
    id: str              # unique identifier (e.g., "temporal-cla", "hive-claim")
    workspace: str
    phase: CampaignPhase
    action: str          # e.g., "Sign CLA at cla-assistant.io"
    priority: int        # 0 = highest
    manual: bool         # requires human action (CLA signing, Discord join)
    automated: bool      # can be done by engine (changeset generation, journal update)
    blocked_by: list[str] = Field(default_factory=list)  # action IDs this depends on
    completed: bool = False
    completed_at: str = ""

    model_config = {"extra": "allow"}

class Campaign(BaseModel):
    name: str = "The Plague"
    started: str
    targets: list[str] = Field(default_factory=list)
    actions: list[CampaignAction] = Field(default_factory=list)

    model_config = {"extra": "allow"}

    def next_actions(self, limit: int = 5) -> list[CampaignAction]:
        """Return top-priority unblocked incomplete actions.

        Resolution: filter actions where completed=False AND all blocked_by
        IDs reference actions with completed=True. If a blocked_by ID is not
        found in the actions list, treat it as unblocked (defensive — allows
        external/manual dependencies to be cleared by removing the ID).
        Sort by priority ascending (0 = highest).
        """
        ...

    def phase_summary(self) -> dict[CampaignPhase, int]:
        """Count workspaces per phase (based on highest incomplete action phase)."""
        ...
```

**Priority ordering algorithm:**

1. Blockers first (P0) — anything preventing PR merge
2. High-visibility targets second (P1) — anthropic 100K stars, langgraph 27K, hive 10K
3. Responsive targets third (P2) — anyone who has commented/reviewed
4. Silent targets last (P3) — investigate before escalating

**CLI:**

```
python -m contrib_engine campaign show        # Current state + next 5 actions
python -m contrib_engine campaign next        # Single next action
python -m contrib_engine campaign complete <id>  # Mark action done
python -m contrib_engine campaign plan        # Generate full action queue from current state
```

### 3b. Outreach Tracker (`contrib_engine/outreach.py`)

Models the relationship lifecycle per target — the human engagement layer that sits above the code layer.

**Data model:**

```python
class OutreachChannel(StrEnum):
    GITHUB_ISSUE = "github_issue"
    GITHUB_PR = "github_pr"
    DISCORD = "discord"
    SLACK = "slack"
    EMAIL = "email"
    TWITTER = "twitter"

class OutreachDirection(StrEnum):
    OUTBOUND = "outbound"
    INBOUND = "inbound"
    MUTUAL = "mutual"

class OutreachEvent(BaseModel):
    channel: OutreachChannel
    date: str
    direction: OutreachDirection
    summary: str
    url: str = ""

    model_config = {"extra": "allow"}

class TargetRelationship(BaseModel):
    workspace: str
    target: str           # owner/repo
    maintainers: list[str] = Field(default_factory=list)
    community_channels: list[dict] = Field(default_factory=list)  # [{type: "discord", url: "...", joined: true}]
    outreach_events: list[OutreachEvent] = Field(default_factory=list)
    issue_claimed: bool = False
    issue_assigned: bool = False
    cla_signed: bool = False
    first_human_contact: str = ""  # date
    relationship_score: int = 0    # 0-100 computed from events

    model_config = {"extra": "allow"}

class OutreachIndex(BaseModel):
    generated: str
    relationships: list[TargetRelationship] = Field(default_factory=list)

    model_config = {"extra": "allow"}
```

**Persisted to:** `contrib_engine/data/outreach.yaml`

**CLI:**

```
python -m contrib_engine outreach show           # All relationships
python -m contrib_engine outreach show <workspace>  # Single relationship detail
python -m contrib_engine outreach log <workspace> <channel> <summary>  # Record an event
python -m contrib_engine outreach check          # Poll GitHub for new interactions
```

### 3c. Backflow Pipeline (`contrib_engine/backflow.py`)

Defines and tracks what flows back into ORGANVM from each external engagement.

**Organ mapping:**

| Organ | ID | Backflow Type | Description |
|-------|----|--------------|-------------|
| ORGAN-I (Theoria) | `theory` | Pattern formalization | State machine mappings, architectural insights, universal patterns extracted |
| ORGAN-II (Poiesis) | `generative` | Visualization artifacts | Diagrams, comparisons, before/after, Mermaid/SVG |
| ORGAN-III (Ergon) | `code` | Reusable code patterns | Patterns extracted from their codebase applicable to ORGANVM |
| ORGAN-V (Logos) | `narrative` | Public essay/post | "How I contributed X to Y" — the story of the engagement |
| ORGAN-VI (Koinonia) | `community` | Relationship artifacts | Discord membership, contacts added, community standing |
| ORGAN-VII (Kerygma) | `distribution` | Announcement content | Tweet, post, newsletter item about merged PR |

**Data model:**

```python
class BackflowType(StrEnum):
    THEORY = "theory"
    GENERATIVE = "generative"
    CODE = "code"
    NARRATIVE = "narrative"
    COMMUNITY = "community"
    DISTRIBUTION = "distribution"

class BackflowStatus(StrEnum):
    PENDING = "pending"
    EXTRACTED = "extracted"
    DEPOSITED = "deposited"
    PUBLISHED = "published"

class BackflowItem(BaseModel):
    workspace: str
    organ: str          # "I", "II", "III", "V", "VI", "VII"
    backflow_type: BackflowType
    title: str
    description: str
    status: BackflowStatus = BackflowStatus.PENDING
    artifact_path: str = ""  # path to the artifact file once created
    deposited_at: str = ""   # date deposited into target organ

    model_config = {"extra": "allow"}

class BackflowIndex(BaseModel):
    generated: str
    items: list[BackflowItem] = Field(default_factory=list)

    model_config = {"extra": "allow"}

    def pending_by_organ(self) -> dict[str, list[BackflowItem]]:
        """Group items where status == PENDING by organ field."""
        ...
```

**Persisted to:** `contrib_engine/data/backflow.yaml`

**CLI:**

```
python -m contrib_engine backflow show           # All backflow items by organ
python -m contrib_engine backflow pending         # What hasn't been extracted yet
python -m contrib_engine backflow add <workspace> <organ> <type> <title>
python -m contrib_engine backflow deposit <id>    # Mark as deposited
```

---

## 4. Workspace Activation

### 4a. CONTRIBUTION-PROMPT.md Generation

Each of the 6 SETUP workspaces needs a deep, target-specific CONTRIBUTION-PROMPT.md modeled on adenhq-hive's. This requires per-workspace:

1. Read target repo's CONTRIBUTING.md, CLAUDE.md, AGENTS.md (where they exist)
2. Explore codebase architecture, test framework, CI setup
3. Identify highest-impact issue where ORGANVM capabilities match
4. Map the fusion — what flows in, what flows back
5. Write the CONTRIBUTION-PROMPT.md with target-specific context

**Target CONTRIBUTING.md availability (verified):**

| Workspace | CONTRIBUTING.md | CLAUDE.md | AGENTS.md |
|-----------|:-:|:-:|:-:|
| adenhq-hive | YES | YES | YES |
| anthropic-skills | NO | NO | NO |
| dbt-mcp | YES | YES | YES |
| ipqwery-ipapi-py | NO | NO | NO |
| langchain-langgraph | NO | YES | YES |
| primeinc-github-stars | NO | NO | YES |
| temporal-sdk-python | NO | NO | NO |

For repos without CONTRIBUTING.md, infer from: README, existing PRs, issue templates, CI config.

### 4b. Priority Ordering for Activation

Logic-ordered by: blocker fixability x visibility x responsiveness x domain overlap.

**Wave 1 — Unblock (immediate, parallel):**
1. `temporal-sdk-python` — Sign CLA (manual, 5 minutes), unblocks merge of a clean PR
2. `adenhq-hive` — Claim issue #6613, get assigned, re-link PR #6707
3. `primeinc-github-stars` — Add changeset file per their process

**Wave 2 — Engage (after unblocking, parallel):**
4. `langchain-langgraph` — 27K stars, has bot review, needs human attention. Join their community, engage on the issue.
5. `anthropic-skills` — 100K stars, your skill system is directly aligned. Investigate review process — this is Anthropic's own repo, high strategic value.
6. `dbt-mcp` — 516 stars, has CONTRIBUTING.md. Strong MCP domain overlap. Follow their process precisely.

**Wave 3 — Cultivate:**
7. `ipqwery-ipapi-py` — Smallest repo (151 stars). Lower priority but easy win. Follow up if silent after 14 days.

---

## 5. Campaign Roadmap Document

Living artifact at `contrib_engine/data/campaign.yaml`. Generated and updated by the campaign sequencer.

### Initial Campaign State

```yaml
# campaign.yaml — flat action list matching Campaign Pydantic model
name: "The Plague"
started: "2026-03-22"
targets:
  - contrib--temporal-sdk-python
  - contrib--adenhq-hive
  - contrib--primeinc-github-stars
  - contrib--langchain-langgraph
  - contrib--anthropic-skills
  - contrib--dbt-mcp
  - contrib--ipqwery-ipapi-py
actions:
  # --- UNBLOCK phase (P0) ---
  - id: temporal-cla
    workspace: contrib--temporal-sdk-python
    phase: unblock
    action: "Sign CLA at cla-assistant.io"
    priority: 0
    manual: true
    automated: false
  - id: temporal-await
    workspace: contrib--temporal-sdk-python
    phase: unblock
    action: "Await CI re-run after CLA"
    priority: 0
    manual: false
    automated: false
    blocked_by: [temporal-cla]
  - id: hive-claim
    workspace: contrib--adenhq-hive
    phase: unblock
    action: "Comment on issue #6613 to claim"
    priority: 0
    manual: true
    automated: false
  - id: hive-await-assign
    workspace: contrib--adenhq-hive
    phase: unblock
    action: "Wait for assignment (24h per CONTRIBUTING.md)"
    priority: 0
    manual: false
    automated: false
    blocked_by: [hive-claim]
  - id: hive-link-pr
    workspace: contrib--adenhq-hive
    phase: unblock
    action: "Update PR #6707 description to reference issue #6613"
    priority: 0
    manual: false
    automated: true
    blocked_by: [hive-await-assign]
  - id: prime-changeset
    workspace: contrib--primeinc-github-stars
    phase: unblock
    action: "Add changeset file per changeset-bot requirements"
    priority: 1
    manual: false
    automated: true
  # --- ENGAGE phase (P1-P2) ---
  - id: langgraph-community
    workspace: contrib--langchain-langgraph
    phase: engage
    action: "Find and join LangChain community channel"
    priority: 2
    manual: true
    automated: false
  - id: langgraph-bump
    workspace: contrib--langchain-langgraph
    phase: engage
    action: "Polite comment on PR #7237 requesting review"
    priority: 2
    manual: false
    automated: true
  - id: anthropic-investigate
    workspace: contrib--anthropic-skills
    phase: engage
    action: "Check if anthropics/skills accepts external PRs (review process)"
    priority: 2
    manual: false
    automated: true
  - id: anthropic-engage
    workspace: contrib--anthropic-skills
    phase: engage
    action: "Comment on PR #723 or related issue"
    priority: 2
    manual: false
    automated: true
    blocked_by: [anthropic-investigate]
  - id: dbt-engage
    workspace: contrib--dbt-mcp
    phase: engage
    action: "Follow up on PR #669 — check if maintainers are active"
    priority: 3
    manual: false
    automated: true
  - id: ipqwery-patience
    workspace: contrib--ipqwery-ipapi-py
    phase: engage
    action: "Wait 14 days from PR submission, then polite bump"
    priority: 4
    manual: false
    automated: false
  # --- CULTIVATE / HARVEST / INJECT phases are trigger-based ---
  # These are not pre-scheduled actions but reactive triggers:
  # CULTIVATE: Any PR receives human review → respond within 24h
  # CULTIVATE: Any PR receives change request → implement within 48h
  # HARVEST: PR merged → extract theory, patterns, artifacts within 72h
  # HARVEST: PR closed → journal lessons learned, assess retry viability
  # INJECT: Harvest complete → deposit into target organs
  # INJECT: All organs deposited → publish narrative (ORGAN-V)
  # INJECT: Narrative published → distribute (ORGAN-VII)
```

---

## 6. Networking Outreach Protocol

Codified at `contrib_engine/outreach_protocol.md` and enforced by the outreach tracker.

### Pre-PR Protocol (for future targets)

1. Star the repo
2. Read CONTRIBUTING.md end-to-end
3. Join community channel (Discord/Slack) if one exists — introduce yourself
4. Identify target issue — comment to claim, wait for assignment
5. If no assignment process: open an issue proposing the contribution
6. Fork, build, test locally against their CI requirements
7. Submit PR referencing the issue

### Active PR Protocol (current state — all 7)

1. Resolve all technical blockers (CLA, changesets, CI failures)
2. If PR has been silent >7 days: polite bump comment ("Checking in — happy to address any feedback")
3. If PR has bot-only reviews: investigate human review process (some repos require maintainer request)
4. Respond to ALL review feedback within 24 hours
5. If changes requested: implement, push, comment confirming
6. If approved but not merged: wait 48h, then polite request

### Post-Merge Protocol

1. Thank maintainers in PR comment
2. Write journal entry documenting the full engagement
3. Update outreach tracker with relationship score
4. Begin backflow extraction:
   - ORGAN-I: What universal pattern did this contribution prove?
   - ORGAN-II: What visualization artifacts were produced?
   - ORGAN-III: What reusable code patterns were learned?
   - ORGAN-V: Draft the narrative ("How ORGANVM contributed X to Y")
   - ORGAN-VI: Record community membership, contacts
   - ORGAN-VII: Prepare distribution content
5. Look for Phase 2 issues in the same repo
6. Stay active in community channel

### Post-Rejection Protocol

1. Journal the rejection with reasoning
2. Assess: was the contribution wrong for the repo, or wrong timing?
3. If fixable: revise and resubmit
4. If fundamental mismatch: archive workspace, extract lessons
5. Do NOT burn the relationship — thank reviewers regardless

---

## 7. File Layout (Post-Expansion)

```
contrib_engine/
  __init__.py            # No export changes needed (modules import directly)
  __main__.py            # NEW — standalone CLI entry point
  schemas.py             # EXPANDED — all new Pydantic models added here
  capabilities.py        # UNCHANGED
  github_client.py       # UNCHANGED
  scanner.py             # EXPANDED — 4 new data sources
  orchestrator.py        # UNCHANGED
  monitor.py             # FIXED — seed.yaml parsing for both formats
  cli.py                 # REFACTORED — prefix parameter for dual-mode registration
  campaign.py            # NEW — campaign sequencer (business logic + persistence)
  outreach.py            # NEW — outreach tracker (business logic + persistence)
  backflow.py            # NEW — backflow pipeline (business logic + persistence)
  outreach_protocol.md   # NEW — codified human engagement protocol
  data/                  # All files COMMITTED (living state, not ephemeral)
    ranked_targets.yaml
    contribution_status.yaml
    campaign.yaml         # NEW — living campaign state
    outreach.yaml         # NEW — relationship index
    backflow.yaml         # NEW — backflow tracking
```

---

## 8. Test Coverage Requirements

| Module | Current Tests | Required New Tests | Notes |
|--------|-------------|-------------------|-------|
| scanner.py | 7 | +8 | 2 per new source (happy path + empty/error): stars, forks, deps, PR history |
| monitor.py | 9 | +3 | New seed.yaml dict format, both formats in one test, missing produces edge |
| campaign.py | 0 | +8 | Phase assignment, priority ordering, blocked_by resolution, next_actions, phase_summary, action completion, plan generation, all-complete edge case |
| outreach.py | 0 | +6 | Event logging, relationship scoring, channel tracking, persistence round-trip, empty index, multiple events |
| backflow.py | 0 | +6 | Item creation, organ routing, status transitions, pending_by_organ, persistence round-trip, empty index |
| cli.py / __main__.py | 0 | +6 | Subcommand routing for all 8 commands, help text, invalid subcommand, prefix parameter, integration test (campaign show with fixture), error on missing data |
| github_client.py | 0 | +3 | Mock `who_starred_my_repos()`, mock `get_repo_info()` timeout, mock `search_issues()` empty |
| cross-module | 0 | +2 | Campaign reads monitor PR state (integration), campaign + outreach interaction |

**Target: 25 existing + 42 new = 67 tests minimum.**

---

## 9. Implementation Order (Logic-Dictated)

Dependencies flow downward — each phase depends on the previous.

### Phase 1: Foundation (engine fixes)
1. Fix `monitor.py` `_infer_target()` for both seed.yaml formats
2. Refactor `cli.py` to accept `prefix` parameter
3. Create `__main__.py` CLI entry point (uses `cli.py` with `prefix=""`)
4. Add all new Pydantic models to `schemas.py` (as defined in Sections 3a-3c)
5. Write tests for all fixes

### Phase 2: New Modules (can run parallel with Phase 3)
6. Build `campaign.py` with phase model and priority ordering
7. Build `outreach.py` with relationship tracking
8. Build `backflow.py` with organ routing
9. Wire new CLI subcommands (campaign, outreach, backflow)
10. Write tests for all new modules

### Phase 3: Scanner Expansion (can run parallel with Phase 2)
11. Wire `who_starred_my_repos()` into scanner
12. Add fork graph scanning
13. Add dependency scanning
14. Add active PR scanning
15. Write github_client mock tests
16. Write tests for new scanner sources

### Phase 4: Campaign Initialization (requires Phase 2 complete)
17. Generate initial `campaign.yaml` from current workspace states
18. Generate initial `outreach.yaml` from PR/journal data
19. Generate initial `backflow.yaml` with pending items for all 7
20. Write `outreach_protocol.md`
21. Write cross-module integration tests

### Phase 5: Workspace Activation
22. Generate CONTRIBUTION-PROMPT.md for temporal-sdk-python
23. Generate CONTRIBUTION-PROMPT.md for langchain-langgraph
24. Generate CONTRIBUTION-PROMPT.md for anthropic-skills
25. Generate CONTRIBUTION-PROMPT.md for dbt-mcp
26. Generate CONTRIBUTION-PROMPT.md for primeinc-github-stars
27. Generate CONTRIBUTION-PROMPT.md for ipqwery-ipapi-py

### Phase 6: Campaign Launch (Manual + Automated)
28. UNBLOCK: Sign temporal CLA (manual)
29. UNBLOCK: Claim hive issue #6613 (manual)
30. UNBLOCK: Add primeinc changeset (automated)
31. ENGAGE: Investigate anthropic review process
32. ENGAGE: Join LangChain community
33. ENGAGE: Follow up on dbt-mcp PR
34. Monitor and respond to all engagement

---

## 10. Success Criteria

| Metric | Current | Target |
|--------|---------|--------|
| PRs with human engagement | 0/7 | 7/7 |
| PRs merged | 0/7 | 3/7 (within 30 days) |
| Technical blockers | 3 | 0 |
| CONTRIBUTION-PROMPTs | 1/7 | 7/7 |
| Backflow items deposited | 0 | 7+ (1+ per organ minimum) |
| Outreach events logged | 0 | 21+ (3+ per workspace) |
| Tests | 25 | 67+ |
| Campaign actions completed | 0 | 20+ |
| Narratives published (ORGAN-V) | 0 | 1+ |
