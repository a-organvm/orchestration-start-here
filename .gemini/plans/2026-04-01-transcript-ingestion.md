# Transcript Ingestion Plan: S48/S49 Full Audit & Recovery

**Date:** 2026-04-01
**Assignment:** Full-transcript ingestion 100% start>finish for S48 (Philosophical Grounding) and S49 (Pipeline/IRF Audit).
**Source:** Claude Code, Gemini CLI, and Codex transcripts.

## Phase 1: Context Extraction

1. **Tool Identification:**
   - **Claude Code:** Handled S48 philosophical grounding (`a-organvm`), memory creation (absorption purity, portals, rendering languages).
   - **Gemini CLI:** Handled S49 pipeline audit, Precision Mode compliance (pruning 78 surplus entries to `research_pool/`), and IRF sync attempts.
   - **Codex / Critic:** Acted as hall-monitor, identifying uncommitted files, YAML regressions (duplicate keys), and IRF structural corruption.

2. **Repo Context:**
   - `a-organvm`: New navigation surface (`CLAUDE.md`), `RELAY.md` S48 update, local memory files.
   - `application-pipeline`: Pipeline state (10 active entries), restoration of Grafana recruiter prep, duplicate key regressions in deadline/deferral blocks, untracked repair scripts.
   - `meta-organvm/organvm-corpvs-testamentvm`: IRF update attempts that resulted in prose corruption, missing completion rows, and ID drift.

3. **Phase Structure:**
   - **[α] Alpha (Decisions):** The 1:1 local-to-remote rule must be strictly enforced. The "soul" (memory) needs remote tracking.
   - **[β] Beta (Implementation):** Restoring the IRF to a syntactically correct state. Stripping duplicate YAML keys.
   - **[ω] Omega (Cleanup):** Validating pipeline with strict parsing. Ensuring no stray repair scripts (`repair_irf_*.py`) linger in the working tree.

## Phase 2: Artifact Production & Execution Strategy

To achieve 100% ingestion and correct the anomalies discovered by the hall-monitor, the following tasks must be executed:

### 1. IRF Integrity Restoration (`meta-organvm`)
- **Fix Prose Corruption:** Remove stray `DONE-` rows and `## Blocked` text injected into the "Update protocol" and "External Index Propagation" sections (around lines 29-35 and 365).
- **Ledger Verification:** Ensure `DONE-IRF-APP-067`, `071`, `072`, and `064` are properly recorded in the `## Completed` table.
- **ID Drift Check:** Verify `IRF-APP-065b` and `066b` are uniquely keyed in the active tables.
- **Commit:** `chore: IRF repair — resolve prose corruption and ID drift from S49`

### 2. YAML Data Health (`application-pipeline`)
- **Duplicate Key Purge:** Remove duplicate `time:` and `timezone:` keys in `prix-ars-electronica.yaml`, `starts-prize.yaml`, `artadia-nyc.yaml`, and `watermill-center.yaml`.
- **Deferral Duplicates:** Remove duplicate `deferral:` blocks in `coinbase-senior-machine-learning-platform-engineer-platform.yaml`, `stripe-staff-software-engineer-stream-compute.yaml`, and `toast-senior-backend-engineer-enterprise-financial-systems.yaml`.
- **Commit Deletions:** Commit the deletion of the scratch repair scripts (`repair_irf_v2.py`, etc.).
- **Commit:** `fix: YAML health — purge duplicate deferral and time keys, clean scratch files`

### 3. Memory Tracking (`a-organvm`)
- **Chezmoi Addition:** Add `~/.claude/projects/-Users-4jp-Workspace-a-organvm/` to `chezmoi` so the autopoietic memory files have a remote backup. (This requires human action on the host, as requested in S48).

### 4. Board Atomization & Intake
- Generate `docs/superpowers/intakes/2026-04-01-s48-s49-board-atomization.md` mapping the remaining unblocked work to the operating board.

## Phase 3: Mobilization
Once this plan is approved and the modifications are executed, we will mobilize the required agents (Codex for surgical YAML/Markdown edits, Gemini for overall verification) to complete the repairs and close the ingestion.
