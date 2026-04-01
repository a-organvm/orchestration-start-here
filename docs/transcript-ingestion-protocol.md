# Transcript Ingestion Protocol

**Date:** 2026-04-01
**Updated:** 2026-04-01
**Purpose:** Standardize the process of ingesting raw AI session transcripts into the orchestration system

## Supported Tools

| Tool | CLI Name | Session Pattern |
|------|----------|-----------------|
| Codex | `codex` | `›` prompts, `❯` commands |
| Gemini CLI | `gemini` | `❯` prompts, tool output blocks |
| Claude Code | `claude --chrome` | `❯` prompts, `⏺` markers |

## Input

Raw transcript containing:
- Command history (tool prompts and outputs)
- File operations (explore, read, list, search, edit)
- GitHub mutations (issue create/edit/close, project updates)
- Session close markers

## Output Artifacts

| Artifact | Location | Purpose |
|----------|----------|---------|
| Plan file | `.codex/plans/YYYY-MM-DD-{slug}.md` | Dated audit trail |
| Intake doc | `docs/superpowers/intakes/YYYY-MM-DD-{name}.md` | Normalized source material |
| Memory update | `.claude/projects/.../memory/` | Persistent memory entries |
| GitHub issues | org/repo/issues | Operational work items |
| Board items | GitHub Project | Mapped to operating board |
| IRF update | `INST-INDEX-RERUM-FACIENDARUM.md` | Universal work registry |

## Standardized Ingestion Flow

### Phase 1: Context Extraction

From the transcript, extract:

1. **Tool identification** — which CLI was used?
2. **Source handoff** — what was the input task?
   - Named handoff (e.g., "Maddie Spiral Path")
   - File references
   - Status indicator
3. **Repo context** — which repo was targeted?
   - Working directory
   - Seed/AGENTS.md references
   - Git remote
4. **Phase structure** — what phases are in play?
   - α (alpha) — decisions, blockers
   - β (beta) — implementation
   - γ (gamma) — backlog/future
   - ω (omega) — cleanup/corrections

### Phase 2: Artifact Production

1. **Plan file** (always)
   - Location: `.codex/plans/YYYY-MM-DD-{assignment-slug}.md`
   - Contains: date, repo, context, work plan, expected outputs

2. **Intake normalization** (if new source material)
   - Location: `docs/superpowers/intakes/YYYY-MM-DD-{name}-board-atomization.md`
   - Contains: source verification, what changed, existing issue map, new issues justified, recommended board outcome, remaining dependencies

3. **Memory entries** (if new patterns/discoveries)
   - Location: `.claude/projects/-Users-4jp-Workspace-.../memory/`
   - Contains: new patterns, converged findings, relationship updates

4. **IRF propagation** (if work completed/discovered)
   - Run `update_irf.py` if session discovered new items
   - Map to existing IRF IDs or create new domain entries

### Phase 3: GitHub Mutation

Standard operations:

| Operation | When Used | Command Pattern |
|-----------|-----------|------------------|
| Close stale | Intake satisfied | `gh issue close #N --reason completed` |
| Update in place | Scope refresh | `gh issue edit #N --title "..." --body-file -` |
| Create new | New workstream | `gh issue create --title "..." --label ... --project ... --body-file -` |
| Project add | Board mapping | `--project "$project_title"` on create |

### Phase 4: Hall-Monitor Audit

Per session close protocol:

1. **Git parity check**: `(local):(remote) = 1:1`
   - `git status --short`
   - `git add . && git commit && git push` if needed
2. **Precision mode check** (application-pipeline only):
   - Max 10 actionable entries in `pipeline/active/`
   - Max 1 per organization
   - Move surplus to `pipeline/research_pool/`
3. **IRF update**: Run `update_irf.py` if new items discovered
4. **Memory sync**: Update project memory index if new entries created

### Phase 5: Verification

- `gh issue list --limit 30 --state all --json number,title,state,labels,url`
- `gh project item-list PROJECT --owner ORG --format json`
- Compare against recommended board outcome

## Standard Labels

| Label | Use Case |
|-------|----------|
| roadmap | Primary tracking label |
| P0 | Launch critical |
| P1 | This sprint |
| P2 | Next sprint |
| P3 | Backlog |
| client | Requires Maddie decision |
| infra | Infrastructure/deploy |
| content | Content/copy work |
| spiral | Spiral-specific |
| bug | Something isn't working |

## Standard Phase Prefix

- `[α.N]` — Alpha decisions/blockers
- `[β.N]` — Beta implementation
- `[γ.N]` — Gamma backlog
- `[ω.N]` — Omega cleanup

## Session Close Protocol

1. All local artifacts created
2. All GitHub mutations executed
3. Git parity verified (commit + push if needed)
4. IRF updated if new items discovered
5. Board verified (item count matches expected)
6. Summarize: what changed, what still blocked, where artifacts live
7. Close with relay-switch marker

## Example Transcripts Ingested

### 1. Codex — Maddie Spiral Path (2026-04-01)

**Input:** 127-file handoff from Maddie (health/, mindset/, business/, water/, etc.)

**Extracted phases:**
- α.4 — Node architecture lock
- α.5 — Media access verification
- β.5 — V5/V6 prototype merge
- β.6 — Editorial review
- β.7 — Water Hub placement
- β.8 — Video hosting decision
- γ.3 — Inner Child Book packaging
- γ.4 — Creature Selves decision

**Outputs produced:**
- `.codex/plans/2026-04-01-maddie-spiral-orchestration-assignment.md`
- `docs/superpowers/intakes/2026-04-01-maddie-spiral-path-board-atomization.md`
- 8 new GitHub issues (#13-#20)
- Project 5 updated from 11 items to 19 items

### 2. Gemini CLI — Application Pipeline Hall-Monitor (2026-04-01)

**Input:** Hall-monitor audit prompt + IRF update protocol

**Key actions:**
- Found Precision Mode violation: 88 actionable entries (max 10)
- Pruned 78 surplus entries (Coinbase, Toast, Samsara) back to research_pool/
- Executed `update_irf.py` to propagate 17 OpenClaw vacuums
- Created IRF-APP-064, IRF-DOM-022 through IRF-DOM-025
- Git commit + push to restore 1:1 parity

**Outputs produced:**
- Pipeline now compliant: 10 entries, 1 per org
- IRF synced with meta-organvm
- Stripe "location: N/A" vacuums identified (9 entries)

### 3. Claude Code — Sibling Container Protocol (2026-04-01)

**Input:** New sibling container with Maddie info dump

**Key actions:**
- Received PDF intake + full HTML V5 content (6942 lines)
- Ingested 6 content folders concurrently (~360K words)
- Discovered 13-vs-14 node structural divergence
- Identified 13 editorial flags + 3 standalone products

**Outputs produced:**
- 527-line handoff at `docs/handoff-maddie-spiral-path-2026-04-01.md`
- Memory entries indexed (2 created)
- Sibling relay protocol acknowledged
