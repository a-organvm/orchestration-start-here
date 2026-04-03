# Prompt History Analysis: Past Week (March 27 - April 3, 2026)

## Data Sources Extracted

| Source | Records | Format |
|--------|---------|--------|
| Warp Shell Commands | 329 | SQLite |
| Warp AI Queries | 3 | SQLite |
| Claude Plans | 43 | Markdown |
| Codex History | N/A | Binary (inaccessible) |
| zsh History | N/A | Global file only |

## Key Findings

### AI Tool Preference

Primary tools used (shell invocations):
- **other**: 119 (36%)
- **Claude Code**: 91 (27%)
- **Gemini CLI**: 43 (13%)
- **OpenCode**: 26 (7%)
- **Codex**: 26 (7%)
- **OpenClaw**: 17 (5%)
- **Ollama**: 3 (0%)
- **Perplexity**: 2 (0%)
- **Cline**: 1 (0%)
- **Goose**: 1 (0%)

**Insight:** Claude Code dominates (~38% of AI tool invocations), followed by Gemini CLI (~18%) and equal usage of Codex + OpenCode (~11% each).

### Directory Attention

Repositories receiving AI tool time:
- **other**: 96
- **organvm-iv-taxis**: 76
- **4444J99**: 66
- **meta-organvm**: 47
- **organvm-iii-ergon**: 22
- **a-organvm**: 12
- **organvm-i-theoria**: 10

**Insight:** `organvm-iv-taxis` leads with orchestration work, followed by personal workspace `4444J99` and `meta-organvm`.

### Temporal Patterns

**Daily Activity:**
- 2026-03-27: 6 commands
- 2026-03-28: 20 commands
- 2026-03-30: 58 commands
- 2026-03-31: 166 commands
- 2026-04-01: 40 commands
- 2026-04-02: 37 commands
- 2026-04-03: 2 commands

**Insight:** March 31 was the most intensive day (166 commands), indicating a deep work session. Activity drops significantly on weekends (March 29 = missing = Saturday).

**Hourly Pattern:**
- 00:00 - 16 commands
- 01:00 - 8 commands
- 02:00 - 10 commands
- 03:00 - 46 commands
- 04:00 - 30 commands
- 05:00 - 4 commands
- 07:00 - 14 commands
- 08:00 - 35 commands
- 09:00 - 3 commands
- 11:00 - 8 commands
- 12:00 - 12 commands
- 13:00 - 11 commands
- 14:00 - 19 commands
- 15:00 - 27 commands
- 16:00 - 10 commands
- 17:00 - 15 commands
- 18:00 - 10 commands
- 19:00 - 2 commands
- 20:00 - 1 commands
- 21:00 - 7 commands
- 22:00 - 19 commands
- 23:00 - 22 commands

**Insight:** Primary work windows are 03:00-04:00 (late night), 08:00 (morning), and 15:00. Heavy late-night/early-morning usage suggests AI coding as a creative flow state.

### Workflow Observations

1. **Multi-tool orchestration**: You switch between Claude, Codex, Gemini, and OpenCode depending on context
2. **Session chaining**: Common pattern: `gemini` → `claude` → `opencode` in sequence
3. **Orchestration focus**: Heavy activity in `organvm-iv-taxis/orchestration-start-here` suggests building coordination systems
4. **Pipelining**: `application-pipeline` work involves iterative refinement across tools

### Gaps Identified

1. **No Codex access**: History stored in binary LevelDB, cannot analyze prompts
2. **No Gemini CLI prompts**: Only directory metadata, actual prompts not stored
3. **No web chat history**: chatGPT.com conversations not captured
4. **zsh global only**: No per-command directory context in shell history

## Recommendations for Preservation

To build a complete "truth source":

1. **Codex**: Need to use `--print-history` or export feature if available
2. **Gemini CLI**: Enable chat logging or parse `~/.gemini/history/` structure  
3. **Web chats**: Consider manual exports from chatgpt.com
4. **zsh**: Enable `HIST_STAMPS` with directory tracking via `chpwd` hooks

---
*Generated: 2026-04-03T04:24:41.172698*
*Sources: Warp SQLite, Claude Plans, filesystem*
